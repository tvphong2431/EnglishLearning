from app.models.transcript import Sentence
from pathlib import Path
from app.services.transcript_service import (
    build_sentences,
    build_sentences_from_whisper,
)
from app.errors import AppError
import pytest

@pytest.mark.unit
def test_build_sentences_from_whisper():
    fake_result = {
        "segments": [
            {
                "words": [
                    {"word": " Hello", "start": 0.0, "end": 0.5},
                    {"word": " world.", "start": 0.5, "end": 1.0},
                    {"word": " How", "start": 1.5, "end": 1.8},
                    {"word": " are", "start": 1.8, "end": 2.0},
                    {"word": " you?", "start": 2.0, "end": 2.4},
                ]
            }
        ]
    }

    result = build_sentences_from_whisper(fake_result)

    assert len(result) == 2

    assert result[0].text == "Hello world."
    assert result[0].start == 0.0
    assert result[0].duration == 1.0
    assert result[0].word_count == 2

    assert result[1].text == "How are you?"
    assert result[1].start == 1.5
    assert result[1].duration == pytest.approx(0.9)
    assert result[1].word_count == 3

@pytest.mark.unit
def test_build_sentences_from_whisper_without_final_punctuation():
    fake_result = {
        "segments": [
            {
                "words": [
                    {"word": " Thanks", "start": 0.0, "end": 0.4},
                    {"word": " for", "start": 0.4, "end": 0.7},
                    {"word": " watching", "start": 0.7, "end": 1.2},
                ]
            }
        ]
    }

    result = build_sentences_from_whisper(fake_result)

    assert len(result) == 1
    assert result[0].text == "Thanks for watching"
    assert result[0].start == 0.0
    assert result[0].duration == pytest.approx(1.2)
    assert result[0].word_count == 3

@pytest.mark.unit
def test_build_sentences_uses_whisper(monkeypatch):
    fake_whisper_result = {
        "segments": [
            {
                "words": [
                    {
                        "word": "Hello ",
                        "start": 0.0,
                        "end": 0.5,
                    },
                    {
                        "word": "world.",
                        "start": 0.5,
                        "end": 1.5,
                    },
                ]
            }
        ]
    }

    monkeypatch.setattr(
        "app.services.transcript_service.download_audio",
        lambda video_id: Path("fake_audio.mp3"),
    )

    monkeypatch.setattr(
        "app.services.transcript_service.transcribe_audio",
        lambda audio_path: fake_whisper_result,
    )

    result = build_sentences("abc123")

    assert len(result) == 1
    assert result[0].text == "Hello world."
    assert result[0].start == 0.0
    assert result[0].duration == 1.5
    assert result[0].word_count == 2
