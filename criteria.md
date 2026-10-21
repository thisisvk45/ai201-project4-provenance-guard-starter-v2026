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
