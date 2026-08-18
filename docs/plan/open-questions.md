# 미해결 질문 · 확정 필요 사항

구현 중 최적값으로 정하기로 한 항목과, 팀 결정이 필요한 계약을 모아둔다.
정해지면 해당 스펙 문서와 `spec.md`를 함께 갱신한다.

## 스펙 모순 (구현하며 확정)

| # | 항목 | 충돌 | 상태 |
| --- | --- | --- | --- |
| Q1 | `exercise_min` 상한 | DB/Pydantic 0~300 vs 화면 슬라이더 0~120 | 미정 — 실사용상 120이 자연스러움 |
| Q2 | skin_score 예시 | spec §5 응답 예시(4/3/4→54)가 계산식 결과(신 식 47)와 불일치 | 예시 오타로 추정, 식이 정본 |
| Q3 | whatif `late_snack` | bool 평균에 "주당 횟수" 단위를 빼는 처리 애매 | 미정 — 모델 입력 정규화 방식 정해야 |
| Q4 | whatif `cosmetic_changed` | targetHabit/DELTA에서 제외됨 | 의도 여부 확인 필요 |

> Q1·Q3은 사용자 지침상 "개발 워크플로우 진행하며 최적 결과로 수정".

## 아키텍처 계약

| # | 항목 | 내용 |
| --- | --- | --- |
| A1 | BE ↔ AI Repo 연동 | in-process(패키지/서브모듈) vs HTTP 서비스? 입출력 스키마는 04-api·03-types와 일치 |
| A2 | 직렬화 규칙 | camelCase(FE) ↔ snake_case(BE) 변환 지점 확정 (Pydantic alias/by_alias) |
| A3 | 배포 대상 | 원 spec은 Vercel+App Runner, 실제는 가비아 클라우드 1대 — FE/BE/AI를 한 서버에 어떻게 배치할지 |
| A4 | DB 계정 | web.md상 앱은 read-only. 쓰기(기록 저장)는 별도 계정/경로 필요 → 권한 설계 |

## 운영·팀

| # | 항목 | 내용 |
| --- | --- | --- |
| O1 | QA(구현순서 13) 담당 | 원 spec은 박진영이나 개발 미참여 → 재배정 |
| O2 | 환경변수 목록 | `NEXT_PUBLIC_API_BASE`, `DATABASE_URL`, `OPENAI_API_KEY` 등 공유 방법 |
| O3 | CORS 허용 도메인 | 현재 `*`. 배포 시 FE 도메인으로 좁힘 |

## 결정 로그

정해진 항목은 여기에 한 줄씩 옮긴다.

- (예) 2026-08-__ Q1: exercise 상한 120으로 통일. DB CHECK·Pydantic·화면 일치.
- 2026-08-17 A1(폐기): BE↔AI HTTP 분리안 — feat/backend-core 초안. 아래로 대체됨.
- 2026-08-18 A1(확정): BE↔AI는 **in-process**. patterns/whatif가 `src.habit_pattern`·`src.whatif`를 직접 호출하고 `llm_formatter`로 문장화(PR #4, 김서진). 프론트가 records를 body로 전송(`RecordsPayload`). AI 모듈(`src.*`) 미설치 환경에선 지연 import 가드로 앱은 부팅되고 patterns/whatif만 503. ※ RecordsPayload 주석대로, 추후 DB(records) 기반 session 조회 방식으로 통합 여지.
- 2026-08-17 A2: 직렬화는 **경계 camelCase / 내부 snake_case**. Pydantic `CamelModel`(alias_generator=to_camel, populate_by_name). 요청은 양쪽 허용, 응답은 by_alias.
- 2026-08-17 A4/DB: 로컬 P1은 **SQLite 기본**(`DATABASE_URL` 미설정 시), 모델은 Postgres 호환 포터블 타입. 프로덕션 스키마 생성은 사람이 수동(web.md). 테스트는 인메모리 SQLite.
- 2026-08-17 Q2: skin_score는 **정본 계산식**이 기준. spec §5 예시(4/3/4→54)는 오타, 계산값 47이 정답. 테스트로 고정.
