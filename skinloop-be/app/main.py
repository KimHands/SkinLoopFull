from contextlib import asynccontextmanager
import os
import re

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import CORS_ORIGINS
from app.routers import demo, patterns, records, session, whatif


def _snake_upper(name: str) -> str:
    """camelCase 필드명을 SNAKE_UPPER로 변환. stressLevel → STRESS_LEVEL."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).upper()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 로컬/데모 부트스트랩용. 프로덕션 스키마는 사람이 수동 생성한다(web.md).
    # compose에서만 AUTO_INIT_DB=1로 켠다.
    if os.getenv("AUTO_INIT_DB") == "1":
        from app.db import init_db

        init_db()
    yield


app = FastAPI(title="SkinLoop API", version="0.1.0", lifespan=lifespan)

_origins = ["*"] if CORS_ORIGINS.strip() == "*" else [o.strip() for o in CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,  # 배포 시 CORS_ORIGINS로 FE 도메인만 허용
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """detail이 dict이면 spec의 {error, message, ...} 형태로 그대로 최상위에 낸다."""
    if isinstance(exc.detail, dict):
        return JSONResponse(status_code=exc.status_code, content=exc.detail, headers=exc.headers)
    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.detail}, headers=exc.headers
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Pydantic 검증 실패(422)를 spec의 400 INVALID_<FIELD> 형태로 변환한다."""
    first = exc.errors()[0] if exc.errors() else {}
    loc = first.get("loc", [])
    field = loc[-1] if loc else "REQUEST"
    code = f"INVALID_{_snake_upper(str(field))}"
    message = first.get("msg", "유효성 검증에 실패했습니다")
    return JSONResponse(status_code=400, content={"error": code, "message": message})


app.include_router(session.router)
app.include_router(records.router)
app.include_router(patterns.router)
app.include_router(whatif.router)
app.include_router(demo.router)


@app.get("/health")
def health():
    return {"status": "ok"}
