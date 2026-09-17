import whisper


_model = None


def get_model():
    global _model

    if _model is None:
        _model = whisper.load_model("base.en")

    return _model


def transcribe_audio(audio_path: str):
    model = get_model()

    result = model.transcribe(
        str(audio_path),
        word_timestamps=True,
    )

    return result