# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-04 21:19
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 201 | `d7ddea22-20ee-4363-8dbe-02e904aa7419` | unsure | 0.280 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 201 | `9aeb1768-35d8-4e6b-9f33-1aa31d16c541` | unsure | 0.463 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 201 | `f63f701c-8b5f-459b-aa4d-2b6b43784908` | unsure | 0.578 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 201 | `6cecfbb4-8585-4a49-b728-d08f84458102` | unsure | 0.590 |  |
| EV05 | evasion | both signals: heavy human editing pass | 201 | `7d132c56-3025-4a6e-8ef0-39ca2a7041dd` | unsure | 0.314 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 201 | `3638ba20-f3c3-4750-82d3-72bcce069d18` | unsure | 0.433 |  |
| EV07 | evasion | signal two: padding with punctuation | 201 | `c80a52cb-bd13-48ef-8b45-3ef21be51c9f` | unsure | 0.515 |  |
| EV08 | evasion | signal one: text below the token window | 201 | `f20407f3-f800-4cab-b4b0-b5e6afc474ff` | unsure | 0.455 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 201 | `15239b70-f283-4c41-9bab-df65da7dbe32` | unsure | 0.605 |  |
| EV10 | evasion | signal two: repeated stanza structure | 201 | `468f3d55-c447-4ff6-8818-a80e69de13b5` | ai | 0.911 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 201 | `164e48a8-2a98-4e3f-94b5-67bdf335274a` | unsure | 0.576 |  |
| FP02 | false_positive | human writing in a formal register | 201 | `9bd79d6a-6be1-41a2-b344-ec2b4d15ce11` | unsure | 0.692 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 201 | `5d4014f7-7c18-4057-8b05-c3db4fc14b8c` | unsure | 0.723 |  |
| FP04 | false_positive | a student essay written to a rubric | 201 | `509db189-9a83-414e-bd7b-19812fc598ce` | unsure | 0.725 |  |
| FP05 | false_positive | technical documentation written by a person | 201 | `6239d20f-1be0-4d2a-98f9-39e4d7d6d523` | unsure | 0.745 |  |
| FP06 | false_positive | a person imitating a formal template | 201 | `39c6efa1-7061-4e5a-b610-7f08be6fb707` | unsure | 0.751 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 201 | `3973dd1e-2699-46ad-b968-4ffb6f218004` | unsure | 0.757 |  |
| FP08 | false_positive | very short genuine human submission | 201 | `46d59a08-5889-467a-b01f-ff0ae77df4a5` | unsure | 0.469 |  |
| PI01 | prompt_injection | instruction to ignore the check | 201 | `4772f6f5-1f98-4d30-986d-231384d838bc` | unsure | 0.417 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 201 | `4e32036c-7c35-468e-b1b9-5be49346afd8` | human | 0.228 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 201 | `0032cd29-b517-4114-8073-eb9acad3dcb0` | unsure | 0.530 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 201 | `3ccba992-c5d5-4f9b-a799-67f314278682` | unsure | 0.478 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 201 | `34ded212-22f4-4847-b918-5e689a4b1de2` | unsure | 0.525 |  |
| PI06 | prompt_injection | instruction plus real human text | 201 | `f5abe39d-59ea-4b49-a3f4-730c38212cc8` | unsure | 0.531 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 422 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 400 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 422 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 422 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 422 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 201 | `7aff6d5b-8f3b-4fe1-bbae-d17bf8b25fdc` | unsure | 0.571 |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 415 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 201 | `e362523b-98a4-458f-8509-0aac655cba4b` | unsure | 0.418 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 201 | `bf0bbbe5-09d3-44d8-8e35-eb7e5e4299a5` | unsure | 0.418 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 201 | `3baea778-cdc2-4d7b-bb7e-58c2954f82ea` | unsure | 0.418 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 201 | `bb4c5e64-c3b9-42cd-9181-913b6a5d9f9e` | unsure | 0.418 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 201 | `4be237af-344c-45f7-8499-ca5a821cfc47` | unsure | 0.418 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 201 | `6bfb1444-c855-4aa1-b1c9-482ce4d96972` | unsure | 0.418 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 201,
  "content_id": "d7ddea22-20ee-4363-8dbe-02e904aa7419",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.28047,
  "model_score": 0.1635,
  "style_score": 0.5534,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 201,
  "content_id": "9aeb1768-35d8-4e6b-9f33-1aa31d16c541",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.46338,
  "model_score": 0.5943,
  "style_score": 0.1579,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 201,
  "content_id": "f63f701c-8b5f-459b-aa4d-2b6b43784908",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5783,
  "model_score": 0.6662,
  "style_score": 0.3732,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 201,
  "content_id": "6cecfbb4-8585-4a49-b728-d08f84458102",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.59046,
  "model_score": 0.6114,
  "style_score": 0.5416,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 201,
  "content_id": "7d132c56-3025-4a6e-8ef0-39ca2a7041dd",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.31442,
  "model_score": 0.3212,
  "style_score": 0.2986,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 201,
  "content_id": "3638ba20-f3c3-4750-82d3-72bcce069d18",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.43284,
  "model_score": 0.5727,
  "style_score": 0.1065,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 201,
  "content_id": "c80a52cb-bd13-48ef-8b45-3ef21be51c9f",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.515085,
  "model_score": 0.5862,
  "style_score": 0.5,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 201,
  "content_id": "f20407f3-f800-4cab-b4b0-b5e6afc474ff",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.45541,
  "model_score": 0.2452,
  "style_score": 0.5,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 201,
  "content_id": "15239b70-f283-4c41-9bab-df65da7dbe32",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.60454,
  "model_score": 0.7042,
  "style_score": 0.372,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 201,
  "content_id": "468f3d55-c447-4ff6-8818-a80e69de13b5",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.91089,
  "model_score": 0.9792,
  "style_score": 0.7515,
  "label": "This writing shows patterns often found in AI-generated text. This is an automated estimate, not proof of authorship. If this seems wrong, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 201,
  "content_id": "164e48a8-2a98-4e3f-94b5-67bdf335274a",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.57577,
  "model_score": 0.6175,
  "style_score": 0.4784,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 201,
  "content_id": "9bd79d6a-6be1-41a2-b344-ec2b4d15ce11",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.69211,
  "model_score": 0.7387,
  "style_score": 0.5834,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 201,
  "content_id": "5d4014f7-7c18-4057-8b05-c3db4fc14b8c",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.72314,
  "model_score": 0.8051,
  "style_score": 0.5319,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 201,
  "content_id": "509db189-9a83-414e-bd7b-19812fc598ce",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.72505,
  "model_score": 0.8329,
  "style_score": 0.4734,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 201,
  "content_id": "6239d20f-1be0-4d2a-98f9-39e4d7d6d523",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.74476,
  "model_score": 0.8005,
  "style_score": 0.6147,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 201,
  "content_id": "39c6efa1-7061-4e5a-b610-7f08be6fb707",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.75093,
  "model_score": 0.8814,
  "style_score": 0.4465,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 201,
  "content_id": "3973dd1e-2699-46ad-b968-4ffb6f218004",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.75695,
  "model_score": 0.8816,
  "style_score": 0.4661,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 201,
  "content_id": "46d59a08-5889-467a-b01f-ff0ae77df4a5",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.468902,
  "model_score": 0.3223,
  "style_score": 0.5,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 201,
  "content_id": "4772f6f5-1f98-4d30-986d-231384d838bc",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.41726,
  "model_score": 0.4625,
  "style_score": 0.3117,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 201,
  "content_id": "4e32036c-7c35-468e-b1b9-5be49346afd8",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.22822,
  "model_score": 0.2044,
  "style_score": 0.2838,
  "label": "This writing shows patterns often found in human writing. This automated estimate does not verify who wrote it. You can request a review if it seems wrong.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 201,
  "content_id": "0032cd29-b517-4114-8073-eb9acad3dcb0",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.53043,
  "model_score": 0.5943,
  "style_score": 0.3814,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 201,
  "content_id": "3ccba992-c5d5-4f9b-a799-67f314278682",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.47754,
  "model_score": 0.4998,
  "style_score": 0.4256,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 201,
  "content_id": "34ded212-22f4-4847-b918-5e689a4b1de2",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.524517,
  "model_score": 0.6401,
  "style_score": 0.5,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 201,
  "content_id": "f5abe39d-59ea-4b49-a3f4-730c38212cc8",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.53076,
  "model_score": 0.5583,
  "style_score": 0.4665,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 201,
  "content_id": "7aff6d5b-8f3b-4fe1-bbae-d17bf8b25fdc",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.57112,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 415,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 201,
  "content_id": "e362523b-98a4-458f-8509-0aac655cba4b",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.417523,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 201,
  "content_id": "bf0bbbe5-09d3-44d8-8e35-eb7e5e4299a5",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.417523,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 201,
  "content_id": "3baea778-cdc2-4d7b-bb7e-58c2954f82ea",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.417523,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 201,
  "content_id": "bb4c5e64-c3b9-42cd-9181-913b6a5d9f9e",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.417523,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 201,
  "content_id": "4be237af-344c-45f7-8499-ca5a821cfc47",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.417523,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 201,
  "content_id": "6bfb1444-c855-4aa1-b1c9-482ce4d96972",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.417523,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
