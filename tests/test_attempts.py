def test_attempt_score_is_checked_before_the_database(client):
    url = "/api/quizzes/1/attempts"
    assert client.post(url, json={"score": 5, "total": 4}).status_code == 422
    assert client.post(url, json={"score": -1, "total": 4}).status_code == 422
    assert client.post(url, json={"score": 0, "total": 0}).status_code == 422


def test_settings_reject_unknown_task_or_model(client):
    assert client.put("/api/me/settings", json={"models": {"nope": ""}}).status_code == 422
    assert client.put("/api/me/settings", json={"models": {"grade": "gpt-4"}}).status_code == 422


def test_quiz_title_and_category_reach_the_prompts(client, ai):
    ai.reply = [{"d": ["a", "b", "c"], "e": "x"}]
    client.post("/api/distractors", json={"items": [{"q": "Q", "a": '["1", "2"]', "kind": "multiselect"}],
                                          "title": "Windows networking", "category": "Security"})
    assert 'title "Windows networking" and category "Security"' in ai.prompt and "a mix of kinds" in ai.prompt
    ai.reply = ["x"]
    client.post("/api/answers", json={"questions": ["Q?"], "title": "Windows networking"})
    assert 'title "Windows networking"' in ai.prompt and "category" not in ai.prompt
    ai.reply = {"explanation": "y"}
    client.post("/api/explain", json={"q": "Q", "a": "A", "category": "Security"})
    assert 'category "Security"' in ai.prompt
    client.post("/api/explain", json={"q": "Q", "a": "A"})
    assert "belong to a quiz" not in ai.prompt
