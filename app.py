#!/usr/bin/env python3
"""Provenance Guard: local estimates, durable audit events, and appeals.

POST /ping        unchanged starter control route
POST /submit      validate, score with two mechanisms, and persist a decision
POST /appeal      append a review request without changing the original decision
GET /content/<id> retrieve original decision, appeals, and current review status
GET /log          retrieve audit events
GET /health       report model and storage readiness

Run with `python app.py`; see RUNNING.md for setup and verification.
"""

import uuid
import hashlib
import re
import threading
from werkzeug.exceptions import BadRequest

import detector
import stylometry
import scoring

from flask import Flask, jsonify, request

import audit
import config

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = config.MAX_BODY_BYTES
_inference_slot = threading.BoundedSemaphore(1)


# ── Rate limiting — UNIT 8 ────────────────────────────────────────────────────
# Off until you turn it on. In unit 8, Milestone 1:
#
#   1. Set RATE_LIMITING_ENABLED = True in config.py (or AI201_RATE_LIMITS=1)
#   2. Choose your numbers there
#   3. Uncomment the @limiter.limit(...) line on /submit below
#
# The order doesn't matter. While limiting is off, that decorator is a no-op
# that quietly does nothing, so uncommenting it early costs you nothing — but
# it also means no 429 until you've done step 1.
#
# The storage backend is preconfigured, which stops Flask-Limiter printing a
# warning on every start. In-memory is right for one laptop and wrong for
# anything real — a restart forgets every count.

class _LimiterOff:
    """
    Stands in for the real limiter while rate limiting is off.

    It makes @limiter.limit(...) a decorator that returns the route
    untouched, so uncommenting the line before you flip the setting is
    harmless instead of a crash on startup.
    """

    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()
if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def rate_limit_key():
        """
        Who a request counts against.

        Falling back to the caller's address is the easy version. Unit 8's
        stretch asks about per-creator limits instead — and the difference
        matters: one script can look like a thousand callers, and one household
        can look like one.
        """
        payload = request.get_json(silent=True)
        # A body that parses as JSON but isn't an object — a bare list or
        # string — has no .get. Without this guard the key function raises
        # BEFORE the route runs, and a malformed request becomes a 500 that
        # looks like your handler crashed when your handler never ran.
        if not isinstance(payload, dict):
            return get_remote_address()
        creator = payload.get("creator_id")
        return creator if isinstance(creator, str) and creator.strip() else get_remote_address()

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        """
        A rejected request still leaves a trace.

        ⚠️ An attack that shows up only as an absence is one you'll never find.
        """
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            payload = {}
        audit.log_rejection(
            creator_id=payload.get("creator_id", "unknown"),
            reason="rate_limited",
            limit=str(exc.description),
        )
        return jsonify({
            "error": "rate_limited",
            "message": "Too many submissions. Try again shortly.",
            "limit": str(exc.description),
        }), 429


# ── The worked example. Already works. Don't edit. ────────────────────────────

@app.post("/ping")
def ping():
    """
    Everything a route needs, in six lines.

    JSON arrives as a dict. You pull things out of it. You return a dict and
    the framework turns it into a response. That's the whole idea.
    """
    payload = request.get_json(silent=True) or {}
    return jsonify({
        "ok": True,
        "you_sent": payload.get("message"),
        "service": "provenance-guard",
    })


@app.get("/health")
def health():
    """Is the service up, and has the model been downloaded yet?"""
    import detector

    loaded = detector._model is not None
    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "log_entries": len(audit.read_entries()),
    })



# ── Validated project endpoints ──────────────────────────────────────────────

class APIError(Exception):
    def __init__(self, code, message, status=400):
        self.code, self.message, self.status = code, message, status


@app.errorhandler(APIError)
def api_error(exc):
    if 400 <= exc.status < 500:
        try:
            audit.log_rejection("unknown", exc.code, endpoint=request.path, http_status=exc.status)
        except OSError:
            return jsonify(error="audit_unavailable", message="The audit store is unavailable. Try again later."), 503
    return jsonify(error=exc.code, message=exc.message), exc.status


@app.errorhandler(413)
def body_too_large(exc):
    return api_error(APIError("body_too_large", "Request body exceeds 65,536 bytes.", 413))


@app.errorhandler(OSError)
def storage_error(exc):
    app.logger.error("Audit storage error: %s", type(exc).__name__)
    return jsonify(error="audit_unavailable", message="The audit store is unavailable. Try again later."), 503


def json_object():
    if not request.is_json:
        raise APIError("unsupported_media_type", "Send an application/json request.", 415)
    try:
        payload = request.get_json()
    except BadRequest as exc:
        raise APIError("invalid_json", "The body must contain valid JSON.") from exc
    if not isinstance(payload, dict):
        raise APIError("invalid_body", "The JSON body must be an object.")
    return payload


def required_string(payload, field, maximum):
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise APIError("invalid_" + field, f"{field} must be a nonblank string.")
    # Reject invalid Unicode scalars before hashing, tokenizing, or logging.
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise APIError("invalid_" + field, f"{field} must be valid Unicode text.") from exc
    if len(value) > maximum:
        raise APIError("oversized_" + field, f"{field} exceeds {maximum} characters.", 413)
    return value


def valid_content_id(value):
    if not isinstance(value, str):
        raise APIError("invalid_content_id", "content_id must be a UUID string.")
    try:
        return str(uuid.UUID(value))
    except (ValueError, AttributeError) as exc:
        raise APIError("invalid_content_id", "content_id must be a UUID string.") from exc


