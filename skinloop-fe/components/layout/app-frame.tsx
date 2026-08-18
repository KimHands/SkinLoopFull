"use client";

import { useSessionStore } from "@/stores/session-store";
import { AppSidebar, BottomNavigation } from "./app-navigation";
import { MobileStatusBar } from "./mobile-status-bar";

export function AppFrame({ children }: { children: React.ReactNode }) {
  const isDemo = useSessionStore((state) => state.isDemo);
  return (
    <div className="app-shell">
      <AppSidebar />
      <div className="app-content">
        <main className="app-main">
          <MobileStatusBar />
          {isDemo && (
            <div className="demo-banner">28일치 샘플 데이터 체험 중</div>
          )}
          {children}
        </main>
        <BottomNavigation />
      </div>
    </div>
  );
}
