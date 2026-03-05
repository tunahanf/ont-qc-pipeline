#!/usr/bin/env python3
"""
simulate_reads.py — Simulates ONT-style long reads and writes a FASTQ file.

Usage:
    python scripts/simulate_reads.py <config.yaml> <output.fastq>
"""

import sys
import yaml
import numpy as np


def simulate_reads(config_path: str, output_path: str) -> None:
    with open(config_path) as f:
        cfg = yaml.safe_load(f)["simulate"]

    rng = np.random.default_rng(cfg.get("seed", 42))

    num_reads = cfg["num_reads"]
    mu = cfg["lognormal_mu"]
    sigma = cfg["lognormal_sigma"]
    gc_min = cfg["gc_min"]
    gc_max = cfg["gc_max"]
    q_min = cfg["quality_min"]
    q_max = cfg["quality_max"]

    # Sample read lengths from lognormal, clip to [1000, 50000]
    raw_lengths = rng.lognormal(mean=mu, sigma=sigma, size=num_reads).astype(int)
    lengths = np.clip(raw_lengths, 1000, 50000)

    with open(output_path, "w") as out:
        for i, length in enumerate(lengths):
            read_id = f"read_{i:06d}"

            # Per-read GC content drawn uniformly in [gc_min, gc_max]
            gc = rng.uniform(gc_min, gc_max)
            at = 1.0 - gc
            # Multinomial base frequencies: G, C, A, T
            probs = [gc / 2, gc / 2, at / 2, at / 2]
            bases = rng.choice(["G", "C", "A", "T"], size=length, p=probs)
            sequence = "".join(bases)

            # Per-base quality scores: Normal(12, 3) clipped to [q_min, q_max]
            raw_quals = rng.normal(loc=12.0, scale=3.0, size=length)
            phred_scores = np.clip(raw_quals, q_min, q_max).astype(int)
            quality_str = "".join(chr(q + 33) for q in phred_scores)

            # Write 4-line FASTQ record
            out.write(f"@{read_id}\n")
            out.write(f"{sequence}\n")
            out.write("+\n")
            out.write(f"{quality_str}\n")

    print(f"Simulated {num_reads} reads -> {output_path}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <config.yaml> <output.fastq>", file=sys.stderr)
        sys.exit(1)
    simulate_reads(sys.argv[1], sys.argv[2])
