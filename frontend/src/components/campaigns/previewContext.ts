import { Contact, OrganizationTemplateData } from "./CampaignTypes";

function clean(value: unknown, fallback = "") {
  if (value === null || value === undefined) return fallback;
  const text = String(value).trim();
  return text || fallback;
}

function fullName(contact?: Contact | null) {
  const first = clean(contact?.first_name);
  const last = clean(contact?.last_name);
  return [first, last].filter(Boolean).join(" ") || "Arian";
}

export function pickPreviewContact(contacts: Contact[]) {
  if (!contacts.length) return null;

  const usable = contacts.filter((contact) => contact.email || contact.first_name || contact.last_name);
  if (!usable.length) return contacts[0];

  const randomIndex = Math.floor(Math.random() * usable.length);
  return usable[randomIndex];
}

export function buildPreviewContext(
  organization?: OrganizationTemplateData | null,
  contact?: Contact | null,
): Record<string, string> {
  const hasContact = Boolean(contact);

  const orgName = clean(organization?.name, "Your Organization");
  const brandName = clean(organization?.brand_name, orgName);
  const legalName = clean(organization?.company_legal_name, brandName);

  const firstName = hasContact ? clean(contact?.first_name, "Client") : "Arian";
  const lastName = hasContact ? clean(contact?.last_name, "") : "";
  const email = hasContact ? clean(contact?.email, "client@example.com") : "arian@example.com";

  const contactCompany = clean(
    contact?.company_name || contact?.company,
    brandName,
  );

  const context: Record<string, string> = {
    first_name: firstName,
    last_name: lastName,
    full_name: fullName(contact),
    email,
    phone: clean(contact?.phone, ""),
    company_name: contactCompany,
    job_title: clean(contact?.job_title, ""),
    city: clean(contact?.city || organization?.city, ""),
    country: clean(contact?.country || organization?.country, ""),

    organization_name: orgName,
    organization_brand_name: brandName,
    organization_legal_name: legalName,
    organization_subdomain: clean(organization?.subdomain, ""),
    organization_website: clean(organization?.website, ""),
    organization_logo_url: clean(organization?.logo_url, ""),
    organization_favicon_url: clean(organization?.favicon_url, ""),
    organization_timezone: clean(organization?.timezone, ""),

    brand_name: brandName,
    brand_primary_color: clean(organization?.primary_color, "#2563eb"),
    brand_secondary_color: clean(organization?.secondary_color, "#111827"),
    brand_accent_color: clean(organization?.accent_color, "#10b981"),
    brand_font_family: clean(organization?.font_family, "Inter"),

    from_name: clean(organization?.default_from_name, brandName),
    from_email: clean(organization?.default_from_email, ""),
    reply_to_email: clean(organization?.default_reply_to_email, ""),

    support_email: clean(organization?.support_email, ""),
    business_phone: clean(organization?.business_phone, ""),
    business_address: clean(organization?.business_address, ""),
    business_city: clean(organization?.city, ""),
    business_state: clean(organization?.state, ""),
    business_postal_code: clean(organization?.postal_code, ""),
    business_country: clean(organization?.country, ""),

    facebook_url: clean(
      organization?.facebook_url,
      "https://facebook.com",
    ),

    instagram_url: clean(
      organization?.instagram_url,
      "https://instagram.com",
    ),

    linkedin_url: clean(
      organization?.linkedin_url,
      "https://linkedin.com",
    ),

    twitter_url: clean(
      organization?.twitter_url,
      "https://twitter.com",
    ),

    youtube_url: clean(
      organization?.youtube_url,
      "https://youtube.com",
    ),

    tiktok_url: clean(
      organization?.tiktok_url,
      "https://tiktok.com",
    ),

    whatsapp_number: clean(
      organization?.whatsapp_number,
      "https://wa.me/",
    ),

    dashboard_url: clean(organization?.website, "https://example.com"),
    current_year: String(new Date().getFullYear()),
  };

  Object.entries(contact?.custom_fields ?? {}).forEach(([key, value]) => {
    context[key] = clean(value);
    context[`contact_${key}`] = clean(value);
  });

  return context;
}

export function contextToJson(context: Record<string, string>) {
  return JSON.stringify(context, null, 2);
}
