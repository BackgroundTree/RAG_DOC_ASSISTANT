from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import pytest

from app.main import app


@pytest.fixture
def client():
    with patch("app.main.chromadb.PersistentClient") as mock_chroma, patch(
        "app.main.SentenceTransformer"
    ) as mock_st:
        mock_chroma.return_value = MagicMock()
        mock_st.return_value = MagicMock()
        with TestClient(app) as test_client:
            yield test_client


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("app.api.routes.query.generate_answer_service")
@patch("app.api.routes.query.retrieval_service")
def test_query_success(mock_retrieval, mock_generate, client):
    mock_retrieval.return_value = (
        "Majima uses Breaker style.",
        ["guide_chapter_1.txt"],
    )
    mock_generate.return_value = (
        "Majima uses Breaker style to clear groups of enemies."
    )

    response = client.post(
        "/query", json={"question": "What is Majima's best fighting style?"}
    )

    assert response.status_code == 200
    data = response.json()
    assert (
        data["answer"]
        == "Majima uses Breaker style to clear groups of enemies."
    )
    assert data["sources"] == ["guide_chapter_1.txt"]

    mock_retrieval.assert_called_once()
    mock_generate.assert_called_once()


def test_query_invalid_payload(client):
    response = client.post("/query", json={"question": "hi"})
    assert response.status_code == 422