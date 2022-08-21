from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_read_cards():
    response = client.get("/cards")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_card_not_exists():
    response = client.get("/cards/100")
    assert response.status_code == 404

def test_create_card():
    response = client.post("/cards", json={"texto": "Teste", "tags": [{"name": "test1"}]})
    assert response.status_code == 201

def test_create_card_without_tags():
    response = client.post("/cards", json={"texto": "Teste"})
    assert response.status_code == 201
    
def test_create_card_with_existing_tag():
    response = client.post("/cards", json={"texto": "Teste", "tags": [{"name": "tag1"}]})
    assert response.status_code == 201

def test_update_card():
    response = client.put("/cards/1", json={"texto": "Card Updated via test", "tags": [{"name": "tag1"}]})
    assert response.status_code == 200

def test_delete_card():
    response = client.delete("/cards/1")
    assert response.status_code == 200

def test_delete_card_not_exists():
    response = client.delete("/cards/200")
    assert response.status_code == 404


