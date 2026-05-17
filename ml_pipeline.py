from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def train_model(model_out: Path, metrics_out: Path, random_state: int = 42) -> dict[str, float | str]:
    iris = load_iris()
    x_train, x_test, y_train, y_test = train_test_split(
        iris.data,
        iris.target,
        test_size=0.2,
        random_state=random_state,
        stratify=iris.target,
    )

    model = RandomForestClassifier(n_estimators=100, random_state=random_state)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)

    model_out.parent.mkdir(parents=True, exist_ok=True)
    metrics_out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_out)

    metrics = {
        "dataset": "sklearn.datasets.load_iris",
        "model_type": "RandomForestClassifier",
        "random_state": random_state,
        "n_estimators": 100,
        "test_size": 0.2,
        "accuracy": round(float(accuracy), 6),
        "model_path": str(model_out),
    }
    metrics_out.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Train deterministic HW7 demo ML model.")
    parser.add_argument("--model-out", default="models/model.joblib")
    parser.add_argument("--metrics-out", default="reports/offline_metrics.json")
    args = parser.parse_args()

    metrics = train_model(Path(args.model_out), Path(args.metrics_out))
    print(f"accuracy={metrics['accuracy']:.4f}")
    print(f"model={metrics['model_path']}")


if __name__ == "__main__":
    main()
