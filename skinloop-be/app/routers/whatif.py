from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api", tags=["whatif"])


@router.post("/whatif")
def post_whatif():
    # TODO: 습관 변경 시나리오 비교 (range 응답) (spec 5·6절)
    raise HTTPException(status_code=501, detail="NOT_IMPLEMENTED")
