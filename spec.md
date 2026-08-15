# SkinLoop 개발 명세서

생활습관과 피부 상태를 함께 기록하고, 둘 사이의 상관 패턴을 찾아 사용자가 직접 검증하게 하는 웹 서비스.

---

## 1. 개요

### 무엇을 만드는가

사용자가 매일 1분 안에 생활습관(수면·야식·스트레스·운동·화장품)과 피부 상태(붉은기·트러블 개수·유분감)를 기록한다. 기록이 7일 이상 쌓이면 어떤 습관이 피부 변화와 반복적으로 연관되는지 분석해서 보여주고, 습관 하나를 바꿨을 때 4주 뒤 어떻게 달라질지 시나리오로 비교해 준다.

### 핵심 제약


| 제약        | 내용                                                   |
| --------- | ---------------------------------------------------- |
| 로그인 없음    | 회원가입·로그인 화면을 만들지 않는다. 브라우저 localStorage의 익명 UUID로 식별 |
| 모바일 우선    | 세로 화면 기준으로 설계. 데스크톱은 중앙 정렬 컨테이너                      |
| 개발 기간     | 5일. 핵심 기능 3개만 구현                                     |
| 의학적 표현 금지 | 진단명·질병명·치료법 언급 불가. "원인" 대신 "연관 요인"                   |


### 핵심 기능 3개


| 순번  | 기능            | 설명                                 |
| --- | ------------- | ---------------------------------- |
| ①   | 데일리 스킨 체크인    | 로그인 없이 1분 안에 오늘의 습관과 피부 상태를 기록     |
| ②   | 원인 후보 패턴 분석   | 누적 기록에서 영향 가능성이 높은 습관을 순위로 제시      |
| ③   | 습관 변경 시나리오 비교 | 습관 하나를 바꿨을 때 4주 뒤 변화 범위를 현재 유지와 비교 |


---

## 2. 기술 스택

### 프론트엔드

```
Next.js 15 (App Router)
TypeScript
Zustand         상태 관리
Tailwind CSS    스타일
Recharts        그래프 (영향도 막대, 4주 추세선)

```

배포: Vercel

### 백엔드

```
FastAPI (Python 3.11+)
Pydantic        스키마 검증
SQLAlchemy      ORM
psycopg         PostgreSQL 드라이버

```

배포: AWS App Runner

### 데이터

```
PostgreSQL      Supabase 무료 티어

```

### AI 분석

```
pandas, numpy        데이터 처리
scipy                Spearman 상관
scikit-learn         GradientBoostingRegressor, permutation_importance
openai               GPT-4o (문장화 전용)

```

### 레포 구성

```
skinloop-fe    Next.js
skinloop-be    FastAPI + AI 분석 모듈

```

AI 분석은 별도 서비스로 분리하지 않고 백엔드 내 모듈로 둔다. 계산이 요청당 수백 ms 수준이라 분리할 이유가 없다.

---

## 3. 데이터 모델

### 테이블 4개

```
sessions ──1:N──▶ records ──▶ analyses
    │
    └──1:N──▶ experiments

```

users 테이블은 만들지 않는다.

### sessions


| 컬럼             | 타입        | 제약               |
| -------------- | --------- | ---------------- |
| id             | SERIAL    | PK               |
| anon_token     | UUID      | UNIQUE, NOT NULL |
| is_demo        | BOOLEAN   | DEFAULT false    |
| created_at     | TIMESTAMP | DEFAULT now()    |
| last_active_at | TIMESTAMP |                  |


### records


