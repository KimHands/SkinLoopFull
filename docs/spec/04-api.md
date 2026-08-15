# 04. API 명세

> 원본: `spec.md` §5 — 요청/응답 JSON 예시의 정본은 spec.md.

## 공통

- Base URL은 환경변수(`NEXT_PUBLIC_API_BASE`).
- 모든 요청 헤더에 `X-Anon-Token: {uuid}`.

## 엔드포인트

| 메서드 | 경로 | 용도 | 우선순위 | 현재 상태 |
| --- | --- | --- | --- | --- |
| POST | /api/session | 익명 세션 발급 | P0 | stub(501) |
| POST | /api/records | 일일 기록 저장 | P0 | stub(501) |
| GET | /api/patterns | 패턴 분석 결과 | P0 | stub(501) |
| POST | /api/whatif | 시나리오 비교 | P0 | stub(501) |
| GET | /api/demo | 시드 데이터 로드 | P0 | stub(501) |
| DELETE | /api/demo | 시드 데이터 해제 | P0 | stub(501) |
| GET | /api/records | 기록 목록 조회 | P1 | stub(501) |
| GET | /api/experiments/:id/result | 실험 결과 | P1 | 미생성 |

## 핵심 동작 노트

### POST /api/session
- 없으면 생성, 있으면 기존 세션 반환(멱등). 응답에 `totalRecords` 포함.

### POST /api/records
- 저장 시 `skin_score` 계산(02-data-model) 후 저장.
- 응답 `patternReady`: 총 기록 ≥7이면 true.
- **에러**: 400 `INVALID_*`(유효성), 409 `DUPLICATE_DATE`(같은 날 중복 — 응답에 기존 recordId 포함).

### GET /api/patterns
세 가지 응답 형태(모두 200):
1. **정상**(≥7일): impacts·insight·evidenceDates·suggestedExperiment.
2. **기록 부족**(<7일): `reason:"NOT_ENOUGH_RECORDS"`, `needMore`, `message`.
3. **폴백**(LLM 실패): `isFallback:true`, impacts는 그대로 유지하고 insight만 규칙 기반 문장으로 대체.

confidence 기준:

| 기록 일수 | confidence |
| --- | --- |
| 0~6 | null (분석 불가) |
| 7~13 | low |
| 14~20 | medium |
| 21+ | high |

### POST /api/whatif
- 입력 `{targetHabit, changeValue}`. 대상: sleep_short(시간)·late_snack(주당 횟수↓)·stress(척도↓)·exercise(분).
- **점 추정치 금지** — 항상 `range{min,max}`. `trend`는 4주치 주간 평균 4개.
- `cosmetic_changed`는 whatif 대상에서 제외 ([open-questions](../plan/open-questions.md)에서 의도 확인).

### GET/DELETE /api/demo
- GET: `is_demo=true`, records 28건 + experiments 1건 INSERT(오늘 기준 역산).
- DELETE: 해당 세션 records·experiments 전량 삭제, `is_demo=false`.

## 공통 에러 코드

| 코드 | 상황 |
| --- | --- |
| 400 | 유효성 검증 실패 |
| 401 | X-Anon-Token 누락/미등록 |
| 409 | 중복 기록 |
| 500 | 서버 오류 |
| 503 | AI 일시 불가 (폴백 트리거) |

## 응답 시간 목표

| 엔드포인트 | 목표 |
| --- | --- |
| POST /api/records | 1초 이내 |
| GET /api/patterns | 5초 이내 |
| POST /api/whatif | 5초 이내 |
| GET /api/demo | 2초 이내 |
