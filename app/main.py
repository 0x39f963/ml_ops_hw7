from __future__ import annotations

import os
from time import perf_counter

from fastapi import FastAPI
from prometheus_client import Counter, Histogram, make_asgi_app
from pydantic import BaseModel, Field
from sklearn.datasets import load_iris

from app.model_io import load_model, normalize_features

APP_VERSION = os.getenv("MODEL_VERSION", "v1.1.0")

REQUEST_COUNT = Counter(
    "hw7_predict_requests_total",
    "Total predict requests served by the HW7 ML service.",
)
REQUEST_LATENCY = Histogram(
    "hw7_predict_latency_seconds",
    "Predict endpoint latency in seconds.",
)

app = FastAPI(title="HW7 ML Deployment Service", version=APP_VERSION)
app.mount("/metrics", make_asgi_app())

model = load_model()
target_names = load_iris().target_names


class PredictRequest(BaseModel):
    x: list[float] = Field(
        ...,
        min_length=1,
        max_length=4,
        description="Iris-like numeric features. Short demo vectors are padded to 4 values.",
    )


class PredictResponse(BaseModel):
    prediction: int
    label: str
    version: str
    input_features: list[float]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": APP_VERSION}


@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest) -> PredictResponse:
    started = perf_counter()
    features = normalize_features(payload.x)
    pred = int(model.predict(features)[0])
    REQUEST_COUNT.inc()
    REQUEST_LATENCY.observe(perf_counter() - started)
    return PredictResponse(
        prediction=pred,
        label=str(target_names[pred]),
        version=APP_VERSION,
        input_features=features.flatten().tolist(),
    )
