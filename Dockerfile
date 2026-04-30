# SPEACE Framework - Full Project Dockerfile
# Build: docker build -t speace .
# Run:   docker run -it --env-file .env speace
#
# For GPU support:
#   docker build --build-arg CUDA=true -t speace:gpu .
#   docker run --gpus all -it speace:gpu

FROM python:3.12-slim AS base

LABEL org.opencontainers.image.title="SPEACE Framework"
LABEL org.opencontainers.image.description="SuPer Autonomous Cybernetic Evolutive Entity — TINA reference implementation"
LABEL org.opencontainers.image.authors="SPEACE Development Team / Rigene Project"
LABEL org.opencontainers.image.licenses="MIT"

ARG CUDA=false

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Core dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Optional ML dependencies
COPY requirements-ml.txt .
RUN if [ "$CUDA" = "true" ]; then \
        echo "Installing ML dependencies (PyTorch, transformers, etc.)..."; \
        pip install --no-cache-dir -r requirements-ml.txt; \
    else \
        echo "Skipping ML dependencies (use --build-arg CUDA=true for GPU)"; \
    fi

COPY . .

RUN mkdir -p data/rl_models vector_data logs

EXPOSE 8000 8003 5000

ENTRYPOINT ["python", "scripts/speace-cli.py"]
CMD ["--help"]
