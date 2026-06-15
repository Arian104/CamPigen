"use client";

import {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

type LoginResponse = {
  access?: string;
  refresh?: string;
};

type PlatformContextValue = {
  apiBase: string;
  setApiBase: (value: string) => void;
  accessToken: string;
  refreshToken: string;
  username: string;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  refreshAccessToken: () => Promise<boolean>;
  logout: () => void;
  request: (
    path: string,
    init?: RequestInit,
    requiresAuth?: boolean,
  ) => Promise<{ ok: boolean; status: number; body: unknown }>;
};

const DEFAULT_API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api";

const PlatformContext = createContext<PlatformContextValue | null>(null);

function parseJsonSafe(text: string): unknown {
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

export function PlatformProvider({ children }: { children: ReactNode }) {
  const [apiBase, setApiBase] = useState(() => {
    if (typeof window === "undefined") return DEFAULT_API_BASE;
    return localStorage.getItem("platform_api_base") ?? DEFAULT_API_BASE;
  });

  const [accessToken, setAccessToken] = useState(() => {
    if (typeof window === "undefined") return "";
    return localStorage.getItem("platform_access_token") ?? "";
  });

  const [refreshToken, setRefreshToken] = useState(() => {
    if (typeof window === "undefined") return "";
    return localStorage.getItem("platform_refresh_token") ?? "";
  });

  const [username, setUsername] = useState(() => {
    if (typeof window === "undefined") return "";
    return localStorage.getItem("platform_username") ?? "";
  });

  useEffect(() => {
    localStorage.setItem("platform_api_base", apiBase);
  }, [apiBase]);

  useEffect(() => {
    localStorage.setItem("platform_access_token", accessToken);
  }, [accessToken]);

  useEffect(() => {
    localStorage.setItem("platform_refresh_token", refreshToken);
  }, [refreshToken]);

  useEffect(() => {
    localStorage.setItem("platform_username", username);
  }, [username]);

  const normalizedBase = useMemo(() => apiBase.replace(/\/+$/, ""), [apiBase]);
  const isAuthenticated = Boolean(accessToken);

  async function request(
    path: string,
    init: RequestInit = {},
    requiresAuth = true,
  ): Promise<{ ok: boolean; status: number; body: unknown }> {
    const headers = new Headers(init.headers ?? {});

    if (!headers.has("Content-Type") && init.body) {
      headers.set("Content-Type", "application/json");
    }

    if (requiresAuth && accessToken) {
      headers.set("Authorization", `Bearer ${accessToken}`);
    }

    const res = await fetch(`${normalizedBase}${path}`, {
      ...init,
      headers,
    });

    const text = await res.text();
    const body = parseJsonSafe(text);

    if (requiresAuth && res.status === 401) {
      logout();
    }

    return { ok: res.ok, status: res.status, body };
  }

  async function login(email: string, password: string): Promise<boolean> {
    const result = await request(
      "/auth/login/",
      {
        method: "POST",
        body: JSON.stringify({ email, password }),
      },
      false,
    );

    if (!result.ok || typeof result.body !== "object" || !result.body) {
      return false;
    }

    const data = result.body as LoginResponse;

    setAccessToken(data.access ?? "");
    setRefreshToken(data.refresh ?? "");
    setUsername(email);

    return Boolean(data.access);
  }

  async function refreshAccessTokenInternal(): Promise<boolean> {
    if (!refreshToken) return false;

    const result = await request(
      "/auth/refresh/",
      {
        method: "POST",
        body: JSON.stringify({ refresh: refreshToken }),
      },
      false,
    );

    if (!result.ok || typeof result.body !== "object" || !result.body) {
      return false;
    }

    const data = result.body as LoginResponse;

    if (!data.access) return false;

    setAccessToken(data.access);
    return true;
  }

  function logout() {
    setAccessToken("");
    setRefreshToken("");
    setUsername("");
  }

  const value: PlatformContextValue = {
    apiBase,
    setApiBase,
    accessToken,
    refreshToken,
    username,
    isAuthenticated,
    login,
    refreshAccessToken: refreshAccessTokenInternal,
    logout,
    request,
  };

  return <PlatformContext.Provider value={value}>{children}</PlatformContext.Provider>;
}

export function usePlatform() {
  const context = useContext(PlatformContext);

  if (!context) {
    throw new Error("usePlatform must be used within PlatformProvider");
  }

  return context;
}