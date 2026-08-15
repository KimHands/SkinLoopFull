# 06. 시드 데이터

> 원본: `spec.md` §7 — seed_generator.py 전체 코드의 정본은 spec.md.
> 생성 스크립트의 구현 위치는 **AI Repo**(또는 공용 scripts). 적재는 BE `/api/demo`가 담당.

## 왜 필요한가

기록이 없으면 기능 ②③을 확인할 수 없다. **28일치 시드**를 버튼 한 번으로 적용한다.

## 구간 설계

| 구간 | 일수 | 습관 | skin_score |
| --- | --- | --- | --- |
| 양호 | Day 1~10 | 수면 7~8h, 야식 없음, 스트레스 1~2 | 72~78 |
| 악화 | Day 11~20 | 수면 4.5~5.5h(6일), 야식 6일, 스트레스 4~5 | 52~60 |
| 회복 | Day 21~28 | 수면 6.5~7.5h, 야식 1회, 스트레스 2~3 | 66~72 |

- 수면 부족을 **1위**(impact 0.4대), 야식을 **2위**(0.3대), 스트레스를 **3위**(0.1대)로 심는다.
- 운동·화장품에는 **일부러 상관을 심지 않는다** → 모델이 없는 패턴을 만들지 않는지 확인하는 대조군.
- `random.seed(42)` 고정 — 매번 같은 데이터.

## 함께 넣는 완료 실험 1건

experiments 테이블에 `sleep_short` / "취침 시간 40분 앞당기기" / 14일 / status=done / 56.4→68.2 / improved.

## 검증 (6항목, 하나라도 실패 시 상관 강도 조정 후 재생성)

```
[ ] impacts 1위가 sleep_short
[ ] 2위가 late_snack
[ ] exercise·cosmetic_changed impact < 0.1
[ ] confidence == high (28일)
[ ] whatif("sleep_short", 1.0) direction == improve
[ ] Day 21~28 평균이 Day 11~20 평균보다 8점 이상 높음
```

## 적재 (BE)

- `GET /api/demo`: `sessions.is_demo=true`, records 28건 INSERT(recorded_at 오늘 기준 역산), experiments 1건 INSERT.
- `DELETE /api/demo`: 해당 세션 records·experiments 삭제, `is_demo=false`.
- 별도 테이블 없이 같은 구조로 INSERT.

## 순서 의존성

시드는 06→ **기능 ②③의 확인 전제**(work-plan 3번). 스키마(02) 다음으로 가장 먼저 끝내야 한다.
