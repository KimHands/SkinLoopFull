# feat/insight-flow

## 목적
분석 로딩부터 기록 부족·정상·폴백 인사이트까지 백엔드 응답 상태를 화면에 반영한다.

## 브랜치 관계
- 기준 브랜치: `feat/record-screen`

## 작업 내용
- `GET /api/patterns` 연결과 재시도
- `NOT_ENOUGH_RECORDS`, `isFallback`, 정상 응답 분기
- 영향 요인 상위 3개, 근거 날짜, 신뢰도 표시
- 통계적 연관성 및 비의료 고지

## 검증
- 최종 통합 QA에서 기록 부족과 샘플 응답 확인
