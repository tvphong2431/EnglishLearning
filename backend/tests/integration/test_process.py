import pytest
from fastapi.testclient import TestClient
from app.models.transcript import Sentence
from app.errors import AppError
from app.main import app

@pytest.mark.integration
def test_process(monkeypatch):
    def fake_build_sentences(video_id):
        return [
            Sentence(
                text="Hello",
                start=0.0,
                duration=2.5,
            )
        ]

    monkeypatch.setattr(
        "app.api.process.build_sentences",
        fake_build_sentences,
    )

    client = TestClient(app)

    response = client.post(
        "/process",
        json={
            "youtube_url": "https://www.youtube.com/watch?v=abc123",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "sentences": [
            {
                "text": "Hello",
                "start": 0.0,
                "duration": 2.5,
            }
        ]
    }


@pytest.mark.integration
def test_process_without_youtube_url():
    client = TestClient(app)

    response = client.post(
        "/process",
        json={},
    )

    assert response.status_code == 422

@pytest.mark.integration
def test_process_when_build_sentences_fails(monkeypatch):
    def fake_build_sentences(video_id):
        raise AppError(
            code="YOUTUBE_ACCESS_BLOCKED",
            message="YouTube access is temporarily blocked.",
            status_code=429,
        )

    monkeypatch.setattr(
        "app.api.process.build_sentences",
        fake_build_sentences,
    )

    client = TestClient(app)

    response = client.post(
        "/process",
        json={
            "youtube_url": "https://www.youtube.com/watch?v=abc123",
        },
    )

    assert response.status_code == 429
    assert response.json() == {
        "code": "YOUTUBE_ACCESS_BLOCKED",
        "message": "YouTube access is temporarily blocked.",
    }