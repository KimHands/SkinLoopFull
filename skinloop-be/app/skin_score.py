"""skin_score 파생값 계산 (spec §3 / docs/spec/02-data-model).

애플리케이션 레이어에서 계산해 records.skin_score에 저장한다.
(1,1,1)→100, (3,3,3)→60, (5,5,5)→20 이 되도록 정규화한 식.
"""


def calc_skin_score(redness: int, acne: int, oiliness: int) -> int:
    return round(100 - ((redness + acne + oiliness - 3) / 12 * 80))
