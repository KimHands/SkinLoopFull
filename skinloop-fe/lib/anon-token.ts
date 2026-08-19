const ANON_TOKEN_KEY = "skinloop:anon-token";

// crypto.randomUUID()는 보안 컨텍스트(HTTPS/localhost)에서만 동작한다.
// 평문 http(공인 IP 배포)에서는 없으므로 getRandomValues 기반 UUID v4로 폴백한다.
function generateUuid(): string {
  if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
    return crypto.randomUUID();
  }
  const bytes = new Uint8Array(16);
  if (typeof crypto !== "undefined" && crypto.getRandomValues) {
    crypto.getRandomValues(bytes);
  } else {
    for (let i = 0; i < 16; i += 1) bytes[i] = Math.floor(Math.random() * 256);
  }
  bytes[6] = (bytes[6] & 0x0f) | 0x40; // version 4
  bytes[8] = (bytes[8] & 0x3f) | 0x80; // variant
  const hex = Array.from(bytes, (b) => b.toString(16).padStart(2, "0"));
  return (
    hex.slice(0, 4).join("") +
    "-" +
    hex.slice(4, 6).join("") +
    "-" +
    hex.slice(6, 8).join("") +
    "-" +
    hex.slice(8, 10).join("") +
    "-" +
    hex.slice(10, 16).join("")
  );
}

export function getAnonToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(ANON_TOKEN_KEY);
}

export function getOrCreateAnonToken(): string {
  const storedToken = getAnonToken();
  if (storedToken) return storedToken;

  const token = generateUuid();
  window.localStorage.setItem(ANON_TOKEN_KEY, token);
  return token;
}
