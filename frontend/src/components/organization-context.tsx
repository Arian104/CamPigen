"use client";

import {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useState,
} from "react";

import { usePlatform } from "@/components/platform-context";

export type Organization = {
  id: string;
  name: string;
  subdomain: string;
  role: "owner" | "admin" | "manager" | "viewer" | string;
  is_active: boolean;
};

type OrganizationContextValue = {
  organizations: Organization[];
  activeOrganization: Organization | null;
  loadingOrganizations: boolean;
  organizationMessage: string;
  loadOrganizations: () => Promise<void>;
  switchOrganization: (organizationId: string) => Promise<boolean>;
};

const OrganizationContext = createContext<OrganizationContextValue | null>(null);

export function OrganizationProvider({ children }: { children: ReactNode }) {
  const { request, isAuthenticated } = usePlatform();

  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [activeOrganization, setActiveOrganization] = useState<Organization | null>(null);
  const [loadingOrganizations, setLoadingOrganizations] = useState(false);
  const [organizationMessage, setOrganizationMessage] = useState("");

  async function loadOrganizations() {
    if (!isAuthenticated) {
      setOrganizations([]);
      setActiveOrganization(null);
      return;
    }

    setLoadingOrganizations(true);

    const result = await request("/v1/organizations/");

    if (result.ok && Array.isArray(result.body)) {
      const rows = result.body as Organization[];
      setOrganizations(rows);

      const active = rows.find((org) => org.is_active) ?? rows[0] ?? null;
      setActiveOrganization(active);

      setOrganizationMessage(
        active ? `Active organization: ${active.name}` : "No organization found.",
      );
    } else {
      setOrganizations([]);
      setActiveOrganization(null);
      setOrganizationMessage("Failed to load organizations.");
    }

    setLoadingOrganizations(false);
  }

  async function switchOrganization(organizationId: string): Promise<boolean> {
    setLoadingOrganizations(true);

    const result = await request("/v1/organizations/switch/", {
      method: "POST",
      body: JSON.stringify({
        organization_id: organizationId,
      }),
    });

    if (result.ok) {
      await loadOrganizations();
      setLoadingOrganizations(false);
      return true;
    }

    setOrganizationMessage("Failed to switch organization.");
    setLoadingOrganizations(false);
    return false;
  }

  useEffect(() => {
    void loadOrganizations();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAuthenticated]);

  const value: OrganizationContextValue = {
    organizations,
    activeOrganization,
    loadingOrganizations,
    organizationMessage,
    loadOrganizations,
    switchOrganization,
  };

  return (
    <OrganizationContext.Provider value={value}>
      {children}
    </OrganizationContext.Provider>
  );
}

export function useOrganization() {
  const context = useContext(OrganizationContext);

  if (!context) {
    throw new Error("useOrganization must be used within OrganizationProvider");
  }

  return context;
}