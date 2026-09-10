from app.adapters.youtube_adapter import fetch_transcript


def test_fetch_transcript(monkeypatch):
    fake_transcript = [
        {
            "text": "Hello",
            "start": 0.0,
            "duration": 2.5,
        }
    ]

    def fake_fetch(self, video_id):
        return fake_transcript

    monkeypatch.setattr(
        "app.adapters.youtube_adapter.YouTubeTranscriptApi.fetch",
        fake_fetch,
    )

    result = fetch_transcript("abc123")

    assert result == fake_transcript