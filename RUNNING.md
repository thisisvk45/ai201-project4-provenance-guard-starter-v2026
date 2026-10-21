# Running Provenance Guard

This is a local Flask prototype for CodePath AI201 Unit 7. Its detector runs on your laptop after the initial model download; no API key is required.

## Setup

Verified with Python 3.12.13 on macOS arm64. Use Python 3.12 and a fresh virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
python -c 'import detector; print(detector.warm_up())'
python test.py
```

`requirements.lock` captures the tested versions. `requirements.txt` retains the portable dependency ranges from the starter. If a lock entry has no wheel for your platform, install `requirements.txt` in a separate environment and rerun the checks; do not assume the recorded results transfer. First model download is approximately 550 MB and requires network access. Later runs can use the cached model with `HF_HUB_OFFLINE=1`.

On Windows, activate with `.venv\Scripts\Activate.ps1`. Use `curl.exe` instead of PowerShell's `curl` alias, and put shell commands on one line.

## Run

```bash
PORT=5057 AI201_DEBUG=0 python app.py
```

Keep that terminal running. Port 5057 avoids the common macOS conflict on port 5000. Default host is loopback (`127.0.0.1`), and debug is off. The first submission loads the model into this process even if a previous warm-up process downloaded it.

In another terminal, from the repository directory:

```bash
curl http://127.0.0.1:5057/health
curl http://127.0.0.1:5057/ping -H 'Content-Type: application/json' -d '{"message":"hello"}'
curl http://127.0.0.1:5057/submit -H 'Content-Type: application/json' --data-binary @fixtures/sample_submit.json
```

Copy the **new** `content_id` from that response into the following two commands. The UUID already in `fixtures/sample_appeal.json` belongs to the committed historical example.

```bash
curl http://127.0.0.1:5057/appeal -H 'Content-Type: application/json' -d '{"content_id":"REPLACE_WITH_NEW_ID","reasoning":"Please review this estimate."}'
curl http://127.0.0.1:5057/content/REPLACE_WITH_NEW_ID
curl 'http://127.0.0.1:5057/log?limit=2'
```

A valid submission returns 201. An appeal and a content lookup return 200. The lookup shows `status=under_review` while retaining the original decision. Press Ctrl+C in the server terminal to stop.

## Validation and failures

- JSON objects and nonblank string fields are required. Text must contain at least three words and at most 10,000 characters.
- Creator IDs must match `[A-Za-z0-9_.-]{1,128}`. Appeal reasons may contain at most 2,000 characters; content IDs must be valid UUIDs.
- Request bodies are capped at 65,536 bytes. Accepted short, low-sentence-count, and model-truncated inputs receive unsure labels with evidence limits.
- Errors are structured JSON: 400 invalid request, 404 unknown content, 413 too large, 415 wrong media type, 422 too few words, 503 model busy/unavailable or audit failure.
- Only one model inference runs at once; concurrent attempts receive 503. Retry after the in-flight request completes. A failed or retried request is not guaranteed idempotent.

## Verify

```bash
python -m unittest discover -s tests -v
python test.py
python scripts/verify_unit7.py --output results/my_verification.json
```

The first command uses detector doubles where needed to test boundaries and failure paths. It does not download or evaluate model quality. The environment check inspects installed dependencies and model cache. The final command requires a previously cached model, starts its own loopback server, makes ten real submissions and appeals, restarts that process, and verifies persistence. It refuses to overwrite an existing output file, appends to the audit log, and shuts down its server on completion. Choose a new output path for each rerun. Recorded runs and complete examples are in README.md and `results/`.

## Storage and operating limits

Audit events default to `logs/audit.jsonl`. Override with `AI201_LOG_DIR=/absolute/test/path`. Each successful decision or appeal is flushed and fsynced before a success response. Current status is reconstructed from the log; restarting the process does not erase appeals. The supplied file intentionally retains the recorded development runs.

The store supports threads in **one** process. Do not run multiple workers against it. Lookups and append validation read the file, so cost grows with history. Keep a backup before editing or moving logs. Corrupt or unreadable history returns 503 rather than silently discarding evidence; restore a known-good backup or investigate the bad record, preserving the damaged copy for diagnosis. Do not clear historical evidence to hide a failure.

This prototype has no authentication, authorization, private reviewer console, or completed-review workflow. Caller-supplied creator IDs are not identity proof. Keep it on loopback and use test data. The log contains creator IDs and appeal reasons; do not publish real private submissions or reasons. Submitted text is represented by a hash and length in audit records, not stored verbatim there.

## Unit 8 boundary

Rate limiting is off by default (`AI201_RATE_LIMITS=0`). The starter's attack/evaluation scripts remain for Unit 8. They are not claimed as passing or completed. Criteria 1 and 2 need a new frozen held-out corpus; development fixtures must not be reused as that evaluation set. The five original criteria and current scoring thresholds remain unchanged.
