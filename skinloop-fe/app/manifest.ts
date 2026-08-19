import type { MetadataRoute } from "next";

// PWA 매니페스트. "홈 화면에 추가" 시 앱 아이콘·독립 실행(standalone) 지원.
export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "SkinLoop",
    short_name: "SkinLoop",
    description: "생활습관과 피부 상태를 기록하고 연관 패턴을 찾는 서비스",
    start_url: "/",
    display: "standalone",
    background_color: "#fbf6f2",
    theme_color: "#d38b9d",
    lang: "ko",
    icons: [
      { src: "/icon-192.png", sizes: "192x192", type: "image/png", purpose: "any" },
      { src: "/icon-512.png", sizes: "512x512", type: "image/png", purpose: "any" },
      {
        src: "/icon-maskable-512.png",
        sizes: "512x512",
        type: "image/png",
        purpose: "maskable",
      },
    ],
  };
}
