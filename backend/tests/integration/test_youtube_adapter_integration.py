from app.adapters.youtube_adapter import fetch_transcript
import pytest

@pytest.mark.integration 
def test_fetch_transcript():
    video_id = "M7lemjPlHkc"
    result = fetch_transcript(video_id)
    assert result is not None