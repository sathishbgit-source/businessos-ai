"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { navigationItems } from "../../lib/navigation";

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="app-sidebar">
      <div className="app-sidebar-brand">
        <Link href="/dashboard" className="app-brand">
          BusinessOS
        </Link>
      </div>

      <nav className="app-sidebar-nav" aria-label="Primary navigation">
        {navigationItems.map((item) => {
          const isActive =
            pathname === item.href ||
            pathname.startsWith(`${item.href}/`);

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`app-nav-item ${isActive ? "is-active" : ""}`}
              aria-current={isActive ? "page" : undefined}
            >
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
