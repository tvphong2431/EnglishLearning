from dataclasses import dataclass

from app.models.transcript import Sentence


@dataclass
class Session:
    video_id: str
    sentences: list[Sentence]