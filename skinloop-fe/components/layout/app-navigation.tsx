"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  CalendarDays,
  ChartNoAxesColumnIncreasing,
  ClipboardPenLine,
  Home,
  type LucideIcon,
} from "lucide-react";

const items: Array<{ href: string; label: string; icon: LucideIcon }> = [
  { href: "/", label: "홈", icon: Home },
  { href: "/record", label: "기록", icon: ClipboardPenLine },
  { href: "/insight", label: "인사이트", icon: ChartNoAxesColumnIncreasing },
  { href: "/records", label: "내 기록", icon: CalendarDays },
];

function Links({ side = false }: { side?: boolean }) {
  const path = usePathname();
  return (
    <nav className={side ? "side-nav" : "bottom-nav"} aria-label="주요 메뉴">
      {items.map((item) => {
        const Icon = item.icon;
        return (
          <Link
            key={item.href}
            href={item.href}
            className={`nav-link ${path === item.href ? "active" : ""}`}
          >
            <Icon
              className="nav-icon"
              size={20}
              strokeWidth={1.8}
              aria-hidden="true"
            />
            <span className="nav-label">{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
}

export function AppSidebar() {
  return (
    <aside className="app-sidebar">
      <div className="brand">
        <span className="brand-full">SkinLoop</span>
        <span className="brand-short">SL</span>
      </div>
      <Links side />
    </aside>
  );
}
export function BottomNavigation() {
  return <Links />;
}
