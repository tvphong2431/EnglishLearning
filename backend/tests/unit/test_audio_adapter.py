from pathlib import Path
from app.adapters.audio_adapter import _download_from_youtube
from app.adapters.audio_adapter import download_audio


def test_download_audio_returns_audio_path(monkeypatch, tmp_path):
    fake_audio = tmp_path / "abc123.mp3"
    fake_audio.touch()

    def fake_downloader(video_id, output_path):
        assert video_id == "abc123"
        assert output_path == Path("abc123")
        return fake_audio

    monkeypatch.setattr(
        "app.adapters.audio_adapter._download_from_youtube",
        fake_downloader,
    )

    result = download_audio("abc123")

    assert result == fake_audio

def test_download_from_youtube(monkeypatch, tmp_path):
    calls = []

    class FakeYoutubeDL:
        def __init__(self, options):
            calls.append(("init", options))

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def download(self, urls):
            calls.append(("download", urls))

    monkeypatch.setattr(
        "app.adapters.audio_adapter.YoutubeDL",
        FakeYoutubeDL,
    )

    class FakeSettings:
        deno_path = r"C:\fake\deno.exe"
        pot_server_url = "http://fake-pot-server:4416"


    monkeypatch.setattr(
        "app.adapters.audio_adapter.Settings",
        FakeSettings,
    )

    output_path = tmp_path / "abc123"


    result = _download_from_youtube(
        "abc123",
        output_path,
    )

    assert result == Path(f"{output_path}.mp3")

    options = calls[0][1]

    assert options["format"] == "bestaudio/best"
    assert options["outtmpl"] == str(output_path)
    assert options["postprocessors"] == [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }
    ]

    assert options["js_runtimes"] == {
        "deno": {
            "path": r"C:\fake\deno.exe",
        },
    }

    assert options["extractor_args"] == {
        "youtubepot-bgutilhttp": {
            "base_url": "http://fake-pot-server:4416",
        },
        "youtube": {
            "player_client": ["mweb"],
        },
    }


    assert calls[1] == (
        "download",
        ["https://www.youtube.com/watch?v=abc123"],
    )