# Pydantic 스키마. 기능 구현 단계에서 spec.md 5절 기준으로 채운다.
# (RecordCreate, Impact, PatternResponse, WhatIf 등)

from datetime import date
from typing import Literal
from pydantic import BaseModel, Field, field_validator


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
