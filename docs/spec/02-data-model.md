# 02. 데이터 모델

> 원본: `spec.md` §3 — 컬럼 타입/제약의 정본은 spec.md.

## 관계

```
sessions ──1:N──▶ records ──▶ analyses
    │
    └──1:N──▶ experiments
```

- `users` 테이블은 만들지 않는다 (익명 토큰 식별).

## 테이블 요약

### sessions
익명 세션. `anon_token`(UUID, UNIQUE)으로 식별. `is_demo`로 샘플 모드 구분.

### records
일일 기록. **하루 1건** — `UNIQUE(session_id, recorded_at)`.
- 생활습관: `sleep_hours`(0~14), `late_snack`(bool), `stress_level`(1~5), `exercise_min`, `cosmetic_changed`(bool)
- 피부: `skin_redness`·`skin_acne_count`·`skin_oiliness`(각 1~5)
- 파생: `skin_score`(20~100, 애플리케이션에서 계산해 저장)
- ⚠️ `exercise_min` 범위: DB/Pydantic은 0~300, 화면은 0~120 — 불일치 ([open-questions](../plan/open-questions.md))

### analyses
분석 결과 캐시. `impacts`(JSONB), `insight`(LLM 문장), `confidence`, `evidence_dates`(JSONB), `record_days`, `is_fallback`, `model_version`.

### experiments
습관 변경 실험. `target_habit`, `status`(proposed/running/done), `baseline_score`, `result_score`, `verdict`(improved/no_change/needs_more).

## 인덱스

```sql
CREATE UNIQUE INDEX idx_sessions_token       ON sessions(anon_token);
CREATE UNIQUE INDEX idx_records_session_date ON records(session_id, recorded_at);
CREATE INDEX        idx_records_session      ON records(session_id, recorded_at DESC);
CREATE INDEX        idx_analyses_session     ON analyses(session_id, created_at DESC);
```

## skin_score 계산

```python
def calc_skin_score(redness: int, acne: int, oiliness: int) -> int:
    return round(100 - ((redness + acne + oiliness - 3) / 12 * 80))
```

- (1,1,1) → 100, (3,3,3) → 60, (5,5,5) → 20. **애플리케이션 레이어에서 계산해 저장.**
  (전부 1점(최상)일 때 100, 전부 5점(최악)일 때 20이 되도록 정규화한 식.)
- ⚠️ spec §5의 records 응답 예시(입력 4/3/4 → skinScore 54)는 이 식과도 불일치(계산상 47). 예시 오타로 추정 ([open-questions](../plan/open-questions.md)).

## 마이그레이션 규칙

web.md에 따라 **스키마 생성·변경은 사람이** 한다. BE 코드(`app/models.py`)는 모델 정의만 두고,
실제 `CREATE TABLE`/마이그레이션 실행은 담당자(김서연 FS)가 수동 수행 후 팀에 공유한다.
