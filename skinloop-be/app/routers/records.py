from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api", tags=["records"])


@router.post("/records", status_code=201)
def create_record():
    # TODO: 일일 기록 저장 + skin_score 계산 (spec 5절)
    raise HTTPException(status_code=501, detail="NOT_IMPLEMENTED")


@router.get("/records")
def list_records():
    # TODO: 기록 목록 조회 (P1)
    raise HTTPException(status_code=501, detail="NOT_IMPLEMENTED")
