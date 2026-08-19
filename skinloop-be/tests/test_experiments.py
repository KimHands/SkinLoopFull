HEADERS = lambda token: {"X-Anon-Token": token}


def test_experiments_empty_without_demo(client, session_token):
    resp = client.get("/api/experiments", headers=HEADERS(session_token))
    assert resp.status_code == 200
    assert resp.json() == []


def test_experiments_missing_token_returns_401(client):
    assert client.get("/api/experiments").status_code == 401


def test_demo_experiment_exposes_real_scores(client, session_token):
    client.get("/api/demo", headers=HEADERS(session_token))
    resp = client.get("/api/experiments", headers=HEADERS(session_token))
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 1
    exp = items[0]
    # 시드가 넣은 실제 값이 camelCase로 노출된다(하드코딩 아님).
    assert exp["targetHabit"] == "sleep_short"
    assert exp["baselineScore"] == 56.4
    assert exp["resultScore"] == 68.2
    assert exp["verdict"] == "improved"
    assert exp["durationDays"] == 14
