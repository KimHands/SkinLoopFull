# feat/session-store

## 목적

로그인 없이 사용하는 SkinLoop에서 앱 최초 진입 시 익명 세션을 준비하고, 모든 화면이 동일한 세션 상태를 사용하도록 한다.

## 브랜치 관계

- 기준 브랜치: `feat/api-client`
- 선행 커밋: `cbc045c feat: 백엔드 API 클라이언트와 응답 타입 구성`
- `main`에 바로 병합하는 독립 브랜치가 아니라 API 클라이언트 위에 쌓는 스택 브랜치다.

## 작업 내용

- Zustand 세션 스토어 추가
- 최초 렌더링에서 `POST /api/session` 1회 호출
- 세션 ID, 샘플 모드 여부, 총 기록 수를 전역 상태로 관리
- 기록 저장과 샘플 적용 후 화면에서 상태를 갱신할 수 있는 액션 제공
- 세션 준비 중 상태와 네트워크 실패 재시도 화면 제공
- 루트 레이아웃에 세션 부트스트랩 연결

## 변경 파일

- `skinloop-fe/stores/session-store.ts`
- `skinloop-fe/components/session/session-bootstrap.tsx`
- `skinloop-fe/app/layout.tsx`

## 검증

- 정적 검증 예정: `npm run lint`, `npm run build`
- 실제 세션 통합 검증: FastAPI 실행 후 최초 호출 201, 재진입 멱등 응답 확인

## 후속 작업

- `feat/responsive-app-shell`: 반응형 공통 레이아웃과 내비게이션
- `feat/home-screen`: `totalRecords`, `isDemo`에 따른 홈 상태 분기
