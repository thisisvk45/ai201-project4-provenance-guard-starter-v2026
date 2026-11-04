# Held Out Evaluation Data

Add one JSON object per line to `held_out.jsonl`. Do not add generated text and describe it as human writing.

Each record needs an id, origin, source, verification, topic, and text.

```json
{"id":"human_01","origin":"human","source":"author or stable source link","verified":true,"topic":"campus life","text":"A verified human written passage with fifty to two hundred fifty words goes here."}
```

Use 20 verified human passages and 20 AI passages. Match topics and approximate length across the two groups. Keep this data separate from `fixtures/development.json`.

Run this before evaluation:

```bash
.venv/bin/python scripts/validate_held_out.py evaluation/held_out.jsonl
```

The validator checks count, source fields, verification, word range, duplicate text, and topic coverage. It does not decide whether a source claim is true. That confirmation belongs to the person adding the data.
