from pydantic import BaseModel


class SentenceResponse(BaseModel):
    text: str
    start: float
    duration: float


class TranscriptResponse(BaseModel):
    sentences: list[SentenceResponse]