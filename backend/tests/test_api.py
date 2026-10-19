import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from app import app

PAYLOAD = json.loads(
    (ROOT / "backend/test_payload.json").read_text(encoding="utf-8")
)


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["features"] == 41


def test_valid_prediction(client):
    response = client.post("/predict", json=PAYLOAD)
    result = response.get_json()

    assert response.status_code == 200
    assert result["prediction"] == 0
    assert result["classes"] == [0, 1]
    assert result["delay_probability"] == pytest.approx(
        0.39497275308848623
    )
    assert sum(result["probabilities"]) == pytest.approx(1.0)


def test_missing_feature(client):
    incomplete = dict(PAYLOAD)
    missing = next(iter(incomplete))
    incomplete.pop(missing)

    response = client.post("/predict", json=incomplete)

    assert response.status_code == 400
    assert missing in response.get_json()["missing"]


def test_invalid_json(client):
    response = client.post(
        "/predict",
        data="not-json",
        content_type="application/json",
    )

    assert response.status_code == 400


def test_extra_feature(client):
    response = client.post(
        "/predict",
        json={**PAYLOAD, "unexpected_feature": 123},
    )

    assert response.status_code == 400
    assert "unexpected_feature" in response.get_json()["extra"]


@pytest.mark.parametrize("invalid_value", ["abc", None, True])
def test_invalid_numeric_input(client, invalid_value):
    response = client.post(
        "/predict",
        json={**PAYLOAD, "Month": invalid_value},
    )

    assert response.status_code == 400