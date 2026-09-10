import pytest
from app.adapters.youtube_adapter import fetch_transcript
from app.errors import AppError
from youtube_transcript_api._errors import IpBlocked, VideoUnavailable, TranscriptsDisabled, NoTranscriptFound

# IP Blocked
@pytest.mark.unit
def test_fetch_transcript_when_ip_blocked(monkeypatch):
    def fake_fetch(self, video_id):
        raise IpBlocked(video_id)
    
    monkeypatch.setattr(
        "app.adapters.youtube_adapter.YouTubeTranscriptApi.fetch",
        fake_fetch,
    )
    with pytest.raises(AppError) as exc_info:
        fetch_transcript("abc123")

    assert exc_info.value.code == "YOUTUBE_ACCESS_BLOCKED"
    assert exc_info.value.status_code == 429

# Video Unavailable
@pytest.mark.unit
def test_fetch_transcript_when_video_unavailable(monkeypatch):
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

# Transcripts Disabled
def test_fetch_transcript_when_transcripts_disabled(monkeypatch):
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

# NoTranscriptFound
@pytest.mark.unit
def test_fetch_transcript_when_no_transcript_found(monkeypatch):
    def fake_fetch(self, video_id):
        raise NoTranscriptFound(video_id,["en"],[])

    monkeypatch.setattr(
        "app.adapters.youtube_adapter.YouTubeTranscriptApi.fetch",
        fake_fetch,
    )

    with pytest.raises(AppError) as exc_info:
        fetch_transcript("abc123")

    assert exc_info.value.code == "TRANSCRIPT_NOT_FOUND"
    assert exc_info.value.status_code == 404