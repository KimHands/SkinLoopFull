"""환경 설정. 값은 .env 또는 환경변수로 주입한다 (.env.example 참조)."""
import os

from dotenv import load_dotenv

load_dotenv()

# 로컬 P1은 SQLite 기본. 배포 시 Postgres(가비아/Supabase)로 DATABASE_URL 주입.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./skinloop.db")

# AI 분석 엔진은 별도 HTTP 서비스(AI Repo). 미설정/불가 시 폴백.
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "")
AI_TIMEOUT_SECONDS = float(os.getenv("AI_TIMEOUT_SECONDS", "5"))

# CORS 허용 오리진(콤마 구분). 기본은 개발 편의상 전체 허용.
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
