from fastapi import APIRouter

from app.schemas.youtube import YouTubeRequest
from app.services.youtube_service import extract_youtube_video_id
from app.services.transcript_service import build_sentences

router = APIRouter()



@router.post("/process")
def process(request: YouTubeRequest):
    video_id = extract_youtube_video_id(request.youtube_url)
    sentences = build_sentences(video_id)

    return {
        "sentences": sentences
    }