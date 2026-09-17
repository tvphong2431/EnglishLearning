import pytest

from app.adapters.whisper_adapter import transcribe_audio


class FakeModel:
    def transcribe(self, audio_path, word_timestamps):
        return {
            "text": "Hello world.",
            "segments": [],
        }


@pytest.mark.unit
def test_transcribe_audio(monkeypatch):
    def fake_load_model(model_name):
        return FakeModel()

    monkeypatch.setattr(
        "app.adapters.whisper_adapter.whisper.load_model",
        fake_load_model,
    )

    result = transcribe_audio("test_audio.mp3")

    assert result["text"] == "Hello world."

@pytest.mark.unit
def test_whisper_model_is_loaded_once(monkeypatch):
    load_count = 0

    class FakeModel:
        def transcribe(self, audio_path, word_timestamps):
            return {
                "text": "Hello",
                "segments": [],
            }

    def fake_load_model(model_name):
        nonlocal load_count
        load_count += 1
        return FakeModel()

    monkeypatch.setattr(
        "app.adapters.whisper_adapter.whisper.load_model",
        fake_load_model,
    )

    monkeypatch.setattr(
        "app.adapters.whisper_adapter._model",
        None,
    )

    transcribe_audio("audio_1.mp3")
    transcribe_audio("audio_2.mp3")

    assert load_count == 1