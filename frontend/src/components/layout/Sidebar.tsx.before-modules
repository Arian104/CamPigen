"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  ChevronLeft,
  ChevronRight,
  Home,
  Mail,
  Send,
  Server,
  History,
  Users,
  Webhook,
  Settings,
  Link as LinkIcon,
} from "lucide-react";

import styles from "./Sidebar.module.css";

type SidebarProps = {
  collapsed: boolean;
  onToggle: () => void;
};

const NAV_ITEMS = [
  { href: "/", label: "Home", icon: Home },
  { href: "/campaigns", label: "Campaigns", icon: Mail },
  { href: "/instant-send", label: "Instant Send", icon: Send },
  { href: "/smtp", label: "SMTP Management", icon: Server },
  { href: "/email-history", label: "Email History", icon: History },
  { href: "/contacts", label: "Contacts", icon: Users },
  { href: "/links", label: "Links", icon: LinkIcon },
  { href: "/webhooks", label: "Webhooks", icon: Webhook },
  { href: "/settings/organization", label: "Settings", icon: Settings },
];

export function Sidebar({ collapsed, onToggle }: SidebarProps) {
  const pathname = usePathname();

  return (
    <aside className={collapsed ? `${styles.sidebar} ${styles.collapsed}` : styles.sidebar}>
      <div className={styles.header}>
        <button
          type="button"
          className={styles.toggle}
          onClick={onToggle}
          aria-label="Toggle sidebar"
        >
          {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
          {!collapsed ? <span>Collapse</span> : null}
        </button>
      </div>

      <nav className={styles.nav}>
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const active =
            pathname === item.href ||
            (item.href !== "/" && pathname.startsWith(item.href));

          return (
            <Link
              key={item.href}
              href={item.href}
              className={active ? `${styles.item} ${styles.active}` : styles.item}
              title={collapsed ? item.label : undefined}
            >
              <Icon size={19} />
              {!collapsed ? <span>{item.label}</span> : null}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
