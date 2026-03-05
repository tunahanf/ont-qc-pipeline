#!/usr/bin/env python3
"""
visualize_metrics.py — Generate QC plots from read_metrics.csv.

Produces:
  - results/plots/read_length_hist.png
  - results/plots/gc_content_hist.png
  - results/plots/mean_quality_hist.png
  - results/plots/qc_metrics_combined.png

And prints summary statistics to stdout.

Usage:
    python scripts/visualize_metrics.py <input.csv> <output_dir>
"""

import matplotlib
matplotlib.use("Agg")  # Must be first — no display server in Docker

import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


METRICS = [
    {
        "col": "read_length",
        "title": "Read Length Distribution",
        "xlabel": "Read Length (bp)",
        "color": "steelblue",
        "filename": "read_length_hist.png",
    },
    {
        "col": "gc_content_pct",
        "title": "GC Content Distribution",
        "xlabel": "GC Content (%)",
        "color": "mediumseagreen",
        "filename": "gc_content_hist.png",
    },
    {
        "col": "mean_quality",
        "title": "Mean Read Quality Distribution",
        "xlabel": "Mean Phred Quality Score",
        "color": "coral",
        "filename": "mean_quality_hist.png",
    },
]


def plot_metric(ax, series, title, xlabel, color):
    mean_val = series.mean()
    median_val = series.median()

    sns.histplot(series, kde=True, ax=ax, color=color, edgecolor="white", linewidth=0.5)
    ax.axvline(mean_val, color="navy", linestyle="--", linewidth=1.5, label=f"Mean: {mean_val:.2f}")
    ax.axvline(median_val, color="darkred", linestyle=":", linewidth=1.5, label=f"Median: {median_val:.2f}")

    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel("Count", fontsize=11)
    ax.legend(fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def visualize_metrics(csv_path: str, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} reads from {csv_path}\n")

    # --- Summary statistics ---
    print("=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    for m in METRICS:
        col = m["col"]
        s = df[col]
        print(f"\n{m['title']}")
        print(f"  Count  : {s.count()}")
        print(f"  Mean   : {s.mean():.4f}")
        print(f"  Median : {s.median():.4f}")
        print(f"  Std    : {s.std():.4f}")
        print(f"  Min    : {s.min():.4f}")
        print(f"  Q25    : {s.quantile(0.25):.4f}")
        print(f"  Q75    : {s.quantile(0.75):.4f}")
        print(f"  Max    : {s.max():.4f}")
    print("=" * 60)

    # --- Individual plots ---
    for m in METRICS:
        fig, ax = plt.subplots(figsize=(8, 5))
        plot_metric(ax, df[m["col"]], m["title"], m["xlabel"], m["color"])
        fig.tight_layout()
        out_path = os.path.join(output_dir, m["filename"])
        fig.savefig(out_path, dpi=150)
        plt.close(fig)
        print(f"Saved: {out_path}", file=sys.stderr)

    # --- Combined 3-panel figure ---
    fig, axes = plt.subplots(1, 3, figsize=(20, 5))
    fig.suptitle("ONT Read QC Metrics Overview", fontsize=15, fontweight="bold", y=1.02)
    for ax, m in zip(axes, METRICS):
        plot_metric(ax, df[m["col"]], m["title"], m["xlabel"], m["color"])
    fig.tight_layout()
    combined_path = os.path.join(output_dir, "qc_metrics_combined.png")
    fig.savefig(combined_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {combined_path}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.csv> <output_dir>", file=sys.stderr)
        sys.exit(1)
    visualize_metrics(sys.argv[1], sys.argv[2])
