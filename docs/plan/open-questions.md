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
