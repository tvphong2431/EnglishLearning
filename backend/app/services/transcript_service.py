from app.models.transcript import Sentence
from app.adapters.audio_adapter import download_audio
from app.adapters.whisper_adapter import transcribe_audio

import time


def build_sentences(video_id: str) -> list[Sentence]:
    audio_path = download_audio(video_id)

    try:
        whisper_result = transcribe_audio(audio_path)

        sentences = build_sentences_from_whisper(whisper_result)

        return sentences

    finally:
        audio_path.unlink(missing_ok=True)

def build_sentences_from_whisper(result: dict) -> list[Sentence]:
    sentences = []

    current_text = ""
    sentence_start = None
    sentence_end = None
    word_count = 0

    for segment in result["segments"]:
        for word in segment["words"]:
            text = word["word"]

            if sentence_start is None:
                sentence_start = float(word["start"])

            current_text += text
            sentence_end = float(word["end"])
            word_count += 1

            if text.strip().endswith((".", "?", "!")):
                sentences.append(
                    Sentence(
                        text=current_text.strip(),
                        start=sentence_start,
                        duration=sentence_end - sentence_start,
                        word_count=word_count,
                    )
                )

                current_text = ""
                sentence_start = None
                sentence_end = None
                word_count = 0

    if current_text:
        sentences.append(
            Sentence(
                text=current_text.strip(),
                start=sentence_start,
                duration=sentence_end - sentence_start,
                word_count=word_count
            )
        )

    return sentences