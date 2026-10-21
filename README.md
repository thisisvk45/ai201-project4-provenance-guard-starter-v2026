# Provenance Guard

An English-writing provenance estimate with uncertainty and an appeal path. Built from the CodePath AI201 Unit 7 starter; this same fork will be used in Unit 8.

## What This Does

The design was recorded before implementation and results in commit `9d6261c`. The implemented request path is:

1. Validate JSON, field types, size limits, and a caller-supplied creator identifier.
2. Obtain a GPT-2 predictability score locally, retaining token coverage metadata.
3. Independently compute sentence-length variation, vocabulary variety, and punctuation density.
4. Combine model/style scores at 0.70/0.30. If their difference exceeds 0.50, shrink the result halfway toward 0.50.
5. For fewer than 40 words, fewer than three sentences, or truncated model input, shrink again to `0.5 + 0.25 * (score - 0.5)`, which always lands in the unsure band.
6. Map to human (`<=0.25`), unsure (`>0.25` and `<0.80`), or AI (`>=0.80`), persist the decision, and return its identifier.
7. Append appeals as `under_review` events without overwriting the original. Derive current status from the log, including after restart.

The expensive error is a human writer receiving an AI label. The system never removes writing or bans a creator. A false-positive score of 0.86 yields a qualified label and a review route, not a finding of misconduct.

### Endpoint contract

| Endpoint | Input | Success | Errors |
|---|---|---|---|
| `POST /submit` | JSON: `text`, `creator_id` | 201: `content_id`, `guess`, `confidence`, `label`, both signal scores, `combined_score`, `status`, evidence metadata | 400 invalid JSON/fields, 415 media type, 413 size, 422 too little text, 503 detector/storage unavailable |
| `POST /appeal` | JSON: UUID `content_id`, nonblank `reasoning` | 200: `content_id`, `status=under_review`, confirmation | 400 invalid input, 404 unknown, 413 size, 503 storage unavailable |
| `GET /content/<id>` | UUID path parameter | 200: original decision, current status, appeal history | 400 invalid UUID, 404 unknown, 503 storage unavailable |
| `GET /log` | optional nonnegative integer `limit` | audit events, oldest first | 400 invalid limit, 503 storage unavailable |
| `GET /health` | none | startup/model/log state | 503 unreadable audit store |
| `POST /ping` | starter example | unchanged starter response | unchanged starter behavior |

Declared stretch before implementation: `GET /content/<id>`. No third signal or verified-human credential is claimed. Unit 8 rate limiting and attacks are left for that unit.

Run locally with Python 3.12: `python3.12 -m venv .venv`, activate it, install `requirements.lock`, then `PORT=5057 python app.py`. See [RUNNING.md](RUNNING.md) for complete setup, model download, curl examples, and verification. No API key is needed.

The service is a single-process local prototype. Creator IDs are caller-supplied and unauthenticated; knowing a content ID is enough to request its review. An appeal records a review request, but there is no human-review resolution workflow. JSONL storage is locked across threads and flushed with `fsync` before success, not coordinated across processes. Lookups scan the log; this is not a production database. Decisions store text hashes and lengths rather than raw text, but appeal reasons and creator IDs are stored. Use only test data when sharing logs. Repeating a submission creates a new ID.

## Signals and Scoring

The combining function is `scoring.py::combine_signals`; weights and thresholds live in `config.py`. `confidence` means **uncalibrated AI-likeness**, not a probability of cheating or certainty in the returned label. Zero points toward human-like patterns; one toward AI-like patterns.

GPT-2 measures contextual token predictability, not authorship. Plain human writing can look predictable; unusual AI prose can look surprising. The style signal measures surface form, not meaning. Editing punctuation, sentence breaks, or spelling can move it without changing origin. Different mechanisms do not establish statistical independence.

Style implementation: coefficient of variation of sentence word counts; length-weighted mean type/token ratio in consecutive 50-word windows; Unicode punctuation characters per word. Normalize AI-oriented components as `max(0, 1-CV)`, `clip((0.9-TTR)/0.5)`, and `max(0, 1-density/0.3)`, then combine at 0.55/0.30/0.15. These are transparent heuristics, not fitted probabilities. Fewer than three sentences or 40 words makes style neutral (0.5); the measurements are still reported.

The supplied GPT-2 rule is `1 / (1 + exp(1.6 * (log(perplexity) - log(45))))`, rounded to four decimals. The implementation evaluates it in a numerically bounded form. No classifier training or threshold fitting was performed. The final score is rounded to six decimals and both `confidence` and `combined_score` carry that same value. Severe signal disagreement means `abs(model-style) > 0.50`; `signals_disagree` reports that condition. This differs from merely falling on opposite sides of 0.5.

