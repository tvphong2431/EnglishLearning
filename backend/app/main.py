from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.errors import AppError
from app.api.process import router as process_router

from app.schemas.session import (
    CreateSessionRequest,
    CreateSessionResponse,
    SentenceInfo,
    CheckAnswerRequest,
    CheckAnswerResponse,
)
from app.services import (
    session_service,
    transcript_service,
)
from app.services.youtube_service import extract_youtube_video_id



app = FastAPI()
app.include_router(process_router)

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code" : exc.code,
            "message" : exc.message,
        },
    )

@app.get("/")
def root():
    return {
        "message": "EnglishLearning API is running"
    }

@app.post("/sessions", response_model=CreateSessionResponse)
def create_dictation_session(request: CreateSessionRequest):
    video_id = extract_youtube_video_id(request.url)

    sentences = transcript_service.build_sentences(video_id)

    session_id = session_service.create_session(
        video_id,
        sentences,
    )

    sentence_infos = []

    for index, sentence in enumerate(sentences): # get index and sentence
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
        video_id=video_id,
        sentences=sentence_infos,
    )
@app.post(
    "/sessions/{session_id}/check",
    response_model=CheckAnswerResponse,
)
def check_answer(
    session_id: str,
    request: CheckAnswerRequest,):
    session = session_service.get_session(session_id)

    sentence = session["sentences"][request.sentence_id]

    correct = request.answer == sentence.text

    return CheckAnswerResponse(
        correct=correct,
    )