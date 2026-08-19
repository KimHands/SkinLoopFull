# chore/integration-qa

## 목적
완성된 프론트엔드 화면을 `origin/feat/backend-core`의 실제 FastAPI 응답과 연결하고 빌드·브라우저·반응형 동작을 검증한다.

## 브랜치 관계
- 기준 브랜치: `feat/records-screen`

## 수정 내용
- Next.js 페이지에서 허용되지 않는 추가 export 제거

## 검증 결과
- 프론트 ESLint: 오류 0개, 이미지 미리보기 최적화 경고 1개
- Next.js production build: 성공, 8개 라우트 정적 생성
- backend-core pytest: 35개 통과
- 실제 API: session 201, demo 200, patterns 200, records 200 확인
- 샘플 모드: 28개 기록 렌더링 확인
- whatif: `AI_SERVICE_URL` 미설정 상태에서 백엔드 503 및 프론트 재시도 UI 확인
- 브라우저 콘솔 오류: 0개
- 반응형: 360px 하단 고정 메뉴, 768px 확장 메뉴, 1440px PC 사이드바 확인

## 참고
- 사진 업로드, 기록 수정, 실험 시작·결과 조회는 현재 백엔드 계약에 없음
- 실제 시나리오 성공 결과는 별도 AI Repo 배포 후 `AI_SERVICE_URL` 설정이 필요함
