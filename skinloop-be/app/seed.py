"""28일치 시드 데이터 생성 (spec §7 / docs/spec/06-seed).

구간: 양호(1~10) / 악화(11~20) / 회복(21~28).
수면부족 1위·야식 2위·스트레스 3위로 상관을 심고, 운동·화장품은 대조군(무상관).
random.seed(42) 고정 — 매번 같은 데이터.
"""
import random
from datetime import date, timedelta

from app.skin_score import calc_skin_score

# 시드와 함께 넣는 완료된 실험 1건 (spec §7)
DEMO_EXPERIMENT = {
    "target_habit": "sleep_short",
    "title": "취침 시간 40분 앞당기기",
    "duration_days": 14,
    "status": "done",
    "baseline_score": 56.4,
    "result_score": 68.2,
    "verdict": "improved",
}


def _make_day(i: int, today: date, rng: random.Random) -> dict:
    d = today - timedelta(days=27 - i)

    if i < 10:  # 양호
        sleep = round(rng.uniform(7.0, 8.0), 1)
        snack, stress = False, rng.randint(1, 2)
        ex, base = rng.choice([20, 30, 40]), rng.randint(1, 2)
    elif i < 20:  # 악화
        bad = rng.random() < 0.6
        sleep = round(rng.uniform(4.5, 5.5), 1) if bad else round(rng.uniform(6.5, 7.0), 1)
        snack = bad
        stress = rng.randint(4, 5) if bad else 3
        ex, base = 0, (rng.randint(4, 5) if bad else 3)
    else:  # 회복
        sleep = round(rng.uniform(6.5, 7.5), 1)
        snack = rng.random() < 0.15
        stress = rng.randint(2, 3)
        ex, base = rng.choice([20, 30]), rng.randint(2, 3)

    r = min(5, max(1, base + rng.choice([-1, 0, 0, 1])))
    a = min(5, max(1, base + rng.choice([-1, 0, 0])))
    o = min(5, max(1, base + rng.choice([0, 0, 1])))

    return {
        "recorded_at": d,
        "sleep_hours": sleep,
        "late_snack": snack,
        "stress_level": stress,
        "exercise_min": ex,
        "cosmetic_changed": rng.random() < 0.1,
        "skin_redness": r,
        "skin_acne_count": a,
        "skin_oiliness": o,
        "skin_score": calc_skin_score(r, a, o),
        "memo": None,
    }


def generate_seed_records(today: date) -> list[dict]:
    """recorded_at 오름차순 28건. today가 마지막 날."""
    rng = random.Random(42)
    return [_make_day(i, today, rng) for i in range(28)]
