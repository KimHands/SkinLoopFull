def _h(token):
    return {"X-Anon-Token": token}


def test_demo_loads_28_records(client, session_token):
    resp = client.get("/api/demo", headers=_h(session_token))
    assert resp.status_code == 200
    body = resp.json()
    assert body["loaded"] is True
    assert body["isDemo"] is True
    assert body["recordDays"] == 28
    assert body["period"]["from"] and body["period"]["to"]

    listed = client.get("/api/records", headers=_h(session_token)).json()
    assert len(listed) == 28


def test_demo_marks_session_is_demo(client, session_token):
    client.get("/api/demo", headers=_h(session_token))
    sess = client.post("/api/session", json={"anonToken": session_token}).json()
    assert sess["isDemo"] is True
    assert sess["totalRecords"] == 28


def test_demo_is_idempotent(client, session_token):
    client.get("/api/demo", headers=_h(session_token))
    client.get("/api/demo", headers=_h(session_token))
    listed = client.get("/api/records", headers=_h(session_token)).json()
    assert len(listed) == 28


def test_demo_delete_clears(client, session_token):
    client.get("/api/demo", headers=_h(session_token))
    resp = client.delete("/api/demo", headers=_h(session_token))
    assert resp.status_code == 200
    assert resp.json()["cleared"] is True

    listed = client.get("/api/records", headers=_h(session_token)).json()
    assert listed == []
    sess = client.post("/api/session", json={"anonToken": session_token}).json()
    assert sess["isDemo"] is False
