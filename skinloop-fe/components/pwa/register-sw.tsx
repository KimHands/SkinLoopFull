"use client";

import { useEffect } from "react";

// 서비스워커 등록. 보안 컨텍스트(HTTPS/localhost)에서만 동작한다.
// 평문 http 배포에서는 등록을 건너뛴다(브라우저가 막음) — 에러 없이 무시.
export function RegisterSW() {
  useEffect(() => {
    if (
      typeof navigator === "undefined" ||
      !("serviceWorker" in navigator) ||
      !window.isSecureContext
    ) {
      return;
    }
    const register = () => {
      navigator.serviceWorker.register("/sw.js").catch(() => {});
    };
    // 이미 load가 끝났으면(대개 그렇다) 바로 등록, 아니면 load에서 한 번.
    if (document.readyState === "complete") {
      register();
    } else {
      window.addEventListener("load", register, { once: true });
      return () => window.removeEventListener("load", register);
    }
  }, []);

  return null;
}
