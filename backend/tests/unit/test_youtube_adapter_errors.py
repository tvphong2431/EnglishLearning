import pytest
from app.adapters.youtube_adapter import fetch_transcript
from app.errors import AppError
from youtube_transcript_api._errors import IpBlocked

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