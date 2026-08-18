"""환경 설정. 값은 .env 또는 환경변수로 주입한다 (.env.example 참조)."""
import os

from dotenv import load_dotenv

load_dotenv()

# 로컬 P1은 SQLite 기본. 배포 시 Postgres(가비아/Supabase)로 DATABASE_URL 주입.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./skinloop.db")

# CORS 허용 오리진(콤마 구분). 기본은 개발 편의상 전체 허용.
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

# 참고: AI 분석(patterns/whatif)은 in-process(src.*) + llm_formatter가 담당한다.
# LLM 문장화에 OPENAI_API_KEY가 필요하다(llm_formatter가 os.environ에서 직접 읽음).
