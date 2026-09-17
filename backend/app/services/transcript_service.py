from app.adapters.youtube_adapter import fetch_transcript
from app.models.transcript import Sentence
from app.errors import AppError
from app.adapters.audio_adapter import download_audio
from app.adapters.whisper_adapter import transcribe_audio
import re

def build_sentences(video_id: str) -> list[Sentence]:
    try:
        transcript = fetch_transcript(video_id)

    except AppError as error:
        if error.code not in {
            "TRANSCRIPT_DISABLED",
            "TRANSCRIPT_NOT_FOUND",
        }:
            raise

        audio_path = download_audio(video_id)

        try:
            whisper_result = transcribe_audio(audio_path)
            return build_sentences_from_whisper(whisper_result)

        finally:
            audio_path.unlink(missing_ok=True)


    sentences = []

    for item in transcript:
        sentence = Sentence(
            text=item["text"],
            start=item["start"],
            duration=item["duration"],
            word_count=len(item["text"].split()),
        )

        sentences.append(sentence)

    return sentences

def build_text_sentences_from_youtube(transcript: list[dict]) -> list[str]:
    full_text = ""

    for item in transcript:
        full_text += " " + item["text"]

    full_text = full_text.strip()

    return re.split(r"(?<=[.!?])\s+", full_text)

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