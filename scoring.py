"""Uncalibrated AI-likeness, with explicit abstention for weak evidence."""
import math
import config

LABELS = {
    "human": "This writing shows patterns often found in human writing. This automated estimate does not verify who wrote it. You can request a review if it seems wrong.",
    "unsure": "We cannot reliably tell how this writing was produced. No conclusion about authorship has been made. You can request a review.",
    "ai": "This writing shows patterns often found in AI-generated text. This is an automated estimate, not proof of authorship. If this seems wrong, you can request a review.",
}


def valid_score(value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("A signal must be a finite number in [0, 1].")
    if not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError("A signal must be a finite number in [0, 1].")
    return float(value)


def combine_signals(model_score: float, style_score: float) -> float:
    model_score, style_score = valid_score(model_score), valid_score(style_score)
    weights = (config.WEIGHT_MODEL_SIGNAL, config.WEIGHT_STYLE_SIGNAL)
    if any(not math.isfinite(w) or w < 0 for w in weights) or not math.isclose(sum(weights), 1.0):
        raise ValueError("Signal weights must be nonnegative and sum to one.")
    score = weights[0] * model_score + weights[1] * style_score
    if abs(model_score - style_score) > config.DISAGREEMENT_THRESHOLD:
        score = 0.5 + config.DISAGREEMENT_SHRINK * (score - 0.5)
    return valid_score(score)


def decision_score(model_score: float, style_score: float, *, weak_evidence: bool) -> float:
    score = combine_signals(model_score, style_score)
    if weak_evidence:
        score = 0.5 + config.WEAK_EVIDENCE_SHRINK * (score - 0.5)
    return round(valid_score(score), 6)


def score_to_label(score: float) -> tuple[str, str]:
    score = valid_score(score)
    if not 0 <= config.HUMAN_THRESHOLD < config.AI_THRESHOLD <= 1:
        raise ValueError("Thresholds must define three nonoverlapping bands.")
    guess = "human" if score <= config.HUMAN_THRESHOLD else "ai" if score >= config.AI_THRESHOLD else "unsure"
    return guess, LABELS[guess]


def label_ranges() -> list[tuple[str, str]]:
    return [
        ("high-confidence human", f"0 <= score <= {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f"{config.HUMAN_THRESHOLD:.2f} < score < {config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} <= score <= 1"),
    ]
