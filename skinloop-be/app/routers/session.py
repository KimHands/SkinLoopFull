import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as OrmSession

from app.db import get_db
from app.models import Record, Session as SessionModel
from app.schemas import SessionCreate, SessionResponse

router = APIRouter(prefix="/api", tags=["session"])


def _is_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except (ValueError, AttributeError, TypeError):
        return False


@router.post("/session", status_code=201, response_model=SessionResponse)
def create_session(payload: SessionCreate, db: OrmSession = Depends(get_db)):
    """익명 토큰으로 세션 발급. 없으면 생성, 있으면 기존 반환(멱등)."""
    token = payload.anon_token
    if not token:
        raise HTTPException(
            status_code=400,
            detail={"error": "MISSING_TOKEN", "message": "anonToken이 필요합니다"},
        )
    if not _is_uuid(token):
        raise HTTPException(
            status_code=400,
            detail={"error": "INVALID_TOKEN", "message": "anonToken은 UUID 형식이어야 합니다"},
        )

    session = db.query(SessionModel).filter(SessionModel.anon_token == token).first()
    if session is None:
        session = SessionModel(anon_token=token)
        db.add(session)
        db.commit()
        db.refresh(session)

    total = db.query(Record).filter(Record.session_id == session.id).count()
    return SessionResponse(
        session_id=f"sess_{session.id}",
        is_demo=session.is_demo,
        total_records=total,
        created_at=session.created_at,
    )
