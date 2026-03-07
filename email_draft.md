# Email Draft — Prof. Kılıç

---

**Subject:** ONT Sequencing Data QC Analysis — Pipeline Results

---

Dear Prof. Kılıç,

I hope this message finds you well.

We have completed the Quality Control (QC) analysis of the Oxford Nanopore Technology (ONT) long-read sequencing dataset (`barcode77.fastq`). The entire workflow has been implemented as an automated, reproducible pipeline using Snakemake and Docker.

---

## What We Did

1. **Input Data:** Real ONT sequencing data (`barcode77.fastq`, 81,011 reads, ~84.1 Mbp total yield) was used directly as input. No simulation was performed.

2. **QC Metrics:** Three core metrics were computed per read using a custom parser (no Biopython dependency):
   - **Read Length**
   - **GC Content (%)**
   - **Mean Phred Quality Score** (error-probability averaged)

3. **Visualizations:** Histogram and KDE plots were generated for all three metrics (`results/plots/`).

4. **NanoPlot Report:** An interactive HTML report was produced using NanoPlot v1.42.0 (`results/nanoplot/NanoPlot-report.html`), providing N50, quality distribution, and read length statistics.

---

## Key Results

| Metric | Value |
|---|---|
| Total reads | 81,011 |
| Total yield | ~84.1 Mbp |
| Mean read length | 1,038 bp |
| Median read length | 547 bp |
| N50 | 1,761 bp |
| Longest read | 686,155 bp |
| Mean Phred quality | Q10.1 |
| Median Phred quality | Q9.9 |
| Reads passing Q≥10 | 39,370 (48.6%) |
| Reads passing Q≥7 | 63,671 (78.6%) |
| Reads ≥ 1,000 bp | 21,802 (26.9%) |
| Mean GC content | 53.0% |

The read length distribution is heavily right-skewed, with the majority of reads below 1 kb but a long tail extending to 686 kb — consistent with typical ONT raw output. Quality scores cluster around Q10, within the expected range for ONT reads prior to any polishing step.

---

## Recommended Next Steps

1. **Quality Filtering:** Remove low-quality and short reads using `filtlong` or `chopper` (recommended thresholds: Q ≥ 10, length ≥ 1,000 bp — retains ~26.9% of reads at higher confidence).
2. **Reference Alignment:** Align filtered reads to a reference genome using `minimap2`.
3. **Variant Calling:** Call SNPs/indels from alignments using `medaka` or `clair3`.

The entire pipeline is containerized with Docker and can be re-run with a single command:

```bash
docker run --rm -v $(pwd):/workspace ont-qc-pipeline
```

All outputs (NanoPlot report, per-read metrics CSV, and QC plots) are available in the `results/` directory.

Please let me know if you have any questions or would like to adjust the analysis parameters.

Best regards,

---

*Türkçe özet:*

Sayın Prof. Kılıç, `barcode77.fastq` adlı gerçek ONT ham verisi (81.011 okuma, ~84,1 Mbp) üzerinde QC analizini tamamladık. Ortalama okuma uzunluğu 1.038 bp, N50 1.761 bp, ortalama kalite skoru Q10,1 olarak ölçüldü. Okumaların %78,6'sı Q≥7 eşiğini, %26,9'u ise 1.000 bp uzunluk eşiğini geçmektedir. Bir sonraki adım olarak kalite filtrelemesi ve `minimap2` ile referans hizalaması önerilmektedir.
