from app.skin_score import calc_skin_score


def test_best_skin_scores_100():
    assert calc_skin_score(1, 1, 1) == 100


def test_mid_skin_scores_60():
    assert calc_skin_score(3, 3, 3) == 60


def test_worst_skin_scores_20():
    assert calc_skin_score(5, 5, 5) == 20


def test_spec_example_4_3_4_rounds_to_47():
    # spec §5 응답 예시는 54지만 정본 계산식으로는 47 (open-questions Q2)
    assert calc_skin_score(4, 3, 4) == 47
