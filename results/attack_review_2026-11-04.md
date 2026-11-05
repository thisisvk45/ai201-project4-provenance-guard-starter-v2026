# Official Attack Review

The official attack folder was run before and after one route validation change.

| Run | File | Requests | Server crashes |
| :--- | :--- | ---: | ---: |
| Before | `attack_run_2026-11-04_2118_before.md` | 56 | 0 |
| After | `attack_run_2026-11-04_2119_after.md` | 56 | 0 |

## Verdicts

| Attack family | Result | Verdict |
| :--- | :--- | :--- |
| EV01 through EV09 | AI styled text reached the unsure label after surface editing | BROKE |
| EV10 | Repeated stanza text reached the AI label | HELD |
| FP01 through FP08 | No genuine human sample received the AI label | HELD |
| PI01 through PI06 | Text instructions did not change the route or label template | HELD |
| MF01, MF02, MF04 through MF06, MF08 | Invalid input received a structured 4xx response | HELD |
| MF03 before | Control characters were accepted and scored | BROKE |
| MF03 after | Control characters received a 400 response | HELD |
| MF07 | Right to left writing was accepted and remained unsure | HELD |
| RQ01 through RQ10 and RQ12 | Malformed requests received a structured 4xx response | HELD |
| RQ11 | A request without a valid creator key received a 429 from the address fallback limit | HELD |
| FL01_01 through FL01_06 | Six requests were accepted within the configured limit | HELD |
| FL01_07 through FL01_12 | Further requests received 429 rate limit responses | HELD |

## Diagnosis

The worst route failure was MF03. The text field was a string, so it passed the original type check. It contained invisible control characters that were then tokenized and scored. The failure stage was the route validation stage. The mechanism was missing control character validation.

The evasion family still exposes a signal limitation. Typos, unusual words, quotation text, altered sentence shape, and human opening text can move the model or style score into the unsure band. The failure stage is signal one, signal two, or the combining rule depending on the attack. I did not lower the AI threshold because the false positive family already contains scores close to that boundary. Lowering it would risk accusing real writers.

## One Measured Improvement

`app.py` now rejects C0 control characters and the DEL character in `text`. Normal tabs and line breaks remain allowed.

MF03 changed from this before outcome:

```text
201 unsure 0.412
```

to this after outcome:

```text
400 invalid_text
```

## Ten Audit Events

```json
[
  {"timestamp":"2026-11-05T02:19:32+00:00","content_id":"d7ddea22-20ee-4363-8dbe-02e904aa7419","creator_id":"attacker_EV01","guess":"unsure","model_score":0.1635,"style_score":0.5534,"combined_score":0.28047,"status":"decided"},
  {"timestamp":"2026-11-05T02:19:33+00:00","content_id":"468f3d55-c447-4ff6-8818-a80e69de13b5","creator_id":"attacker_EV10","guess":"ai","model_score":0.9792,"style_score":0.7515,"combined_score":0.91089,"status":"decided"},
  {"timestamp":"2026-11-05T02:19:34+00:00","content_id":"3973dd1e-2699-46ad-b968-4ffb6f218004","creator_id":"attacker_FP07","guess":"unsure","model_score":0.8816,"style_score":0.4661,"combined_score":0.75695,"status":"decided"},
  {"timestamp":"2026-11-05T02:19:34+00:00","content_id":"4e32036c-7c35-468e-b1b9-5be49346afd8","creator_id":"attacker_PI02","guess":"human","model_score":0.2044,"style_score":0.2838,"combined_score":0.22822,"status":"decided"},
  {"timestamp":"2026-11-05T02:19:35+00:00","content_id":"7aff6d5b-8f3b-4fe1-bbae-d17bf8b25fdc","creator_id":"attacker_MF07","guess":"unsure","model_score":0.9064,"style_score":0.5,"combined_score":0.57112,"status":"decided"},
  {"timestamp":"2026-11-05T02:19:35+00:00","content_id":"6bfb1444-c855-4aa1-b1c9-482ce4d96972","creator_id":"attacker_flood","guess":"unsure","model_score":0.0287,"style_score":0.5,"combined_score":0.417523,"status":"decided"},
  {"timestamp":"2026-11-05T02:19:35+00:00","creator_id":"unknown","event":"rejected","status":"rejected","reason":"invalid_text","http_status":400},
  {"timestamp":"2026-11-05T02:19:35+00:00","creator_id":"unknown","event":"rejected","status":"rejected","reason":"unsupported_media_type","http_status":415},
  {"timestamp":"2026-11-05T02:19:35+00:00","creator_id":"attacker_flood","event":"rejected","status":"rejected","reason":"rate_limited","limit":"6 per 1 minute"},
  {"timestamp":"2026-11-05T02:19:35+00:00","creator_id":"attacker_flood","event":"rejected","status":"rejected","reason":"rate_limited","limit":"6 per 1 minute"}
]
```
