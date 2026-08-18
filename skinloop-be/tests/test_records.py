def _payload(**over):
    base = {
        "recordedAt": "2026-08-13",
        "sleepHours": 5.5,
        "lateSnack": True,
        "stressLevel": 4,
        "exerciseMin": 0,
        "cosmeticChanged": False,
        "skinRedness": 4,
        "skinAcneCount": 3,
        "skinOiliness": 4,
        "memo": "야근함",
    }
    base.update(over)
    return base


def _post(client, token, **over):
    return client.post("/api/records", json=_payload(**over), headers={"X-Anon-Token": token})


def test_saves_record_201_with_skin_score(client, session_token):
    resp = _post(client, session_token)
    assert resp.status_code == 201
    body = resp.json()
    assert body["skinScore"] == 47  # (4,3,4) → 47
    assert body["totalRecords"] == 1
    assert body["patternReady"] is False
    assert body["recordId"]
    assert body["createdAt"]


def test_pattern_ready_true_at_7_records(client, session_token):
    for day in range(1, 8):
        resp = _post(client, session_token, recordedAt=f"2026-08-{day:02d}")
        assert resp.status_code == 201
    assert resp.json()["totalRecords"] == 7
    assert resp.json()["patternReady"] is True


def test_duplicate_date_returns_409_with_record_id(client, session_token):
    first = _post(client, session_token).json()
    resp = _post(client, session_token)
    assert resp.status_code == 409
    body = resp.json()
    assert body["error"] == "DUPLICATE_DATE"
    assert body["recordId"] == first["recordId"]


def test_invalid_stress_level_returns_400(client, session_token):
    resp = _post(client, session_token, stressLevel=6)
    assert resp.status_code == 400
    assert resp.json()["error"] == "INVALID_STRESS_LEVEL"


def test_missing_token_returns_401(client):
    resp = client.post("/api/records", json=_payload())
    assert resp.status_code == 401
    assert resp.json()["error"] == "MISSING_TOKEN"
