"""공통 의존성 — DB 세션, 익명 토큰 인증."""
from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session as OrmSession

from app.db import get_db
from app.models import Session as SessionModel


def require_session(
    x_anon_token: str | None = Header(default=None, alias="X-Anon-Token"),
    db: OrmSession = Depends(get_db),
) -> SessionModel:
    """X-Anon-Token 헤더로 세션을 찾는다. 누락/미등록이면 401."""
    if not x_anon_token:
        raise HTTPException(
            status_code=401,
            detail={"error": "MISSING_TOKEN", "message": "X-Anon-Token 헤더가 필요합니다"},
        )
    session = db.query(SessionModel).filter(SessionModel.anon_token == x_anon_token).first()
    if session is None:
        raise HTTPException(
            status_code=401,
            detail={"error": "UNKNOWN_TOKEN", "message": "등록되지 않은 토큰입니다"},
        )
    return session
