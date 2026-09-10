from app.models.transcript import Sentence
import pytest
@pytest.mark.unit
def test_sentence_model():
    sentence = Sentence(
        text="Hello",
        start=0.0,
        duration=2.5,
    )

    assert sentence.text == "Hello"
    assert sentence.start == 0.0
    assert sentence.duration == 2.5