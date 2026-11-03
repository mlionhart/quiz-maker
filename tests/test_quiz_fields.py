import pytest
from pydantic import ValidationError

import main


def quiz(**kw):
    return main.QuizIn(title="T", items=[], **kw)


def test_category_and_difficulty_default_to_empty():
    q = quiz()
    assert q.category == "" and q.difficulty == ""


def test_accepts_known_difficulties():
    for d in ("beginner", "intermediate", "advanced", ""):
        assert quiz(difficulty=d).difficulty == d


def test_rejects_unknown_difficulty():
    with pytest.raises(ValidationError):
        quiz(difficulty="expert")


def test_category_length_limit():
    assert quiz(category="x" * 60).category == "x" * 60
    with pytest.raises(ValidationError):
        quiz(category="x" * 61)
