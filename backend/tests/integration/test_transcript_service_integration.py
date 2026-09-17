import pytest

from app.services.transcript_service import build_sentences
from app.errors import AppError

# @pytest.mark.integration
# @pytest.mark.external
# def test_build_sentences_with_youtube_transcript():
#     video_id = "uVGV8LG3HHM"

#     result = build_sentences(video_id)

#     assert isinstance(result, list)
#     assert len(result) > 0

#     assert result[0].text
#     assert result[0].start >= 0
#     assert result[0].duration > 0

@pytest.mark.integration
@pytest.mark.external
def test_build_sentences_fallback_to_whisper(monkeypatch):
    def fake_fetch_transcript(video_id):
        raise AppError(
            "TRANSCRIPT_NOT_FOUND",
            "No transcript was found for this video.",
            404,
        )

    monkeypatch.setattr(
        "app.services.transcript_service.fetch_transcript",
        fake_fetch_transcript,
    )

    video_id = "CSj8Y_s_38c"

    result = build_sentences(video_id)

    assert isinstance(result, list)
    assert len(result) > 0

    assert result[0].text
    assert result[0].start >= 0
    assert result[0].duration > 0