"""
계산 결과(dict) -> 사람이 읽는 한국어 문장.

주의:
- estimatedDifference는 실제 피부 점수 변화의 "보장이나 의학적 예측이 아님"
- trend는 각 주를 독립 예측한 값이 아니라 두 시나리오 차이를 비교한 값
문장화할 때 이 두 가지를 과장하지 않도록 프롬프트에 명시해 둔다.
"""

import os
import json
from openai import OpenAI

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")
        _client = OpenAI(api_key=api_key)
    return _client


_SYSTEM_PROMPT = (
    "당신은 피부 관리 기록 앱의 결과를 사용자에게 설명하는 어시스턴트입니다. "
    "주어진 JSON 분석 결과만 근거로 2~3문장의 한국어 요약을 작성하세요. "
    "의학적 진단이나 인과관계 단정 표현('원인입니다', '~때문입니다')은 쓰지 말고, "
    "'연관이 있어 보입니다', '경향이 나타났습니다' 같은 참고 정보 톤을 유지하세요. "
    "JSON에 없는 수치나 사실을 만들어내지 마세요."
)


def _chat(user_content: str) -> str:
    client = _get_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        temperature=0.4,
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()


def summarize_habit_pattern(result: dict) -> str:
    """analyze_patterns() 결과를 문장으로. 실패 시 규칙 기반 폴백을 반환한다."""
    try:
        return _chat(
            "다음은 생활습관과 피부 점수의 연관 분석 결과입니다:\n"
            f"{json.dumps(result, ensure_ascii=False)}\n"
            "가장 영향이 큰 요인 중심으로 요약해 주세요."
        )
    except Exception:
        return _rule_based_habit_pattern(result)


def summarize_whatif(result: dict) -> str:
    """run_whatif() 결과를 문장으로. 실패 시 규칙 기반 폴백을 반환한다."""
    try:
        return _chat(
            "다음은 습관 변경 시나리오(What-if) 비교 결과입니다:\n"
            f"{json.dumps(result, ensure_ascii=False)}\n"
            "estimatedDifference는 예측 보장이 아니라 비교 참고값이라는 점을 "
            "자연스럽게 반영해서 요약해 주세요."
        )
    except Exception:
        return _rule_based_whatif(result)


def _rule_based_habit_pattern(result: dict) -> str:
    impacts = result.get("impacts") or []
    if not impacts:
        return "아직 뚜렷한 연관 패턴을 찾지 못했습니다. 기록을 더 쌓아보세요."
    top = impacts[0]
    factor = top.get("factor", "일부 습관")
    return f"최근 기록에서 {factor}이(가) 피부 상태와 연관이 있는 것으로 나타났습니다."


def _rule_based_whatif(result: dict) -> str:
    label = result.get("label", "선택하신 습관")
    diff = result.get("estimatedDifference")
    if diff is None:
        return f"{label} 변경 시나리오의 비교 결과를 계산했습니다."
    direction = "개선" if diff > 0 else "변화"
    return f"{label}을(를) 바꿨을 때 피부 점수가 참고상 약 {abs(diff):.1f}점 {direction}될 것으로 비교됩니다."