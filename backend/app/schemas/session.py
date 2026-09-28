from pydantic import BaseModel, field_validator

# Send for frontend

class CreateSessionRequest(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str):
        if not value.strip():
            raise ValueError("URL cannot be empty")

        return value.strip()

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

class ShowAnswerResponse(BaseModel):
    answer: str