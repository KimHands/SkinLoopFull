from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api", tags=["patterns"])


@router.get("/patterns")
def get_patterns():
    # TODO: 패턴 분석 결과 (AI Repo 모듈 연동 + 폴백) (spec 5·6절)
    raise HTTPException(status_code=501, detail="NOT_IMPLEMENTED")
