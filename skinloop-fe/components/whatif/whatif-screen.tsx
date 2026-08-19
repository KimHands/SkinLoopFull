"use client";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { api, ApiError } from "@/lib/api-client";
import type { HabitFactor, WhatIfResponse } from "@/types/api";
import { TrendChart } from "./trend-chart";

const options: Array<{ factor: HabitFactor; label: string; value: number }> = [
  { factor: "sleep_short", label: "수면 +1시간", value: 1 },
  { factor: "late_snack", label: "야식 줄이기", value: 2 },
  { factor: "stress", label: "스트레스 낮추기", value: 1 },
  { factor: "exercise", label: "운동 늘리기", value: 20 },
];
export default function WhatIfScreen() {
  const [selected, setSelected] = useState(options[0]);
  const [result, setResult] = useState<WhatIfResponse | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const compare = useCallback(async () => {
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
          : "시나리오를 비교하지 못했어요.",
      );
    } finally {
      setBusy(false);
    }
  }, [selected]);
  useEffect(() => {
    void compare();
  }, [compare]);
  return (
    <div className="page whatif-page stack">
      <header>
        <h1 className="page-title">시나리오 비교</h1>
        <p className="subtle">어떤 습관을 바꿔볼까요?</p>
      </header>
      <div className="habit-pills">
        {options.map((option) => (
          <button
            type="button"
            key={option.factor}
            className={selected.factor === option.factor ? "selected" : ""}
            onClick={() => {
              setSelected(option);
              setResult(null);
            }}
          >
            {option.label}
          </button>
        ))}
      </div>
      {!result && (
        <button
          className="btn btn-primary btn-block"
          disabled={busy}
          onClick={() => void compare()}
        >
          {busy ? "비교하고 있어요…" : "4주 흐름 비교하기"}
        </button>
      )}
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
      {result && (
        <>
          <section className="card chart-card">
            <div className="section-heading">
              <strong>4주 예상 흐름</strong>
              <span>주간 평균</span>
            </div>
            <TrendChart data={result} />
            <div className="chart-legend">
              <span>현재 유지</span>
              <span>변경</span>
            </div>
            <div className="range-grid">
              <div>
                <span>현재 유지</span>
                <strong>
                  {result.current.range.min}~{result.current.range.max}
                </strong>
              </div>
              <div>
                <span>변경</span>
                <strong>
                  {result.changed.range.min}~{result.changed.range.max}
                </strong>
              </div>
            </div>
            <p>{result.message}</p>
          </section>
          <Link className="btn btn-primary btn-block" href="/records">
            이 실험 시작하기
          </Link>
          <p className="experiment-hint">14일 동안 이 습관을 기록해봐요</p>
          <div className="disclaimer">
            본 분석은 통계적 연관성을 보여주는 참고 자료이며 의학적 진단이
            아닙니다.
          </div>
        </>
      )}
    </div>
  );
}
