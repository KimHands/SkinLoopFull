from datetime import date

from app.seed import generate_seed_records
from app.skin_score import calc_skin_score

TODAY = date(2026, 8, 13)


def test_generates_28_records():
    rows = generate_seed_records(TODAY)
    assert len(rows) == 28


def test_is_deterministic_seed_42():
    assert generate_seed_records(TODAY) == generate_seed_records(TODAY)


def test_recorded_at_spans_28_days_back_from_today():
    rows = generate_seed_records(TODAY)
    assert rows[0]["recorded_at"] == date(2026, 7, 17)
    assert rows[-1]["recorded_at"] == TODAY


def test_skin_score_matches_formula():
    for r in generate_seed_records(TODAY):
        assert r["skin_score"] == calc_skin_score(
            r["skin_redness"], r["skin_acne_count"], r["skin_oiliness"]
        )


def test_recovery_avg_at_least_8_higher_than_worsening():
    rows = generate_seed_records(TODAY)
    worsening = [r["skin_score"] for r in rows[10:20]]
    recovery = [r["skin_score"] for r in rows[20:28]]
    assert sum(recovery) / len(recovery) - sum(worsening) / len(worsening) >= 8
