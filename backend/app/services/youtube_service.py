from urllib.parse import parse_qs, urlparse


def extract_youtube_video_id(url: str) -> str:
    parsed_url = urlparse(url)

    if parsed_url.hostname == "youtu.be":
        video_id = parsed_url.path.lstrip("/")

        if not video_id:
            raise ValueError("Invalid YouTube URL")

        return video_id

    if parsed_url.hostname in {"www.youtube.com", "youtube.com"}:
        if parsed_url.path.startswith("/shorts/"):
            video_id = parsed_url.path.removeprefix("/shorts/").split("/")[0]

            if not video_id:
                raise ValueError("Invalid YouTube URL")

            return video_id

        query = parse_qs(parsed_url.query)

        if "v" not in query:
            raise ValueError("Invalid YouTube URL")

        return query["v"][0]

    raise ValueError("Invalid YouTube URL")