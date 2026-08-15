# SkinLoop UI 생성 가이드 (Claude Design용)

박진영 팀원 UI 초안 → 스펙·프로젝트 규칙에 맞춰 **Claude Design (Beta)** 로 재생성하기 위한 입력 모음.

> ⚠️ Claude Design은 **브라우저에서 직접** 사용하는 Anthropic 웹 도구다. 이 문서는 거기에
> **붙여넣을 프롬프트**일 뿐, 자동 생성은 사람이 실행한다.

## 파일 구성

| 파일 | 용도 |
| --- | --- |
| `design-system.md` | 색·타이포·간격·컴포넌트 정의. Claude Design의 **Design System**에 먼저 등록/첨부 |
| `screen-prompts.md` | 화면별 생성 프롬프트. **Mobile app design** 템플릿에 하나씩 붙여넣기 |
| `reference/SkinLoop Screens.dc.html` | Claude Design이 생성한 **화면 7종 목업**(인터랙티브). `support.js`와 같은 폴더 필수 |
| `reference/support.js` | 위 목업 실행용 런타임(dc-runtime, React 기반). 편집 금지 |
| `review.md` | 위 목업을 스펙·규칙 기준으로 **검토한 결과**(P0/P1/P2 + 남은 개선점) |

## 사용 순서

1. Claude Design 접속 → 템플릿 **Mobile app design** 선택, 모델 **Opus 5**.
2. `design-system.md` 내용을 **Design System**으로 등록(또는 첫 프롬프트에 함께 첨부).
3. `screen-prompts.md`의 **공통 규칙 프리앰블**을 매 프롬프트 앞에 붙인다.
4. 화면 프롬프트를 하나씩 생성 → 결과 확인 → 다음 화면.

## 재생성이 바로잡는 것 (원본 대비)

원본 검토에서 나온 이슈를 프롬프트에 미리 반영했다.

- **P0 규칙 위반**: 점수 점추정 → **범위**, 단정 문구 완화, **하단 고지 문구** 추가,
  스펙 밖 지표(물/세안/수분/탄력/건조함) 제거, 샘플 배너 로직·개수(→28일) 정리.
- **P1 기능 UI**: 인사이트 **영향도 막대(상위 3)**, 시나리오 **현재 vs 변경 범위 비교**,
  기록 **입력 폼**, 캘린더 **요일 헤더·기록일 표시**.

근거: `../spec/`(00~08), `AGENTS.md`(프로젝트 규칙).
