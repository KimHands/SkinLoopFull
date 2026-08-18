"use client";

import { useEffect } from "react";

import { useSessionStore } from "@/stores/session-store";

export function SessionBootstrap({ children }: { children: React.ReactNode }) {
  const status = useSessionStore((state) => state.status);
  const errorMessage = useSessionStore((state) => state.errorMessage);
  const initialize = useSessionStore((state) => state.initialize);
  const retry = useSessionStore((state) => state.retry);

  useEffect(() => {
    void initialize();
  }, [initialize]);

  if (status === "idle" || status === "loading") {
    return (
      <main
        aria-busy="true"
        aria-live="polite"
        className="flex min-h-screen items-center justify-center px-5 text-center"
      >
        <p className="text-sm text-gray-500">SkinLoop를 준비하고 있어요.</p>
      </main>
    );
  }

  if (status === "error") {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center gap-4 px-5 text-center">
        <p className="text-sm text-gray-600">{errorMessage}</p>
        <button
          type="button"
          className="rounded-lg border px-5 py-3 text-sm font-semibold"
          onClick={() => void retry()}
        >
          다시 시도하기
        </button>
      </main>
    );
  }

  return children;
}
