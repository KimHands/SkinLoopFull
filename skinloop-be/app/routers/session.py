from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api", tags=["session"])


@router.post("/session", status_code=201)
def create_session():
    # TODO: 익명 토큰으로 세션 발급 (spec 5절)
    raise HTTPException(status_code=501, detail="NOT_IMPLEMENTED")
