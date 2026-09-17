from uuid import uuid4

from app.models.transcript import Sentence
from app.models.session import Session


sessions: dict[str, Session] = {}


def create_session(video_id: str, sentences: list[Sentence]) -> str:
    session_id = str(uuid4()) # Create a unique id for session id

    sessions[session_id] = Session(
        video_id=video_id,
        sentences=sentences,
    )

    return session_id

def get_session(session_id: str) -> dict | None:
    return sessions.get(session_id)