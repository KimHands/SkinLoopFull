from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as OrmSession

from app.db import get_db
from app.deps import require_session
from app.models import Experiment, Session as SessionModel
from app.schemas import ExperimentItem

router = APIRouter(prefix="/api", tags=["experiments"])


@router.get("/experiments", response_model=list[ExperimentItem])
def list_experiments(
    session: SessionModel = Depends(require_session),
    db: OrmSession = Depends(get_db),
):
    """세션의 실험 목록(완료 실험 포함). 데모 시드가 1건 넣는다."""
    rows = (
        db.query(Experiment)
        .filter(Experiment.session_id == session.id)
        .order_by(Experiment.id.asc())
        .all()
    )
    return [
        ExperimentItem(
            experiment_id=f"exp_{r.id}",
            target_habit=r.target_habit,
            title=r.title,
            duration_days=r.duration_days,
            status=r.status,
            baseline_score=r.baseline_score,
            result_score=r.result_score,
            verdict=r.verdict,
        )
        for r in rows
    ]
