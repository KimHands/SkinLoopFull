"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { api } from "@/lib/api-client";
import type { PatternResponse } from "@/types/api";

const CACHE = "skinloop:last-pattern";
const confidence = { low: "낮음", medium: "보통", high: "높음" };
export default function InsightScreen() {
  const [data, setData] = useState<PatternResponse | null>(null);
  const [scoreByDate, setScoreByDate] = useState<Record<string, number>>({});
  const [error, setError] = useState("");
  useEffect(() => {
    const cached = sessionStorage.getItem(CACHE);
    if (cached) {
      setData(JSON.parse(cached));
    } else {
      api
        .getPatterns()
        .then(setData)
        .catch(() => setError("인사이트를 불러오지 못했어요."));
    }
    // 근거 날짜의 실제 피부 점수를 붙이기 위해 기록을 함께 불러온다.
    api
      .getRecords()
      .then((rows) => {
        const map: Record<string, number> = {};
        for (const row of rows) map[row.recordedAt] = row.skinScore;
        setScoreByDate(map);
      })
      .catch(() => {});
  }, []);
  if (error)
    return (
      <div className="page">
        <div className="card stack">
          <p role="alert">{error}</p>
          <Link className="btn btn-outline" href="/analyzing">
            다시 분석하기
          </Link>
        </div>
      </div>
    );
  if (!data)
    return <div className="page loading-copy">인사이트를 불러오고 있어요…</div>;
  if (data.reason === "NOT_ENOUGH_RECORDS")
    return (
      <div className="page stack">
        <div className="card">
          <h1 className="page-title">아직 패턴을 찾기엔 기록이 적어요</h1>
          <p className="subtle">{data.message}</p>
        </div>
        <Link className="btn btn-primary" href="/record">
          오늘 기록하기
        </Link>
        <Link className="btn btn-outline" href="/">
          28일치 샘플로 먼저 둘러보기
        </Link>
      </div>
    );
  const impacts = data.impacts.slice(0, 3);
  return (
    <div className="page insight-page stack">
      <header className="insight-header">
        <h1>
          오늘의 피부
          <br />
          인사이트
        </h1>
        <div>
          <b>{confidence[data.confidence ?? "low"]}</b>
          <span>최근 {data.recordDays}일 기록 기준</span>
        </div>
      </header>
      {data.isFallback && (
        <div className="fallback-note">
          AI 응답이 지연되어 기록 기반 기본 분석을 표시했어요.
        </div>
      )}
      <section className="card">
        <div className="section-heading">
          <strong>연관 가능성이 높은 요인</strong>
          <span>상위 3개</span>
        </div>
        <div className="impact-list">
          {impacts.map((item) => (
            <div key={item.factor}>
              <div>
                <strong>{item.label}</strong>
                <span>
                  연관{" "}
                  {item.impact > 0.35
                    ? "강함"
                    : item.impact > 0.2
                      ? "보통"
                      : "약함"}
                </span>
              </div>
              <i>
                <b style={{ width: `${Math.min(item.impact * 100, 100)}%` }} />
              </i>
            </div>
          ))}
        </div>
      </section>
      <section className="card">
        <h2 className="section-title">인사이트</h2>
        <p className="insight-copy">{data.insight}</p>
      </section>
      {data.evidenceDates.length > 0 && (
        <section className="card">
          <h2 className="section-title">왜 이렇게 분석됐나요?</h2>
          <div className="evidence-list">
            {data.evidenceDates.slice(0, 3).map((date, index) => {
              const score = scoreByDate[date];
              return (
                <div key={date}>
                  <strong>{date}</strong>
                  <span>
                    {impacts[index % Math.max(impacts.length, 1)]?.label ??
                      "생활 기록"}
                  </span>
                  {score != null && (
                    <b>
                      {Math.max(0, score - 3)}~{Math.min(100, score + 3)}
                    </b>
                  )}
                </div>
              );
            })}
          </div>
          <p className="caption">
            점수가 낮았던 날의 생활 기록을 함께 비교했어요.
          </p>
        </section>
      )}
      <Link className="btn btn-primary btn-block" href="/whatif">
        시나리오 비교하기
      </Link>
      <div className="disclaimer">
        본 분석은 통계적 연관성을 보여주는 참고 자료이며 의학적 진단이 아닙니다.
      </div>
    </div>
  );
}
