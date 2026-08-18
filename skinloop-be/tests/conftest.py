"""테스트 하네스 — 인메모리 SQLite로 격리, 테스트마다 새 DB.

각 테스트는 깨끗한 인메모리 DB를 받고, 앱의 get_db 의존성을 이 DB로 교체한다.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    import app.models  # noqa: F401  모델 등록

    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


ANON_TOKEN = "11111111-1111-1111-1111-111111111111"


@pytest.fixture
def session_token(client):
    """세션을 하나 만들고 그 anonToken을 반환한다."""
    resp = client.post("/api/session", json={"anonToken": ANON_TOKEN})
    assert resp.status_code == 201
    return ANON_TOKEN
