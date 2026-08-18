"""Pydantic 스키마 (spec §4 / docs/spec/03-types).

두 계열이 공존한다:
1) session/records/demo (내 DB 기반) — CamelModel 상속. 경계 camelCase / 내부 snake_case.
2) patterns/whatif (AI in-process) — 프론트가 records를 body로 직접 보내는 형태.
   HabitRecord/RecordsPayload/WhatIfRequest. (AI Repo 연동, PR #4)

주석: RecordsPayload는 DB(records)가 완성되면 session 조회 방식으로 바뀔 수 있다(향후 통합).
"""
from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator
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
# patterns / whatif — AI in-process (프론트가 records를 body로 전송, PR #4)
# =========================================================================
class HabitRecord(BaseModel):
    """일일 기록 하나. DB(records 테이블)가 완성되면 그쪽 필드와 맞춘다."""

    recorded_at: date = Field(..., alias="recordedAt")
    sleep_hours: float = Field(..., ge=0, le=14, alias="sleepHours")
    late_snack: bool = Field(..., alias="lateSnack")
    stress_level: int = Field(..., ge=1, le=5, alias="stressLevel")
    exercise_min: int = Field(..., ge=0, le=300, alias="exerciseMin")
    cosmetic_changed: bool = Field(..., alias="cosmeticChanged")
    skin_score: float = Field(..., ge=20, le=100, alias="skinScore")

    model_config = {"populate_by_name": True}

    def to_ai_dict(self) -> dict:
        return {
            "recorded_at": self.recorded_at.isoformat(),
            "sleep_hours": self.sleep_hours,
            "late_snack": self.late_snack,
            "stress_level": self.stress_level,
            "exercise_min": self.exercise_min,
            "cosmetic_changed": self.cosmetic_changed,
            "skin_score": self.skin_score,
        }


class RecordsPayload(BaseModel):
    """지금은 프론트가 기록을 직접 보내는 형태.
    DB(records 테이블)가 완성되면, session으로 DB 조회하는 방식으로 바뀔 수 있다."""

    records: list[HabitRecord]

    @field_validator("records")
    @classmethod
    def no_duplicate_dates(cls, v: list[HabitRecord]) -> list[HabitRecord]:
        dates = [r.recorded_at for r in v]
        if len(dates) != len(set(dates)):
            raise ValueError("recordedAt에 중복된 날짜가 있습니다.")
        return v

    def sorted_ai_records(self) -> list[dict]:
        ordered = sorted(self.records, key=lambda r: r.recorded_at)
        return [r.to_ai_dict() for r in ordered]


TargetHabit = Literal["sleep_short", "late_snack", "stress", "exercise"]


class WhatIfRequest(RecordsPayload):
    target_habit: TargetHabit = Field(..., alias="targetHabit")
    change_value: float = Field(..., alias="changeValue")

    model_config = {"populate_by_name": True}


class ErrorResponse(BaseModel):
    error: str
    detail: str
