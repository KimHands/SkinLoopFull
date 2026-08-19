#!/usr/bin/env bash
# 배포 스모크: 세션→데모→패턴→시나리오→실험→FE홈 을 배포 URL로 확인.
# 사용: bash deploy/smoke.sh http://<공인IP-또는-도메인>
set -euo pipefail

BASE="${1:-http://localhost}"
TOK="$(python3 -c 'import uuid;print(uuid.uuid4())' 2>/dev/null || echo "11111111-1111-1111-1111-111111111111")"
H=(-H "X-Anon-Token: $TOK")
fail() { echo "  ✗ $1"; exit 1; }

echo "BASE=$BASE  token=$TOK"

code=$(curl -s -o /tmp/s.json -w '%{http_code}' -X POST "$BASE/api/session" \
  -H 'Content-Type: application/json' -d "{\"anonToken\":\"$TOK\"}")
[ "$code" = "201" ] || [ "$code" = "200" ] || fail "session $code"; echo "  ✓ session $code"

code=$(curl -s -o /tmp/d.json -w '%{http_code}' "${H[@]}" "$BASE/api/demo")
[ "$code" = "200" ] || fail "demo $code"; echo "  ✓ demo $code ($(grep -o '"recordDays":[0-9]*' /tmp/d.json))"

code=$(curl -s -o /tmp/p.json -w '%{http_code}' "${H[@]}" "$BASE/api/patterns")
[ "$code" = "200" ] || fail "patterns $code ($(cat /tmp/p.json))"
grep -q '"impacts"' /tmp/p.json || fail "patterns: impacts 없음"; echo "  ✓ patterns $code (impacts 있음)"

code=$(curl -s -o /tmp/w.json -w '%{http_code}' "${H[@]}" -X POST "$BASE/api/whatif" \
  -H 'Content-Type: application/json' -d '{"targetHabit":"sleep_short","changeValue":2}')
[ "$code" = "200" ] || fail "whatif $code ($(cat /tmp/w.json))"; echo "  ✓ whatif $code ($(grep -o '"direction":"[a-z]*"' /tmp/w.json))"

code=$(curl -s -o /tmp/e.json -w '%{http_code}' "${H[@]}" "$BASE/api/experiments")
[ "$code" = "200" ] || fail "experiments $code"; echo "  ✓ experiments $code"

code=$(curl -s -o /tmp/h.html -w '%{http_code}' "$BASE/")
[ "$code" = "200" ] || fail "FE home $code"
grep -q "SkinLoop" /tmp/h.html || fail "FE home: SkinLoop 마크업 없음"; echo "  ✓ FE home $code (SkinLoop 렌더)"

echo "SMOKE PASS"
