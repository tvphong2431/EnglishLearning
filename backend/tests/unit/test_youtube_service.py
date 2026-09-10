import pytest

from app.services.youtube_service import extract_youtube_video_id


@pytest.mark.unit
def test_extract_youtube_video_id():
    url = "https://www.youtube.com/watch?v=abc123"

    result = extract_youtube_video_id(url)

    assert result == "abc123"

@pytest.mark.unit
def test_extract_youtube_video_id_from_short_url():
    url = "https://youtu.be/abc123"

    result = extract_youtube_video_id(url)

    assert result == "abc123"


@pytest.mark.unit
def test_extract_youtube_video_id_from_shorts_url():
    url = "https://www.youtube.com/shorts/abc123"

    result = extract_youtube_video_id(url)

    assert result == "abc123"

@pytest.mark.unit
def test_extract_youtube_video_id_with_invalid_url():
    url = "https://example.com/video/abc123"

    with pytest.raises(ValueError):
        extract_youtube_video_id(url)

@pytest.mark.unit
def test_extract_youtube_video_id_when_video_id_missing():
    url = "https://www.youtube.com/watch"

    with pytest.raises(ValueError):
        extract_youtube_video_id(url)