FROM python:3.11-slim-bookworm

# Install system dependencies needed by some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        libfreetype6-dev \
        libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies with pinned versions
RUN pip install --no-cache-dir \
    snakemake==7.32.4 \
    pulp==2.7.0 \
    NanoPlot==1.42.0 \
    kaleido==0.1.0 \
    plotly==5.9.0 \
    pandas==2.2.2 \
    matplotlib==3.9.0 \
    seaborn==0.13.2 \
    numpy==1.26.4 \
    PyYAML==6.0.1

WORKDIR /workspace

# Runtime: mount the project directory here with -v $(pwd):/workspace
CMD ["snakemake", "--cores", "4"]
