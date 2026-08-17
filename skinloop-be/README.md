# skinloop-be

SkinLoop FullStack Repo의 백엔드 (FastAPI). AI 분석 엔진은 별도 AI Repo(HTTP 서비스).

## 로컬 실행

```bash
cd skinloop-be
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 로컬은 DATABASE_URL 미설정 시 SQLite(sqlite:///./skinloop.db) 사용.
# 최초 1회 테이블 생성(로컬 편의용. 프로덕션 스키마는 사람이 수동 적용):
python -c "from app.db import init_db; init_db()"

uvicorn app.main:app --reload --port 8000
```

- 헬스체크: http://localhost:8000/health
- API 문서: http://localhost:8000/docs

## 테스트

```bash
pytest              # 인메모리 SQLite, 테스트마다 격리
```

## 구조

```
app/
├─ main.py            FastAPI 앱 + CORS + 예외 핸들러(400/{error} 변환) + 라우터 등록
├─ config.py          환경변수(DATABASE_URL, AI_SERVICE_URL, CORS_ORIGINS)
├─ db.py              SQLAlchemy 엔진/세션/Base. init_db()는 로컬·테스트용
├─ models.py          모델 4테이블(sessions·records·analyses·experiments), 포터블 타입
├─ schemas.py         Pydantic 스키마. 경계는 camelCase alias(A2)
├─ deps.py            get_db · require_session(X-Anon-Token → 세션, 401)
├─ skin_score.py      calc_skin_score (spec §3)
├─ seed.py            28일치 시드 생성 + 완료 실험 1건 (spec §7)
├─ analysis/
│  ├─ engine.py       AI 서비스 HTTP 클라이언트 + AIServiceUnavailable (계약 문서 포함)
│  ├─ fallback.py     규칙 기반 폴백 문장/실험 (spec §6)
│  └─ frame.py        records → AI 입력 프레임, confidence 산정
└─ routers/           session · records · patterns · whatif · demo
```

## 엔드포인트

| 메서드 | 경로 | 상태 |
| --- | --- | --- |
| POST | /api/session | ✅ 익명 토큰 멱등 발급 |
| POST | /api/records | ✅ 저장 + skin_score, 400/409 |
| GET | /api/records | ✅ 세션별 목록(오름차순) |
| GET | /api/patterns | ✅ 3상태(정상/기록부족/폴백) |
| POST | /api/whatif | ✅ range 응답, AI 불가 시 503 |
| GET/DELETE | /api/demo | ✅ 28일 시드 적재/해제(멱등) |

## AI 서비스 연동 (open-questions A1 = HTTP 분리)

`AI_SERVICE_URL`이 가리키는 AI Repo 서비스에 records를 넘겨 통계 결과를 받는다.
미설정/타임아웃/오류 시 patterns는 규칙 폴백(impacts 없이 문장만), whatif는 503.
기대 계약(요청/응답 스키마)은 `app/analysis/engine.py` 상단 docstring 참조.

상세 명세는 루트의 `spec.md` 및 `docs/spec/`.
