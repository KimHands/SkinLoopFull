import type { Metadata, Viewport } from "next";
import { Geist } from "next/font/google";

import { SessionBootstrap } from "@/components/session/session-bootstrap";
import { AppFrame } from "@/components/layout/app-frame";
import { RegisterSW } from "@/components/pwa/register-sw";

import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "SkinLoop",
  description: "생활습관과 피부 상태를 기록하고 연관 패턴을 찾는 서비스",
  manifest: "/manifest.webmanifest",
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "SkinLoop",
  },
  icons: {
    icon: "/icon-192.png",
    apple: "/apple-touch-icon.png",
  },
};

export const viewport: Viewport = {
  themeColor: "#d38b9d",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body className={`${geistSans.variable} antialiased`}>
        {/* 모바일 우선. 데스크톱은 max-width 480px 중앙 정렬 (spec 8절) */}
        <RegisterSW />
        <SessionBootstrap>
          <AppFrame>{children}</AppFrame>
        </SessionBootstrap>
      </body>
    </html>
  );
}
