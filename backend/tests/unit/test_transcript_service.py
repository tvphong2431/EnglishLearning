from app.models.transcript import Sentence
from app.services.transcript_service import build_sentences
import pytest
@pytest.mark.unit

def test_build_sentences(monkeypatch):
    fake_transcript = [
        {
            "text": "Hello",
            "start": 0.0,
            "duration": 2.5,
        },
        {
            "text": "World",
            "start": 2.5,
            "duration": 1.5,
        },
    ]

    def fake_fetch_transcript(video_id):
        return fake_transcript

    monkeypatch.setattr(
        "app.services.transcript_service.fetch_transcript",
        fake_fetch_transcript,
    )

    result = build_sentences("abc123")

    assert len(result) == 2
    assert isinstance(result[0], Sentence)

    assert result[0].text == "Hello"
    assert result[0].start == 0.0
    assert result[0].duration == 2.5

    assert result[1].text == "World"
    assert result[1].start == 2.5
    assert result[1].duration == 1.5