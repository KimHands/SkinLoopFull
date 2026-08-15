# FullStack Repo 세부 태스크 (브랜치/PR 단위)

이 레포(skinloop-full)에서 진행하는 작업을 **PR 하나로 끝낼 수 있는 크기**로 쪼갠다.
각 태스크는 브랜치 → TDD 구현 → `/code-review` → PR 순.

## 브랜치 네이밍

```
feat/<scope>      새 기능      예) feat/records-api, feat/insight-screen
fix/<scope>       버그 수정
chore/<scope>     설정·배포·문서
```

- base는 `main`. PR 리뷰어는 반대 파트 담당(FS↔) 1명 이상.

## 태스크 목록

| # | 브랜치 | 내용 | 선행 | 완료 기준(테스트) |
| --- | --- | --- | --- | --- |
| T0 | chore/scaffold | FE/BE 골격 | — | ✅ 완료(직커밋) |
| T1 | chore/db-models | SQLAlchemy 모델(4테이블) + Pydantic 스키마 | 2(스키마) | 모델 import·테이블 매핑 테스트 |
| T2 | feat/session-api | POST /api/session (익명 토큰 멱등) | T1 | 신규 생성 201 / 기존 반환 / 토큰 없으면 400 |
| T3 | feat/records-api | POST /api/records + skin_score + 400/409 | T2 | 저장 201·skin_score 정확·중복 409·유효성 400 |
| T4 | feat/records-list | GET /api/records (P1) | T3 | 세션별 목록·정렬 |
| T5 | feat/home-screen | 홈 `/` + 세션 부트스트랩(UUID·POST /session) | T2 | 최초 진입 세션 생성·기록 유무 분기 |
| T6 | feat/record-screen | 기록 입력 `/record` 폼 + 저장 연동 | T3,T5 | 기본값 저장·409 덮어쓰기·1분 플로우 |
| T7 | feat/demo-api | GET/DELETE /api/demo (시드 적재/해제) | T1, 시드(AI) | 28건+실험1 INSERT·해제 |
| T8 | feat/patterns-api | GET /api/patterns + 폴백 + AI 모듈 연동 | T3, AI habit_pattern | 3상태 응답·LLM 실패 시 impacts 유지 |
| T9 | feat/analyzing-screen | 분석 중 `/analyzing` (5초 대기·타임아웃) | T8 | 대기·타임아웃 폴백 진입 |
| T10 | feat/insight-screen | 인사이트 `/insight` + Recharts 막대 | T8 | 상위3 막대·폴백 시 막대 유지 |
| T11 | feat/whatif-api | POST /api/whatif (range 응답) + AI 연동 | T3, AI whatif | range·trend[4]·direction |
| T12 | feat/whatif-screen | 시나리오 비교 `/whatif` 2선 그래프 | T11 | 칩 선택·2선·range 음영·점추정 금지 |
| T13 | feat/experiment-screen | 실험 결과 `/experiment` (P1, 샘플) | T7 | 전/후·verdict 표시 |
| T14 | chore/deploy | 가비아 서버 배포(FE/BE) + 환경변수 | 서버 생성(8/18) | 공인 IP로 접속 |
| T15 | feat/ui-final-qa | UI 톤 통일 + 6화면 QA + 배너·고지문 | T5·T6·T10·T12 | 완료 기준(08) 통과 |

## 공통 준비 (초기에 한 번)

- `feat/api-client`: FE에 fetch 래퍼(자동 `X-Anon-Token` 헤더, base URL env) + Zustand 세션 스토어.
- `feat/schemas-shared`: 03-types의 TS/Pydantic 타입 확정 + camelCase↔snake_case 직렬화 규칙.
- BE 테스트 하네스: pytest + FastAPI TestClient(이미 설치됨) + 테스트용 SQLite/트랜잭션 롤백.
- FE 테스트: 필요 시 Vitest + Testing Library.

## PR 체크리스트 (템플릿)

```
- [ ] 실패 테스트 먼저 작성 후 구현 (TDD)
- [ ] 표현 규칙 준수(원인 금지·점추정 금지·고지문) — 08-conventions
- [ ] /code-review 통과, 필요 시 static-analysis
- [ ] 관련 스펙 문서(docs/) 갱신
- [ ] 리뷰어 1명 이상 승인
```
