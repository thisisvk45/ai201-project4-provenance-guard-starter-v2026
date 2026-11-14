#!/usr/bin/env python3
"""Run the five frozen capstone checks against three fresh service processes."""

import argparse
import json
import math
import os
import socket
import statistics
import subprocess
import time
import uuid
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def send(session, url, method, path, **kwargs):
    response = session.request(method, url + path, timeout=90, **kwargs)
    try:
        body = response.json()
    except ValueError:
        body = {"non_json_response": response.text[:100]}
    return {
        "request_id": response.headers.get("X-Request-ID"),
        "status": response.status_code,
        "body": body,
    }


def matched(rows, ids):
    return {request_id: [row for row in rows if row.get("request_id") == request_id]
            for request_id in ids if request_id}


def trial(service_root, trial_dir, fixture):
    trial_dir.mkdir()
    port = free_port()
    url = f"http://127.0.0.1:{port}"
    env = {**os.environ, "HOST": "127.0.0.1", "PORT": str(port), "AI201_DEBUG": "0",
           "AI201_LOG_DIR": str(trial_dir), "HF_HUB_OFFLINE": "1",
           "TOKENIZERS_PARALLELISM": "false"}
    server_output = (trial_dir / "server.log").open("w")
    process = subprocess.Popen([str(service_root / ".venv/bin/python"), "app.py"],
                               cwd=service_root, env=env, stdout=server_output,
                               stderr=subprocess.STDOUT)
    session = requests.Session()
    session.trust_env = False
    try:
        deadline = time.monotonic() + 30
        while True:
            if process.poll() is not None:
                raise RuntimeError(f"Service exited early; see {trial_dir / 'server.log'}")
            try:
                health = send(session, url, "GET", "/health")
                if health["status"] == 200:
                    break
            except requests.RequestException:
                pass
            if time.monotonic() > deadline:
                raise RuntimeError("Service did not answer /health within 30 seconds")
            time.sleep(0.1)

        def valid_submit(text=None):
            return send(session, url, "POST", "/submit", json={
                "text": text or fixture["text"],
                "creator_id": "capstone_" + uuid.uuid4().hex[:16],
            })

        successful = [valid_submit() for _ in range(10)]
        text_marker = "TEXTMARK_" + uuid.uuid4().hex
        reason_marker = "REASONMARK_" + uuid.uuid4().hex
        query_marker = "QUERYMARK_" + uuid.uuid4().hex
        private_submission = valid_submit(fixture["text"] + " " + text_marker + ".")
        content_id = private_submission["body"].get("content_id")
        if not content_id:
            raise RuntimeError("Privacy probe submission did not return a content ID")
        private_appeal = send(session, url, "POST", "/appeal", json={
            "content_id": content_id, "reasoning": "Review requested: " + reason_marker,
        })
        query_probe = send(session, url, "GET", "/log?marker=" + query_marker)

        rejected = [
            send(session, url, "POST", "/submit", data="hello", headers={"Content-Type": "text/plain"}),
            send(session, url, "POST", "/submit", data="{", headers={"Content-Type": "application/json"}),
            send(session, url, "POST", "/submit", json={"creator_id": "bad"}),
            send(session, url, "POST", "/submit", json={"text": "two words", "creator_id": "bad"}),
            send(session, url, "POST", "/submit", data="x" * 65537,
                 headers={"Content-Type": "application/json"}),
        ]

        warmup = valid_submit()
        measured = [valid_submit() for _ in range(10)]
        rows = [json.loads(line) for line in (trial_dir / "requests.jsonl").read_text().splitlines() if line.strip()]
        raw_log = (trial_dir / "requests.jsonl").read_text()
        audit_rows = [json.loads(line) for line in (trial_dir / "audit.jsonl").read_text().splitlines() if line.strip()]
        ids = [r["request_id"] for r in [health, *successful, private_submission,
                                              private_appeal, query_probe, *rejected,
                                              warmup, *measured]]
        matches = matched(rows, ids)
        def one(result):
            records = matches.get(result["request_id"], [])
            return records[0] if len(records) == 1 else None

        c1 = sum(bool(result["status"] == 201 and result["request_id"] and
                      (row := one(result)) and row["input"]["method"] == "POST" and
                      row["input"]["path"] == "/submit" and row["output"]["status_code"] == 201 and
                      row["output"]["content_id"] == result["body"].get("content_id") and
                      isinstance(row.get("timestamp"), str) and row["timestamp"].endswith("+00:00") and
                      isinstance(row.get("duration_ms"), (int, float)) and
                      math.isfinite(row["duration_ms"]) and row["duration_ms"] >= 0)
                 for result in successful)
        privacy_results = [private_submission, private_appeal, query_probe]
        c2 = sum(one(result) is not None for result in privacy_results)
        c2_private = all(marker not in raw_log for marker in (text_marker, reason_marker, query_marker))
        expected_statuses = [415, 400, 400, 422, 413]
        c3 = sum(bool(result["status"] == expected and result["request_id"] and
                      (row := one(result)) and row["output"]["status_code"] == expected and
                      isinstance(row["output"]["error"], str) and row["output"]["error"])
                 for result, expected in zip(rejected, expected_statuses))
        c3_no_decisions = sum(row.get("event") == "decision" for row in audit_rows) == 22
        health_row = one(health)
        c4 = bool(health["status"] == 200 and health_row and
                  health_row["input"]["method"] == "GET" and
                  health_row["input"]["path"] == "/health" and
                  health_row["output"]["status_code"] == 200)
        c5 = sum(bool((row := one(result)) and
                      isinstance(row.get("model_duration_ms"), (int, float)) and
                      math.isfinite(row["model_duration_ms"]) and
                      0 <= row["model_duration_ms"] <= row["duration_ms"])
                 for result in measured)
        durations = [one(result)["duration_ms"] for result in measured if one(result)]
        return {
            "service_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=service_root, text=True).strip(),
            "health": health, "successful": successful, "privacy": privacy_results,
            "privacy_markers": [text_marker, reason_marker, query_marker],
            "rejected": rejected, "warmup": warmup, "measured": measured,
            "scores": {"criterion_1": f"{c1}/10", "criterion_2": f"{c2}/3 records, markers absent={c2_private}",
                       "criterion_3": f"{c3}/5, no rejected decisions={c3_no_decisions}",
                       "criterion_4": "MET" if c4 else "MISSED", "criterion_5": f"{c5}/10"},
            "measured_durations_ms": durations,
            "mean_warm_seconds": statistics.mean(durations) / 1000 if durations else None,
            "record_count": len(rows),
        }
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        server_output.close()
        session.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--service-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--trials", type=int, default=3)
    args = parser.parse_args()
    if args.trials != 3:
        parser.error("The frozen criteria require exactly three trials")
    service_root = args.service_root.resolve()
    if not (service_root / ".venv/bin/python").exists():
        parser.error("Service checkout needs the pinned .venv setup from RUNNING.md")
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=False)
    fixture = json.loads((ROOT / "fixtures/sample_submit.json").read_text())
    trials = []
    for number in range(1, 4):
        result = trial(service_root, output_dir / f"trial{number}", fixture)
        trials.append(result)
        print(f"Trial {number}: {result['scores']}", flush=True)
    all_ms = [ms for result in trials for ms in result["measured_durations_ms"]]
    report = {"trials": trials, "mean_warm_seconds": statistics.mean(all_ms) / 1000,
              "seconds_for_100_per_day": statistics.mean(all_ms) / 1000 * 100}
    (output_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
