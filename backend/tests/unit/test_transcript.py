import pytest

from app.services.transcript_service import build_text_sentences_from_youtube


@pytest.mark.unit
def test_build_text_sentences_from_youtube():
    transcript = [
        {
            "text": "Hey everybody, welcome to this A1",
            "start": 0.4,
            "duration": 5.04,
        },
        {
            "text": "English listening practice video. You",
            "start": 2.8,
            "duration": 4.479,
        },
        {
            "text": "can use this video to train your listening.",
            "start": 5.04,
            "duration": 4.0,
        },
    ]

    result = build_text_sentences_from_youtube(transcript)

    assert result == [
        "Hey everybody, welcome to this A1 English listening practice video.",
        "You can use this video to train your listening.",
    ]