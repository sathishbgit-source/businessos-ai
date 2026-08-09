"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button, Dropdown } from "../ui";
import { navigationItems } from "../../lib/navigation";

export function Topbar() {
  const [menuOpen, setMenuOpen] = useState(false);
  const pathname = usePathname();

  return (
    <header className="app-topbar">
      <div className="app-topbar-left">
        <Button
          variant="ghost"
          className="app-mobile-menu-button"
          aria-label="Toggle navigation menu"
          aria-expanded={menuOpen}
          onClick={() => setMenuOpen((open) => !open)}
        >
          ☰
        </Button>

        <h1 className="app-topbar-title">BusinessOS</h1>
      </div>

      <div className="app-topbar-actions">
        <Dropdown
          label="Account"
          items={[
            { label: "Profile", value: "profile" },
            { label: "Settings", value: "settings" },           { label: "Sign out", value: "sign-out" },
          ]}
          onSelect={() => undefined}
        />
      </div>

      {menuOpen ? (
        <nav
          className="app-mobile-menu"
          aria-label="Mobile navigation"
        >
          {navigationItems.map((item) => {
            const isActive =
              pathname === item.href ||
              pathname.startsWith(`${item.href}/`);

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`app-mobile-nav-item ${
                  isActive ? "is-active" : ""
                }`}
                aria-current={isActive ? "page" : undefined}
                onClick={() => setMenuOpen(false)}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
      ) : null}
    </header>
  );
}
