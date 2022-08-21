from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)

def test_create_tag():
    response = client.post("/tags", json={"name": "test"})
    assert response.status_code == 201
    
def test_create_tag_with_existing_tag_name():
    response = client.post("/tags", json={"name": "test"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Tag name already exists"}
    
def test_update_tag():
    response = client.put("/tags/1", json={"name": "updated"})
    assert response.status_code == 200

def get_tag():
    response = client.get("/tags/1")
    assert response.status_code == 200

def get_tag_not_exists():
    response = client.get("/tags/100")
    assert response.status_code == 404

def test_delete_tag():
    response = client.delete("/tags/1")
    assert response.status_code == 200

