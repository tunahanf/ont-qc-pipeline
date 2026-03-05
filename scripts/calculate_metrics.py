#!/usr/bin/env python3
"""
calculate_metrics.py — Parse a FASTQ file and compute per-read QC metrics.

Outputs a CSV with columns: read_id, read_length, gc_content_pct, mean_quality

Usage:
    python scripts/calculate_metrics.py <input.fastq> <output.csv>
"""

import sys
import csv


def phred_to_prob(q: int) -> float:
    return 10 ** (-q / 10.0)


def mean_quality_from_string(qual_str: str) -> float:
    """Convert quality string to mean Phred score via error probability averaging."""
    phred_scores = [ord(c) - 33 for c in qual_str]
    if not phred_scores:
        return 0.0
    mean_error_prob = sum(phred_to_prob(q) for q in phred_scores) / len(phred_scores)
    # Back-convert to Phred
    import math
    return -10 * math.log10(mean_error_prob) if mean_error_prob > 0 else 40.0


def calculate_gc(sequence: str) -> float:
    if not sequence:
        return 0.0
    gc = sum(1 for b in sequence.upper() if b in ("G", "C"))
    return (gc / len(sequence)) * 100.0


def parse_fastq(fastq_path: str):
    """Yields (read_id, sequence, quality_string) tuples from a FASTQ file."""
    with open(fastq_path) as f:
        while True:
            header = f.readline().strip()
            if not header:
                break
            sequence = f.readline().strip()
            _ = f.readline()  # '+' line
            quality = f.readline().strip()

            if not header.startswith("@"):
                raise ValueError(f"Malformed FASTQ: expected '@', got '{header}'")

            read_id = header[1:].split()[0]
            yield read_id, sequence, quality


def calculate_metrics(fastq_path: str, output_csv: str) -> None:
    fieldnames = ["read_id", "read_length", "gc_content_pct", "mean_quality"]

    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        count = 0
        for read_id, sequence, quality in parse_fastq(fastq_path):
            if len(sequence) != len(quality):
                print(
                    f"Warning: read {read_id} has mismatched seq/qual lengths, skipping.",
                    file=sys.stderr,
                )
                continue

            writer.writerow(
                {
                    "read_id": read_id,
                    "read_length": len(sequence),
                    "gc_content_pct": round(calculate_gc(sequence), 4),
                    "mean_quality": round(mean_quality_from_string(quality), 4),
                }
            )
            count += 1

    print(f"Processed {count} reads -> {output_csv}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.fastq> <output.csv>", file=sys.stderr)
        sys.exit(1)
    calculate_metrics(sys.argv[1], sys.argv[2])
