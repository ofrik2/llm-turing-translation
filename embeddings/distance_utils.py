import string
import numpy as np
from pathlib import Path


def get_embedding(text: str):
    """
    Very simple embedding: 26-dimensional vector (a-z letter counts).
    Allowed because it's part of embedding & measurement only.
    """
    text = text.lower()
    letters = string.ascii_lowercase
    vec = [0] * len(letters)
    index = {ch: i for i, ch in enumerate(letters)}

    for ch in text:
        if ch in index:
            vec[index[ch]] += 1

    return np.array(vec, dtype=float)


def cosine_distance(v1, v2) -> float:
    num = float(np.dot(v1, v2))
    den = float(np.linalg.norm(v1) * np.linalg.norm(v2))
    if den == 0:
        return 1.0
    return 1.0 - (num / den)


def compute_distance_between_files(original_file, back_file):
    """
    Reads both files, computes embeddings, returns cosine distance.
    """
    orig_text = Path(original_file).read_text(encoding="utf-8").strip()
    back_text = Path(back_file).read_text(encoding="utf-8").strip()

    emb_orig = get_embedding(orig_text)
    emb_back = get_embedding(back_text)

    return cosine_distance(emb_orig, emb_back), orig_text, back_text
