# DB 연결 (SQLAlchemy). 실제 설정은 기능 구현 단계에서 채운다.
# 규칙(web.md): 앱은 read-only 계정으로 연결한다. 스키마 변경·마이그레이션은 사람이 한다.
#
# 예정 구조:
#   engine = create_engine(os.environ["DATABASE_URL"])   # Supabase PostgreSQL
#   SessionLocal = sessionmaker(bind=engine)
