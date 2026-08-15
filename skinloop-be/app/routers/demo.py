from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api", tags=["demo"])


@router.get("/demo")
def load_demo():
    # TODO: 28일치 시드 데이터 적재 (spec 7절)
    raise HTTPException(status_code=501, detail="NOT_IMPLEMENTED")


@router.delete("/demo")
def clear_demo():
    # TODO: 시드 데이터 해제
    raise HTTPException(status_code=501, detail="NOT_IMPLEMENTED")
