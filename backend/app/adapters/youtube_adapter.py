from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import IpBlocked

from app.errors import AppError


def fetch_transcript(video_id: str):
    api = YouTubeTranscriptApi()

    try:
        transcript = api.fetch(video_id)
    except IpBlocked:
        raise AppError(
            code="YOUTUBE_ACCESS_BLOCKED",
            message="Unable to access YouTube.",
            status_code=429,
        )

    return transcript.to_raw_data()