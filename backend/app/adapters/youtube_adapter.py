from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import IpBlocked, VideoUnavailable, TranscriptsDisabled, NoTranscriptFound

from app.errors import AppError


def fetch_transcript(video_id: str):
    api = YouTubeTranscriptApi()

    try:
        transcript = api.fetch(video_id)

    except IpBlocked:
        raise AppError(
            code="YOUTUBE_ACCESS_BLOCKED",
            message="YouTube access is temporarily blocked.",
            status_code=429,
        )

    except VideoUnavailable:
        raise AppError(
            code="VIDEO_UNAVAILABLE",
            message="The video is unavailable.",
            status_code=404,
        )

    except TranscriptsDisabled:
        raise AppError(
            code="TRANSCRIPT_DISABLED",
            message="Transcripts are disabled for this video.",
            status_code=422,
        )

    except NoTranscriptFound:
        raise AppError(
            code="TRANSCRIPT_NOT_FOUND",
            message="No transcript was found for this video.",
            status_code=404,
        )

    return transcript.to_raw_data()