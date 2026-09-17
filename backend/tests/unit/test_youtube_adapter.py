import pytest

from app.adapters.youtube_adapter import fetch_transcript
from app.errors import AppError
from youtube_transcript_api._errors import (
    IpBlocked,
    NoTranscriptFound,
    RequestBlocked,
    TranscriptsDisabled,
    VideoUnavailable,
)

class FakeFetchedTranscript:
    def to_raw_data(self):
        return [
            {
                "text": "Hello",
                "start": 0.0,
                "duration": 2.5,
            }
        ]

@pytest.mark.unit
def test_fetch_transcript_success(monkeypatch):
    def fake_fetch(self, video_id):
        return FakeFetchedTranscript()

    monkeypatch.setattr(
        "app.adapters.youtube_adapter.YouTubeTranscriptApi.fetch",
        fake_fetch,
    )

    result = fetch_transcript("abc123")

    assert result == [
        {
            "text": "Hello",
            "start": 0.0,
            "duration": 2.5,
        }
    ]

@pytest.mark.unit
def test_fetch_transcript_request_blocked(monkeypatch):
    def fake_fetch(self, video_id):
        raise RequestBlocked("Request blocked")

    monkeypatch.setattr(
        "app.adapters.youtube_adapter.YouTubeTranscriptApi.fetch",
        fake_fetch,
    )

    with pytest.raises(AppError) as exc_info:
        fetch_transcript("abc123")

    assert exc_info.value.code == "YOUTUBE_ACCESS_BLOCKED"
    assert exc_info.value.status_code == 429

@pytest.mark.unit
def test_fetch_transcript_ip_blocked(monkeypatch):
    def fake_fetch(self, video_id):
        raise IpBlocked("IP blocked")

    monkeypatch.setattr(
        "app.adapters.youtube_adapter.YouTubeTranscriptApi.fetch",
        fake_fetch,
    )

    with pytest.raises(AppError) as exc_info:
        fetch_transcript("abc123")

    assert exc_info.value.code == "YOUTUBE_ACCESS_BLOCKED"
    assert exc_info.value.status_code == 429

@pytest.mark.unit
def test_fetch_transcript_video_unavailable(monkeypatch):
    def fake_fetch(self, video_id):
        raise VideoUnavailable(video_id)

    monkeypatch.setattr(
        "app.adapters.youtube_adapter.YouTubeTranscriptApi.fetch",
        fake_fetch,
    )

    with pytest.raises(AppError) as exc_info:
        fetch_transcript("abc123")

    assert exc_info.value.code == "VIDEO_UNAVAILABLE"
    assert exc_info.value.status_code == 404

@pytest.mark.unit
def test_fetch_transcript_disabled(monkeypatch):
    def fake_fetch(self, video_id):
        raise TranscriptsDisabled(video_id)

    monkeypatch.setattr(
        "app.adapters.youtube_adapter.YouTubeTranscriptApi.fetch",
        fake_fetch,
    )

    with pytest.raises(AppError) as exc_info:
        fetch_transcript("abc123")

    assert exc_info.value.code == "TRANSCRIPT_DISABLED"
    assert exc_info.value.status_code == 422


@pytest.mark.unit
def test_fetch_transcript_not_found(monkeypatch):
    def fake_fetch(self, video_id):
        raise NoTranscriptFound(
            video_id,
            ["en"],
            None,
        )

    monkeypatch.setattr(
        "app.adapters.youtube_adapter.YouTubeTranscriptApi.fetch",
        fake_fetch,
    )

    with pytest.raises(AppError) as exc_info:
        fetch_transcript("abc123")

    assert exc_info.value.code == "TRANSCRIPT_NOT_FOUND"
    assert exc_info.value.status_code == 404