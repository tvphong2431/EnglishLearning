from app.adapters.youtube_adapter import fetch_transcript
from app.models.transcript import Sentence


def build_sentences(video_id: str) -> list[Sentence]:
    transcript = fetch_transcript(video_id)

    sentences = []

    for item in transcript:
        sentence = Sentence(
            text=item["text"],
            start=item["start"],
            duration=item["duration"],
        )

        sentences.append(sentence)

    return sentences