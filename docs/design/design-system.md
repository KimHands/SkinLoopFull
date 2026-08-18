# SkinLoop Design System

Claude Design의 **Design System**에 등록할 정의. 원본의 연분홍 톤은 유지하되 위계·대비·간격을 정리한다.

## 브랜드 원칙

- 부드럽고 신뢰감 있는 스킨케어 톤. **의료 느낌(임상·진단) 지양**, 생활 기록 앱 느낌.
- 데이터는 **범위·경향**으로 부드럽게. 강한 성공/경고 색으로 피부 상태를 단정하지 않는다.
- 모바일 우선. 세로 화면 기준, 데스크톱은 **max-width 480px 중앙 정렬**.

## 컬러 토큰

| 토큰 | HEX | 용도 |
| --- | --- | --- |
| `bg` | `#FDF6F2` | 앱 배경(웜 크림) |
| `surface` | `#FFFFFF` | 카드 표면 |
| `primary` | `#DE8A9C` | 주 버튼·활성 탭·강조 |
| `primary-pressed` | `#C76D80` | 눌림/호버 |
| `primary-soft` | `#F7DEE4` | secondary 버튼 배경·칩 선택 |
| `primary-pale` | `#FBEEF1` | 배너·연한 강조 배경 |
| `border` | `#EFE1DD` | 카드·구분선 |
| `text` | `#2C2A2E` | 본문 기본 |
| `text-sub` | `#6B6B72` | 보조 텍스트 |
| `text-caption` | `#9A9AA0` | 캡션·비활성 |
| `data` | `#8A6D9E` | 그래프 데이터(차분한 퍼플-톤, 중립) |
| `data-band` | `#EDE6F1` | 범위 밴드(min~max) 채움 |

> 접근성: 텍스트-배경 명도대비 **WCAG AA(본문 4.5:1, 큰 텍스트 3:1)** 충족.
> 특히 버튼 라벨은 `primary` 위 **흰색**, secondary는 `text` 위 `primary-soft`로 대비 확보.
> primary 버튼을 연하게 만들어 "비활성처럼" 보이게 하지 말 것.

## 타이포그래피

- 워드마크 로고: **세리프**, 표기는 `SkinLoop` 로 **통일**(SkinLoop/Skin Loop 혼용 금지).
- 본문: **Pretendard**(한글) / system sans. 아래 스케일.

| 역할 | 크기/굵기 |
| --- | --- |
| H1 화면 제목 | 22 / 700 |
| H2 섹션 제목 | 17 / 600 |
| Body | 15 / 400 |
| Body-strong | 15 / 600 |
| Caption | 12 / 400 (최소 12px, 그 이하 금지) |

## 간격·모양 (8pt 그리드)

- 화면 좌우 패딩 **20**, 섹션 간격 **24**, 카드 내부 패딩 **16**.
- 반경: 카드 **16**, 버튼 **12**(또는 pill), 칩 **10**.
- 카드: `surface` + `1px border(border)` (그림자는 아주 옅게 또는 생략, 한 방식으로 통일).

## 컴포넌트

- **Button / primary**: `primary` 채움, 흰 라벨, 높이 48, pill 또는 r12. 눌림 `primary-pressed`.
- **Button / secondary**: `primary-soft` 배경 + `primary` 라벨.
- **Button / disabled**: `border` 배경 + `text-caption` 라벨 (primary 연한색으로 대체 금지).
- **Card**: 위 카드 규칙. 제목(H2) + 내용.
- **Bottom Tab Bar**: 4탭 `홈 · 기록 · 인사이트 · 내 기록`. 아이콘+라벨(12px).
  활성 = `primary` 아이콘/라벨, 비활성 = `text-caption`. **활성 규칙 전 화면 동일**.
- **Segmented (1~5)**: 스트레스·붉은기·유분감 입력용 5칸 세그먼트.
- **Toggle**: 야식·화장품 변화(불리언).
- **Slider**: 수면 시간(0~14h), 운동(0~120분).
- **Impact Bar**: 인사이트 영향도 가로 막대. 색 `data`, 상위 3개.
- **Trend Chart**: 4주(주간 평균 4점) 라인 + **범위 밴드(`data-band`)**. 현재 유지 vs 변경 2계열.
- **Calendar Cell**: 기록 있음(채움/점) · 없음(빈 원) · 선택(테두리) 상태 구분.
- **Confidence Badge**: `low / medium / high` 소형 뱃지(중립색).
- **Disclaimer**: 분석·결과 화면 하단 캡션.
  `"본 분석은 통계적 연관성을 보여주는 참고 자료이며 의학적 진단이 아닙니다."`
