"use client";

import Link from "next/link";
import { useState } from "react";
import { api, ApiError } from "@/lib/api-client";
import type { HabitFactor, WhatIfResponse } from "@/types/api";

const options: Array<{ factor: HabitFactor; label: string; value: number }> = [
  { factor: "sleep_short", label: "수면 +1시간", value: 1 },
  { factor: "late_snack", label: "야식 주 2회 줄이기", value: 2 },
  { factor: "stress", label: "스트레스 1단계 낮추기", value: 1 },
  { factor: "exercise", label: "운동 +20분", value: 20 },
];

function Trend({ data }: { data: WhatIfResponse }) {
  const values = [
    ...data.current.trend,
    ...data.changed.trend,
    data.current.range.min,
    data.current.range.max,
    data.changed.range.min,
    data.changed.range.max,
  ];
  const minimum = Math.floor(Math.min(...values) / 10) * 10 - 5;
  const maximum = Math.ceil(Math.max(...values) / 10) * 10 + 5;
  const y = (value: number) =>
    150 - ((value - minimum) / Math.max(maximum - minimum, 1)) * 120;
  const points = (trend: number[]) =>
    trend.map((value, index) => `${20 + index * 90},${y(value)}`).join(" ");
  const band = (range: { min: number; max: number }, fill: string) => (
    <rect
      x="20"
      width="270"
      y={y(range.max)}
      height={Math.max(y(range.min) - y(range.max), 2)}
      rx="6"
      fill={fill}
    />
  );
  return (
    <svg
      viewBox="0 0 310 180"
      role="img"
      aria-label="현재 유지와 습관 변경 시 4주 비교 그래프"
      style={{ width: "100%" }}
    >
      {[30, 70, 110, 150].map((y) => (
        <line key={y} x1="20" x2="290" y1={y} y2={y} stroke="#efe1dd" />
      ))}
      {band(data.current.range, "rgba(154,154,160,.12)")}
      {band(data.changed.range, "rgba(138,109,158,.14)")}
      <polyline
        points={points(data.current.trend)}
        fill="none"
        stroke="#9a9aa0"
        strokeWidth="4"
      />
      <polyline
        points={points(data.changed.trend)}
        fill="none"
        stroke="#8a6d9e"
        strokeWidth="4"
      />
      <text x="20" y="174" fontSize="11">
        1주
      </text>
      <text x="275" y="174" fontSize="11">
        4주
      </text>
    </svg>
  );
}

export default function WhatIfPage() {
  const [selected, setSelected] = useState(options[0]);
  const [result, setResult] = useState<WhatIfResponse | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  async function compare() {
    setBusy(true);
    setError("");
    try {
      setResult(
        await api.compareScenario({
          targetHabit: selected.factor,
          changeValue: selected.value,
        }),
      );
    } catch (caught) {
      setError(
        caught instanceof ApiError
          ? caught.message
          : "시나리오를 비교하지 못했습니다.",
      );
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="page stack">
      <header className="page-header">
        <div>
          <h1 className="page-title">시나리오 비교</h1>
          <p className="subtle">
            한 가지 습관을 바꿨을 때의 4주 경향을 범위로 비교해요.
          </p>
        </div>
      </header>
      <section className="card">
        <h2 style={{ marginTop: 0, fontSize: 18 }}>바꿔볼 습관 하나</h2>
        <div className="grid-2">
          {options.map((option) => (
            <button
              type="button"
              key={option.factor}
              className={`btn ${selected.factor === option.factor ? "btn-secondary" : "btn-outline"}`}
              onClick={() => {
                setSelected(option);
                setResult(null);
              }}
            >
              {option.label}
            </button>
          ))}
        </div>
        <button
          className="btn btn-primary btn-block"
          style={{ marginTop: 16 }}
          disabled={busy}
          onClick={() => void compare()}
        >
          {busy ? "비교하고 있어요…" : "4주 시나리오 비교하기"}
        </button>
        {error && (
          <div className="stack">
            <p className="error-text" role="alert">
              {error}
            </p>
            <button className="btn btn-outline" onClick={() => void compare()}>
              다시 시도하기
            </button>
          </div>
        )}
      </section>
      {result && (
        <>
          <section className="card">
            <div style={{ display: "flex", gap: 18, fontSize: 12 }}>
              <span>━ 현재 유지</span>
              <span style={{ color: "var(--data)" }}>━ 습관 변경</span>
            </div>
            <Trend data={result} />
            <div className="grid-2">
              <div className="card">
                <p className="caption">현재 유지</p>
                <strong>
                  {result.current.range.min}~{result.current.range.max}
                </strong>
              </div>
              <div className="card">
                <p className="caption">변경 시</p>
                <strong>
                  {result.changed.range.min}~{result.changed.range.max}
                </strong>
              </div>
            </div>
            <p style={{ lineHeight: 1.7 }}>{result.message}</p>
          </section>
          <Link className="btn btn-primary btn-block" href="/records">
            이 실험 살펴보기
          </Link>
          <div className="disclaimer">
            {result.disclaimer}
            <br />본 분석은 통계적 연관성을 보여주는 참고 자료이며 의학적 진단이
            아닙니다.
          </div>
        </>
      )}
    </div>
  );
}
