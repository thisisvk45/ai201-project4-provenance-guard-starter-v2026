"""
Settings for Provenance Guard.

Everything you're likely to change lives here, at the top, on purpose.

Scoring choices were recorded before implementation; rate limiting belongs to Unit 8.
"""

import os
from pathlib import Path

ROOT = Path(__file__).parent


# ─── The service ─────────────────────────────────────────────────────────────

# `127.0.0.1` is loopback — only your own machine can reach it, which is what
# you want all through units 7 and 8. A host somewhere else has to accept
# traffic from outside the box, and that means `0.0.0.0`. Setting the env var
# is how you get it; the default keeps your local `curl` commands unchanged.
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "5000"))

# Flask's debug mode gives anyone who can reach the service an interactive
# Python prompt inside your process. Fine on loopback, a gift to strangers
# anywhere else — so it turns itself off the moment HOST isn't loopback.
DEBUG = os.getenv("AI201_DEBUG", "0") == "1" and HOST in ("127.0.0.1", "localhost")


# ─── The local model ─────────────────────────────────────────────────────────
# Your first signal runs a language model ON YOUR OWN MACHINE. No account, no
# key, no card. It downloads about 550 MB the first time — do that before
# class, not during it.
#
# What it measures: how *predictable* your text is to a language model. Text a
# model finds easy to predict can come from either a person or a model.
#
# The first call is the slow one — ten to twenty seconds while the model loads,
# longer on an older laptop. After that it stays in memory and a submission
# takes a second or two. That cost is part of what you're learning: this is
# what running a model inline in a request actually looks like.

DETECTOR_MODEL = os.getenv("AI201_DETECTOR_MODEL", "gpt2")

# Longer text gives a steadier reading but takes longer. 400 tokens is roughly
# 300 words. Truncated input is explicitly kept in the unsure band.
DETECTOR_MAX_TOKENS = 400


# ─── Scoring (Milestone 4) ───────────────────────────────────────────────────
# How much each signal counts toward the combined score.
#
# Frozen design choices from the first project commit, explained in README.md.

WEIGHT_MODEL_SIGNAL = 0.7
WEIGHT_STYLE_SIGNAL = 0.3
DISAGREEMENT_THRESHOLD = 0.5
DISAGREEMENT_SHRINK = 0.5
WEAK_EVIDENCE_SHRINK = 0.25
MIN_CONFIDENT_WORDS = 40
MIN_CONFIDENT_SENTENCES = 3
MAX_TEXT_CHARS = 10_000
MAX_BODY_BYTES = 65_536
MAX_REASONING_CHARS = 2_000
SCORING_VERSION = "unit7-v1"


# ─── Thresholds (Milestone 5) ────────────────────────────────────────────────
# Scores indicate uncalibrated AI-likeness, not certainty in authorship.
# score <= HUMAN_THRESHOLD -> human estimate
# score >= AI_THRESHOLD    -> AI estimate
# all other valid scores   -> unsure
# A wide unsure band prioritizes avoiding unsupported accusations.

HUMAN_THRESHOLD = 0.25
AI_THRESHOLD = 0.80

# ─── Rate limiting (UNIT 8) ──────────────────────────────────────────────────
# Off in unit 7. You turn it on and choose the numbers in unit 8, Milestone 1.
#
# Think about two people: a real writer submitting their own work a few times
# an hour, and a script sending a thousand variations to map your thresholds.
# Your README has to say why your numbers and not others.

RATE_LIMITING_ENABLED = os.getenv("AI201_RATE_LIMITS", "0") == "1"

RATE_LIMIT_PER_MINUTE = 10
RATE_LIMIT_PER_DAY = 200

# Flask-Limiter warns loudly without this. In-memory is right for one laptop
# and wrong for anything real — a restart forgets every count, and two copies
# of the service wouldn't share limits.
RATE_LIMIT_STORAGE = "memory://"


# ─── Paths ───────────────────────────────────────────────────────────────────

LOG_DIR = Path(os.getenv("AI201_LOG_DIR", str(ROOT / "logs")))
AUDIT_LOG = LOG_DIR / "audit.jsonl"
RESULTS_DIR = ROOT / "results"
