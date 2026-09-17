from pydantic import BaseModel

# Send for frontend
class SentenceInfo(BaseModel): 
    id: int
    start: float
    duration: float
    word_count: int


class CreateSessionResponse(BaseModel):
    session_id: str
    video_id: str
    sentences: list[SentenceInfo]