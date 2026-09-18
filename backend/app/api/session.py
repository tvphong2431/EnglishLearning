from fastapi import APIRouter

from app.schemas.session import (
    CreateSessionRequest,
    CreateSessionResponse,
    SentenceInfo,
    CheckAnswerRequest,
    CheckAnswerResponse,
    ShowAnswerResponse
)
from app.services import session_service


router = APIRouter()

#
@router.post(
    "/sessions",
    response_model=CreateSessionResponse,
)
def create_dictation_session(request: CreateSessionRequest):
    session_id, session = session_service.create_dictation_session(request.url)

    sentence_infos = []

    for index, sentence in enumerate(session.sentences):
        sentence_infos.append(
            SentenceInfo(
                id=index,
                start=sentence.start,
                duration=sentence.duration,
                word_count=sentence.word_count,
            )
        )

    return CreateSessionResponse(
        session_id=session_id,
        video_id=session.video_id,
        sentences=sentence_infos,
    )

# Check answer
@router.post(
    "/sessions/{session_id}/check",
    response_model=CheckAnswerResponse,
)
def check_answer(session_id: str, request: CheckAnswerRequest):
    correct = session_service.check_answer(
        session_id=session_id,
        sentence_id=request.sentence_id,
        answer=request.answer,
    )

    return CheckAnswerResponse(
        correct=correct,
    )

# Show answer
@router.get(
    "/sessions/{session_id}/sentences/{sentence_id}/answer",
    response_model=ShowAnswerResponse,
)
def get_answer(
    session_id: str,
    sentence_id: int,
):
    answer = session_service.get_answer(
        session_id=session_id,
        sentence_id=sentence_id,
    )

    return ShowAnswerResponse(
        answer=answer,
    )