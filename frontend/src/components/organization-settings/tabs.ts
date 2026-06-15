import {
  Building2,
  Palette,
  Mail,
  Share2,
  ShieldCheck,
  Users,
  Database,
  Crown,
} from "lucide-react";

export const TABS = [
  { key: "profile", label: "Profile", icon: Building2 },
  { key: "branding", label: "Branding", icon: Palette },
  { key: "campaign", label: "Campaign Defaults", icon: Mail },
  { key: "social", label: "Social Links", icon: Share2 },
  { key: "compliance", label: "Compliance", icon: ShieldCheck },
  { key: "team", label: "Team Members", icon: Users },
  { key: "presets", label: "CDP Presets", icon: Database },
  { key: "plan", label: "Plan & Access", icon: Crown },
] as const;

export type OrganizationTabKey = (typeof TABS)[number]["key"];
