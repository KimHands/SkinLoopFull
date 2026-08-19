"""Pydantic 스키마 (spec §4 / docs/spec/03-types).

두 계열이 공존한다:
1) session/records/demo (내 DB 기반) — CamelModel 상속. 경계 camelCase / 내부 snake_case.
2) patterns/whatif (AI in-process) — records는 세션 DB에서 조회한다(명세 04-api).
   patterns는 입력 없는 GET, whatif 입력은 WhatIfRequest({targetHabit, changeValue}).
"""
from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


# =========================================================================
# session / records / demo — DB 기반 (경계 camelCase)
# =========================================================================
class SessionCreate(CamelModel):
    anon_token: Optional[str] = None


class SessionResponse(CamelModel):
    session_id: str
    is_demo: bool
    total_records: int
    created_at: datetime


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


class DemoResponse(CamelModel):
    loaded: bool
    is_demo: bool
    record_days: int
    period: dict
    message: str


class DemoClearedResponse(CamelModel):
    cleared: bool


# =========================================================================
# patterns / whatif — AI in-process
# 명세(04-api): patterns는 GET, whatif 입력은 {targetHabit, changeValue}.
# records는 body가 아니라 세션 DB에서 조회한다(analysis.frame.session_ai_records).
# =========================================================================
TargetHabit = Literal["sleep_short", "late_snack", "stress", "exercise"]


class WhatIfRequest(CamelModel):
    target_habit: TargetHabit
    change_value: float


class ErrorResponse(BaseModel):
    error: str
    detail: str
