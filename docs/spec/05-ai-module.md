# 05. AI 분석 모듈

> 원본: `spec.md` §6 — habit_pattern·whatif·fallback 전체 코드의 정본은 spec.md.
> 이 모듈의 구현 위치는 **AI Repo**. FullStack BE는 계약(입력 DataFrame → 출력 dict)만 맞춘다.

## 설계 원칙

영향도 **계산은 통계 모델**이, **문장화만 LLM**이 한다. LLM에 계산을 맡기면 없는 수치를 만들고 근거를 설명 못 한다.

```
[기록 N일]
   ▼
[HabitPattern] Spearman(lag 0~3) → GBM → permutation importance
   │ impacts[] (숫자)
   ├──────────────┬──────────────┐
   ▼              ▼              ▼
[WhatIf]      [실험 검증]     [LLM 문장화]
회귀 예측      전후 비교        GPT-4o
   └──────────────┴──────────────┘
              ▼
        [폴백] 규칙 기반 문장
```

## HabitPattern (`ai/habit_pattern.py`)

- 입력: `recorded_at` 오름차순 DataFrame(HABITS + skin_score).
- n<7이면 `NOT_ENOUGH_RECORDS` 반환.
- (a) lag 0~3일 **Spearman 교차상관**: 습관(t) → 피부(t+lag). 절댓값 최대인 lag·corr 선택.
- (b) **GBM + permutation importance**(n_repeats=30)로 영향도 산출.
- 상위 3개만 반환. evidence_dates = skin_score 하위 3일.
- **lag를 두는 이유**: 피부가 습관 다음 날 반응 → lag 0만 보면 놓친다.
- **permutation importance 이유**: 수면·스트레스가 상관돼 있어 단순 상관으론 구분 안 됨.
- 출력 factor 키는 `FACTOR_MAP`으로 DB 컬럼명 → HabitFactor 변환.

## WhatIf (`ai/whatif.py`)

- RandomForest(n_estimators=200) 학습 → 최근 7일 평균을 기준점으로 예측.
- `DELTA[target]`로 해당 컬럼만 변화시켜 재예측.
- **불확실성**: 개별 트리 예측의 표준편차로 range 근사.
- direction: diff>2 improve / diff<-2 worsen / 그 외 unclear.
- ⚠️ `late_snack`(bool 평균)에 "주당 횟수" 단위를 빼는 처리가 애매 ([open-questions](../plan/open-questions.md)).

## LLM 문장화

- System 프롬프트 규칙: impacts 1~2위만 언급, 새 수치 금지, "원인" 금지("연관 요인"), 진단·질병·치료 금지, 2문장 이내, 14일 실험 제안, **JSON만 출력**.
- 출력: `{ insight, experiment:{targetHabit,title,durationDays} }`.

## 폴백 (`ai/fallback.py`)

- GPT 호출을 try/except + 5초 타임아웃으로 감싸고, 실패 시 규칙 기반 문장(`FALLBACK_INSIGHT`) + 실험(`FALLBACK_EXPERIMENT`) 사용.
- **impacts는 그대로 유지** — 프론트는 그래프를 그리고 문장만 대체.

## BE ↔ AI Repo 계약 (정의 필요)

FullStack BE가 AI 모듈을 어떻게 호출할지 확정해야 함 ([open-questions](../plan/open-questions.md)):
- (A) AI Repo를 pip 패키지/서브모듈로 가져와 in-process 호출, 또는
- (B) AI Repo를 별도 HTTP 서비스로 띄우고 BE가 호출.
- 어느 쪽이든 **입력(records DataFrame 상당) / 출력(PatternResponse dict)** 스키마는 04-api·03-types와 일치해야 한다.
