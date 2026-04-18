import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import app
from db.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)
client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def get_token(username="testuser", email="test@test.com", password="testpass123"):
    client.post("/register", json={"username": username, "email": email, "password": password})
    res = client.post("/login", json={"username": username, "password": password})
    return res.json()["access_token"]

def test_register():
    res = client.post("/register", json={"username": "kader", "email": "kader@test.com", "password": "pass123"})
    assert res.status_code == 201

def test_register_duplicate_username():
    client.post("/register", json={"username": "kader", "email": "kader@test.com", "password": "pass123"})
    res = client.post("/register", json={"username": "kader", "email": "other@test.com", "password": "pass123"})
    assert res.status_code == 400

def test_login_success():
    client.post("/register", json={"username": "kader", "email": "kader@test.com", "password": "pass123"})
    res = client.post("/login", json={"username": "kader", "password": "pass123"})
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_login_wrong_password():
    client.post("/register", json={"username": "kader", "email": "kader@test.com", "password": "pass123"})
    res = client.post("/login", json={"username": "kader", "password": "wrongpass"})
    assert res.status_code == 401

def test_create_task():
    token = get_token()
    res = client.post("/tasks", json={"title": "Buy groceries"},
                      headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 201
    assert res.json()["title"] == "Buy groceries"

def test_get_tasks():
    token = get_token()
    client.post("/tasks", json={"title": "Task 1"}, headers={"Authorization": f"Bearer {token}"})
    client.post("/tasks", json={"title": "Task 2"}, headers={"Authorization": f"Bearer {token}"})
    res = client.get("/tasks", headers={"Authorization": f"Bearer {token}"})
    assert res.json()["total"] == 2

def test_update_task():
    token = get_token()
    created = client.post("/tasks", json={"title": "Old"}, headers={"Authorization": f"Bearer {token}"}).json()
    res = client.put(f"/tasks/{created['id']}", json={"completed": True},
                     headers={"Authorization": f"Bearer {token}"})
    assert res.json()["completed"] == True

def test_delete_task():
    token = get_token()
    created = client.post("/tasks", json={"title": "To delete"}, headers={"Authorization": f"Bearer {token}"}).json()
    res = client.delete(f"/tasks/{created['id']}", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 204

def test_filter_completed():
    token = get_token()
    t1 = client.post("/tasks", json={"title": "Task 1"}, headers={"Authorization": f"Bearer {token}"}).json()
    client.post("/tasks", json={"title": "Task 2"}, headers={"Authorization": f"Bearer {token}"})
    client.put(f"/tasks/{t1['id']}", json={"completed": True}, headers={"Authorization": f"Bearer {token}"})
    res = client.get("/tasks?completed=true", headers={"Authorization": f"Bearer {token}"})
    assert res.json()["total"] == 1

def test_unauthorized_access():
    res = client.get("/tasks")
    assert res.status_code == 401