from app.models.transcript import Sentence
from pathlib import Path
from app.services.transcript_service import (
    build_sentences,
    build_sentences_from_whisper,
    build_text_sentences_from_youtube,
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
def test_build_sentences_uses_youtube_transcript(monkeypatch):
    fake_transcript = [
        {
            "text": "Hello world.",
            "start": 0.0,
            "duration": 1.5,
        }
    ]

    def fake_fetch_transcript(video_id):
        return fake_transcript

    monkeypatch.setattr(
        "app.services.transcript_service.fetch_transcript",
        fake_fetch_transcript,
    )

    result = build_sentences("abc123")

    assert len(result) == 1
    assert result[0].text == "Hello world."
    assert result[0].start == 0.0
    assert result[0].duration == 1.5

@pytest.mark.unit
def test_build_sentences_fallback_when_transcript_not_found(monkeypatch):
    def fake_fetch_transcript(video_id):
        raise AppError(
            "TRANSCRIPT_NOT_FOUND",
            "No transcript was found for this video.",
            404,
        )

    def fake_download_audio(video_id):
        return Path("fake_audio.mp3")

    def fake_transcribe_audio(audio_path):
        return {
            "segments": [
                {
                    "words": [
                        {
                            "word": " Hello",
                            "start": 0.0,
                            "end": 0.5,
                        },
                        {
                            "word": " world.",
                            "start": 0.5,
                            "end": 1.0,
                        },
                    ]
                }
            ]
        }

    monkeypatch.setattr(
        "app.services.transcript_service.fetch_transcript",
        fake_fetch_transcript,
    )

    monkeypatch.setattr(
        "app.services.transcript_service.download_audio",
        fake_download_audio,
    )

    monkeypatch.setattr(
        "app.services.transcript_service.transcribe_audio",
        fake_transcribe_audio,
    )

    result = build_sentences("abc123")

    assert len(result) == 1
    assert result[0].text == "Hello world."
    assert result[0].start == 0.0
    assert result[0].duration == 1.0

@pytest.mark.unit
def test_build_sentences_fallback_when_transcript_disabled(monkeypatch):
    def fake_fetch_transcript(video_id):
        raise AppError(
            "TRANSCRIPT_DISABLED",
            "Transcripts are disabled for this video.",
            422,
        )

    def fake_download_audio(video_id):
        return Path("fake_audio.mp3")

    def fake_transcribe_audio(audio_path):
        return {
            "segments": [
                {
                    "words": [
                        {
                            "word": " You",
                            "start": 2.0,
                            "end": 2.3,
                        },
                        {
                            "word": " ready?",
                            "start": 2.3,
                            "end": 2.8,
                        },
                    ]
                }
            ]
        }

    monkeypatch.setattr(
        "app.services.transcript_service.fetch_transcript",
        fake_fetch_transcript,
    )

    monkeypatch.setattr(
        "app.services.transcript_service.download_audio",
        fake_download_audio,
    )

    monkeypatch.setattr(
        "app.services.transcript_service.transcribe_audio",
        fake_transcribe_audio,
    )

    result = build_sentences("abc123")

    assert len(result) == 1
    assert result[0].text == "You ready?"
    assert result[0].start == 2.0
    assert result[0].duration == pytest.approx(0.8)

@pytest.mark.unit
def test_build_sentences_does_not_fallback_for_video_unavailable(monkeypatch):
    def fake_fetch_transcript(video_id):
        raise AppError(
            "VIDEO_UNAVAILABLE",
            "The video is unavailable.",
            404,
        )

    monkeypatch.setattr(
        "app.services.transcript_service.fetch_transcript",
        fake_fetch_transcript,
    )

    with pytest.raises(AppError) as exc_info:
        build_sentences("abc123")

    assert exc_info.value.code == "VIDEO_UNAVAILABLE"
    assert exc_info.value.status_code == 404

@pytest.mark.unit
def test_build_text_sentences_from_youtube():
    transcript = [
        {
            "text": "Hey everybody, welcome to this A1",
            "start": 0.4,
            "duration": 5.04,
        },
        {
            "text": "English listening practice video. You",
            "start": 2.8,
            "duration": 4.479,
        },
        {
            "text": "can use this video to train your listening.",
            "start": 5.04,
            "duration": 4.0,
        },
    ]

    result = build_text_sentences_from_youtube(transcript)

    assert result == [
        "Hey everybody, welcome to this A1 English listening practice video.",
        "You can use this video to train your listening.",
    ]