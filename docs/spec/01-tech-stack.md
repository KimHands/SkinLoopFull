# 01. 기술 스택 · 레포 구성

> 원본: `spec.md` §2

## 프론트엔드 (skinloop-fe)

| 항목 | 선택 | 용도 |
| --- | --- | --- |
| 프레임워크 | Next.js 15 (App Router) | — |
| 언어 | TypeScript | — |
| 상태 관리 | Zustand | 세션 토큰·기록·분석 결과 캐시 |
| 스타일 | Tailwind CSS | — |
| 그래프 | Recharts | 영향도 막대, 4주 추세선 |
| 배포 | 멋사 제공 가비아 클라우드 (원 spec은 Vercel) | ⚠️ [open-questions](../plan/open-questions.md) |

## 백엔드 (skinloop-be)

| 항목 | 선택 | 용도 |
| --- | --- | --- |
| 프레임워크 | FastAPI (Python 3.11+) | — |
| 검증 | Pydantic | 요청/응답 스키마 |
| ORM | SQLAlchemy | — |
| 드라이버 | psycopg | PostgreSQL |
| 배포 | 멋사 제공 가비아 클라우드 (원 spec은 AWS App Runner) | ⚠️ [open-questions](../plan/open-questions.md) |

## 데이터

- PostgreSQL — Supabase 무료 티어.
- 규칙(web.md): 앱은 **read-only 계정**으로 연결. 스키마 변경·마이그레이션은 **사람이** 수행.

## AI 분석

pandas·numpy(처리), scipy(Spearman 상관), scikit-learn(GBM·permutation importance), openai(GPT-4o, 문장화 전용).
자세한 설계는 [05-ai-module.md](05-ai-module.md).

## 레포 구성 (확정)

| 레포 | 내용 | 위치 |
| --- | --- | --- |
| **FullStack Repo** (`skinloop-full`, 이 레포) | Next.js FE + FastAPI BE | GitHub: KimHands/skinloop-full |
| **AI Repo** | AI 분석 모듈(habit_pattern·whatif·LLM·seed) | GitHub 별도 |

- 원 spec §2는 "AI 분석은 백엔드 내 모듈로 둔다"였으나, **실제 운영은 AI Repo로 분리**한다.
  → BE와 AI 모듈 간 **인터페이스 계약**을 정의해야 함 ([open-questions](../plan/open-questions.md) 참조).

## 실제 폴더 구조 (현재)

```
skinloop-full/
├─ skinloop-fe/     Next.js 15 (App Router)
├─ skinloop-be/     FastAPI
├─ docs/            이 문서
└─ spec.md          단일 소스
```
