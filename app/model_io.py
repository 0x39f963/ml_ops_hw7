from __future__ import annotations

import os
from pathlib import Path

import joblib
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

MODEL_PATH = Path(os.getenv("MODEL_PATH", "models/model.joblib"))


def train_default_model(random_state: int = 42) -> RandomForestClassifier:
    iris = load_iris()
    x_train, _, y_train, _ = train_test_split(
        iris.data,
        iris.target,
        test_size=0.2,
        random_state=random_state,
        stratify=iris.target,
    )
    model = RandomForestClassifier(n_estimators=100, random_state=random_state)
    model.fit(x_train, y_train)
    return model


def load_model() -> RandomForestClassifier:
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return train_default_model()


def normalize_features(values: list[float]) -> np.ndarray:
    if len(values) != 4:
        padded = (values + [0.0, 0.0, 0.0, 0.0])[:4]
        values = padded
    return np.array(values, dtype=float).reshape(1, -1)
