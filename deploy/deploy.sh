#!/usr/bin/env bash
# 가비아 서버에서 실행: 최신 main으로 스택을 (재)기동한다.
# 사전: Docker/Compose 설치 + 이 레포 clone + deploy/.env 작성(운영값).
# 사용: bash deploy/deploy.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [ ! -f .env ]; then
  echo "[!] .env 가 없습니다. .env.example 을 복사해 운영값을 채우세요:"
  echo "    cp .env.example .env && \$EDITOR .env"
  exit 1
fi

echo "[1/3] 최신 main 반영"
git fetch origin main
git checkout main
git pull --ff-only origin main

echo "[2/3] 이미지 빌드 + 기동(백그라운드)"
docker compose up -d --build

echo "[3/3] 백엔드 준비 대기(테이블은 AUTO_INIT_DB=1로 자동 생성)"
for i in $(seq 1 60); do
  code=$(curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost/api/session \
    -H 'Content-Type: application/json' -d '{"anonToken":"00000000-0000-0000-0000-000000000000"}' || true)
  if [ "$code" = "201" ] || [ "$code" = "200" ]; then
    echo "    backend OK (POST /api/session -> $code)"; break
  fi
  sleep 3
  [ "$i" = "60" ] && { echo "[!] 백엔드가 뜨지 않음"; docker compose logs --tail=50 be; exit 1; }
done

echo "완료. 스모크는: bash deploy/smoke.sh http://localhost"
docker compose ps
