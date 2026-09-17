from pydantic import BaseModel

# Send for frontend

class CreateSessionRequest(BaseModel):
    url: str

class SentenceInfo(BaseModel): 
    id: int
    start: float
    duration: float
    word_count: int

class CreateSessionResponse(BaseModel):
    session_id: str
    video_id: str
    sentences: list[SentenceInfo]   

# Validate input
class CheckAnswerRequest(BaseModel):
    sentence_id: int
    answer: str

class CheckAnswerResponse(BaseModel):
    correct: bool