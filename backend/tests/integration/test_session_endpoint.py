import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.transcript import Sentence
from app.services import transcript_service
from app.services.session_service import (
    sessions, create_session
)


client = TestClient(app)

@pytest.mark.integration
def test_create_session_endpoint(monkeypatch):
    sessions.clear()

    def fake_build_sentences(video_id):
        return [
            Sentence(
                text="You ready?",
                start=10.26,
                duration=0.44,
                word_count=2,
            )
        ]

    monkeypatch.setattr(
        transcript_service,
        "build_sentences",
        fake_build_sentences,
    )

    response = client.post(
        "/sessions",
        json={
            "url": "https://www.youtube.com/watch?v=uVGV8LG3HHM"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["session_id"], str)
    assert data["video_id"] == "uVGV8LG3HHM"

    assert data["sentences"] == [
        {
            "id": 0,
            "start": 10.26,
            "duration": 0.44,
            "word_count": 2,
        }
    ]

    assert "text" not in data["sentences"][0]

@pytest.mark.integration
def test_check_answer_returns_true_when_correct():
    sessions.clear()

    sentences = [
        Sentence(
            text="You ready?",
            start=10.26,
            duration=0.44,
            word_count=2,
        )
    ]

    session_id = create_session(
        video_id="abc123",
        sentences=sentences,
    )

    request_body = {
        "sentence_id": 0,
        "answer": "You ready?",
    }

    response = client.post(
        f"/sessions/{session_id}/check",
        json=request_body,
    )

    assert response.status_code == 200

    response_body = response.json()

    assert response_body == {
        "correct": True,
    }  