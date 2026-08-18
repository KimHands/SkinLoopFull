def _payload(date_str):
    return {
        "recordedAt": date_str,
        "sleepHours": 7.0,
        "lateSnack": False,
        "stressLevel": 2,
        "exerciseMin": 30,
        "cosmeticChanged": False,
        "skinRedness": 2,
        "skinAcneCount": 2,
        "skinOiliness": 2,
    }


def test_lists_records_sorted_ascending(client, session_token):
    for d in ["2026-08-05", "2026-08-01", "2026-08-03"]:
        client.post("/api/records", json=_payload(d), headers={"X-Anon-Token": session_token})
    resp = client.get("/api/records", headers={"X-Anon-Token": session_token})
    assert resp.status_code == 200
    dates = [r["recordedAt"] for r in resp.json()]
    assert dates == ["2026-08-01", "2026-08-03", "2026-08-05"]


def test_lists_only_own_session_records(client, session_token):
    client.post("/api/records", json=_payload("2026-08-01"), headers={"X-Anon-Token": session_token})
    other = "33333333-3333-3333-3333-333333333333"
    client.post("/api/session", json={"anonToken": other})
    resp = client.get("/api/records", headers={"X-Anon-Token": other})
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_missing_token_returns_401(client):
    resp = client.get("/api/records")
    assert resp.status_code == 401
