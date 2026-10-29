import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_login_student():
    response = client.post("/api/auth/login", json={
        "email": "student@alumnia.edu",
        "password": "Password123!"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["role"] == "student"

def test_login_admin():
    response = client.post("/api/auth/login", json={
        "email": "admin@alumnia.edu",
        "password": "Password123!"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["role"] == "admin"

def test_get_recommendations():
    # Login as student first
    login_resp = client.post("/api/auth/login", json={
        "email": "student@alumnia.edu",
        "password": "Password123!"
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch recommendations
    rec_resp = client.get("/api/recommendations", headers=headers)
    assert rec_resp.status_code == 200
    recs = rec_resp.json()
    assert len(recs) > 0
    # Top recommendation should have high score and explanation
    top = recs[0]
    assert "score" in top
    assert "explanation" in top
    assert "conversation_starter" in top
    assert "breakdown" in top
    assert top["score"] >= 60

def test_jobs_list():
    login_resp = client.post("/api/auth/login", json={
        "email": "student@alumnia.edu",
        "password": "Password123!"
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    jobs_resp = client.get("/api/jobs", headers=headers)
    assert jobs_resp.status_code == 200
    jobs = jobs_resp.json()
    assert len(jobs) >= 4
