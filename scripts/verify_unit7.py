"""Exercise the real HTTP service and save evidence. Does not run Unit 8 attacks."""
import argparse
import hashlib
import json
import math
import os
import platform
import socket
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/unit7_verification.json")
    args = parser.parse_args()
    output = ROOT / args.output
    if output.exists():
        raise SystemExit("Evidence already exists; choose a new --output path. Nothing was overwritten.")
    fixtures_path = ROOT / "fixtures/development.json"
    fixtures = json.loads(fixtures_path.read_text())
    run_id = uuid.uuid4().hex[:10]
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    base = f"http://127.0.0.1:{port}"
    env = {**os.environ, "HOST": "127.0.0.1", "PORT": str(port), "AI201_DEBUG": "0",
           "AI201_RATE_LIMITS": "0", "AI201_LOG_DIR": str(ROOT / "logs"),
           "HF_HUB_OFFLINE": "1", "TOKENIZERS_PARALLELISM": "false"}
    output.parent.mkdir(exist_ok=True)
    server_log = output.with_suffix(".server.log")
    process = None
    stream = server_log.open("w")
    session = requests.Session()
    session.trust_env = False

    def start():
        nonlocal process
        process = subprocess.Popen([sys.executable, "-u", "app.py"], cwd=ROOT, env=env,
                                   stdout=stream, stderr=subprocess.STDOUT)
        for _ in range(150):
            if process.poll() is not None:
                raise RuntimeError("Service exited; inspect the server log.")
            try:
                response = session.get(base + "/health", timeout=1)
                if response.status_code == 200:
                    return response.json()
            except requests.RequestException:
                pass
            time.sleep(.1)
        raise RuntimeError("Service did not become ready.")

    def stop():
        nonlocal process
        if process is not None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            process = None

    result = {"timestamp": datetime.now(timezone.utc).isoformat(), "run_id": run_id,
              "base_url": base, "python": sys.version, "platform": platform.platform(),
              "fixture_sha256": hashlib.sha256(fixtures_path.read_bytes()).hexdigest(),
              "code_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "inference": "real local GPT-2; no mocked scores", "samples": [], "appeals": []}
    try:
        result["initial_health"] = start()
        ping = session.post(base + "/ping", json={"message": "unit7"}, timeout=10)
        assert ping.status_code == 200 and ping.json()["you_sent"] == "unit7"
        # Nine fixtures plus one explicitly named replay = ten durable decisions/appeals.
        for i, fixture in enumerate(fixtures + [dict(fixtures[0], id=fixtures[0]["id"] + "_replay")]):
            body = {"text": fixture["text"], "creator_id": f"dev_{run_id}_{i}"}
            began = time.perf_counter()
            response = session.post(base + "/submit", json=body, timeout=120)
            elapsed = time.perf_counter() - began
            assert response.status_code == 201, (fixture["id"], response.status_code, response.text)
            payload = response.json()
            for field in ("model_score", "style_score", "combined_score", "confidence"):
                assert math.isfinite(payload[field]) and 0 <= payload[field] <= 1, (fixture["id"], field)
            assert payload["confidence"] == payload["combined_score"]
            expected = "human" if payload["confidence"] <= .25 else "ai" if payload["confidence"] >= .80 else "unsure"
            assert payload["guess"] == expected, fixture["id"]
            if payload["evidence"]["limitations"]:
                assert payload["guess"] == "unsure", fixture["id"]
            result["samples"].append({"fixture_id": fixture["id"], "category": fixture["category"],
                                      "provenance": fixture["provenance"], "request": body,
                                      "http_status": response.status_code, "seconds": round(elapsed, 4),
                                      "response": payload})
            print(f'{fixture["id"]}: model={payload["model_score"]:.4f} '
                  f'style={payload["style_score"]:.4f} combined={payload["confidence"]:.6f} '
                  f'guess={payload["guess"]}', flush=True)
        decisions_before = session.get(base + "/log", timeout=10).json()["entries"]
        for sample in result["samples"]:
            current = session.get(base + "/content/" + sample["response"]["content_id"], timeout=10)
            assert current.status_code == 200
            assert current.json()["status"] == "decided" and current.json()["appeals"] == []
            body = {"content_id": sample["response"]["content_id"],
                    "reasoning": f'Development review request for {sample["fixture_id"]}. Please inspect the recorded signal evidence; this is not an authorship admission.'}
            if sample is result["samples"][0]:
                body["reasoning"] += "\u2028Draft context.\u2029Review requested.\u0085End."
            response = session.post(base + "/appeal", json=body, timeout=10)
            assert response.status_code == 200 and response.json()["status"] == "under_review"
            result["appeals"].append({"request": body, "http_status": response.status_code, "response": response.json()})
        all_events = session.get(base + "/log", timeout=10).json()["entries"]
        ids = {s["response"]["content_id"] for s in result["samples"]}
        relevant = [e for e in all_events if e.get("content_id") in ids]
        original = [e for e in decisions_before if e.get("content_id") in ids]
        assert [e for e in relevant if e.get("event") == "decision"] == original
        assert len([e for e in relevant if e.get("event") == "appeal"]) == 10
        result["audit_entries"] = relevant
        stop()
        result["restarted_health"] = start()
        assert result["restarted_health"]["detector_loaded"] is False
        result["restart_checks"] = []
        for item in result["appeals"]:
            cid = item["request"]["content_id"]
            response = session.get(base + "/content/" + cid, timeout=10)
            payload = response.json()
            assert response.status_code == 200 and payload["status"] == "under_review"
            assert payload["appeals"][0]["reasoning"] == item["request"]["reasoning"]
            assert payload["original_decision"] == next(e for e in original if e["content_id"] == cid)
            result["restart_checks"].append({"content_id": cid, "status": payload["status"], "exact_reasoning_retained": True,
                                            "original_unchanged": True})
        result["label_coverage"] = sorted({s["response"]["guess"] for s in result["samples"]})
        result["all_three_labels_reached"] = result["label_coverage"] == ["ai", "human", "unsure"]
        result["appeal_restart_pass"] = len(result["restart_checks"]) == 10
        result["limitations"] = [
            "Development fixtures are deliberately chosen and not an accuracy benchmark.",
            "Human sources are public-domain literature, not the student's own writing or a representative held-out sample.",
            "One repeated AI control and one unusual AI passage exercise extremes; they do not establish reliable provenance detection.",
            "Criteria 1 and 2 require a separate frozen held-out corpus in Unit 8 and are not evaluated here.",
        ]
        output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        if not result["all_three_labels_reached"]:
            raise SystemExit(f"Label coverage failed: {result['label_coverage']}. Evidence saved to {output}.")
        print(f"Saved {output}; label coverage={result['label_coverage']}; 10/10 appeals survived restart.", flush=True)
    finally:
        stop()
        stream.close()

if __name__ == "__main__":
    main()
