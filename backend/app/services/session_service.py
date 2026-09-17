from uuid import uuid4

from app.models.transcript import Sentence
from app.models.session import Session
from app.services.transcript_service import build_sentences
from app.services.youtube_service import extract_youtube_video_id
from app.errors import AppError
import string

sessions: dict[str, Session] = {}


def create_session(video_id: str, sentences: list[Sentence]) -> str:
    session_id = str(uuid4()) # Create a unique id for session id

    sessions[session_id] = Session(
        video_id=video_id,
        sentences=sentences,
    )

    return session_id

def get_session(session_id: str) -> Session | None:
    return sessions.get(session_id)

def create_dictation_session(youtube_url: str) -> tuple[str, Session]:
    video_id = extract_youtube_video_id(youtube_url)

    sentences = build_sentences(video_id)

    session_id = create_session(
        video_id=video_id,
        sentences=sentences,
    )

    return session_id, sessions[session_id]

def normalize_answer(text: str) -> str:
    text = text.lower()

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    return " ".join(text.split())

def check_answer(session_id: str, sentence_id: int, answer: str,) -> bool:
    session = get_session(session_id)

    if session is None:
        raise AppError(
            "SESSION_NOT_FOUND",
            "Session not found.",
            404,
        )
    if sentence_id < 0 or sentence_id >= len(session.sentences):
        raise AppError(
            "SENTENCE_NOT_FOUND",
            "Sentence not found.",
            404,
        )
    sentence = session.sentences[sentence_id]

    return normalize_answer(answer) == normalize_answer(sentence.text)