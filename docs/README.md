# SkinLoop 문서

루트 `spec.md`(단일 소스)를 섹션별로 분리·상세화한 문서와, 이후 작업 계획을 모아둔다.

> 긴 알고리즘 코드(habit_pattern, whatif, seed_generator 등)의 **정본은 `spec.md`**다.
> 이 문서들은 구조·표·구현 노트를 담고 필요한 곳에서 `spec.md` 절을 참조한다.

## 스펙 (`spec/`)

| 파일 | 내용 | 원본 |
| --- | --- | --- |
| [00-overview.md](spec/00-overview.md) | 개요·핵심 제약·핵심 기능 3개 | spec §1 |
| [01-tech-stack.md](spec/01-tech-stack.md) | 기술 스택·레포 구성·배포 | spec §2 |
| [02-data-model.md](spec/02-data-model.md) | 테이블 4개·인덱스·skin_score | spec §3 |
| [03-types.md](spec/03-types.md) | TypeScript / Pydantic 타입 | spec §4 |
| [04-api.md](spec/04-api.md) | 엔드포인트·요청/응답·에러·성능 목표 | spec §5 |
| [05-ai-module.md](spec/05-ai-module.md) | HabitPattern·WhatIf·LLM 문장화·폴백 | spec §6 |
| [06-seed.md](spec/06-seed.md) | 28일 시드 설계·검증·적재 | spec §7 |
| [07-screens.md](spec/07-screens.md) | 화면 6개·정보구조·실패 경로 | spec §8 |
| [08-conventions.md](spec/08-conventions.md) | 표현 규칙·구현 안 하는 것·완료 기준 | spec §10·11·12 |

## 계획 (`plan/`)

| 파일 | 내용 |
| --- | --- |
| [work-plan.md](plan/work-plan.md) | 전체 마일스톤·일정·담당(구현 순서 13단계) |
| [fullstack-tasks.md](plan/fullstack-tasks.md) | 이 레포(FullStack) 브랜치/PR 단위 세부 태스크 |
| [open-questions.md](plan/open-questions.md) | 확정 필요한 스펙 모순·인터페이스 계약 |

## 이 레포의 위치

`skinloop-full` = **FullStack Repo** (Next.js FE + FastAPI BE). AI 분석 모듈은 **별도 AI Repo**.
스펙 문서는 제품 전체를 다루므로 AI 파트 내용(§5·6·7 일부)도 포함하되, 실제 구현 위치는 레포가 다를 수 있음.
