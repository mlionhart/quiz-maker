import pytest
from pydantic import ValidationError

import main


def test_true_false_answer_must_be_true_or_false():
    assert main.Item(q="Water is wet", a="True", kind="truefalse").a == "True"
    with pytest.raises(ValidationError):
        main.Item(q="Water is wet", a="maybe", kind="truefalse")
    with pytest.raises(ValidationError):
        main.Item(q="Water is wet", a="", kind="truefalse")


def test_choice_needs_an_answer():
    with pytest.raises(ValidationError):
        main.Item(q="q", a=" ", kind="choice")


def test_exact_written_needs_an_answer():
    with pytest.raises(ValidationError):
        main.Item(q="q", a="", kind="written", grading="exact")
    assert main.Item(q="q", a="", kind="written").a == ""   # AI-graded written questions may have no answer


def test_unknown_kind_rejected():
    with pytest.raises(ValidationError):
        main.Item(q="q", a="a", kind="essay")


def test_what_each_kind_stores():
    assert main.HAS_WRONG_ANSWERS == {"choice", "multiselect"}
    assert main.HAS_EXPLANATION == {"choice", "truefalse", "multiselect"}


def test_distractors_endpoint_accepts_true_false(client, ai):
    ai.reply = [{"d": [], "e": "Because."}]
    r = client.post("/api/distractors", json={"items": [{"q": "Water is wet", "a": "True", "kind": "truefalse"}]})
    assert r.status_code == 200 and r.json()["items"][0]["e"] == "Because."


def test_select_multiple_answers_are_a_json_list():
    assert main.correct_answers('["a", " b ", ""]') == ["a", "b"]
    assert main.correct_answers("not json") == []
    assert main.correct_answers('{"a": 1}') == []
    assert main.correct_answers("[1, 2]") == []
    assert main.Item(q="q", a='["a", "b"]', d=["x"], kind="multiselect").kind == "multiselect"
    for bad in ("", "[]", "plain text", '[""]'):
        with pytest.raises(ValidationError):
            main.Item(q="q", a=bad, kind="multiselect")


def test_select_multiple_fill_shows_separate_options_and_keeps_three(client, ai):
    ai.reply = [{"d": list("abcdefgh"), "e": "Because."}]
    r = client.post("/api/distractors", json={"items": [{"q": "q", "a": '["1","2","3","4","5"]', "kind": "multiselect"}]})
    assert len(r.json()["items"][0]["d"]) == 3
    assert "1; 2; 3; 4; 5" in ai.prompt and '["1"' not in ai.prompt
    assert "never a list" in ai.prompt
