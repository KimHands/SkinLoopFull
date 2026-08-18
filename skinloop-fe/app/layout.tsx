import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";

import { SessionBootstrap } from "@/components/session/session-bootstrap";

import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "SkinLoop",
  description: "생활습관과 피부 상태를 기록하고 연관 패턴을 찾는 서비스",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {/* 모바일 우선. 데스크톱은 max-width 480px 중앙 정렬 (spec 8절) */}
        <SessionBootstrap>
          <div className="mx-auto min-h-screen w-full max-w-[480px] px-4">
            {children}
          </div>
        </SessionBootstrap>
      </body>
    </html>
  );
}
