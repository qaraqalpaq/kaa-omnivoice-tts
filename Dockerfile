ARG PYTHON_IMAGE=python:3.12-slim
FROM ${PYTHON_IMAGE}

ARG DEVICE=cpu
ARG TORCH_INDEX_CPU=https://download.pytorch.org/whl/cpu
ARG TORCH_INDEX_CUDA=https://download.pytorch.org/whl/cu128

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    HF_HOME=/cache/huggingface \
    KAA_TTS_HOST=0.0.0.0 \
    KAA_TTS_PORT=7861

RUN set -eux; \
    if [ "$DEVICE" = "cuda" ]; then index="$TORCH_INDEX_CUDA"; else index="$TORCH_INDEX_CPU"; fi; \
    pip install --index-url "$index" torch torchaudio

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN useradd --create-home --uid 10001 app && mkdir -p /cache && chown app:app /cache
COPY --chown=app:app . .
USER app
VOLUME ["/cache"]

EXPOSE 7861
HEALTHCHECK --interval=30s --timeout=10s --start-period=900s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen(f'http://127.0.0.1:{os.environ[\"KAA_TTS_PORT\"]}/health', timeout=5)"

CMD ["python", "app.py"]
