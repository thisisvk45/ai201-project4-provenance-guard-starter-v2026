# Provenance Guard

An English-writing provenance estimate with uncertainty and an appeal path. Built from the CodePath AI201 Unit 7 starter; this same fork will be used in Unit 8.

## What This Does

Design recorded before implementation and results:

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

## Signals and Scoring

The combining function will be `scoring.py::combine_signals`; weights and thresholds live in `config.py`. `confidence` means **uncalibrated AI-likeness**, not a probability of cheating or certainty in the returned label. Zero points toward human-like patterns; one toward AI-like patterns.

GPT-2 measures contextual token predictability, not authorship. Plain human writing can look predictable; unusual AI prose can look surprising. The style signal measures surface form, not meaning. Editing punctuation, sentence breaks, or spelling can move it without changing origin. Different mechanisms do not establish statistical independence.

Style plan: coefficient of variation of sentence word counts; mean type/token ratio in consecutive 50-word windows; Unicode punctuation characters per word. Normalize AI-oriented components as `max(0, 1-CV)`, `clip((0.9-TTR)/0.5)`, and `max(0, 1-density/0.3)`, then combine at 0.55/0.30/0.15. These are transparent heuristics, not fitted probabilities. Fewer than three sentences or 40 words makes style neutral (0.5); the measurements are still reported.

## Label Variants

| Band | Exact reader-facing text |
|---|---|
| `0 <= score <= 0.25` | This writing shows patterns often found in human writing. This automated estimate does not verify who wrote it. You can request a review if it seems wrong. |
| `0.25 < score < 0.80` | We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review. |
| `0.80 <= score <= 1` | This writing shows patterns often found in AI-generated text. This is an automated estimate, not proof of authorship. If this seems wrong, you can request a review. |

## Sample Run

Actual requests, responses, audit entries, model metadata, and limitations will be recorded here after implementation. No results exist at this design commit.

## How I Used AI

The student explicitly asked Codex to handle the project, including criteria and engineering decisions. Codex drafted `criteria.md` and this design before implementation or scoring. The course asks for student-authored criteria; these are AI-authored and are disclosed as such. No claim is made that the student independently wrote or reviewed them.

Implementation and verification details will be added as they occur. Human-authored fixtures will be attributed public-domain excerpts, never model-generated passages presented as human writing. Generated and edited passages will retain their actual provenance.
