# SkinLoop 백엔드 (FastAPI + in-process AI 계산모듈 src/)
FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/srv

WORKDIR /srv

# 의존성 먼저 설치(레이어 캐시). numpy/pandas/scipy/scikit-learn 포함.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# app(백엔드) + src(vendored AI 계산모듈). `from src.*`가 resolve되도록 함께 둔다.
COPY app ./app
COPY src ./src

EXPOSE 8000

# 프로덕션 ASGI. 워커는 서버 사양(2vCore)에 맞춰 조정 가능.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
