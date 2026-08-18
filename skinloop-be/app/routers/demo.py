from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as OrmSession

from app.db import get_db
from app.deps import require_session
from app.models import Experiment, Record, Session as SessionModel
from app.schemas import DemoClearedResponse, DemoResponse
from app.seed import DEMO_EXPERIMENT, generate_seed_records

router = APIRouter(prefix="/api", tags=["demo"])


def _wipe_session_data(db: OrmSession, session_id: int) -> None:
    db.query(Record).filter(Record.session_id == session_id).delete()
    db.query(Experiment).filter(Experiment.session_id == session_id).delete()


@router.get("/demo", response_model=DemoResponse)
def load_demo(
    session: SessionModel = Depends(require_session),
    db: OrmSession = Depends(get_db),
):
    """28일치 시드 + 완료 실험 1건 적재. 재호출해도 28건 유지(멱등)."""
    _wipe_session_data(db, session.id)

    rows = generate_seed_records(date.today())
    for row in rows:
        db.add(Record(session_id=session.id, **row))
    db.add(Experiment(session_id=session.id, **DEMO_EXPERIMENT))
    session.is_demo = True
    db.commit()

    return DemoResponse(
        loaded=True,
        is_demo=True,
        record_days=len(rows),
        period={"from": rows[0]["recorded_at"].isoformat(), "to": rows[-1]["recorded_at"].isoformat()},
        message="28일치 샘플 데이터가 적용되었습니다.",
    )


@router.delete("/demo", response_model=DemoClearedResponse)
def clear_demo(
    session: SessionModel = Depends(require_session),
    db: OrmSession = Depends(get_db),
):
    """해당 세션의 records·experiments 전량 삭제, is_demo=false."""
    _wipe_session_data(db, session.id)
    session.is_demo = False
    db.commit()
    return DemoClearedResponse(cleared=True)
