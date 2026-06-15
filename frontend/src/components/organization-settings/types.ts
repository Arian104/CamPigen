export type Organization = {
  id: string;
  name: string;
  subdomain: string;
  plan: string;
  industry_type: string;
  website: string;
  country: string;
  timezone: string;
  is_active: boolean;

  brand_name: string;
  logo_url: string;
  favicon_url: string;
  primary_color: string;
  secondary_color: string;
  accent_color: string;
  font_family: string;
  button_style: string;

  default_from_name: string;
  default_from_email: string;
  default_reply_to_email: string;
  default_campaign_language: string;
  default_footer_text: string;
  default_disclaimer: string;
  default_template_width: number;
  default_header_logo_enabled: boolean;
  default_footer_enabled: boolean;

  company_legal_name: string;
  business_phone: string;
  support_email: string;
  business_address: string;
  city: string;
  state: string;
  postal_code: string;
  unsubscribe_policy: string;
  physical_address_required: boolean;
  gdpr_enabled: boolean;
  double_opt_in_enabled: boolean;
  marketing_consent_required: boolean;

  contact_schema_preset: string;
  preset_applied: boolean;

  facebook_url: string;
  instagram_url: string;
  linkedin_url: string;
  twitter_url: string;
  youtube_url: string;
  tiktok_url: string;
  whatsapp_number: string;

  max_users: number;
  max_contacts: number;
  max_templates: number;
  max_segments: number;
  automation_enabled: boolean;
  advanced_segmentation_enabled: boolean;
  webhooks_enabled: boolean;
  ai_features_enabled: boolean;
  custom_branding_enabled: boolean;
};

export type Member = {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  status: string;
  created_at: string;
};

export type Preset = {
  key: string;
  label: string;
  fields: Array<{ name: string; key: string; field_type: string }>;
  tags: string[];
  lists: string[];
};

export type UpdateOrganizationField = <K extends keyof Organization>(
  key: K,
  value: Organization[K],
) => void;