def content_record(content_id):
    events = audit.entries_for(content_id)
    decisions = [e for e in events if e.get("event") == "decision" or e.get("status") == "decided"]
    if not decisions:
        raise APIError("not_found", "No submission exists for that content_id.", 404)
    return decisions[0], [e for e in events if e.get("event") == "appeal"]


@app.post("/submit")
# @limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day")
def submit():
    payload = json_object()
    text = required_string(payload, "text", config.MAX_TEXT_CHARS)
    creator = required_string(payload, "creator_id", 128)
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,128}", creator):
        raise APIError("invalid_creator_id", "creator_id may contain letters, digits, underscore, dot, or hyphen.")
    style = stylometry.style_details(text)
    if style["word_count"] < 3:
        raise APIError("insufficient_text", "Provide at least three words; short passages may remain unsure.", 422)
    # A durable decision is required; fail before expensive inference on corrupt storage.
    audit.read_entries()
    if not _inference_slot.acquire(blocking=False):
        raise APIError("detector_busy", "Another text is being scored. Try again shortly.", 503)
    try:
        model = detector.signal_details(text)
    except detector.DetectorUnavailable as exc:
        app.logger.error("Detector unavailable: %s", type(exc).__name__)
        raise APIError("detector_unavailable", "The local model is unavailable. Try again later.", 503) from exc
    except (ValueError, RuntimeError, OverflowError) as exc:
        app.logger.error("Detector scoring failed: %s", type(exc).__name__)
        raise APIError("detector_unavailable", "The local model could not score this text.", 503) from exc
    finally:
        _inference_slot.release()
    limitations = []
    if style["word_count"] < config.MIN_CONFIDENT_WORDS:
        limitations.append("fewer_than_40_words")
    if style["sentence_count"] < config.MIN_CONFIDENT_SENTENCES:
        limitations.append("fewer_than_3_sentences")
    if model["truncated"]:
        limitations.append("only_first_400_tokens_scored")
    try:
        score = scoring.decision_score(model["model_score"], style["style_score"], weak_evidence=bool(limitations))
        guess, label = scoring.score_to_label(score)
        disagreement = abs(model["model_score"] - style["style_score"]) > config.DISAGREEMENT_THRESHOLD
    except ValueError as exc:
        raise APIError("invalid_signal", "A signal or scoring configuration was invalid.", 503) from exc
    content_id = str(uuid.uuid4())
    response = {
        "content_id": content_id, "guess": guess, "confidence": score,
        "confidence_kind": "uncalibrated_ai_likeness", "combined_score": score,
        "model_score": model["model_score"], "style_score": style["style_score"],
        "label": label, "status": "decided", "scoring_version": config.SCORING_VERSION,
        "evidence": {"model": model, "style": style, "limitations": limitations,
                     "signals_disagree": disagreement},
        "review_available": True,
    }
    audit.log_decision(
        content_id, creator, guess=guess, model_score=model["model_score"],
        style_score=style["style_score"], combined_score=score, label=label,
        event="decision", confidence=score, confidence_kind=response["confidence_kind"],
        scoring_version=config.SCORING_VERSION, evidence=response["evidence"],
        text_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(), text_length=len(text),
    )
    return jsonify(response), 201


@app.post("/appeal")
def appeal():
    payload = json_object()
    content_id = valid_content_id(payload.get("content_id"))
    reasoning = required_string(payload, "reasoning", config.MAX_REASONING_CHARS)
    decision, _ = content_record(content_id)
    # Creator comes from the original record, never from the caller's appeal body.
    audit.log_appeal(
        content_id, decision["creator_id"], reasoning,
        **{key: decision.get(key) for key in ("guess", "model_score", "style_score", "combined_score", "label")},
    )
    return jsonify(
        content_id=content_id, status="under_review",
        message="Your review request has been recorded. The original estimate is preserved; no automatic reclassification has been made.",
    )


@app.get("/content/<content_id>")
def get_content(content_id):
    content_id = valid_content_id(content_id)
    decision, appeals = content_record(content_id)
    return jsonify(content_id=content_id, status="under_review" if appeals else "decided",
                   original_decision=decision, appeals=appeals)

# ── Already works ─────────────────────────────────────────────────────────────

@app.get("/log")
def get_log():
    """
    The audit log, most recent last.

        curl "http://127.0.0.1:5000/log?limit=10"

    You need this in unit 8 to paste entries into your README, and you need it
    now to see whether your logging is actually working.
    """
    raw_limit = request.args.get("limit")
    if raw_limit is not None and (not raw_limit.isascii() or not raw_limit.isdigit() or len(raw_limit) > 7):
        raise APIError("invalid_limit", "limit must be a nonnegative integer up to 1,000,000.")
    limit = int(raw_limit) if raw_limit is not None else None
    if limit is not None and limit > 1_000_000:
        raise APIError("invalid_limit", "limit must be at most 1,000,000.")
    entries = audit.read_entries(limit=limit)
    return jsonify({"count": len(entries), "entries": entries})


def main():
    print(f"Provenance Guard on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off (unit 8)'}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    print()
    print("Check it's alive:")
    print(f'  curl -X POST http://{config.HOST}:{config.PORT}/ping \\')
    print('    -H "Content-Type: application/json" \\')
    print("    -d '{\"message\": \"hello\"}'")
    print()
    # debug=True hands out an interactive debugger, so it's local-only — see config.py
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