The tokenizer counts the full accepted input, but GPT-2 scores at most its first 400 tokens. Any unscored tail forces an unsure label. Stylometry inspects the full text; sentence boundaries are heuristic and abbreviations may be miscounted. Unicode word/punctuation handling does not make this an evaluated multilingual detector. Scoring has only been exercised on the English development fixtures below.


## Label Variants

| Band | Exact reader-facing text |
|---|---|
| `0 <= score <= 0.25` | This writing shows patterns often found in human writing. This automated estimate does not verify who wrote it. You can request a review if it seems wrong. |
| `0.25 < score < 0.80` | We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review. |
| `0.80 <= score <= 1` | This writing shows patterns often found in AI-generated text. This is an automated estimate, not proof of authorship. If this seems wrong, you can request a review. |

## Sample Run

### Verification results

The final HTTP verification used real local GPT-2 inference on nine frozen fixtures plus one explicit repeat, then appealed all ten decisions and restarted the service in a fresh process. Full requests, responses, elapsed times, audit records, and restart checks are committed in [results/unit7_final_verification.json](results/unit7_final_verification.json). The code under test was `c0b690affa8231cc92968e80425a2307e6e7c03f`; subsequent source changes only correct explanatory comments/docstrings. The earlier run is retained separately, not overwritten.

Environment: macOS arm64, Python 3.12.13, torch 2.14.1, transformers 4.57.6, Flask 3.1.3, CPU inference. Model revision: `607a30d783dfa663caf39e06633721c8d4cfcd7e`. The run began on 2026-10-21 at 22:34:14 UTC. The first request took 2.8177 seconds including model load from the existing cache; subsequent requests took 0.0175–0.1262 seconds. These observations are not a performance guarantee or a download-time measurement.

| Frozen fixture | Actual origin | Model | Style | Final AI-likeness | Guess |
|---|---|---:|---:|---:|---|
| `ai_original` | AI-generated | 0.7607 | 0.6230 | 0.719390 | unsure |
| `ai_repetitive` | AI-generated repetitive control | 0.9951 | 0.9545 | 0.982920 | ai |
| `ai_edited` | Lightly edited AI | 0.6943 | 0.3756 | 0.598690 | unsure |
| `human_alice` | Human narrative | 0.7279 | 0.6236 | 0.696610 | unsure |
| `human_darwin` | Formal human prose | 0.5671 | 0.4552 | 0.533530 | unsure |
| `human_poem` | Human poetry with unusual vocabulary | 0.1806 | 0.5328 | 0.286260 | unsure |
| `ai_short` | Short AI fragment | 0.2879 | 0.5000 | 0.462882 | unsure |
| `ai_long` | AI text exceeding model coverage | 0.9970 | 0.9500 | 0.620725 | unsure |
| `ai_ornate` | AI-generated unusual prose | 0.1643 | 0.0663 | 0.134900 | human |
| `ai_original_replay` | AI-generated | 0.7607 | 0.6230 | 0.719390 | unsure |

All three label bands were reached. **The human band was reached by ornate AI-generated prose: a false negative, not evidence of successful human recognition.** All three genuine human excerpts returned unsure. The generic AI paragraph and its edited variant were also unsure; the repetitive control was AI. The edited AI passage had a model score above 0.5 and a style score below 0.5; the human poem showed the reverse. Neither gap exceeded the 0.50 severe-disagreement threshold, so that extra shrink did not fire. The short and long samples exercised the weak-evidence gate and returned unsure despite the long sample's high model score.

