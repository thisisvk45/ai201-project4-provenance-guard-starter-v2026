#!/usr/bin/env python3
"""Run the frozen Unit 8 evaluation corpus and write an evidence report.

The corpus stays separate from development fixtures. Each passage receives a
new creator ID in every trial, so the service rate limit does not turn a model
measurement into a rate limit result.
"""

import argparse
import datetime as dt
import hashlib
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config
from validate_held_out import load_records, validate


def corpus_fingerprint(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def safe_json(response):
    try:
        value = response.json()
    except ValueError:
        return {"unreadable_response": response.text[:300]}
    return value if isinstance(value, dict) else {"response": value}


def submit_trial(records, trial, base_url, timeout, requests):
    rows = []
    for record in records:
        body = {
            "text": record["text"],
            "creator_id": f"heldout_t{trial}_{record['id']}",
        }
        row = {
            "id": record["id"],
            "origin": record["origin"],
            "topic": record["topic"],
        }
        try:
            response = requests.post(f"{base_url}/submit", json=body, timeout=timeout)
            payload = safe_json(response)
            row.update({
                "status": response.status_code,
                "guess": payload.get("guess"),
                "combined_score": payload.get("combined_score"),
                "model_score": payload.get("model_score"),
                "style_score": payload.get("style_score"),
                "error": payload.get("error"),
            })
        except requests.RequestException as exc:
            row.update({"status": None, "error": f"{type(exc).__name__}: {exc}"})
        rows.append(row)
    return rows


def summarize(trial, rows):
    humans = [row for row in rows if row["origin"] == "human"]
    generated = [row for row in rows if row["origin"] == "ai"]
    accepted = [row for row in rows if row.get("status") == 201 and number(row.get("combined_score"))]
    human_scores = [row["combined_score"] for row in humans if row.get("status") == 201 and number(row.get("combined_score"))]
    ai_scores = [row["combined_score"] for row in generated if row.get("status") == 201 and number(row.get("combined_score"))]
    false_accusations = [row["id"] for row in humans if row.get("guess") == "ai"]
    transport_ok = len(accepted) == 40
    enough_scores = len(human_scores) == 20 and len(ai_scores) == 20
    human_median = statistics.median(human_scores) if human_scores else None
    ai_median = statistics.median(ai_scores) if ai_scores else None
    difference = ai_median - human_median if enough_scores else None
    criterion_one = transport_ok and len(false_accusations) <= 1
    criterion_two = transport_ok and difference is not None and difference >= 0.20
    return {
        "trial": trial,
        "accepted": len(accepted),
        "human_false_accusations": len(false_accusations),
        "false_accusation_ids": false_accusations,
        "human_median": human_median,
        "ai_median": ai_median,
        "median_difference": difference,
        "criterion_1_pass": criterion_one,
        "criterion_2_pass": criterion_two,
        "rows": rows,
    }


def display_score(value):
    return f"{value:.6f}" if number(value) else "not available"


def write_report(path, source_path, fingerprint, base_url, trials):
    one_pass = all(trial["criterion_1_pass"] for trial in trials)
    two_pass = all(trial["criterion_2_pass"] for trial in trials)
    lines = [
        "# Held Out Evaluation",
        "",
        "This report records real local service calls against the frozen evaluation corpus. It does not claim that a score proves authorship.",
        "",
        "## Run Details",
        "",
        f"Corpus: `{source_path}`",
        "",
        f"Corpus SHA256: `{fingerprint}`",
        "",
        f"Service: `{base_url}`",
        "",
        f"Trials: {len(trials)}",
        "",
        "## Results",
        "",
        "| Trial | Accepted | Human passages called AI | Human median | AI median | Difference | Criterion 1 | Criterion 2 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for trial in trials:
        lines.append(
            "| {trial} | {accepted}/40 | {false_accusations} | {human_median} | {ai_median} | {difference} | {one} | {two} |".format(
                trial=trial["trial"],
                accepted=trial["accepted"],
                false_accusations=trial["human_false_accusations"],
                human_median=display_score(trial["human_median"]),
                ai_median=display_score(trial["ai_median"]),
                difference=display_score(trial["median_difference"]),
                one="pass" if trial["criterion_1_pass"] else "not met",
                two="pass" if trial["criterion_2_pass"] else "not met",
            )
        )
    lines += [
        "",
        "Criterion 1 passes only when all 20 human passages receive valid responses and no more than one is labelled AI.",
        "",
        "Criterion 2 passes only when all 40 passages receive valid responses and the AI median is at least 0.20 above the human median.",
        "",
        f"Criterion 1 overall: {'pass' if one_pass else 'not met'}.",
        "",
        f"Criterion 2 overall: {'pass' if two_pass else 'not met'}.",
        "",
        "## Exact Trial Data",
        "",
    ]
    for trial in trials:
        lines += [f"### Trial {trial['trial']}", "", "```json", json.dumps(trial, indent=2), "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=Path("evaluation/held_out.jsonl"))
    parser.add_argument("--url", default=f"http://{config.HOST}:{config.PORT}")
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--timeout", type=float, default=90.0)
    parser.add_argument("--label", default="after")
    args = parser.parse_args()

    if args.trials < 3:
        raise SystemExit("Use at least three trials for the Unit 8 criteria.")
    if not args.corpus.exists():
        raise SystemExit(f"Missing corpus: {args.corpus}")
    records = load_records(args.corpus)
    errors = validate(records)
    if errors:
        raise SystemExit("Corpus is not ready:\n" + "\n".join(errors))
    try:
        import requests
        health = requests.get(f"{args.url}/health", timeout=5)
        health.raise_for_status()
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"Service is not ready at {args.url}: {exc}") from exc

    trials = []
    for trial in range(1, args.trials + 1):
        print(f"Running trial {trial} of {args.trials}")
        trials.append(summarize(trial, submit_trial(records, trial, args.url, args.timeout, requests)))

    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    report = config.RESULTS_DIR / f"held_out_evaluation_{stamp}{label}.md"
    write_report(report, args.corpus, corpus_fingerprint(args.corpus), args.url, trials)
    print(f"Wrote {report}")
    for trial in trials:
        print(
            f"Trial {trial['trial']}: criterion 1 {'pass' if trial['criterion_1_pass'] else 'not met'}; "
            f"criterion 2 {'pass' if trial['criterion_2_pass'] else 'not met'}; "
            f"difference {display_score(trial['median_difference'])}"
        )


if __name__ == "__main__":
    main()
