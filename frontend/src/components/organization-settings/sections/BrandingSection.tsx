"use client";

import { Field } from "../FormControls";
import { Organization, UpdateOrganizationField } from "../types";

export function BrandingSection({
  organization,
  updateField,
}: {
  organization: Organization;
  updateField: UpdateOrganizationField;
}) {
  return (
    <div>
      <h2>Branding</h2>

      <div className="brandPreview">
        <div className="brandPreviewLogo" style={{ background: organization.primary_color }}>
          {organization.logo_url ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={organization.logo_url} alt="Logo" />
          ) : (
            <span>{(organization.brand_name || organization.name || "EP").slice(0, 2).toUpperCase()}</span>
          )}
        </div>

        <div>
          <strong>{organization.brand_name || organization.name}</strong>
          <p className="muted">Brand preview for campaign templates and public pages.</p>
        </div>
      </div>

      <div className="formGrid">
        <Field label="Brand Name">
          <input value={organization.brand_name} onChange={(e) => updateField("brand_name", e.target.value)} />
        </Field>

        <Field label="Primary Color">
          <input value={organization.primary_color} onChange={(e) => updateField("primary_color", e.target.value)} />
        </Field>

        <Field label="Secondary Color">
          <input value={organization.secondary_color} onChange={(e) => updateField("secondary_color", e.target.value)} />
        </Field>

        <Field label="Accent Color">
          <input value={organization.accent_color} onChange={(e) => updateField("accent_color", e.target.value)} />
        </Field>

        <Field label="Font Family">
          <input value={organization.font_family} onChange={(e) => updateField("font_family", e.target.value)} />
        </Field>

        <Field label="Button Style">
          <select value={organization.button_style} onChange={(e) => updateField("button_style", e.target.value)}>
            <option value="rounded">Rounded</option>
            <option value="pill">Pill</option>
            <option value="sharp">Sharp</option>
          </select>
        </Field>
      </div>

      <p className="muted smallNote">
        Logo upload UI can be added after backend media serving is finalized.
      </p>
    </div>
  );
}
