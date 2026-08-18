import { create } from "zustand";

import { api, ApiError } from "@/lib/api-client";

type SessionStatus = "idle" | "loading" | "ready" | "error";

interface SessionState {
  status: SessionStatus;
  sessionId: string | null;
  isDemo: boolean;
  totalRecords: number;
  errorMessage: string | null;
  initialize: () => Promise<void>;
  retry: () => Promise<void>;
  setRecordSummary: (totalRecords: number) => void;
  setDemoMode: (isDemo: boolean, totalRecords?: number) => void;
}

async function createSession(set: (state: Partial<SessionState>) => void) {
  set({ status: "loading", errorMessage: null });

  try {
    const session = await api.createSession();
    set({
      status: "ready",
      sessionId: session.sessionId,
      isDemo: session.isDemo,
      totalRecords: session.totalRecords,
      errorMessage: null,
    });
  } catch (error) {
    const message =
      error instanceof ApiError
        ? error.message
        : "세션을 준비하지 못했습니다. 잠시 후 다시 시도해 주세요.";
    set({ status: "error", errorMessage: message });
  }
}

export const useSessionStore = create<SessionState>((set, get) => ({
  status: "idle",
  sessionId: null,
  isDemo: false,
  totalRecords: 0,
  errorMessage: null,

  async initialize() {
    if (get().status !== "idle") return;
    await createSession(set);
  },

  async retry() {
    await createSession(set);
  },

  setRecordSummary(totalRecords) {
    set({ totalRecords });
  },

  setDemoMode(isDemo, totalRecords) {
    set((state) => ({
      isDemo,
      totalRecords: totalRecords ?? state.totalRecords,
    }));
  },
}));
