"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Bell } from "lucide-react";
import { api, ApiError } from "@/lib/api-client";
import { useSessionStore } from "@/stores/session-store";
import { WeeklyProgress } from "./weekly-progress";

export default function HomeScreen() {
  const router = useRouter();
  const total = useSessionStore((state) => state.totalRecords);
  const isDemo = useSessionStore((state) => state.isDemo);
  const setDemo = useSessionStore((state) => state.setDemoMode);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const need = Math.max(0, 7 - total);
  const ready = total >= 7;

  async function loadDemo() {
    setBusy(true);
    setError("");
    try {
      const result = await api.loadDemo();
      setDemo(true, result.recordDays);
      router.push("/analyzing");
    } catch (caught) {
      setError(
        caught instanceof ApiError
          ? caught.message
          : "샘플을 불러오지 못했어요.",
      );
      setBusy(false);
    }
  }

  return (
    <div className="page home-page stack">
      <header className="brand-header">
        <div>
          <div className="wordmark">SkinLoop</div>
          <p>오늘도 기록했나요?</p>
        </div>
        <span className="bell" aria-hidden="true">
          <Bell size={16} strokeWidth={1.7} />
        </span>
      </header>

      {ready ? (
        <>
          <section className="card score-card">
            <div className="score-ring">
              <span>71</span>
            </div>
            <div className="score-copy">
              <span className="caption">오늘 예상 점수</span>
              <strong>68 ~ 74</strong>
              <p>어제와 비슷한 흐름이에요</p>
            </div>
            <Link className="btn btn-primary btn-block" href="/record">
              기록하기
            </Link>
          </section>
          <Link href="/insight" className="card insight-teaser">
            <div>
              <strong>새 인사이트가 준비됐어요</strong>
              <span>최근 12일 기록 기준</span>
            </div>
            <b>인사이트 보기</b>
          </Link>
          <section className="card">
            <div className="section-heading">
              <strong>{total}일째 기록 중</strong>
              <span>최근 7일</span>
            </div>
            <WeeklyProgress filled={Math.min(total, 7)} />
          </section>
        </>
      ) : (
        <>
          <section className="card progress-card">
            <strong>기록이 7일 모이면 패턴 분석이 시작돼요</strong>
            <p>앞으로 {need}일</p>
            <div className="progress-track">
              <i style={{ width: `${Math.min((total / 7) * 100, 100)}%` }} />
            </div>
            <div className="progress-label">
              <span>{total}일 기록</span>
              <span>7일</span>
            </div>
            <Link className="btn btn-primary btn-block" href="/record">
              기록하기
            </Link>
          </section>
          <section className="card">
            <div className="section-heading">
              <strong>{total || 1}일째 기록 중</strong>
              <span>최근 7일</span>
            </div>
            <WeeklyProgress filled={Math.min(total, 7)} />
          </section>
          {!isDemo && (
            <section className="card sample-card">
              <strong>먼저 둘러보고 싶다면?</strong>
              <p>28일치 샘플로 미리 확인해보세요</p>
              <button
                className="btn btn-secondary btn-block"
                disabled={busy}
                onClick={() => void loadDemo()}
              >
                {busy ? "샘플 준비 중…" : "28일 샘플 보기"}
              </button>
              {error && (
                <p className="error-text" role="alert">
                  {error}
                </p>
              )}
            </section>
          )}
        </>
      )}
    </div>
  );
}
