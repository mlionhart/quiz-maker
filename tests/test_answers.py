def test_returns_one_answer_per_question(client, ai):
    ai.reply = [" GET ", "Body"]
    r = client.post("/api/answers", json={"questions": ["Most common HTTP method?", "Which part carries data?"]})
    assert r.json() == {"answers": ["GET", "Body"]}
    assert "general knowledge" in ai.prompt and "<source_material>" not in ai.prompt


def test_uses_source_when_given(client, ai):
    ai.reply = ["x"]
    client.post("/api/answers", json={"questions": ["Q?"], "source": "Notes about hosting"})
    assert "<source_material>\nNotes about hosting\n</source_material>" in ai.prompt


def test_wrong_count_is_502(client, ai):
    ai.reply = ["only one"]
    assert client.post("/api/answers", json={"questions": ["a", "b"]}).status_code == 502


def test_too_many_questions_is_422(client, ai):
    assert client.post("/api/answers", json={"questions": ["q"] * 101}).status_code == 422
