# ONT QC Pipeline

A reproducible mini-bioinformatics pipeline for Quality Control analysis of Oxford Nanopore Technology (ONT) long-read sequencing data. Reads are simulated; the pipeline runs end-to-end with Snakemake and can be executed inside Docker for full reproducibility.

---

## Pipeline Overview

```
config.yaml
    |
    v
[simulate_reads] --> data/simulated_reads.fastq
                            |
              +-------------+-------------+
              |                           |
              v                           v
       [nanoplot_qc]           [calculate_metrics]
              |                           |
              v                           v
  results/nanoplot/            results/metrics/read_metrics.csv
  NanoPlot-report.html                    |
                                          v
                               [visualize_metrics]
                                          |
                                          v
                              results/plots/*.png + summary stats
```

---

## Output Files

| Path | Description |
|---|---|
| `data/simulated_reads.fastq` | Simulated ONT reads (1000 reads, lognormal lengths) |
| `results/nanoplot/NanoPlot-report.html` | Interactive NanoPlot QC report (N50, quality, length) |
| `results/metrics/read_metrics.csv` | Per-read: read_id, read_length, gc_content_pct, mean_quality |
| `results/plots/read_length_hist.png` | Read length histogram + KDE |
| `results/plots/gc_content_hist.png` | GC content histogram + KDE |
| `results/plots/mean_quality_hist.png` | Mean quality histogram + KDE |
| `results/plots/qc_metrics_combined.png` | Combined 3-panel figure |

---

## Configuration (`config.yaml`)

| Parameter | Default | Description |
|---|---|---|
| `simulate.num_reads` | 1000 | Number of reads to simulate |
| `simulate.lognormal_mu` | 8.5 | Log-mean for read length distribution |
| `simulate.lognormal_sigma` | 1.0 | Log-std for read length distribution |
| `simulate.gc_min` | 0.40 | Minimum GC content per read |
| `simulate.gc_max` | 0.60 | Maximum GC content per read |
| `simulate.quality_min` | 7 | Minimum Phred quality score |
| `simulate.quality_max` | 20 | Maximum Phred quality score |
| `simulate.seed` | 42 | Random seed for reproducibility |
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
# Check FASTQ has exactly 4000 lines (4 lines × 1000 reads)
wc -l data/simulated_reads.fastq
# Expected: 4000

# Check 1000 read headers
grep -c "^@" data/simulated_reads.fastq
# Expected: 1000

# Check CSV has 1001 lines (header + 1000 rows)
wc -l results/metrics/read_metrics.csv
# Expected: 1001

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
├── data/                        # FASTQ files (git-ignored)
├── results/                     # All outputs (git-ignored)
├── scripts/
│   ├── simulate_reads.py        # ONT-style FASTQ simulation
│   ├── calculate_metrics.py     # Per-read QC metrics (no Biopython)
│   └── visualize_metrics.py     # Histogram/KDE plots + summary stats
├── logs/                        # Snakemake rule logs (git-ignored)
├── Snakefile                    # Pipeline DAG definition
├── Dockerfile                   # Self-contained container image
├── config.yaml                  # All tunable parameters
├── environment.yml              # Conda alternative
└── README.md
```
