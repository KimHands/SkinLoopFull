"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
const items = [
  { href: "/", label: "홈" },
  { href: "/record", label: "기록" },
  { href: "/insight", label: "인사이트" },
  { href: "/records", label: "내 기록" },
];
function Links({ side = false }: { side?: boolean }) {
  const path = usePathname();
  return (
    <nav className={side ? "side-nav" : "bottom-nav"} aria-label="주요 메뉴">
      {items.map(({ href, label }) => (
        <Link
          key={href}
          href={href}
          className={`nav-link ${path === href ? "active" : ""}`}
        >
          {label}
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
