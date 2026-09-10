import pytest
from fastapi.testclient import TestClient
from app.models.transcript import Sentence

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