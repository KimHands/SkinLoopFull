const ANON_TOKEN_KEY = "skinloop:anon-token";

export function getAnonToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(ANON_TOKEN_KEY);
}

export function getOrCreateAnonToken(): string {
  const storedToken = getAnonToken();
  if (storedToken) return storedToken;

  const token = crypto.randomUUID();
  window.localStorage.setItem(ANON_TOKEN_KEY, token);
  return token;
}
