from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import session, records, patterns, whatif, demo

app = FastAPI(title="SkinLoop API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: 배포 시 FE 도메인으로 좁힌다
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session.router)
app.include_router(records.router)
app.include_router(patterns.router)
app.include_router(whatif.router)
app.include_router(demo.router)


@app.get("/health")
def health():
    return {"status": "ok"}
