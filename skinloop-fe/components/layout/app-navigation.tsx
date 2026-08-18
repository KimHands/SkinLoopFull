"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const items = [
  { href: "/", label: "홈", icon: "⌂" },
  { href: "/record", label: "기록", icon: "▤" },
  { href: "/insight", label: "인사이트", icon: "⌁" },
  { href: "/records", label: "내 기록", icon: "□" },
];

function Links({ side = false }: { side?: boolean }) {
  const path = usePathname();
  return (
    <nav className={side ? "side-nav" : "bottom-nav"} aria-label="주요 메뉴">
      {items.map((item) => (
        <Link
          key={item.href}
          href={item.href}
          className={`nav-link ${path === item.href ? "active" : ""}`}
        >
          <span className="nav-icon" aria-hidden="true">
            {item.icon}
          </span>
          <span>{item.label}</span>
        </Link>
      ))}
    </nav>
  );
}

export function AppSidebar() {
  return (
    <aside className="app-sidebar">
      <div className="brand">SkinLoop</div>
      <Links side />
    </aside>
  );
}
export function BottomNavigation() {
  return <Links />;
}
