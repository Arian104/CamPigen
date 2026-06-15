import { EmailBuilderSchema } from "@/components/email-builder/types";

export type Campaign = {
  id: string;
  name: string;
  subject: string;
  status: string;
  scheduled_at?: string | null;
  created_at?: string;
  updated_at?: string;
  template?: string | null;
  target_lists?: string[];
  total_sent?: number;
  total_opens?: number;
  total_clicks?: number;
  from_email?: string;
  from_name?: string;
  reply_to?: string;
};

export type Template = {
  id: string;
  name: string;
  subject: string;
  html_content: string;
  text_content?: string;
  template_type?: string;
  status?: string;
  variables?: string[];
  preview_data?: Record<string, string>;
  builder_schema?: EmailBuilderSchema;
};

export type Contact = {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
};

export type ContactList = {
  id: string;
  name: string;
  list_type?: string;
  description?: string;
  total_contacts?: number;
  is_active?: boolean;
};

export type OrganizationTemplateData = {
  id?: string;
  name?: string;
  brand_name?: string;
  website?: string;
  default_from_name?: string;
  default_from_email?: string;
  default_reply_to_email?: string;
  default_footer_text?: string;
  default_disclaimer?: string;
  facebook_url?: string;
  instagram_url?: string;
  linkedin_url?: string;
  whatsapp_number?: string;
  primary_color?: string;
  secondary_color?: string;
  accent_color?: string;
};
