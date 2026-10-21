"""Signal two: transparent surface statistics; no authorship verification."""
import json
import re
import statistics
import unicodedata
import config


def sentences(text: str) -> list[str]:
    # Handles closing quotation marks and line boundaries; abbreviations remain a blind spot.
    return [s for s in re.split(r'(?<=[.!?])\s+|(?<=[.!?]["”’])\s+|\n+', text.strip()) if words(s)]


def words(text: str) -> list[str]:
    return re.findall(r"[^\W_]+(?:['’][^\W_]+)*", text.casefold(), flags=re.UNICODE)


def sentence_length_spread(text: str) -> float:
    counts = [len(words(s)) for s in sentences(text)]
    return statistics.pstdev(counts) / statistics.mean(counts) if len(counts) >= 2 else 0.0


def type_token_ratio(text: str) -> float:
    tokens = words(text)
    return len(set(tokens)) / len(tokens) if tokens else 0.0


def windowed_type_token_ratio(text: str) -> float:
    tokens = words(text)
    windows = [tokens[i:i + 50] for i in range(0, len(tokens), 50)]
    # Weight by window length so a tiny tail does not count as a whole window.
    return sum(len(set(w)) for w in windows) / len(tokens) if tokens else 0.0


def punctuation_density(text: str) -> float:
    n = len(words(text))
    return sum(unicodedata.category(c).startswith("P") for c in text) / n if n else 0.0


def style_details(text: str) -> dict:
    n_words, n_sentences = len(words(text)), len(sentences(text))
    spread = sentence_length_spread(text)
    variety = windowed_type_token_ratio(text)
    punctuation = punctuation_density(text)
    components = {
        "uniformity": max(0.0, 1.0 - spread),
        "repetition": min(1.0, max(0.0, (0.9 - variety) / 0.5)),
        "sparse_punctuation": max(0.0, 1.0 - punctuation / 0.3),
    }
    sufficient = n_words >= config.MIN_CONFIDENT_WORDS and n_sentences >= config.MIN_CONFIDENT_SENTENCES
    score = (0.55 * components["uniformity"] + 0.30 * components["repetition"]
             + 0.15 * components["sparse_punctuation"]) if sufficient else 0.5
    return {
        "style_score": round(score, 4), "word_count": n_words,
        "sentence_count": n_sentences, "sufficient_evidence": sufficient,
        "sentence_length_spread": round(spread, 6),
        "type_token_ratio": round(type_token_ratio(text), 6),
        "windowed_type_token_ratio": round(variety, 6),
        "punctuation_density": round(punctuation, 6),
        "components": {k: round(v, 6) for k, v in components.items()},
    }


def style_signal(text: str) -> float:
    return style_details(text)["style_score"]


if __name__ == "__main__":
    import sys
    print(json.dumps(style_details(" ".join(sys.argv[1:]) or "A short sample."), indent=2))
