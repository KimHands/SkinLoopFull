"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, ApiError } from "@/lib/api-client";
import { useSessionStore } from "@/stores/session-store";
import type { RecordItem } from "@/types/api";
import { RecordsCalendar } from "./records-calendar";

export default function RecordsScreen() {
  const router = useRouter();
  const isDemo = useSessionStore((state) => state.isDemo);
  const setDemo = useSessionStore((state) => state.setDemoMode);
  const [records, setRecords] = useState<RecordItem[]>([]);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  useEffect(() => {
    api
      .getRecords()
      .then(setRecords)
      .catch((caught) =>
        setError(
          caught instanceof ApiError
            ? caught.message
            : "기록을 불러오지 못했어요.",
        ),
      );
  }, []);
  async function clearDemo() {
    if (!window.confirm("샘플 기록 28일과 샘플 실험 결과를 삭제할까요?"))
      return;
    setBusy(true);
    try {
      await api.clearDemo();
      setDemo(false, 0);
      router.push("/");
    } catch (caught) {
      setError(
        caught instanceof ApiError
          ? caught.message
          : "샘플을 종료하지 못했어요.",
      );
      setBusy(false);
    }
  }
  const recent = records.slice(-7);
  const average = (key: "sleepHours" | "stressLevel" | "exerciseMin") =>
    recent.length
      ? recent.reduce((sum, item) => sum + item[key], 0) / recent.length
      : 0;
  return (
    <div className="page records-page stack">
      <header className="page-header">
        <h1 className="page-title">내 기록</h1>
        <Link className="text-action" href="/record">
          기록 추가
        </Link>
      </header>
      {error && (
        <p className="error-text" role="alert">
          {error}
        </p>
      )}
      <RecordsCalendar records={records} />
      <section className="card">
        <h2 className="section-title">이번 주 요약</h2>
        <p className="summary-score">
          평균 점수{" "}
          <strong>
            {recent.length
              ? `${Math.max(0, Math.round(recent.reduce((sum, item) => sum + item.skinScore, 0) / recent.length) - 3)} ~ ${Math.min(100, Math.round(recent.reduce((sum, item) => sum + item.skinScore, 0) / recent.length) + 3)}`
              : "기록 없음"}
          </strong>
        </p>
        <div className="metric-grid">
          <div>
            <span>수면 평균</span>
            <strong>{average("sleepHours").toFixed(1)}시간</strong>
          </div>
          <div>
            <span>스트레스 평균</span>
            <strong>{average("stressLevel").toFixed(1)} / 5</strong>
          </div>
          <div>
            <span>운동 평균</span>
            <strong>{Math.round(average("exerciseMin"))}분</strong>
          </div>
        </div>
      </section>
      {isDemo && (
        <section className="card result-card">
          <div className="section-heading">
            <strong>실험 결과</strong>
            <span>수면 +1시간 · 14일</span>
          </div>
          <p>실험 전 7일과 실험 중 14일의 경향을 비교했어요.</p>
          <div className="range-grid">
            <div>
              <span>실험 전</span>
              <strong>52~58</strong>
            </div>
            <div>
              <span>실험 중</span>
              <strong>60~66</strong>
            </div>
          </div>
        </section>
      )}
      {records.length > 0 && (
        <section className="card">
          <h2 className="section-title">최근 기록</h2>
          <div className="record-list">
            {[...records]
              .reverse()
              .slice(0, 5)
              .map((record) => (
                <article key={record.recordId}>
                  <strong>{record.recordedAt}</strong>
                  <span>
                    수면 {record.sleepHours}시간 · 스트레스 {record.stressLevel}
                    /5
                  </span>
                  <b>
                    {Math.max(0, record.skinScore - 3)}~
                    {Math.min(100, record.skinScore + 3)}
                  </b>
                </article>
              ))}
          </div>
        </section>
      )}
      {isDemo && (
        <button
          className="btn btn-outline btn-block"
          disabled={busy}
          onClick={() => void clearDemo()}
        >
          {busy ? "샘플을 정리하고 있어요…" : "샘플 체험 종료하기"}
        </button>
      )}
      <div className="disclaimer">
        본 분석은 통계적 연관성을 보여주는 참고 자료이며 의학적 진단이 아닙니다.
      </div>
    </div>
  );
}
