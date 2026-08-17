"""DB 연결 (SQLAlchemy 2.0).

- 로컬/테스트: SQLite. 배포: Postgres(가비아/Supabase) — DATABASE_URL로 전환.
- 모델은 두 백엔드 모두에 매핑되도록 포터블 타입만 쓴다(JSON/Integer PK).
- web.md 규칙: 프로덕션 스키마 생성·변경은 사람이 수동 수행.
  init_db()는 로컬/테스트 부트스트랩 편의용이다.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import DATABASE_URL

_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=_connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """로컬/테스트에서 테이블을 만든다. 프로덕션에서는 호출하지 않는다."""
    from app import models  # noqa: F401  모델 등록

    Base.metadata.create_all(bind=engine)
