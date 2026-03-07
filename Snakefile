configfile: "config.yaml"


rule all:
    input:
        "results/nanoplot/NanoPlot-report.html",
        expand("results/plots/{plot}.png", plot=[
            "read_length_hist",
            "gc_content_hist",
            "mean_quality_hist",
            "qc_metrics_combined",
        ]),


rule nanoplot_qc:
    input:
        "barcode77.fastq",
    output:
        "results/nanoplot/NanoPlot-report.html",
    log:
        "logs/nanoplot_qc.log",
    params:
        threads=config["nanoplot"]["threads"],
        outdir="results/nanoplot",
    shell:
        """
        NanoPlot \
            --fastq {input} \
            --outdir {params.outdir} \
            --threads {params.threads} \
            --plots dot \
            --N50 \
            > {log} 2>&1
        """


rule calculate_metrics:
    input:
        "barcode77.fastq",
    output:
        "results/metrics/read_metrics.csv",
    log:
        "logs/calculate_metrics.log",
    shell:
        """
        mkdir -p results/metrics
        python scripts/calculate_metrics.py {input} {output} > {log} 2>&1
        """


rule visualize_metrics:
    input:
        "results/metrics/read_metrics.csv",
    output:
        expand("results/plots/{plot}.png", plot=[
            "read_length_hist",
            "gc_content_hist",
            "mean_quality_hist",
            "qc_metrics_combined",
        ]),
    log:
        "logs/visualize_metrics.log",
    shell:
        """
        python scripts/visualize_metrics.py {input} results/plots > {log} 2>&1
        """
