from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_has_status_and_version():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["version"].startswith("v")


def test_predict_accepts_short_homework_payload():
    response = client.post("/predict", json={"x": [1, 2, 3]})
    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"prediction", "label", "version", "input_features"}
    assert len(body["input_features"]) == 4


def test_metrics_endpoint_is_mounted():
    response = client.get("/metrics")
    assert response.status_code in {200, 307}
