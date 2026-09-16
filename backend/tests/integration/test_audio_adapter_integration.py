import pytest

from app.adapters.audio_adapter import download_audio


@pytest.mark.integration
@pytest.mark.external
def test_download_audio():
    video_id = "4EtXW3nnfPI"

    result = download_audio(video_id)

    assert result.exists()
    assert result.suffix == ".mp3"
    assert result.stat().st_size > 0