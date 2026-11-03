def test_returns_one_answer_per_question(client, ai):
    ai.reply = [" GET ", "Body"]
    r = client.post("/api/answers", json={"questions": ["Most common HTTP method?", "Which part carries data?"]})
    assert r.json()["answers"] == ["GET", "Body"]
    assert "general knowledge" in ai.prompt and "<source_material>" not in ai.prompt


def test_uses_source_when_given(client, ai):
    ai.reply = ["x"]
    client.post("/api/answers", json={"questions": ["Q?"], "source": "Notes about hosting"})
    assert "<source_material>\nNotes about hosting\n</source_material>" in ai.prompt


def test_model_choice(client, ai):
    ai.reply = ["x"]
    client.post("/api/answers", json={"questions": ["Q?"]})
    assert ai.model is None   # server default
    client.post("/api/answers", json={"questions": ["Q?"], "model": "claude-sonnet-5-5"})
    assert ai.model == "claude-sonnet-5-5"


def test_unknown_model_is_422(client, ai):
    ai.reply = ["x"]
    assert client.post("/api/answers", json={"questions": ["Q?"], "model": "gpt-4"}).status_code == 422


def test_settings_lists_models(client):
    s = client.get("/api/settings").json()
    assert s["default"] in [m["id"] for m in s["models"]]


def test_wrong_count_is_502(client, ai):
    ai.reply = ["only one"]
    assert client.post("/api/answers", json={"questions": ["a", "b"]}).status_code == 502


def test_too_many_questions_is_422(client, ai):
    assert client.post("/api/answers", json={"questions": ["q"] * 101}).status_code == 422
