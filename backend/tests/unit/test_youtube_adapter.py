from app.adapters.youtube_adapter import fetch_transcript
import pytest

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
def test_fetch_transcript(monkeypatch):
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