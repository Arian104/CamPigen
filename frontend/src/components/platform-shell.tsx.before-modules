"use client";

import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

import { Sidebar } from "@/components/layout/Sidebar";
import { Topbar } from "@/components/layout/Topbar";
import { usePlatform } from "@/components/platform-context";
import { AccountProfile } from "@/types/account";
import {
  applyAccountPersonalization,
  getInitialSidebarCollapsed,
} from "@/lib/personalization";

import styles from "@/components/PlatformShell.module.css";

const PUBLIC_ROUTES = [
  "/login",
  "/register",
  "/forgot-password",
  "/reset-password",
  "/verify-email",
];

export function PlatformShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { request } = usePlatform();

  const [collapsed, setCollapsed] = useState(false);
  const [account, setAccount] = useState<AccountProfile | null>(null);
  const [mounted, setMounted] = useState(false);

  const isPublicRoute = PUBLIC_ROUTES.some((route) => pathname.startsWith(route));

  async function loadAccountProfile() {
    const result = await request("/v1/accounts/me/");

    if (result.ok && result.body) {
      const profile = result.body as AccountProfile;
      setAccount(profile);
      setCollapsed(Boolean(profile.sidebar_collapsed));
      applyAccountPersonalization(profile);
    } else {
      setCollapsed(getInitialSidebarCollapsed());
    }
  }

  async function toggleSidebar() {
    const next = !collapsed;
    setCollapsed(next);

    window.localStorage.setItem("account-sidebar-collapsed", String(next));

    await request("/v1/accounts/me/preferences/", {
      method: "PATCH",
      body: JSON.stringify({
        sidebar_collapsed: next,
      }),
    });
  }

  function updateAccount(profile: AccountProfile) {
    setAccount(profile);
    setCollapsed(Boolean(profile.sidebar_collapsed));
    applyAccountPersonalization(profile);
  }

  useEffect(() => {
    setMounted(true);

    if (!isPublicRoute) {
      void loadAccountProfile();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isPublicRoute]);

  if (isPublicRoute) {
    return <>{children}</>;
  }

  return (
    <div className={collapsed ? `${styles.shell} ${styles.collapsed}` : styles.shell}>
      <Topbar account={account} mounted={mounted} onAccountUpdated={updateAccount} />

      <Sidebar collapsed={collapsed} onToggle={() => void toggleSidebar()} />

      <main className={styles.content}>{children}</main>
    </div>
  );
}
