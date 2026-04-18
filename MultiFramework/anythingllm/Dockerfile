FROM python:3.11-slim

LABEL maintainer="SPEACE Cortex <rigeneproject@rigene.eu>"
LABEL description="SPEACE World Model - AnythingLLM REST API"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY MultiFramework/anythingllm/ /app/

# Install Python dependencies
RUN pip install --no-cache-dir \
    flask>=2.3.0 \
    gunicorn>=21.0.0 \
    waitress>=2.1.0

# Create non-root user
RUN useradd -m -u 1000 speace && \
    chown -R speace:speace /app

USER speace

# Expose port
EXPOSE 8003

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8003/health || exit 1

# Run with gunicorn (production) or waitress (Windows compatibility)
CMD ["python", "-m", "MultiFramework.anythingllm.api.server"]
