import pytest

from app.models.transcript import Sentence
from app.services.session_service import (
    create_session,
    get_session,
    sessions,
)


@pytest.mark.unit
def test_create_session():
    sessions.clear()

    sentences = [
        Sentence(
            text="You ready?",
            start=10.26,
            duration=0.44,
            word_count=2,
        )
    ]

    session_id = create_session(
        video_id="abc123",
        sentences=sentences,
    )

    session = get_session(session_id)

    assert isinstance(session_id, str)
    assert session is not None
    assert session["video_id"] == "abc123"
    assert session["sentences"] == sentences


@pytest.mark.unit
def test_get_session_returns_none_when_not_found():
    sessions.clear()

    result = get_session("not-exist")

    assert result is None