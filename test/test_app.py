import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app


@pytest.fixture()
def client(tmp_path):
    db_path = os.path.join(tmp_path, "test.db")
    app = create_app({"TESTING": True, "DATABASE": db_path})
    return app.test_client()


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_create_and_list_client(client):
    create_response = client.post(
        "/clients",
        json={"name": "Ava", "age": 28, "program": "Fat Loss"},
    )
    assert create_response.status_code == 201
    payload = create_response.get_json()
    assert "id" in payload

    list_response = client.get("/clients")
    assert list_response.status_code == 200
    clients = list_response.get_json()
    assert len(clients) == 1
    assert clients[0]["name"] == "Ava"


def test_create_client_missing_fields(client):
    response = client.post("/clients", json={"name": "NoAge"})
    assert response.status_code == 400
    assert "missing fields" in response.get_json()["error"]


def test_log_workout_for_existing_client(client):
    created = client.post(
        "/clients",
        json={"name": "Leo", "age": 33, "program": "Muscle Gain"},
    ).get_json()

    response = client.post(
        "/workouts",
        json={
            "client_id": created["id"],
            "workout_type": "Strength",
            "duration_minutes": 60,
            "notes": "Upper body session",
        },
    )
    assert response.status_code == 201

    workouts_response = client.get(f"/clients/{created['id']}/workouts")
    assert workouts_response.status_code == 200
    workouts = workouts_response.get_json()
    assert len(workouts) == 1
    assert workouts[0]["workout_type"] == "Strength"


def test_log_workout_for_unknown_client(client):
    response = client.post(
        "/workouts",
        json={"client_id": 999, "workout_type": "Cardio", "duration_minutes": 30},
    )
    assert response.status_code == 404
