from app.adapters.youtube_adapter import fetch_transcript
import pytest

@pytest.mark.integration 
@pytest.mark.external
def test_fetch_transcript():
    video_id = "uVGV8LG3HHM"
    result = fetch_transcript(video_id)
    assert result is not None