from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as OrmSession

from app.analysis.frame import MIN_RECORDS, load_session_records
from app.db import get_db
from app.deps import require_session
from app.models import Record, Session as SessionModel
from app.schemas import RecordCreate, RecordItem, RecordResponse
from app.skin_score import calc_skin_score

router = APIRouter(prefix="/api", tags=["records"])


def _duplicate_error(existing: Record) -> HTTPException:
    return HTTPException(
        status_code=409,
        detail={
            "error": "DUPLICATE_DATE",
            "message": "이미 해당 날짜의 기록이 있습니다",
            "recordId": f"rec_{existing.id}",
        },
    )


@router.post("/records", status_code=201, response_model=RecordResponse)
def create_record(
    payload: RecordCreate,
    session: SessionModel = Depends(require_session),
    db: OrmSession = Depends(get_db),
):
    """일일 기록 저장. skin_score 계산 후 저장. 같은 날 중복이면 409."""
    existing = (
        db.query(Record)
        .filter(Record.session_id == session.id, Record.recorded_at == payload.recorded_at)
        .first()
    )
    if existing is not None:
        raise _duplicate_error(existing)

    score = calc_skin_score(payload.skin_redness, payload.skin_acne_count, payload.skin_oiliness)
    record = Record(session_id=session.id, skin_score=score, **payload.model_dump())
    db.add(record)
    try:
        db.commit()
    except IntegrityError:
        # 동시 요청이 같은 날짜를 먼저 넣은 경쟁 조건 → 409로 수렴
        db.rollback()
        existing = (
            db.query(Record)
            .filter(Record.session_id == session.id, Record.recorded_at == payload.recorded_at)
            .first()
        )
        raise _duplicate_error(existing)
    db.refresh(record)

    total = db.query(Record).filter(Record.session_id == session.id).count()
    return RecordResponse(
        record_id=f"rec_{record.id}",
        skin_score=score,
        total_records=total,
        pattern_ready=total >= MIN_RECORDS,
        created_at=record.created_at,
    )


@router.get("/records", response_model=list[RecordItem])
def list_records(
    session: SessionModel = Depends(require_session),
    db: OrmSession = Depends(get_db),
):
    """세션의 기록 목록. recorded_at 오름차순."""
    rows = load_session_records(db, session.id)
    return [
        RecordItem(
            record_id=f"rec_{r.id}",
            recorded_at=r.recorded_at,
            sleep_hours=r.sleep_hours,
            late_snack=r.late_snack,
            stress_level=r.stress_level,
            exercise_min=r.exercise_min,
            cosmetic_changed=r.cosmetic_changed,
            skin_redness=r.skin_redness,
            skin_acne_count=r.skin_acne_count,
            skin_oiliness=r.skin_oiliness,
            skin_score=r.skin_score,
            memo=r.memo,
        )
        for r in rows
    ]
