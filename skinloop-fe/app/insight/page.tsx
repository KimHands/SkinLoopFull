"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api } from "@/lib/api-client";
import type { PatternResponse } from "@/types/api";

const CACHE_KEY = "skinloop:last-pattern";

export default function InsightPage() {
  const [data, setData] = useState<PatternResponse | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    const cached = sessionStorage.getItem(CACHE_KEY);
    if (cached) { setData(JSON.parse(cached)); return; }
    api.getPatterns().then(setData).catch(() => setError("인사이트를 불러오지 못했습니다."));
  }, []);
  if (error) return <div className="page"><div className="card"><p role="alert">{error}</p><Link className="btn btn-outline" href="/analyzing">다시 분석하기</Link></div></div>;
  if (!data) return <div className="page"><p aria-live="polite">인사이트를 불러오고 있어요.</p></div>;
  if (data.reason === "NOT_ENOUGH_RECORDS") return <div className="page stack"><div className="card"><h1 className="page-title">아직 패턴을 찾기엔 기록이 적어요</h1><p className="subtle">{data.message}</p></div><Link className="btn btn-primary" href="/record">오늘 기록하기</Link><Link className="btn btn-outline" href="/">28일치 샘플로 먼저 둘러보기</Link></div>;
  return <div className="page stack">
    <header className="page-header"><div><h1 className="page-title">오늘의 피부 인사이트</h1><p className="caption">최근 {data.recordDays}일 기록 · 신뢰도 {data.confidence ?? "확인 중"}</p></div></header>
    {data.isFallback && <div className="card" style={{ background: "var(--pale)" }}>분석 연결이 지연되어 기본 안내를 표시했어요. 다시 분석할 수 있어요.</div>}
    <div className="grid-2"><section className="card"><h2 style={{ marginTop: 0, fontSize: 18 }}>함께 나타난 요인</h2><div className="stack">{data.impacts.length ? data.impacts.slice(0, 3).map((item, index) => <div key={item.factor}><div style={{ display: "flex", justifyContent: "space-between" }}><strong>{index + 1}. {item.label}</strong><span>{Math.round(item.impact * 100)}%</span></div><div style={{ height: 10, background: "var(--border)", borderRadius: 8, marginTop: 8 }}><div style={{ height: "100%", width: `${Math.min(item.impact * 100, 100)}%`, background: "var(--data)", borderRadius: 8 }} /></div></div>) : <p className="subtle">영향도 데이터는 준비 중이지만 안내 문장은 확인할 수 있어요.</p>}</div></section>
      <section className="card"><h2 style={{ marginTop: 0, fontSize: 18 }}>인사이트</h2><p style={{ lineHeight: 1.7 }}>{data.insight}</p>{data.evidenceDates.length > 0 && <><p className="caption">근거가 된 날짜</p><p>{data.evidenceDates.slice(0, 3).join(" · ")}</p></>}</section></div>
    <Link className="btn btn-primary btn-block" href="/whatif">시나리오 비교하기</Link><div className="disclaimer">본 분석은 통계적 연관성을 보여주는 참고 자료이며 의학적 진단이 아닙니다.</div>
  </div>;
}
