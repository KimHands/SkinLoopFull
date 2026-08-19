"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { api, ApiError } from "@/lib/api-client";

const CACHE = "skinloop:last-pattern";
export default function AnalyzingScreen() {
  const router = useRouter();
  const [error, setError] = useState("");
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    let active = true;
    api
      .getPatterns()
      .then((result) => {
        if (!active) return;
        sessionStorage.setItem(CACHE, JSON.stringify(result));
        router.replace("/insight");
      })
      .catch((caught) => {
        if (active)
          setError(
            caught instanceof ApiError
              ? caught.message
              : "분석 결과를 불러오지 못했어요.",
          );
      });
    return () => {
      active = false;
    };
  }, [router, attempt]);
  return (
    <div className="page analyzing-page">
      <div className="analyzing-center">
        <div className="analysis-spinner" />
        <h1>기록을 살펴보고 있어요</h1>
        <p>잠시만 기다려주세요</p>
        {error && (
          <div className="stack retry-box">
            <p className="error-text" role="alert">
              {error}
            </p>
            <button
              className="btn btn-primary"
              onClick={() => {
                setError("");
                setAttempt((value) => value + 1);
              }}
            >
              다시 분석하기
            </button>
            <Link className="btn btn-outline" href="/">
              홈으로
            </Link>
          </div>
        )}
      </div>
      <p className="bottom-disclaimer">
        본 분석은 통계적 연관성을 보여주는 참고 자료이며 의학적 진단이 아닙니다.
      </p>
    </div>
  );
}
