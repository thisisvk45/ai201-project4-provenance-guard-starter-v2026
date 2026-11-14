# Acceptance criteria: Provenance Guard

I defined the acceptance criteria and expected behavior, with AI support for wording and edge cases. The five targets below were committed before implementation and model results.

These targets are frozen in the first project commit. In Unit 8, every target must hold in each of three trials. Targets will not be lowered after observing results. Development samples are not the held-out evaluation set.

## 1. Limit false accusations

On 20 previously unused, independently human-authored English passages of 50–250 words, at most one passage per trial may receive `guess="ai"`. Include at least five examples of plain writing and five of formal writing. Record author/source and exact text before scoring; synthetic human-like prose is ineligible. Returning `unsure` is not a false accusation.

**Why this target:** A wrong accusation harms a writer more than a missed detection harms this prototype. A 5% empirical ceiling is a meaningful first check, not evidence of a 5% population error rate; 20 examples cannot establish production reliability.

## 2. Separate known origins

On the 20 human passages above and 20 AI-generated English passages matched by topic and approximate length, the median combined AI-likeness score for AI passages must exceed the human median by at least 0.20 in every trial. Freeze both sets before evaluation and keep them separate from development examples.

**Why this target:** A system that calls everything unsure could satisfy criterion 1 while providing no useful signal. A 0.20 median separation demands discrimination, although overlapping distributions can still produce errors.

## 3. Cover all labels and handle weak evidence

Across a frozen development fixture set, real local model calls must produce all three labels at least once. Independently, every finite score from 0 through 1 must map to exactly one label: human at `score <= 0.25`, unsure at `0.25 < score < 0.80`, AI at `score >= 0.80`. Verify boundaries and a 1,001-point grid. Every accepted text with fewer than 40 words, fewer than three sentences, or more than 400 model tokens must return `unsure` and explain the evidence limit.

**Why this target:** The middle band is an explicit product state. Boundary checks prevent gaps, while the evidence gate prevents a confident decision about a short fragment or an unexamined tail. Fixture coverage proves reachability, not accuracy.

## 4. Preserve decisions and appeals

For ten successful submissions followed by ten valid appeals, all ten appeals must return `under_review`, preserve their exact reasoning, and leave the original decision unchanged in the JSONL audit log. After a fresh service process starts against that log, all ten content lookups must still report `under_review`. An unknown content ID must return 404 without creating an appeal. An audit-write failure must return 503 instead of claiming success.

**Why this target:** An appeal is the recovery path when detection fails. A success response without durable evidence is worse than an explicit temporary failure. Restart recovery matters even for a laptop prototype.

## 5. Reject invalid requests before inference

All cases in a committed malformed-input suite must return a structured JSON 4xx response, make zero detector calls, and create zero decision/appeal records: non-JSON media type, malformed JSON, non-object JSON, absent/null/non-string/blank fields, fewer than three words, text over 10,000 characters, creator ID outside `[A-Za-z0-9_.-]{1,128}`, appeal reasoning over 2,000 characters, malformed content IDs, and bodies over 65,536 bytes. Accepted requests must contain all documented response fields with finite scores in `[0,1]`.

**Why this target:** Invalid input should cost a validation check, not a model invocation. Explicit size and type limits bound work and give clients actionable errors. A rejection log entry is allowed; a fabricated decision is not.

## Capstone acceptance criteria: operational request logging

These five targets apply to the capstone extension and are frozen before the scored run log. Codex drafted them at my request; I will disclose that assistance in the capstone README. Each target must hold in each of three separate trials. Use a fresh request-log directory per trial so records from earlier work cannot satisfy a target.

### 1. Correlate successful submissions with records

For ten sequential valid `POST /submit` requests using the committed sample text and distinct creator IDs, all ten must return HTTP 201 with an `X-Request-ID` header. Each ID must match exactly one JSONL record in `requests.jsonl`. Every matched record must contain a UTC timestamp, the input method and path, HTTP 201 and a content ID in the output, and a finite nonnegative `duration_ms`.

**Why this target:** The service already saves decisions, but an operator needs to connect a caller's response to the request that produced it. Ten requests expose missing or duplicate entries that one happy-path call would miss.

### 2. Keep private content out of operational logs

In each trial, submit text containing a unique marker, appeal it with a different unique marker, and request `/log` with a third unique marker in the query string. All three requests must appear in `requests.jsonl`, and none of the three marker strings may appear anywhere in that file. The linked audit log may retain the appeal reason as designed.

**Why this target:** A useful operational record should not become a second store of writers' text or review reasons. Three distinct markers make the text, appeal, and query-string paths separately checkable.

### 3. Record rejected requests without decisions

Send five invalid `POST /submit` requests in each trial: non-JSON media type, malformed JSON, missing text, two-word text, and a body above 65,536 bytes. All five must return their documented 4xx status and an `X-Request-ID`. Each ID must match exactly one request-log record with the same HTTP status and a nonblank error code. None may create an audit decision.

**Why this target:** Bad input is a normal failure path. If it vanishes from the operational record, the service cannot distinguish a quiet period from repeated rejected calls.

### 4. Start from a clean checkout

From a separate clean checkout with the pinned dependencies installed, start the service using the single command in `RUNNING.md` in three fresh processes. In each process, `GET /health` must return HTTP 200 and its `X-Request-ID` must match one new JSONL request record with method `GET`, path `/health`, and status 200.

**Why this target:** The local-with-logs path is the deployment evidence for this model-heavy service. A repeatable start and observable response matter more than one successful run in the development directory.

### 5. Expose model time within request time

For ten warm, valid `POST /submit` requests in each trial, all ten matched request-log records must include a finite `model_duration_ms` measured around model inference, with `0 <= model_duration_ms <= duration_ms`. The total `duration_ms` must remain present. Exclude one explicit warmup request from the ten measured requests.

**Why this target:** Total response time alone cannot show whether the local model or another stage caused a slow request. The model is the largest expected compute cost, so its own timing is the first breakdown needed for diagnosis.
