"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, ApiError } from "@/lib/api-client";
import { useSessionStore } from "@/stores/session-store";
import type { RecordItem } from "@/types/api";

export default function RecordsPage() {
  const router = useRouter();
  const isDemo = useSessionStore((state) => state.isDemo);
  const setDemo = useSessionStore((state) => state.setDemoMode);
  const [records, setRecords] = useState<RecordItem[]>([]);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  useEffect(() => { api.getRecords().then(setRecords).catch((caught) => setError(caught instanceof ApiError ? caught.message : "기록을 불러오지 못했습니다.")); }, []);
  async function clearDemo() {
    if (!window.confirm("샘플 기록 28일과 샘플 실험 결과를 삭제할까요?")) return;
    setBusy(true);
    try { await api.clearDemo(); setDemo(false, 0); router.push("/"); }
    catch (caught) { setError(caught instanceof ApiError ? caught.message : "샘플을 종료하지 못했습니다."); setBusy(false); }
  }
  return <div className="page stack"><header className="page-header"><div><h1 className="page-title">내 기록</h1><p className="subtle">날짜별 생활 습관과 피부 점수 범위를 돌아봐요.</p></div><Link className="btn btn-secondary" href="/record">기록 추가</Link></header>
    {error && <p className="error-text" role="alert">{error}</p>}
    {isDemo && <section className="card"><p className="caption">완료된 샘플 실험</p><h2 style={{ marginTop: 0, fontSize: 18 }}>취침 시간을 조금 앞당겨 본 14일</h2><p className="subtle">실험 전 7일과 실험 중 14일의 경향을 비교했어요.</p><div className="grid-2"><div><span className="caption">실험 전</span><p><strong>52~58</strong></p></div><div><span className="caption">실험 중</span><p><strong>60~66</strong></p></div></div><p>평균적으로 더 높은 범위와 함께 나타나는 경향이 보였어요.</p></section>}
    <section className="card"><h2 style={{ marginTop: 0, fontSize: 18 }}>날짜별 기록</h2>{records.length === 0 && !error ? <p className="subtle">아직 기록이 없어요.</p> : <div className="stack">{[...records].reverse().map((record) => <article key={record.recordId} style={{ borderBottom: "1px solid var(--border)", paddingBottom: 14 }}><div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}><strong>{record.recordedAt}</strong><span>피부 점수 {Math.max(0, record.skinScore - 3)}~{Math.min(100, record.skinScore + 3)}</span></div><p className="caption">수면 {record.sleepHours}시간 · 스트레스 {record.stressLevel}/5 · 운동 {record.exerciseMin}분{record.lateSnack ? " · 야식" : ""}</p></article>)}</div>}</section>
    {isDemo && <button className="btn btn-outline btn-block" disabled={busy} onClick={() => void clearDemo()}>{busy ? "샘플을 정리하고 있어요…" : "샘플 체험 종료하기"}</button>}
    <div className="disclaimer">본 분석은 통계적 연관성을 보여주는 참고 자료이며 의학적 진단이 아닙니다.</div>
  </div>;
}
