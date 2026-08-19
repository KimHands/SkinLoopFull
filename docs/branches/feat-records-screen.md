# feat/records-screen

## 목적
날짜별 기록과 샘플 모드의 완료된 실험 결과를 하나의 화면에서 제공한다.

## 브랜치 관계
- 기준 브랜치: `feat/whatif-screen`

## 작업 내용
- `GET /api/records` 날짜별 목록
- 피부 점수를 범위로 변환해 표시
- 샘플 실험 결과 카드
- `DELETE /api/demo` 확인·종료 동작
- 기존 `/experiment`를 `/records`로 통합

## 검증
- 최종 통합 QA에서 샘플 28건과 샘플 종료 확인
