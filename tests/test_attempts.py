def test_attempt_score_is_checked_before_the_database(client):
    url = "/api/quizzes/1/attempts"
    assert client.post(url, json={"score": 5, "total": 4}).status_code == 422
    assert client.post(url, json={"score": -1, "total": 4}).status_code == 422
    assert client.post(url, json={"score": 0, "total": 0}).status_code == 422
