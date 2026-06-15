export type Contact = {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  full_name?: string;

  phone?: string;
  company?: string;
  job_title?: string;
  city?: string;
  country?: string;
  timezone?: string;
  language?: string;

  source?: string;
  source_detail?: string;
  lifecycle_stage?: string;

  lead_score?: number;
  engagement_score?: number;

  consent_status?: string;
  is_unsubscribed?: boolean;
  email_verified?: boolean;
  email_status?: string;

  custom_fields?: Record<string, string | number | boolean | string[]>;
  metadata?: Record<string, string>;
  preferences?: Record<string, unknown>;

  tag_ids?: string[];
  tag_names?: string[];
  list_ids?: string[];

  created_at?: string;
  updated_at?: string;
};

export type ContactPayload = Partial<Contact>;

export type ContactFieldDefinition = {
  id: string;
  field_key: string;
  label: string;
  field_type:
    | "text"
    | "textarea"
    | "number"
    | "decimal"
    | "date"
    | "datetime"
    | "boolean"
    | "select"
    | "multi_select"
    | "email"
    | "phone"
    | "url";
  options?: string[];
  default_value?: string;
  is_required?: boolean;
  is_filterable?: boolean;
  is_visible_in_table?: boolean;
  is_importable?: boolean;
  help_text?: string;
  placeholder?: string;
  order?: number;
  is_active?: boolean;
};

export type Tag = {
  id: string;
  name: string;
  slug?: string;
  tag_type?: string;
  color?: string;
  description?: string;
  contact_count?: number;
};

export type ContactList = {
  id: string;
  name: string;
  list_type: "static" | "dynamic" | "suppression" | "seed";
  description?: string;
  filter_criteria?: Record<string, unknown>;
  total_contacts?: number;
  contact_count?: number;
  is_active?: boolean;
};

export type Paginated<T> = {
  count?: number;
  results?: T[];
};

export function rowsFromApi<T>(body: unknown): T[] {
  if (Array.isArray(body)) return body as T[];
  if (typeof body === "object" && body !== null && "results" in body) {
    return ((body as Paginated<T>).results ?? []) as T[];
  }
  return [];
}
