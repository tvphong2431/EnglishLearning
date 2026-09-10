from dataclasses import dataclass


@dataclass
class Sentence:
    text: str
    start: float
    duration: float