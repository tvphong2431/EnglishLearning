from pathlib import Path
from yt_dlp import YoutubeDL
def _download_from_youtube(video_id: str, output_path: Path) -> Path:
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
    }

    with YoutubeDL(options) as ydl:
        ydl.download([url])

    return output_path

def download_audio(video_id: str) -> Path:
    output_path = Path(f"{video_id}.mp3")
    return _download_from_youtube(video_id, output_path)