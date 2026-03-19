import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Set up the test database (in-memory SQLite)
from .database import Base
from .main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the test tables
Base.metadata.create_all(bind=engine)

# Dependency override for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Test cases

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Persistent Microservice Demo API!"}

def test_create_item():
    response = client.post(
        "/items",
        json={"name": "Test Item", "description": "This is a test description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert "id" in data

def test_read_items():
    # Ensure there is at least one item
    client.post("/items", json={"name": "Item 1", "description": "Desc 1"})
    client.post("/items", json={"name": "Item 2", "description": "Desc 2"})
    
    response = client.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 2

def test_read_item_by_id():
    # Create an item to test
    create_response = client.post("/items", json={"name": "Find Me", "description": "Specific desc"})
    item_id = create_response.json()["id"]
    
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Find Me"

def test_read_item_not_found():
    response = client.get("/items/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
