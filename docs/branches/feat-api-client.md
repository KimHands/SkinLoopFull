# feat/api-client

## 목적

FastAPI 백엔드와 화면을 연결하기 전에 프론트엔드의 API 계약과 공통 요청 방식을 고정한다.

## 작업 내용

- 백엔드 camelCase 요청·응답에 대응하는 TypeScript 타입 정의
- 브라우저 `localStorage` 기반 익명 UUID 생성 및 재사용
- `NEXT_PUBLIC_API_BASE` 기반 공통 API 클라이언트 구성
- 인증 요청에 `X-Anon-Token` 헤더 자동 첨부
- HTTP 오류와 네트워크 오류를 `ApiError`로 통합
- session, records, patterns, whatif, demo 엔드포인트 함수 제공

## 백엔드 기준

- 확인 브랜치: `origin/feat/backend-core`
- 백엔드 브랜치는 체크아웃하거나 수정하지 않음
- API 경계는 camelCase, 백엔드 내부는 snake_case
- 사진 업로드, 기록 수정, 실험 시작·결과 조회 API는 현재 계약에 없음

## 변경 파일

- `skinloop-fe/types/api.ts`
- `skinloop-fe/lib/anon-token.ts`
- `skinloop-fe/lib/api-client.ts`

## 검증

- 정적 검증 예정: `npm run lint`, `npm run build`
- 현재 환경에서는 `node_modules`가 없고 `npm ci`가 응답 없이 지연되어 설치를 중단함
- 의존성 설치가 가능한 환경에서 위 두 명령을 다시 실행해야 함

## 후속 작업

- `feat/session-store`: 최초 진입 세션 부트스트랩과 전역 세션 상태
- `feat/responsive-app-shell`: PC·태블릿·모바일 공통 레이아웃
- 화면별 브랜치에서 API 클라이언트를 연결
