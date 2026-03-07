# ONT QC Pipeline

A reproducible mini-bioinformatics pipeline for Quality Control analysis of Oxford Nanopore Technology (ONT) long-read sequencing data. The pipeline processes real ONT sequencing data (`barcode77.fastq`) end-to-end with Snakemake and can be executed inside Docker for full reproducibility.

---

## Pipeline Overview

```
barcode77.fastq (real ONT data, 81,011 reads)
        |
        +------------------+
        |                  |
        v                  v
 [nanoplot_qc]    [calculate_metrics]
        |                  |
        v                  v
results/nanoplot/  results/metrics/read_metrics.csv
NanoPlot-report.html       |
                           v
                  [visualize_metrics]
                           |
                           v
               results/plots/*.png
```

---

## Output Files

| Path | Description |
|---|---|
| `results/nanoplot/NanoPlot-report.html` | Interactive NanoPlot QC report (N50, quality, length) |
| `results/metrics/read_metrics.csv` | Per-read: read_id, read_length, gc_content_pct, mean_quality |
| `results/plots/read_length_hist.png` | Read length histogram + KDE |
| `results/plots/gc_content_hist.png` | GC content histogram + KDE |
| `results/plots/mean_quality_hist.png` | Mean quality histogram + KDE |
| `results/plots/qc_metrics_combined.png` | Combined 3-panel figure |

---

## Input Data

Place `barcode77.fastq` in the project root before running. This file is git-ignored due to its size (~191 MB, 81,011 reads).

---

## Configuration (`config.yaml`)

| Parameter | Default | Description |
|---|---|---|
| `nanoplot.threads` | 4 | CPU threads for NanoPlot |

---

## Running with Docker (Recommended)

### 1. Build the image

```bash
docker build -t ont-qc-pipeline .
```

### 2. Run the full pipeline

```bash
# Linux / macOS / Git Bash
docker run --rm -v $(pwd):/workspace ont-qc-pipeline

# PowerShell (Windows)
docker run --rm -v ${PWD}:/workspace ont-qc-pipeline

# CMD (Windows)
docker run --rm -v %cd%:/workspace ont-qc-pipeline
```

### 3. Dry-run (preview DAG without executing)

```bash
docker run --rm -v $(pwd):/workspace ont-qc-pipeline snakemake --cores 4 --dry-run
```

---

## Running Locally (Conda)

```bash
# Create and activate environment
conda env create -f environment.yml
conda activate ont-qc

# Run pipeline
snakemake --cores 4

# Dry-run
snakemake --cores 4 --dry-run
```

---

## Verification

```bash
# Check read count (expect 81,011 headers)
grep -c "^@" barcode77.fastq

# Check CSV has 81,012 lines (header + 81,011 rows)
wc -l results/metrics/read_metrics.csv

# Check plots were created
ls results/plots/*.png
# Expected: 4 PNG files

# Re-running should do nothing
snakemake --cores 4
# Expected: Nothing to be done.
```

---

## Project Structure

```
ont-qc-pipeline/
├── barcode77.fastq              # Real ONT reads (git-ignored, place here before running)
├── data/                        # Additional FASTQ files (git-ignored)
├── results/                     # All outputs (git-ignored)
├── scripts/
│   ├── calculate_metrics.py     # Per-read QC metrics (no Biopython)
│   └── visualize_metrics.py     # Histogram/KDE plots + summary stats
├── logs/                        # Snakemake rule logs (git-ignored)
├── Snakefile                    # Pipeline DAG definition
├── Dockerfile                   # Self-contained container image
├── config.yaml                  # All tunable parameters
├── environment.yml              # Conda alternative
└── README.md
```
