FROM python:3.11-slim

ARG MODEL_VERSION=v1.1.0

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_VERSION=${MODEL_VERSION}

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY policies ./policies
COPY ml_pipeline.py model_gate.py ./

RUN python ml_pipeline.py --model-out models/model.joblib --metrics-out reports/offline_metrics.json && \
    python model_gate.py --metrics reports/offline_metrics.json --policy policies/model_policy.yaml

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
