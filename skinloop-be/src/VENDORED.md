# vendored: skinloop-ai/src

이 디렉터리는 AI 레포(github.com/KimHands/SkinLoopAI)의 `src/`를 **복사(vendoring)**한 것이다.
BE가 `from src.habit_pattern import analyze_patterns` / `from src.whatif import run_whatif`로
in-process 호출한다(BE↔AI in-process 결정: docs/plan/open-questions.md A1).

- 정본은 AI 레포. 계산 로직 수정은 AI 레포에서 하고 여기로 다시 복사한다.
- 계약: skinloop-ai/docs/integration_contract.md
- 의존성: numpy/pandas/scipy/scikit-learn (requirements.txt)
