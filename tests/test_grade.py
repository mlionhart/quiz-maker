def grade(client, **kw):
    return client.post("/api/grade", json={"q": "Q?", "a": "Provides the server", "response": "x", **kw})


def test_exact_ignores_case_spacing_and_end_punctuation(client, ai):
    r = grade(client, grading="exact", response="  provides   THE server. ")
    assert r.json()["correct"] is True
    assert ai.prompt == ""   # exact never calls the AI


def test_exact_mismatch(client, ai):
    r = grade(client, grading="exact", response="something else")
    assert r.json()["correct"] is False


def test_prompt_speaks_to_the_quiz_taker(client, ai):
    ai.reply = {"correct": True, "feedback": "Yes.", "answer": "a"}
    grade(client, grading="standard")
    assert 'as "you"' in ai.prompt
    assert "Never mention the reference answer" in ai.prompt


def test_gist_uses_generous_instruction(client, ai):
    ai.reply = {"correct": True, "feedback": "Yes.", "answer": "a"}
    grade(client, grading="gist")
    assert "main idea" in ai.prompt


def test_model_choice(client, ai):
    ai.reply = {"correct": True, "feedback": "Yes.", "answer": "a"}
    grade(client, grading="standard")
    assert ai.model is None
    grade(client, grading="standard", model="claude-sonnet-5-5")
    assert ai.model == "claude-sonnet-5-5"
    assert grade(client, grading="standard", model="nope").status_code == 422


def test_unparseable_reply_is_502(client, ai):
    ai.reply = None
    assert grade(client, grading="standard").status_code == 502
