export type ActiveOrganizationDetail = {
  id: string;
  name: string;
  subdomain?: string;
  role?: string;
} | null;

export type AccountProfile = {
  id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  display_name: string;
  phone: string;
  job_title: string;
  department: string;
  avatar?: string | null;
  avatar_url: string;
  avatar_display_url: string;
  email_verified: boolean;
  timezone: string;
  language: string;
  date_format: string;
  time_format: "12h" | "24h";
  theme_mode: "system" | "light" | "dark";
  accent_color: string;
  sidebar_collapsed: boolean;
  default_dashboard: string;
  preferences: Record<string, unknown>;
  notification_preferences: Record<string, unknown>;
  active_organization: string | null;
  active_organization_detail: ActiveOrganizationDetail;
  is_staff: boolean;
  last_seen_at?: string | null;
  last_login_ip?: string | null;
  password_changed_at?: string | null;
  date_joined?: string | null;
};

export type AccountSession = {
  id: string;
  session_key: string;
  ip_address: string | null;
  user_agent: string;
  device_name: string;
  browser: string;
  os: string;
  country: string;
  city: string;
  is_active: boolean;
  last_activity_at: string;
  revoked_at: string | null;
  revoked_reason: string;
  created_at: string;
};

export type AccountActivity = {
  id: string;
  organization: string | null;
  organization_name: string | null;
  action: string;
  description: string;
  metadata: Record<string, unknown>;
  ip_address: string | null;
  user_agent: string;
  created_at: string;
};
