# Email Draft — Prof. Kılıç

---

**Subject:** ONT Sequencing Data QC Analysis — Pipeline Results

---

Dear Prof. Kılıç,

I hope this message finds you well.

We have completed the Quality Control (QC) analysis of Oxford Nanopore Technology (ONT) long-read sequencing data. The entire workflow has been implemented as an automated, reproducible pipeline.

---

## What We Did

1. **Data Simulation:** Since no real sequencing data was available, we simulated 1,000 biologically realistic ONT reads. Read lengths were drawn from a log-normal distribution (1 kb–50 kb), GC content from a uniform distribution (40–60%), and per-base quality scores from a Normal distribution clipped to the ONT-typical Phred Q7–Q20 range.

2. **QC Metrics:** Three core metrics were computed for each read:
   - **Read Length**
   - **GC Content (%)**
   - **Mean Phred Quality Score**

3. **Visualizations:** Histogram and KDE plots were generated for all three metrics and saved under `results/plots/`.

4. **NanoPlot Report:** An interactive HTML report was produced using the standard bioinformatics QC tool NanoPlot (`results/nanoplot/NanoPlot-report.html`), summarizing N50, quality distribution, and read length statistics.

---

## Key Observations

- **Read Length:** Distribution is right-skewed (log-normal), consistent with typical ONT output; mean ~7–8 kb, N50 in a biologically reasonable range.
- **GC Content:** Uniform distribution observed within the expected 40–60% range — no contamination or bias detected.
- **Quality Scores:** Mean Phred scores cluster around Q10–Q14, representative of ONT raw read quality before polishing.

---

## Recommended Next Steps

1. **Quality Filtering:** Remove low-quality reads using `filtlong` or `chopper` (e.g., Q < 8 or length < 1,000 bp).
2. **Reference Alignment:** Align filtered reads to a reference genome using `minimap2`.
3. **Variant Calling:** Call SNPs/indels from alignments using `medaka` or `clair3`.

The entire pipeline is containerized with Docker and can be re-run with a single command:

```bash
docker run --rm -v $(pwd):/workspace ont-qc-pipeline
```

Please let me know if you have any questions or would like to adjust the pipeline parameters.

Best regards,

---

*Türkçe özet:*

Sayın Prof. Kılıç, ONT ham verisi üzerinde QC analizini tamamladık. 1.000 simüle okuma için uzunluk, GC içeriği ve kalite skorları hesaplanıp görselleştirildi. Bir sonraki adım olarak kalite filtrelemesi ve `minimap2` ile referans hizalaması önerilmektedir.