| 컬럼               | 타입           | 제약                                               | 비고         |
| ---------------- | ------------ | ------------------------------------------------ | ---------- |
| id               | SERIAL       | PK                                               |            |
| session_id       | INT          | FK → [sessions.id](http://sessions.id), NOT NULL |            |
| recorded_at      | DATE         | NOT NULL                                         |            |
| sleep_hours      | NUMERIC(3,1) | NOT NULL                                         | 0~14       |
| late_snack       | BOOLEAN      | NOT NULL                                         |            |
| stress_level     | SMALLINT     | NOT NULL, CHECK 1~5                              |            |
| exercise_min     | SMALLINT     | DEFAULT 0                                        | 0~300      |
| cosmetic_changed | BOOLEAN      | DEFAULT false                                    |            |
| skin_redness     | SMALLINT     | NOT NULL, CHECK 1~5                              |            |
| skin_acne_count  | SMALLINT     | NOT NULL, CHECK 1~5                              | 구간값        |
| skin_oiliness    | SMALLINT     | NOT NULL, CHECK 1~5                              |            |
| skin_score       | SMALLINT     | NOT NULL                                         | 계산값 20~100 |
| memo             | VARCHAR(200) | NULL                                             |            |
| created_at       | TIMESTAMP    | DEFAULT now()                                    |            |


`UNIQUE(session_id, recorded_at)` — 하루 1건

### analyses


| 컬럼             | 타입          | 비고                                     |
| -------------- | ----------- | -------------------------------------- |
| id             | SERIAL      | PK                                     |
| session_id     | INT         | FK → [sessions.id](http://sessions.id) |
| impacts        | JSONB       | 계산 결과 배열                               |
| insight        | TEXT        | LLM 생성 문장                              |
| confidence     | VARCHAR(10) | low / medium / high                    |
| evidence_dates | JSONB       | 근거 일자 배열                               |
| record_days    | SMALLINT    | 분석 시점 기록 일수                            |
| is_fallback    | BOOLEAN     | DEFAULT false                          |
| model_version  | VARCHAR(30) |                                        |
| created_at     | TIMESTAMP   | DEFAULT now()                          |


### experiments


| 컬럼             | 타입           | 비고                                     |
| -------------- | ------------ | -------------------------------------- |
| id             | SERIAL       | PK                                     |
| session_id     | INT          | FK → [sessions.id](http://sessions.id) |
| target_habit   | VARCHAR(30)  | NOT NULL                               |
| title          | VARCHAR(100) |                                        |
| duration_days  | SMALLINT     | DEFAULT 14                             |
| status         | VARCHAR(20)  | proposed / running / done              |
| baseline_score | NUMERIC(4,1) |                                        |
| result_score   | NUMERIC(4,1) |                                        |
| verdict        | VARCHAR(20)  | improved / no_change / needs_more      |
| started_at     | DATE         |                                        |
| ended_at       | DATE         |                                        |


### 인덱스

```sql
CREATE UNIQUE INDEX idx_sessions_token ON sessions(anon_token);
CREATE UNIQUE INDEX idx_records_session_date ON records(session_id, recorded_at);
CREATE INDEX idx_records_session ON records(session_id, recorded_at DESC);
CREATE INDEX idx_analyses_session ON analyses(session_id, created_at DESC);

```

### skin_score 계산

```python
def calc_skin_score(redness: int, acne: int, oiliness: int) -> int:
    return round(100 - ((redness + acne + oiliness) / 15 * 100 * 0.8))

```

입력 (1,1,1) → 84점, (5,5,5) → 20점. 애플리케이션 레이어에서 계산해 저장한다.

---

## 4. 타입 정의

### 프론트엔드 (TypeScript)

```typescript
// types/record.ts
export interface DailyRecord {
  recordedAt: string;        // YYYY-MM-DD
  sleepHours: number;        // 0~14, 0.5 단위
  lateSnack: boolean;
  stressLevel: 1 | 2 | 3 | 4 | 5;
  exerciseMin: number;       // 0~300
  cosmeticChanged: boolean;
  skinRedness: 1 | 2 | 3 | 4 | 5;
  skinAcneCount: 1 | 2 | 3 | 4 | 5;
  skinOiliness: 1 | 2 | 3 | 4 | 5;
  memo?: string;
}

export interface RecordResponse {
  recordId: string;
  skinScore: number;
  totalRecords: number;
  patternReady: boolean;
  createdAt: string;
}

// types/analysis.ts
export type HabitFactor =
  | "sleep_short" | "late_snack" | "stress"
  | "exercise" | "cosmetic_changed";

export interface Impact {
  factor: HabitFactor;
  label: string;
  impact: number;   // 0~1
  lag: 0 | 1 | 2 | 3;
  corr: number;     // -1~1
}

export interface PatternResult {
  confidence: "low" | "medium" | "high" | null;
  recordDays: number;
  impacts: Impact[];
  insight: string | null;
  evidenceDates: string[];
  suggestedExperiment?: {
    targetHabit: HabitFactor;
    title: string;
    durationDays: number;
  };
  isFallback: boolean;
  modelVersion?: string;
  // 기록 부족 시에만
  reason?: "NOT_ENOUGH_RECORDS";
  needMore?: number;
  message?: string;
}

export interface WhatIfResult {
  targetHabit: HabitFactor;
  label: string;
  current: { label: string; range: { min: number; max: number }; trend: number[] };
  changed: { label: string; range: { min: number; max: number }; trend: number[] };
  direction: "improve" | "worsen" | "unclear";
  confidence: "low" | "medium" | "high";
  message: string;
  disclaimer: string;
}

```

### 백엔드 (Pydantic)

```python
# schemas.py
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Literal, Optional

HabitFactor = Literal["sleep_short", "late_snack", "stress", "exercise", "cosmetic_changed"]

class RecordCreate(BaseModel):
    recorded_at: date
    sleep_hours: float = Field(ge=0, le=14)
    late_snack: bool
    stress_level: int = Field(ge=1, le=5)
    exercise_min: int = Field(ge=0, le=300, default=0)
    cosmetic_changed: bool = False
    skin_redness: int = Field(ge=1, le=5)
    skin_acne_count: int = Field(ge=1, le=5)
    skin_oiliness: int = Field(ge=1, le=5)
    memo: Optional[str] = Field(None, max_length=200)

class Impact(BaseModel):
    factor: HabitFactor
    label: str
    impact: float
    lag: int
    corr: float

class PatternResponse(BaseModel):
    confidence: Optional[str]
    record_days: int
    impacts: list[Impact]
    insight: Optional[str]
    evidence_dates: list[str] = []
    suggested_experiment: Optional[dict] = None
    is_fallback: bool = False
    model_version: Optional[str] = None
    reason: Optional[str] = None
    need_more: Optional[int] = None
    message: Optional[str] = None

```

---

## 5. API 명세

Base URL은 환경변수로 관리. 모든 요청 헤더에 `X-Anon-Token: {uuid}`를 실는다.

### 엔드포인트 목록


| 메서드    | 경로                          | 용도        | 우선순위 |
| ------ | --------------------------- | --------- | ---- |
| POST   | /api/session                | 익명 세션 발급  | P0   |
| POST   | /api/records                | 일일 기록 저장  | P0   |
| GET    | /api/patterns               | 패턴 분석 결과  | P0   |
| POST   | /api/whatif                 | 시나리오 비교   | P0   |
| GET    | /api/demo                   | 시드 데이터 로드 | P0   |
| DELETE | /api/demo                   | 시드 데이터 해제 | P0   |
| GET    | /api/records                | 기록 목록 조회  | P1   |
| GET    | /api/experiments/:id/result | 실험 결과     | P1   |


### POST /api/session

요청

```json
{ "anonToken": "a1b2c3d4-e5f6-7890-abcd-ef1234567890" }

```

응답 201

```json
{
  "sessionId": "sess_001",
  "isDemo": false,
  "totalRecords": 0,
  "createdAt": "2026-08-13T10:00:00Z"
}

```

### POST /api/records

요청

```json
{
  "recordedAt": "2026-08-13",
  "sleepHours": 5.5,
  "lateSnack": true,
  "stressLevel": 4,
  "exerciseMin": 0,
  "cosmeticChanged": false,
  "skinRedness": 4,
  "skinAcneCount": 3,
  "skinOiliness": 4,
  "memo": "야근함"
}

```

응답 201

```json
{
  "recordId": "rec_0813_ab12",
  "skinScore": 54,
  "totalRecords": 8,
  "patternReady": true,
  "createdAt": "2026-08-13T23:14:00Z"
}

```

응답 400

```json
{ "error": "INVALID_STRESS_LEVEL", "message": "stressLevel은 1~5여야 합니다" }

```

응답 409 (같은 날짜 중복)

```json
{ "error": "DUPLICATE_DATE", "message": "이미 오늘 기록이 있습니다", "recordId": "rec_0813_ab12" }

```

### GET /api/patterns

응답 200 (기록 7일 이상)

```json
{
  "confidence": "high",
  "recordDays": 28,
  "impacts": [
    { "factor": "sleep_short", "label": "6시간 미만 수면", "impact": 0.42, "lag": 1, "corr": 0.61 },
    { "factor": "late_snack", "label": "야식", "impact": 0.31, "lag": 1, "corr": 0.48 },
    { "factor": "stress", "label": "스트레스", "impact": 0.14, "lag": 0, "corr": 0.22 }
  ],
  "insight": "피부 상태가 나빴던 날의 72%에서 전날 수면이 6시간 미만이었습니다.",
  "evidenceDates": ["2026-07-28", "2026-08-02", "2026-08-07"],
  "suggestedExperiment": {
    "targetHabit": "sleep_short",
    "title": "취침 시간 40분 앞당기기",
    "durationDays": 14
  },
  "isFallback": false,
  "modelVersion": "habitpattern-v1.0"
}

```

응답 200 (기록 7일 미만)

```json
{
  "confidence": null,
  "recordDays": 3,
  "impacts": [],
  "insight": null,
  "reason": "NOT_ENOUGH_RECORDS",
  "needMore": 4,
  "message": "앞으로 4일 더 기록하면 패턴 분석이 시작됩니다."
}

```

응답 200 (LLM 실패 시 폴백)

```json
{
  "confidence": "medium",
  "recordDays": 14,
  "impacts": [ /* 계산 결과 그대로 유지 */ ],
  "insight": "6시간 미만 수면이 다음 날 피부 상태와 가장 높은 연관을 보였습니다.",
  "isFallback": true
}

```

폴백 상황에서도 impacts는 그대로 담는다. 프론트는 그래프를 그리고 문장만 대체한다.

confidence 기준


| 기록 일수  | confidence   |
| ------ | ------------ |
| 0~6일   | null (분석 불가) |
| 7~13일  | low          |
| 14~20일 | medium       |
| 21일 이상 | high         |


### POST /api/whatif

요청

```json
{ "targetHabit": "sleep_short", "changeValue": 1.0 }

```


| targetHabit | 의미        | changeValue 단위 |
| ----------- | --------- | -------------- |
| sleep_short | 수면 시간 늘리기 | 시간             |
| late_snack  | 야식 줄이기    | 주당 횟수 감소       |
| stress      | 스트레스 관리   | 척도 감소          |
| exercise    | 운동 늘리기    | 분              |


응답 200

```json
{
  "targetHabit": "sleep_short",
  "label": "수면 +1시간",
  "current": {
    "label": "현재 습관 유지",
    "range": { "min": 52, "max": 58 },
    "trend": [54, 54, 53, 55]
  },
  "changed": {
    "label": "수면 +1시간 적용",
    "range": { "min": 60, "max": 66 },
    "trend": [55, 58, 61, 63]
  },
  "direction": "improve",
  "confidence": "medium",
  "message": "수면을 1시간 늘린 경우, 지금까지 기록에서 좋았던 날들과 유사한 패턴을 보입니다.",
  "disclaimer": "예측이 아닌 시나리오 비교이며, 실제 결과는 다를 수 있습니다."
}

```

점 추정치는 응답하지 않는다. 항상 range로 낸다. trend는 4주치 주간 평균 4개 값.

### GET /api/demo

응답 200

```json
{
  "loaded": true,
  "isDemo": true,
  "recordDays": 28,
  "period": { "from": "2026-07-17", "to": "2026-08-13" },
  "message": "28일치 샘플 데이터가 적용되었습니다."
}

```

`DELETE /api/demo` → `{ "cleared": true }`

### 공통 에러


| 코드  | 상황                     |
| --- | ---------------------- |
| 400 | 유효성 검증 실패              |
| 401 | X-Anon-Token 누락 또는 미등록 |
| 409 | 중복 기록                  |
| 500 | 서버 오류                  |
| 503 | AI 서비스 일시 불가 (폴백 트리거)  |


### 응답 시간 목표


| 엔드포인트             | 목표    |
| ----------------- | ----- |
| POST /api/records | 1초 이내 |
| GET /api/patterns | 5초 이내 |
| POST /api/whatif  | 5초 이내 |
| GET /api/demo     | 2초 이내 |


---

## 6. AI 분석 모듈

### 설계 원칙

영향도 계산은 통계 모델이 하고, LLM은 그 숫자를 문장으로 바꾸는 역할만 한다. LLM에 계산을 맡기면 없는 수치를 만들어내고 결과의 근거를 설명할 수 없다.

```
[기록 N일]
     ▼
[HabitPattern]  Spearman(lag 0~3) → GBM → permutation importance
     │ impacts[] (숫자)
     ├──────────────┬──────────────┐
     ▼              ▼              ▼
[WhatIf]      [실험 검증]      [LLM 문장화]
회귀 예측      전후 비교        GPT-4o
     │              │              │
     └──────────────┴──────────────┘
                    ▼
            [폴백] 규칙 기반 문장

```

### HabitPattern 구현

```python
# ai/habit_pattern.py
import pandas as pd
from scipy.stats import spearmanr
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.inspection import permutation_importance

HABITS = ["sleep_hours", "stress_level", "late_snack", "exercise_min", "cosmetic_changed"]

LABELS = {
    "sleep_short": "6시간 미만 수면",
    "late_snack": "야식",
    "stress": "스트레스",
    "exercise": "운동 부족",
    "cosmetic_changed": "화장품 변경",
}

FACTOR_MAP = {
    "sleep_hours": "sleep_short",
    "stress_level": "stress",
    "late_snack": "late_snack",
    "exercise_min": "exercise",
    "cosmetic_changed": "cosmetic_changed",
}

MODEL_VERSION = "habitpattern-v1.0"


def habit_pattern(df: pd.DataFrame) -> dict:
    """
    df: recorded_at 오름차순 정렬된 일자별 기록.
        컬럼은 HABITS + skin_score.
    """
    n = len(df)
    if n < 7:
        return {
            "confidence": None, "record_days": n, "impacts": [], "insight": None,
            "reason": "NOT_ENOUGH_RECORDS", "need_more": 7 - n,
            "message": f"앞으로 {7 - n}일 더 기록하면 패턴 분석이 시작됩니다.",
        }

    df = df.copy()
    df["late_snack"] = df["late_snack"].astype(int)
    df["cosmetic_changed"] = df["cosmetic_changed"].astype(int)

    # (a) lag 0~3일 Spearman 교차상관. 습관(t) → 피부(t+lag)
    lag_info = {}
    for h in HABITS:
        best_lag, best_corr = 0, 0.0
        for lag in range(0, 4):
            if n - lag < 5:
                continue
            x = df[h].iloc[: n - lag]
            y = df["skin_score"].iloc[lag:]
            c = spearmanr(x, y).correlation
            if c is not None and c == c and abs(c) > abs(best_corr):
                best_lag, best_corr = lag, c
        lag_info[h] = {"lag": best_lag, "corr": round(float(best_corr), 3)}

    # (b) GBM + permutation importance
    X, y = df[HABITS], df["skin_score"]
    model = GradientBoostingRegressor(random_state=42).fit(X, y)
    imp = permutation_importance(model, X, y, n_repeats=30, random_state=42)

    impacts = []
    for i, h in enumerate(HABITS):
        factor = FACTOR_MAP[h]
        impacts.append({
            "factor": factor,
            "label": LABELS[factor],
            "impact": round(float(max(imp.importances_mean[i], 0.0)), 3),
            "lag": lag_info[h]["lag"],
            "corr": lag_info[h]["corr"],
        })
    impacts.sort(key=lambda d: d["impact"], reverse=True)

    confidence = "high" if n >= 21 else ("medium" if n >= 14 else "low")

    # 근거 일자: skin_score 하위 3일
    evidence = df.nsmallest(3, "skin_score")["recorded_at"].astype(str).tolist()

    return {
        "confidence": confidence,
        "record_days": n,
        "impacts": impacts[:3],
        "evidence_dates": sorted(evidence),
        "model_version": MODEL_VERSION,
    }

```

lag를 두는 이유는 피부가 습관 다음 날 반응하기 때문이다. lag 0만 보면 잡히지 않는다. permutation importance를 쓰는 이유는 수면과 스트레스가 서로 상관돼 있어 단순 상관만으로는 구분이 안 되기 때문이다.

### WhatIf 구현

```python
# ai/whatif.py
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

HABITS = ["sleep_hours", "stress_level", "late_snack", "exercise_min", "cosmetic_changed"]

DELTA = {   # targetHabit → (컬럼, 변화량 부호)
    "sleep_short": ("sleep_hours", +1),
    "late_snack": ("late_snack", -1),
    "stress": ("stress_level", -1),
    "exercise": ("exercise_min", +1),
}


def whatif(df: pd.DataFrame, target_habit: str, change_value: float) -> dict:
    df = df.copy()
    df["late_snack"] = df["late_snack"].astype(int)
    df["cosmetic_changed"] = df["cosmetic_changed"].astype(int)

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(df[HABITS], df["skin_score"])

    recent = df[HABITS].tail(7).mean()

    base_pred = float(model.predict([recent.values])[0])

    col, sign = DELTA[target_habit]
    changed = recent.copy()
    changed[col] = changed[col] + sign * change_value
    changed_pred = float(model.predict([changed.values])[0])

    # 예측 불확실성은 개별 트리 예측의 표준편차로 근사
    def spread(row):
        preds = np.array([t.predict([row.values])[0] for t in model.estimators_])
        return float(preds.std())

    base_sd, changed_sd = spread(recent), spread(changed)

    def to_range(center, sd):
        return {"min": round(center - sd), "max": round(center + sd)}

    # 4주 추세는 선형 보간
    def trend(start, end):
        return [round(start + (end - start) * (i + 1) / 4) for i in range(4)]

    diff = changed_pred - base_pred
    direction = "improve" if diff > 2 else ("worsen" if diff < -2 else "unclear")

    n = len(df)
    confidence = "high" if n >= 21 else ("medium" if n >= 14 else "low")

    return {
        "target_habit": target_habit,
        "current": {
            "label": "현재 습관 유지",
            "range": to_range(base_pred, base_sd),
            "trend": trend(base_pred, base_pred),
        },
        "changed": {
            "label": "습관 변경 적용",
            "range": to_range(changed_pred, changed_sd),
            "trend": trend(base_pred, changed_pred),
        },
        "direction": direction,
        "confidence": confidence,
        "disclaimer": "예측이 아닌 시나리오 비교이며, 실제 결과는 다를 수 있습니다.",
    }

```

### LLM 문장화

System 프롬프트

```
당신은 생활습관 기록 분석 결과를 사용자에게 설명하는 도우미입니다.
통계 모델이 이미 계산을 끝냈습니다. 당신은 계산하지 마세요.

규칙:
1. 주어진 impacts 목록의 1~2위만 언급하세요. 목록에 없는 요인을 만들지 마세요.
2. 새로운 수치를 만들지 마세요. 주어진 값만 사용하세요.
3. '원인'이라고 단정하지 마세요. '연관 요인', '영향 가능성이 높은 요인'으로 표현하세요.
4. 의학적 진단, 질병명, 치료법을 언급하지 마세요.
5. confidence가 low면 단정하지 말고 '가능성', '경향'으로 표현하세요.
6. 문장은 2문장 이내로 쓰세요.
7. impacts 1위 요인 하나만 바꾸는 14일 실험을 제안하세요.
8. 반드시 JSON만 출력하세요. 설명, 마크다운, 코드블록 금지.

출력 형식:
{
  "insight": "...",
  "experiment": { "targetHabit": "...", "title": "...", "durationDays": 14 }
}

```

User 메시지에는 impacts, confidence, recordDays, evidenceDates를 텍스트로 넣는다.

### 폴백

```python
# ai/fallback.py
FALLBACK_INSIGHT = {
    "sleep_short": "6시간 미만 수면이 다음 날 피부 상태와 가장 높은 연관을 보였습니다.",
    "late_snack": "야식이 다음 날 피부 상태와 높은 연관을 보였습니다.",
    "stress": "스트레스가 높았던 날 피부 상태가 낮게 기록되었습니다.",
    "exercise": "운동량과 피부 상태 사이에 일정한 경향이 나타났습니다.",
    "cosmetic_changed": "화장품 변경 시점과 피부 변화가 함께 나타났습니다.",
}

FALLBACK_EXPERIMENT = {
    "sleep_short": ("취침 시간 40분 앞당기기", 14),
    "late_snack": ("야식 주 2회 이하로 줄이기", 14),
    "stress": ("취침 전 10분 이완 루틴", 14),
    "exercise": ("주 3회 20분 걷기", 14),
    "cosmetic_changed": ("2주간 화장품 변경 없이 유지하기", 14),
}


def fallback(impacts: list[dict]) -> dict:
    if not impacts:
        return {"insight": "기록이 더 쌓이면 더 정확한 패턴을 찾을 수 있어요.", "is_fallback": True}
    top = impacts[0]["factor"]
    title, days = FALLBACK_EXPERIMENT.get(top, ("생활습관 하나 바꿔보기", 14))
    return {
        "insight": FALLBACK_INSIGHT.get(top, "기록에서 일정한 경향이 나타났습니다."),
        "suggested_experiment": {"targetHabit": top, "title": title, "durationDays": days},
        "is_fallback": True,
    }

```

GPT 호출은 try/except로 감싸고, 예외나 5초 타임아웃 시 폴백을 쓴다. impacts는 그대로 유지한다.

---

## 7. 시드 데이터

기록이 없으면 기능 ②③을 확인할 수 없다. 28일치 시드를 만들어 버튼 한 번으로 적용한다.

### 구간 설계

```
Day 1~10    양호   수면 7~8h, 야식 없음, 스트레스 1~2  → skin_score 72~78
Day 11~20   악화   수면 4.5~5.5h 6일, 야식 6일, 스트레스 4~5 → 52~60
Day 21~28   회복   수면 6.5~7.5h, 야식 1회, 스트레스 2~3 → 66~72

```

수면 부족을 1위(impact 0.4대), 야식을 2위(0.3대), 스트레스를 3위(0.1대)로 심는다. 운동과 화장품에는 일부러 상관을 심지 않는다. 모델이 없는 패턴을 만들어내지 않는지 확인하는 대조군이다.

### 생성 스크립트

```python
# scripts/seed_generator.py
import random, json
from datetime import date, timedelta

random.seed(42)   # 매번 같은 데이터가 나오도록 고정


def skin_score(r, a, o):
    return round(100 - ((r + a + o) / 15 * 100 * 0.8))


def make_day(i, today):
    d = today - timedelta(days=27 - i)

    if i < 10:
        sleep = round(random.uniform(7.0, 8.0), 1)
        snack, stress = False, random.randint(1, 2)
        ex, base = random.choice([20, 30, 40]), random.randint(1, 2)
    elif i < 20:
        bad = random.random() < 0.6
        sleep = round(random.uniform(4.5, 5.5), 1) if bad else round(random.uniform(6.5, 7.0), 1)
        snack = bad
        stress = random.randint(4, 5) if bad else 3
        ex, base = 0, (random.randint(4, 5) if bad else 3)
    else:
        sleep = round(random.uniform(6.5, 7.5), 1)
        snack = random.random() < 0.15
        stress = random.randint(2, 3)
        ex, base = random.choice([20, 30]), random.randint(2, 3)

    r = min(5, max(1, base + random.choice([-1, 0, 0, 1])))
    a = min(5, max(1, base + random.choice([-1, 0, 0])))
    o = min(5, max(1, base + random.choice([0, 0, 1])))

    return {
        "recorded_at": d.isoformat(),
        "sleep_hours": sleep,
        "late_snack": snack,
        "stress_level": stress,
        "exercise_min": ex,
        "cosmetic_changed": random.random() < 0.1,
        "skin_redness": r,
        "skin_acne_count": a,
        "skin_oiliness": o,
        "skin_score": skin_score(r, a, o),
        "memo": None,
    }


if __name__ == "__main__":
    today = date.today()
    seed = [make_day(i, today) for i in range(28)]
    with open("seed_28days.json", "w", encoding="utf-8") as f:
        json.dump(seed, f, ensure_ascii=False, indent=2)

```

### 완료된 실험 1건

시드와 함께 experiments 테이블에 넣는다.

```json
{
  "target_habit": "sleep_short",
  "title": "취침 시간 40분 앞당기기",
  "duration_days": 14,
  "status": "done",
  "baseline_score": 56.4,
  "result_score": 68.2,
  "verdict": "improved"
}

```

### 검증

생성 후 아래를 확인한다. 하나라도 실패하면 상관 강도를 조정해 재생성한다.

```
[ ] habit_pattern() 결과의 impacts 1위가 sleep_short인가
[ ] 2위가 late_snack인가
[ ] exercise와 cosmetic_changed의 impact가 0.1 미만인가
[ ] confidence가 high인가 (28일)
[ ] whatif("sleep_short", 1.0)의 direction이 improve인가
[ ] Day 21~28 평균이 Day 11~20 평균보다 8점 이상 높은가

```

### 적재

별도 테이블을 만들지 않고 같은 구조로 INSERT 한다.

```
GET /api/demo
  sessions.is_demo = true
  records 28건 INSERT (recorded_at은 오늘 기준 역산)
  experiments 1건 INSERT

DELETE /api/demo
  해당 세션의 records, experiments 전량 삭제
  is_demo = false

```

---

## 8. 화면 명세

전체 6개. 모바일 세로 기준으로 설계하고 데스크톱은 max-width 480px 중앙 정렬.

### 정보구조

```
홈
├─ 기록 입력
├─ 분석 중 (로딩)
├─ 인사이트
│   └─ 시나리오 비교
└─ 실험 결과 (샘플 모드)

```

### 1. 홈 `/`

```
┌─────────────────────────────────┐
│  SkinLoop                       │
│                                 │
│  [기록 있음]                     │
│    오늘의 피부 점수 68           │
│    기록 8일차 · 패턴 분석 가능    │
│    [ 인사이트 보기 ]             │
│                                 │
│  [기록 없음]                     │
│    오늘의 피부, 기록해 볼까요?    │
│                                 │
│  [ 오늘 기록하기 ]  ← 주 CTA     │
│                                 │
│  ─────── 또는 ───────            │
│                                 │
│  [ 28일치 샘플로 둘러보기 ]       │
└─────────────────────────────────┘

```

동작

- 최초 진입 시 localStorage에 UUID가 없으면 생성하고 `POST /api/session` 호출
- 기록 1~6일차면 "앞으로 N일 더 기록하면 패턴 분석이 시작됩니다 (n/7)" 진행도 표시
- 샘플 버튼은 항상 노출. 처음 오는 사람이 즉시 결과를 볼 수 있는 유일한 경로

### 2. 기록 입력 `/record`

한 화면에 전부 넣는다. 스텝을 나누지 않는다. 목표는 1분 이내 완료.

```
┌─────────────────────────────────┐
│  ← 오늘의 기록                   │
│                                 │
│  생활습관                        │
│  수면 시간      [====○──] 6.5h   │
│  야식           [ 안 먹음 | 먹음 ]│
│  스트레스       [==○────] 3      │
│  운동           [=○─────] 20분   │
│  화장품 변경    [ 없음 | 있음 ]   │
│                                 │
│  피부 상태                       │
│  붉은기         ○ ○ ● ○ ○       │
│  트러블 개수    ○ ● ○ ○ ○       │
│  유분감         ○ ○ ○ ● ○       │
│                                 │
│  메모 (선택)    [____________]   │
│                                 │
│  [ 저장하기 ]                    │
└─────────────────────────────────┘

```

입력 컴포넌트


| 항목     | 컴포넌트   | 범위                                | 기본값  |
| ------ | ------ | --------------------------------- | ---- |
| 수면 시간  | 슬라이더   | 0~14, 0.5 단위                      | 7.0  |
| 야식     | 2지 선택  | boolean                           | 안 먹음 |
| 스트레스   | 슬라이더   | 1~5                               | 3    |
| 운동     | 슬라이더   | 0~120분, 10분 단위                    | 0    |
| 화장품 변경 | 2지 선택  | boolean                           | 없음   |
| 붉은기    | 5점 라디오 | 1~5                               | 3    |
| 트러블 개수 | 5점 라디오 | 1~5 (0개 / 1~2 / 3~5 / 6~10 / 10+) | 2    |
| 유분감    | 5점 라디오 | 1~5                               | 3    |


동작

- 전부 기본값이 있어 슬라이더를 안 만져도 저장 가능
- 저장 시 `POST /api/records`
- 409(중복)면 "오늘 기록을 수정할까요?" 확인 후 덮어쓰기
- 저장 후 `patternReady`가 true면 분석 중 화면으로, false면 홈으로

### 3. 분석 중 `/analyzing`

```
┌─────────────────────────────────┐
│                                 │
│         [진행 애니메이션]         │
│                                 │
│    기록을 살펴보고 있어요         │
│                                 │
└─────────────────────────────────┘

```

`GET /api/patterns` 호출. 최대 5초 대기 후 결과 화면으로. 타임아웃되면 폴백 결과로 진입.

### 4. 인사이트 `/insight`

```
┌─────────────────────────────────┐
│  ← 내 패턴                       │
│                                 │
│  피부 상태가 나빴던 날의 대부분에서│
│  전날 수면이 6시간 미만이었습니다. │
│                                 │
│  분석 신뢰도  높음 (28일 기록)    │
│                                 │
│  영향 가능성이 높은 요인          │
│  ┌───────────────────────────┐  │
│  │ 6시간 미만 수면 ████████ 0.42│ │
│  │ 야식           ██████ 0.31 │  │
│  │ 스트레스       ███ 0.14    │  │
│  └───────────────────────────┘  │
│                                 │
│  근거가 된 날                     │
│  7/28 (54점) 8/2 (52점) 8/7 (56)│
│                                 │
│  ┌───────────────────────────┐  │
│  │ 이번 실험 제안              │  │
│  │ 취침 시간 40분 앞당기기      │  │
│  │ 14일                       │  │
│  │ [ 시나리오 비교하기 ]        │  │
│  └───────────────────────────┘  │
│                                 │
│  본 분석은 통계적 연관성을 보여주는│
│  참고 자료이며 의학적 진단이 아닙니다│
└─────────────────────────────────┘

```

동작

- 영향도는 Recharts 가로 막대. 상위 3개만
- `isFallback: true`면 문장 아래에 "일시적으로 간단 분석을 보여드리고 있어요" + 재시도 버튼. **막대그래프는 그대로 표시**
- 기록 7일 미만이면 진행도와 샘플 버튼만 표시

### 5. 시나리오 비교 `/whatif`

```
┌─────────────────────────────────┐
│  ← 습관을 바꾸면                  │
│                                 │
│  어떤 습관을 바꿔볼까요?          │
│  [수면 +1시간] [야식 줄이기]      │
│  [스트레스 관리] [운동 늘리기]     │
│                                 │
│  4주 뒤 예상                     │
│  ┌───────────────────────────┐  │
│  │        ╱───── 변경 60~66   │  │
│  │    ╱                       │  │
│  │ ──────────── 유지 52~58    │  │
│  │  1주  2주  3주  4주         │  │
│  └───────────────────────────┘  │
│                                 │
│  수면을 1시간 늘린 경우, 지금까지  │
│  기록에서 좋았던 날들과 유사한     │
│  패턴을 보입니다.                 │
│                                 │
│  예측이 아닌 시나리오 비교이며     │
│  실제 결과는 다를 수 있습니다.     │
│                                 │
│  [ 이 실험 시작하기 ]  (P1)       │
└─────────────────────────────────┘

```

동작

- 습관 칩 선택 시 `POST /api/whatif`
- Recharts LineChart 2선. 범위는 Area로 음영 처리
- **점 추정치를 화면에 쓰지 않는다.** 항상 "60~66" 형태

### 6. 실험 결과 `/experiment` (P1, 샘플 모드에서만)

```
┌─────────────────────────────────┐
│  ← 실험 결과                     │
│                                 │
│  취침 시간 40분 앞당기기          │
│  8/1 ~ 8/14 (14일)              │
│                                 │
│  실험 전 평균   56.4             │
│  실험 후 평균   68.2             │
│  변화          +11.8             │
│                                 │
│  [ 개선 ]                        │
│                                 │
│  이 습관은 개선 가능성이 있는      │
│  요인으로 저장되었습니다.          │
└─────────────────────────────────┘

```

### 샘플 모드 배너

샘플 모드일 때 모든 화면 상단에 고정 표시.

```
┌─────────────────────────────────┐
│ 샘플 데이터 체험 중  [내 기록으로] │
└─────────────────────────────────┘

```

### 실패 경로


| 상황         | 처리                              |
| ---------- | ------------------------------- |
| 기록 7일 미만   | 진행도 "n/7" 표시 + 샘플 버튼 노출         |
| AI 실패·타임아웃 | 폴백 문장 + 재시도 버튼. 그래프는 유지         |
| 필수 항목 미입력  | 해당 항목 하이라이트 (기본값이 있어 거의 발생 안 함) |
| 네트워크 오류    | localStorage 임시 저장 + 재시도 버튼     |
| 같은 날 중복 기록 | "오늘 기록을 수정할까요?" 확인 후 덮어쓰기       |


---

## 9. 구현 순서


| 순서  | 작업                              | 담당      | 완료 기준                       |
| --- | ------------------------------- | ------- | --------------------------- |
| 1   | 배포 골격                           | 김종건     | 빈 화면이라도 프론트·백엔드 URL이 열림     |
| 2   | DB 스키마 + 마이그레이션                 | 김서연(FS) | 테이블 4개 생성                   |
| 3   | 시드 데이터 생성 + 검증                  | 김서연(AI) | 검증 6항목 통과                   |
| 4   | POST /api/session, /api/records | 김서진     | 기록 저장 성공                    |
| 5   | 홈 + 기록 입력 화면                    | 김서연(FS) | 저장까지 동작                     |
| 6   | habit_pattern() 모듈              | 김서연(AI) | 시드로 impacts 1위가 sleep_short |
| 7   | GET /api/patterns + 폴백          | 김서진     | LLM 실패해도 impacts 반환         |
| 8   | GET /api/demo                   | 김서진     | 버튼 1회로 28일치 적용              |
| 9   | 인사이트 화면                         | 김서연(FS) | 막대그래프 표시                    |
| 10  | whatif() 모듈                     | 김서연(AI) | direction이 improve로 나옴      |
| 11  | POST /api/whatif                | 김서진     | range 응답                    |
| 12  | 시나리오 비교 화면                      | 김서연(FS) | 2선 그래프 표시                   |
| 13  | UI 최종본 적용 + QA                  | 박진영     | 6개 화면 톤 통일                  |


3번(시드 데이터)이 6·8·9·12번의 확인 전제다. 가장 먼저 끝내야 한다.

---

## 10. 완료 기준

### 최소 통과 (이것만 되면 서비스로 성립)

```
[ ] 배포 URL로 접속된다
[ ] 로그인 없이 바로 기록 입력 화면에 들어간다
[ ] 기록을 저장하면 skin_score가 나온다
[ ] 샘플 버튼 1회로 28일치가 적용된다
[ ] 샘플 모드에서 인사이트 화면에 영향도 막대 3개가 뜬다
[ ] AI 응답이 실패해도 빈 화면이 아니라 폴백 문장이 뜬다

```

### 완전 통과

```
[ ] 위 전부 + 시나리오 비교 그래프가 뜬다
[ ] 기록 7일 미만일 때 진행도가 표시된다
[ ] 실험 결과 화면이 샘플 모드에서 보인다
[ ] 모바일 세로 화면에서 레이아웃이 깨지지 않는다
[ ] 다른 브라우저에서 접속해도 정상 동작한다

```

---

## 11. 구현하지 않는 것

혼동을 막기 위해 명시한다.


| 항목              | 사유                       |
| --------------- | ------------------------ |
| 로그인·회원가입        | 익명 토큰으로 대체               |
| 사진 업로드·S3       | 분석에 쓰지 않는데 구현 비용이 크다. P2 |
| 사진 기반 AI 자동 점수화 | 학습 데이터가 없고 정확도 확보 불가     |
| 제품 추천           | 서비스 방향과 다르다              |
| 커뮤니티·공유 기능      | P2                       |
| 푸시 알림           | 웹 기반이라 제외                |
| 다국어             | 한국어만                     |
| 생리주기 입력         | 민감 건강정보. 별도 동의 절차 필요     |


---

## 12. 표현 규칙

코드와 UI 문구 전반에 적용한다.


| 규칙             | 예시                                         |
| -------------- | ------------------------------------------ |
| "원인"이라고 쓰지 않는다 | "연관 요인", "영향 가능성이 높은 요인"                   |
| 진단명·질병명·치료법 금지 | "여드름 치료" 같은 표현 사용 불가                       |
| 점 추정치를 쓰지 않는다  | "63점" ✕ → "60~66" ○                        |
| 예측이 아니라 시나리오   | "4주 뒤 이렇게 됩니다" ✕ → "유사한 패턴을 보입니다" ○        |
| 화면 하단 고지       | "본 분석은 통계적 연관성을 보여주는 참고 자료이며 의학적 진단이 아닙니다" |


