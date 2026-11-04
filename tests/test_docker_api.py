
import pytest
import requests

BASE_URL = "http://127.0.0.1:7860"


def test_health():
    response = requests.get(f"{BASE_URL}/health", timeout=10)

    assert response.status_code == 200
    assert response.json()["model_loaded"] is True


@pytest.mark.parametrize("size", [1, 50, 100])
def test_batch_sizes(size):
    comments = ["This video is amazing"] * size

    response = requests.post(
        f"{BASE_URL}/predict_batch",
        json={"comments": comments},
        timeout=30
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["results"]) == size
    assert data["statistics"]["total"] == size
    assert sum(data["statistics"]["counts"].values()) == size

    for result in data["results"]:
        assert result["sentiment"] in [
            "positive", "neutral", "negative"
        ]
        assert 0 <= result["confidence"] <= 1


@pytest.mark.parametrize("payload", [
    {"comments": []},
    {"comments": ["   "]},
    {}
])
def test_invalid_requests(payload):
    response = requests.post(
        f"{BASE_URL}/predict_batch",
        json=payload,
        timeout=10
    )

    assert response.status_code == 422


def test_edge_cases():
    comments = [
        "Good",
        "Bad",
        "😂🔥❤️",
        "This video est vraiment amazing!",
        "Great " * 200
    ]

    response = requests.post(
        f"{BASE_URL}/predict_batch",
        json={"comments": comments},
        timeout=30
    )

    assert response.status_code == 200
    assert len(response.json()["results"]) == len(comments)
