import json
from pathlib import Path

from ml_pipeline import train_model
from model_gate import check_gate


def test_train_model_writes_model_and_metrics(tmp_path: Path):
    model_path = tmp_path / "model.joblib"
    metrics_path = tmp_path / "metrics.json"

    metrics = train_model(model_path, metrics_path)

    assert model_path.exists()
    assert metrics_path.exists()
    assert metrics["accuracy"] >= 0.9
    assert json.loads(metrics_path.read_text(encoding="utf-8"))["model_path"] == str(model_path)


def test_model_gate_passes_for_current_policy(tmp_path: Path):
    model_path = tmp_path / "model.joblib"
    metrics_path = tmp_path / "metrics.json"
    train_model(model_path, metrics_path)

    check_gate(metrics_path, Path("policies/model_policy.yaml"))
