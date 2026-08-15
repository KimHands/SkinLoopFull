# skinloop-be

SkinLoop FullStack Repo의 백엔드 (FastAPI). AI 분석 모듈은 별도 AI Repo.

## 로컬 실행

```bash
cd skinloop-be
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

- 헬스체크: http://localhost:8000/health
- API 문서: http://localhost:8000/docs

## 구조

```
app/
├─ main.py        FastAPI 앱 + CORS + 라우터 등록
├─ db.py          DB 연결 (구현 예정)
├─ models.py      SQLAlchemy 모델 (구현 예정, spec 3절)
├─ schemas.py     Pydantic 스키마 (구현 예정, spec 5절)
└─ routers/       session · records · patterns · whatif · demo (현재 stub)
```

현재는 골격 단계 — 엔드포인트는 501을 반환한다. 상세 명세는 루트의 `spec.md`.
