import csv
import matplotlib.pyplot as plt
from pathlib import Path
from distance_utils import compute_distance_between_files


def main():
    typo_levels = [0, 20, 40]
    results = []

    for level in typo_levels:
        orig = f"../data/en_input_{level}.txt"
        back = f"../data/en_back_{level}.txt"

        dist, orig_text, back_text = compute_distance_between_files(orig, back)
        results.append((level, dist))

    # Save CSV
    out_csv = "../experiments/results.csv"
    with open(out_csv, "w", newline="") as f:
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

    out_png = "../experiments/typos_vs_distance.png"
    plt.savefig(out_png)

    print("Experiment complete!")
    print(f"CSV saved to: {out_csv}")
    print(f"Plot saved to: {out_png}")


if __name__ == "__main__":
    main()
