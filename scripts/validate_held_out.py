#!/usr/bin/env python3
"""Check the provenance and shape of the Unit 8 held out evaluation set."""

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path


def word_count(text: str) -> int:
    return len(re.findall(r"[^\W_]+(?:['’][^\W_]+)*", text, flags=re.UNICODE))


def load_records(path: Path) -> list[dict]:
    records = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {number} is not valid JSON: {exc.msg}") from exc
        if not isinstance(record, dict):
            raise ValueError(f"line {number} must be a JSON object")
        records.append(record)
    return records


def validate(records: list[dict]) -> list[str]:
    errors = []
    required = ("id", "origin", "source", "verified", "topic", "text")
    identifiers, hashes = set(), set()
    origins, topics = Counter(), {"human": Counter(), "ai": Counter()}

    for number, record in enumerate(records, 1):
        missing = [field for field in required if field not in record]
        if missing:
            errors.append(f"record {number} is missing: {', '.join(missing)}")
            continue
        identifier = record["id"]
        if not isinstance(identifier, str) or not identifier.strip() or identifier in identifiers:
            errors.append(f"record {number} needs a unique nonempty id")
        identifiers.add(identifier)
        origin = record["origin"]
        if origin not in {"human", "ai"}:
            errors.append(f"record {number} has an invalid origin")
            continue
        origins[origin] += 1
        if not isinstance(record["source"], str) or not record["source"].strip():
            errors.append(f"record {number} needs a source description")
        if record["verified"] is not True:
            errors.append(f"record {number} is not marked verified")
        if not isinstance(record["topic"], str) or not record["topic"].strip():
            errors.append(f"record {number} needs a topic")
        else:
            topics[origin][record["topic"].strip().casefold()] += 1
        text = record["text"]
        if not isinstance(text, str):
            errors.append(f"record {number} text must be a string")
            continue
        count = word_count(text)
        if not 50 <= count <= 250:
            errors.append(f"record {number} has {count} words; expected 50 through 250")
        fingerprint = hashlib.sha256(text.strip().casefold().encode("utf-8")).hexdigest()
        if fingerprint in hashes:
            errors.append(f"record {number} repeats text already in the set")
        hashes.add(fingerprint)

    for origin in ("human", "ai"):
        if origins[origin] != 20:
            errors.append(f"expected 20 {origin} records, found {origins[origin]}")
    if set(topics["human"]) != set(topics["ai"]):
        errors.append("human and AI topic labels must match")
    return errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path("evaluation/held_out.jsonl")
    if not path.exists():
        print(f"Missing {path}. Read evaluation/README.md before creating it.")
        return 1
    try:
        records = load_records(path)
    except (OSError, ValueError) as exc:
        print(f"Invalid evaluation file: {exc}")
        return 1
    errors = validate(records)
    if errors:
        print("The held out set is not ready:")
        for error in errors:
            print(f"* {error}")
        return 1
    print("Held out evaluation set is ready: 20 verified human and 20 AI passages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
