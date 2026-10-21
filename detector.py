"""Signal one: local GPT-2 contextual predictability, not authorship verification.

The supplied starter maps perplexity to an AI-oriented score. This project
preserves its midpoint (45) and slope (1.6), adds coverage metadata, and uses
safe model loading and bounded concurrent inference. Low perplexity means
predictable tokens, which can occur in both human and generated writing.
Ornate AI text can score human-like; the committed real-model results include
that failure. No accuracy or demographic-performance claim is established.

The model runs locally after its initial download. No hosted inference or API
key is involved. See README.md for score semantics and observed limitations.
"""

import math
import threading

import config

_model = None
_tokenizer = None
_load_lock = threading.Lock()
_inference_lock = threading.Lock()


class DetectorUnavailable(RuntimeError):
    """The model couldn't be loaded — no download yet, or no disk."""


def _load():
    """Load the model once and keep it. First call downloads ~550 MB."""
    with _load_lock:
        return _load_once()


def _load_once():
    global _model, _tokenizer
    if _model is not None:
        return _model, _tokenizer

    try:
        import torch  # noqa: F401
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as exc:
        raise DetectorUnavailable(
            f"transformers or torch isn't installed ({exc}).\n"
            f"Run: pip install -r requirements.txt"
        ) from exc

    try:
        tokenizer = AutoTokenizer.from_pretrained(config.DETECTOR_MODEL)
        model = AutoModelForCausalLM.from_pretrained(config.DETECTOR_MODEL, use_safetensors=True)
        model.eval()
        torch.set_num_threads(min(4, torch.get_num_threads()))
        # Publish both objects only after a successful load.
        _tokenizer, _model = tokenizer, model
    except Exception as exc:  # noqa: BLE001
        raise DetectorUnavailable(
            f"Couldn't load '{config.DETECTOR_MODEL}': {exc}\n"
            f"The first run downloads about 550 MB — check your connection and "
            f"that you have disk space free."
        ) from exc

    return _model, _tokenizer


def _measure(text: str) -> dict:
    """
    How surprised the model is by this text. Lower means more predictable.

    Returns perplexity and coverage metadata from one model invocation.
    """
    import torch

    model, tokenizer = _load()

    tokens = tokenizer.encode(text, add_special_tokens=False, truncation=False)
    input_ids = torch.tensor([tokens[:config.DETECTOR_MAX_TOKENS]], dtype=torch.long)

    # Two tokens is not enough to be surprised by anything.
    if input_ids.shape[1] < 3:
        raise ValueError("Text is too short to score — a few sentences at least.")

    with _inference_lock, torch.inference_mode():
        output = model(input_ids, labels=input_ids)

    # The model's loss here IS mean negative log-likelihood per token.
    loss = float(output.loss.item())
    if not math.isfinite(loss):
        raise DetectorUnavailable("The model returned a non-finite loss.")
    return {"perplexity": math.exp(min(loss, 700)), "tokens_total": len(tokens),
            "tokens_scored": input_ids.shape[1], "truncated": len(tokens) > config.DETECTOR_MAX_TOKENS,
            "model": config.DETECTOR_MODEL, "model_revision": getattr(model.config, "_commit_hash", None),
            "device": str(model.device)}


def perplexity(text: str) -> float:
    return _measure(text)["perplexity"]


def model_signal(text: str) -> float:
    """Return an uncalibrated AI-likeness score; 0.5 is not a probability."""
    return signal_details(text)["model_score"]


def signal_details(text: str) -> dict:
    """One inference, plus coverage evidence for the service's uncertainty gate."""
    details = _measure(text)
    ppl = details["perplexity"]

    midpoint = 45.0    # perplexity that scores 0.5
    steepness = 1.6    # how sharply the score moves either side of it

    # Logistic on log-perplexity. Low perplexity -> high AI score.
    exponent = steepness * (math.log(ppl) - math.log(midpoint))
    score = 1.0 / (1.0 + math.exp(min(700.0, exponent)))
    details["model_score"] = round(min(max(score, 0.0), 1.0), 4)
    return details


def warm_up() -> str:
    """Load the model without scoring anything. Run this before class."""
    _load()
    return f"{config.DETECTOR_MODEL} loaded and ready."


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = (
            "The implementation of the proposed framework requires careful "
            "consideration of several key factors. First, it is important to "
            "note that the system must be able to handle a wide variety of "
            "different inputs. Additionally, the overall performance of the "
            "solution depends on a number of important variables."
        )
        print("(no text given — scoring a sample)\n")

    print(f"Loading {config.DETECTOR_MODEL} (first run downloads ~550 MB)…")
    print(f"perplexity     {perplexity(text):.1f}")
    print(f"model_signal   {model_signal(text):.4f}   (higher = more likely AI)")
