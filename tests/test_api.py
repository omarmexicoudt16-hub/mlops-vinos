from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_predict():
    payload = {"alcohol": 13.2, "flavanoids": 2.5, "color_intensity": 5.0, "proline": 1000}
    r = client.post("/predict", json=payload)
    assert r.status_code == 200
    assert r.json()["prediction"] in (0, 1, 2)


def test_predict_invalido():
    payload = {"alcohol": -5, "flavanoids": 2.5, "color_intensity": 5.0, "proline": 1000}
    r = client.post("/predict", json=payload)
    assert r.status_code == 422
