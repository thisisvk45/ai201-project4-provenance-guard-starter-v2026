#!/usr/bin/env python3
"""Measure ten warm local submissions using the service's request records."""

import argparse
import json
import statistics
import sys
import uuid
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:5057")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.count < 1:
        parser.error("--count must be positive")
    fixture = json.loads((config.ROOT / "fixtures/sample_submit.json").read_text())
    session = requests.Session()
    request_ids = []
    for index in range(args.count + 1):
        body = {**fixture, "creator_id": "capstone_" + uuid.uuid4().hex[:16]}
        response = session.post(args.url.rstrip("/") + "/submit", json=body, timeout=60)
        response.raise_for_status()
        if response.status_code != 201 or "X-Request-ID" not in response.headers:
            raise RuntimeError(f"Unexpected submission response on request {index}: {response.status_code}")
        if index:
            request_ids.append(response.headers["X-Request-ID"])
    records = [json.loads(line) for line in config.REQUEST_LOG.read_text().splitlines() if line.strip()]
    by_id = {record["request_id"]: record for record in records}
    if any(request_id not in by_id for request_id in request_ids):
        raise RuntimeError("A successful response is missing its structured log record")
    durations_ms = [by_id[request_id]["duration_ms"] for request_id in request_ids]
    if any(by_id[request_id]["output"]["status_code"] != 201 for request_id in request_ids):
        raise RuntimeError("A logged submission has an unexpected status")
    average_seconds = statistics.mean(durations_ms) / 1000
    result = {
        "method": "one warmup excluded, then sequential submissions of the committed sample text; server request duration",
        "count": args.count,
        "request_ids": request_ids,
        "durations_ms": durations_ms,
        "average_seconds_per_run": round(average_seconds, 6),
        "seconds_for_100_per_day": round(100 * average_seconds, 3),
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as stream:
            stream.write(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
