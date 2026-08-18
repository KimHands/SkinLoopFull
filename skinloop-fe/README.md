# SkinLoop Frontend

생활 습관과 피부 상태를 함께 기록하고 반복적으로 나타나는 연관 패턴과 4주 시나리오를 살펴보는 Next.js 프론트엔드입니다.

## 요구 사항

- Node.js 20 이상
- npm 또는 pnpm
- `feat/backend-core` 기반 FastAPI 서버

## 환경변수

```powershell
Copy-Item .env.example .env.local
```

기본 예제는 백엔드가 `http://127.0.0.1:8000`에서 실행된다고 가정합니다.

```env
NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000
```

환경변수가 없으면 앱에서 `API_BASE_NOT_CONFIGURED` 오류와 재시도 안내를 표시합니다.

## 실행

```powershell
npm install
npm run dev
```

브라우저에서 [http://localhost:3000](http://localhost:3000)을 엽니다.

## 검증

```powershell
npm run lint
npm run build
```

## 주요 경로

| 경로 | 화면 |
| --- | --- |
| `/` | 기록 진행도와 28일 샘플 진입 |
| `/record` | 생활 습관·피부 상태 기록 |
| `/analyzing` | 패턴 분석 로딩과 재시도 |
| `/insight` | 패턴·근거·신뢰도 |
| `/whatif` | 4주 시나리오 비교 |
| `/records` | 날짜별 기록과 샘플 실험 결과 |

## 백엔드 연결 범위

- `POST /api/session`
- `POST/GET /api/records`
- `GET /api/patterns`
- `POST /api/whatif`
- `GET/DELETE /api/demo`

`POST /api/whatif`의 성공 결과는 백엔드에 별도 AI 서비스의 `AI_SERVICE_URL`이 설정되어야 합니다. AI 서비스가 없으면 백엔드는 503을 반환하고 프론트는 재시도 UI를 표시합니다.

사진은 현재 로컬 미리보기만 지원하며 서버에 업로드되지 않습니다. 기록 수정, 실험 시작, 실험 결과 조회 API도 현재 백엔드 계약에는 포함되어 있지 않습니다.
