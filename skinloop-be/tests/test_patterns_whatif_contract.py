"""patterns/whatif 라우터 계약 회귀 테스트 (명세 04-api 준수).

AI 모듈(src.*)은 이 레포에 없으므로 실제 분석 결과는 검증할 수 없다.
여기서는 명세가 정한 계약만 고정한다:
- patterns는 GET, whatif 입력은 {targetHabit, changeValue}이며 records를 body로 받지 않는다.
- 인증 헤더 누락은 401.
- AI 모듈 미설치 시 503 AI_UNAVAILABLE로 수렴(라우터·세션·DB 조회까지 정상 도달했다는 뜻).
"""

HEADERS = lambda token: {"X-Anon-Token": token}


def test_patterns_is_get(client):
    # POST는 더 이상 허용되지 않는다(405).
    assert client.post("/api/patterns").status_code == 405


def test_patterns_missing_token_returns_401(client):
    assert client.get("/api/patterns").status_code == 401


def test_patterns_happy_path_with_demo(client, session_token):
    # 데모 28일 시드 → 세션 DB 조회 → AI 계산까지 in-process로 도는 통합 경로.
    # AI 의존성(numpy/pandas/scipy/scikit-learn)이 설치돼 있어야 통과한다.
    client.get("/api/demo", headers=HEADERS(session_token))
    resp = client.get("/api/patterns", headers=HEADERS(session_token))
    assert resp.status_code == 200, resp.json()
    body = resp.json()
    assert body["recordDays"] == 28
    assert body["confidence"] == "high"
    assert len(body["impacts"]) == 3
    # 문장화는 OPENAI_API_KEY 없어도 규칙 기반 폴백으로 채워진다.
    assert body["insight"]


def test_whatif_missing_token_returns_401(client):
    resp = client.post("/api/whatif", json={"targetHabit": "sleep_short", "changeValue": 1})
    assert resp.status_code == 401


def test_whatif_happy_path_reads_records_from_session(client, session_token):
    # body에 records를 넣지 않아도, 세션 DB의 기록으로 시나리오를 계산한다.
    client.get("/api/demo", headers=HEADERS(session_token))
    resp = client.post(
        "/api/whatif",
        json={"targetHabit": "sleep_short", "changeValue": 2},
        headers=HEADERS(session_token),
    )
    assert resp.status_code == 200, resp.json()
    body = resp.json()
    assert body["current"]["range"]["min"] <= body["current"]["range"]["max"]
    assert body["changed"]["range"]["min"] <= body["changed"]["range"]["max"]
    assert body["direction"] in {"improve", "worsen", "unclear"}
    assert body["disclaimer"]  # 하단 고지 문구 보장(백엔드 setdefault)


def test_whatif_missing_target_returns_400(client, session_token):
    resp = client.post(
        "/api/whatif",
        json={"changeValue": 1},
        headers=HEADERS(session_token),
    )
    assert resp.status_code == 400
    assert resp.json()["error"].startswith("INVALID_")


def test_whatif_rejects_unknown_target(client, session_token):
    resp = client.post(
        "/api/whatif",
        json={"targetHabit": "cosmetic_changed", "changeValue": 1},
        headers=HEADERS(session_token),
    )
    assert resp.status_code == 400
