from youtube_transcript_api import YouTubeTranscriptApi


def fetch_transcript(video_id: str):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    return transcript