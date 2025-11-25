import csv
from pathlib import Path
import string


import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# 1. CONFIG
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
EXPERIMENTS_DIR = BASE_DIR / "experiments"
EXPERIMENTS_DIR.mkdir(exist_ok=True, parents=True)

# Define typo levels used in the experiment
TYPO_LEVELS = [0, 20, 40]

RESULTS_CSV = EXPERIMENTS_DIR / "results.csv"
PLOT_PATH = EXPERIMENTS_DIR / "typos_vs_distance.png"


# -----------------------------
# 2. EMBEDDINGS: FILL THIS IN
# -----------------------------

def get_embedding(text: str):
    """
    Very simple, self-contained embedding:
    26-dimensional vector with counts of letters a-z (case-insensitive).

    This is not a 'real' semantic LLM embedding, but it:
    - is numeric,
    - is deterministic,
    - works with cosine distance,
    - requires no external API.

    You can later replace this with a real embedding model if needed.
    """
    text = text.lower()
    letters = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
    vec = [0] * len(letters)
    index = {ch: i for i, ch in enumerate(letters)}

    for ch in text:
        if ch in index:
            vec[index[ch]] += 1

    return vec


# -----------------------------
# 3. DISTANCE FUNCTION
# -----------------------------

def cosine_distance(v1, v2) -> float:
    v1 = np.array(v1, dtype=float)
    v2 = np.array(v2, dtype=float)
    num = float(np.dot(v1, v2))
    den = float(np.linalg.norm(v1) * np.linalg.norm(v2))
    if den == 0.0:
        return 1.0
    return 1.0 - (num / den)


# -----------------------------
# 4. MAIN LOGIC
# -----------------------------

def main():
    rows = []

    for typo in TYPO_LEVELS:
        en_original_path = DATA_DIR / f"en_input_{typo}.txt"
        en_back_path = DATA_DIR / f"en_back_{typo}.txt"

        if not en_original_path.exists():
            raise FileNotFoundError(f"Missing file: {en_original_path}")
        if not en_back_path.exists():
            raise FileNotFoundError(
                f"Missing file: {en_back_path}. "
                "Did you run the translation pipeline first?"
            )

        with en_original_path.open("r", encoding="utf-8") as f:
            original_text = f.read().strip()

        with en_back_path.open("r", encoding="utf-8") as f:
            back_text = f.read().strip()

        print(f"Computing embeddings for typo level {typo}%...")
        emb_original = get_embedding(original_text)
        emb_back = get_embedding(back_text)

        dist = cosine_distance(emb_original, emb_back)
        print(f"Typo {typo}% -> distance = {dist:.4f}")

        rows.append({"typo_percent": typo, "distance": dist})

    # Save CSV
    with RESULTS_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["typo_percent", "distance"])
        writer.writeheader()
        writer.writerows(rows)

    # Plot
    typo_values = [r["typo_percent"] for r in rows]
    dist_values = [r["distance"] for r in rows]

    plt.figure()
    plt.plot(typo_values, dist_values, marker="o")
    plt.xlabel("Typo percentage (%)")
    plt.ylabel("Embedding distance (cosine)")
    plt.title("Typo percentage vs semantic distance after round-trip translation")
    plt.grid(True)
    plt.savefig(PLOT_PATH, bbox_inches="tight", dpi=200)

    print(f"\nSaved results to {RESULTS_CSV}")
    print(f"Saved plot to {PLOT_PATH}")


if __name__ == "__main__":
    main()
