import pytest
from sqlmodel import Session, SQLModel
from fastapi.testclient import TestClient

from .src.db.conn import connect_to_test_db
from .src.main import app

@pytest.fixture(name="session")
def session_fixture():
    engine = connect_to_test_db()
    SQLModel.metadata.create_all(engine)

    with Session() as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session_override] = get_session_override
    
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_card(client: TestClient):
    response = client.post(
        "/cards", json={"texto": "teste", "data_criacao": "2020-01-01", "data_modificacao": "2020-01-01"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["texto"] == "teste"
    assert data["data_criacao"] == "2020-01-01"
    assert data["data_modificacao"] == "2020-01-01"
    assert data["id"] is not None
    