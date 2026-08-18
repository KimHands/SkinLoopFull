export type HabitFactor =
  | "sleep_short"
  | "late_snack"
  | "stress"
  | "exercise"
  | "cosmetic_changed";

export type Confidence = "low" | "medium" | "high";

export interface SessionResponse {
  sessionId: string;
  isDemo: boolean;
  totalRecords: number;
  createdAt: string;
}

export interface RecordCreateRequest {
  recordedAt: string;
  sleepHours: number;
  lateSnack: boolean;
  stressLevel: number;
  exerciseMin: number;
  cosmeticChanged: boolean;
  skinRedness: number;
  skinAcneCount: number;
  skinOiliness: number;
  memo?: string;
}

export interface RecordResponse {
  recordId: string;
  skinScore: number;
  totalRecords: number;
  patternReady: boolean;
  createdAt: string;
}

export interface RecordItem extends Omit<RecordCreateRequest, "memo"> {
  recordId: string;
  skinScore: number;
  memo?: string | null;
}

export interface Impact {
  factor: HabitFactor;
  label: string;
  impact: number;
  lag: number;
  corr: number;
}

export interface SuggestedExperiment {
  targetHabit: HabitFactor;
  title: string;
  durationDays: number;
}

export interface PatternResponse {
  confidence: Confidence | null;
  recordDays: number;
  impacts: Impact[];
  insight: string | null;
  evidenceDates: string[];
  suggestedExperiment: SuggestedExperiment | null;
  isFallback: boolean;
  modelVersion: string | null;
  reason: "NOT_ENOUGH_RECORDS" | null;
  needMore: number | null;
  message: string | null;
}

export interface WhatIfRequest {
  targetHabit: HabitFactor;
  changeValue: number;
}

export interface WhatIfBand {
  label: string;
  range: { min: number; max: number };
  trend: number[];
}

export interface WhatIfResponse {
  targetHabit: HabitFactor;
  label: string;
  current: WhatIfBand;
  changed: WhatIfBand;
  direction: "improve" | "worsen" | "unclear";
  confidence: Confidence;
  message: string;
  disclaimer: string;
}

export interface DemoResponse {
  loaded: boolean;
  isDemo: boolean;
  recordDays: number;
  period: { from: string; to: string };
  message: string;
}

export interface ApiErrorBody {
  error?: string;
  message?: string;
  detail?: string;
  recordId?: string;
}