Fixture provenance is recorded in [fixtures/development.json](fixtures/development.json), frozen in commit `2945a96` before model measurements. The three human excerpts are attributed public-domain passages from [Alice's Adventures in Wonderland, chapter I](https://www.gutenberg.org/files/11/11-h/11-h.htm), [On the Origin of Species, Introduction](https://www.gutenberg.org/files/1228/1228-h/1228-h.htm), and [Through the Looking-Glass, Jabberwocky](https://www.gutenberg.org/files/12/12-h/12-h.htm). Generated and edited fixtures are explicitly marked AI-authored. Famous literature may have appeared in GPT-2 training data. This small, deliberately chosen development set is not a held-out accuracy benchmark or representative of contemporary student writing.

[criteria.md](criteria.md) remains byte-for-byte unchanged from its first commit:

| Criterion | Unit 7 evidence/status |
|---|---|
| 1: human false accusations | Not assessed: the required 20-passage held-out set and three trials belong to Unit 8. |
| 2: median score separation | Not assessed: the matched 20+20 held-out corpus has not been created or measured. |
| 3: label coverage and uncertainty | All three labels reached by real inference; exact thresholds and a 1,001-point grid checked by unit tests; short, insufficient-sentence, and truncated inputs stay unsure. Reachability is not accuracy. |
| 4: appeals and recovery | 10/10 real appeals preserved their exact reasons and original decisions after a fresh process restart. Unknown-ID and storage-failure behavior checked with fault-injection tests. |
| 5: validation | The malformed-input suite passed with zero detector calls and zero decision/appeal records for invalid inputs. Valid-response fields and finite scores are checked. |

[results/unit_tests.txt](results/unit_tests.txt) records 17 passing unit test methods, including subcases for malformed inputs, storage failures/corruption, Unicode handling, scoring boundaries, concurrency, and appeal history. These tests use detector doubles where appropriate; they do not establish model accuracy. [results/environment_check.txt](results/environment_check.txt) records nine passing setup checks. The real HTTP results above are separate from those unit tests.

### Actual curl submission and appeal

The following commands were actually run against `127.0.0.1:5057`; their complete responses are committed under `results/sample_*.json`. They use the existing `ai_original` fixture, not a new claimed human example. To repeat them, use the **new** returned content ID in the appeal and lookup; the recorded ID below belongs to this run.

Request body, also saved as `fixtures/sample_submit.json`:

```json
{
  "text": "A reliable service should be simple to use and easy to understand. It should accept a request and return a clear response. It should record important decisions so that people can review them later. When a mistake occurs, the service should explain what happened and offer a way to request help. These basic steps can improve trust and make the service more useful for everyone.",
  "creator_id": "demo_writer"
}
```

```bash
curl --silent --show-error --noproxy '*'   --output results/sample_submit_response.json --write-out '%{http_code}\n'   http://127.0.0.1:5057/submit --header 'Content-Type: application/json'   --data-binary @fixtures/sample_submit.json
```

HTTP **201**, response:

```json
{
  "combined_score": 0.71939,
  "confidence": 0.71939,
  "confidence_kind": "uncalibrated_ai_likeness",
  "content_id": "c0298b94-20ce-4793-ade0-4e8505f9a433",
  "evidence": {
    "limitations": [],
    "model": {
      "device": "cpu",
      "model": "gpt2",
      "model_revision": "607a30d783dfa663caf39e06633721c8d4cfcd7e",
      "model_score": 0.7607,
      "perplexity": 21.84343051144389,
      "tokens_scored": 71,
      "tokens_total": 71,
      "truncated": false
    },
    "signals_disagree": false,
    "style": {
      "components": {
        "repetition": 0.230769,
        "sparse_punctuation": 0.692308,
        "uniformity": 0.817967
      },
      "punctuation_density": 0.092308,
      "sentence_count": 5,
      "sentence_length_spread": 0.182033,
      "style_score": 0.623,
      "sufficient_evidence": true,
      "type_token_ratio": 0.723077,
      "windowed_type_token_ratio": 0.784615,
      "word_count": 65
    }
  },
  "guess": "unsure",
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "model_score": 0.7607,
  "review_available": true,
  "scoring_version": "unit7-v1",
  "status": "decided",
  "style_score": 0.623
}
```

Appeal request body, saved as `fixtures/sample_appeal.json`:

```json
{
  "content_id": "c0298b94-20ce-4793-ade0-4e8505f9a433",
  "reasoning": "Please review this estimate. This is a development appeal; it is not an admission about authorship."
}
```

```bash
curl --silent --show-error --noproxy '*'   --output results/sample_appeal_response.json --write-out '%{http_code}\n'   http://127.0.0.1:5057/appeal --header 'Content-Type: application/json'   --data-binary @fixtures/sample_appeal.json
```

HTTP **200**, response:

```json
{
  "content_id": "c0298b94-20ce-4793-ade0-4e8505f9a433",
  "message": "Your review request has been recorded. The original estimate is preserved; no automatic reclassification has been made.",
  "status": "under_review"
}
```

These are the two actual appended JSONL records from [logs/audit.jsonl](logs/audit.jsonl), also returned by `GET /log?limit=2`:

```jsonl
{"timestamp": "2026-10-21T22:36:17+00:00", "content_id": "c0298b94-20ce-4793-ade0-4e8505f9a433", "creator_id": "demo_writer", "guess": "unsure", "model_score": 0.7607, "style_score": 0.623, "combined_score": 0.71939, "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.", "status": "decided", "event": "decision", "confidence": 0.71939, "confidence_kind": "uncalibrated_ai_likeness", "scoring_version": "unit7-v1", "evidence": {"model": {"perplexity": 21.84343051144389, "tokens_total": 71, "tokens_scored": 71, "truncated": false, "model": "gpt2", "model_revision": "607a30d783dfa663caf39e06633721c8d4cfcd7e", "device": "cpu", "model_score": 0.7607}, "style": {"style_score": 0.623, "word_count": 65, "sentence_count": 5, "sufficient_evidence": true, "sentence_length_spread": 0.182033, "type_token_ratio": 0.723077, "windowed_type_token_ratio": 0.784615, "punctuation_density": 0.092308, "components": {"uniformity": 0.817967, "repetition": 0.230769, "sparse_punctuation": 0.692308}}, "limitations": [], "signals_disagree": false}, "text_sha256": "ceb68967430286c52a252c49f5a9e367e9184d19133b68da4bd49dd759191f5d", "text_length": 377}
{"guess": "unsure", "model_score": 0.7607, "style_score": 0.623, "combined_score": 0.71939, "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.", "timestamp": "2026-10-21T22:36:26+00:00", "content_id": "c0298b94-20ce-4793-ade0-4e8505f9a433", "creator_id": "demo_writer", "event": "appeal", "status": "under_review", "reasoning": "Please review this estimate. This is a development appeal; it is not an admission about authorship."}
```

### Stretch: retrieve current status

Actual request:

```bash
curl --silent --show-error --noproxy '*'   --output results/sample_content.json --write-out '%{http_code}\n'   http://127.0.0.1:5057/content/c0298b94-20ce-4793-ade0-4e8505f9a433
```

HTTP **200**, complete response. The top-level status is `under_review`; the original decision remains `decided`:

```json
{
  "appeals": [
    {
      "combined_score": 0.71939,
      "content_id": "c0298b94-20ce-4793-ade0-4e8505f9a433",
      "creator_id": "demo_writer",
      "event": "appeal",
      "guess": "unsure",
      "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
      "model_score": 0.7607,
      "reasoning": "Please review this estimate. This is a development appeal; it is not an admission about authorship.",
      "status": "under_review",
      "style_score": 0.623,
      "timestamp": "2026-10-21T22:36:26+00:00"
    }
  ],
  "content_id": "c0298b94-20ce-4793-ade0-4e8505f9a433",
  "original_decision": {
    "combined_score": 0.71939,
    "confidence": 0.71939,
    "confidence_kind": "uncalibrated_ai_likeness",
    "content_id": "c0298b94-20ce-4793-ade0-4e8505f9a433",
    "creator_id": "demo_writer",
    "event": "decision",
    "evidence": {
      "limitations": [],
      "model": {
        "device": "cpu",
        "model": "gpt2",
        "model_revision": "607a30d783dfa663caf39e06633721c8d4cfcd7e",
        "model_score": 0.7607,
        "perplexity": 21.84343051144389,
        "tokens_scored": 71,
        "tokens_total": 71,
        "truncated": false
      },
      "signals_disagree": false,
      "style": {
        "components": {
          "repetition": 0.230769,
          "sparse_punctuation": 0.692308,
          "uniformity": 0.817967
        },
        "punctuation_density": 0.092308,
        "sentence_count": 5,
        "sentence_length_spread": 0.182033,
        "style_score": 0.623,
        "sufficient_evidence": true,
        "type_token_ratio": 0.723077,
        "windowed_type_token_ratio": 0.784615,
        "word_count": 65
      }
    },
    "guess": "unsure",
    "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
    "model_score": 0.7607,
    "scoring_version": "unit7-v1",
    "status": "decided",
    "style_score": 0.623,
    "text_length": 377,
    "text_sha256": "ceb68967430286c52a252c49f5a9e367e9184d19133b68da4bd49dd759191f5d",
    "timestamp": "2026-10-21T22:36:17+00:00"
  },
  "status": "under_review"
}
```

The committed audit file contains 42 genuine events: two retained verification runs of ten decisions and ten appeals each, plus this curl decision and appeal. Unit-test events use isolated temporary stores and are not mixed into that evidence.

## How I Used AI

The student asked Codex to handle the project, including criteria and engineering decisions. The course asks for student-authored criteria; **these criteria are AI-authored**, and this disclosure does not satisfy that authorship requirement. No claim is made that the student independently wrote or reviewed them.

1. **Design and criteria.** The request was to complete Assignment 7 with senior-engineer reasoning, including drafting the criteria. Codex produced five measurable targets, failure costs, an API contract, and a scoring rule before running the detector. The resulting design added a wide uncertainty band, explicit input-coverage gates, immutable original decisions, and restart-persistent appeals. Those targets were committed first and were not lowered after results appeared.
2. **Implementation and evidence.** Codex implemented the service and generated a test plan that separated unit tests with detector doubles from actual model inference over HTTP. Testing and code review exposed unsafe handling of a non-UTF-8 audit file and an overflow edge case in the perplexity transform; Codex added structured storage failure handling and a numerically bounded transform, then reran real verification. The real model also called ornate AI prose human. That failure is reported above, with the original thresholds retained; it was not relabeled or removed to improve the reported outcome.

All generated fixture text retains its AI provenance, including the edited variant. Human fixtures use cited historical sources. Unit 8's held-out evaluation, attack testing, rate limiting, and measured improvement remain future work rather than invented results.
