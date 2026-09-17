import pytest

from app.models.transcript import Sentence
from app.services.session_service import (
    create_session,
    get_session,
    sessions,
)

from app.services import session_service
from app.models.session import Session

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
    assert isinstance(session, Session)
    
    assert session is not None
    assert session.video_id == "abc123"
    assert session.sentences == sentences


@pytest.mark.unit
def test_get_session_returns_none_when_not_found():
    sessions.clear()

    result = get_session("not-exist")

    assert result is None

@pytest.mark.unit
def test_create_dictation_session(monkeypatch):
    session_service.sessions.clear()

    fake_sentences = [
        Sentence(
            text="You ready?",
            start=10.26,
            duration=0.44,
            word_count=2,
        )
    ]

    monkeypatch.setattr(
        session_service,
        "extract_youtube_video_id",
        lambda url: "abc123",
    )

    monkeypatch.setattr(
        session_service,
        "build_sentences",
        lambda video_id: fake_sentences,
    )

    session_id, session = session_service.create_dictation_session(
        "https://www.youtube.com/watch?v=abc123"
    )

    assert isinstance(session_id, str)
    assert session.video_id == "abc123"
    assert session.sentences == fake_sentences
    assert session_service.get_session(session_id) == session

def test_check_answer_returns_true_for_matching_answer():
    session_service.sessions.clear()

    sentences = [
        Sentence(
            text="You ready?",
            start=10.26,
            duration=0.44,
            word_count=2,
        )
    ]

    session_id = session_service.create_session(
        video_id="abc123",
        sentences=sentences,
    )

    result = session_service.check_answer(
        session_id=session_id,
        sentence_id=0,
        answer="You ready?",
    )

    assert result is True