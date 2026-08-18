import { getOrCreateAnonToken } from "@/lib/anon-token";
import type {
  ApiErrorBody,
  DemoResponse,
  PatternResponse,
  RecordCreateRequest,
  RecordItem,
  RecordResponse,
  SessionResponse,
  WhatIfRequest,
  WhatIfResponse,
} from "@/types/api";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE?.replace(/\/$/, "") ?? "";

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly code: string,
    message: string,
    public readonly body: ApiErrorBody,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

interface ApiRequestOptions extends RequestInit {
  authenticated?: boolean;
}

async function apiRequest<T>(path: string, options: ApiRequestOptions = {}): Promise<T> {
  const { authenticated = true, headers, ...requestOptions } = options;
  const requestHeaders = new Headers(headers);
  requestHeaders.set("Accept", "application/json");

  if (requestOptions.body) requestHeaders.set("Content-Type", "application/json");
  if (authenticated) requestHeaders.set("X-Anon-Token", getOrCreateAnonToken());

  let response: Response;
  try {
    response = await fetch(`${API_BASE}${path}`, {
      ...requestOptions,
      headers: requestHeaders,
    });
  } catch {
    throw new ApiError(0, "NETWORK_ERROR", "네트워크 연결을 확인해 주세요.", {});
  }

  if (!response.ok) {
    const body = (await response.json().catch(() => ({}))) as ApiErrorBody;
    throw new ApiError(
      response.status,
      body.error ?? "UNKNOWN_ERROR",
      body.message ?? body.detail ?? "요청을 처리하지 못했습니다.",
      body,
    );
  }

  return response.json() as Promise<T>;
}

export const api = {
  createSession(): Promise<SessionResponse> {
    const anonToken = getOrCreateAnonToken();
    return apiRequest("/api/session", {
      method: "POST",
      authenticated: false,
      body: JSON.stringify({ anonToken }),
    });
  },

  createRecord(payload: RecordCreateRequest): Promise<RecordResponse> {
    return apiRequest("/api/records", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  getRecords(): Promise<RecordItem[]> {
    return apiRequest("/api/records");
  },

  getPatterns(): Promise<PatternResponse> {
    return apiRequest("/api/patterns");
  },

  compareScenario(payload: WhatIfRequest): Promise<WhatIfResponse> {
    return apiRequest("/api/whatif", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  loadDemo(): Promise<DemoResponse> {
    return apiRequest("/api/demo");
  },

  clearDemo(): Promise<{ cleared: boolean }> {
    return apiRequest("/api/demo", { method: "DELETE" });
  },
};
