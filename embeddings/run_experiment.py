from pathlib import Path
import csv
import matplotlib.pyplot as plt
from distance_utils import compute_distance_between_files


def main():
    # Typo levels we want to analyze:
    typo_levels = [0, 10, 20, 30, 40, 50]

    results = []

    for level in typo_levels:
        orig = Path(f"../data/en_input_{level}.txt")
        back = Path(f"../data/en_back_{level}.txt")

        if not orig.exists() or not back.exists():
            print(f"Skipping level {level}%: missing files.")
            continue

        dist, orig_text, back_text = compute_distance_between_files(orig, back)
        results.append((level, dist))

    if not results:
        print("No results to plot (no levels had both files).")
        return

    # Save CSV
    out_csv = Path("../experiments/results.csv")
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    with out_csv.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["typo_percent", "distance"])
        writer.writerows(results)

    # Plot
    xs = [r[0] for r in results]
    ys = [r[1] for r in results]

    plt.figure(figsize=(7, 5))
    plt.plot(xs, ys, marker="o")
    plt.xlabel("Typo Percentage")
    plt.ylabel("Cosine Distance")
    plt.title("Typo % vs Semantic Drift (Round-trip Translation)")
    plt.grid(True)

    out_png = Path("../experiments/typos_vs_distance.png")
    plt.savefig(out_png)

    print("Experiment complete!")
    print(f"CSV saved to: {out_csv}")
    print(f"Plot saved to: {out_png}")


if __name__ == "__main__":
    main()
