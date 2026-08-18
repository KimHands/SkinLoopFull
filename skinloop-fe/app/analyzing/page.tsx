"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { api, ApiError } from "@/lib/api-client";

export const PATTERN_CACHE_KEY = "skinloop:last-pattern";

export default function AnalyzingPage() {
  const router = useRouter();
  const [error, setError] = useState("");
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    let active = true;
    api.getPatterns().then((result) => {
      if (!active) return;
      sessionStorage.setItem(PATTERN_CACHE_KEY, JSON.stringify(result));
      router.replace("/insight");
    }).catch((caught) => {
      if (active) setError(caught instanceof ApiError ? caught.message : "분석 결과를 불러오지 못했습니다.");
    });
    return () => { active = false; };
  }, [router, attempt]);

  return <div className="page" style={{ minHeight: "70vh", display: "grid", placeItems: "center", textAlign: "center" }}>
    <div className="card" style={{ maxWidth: 480 }}>
      <div style={{ fontSize: 40 }}>◌</div>
      <h1 className="page-title">기록을 살펴보고 있어요</h1>
      <p className="subtle">생활 습관과 피부 변화가 함께 나타난 패턴을 정리하고 있어요.</p>
      {error && <div className="stack"><p className="error-text" role="alert">{error}</p><button className="btn btn-primary" onClick={() => { setError(""); setAttempt((v) => v + 1); }}>다시 분석하기</button><Link className="btn btn-outline" href="/">홈으로</Link></div>}
    </div>
  </div>;
}
