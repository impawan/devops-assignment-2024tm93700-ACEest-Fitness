import pytest
from app import create_app
from app.config import TestConfig

@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy", "version": "1.0.0"}

def test_get_members(client):
    response = client.get('/members')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_add_member(client):
    new_member = {"name": "Charlie", "plan": "Pro"}
    response = client.post('/members', json=new_member)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Charlie"
    assert data["plan"] == "Pro"
    assert "id" in data

def test_add_member_invalid(client):
    response = client.post('/members', json={"name": "Invalid"})
    assert response.status_code == 400
