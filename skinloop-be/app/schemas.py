"""Pydantic 스키마 (spec §4 / docs/spec/03-types).

직렬화 규칙(A2 확정): BE 내부는 snake_case, API 경계(요청/응답)는 camelCase.
- CamelModel을 상속하면 alias_generator로 camelCase alias가 붙는다.
- populate_by_name=True → 요청은 camelCase(alias)/snake_case 둘 다 허용.
- FastAPI 응답은 기본 by_alias=True → camelCase로 나간다.
"""
from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

HabitFactor = Literal["sleep_short", "late_snack", "stress", "exercise", "cosmetic_changed"]


class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


# ---- session ----
class SessionCreate(CamelModel):
    anon_token: Optional[str] = None


class SessionResponse(CamelModel):
    session_id: str
    is_demo: bool
    total_records: int
    created_at: datetime


# ---- records ----
class RecordCreate(CamelModel):
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


class RecordResponse(CamelModel):
    record_id: str
    skin_score: int
    total_records: int
    pattern_ready: bool
    created_at: datetime


class RecordItem(CamelModel):
    record_id: str
    recorded_at: date
    sleep_hours: float
    late_snack: bool
    stress_level: int
    exercise_min: int
    cosmetic_changed: bool
    skin_redness: int
    skin_acne_count: int
    skin_oiliness: int
    skin_score: int
    memo: Optional[str] = None


# ---- patterns ----
class Impact(CamelModel):
    factor: HabitFactor
    label: str
    impact: float
    lag: int
    corr: float


class SuggestedExperiment(CamelModel):
    target_habit: HabitFactor
    title: str
    duration_days: int


class PatternResponse(CamelModel):
    confidence: Optional[str] = None
    record_days: int
    impacts: list[Impact] = []
    insight: Optional[str] = None
    evidence_dates: list[str] = []
    suggested_experiment: Optional[SuggestedExperiment] = None
    is_fallback: bool = False
    model_version: Optional[str] = None
    reason: Optional[str] = None
    need_more: Optional[int] = None
    message: Optional[str] = None


# ---- whatif ----
class WhatIfRequest(CamelModel):
    target_habit: HabitFactor
    change_value: float


class WhatIfBand(CamelModel):
    label: str
    range: dict
    trend: list[float]


class WhatIfResponse(CamelModel):
    target_habit: HabitFactor
    label: str
    current: WhatIfBand
    changed: WhatIfBand
    direction: Literal["improve", "worsen", "unclear"]
    confidence: str
    message: str
    disclaimer: str


# ---- demo ----
class DemoResponse(CamelModel):
    loaded: bool
    is_demo: bool
    record_days: int
    period: dict
    message: str


class DemoClearedResponse(CamelModel):
    cleared: bool
