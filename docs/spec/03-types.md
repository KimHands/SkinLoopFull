# 03. 타입 정의

> 원본: `spec.md` §4 — 전체 타입 코드의 정본은 spec.md.

## HabitFactor (공통 열거)

```
"sleep_short" | "late_snack" | "stress" | "exercise" | "cosmetic_changed"
```

- DB 컬럼명(`sleep_hours` 등)과 factor 키(`sleep_short` 등)는 다르다 — 매핑은 05-ai-module의 `FACTOR_MAP`.

## 프론트엔드 (TypeScript)

`skinloop-fe/types/`에 둔다. 핵심 인터페이스:

| 타입 | 파일 | 용도 |
| --- | --- | --- |
| `DailyRecord` | types/record.ts | 기록 입력 페이로드 |
| `RecordResponse` | types/record.ts | 저장 응답 (skinScore, patternReady 등) |
| `Impact` | types/analysis.ts | 영향도 항목 (factor·impact·lag·corr) |
| `PatternResult` | types/analysis.ts | 패턴 분석 결과 (기록 부족/폴백 필드 포함) |
| `WhatIfResult` | types/analysis.ts | 시나리오 비교 (current/changed range·trend) |

- `PatternResult`는 세 상태를 한 타입으로 표현: 정상 / 기록부족(`reason:"NOT_ENOUGH_RECORDS"`) / 폴백(`isFallback:true`).
- `WhatIfResult`는 **점 추정치 없이 range**만 — `{min,max}` + `trend[4]`.

## 백엔드 (Pydantic)

`skinloop-be/app/schemas.py`에 둔다. 핵심 모델:

| 모델 | 용도 | 검증 포인트 |
| --- | --- | --- |
| `RecordCreate` | POST /api/records 입력 | sleep 0~14, stress 1~5, skin_* 1~5, exercise 0~300, memo ≤200 |
| `Impact` | 영향도 항목 | — |
| `PatternResponse` | GET /api/patterns 응답 | Optional 필드로 3상태 표현 |

## camelCase ↔ snake_case

- FE(JSON): `recordedAt`, `skinScore`, `patternReady` (camelCase)
- BE(Pydantic/DB): `recorded_at`, `skin_score` (snake_case)
- → BE 응답에서 alias 또는 `by_alias` 직렬화로 변환. **직렬화 규칙을 초기에 확정**해 FE/BE가 어긋나지 않게 한다.
