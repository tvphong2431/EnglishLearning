from pathlib import Path
from yt_dlp import YoutubeDL
from app.config.settings import Settings
def _download_from_youtube(video_id: str, output_path: Path) -> Path:
    settings = Settings()

    url = f"https://www.youtube.com/watch?v={video_id}"

    options = {
        "format": "bestaudio/best",
        "outtmpl": str(output_path),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
        "js_runtimes": {
            "deno": {
                "path": settings.deno_path,
            },
        },
        "extractor_args": {
            "youtubepot-bgutilhttp": {
                "base_url": settings.pot_server_url,
            },
            "youtube": {
                "player_client": ["mweb"],
            },
        },
    }

    with YoutubeDL(options) as ydl:
        ydl.download([url])

    return Path(f"{output_path}.mp3")

def download_audio(video_id: str) -> Path:
    output_path = Path(video_id)
    return _download_from_youtube(video_id, output_path)