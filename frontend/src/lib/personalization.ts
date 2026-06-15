import { AccountProfile } from "@/types/account";

type ThemeMode = "system" | "light" | "dark";

function getSystemTheme(): "light" | "dark" {
  if (typeof window === "undefined") return "light";
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

export function resolveThemeMode(mode?: ThemeMode | string): "light" | "dark" {
  if (mode === "dark") return "dark";
  if (mode === "light") return "light";
  return getSystemTheme();
}

export function applyThemeMode(mode?: ThemeMode | string) {
  if (typeof document === "undefined") return;

  const resolved = resolveThemeMode(mode);
  document.documentElement.setAttribute("data-theme", resolved);
  document.documentElement.setAttribute("data-theme-preference", mode || "system");

  if (typeof window !== "undefined") {
    window.localStorage.setItem("theme-mode", mode || "system");
  }
}

export function applyAccentColor(color?: string) {
  if (typeof document === "undefined") return;

  const safeColor = color && color.trim() ? color.trim() : "#4f46e5";

  document.documentElement.style.setProperty("--primary", safeColor);
  document.documentElement.style.setProperty("--accent", safeColor);
  document.documentElement.style.setProperty("--primary-hover", safeColor);
  document.documentElement.style.setProperty("--primary-soft", `${safeColor}18`);
}

export function applyAccountPersonalization(profile?: Partial<AccountProfile> | null) {
  if (!profile) return;

  applyThemeMode(profile.theme_mode || "system");
  applyAccentColor(profile.accent_color || "#4f46e5");

  if (typeof window !== "undefined") {
    window.localStorage.setItem("account-theme-mode", profile.theme_mode || "system");
    window.localStorage.setItem("account-accent-color", profile.accent_color || "#4f46e5");
    window.localStorage.setItem("account-sidebar-collapsed", String(Boolean(profile.sidebar_collapsed)));
    window.localStorage.setItem("account-timezone", profile.timezone || "Asia/Dhaka");
    window.localStorage.setItem("account-language", profile.language || "en");
    window.localStorage.setItem("account-date-format", profile.date_format || "MMM D, YYYY");
    window.localStorage.setItem("account-time-format", profile.time_format || "12h");
  }
}

export function getInitialSidebarCollapsed() {
  if (typeof window === "undefined") return false;
  return window.localStorage.getItem("account-sidebar-collapsed") === "true";
}
