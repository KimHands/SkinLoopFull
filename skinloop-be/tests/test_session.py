TOKEN = "22222222-2222-2222-2222-222222222222"


def test_creates_new_session_201(client):
    resp = client.post("/api/session", json={"anonToken": TOKEN})
    assert resp.status_code == 201
    body = resp.json()
    assert body["isDemo"] is False
    assert body["totalRecords"] == 0
    assert body["sessionId"]
    assert body["createdAt"]


def test_existing_token_returns_same_session_idempotent(client):
    first = client.post("/api/session", json={"anonToken": TOKEN}).json()
    resp = client.post("/api/session", json={"anonToken": TOKEN})
    assert resp.status_code == 201
    assert resp.json()["sessionId"] == first["sessionId"]


def test_missing_token_returns_400(client):
    resp = client.post("/api/session", json={})
    assert resp.status_code == 400
    assert resp.json()["error"] == "MISSING_TOKEN"


def test_invalid_token_format_returns_400(client):
    resp = client.post("/api/session", json={"anonToken": "not-a-uuid"})
    assert resp.status_code == 400
    assert resp.json()["error"] == "INVALID_TOKEN"
