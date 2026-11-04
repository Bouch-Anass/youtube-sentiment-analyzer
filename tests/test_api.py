
from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["model_loaded"] is True


def test_predictions():
    response = client.post("/predict_batch", json={
        "comments": [
            "This video is amazing",
            "This is terrible",
            "The video was uploaded yesterday"
        ]
    })

    assert response.status_code == 200

    data = response.json()

    assert len(data["results"]) == 3
    assert data["statistics"]["total"] == 3
    assert sum(data["statistics"]["counts"].values()) == 3

    for result in data["results"]:
        assert result["sentiment"] in [
            "negative", "neutral", "positive"
        ]
        assert 0 <= result["confidence"] <= 1


def test_empty_batch():
    response = client.post("/predict_batch", json={
        "comments": []
    })

    assert response.status_code == 422


def test_empty_comment():
    response = client.post("/predict_batch", json={
        "comments": ["   "]
    })

    assert response.status_code == 422


def test_missing_comments():
    response = client.post("/predict_batch", json={})

    assert response.status_code == 422
