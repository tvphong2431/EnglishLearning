from youtube_transcript_api import YouTubeTranscriptApi


def fetch_transcript(video_id: str):
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id)

    return transcript