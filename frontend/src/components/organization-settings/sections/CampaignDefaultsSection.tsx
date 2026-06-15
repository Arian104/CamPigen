"use client";

import { Field, Toggle } from "../FormControls";
import { Organization, UpdateOrganizationField } from "../types";

export function CampaignDefaultsSection({
  organization,
  updateField,
}: {
  organization: Organization;
  updateField: UpdateOrganizationField;
}) {
  return (
    <div>
      <h2>Campaign Defaults</h2>

      <div className="formGrid">
        <Field label="Default From Name">
          <input value={organization.default_from_name} onChange={(e) => updateField("default_from_name", e.target.value)} />
        </Field>

        <Field label="Default From Email">
          <input value={organization.default_from_email} onChange={(e) => updateField("default_from_email", e.target.value)} />
        </Field>

        <Field label="Default Reply-To Email">
          <input value={organization.default_reply_to_email} onChange={(e) => updateField("default_reply_to_email", e.target.value)} />
        </Field>

        <Field label="Language">
          <input value={organization.default_campaign_language} onChange={(e) => updateField("default_campaign_language", e.target.value)} />
        </Field>

        <Field label="Template Width">
          <input
            type="number"
            value={organization.default_template_width}
            onChange={(e) => updateField("default_template_width", Number(e.target.value))}
          />
        </Field>

        <Field label="Header Logo">
          <Toggle checked={organization.default_header_logo_enabled} onChange={(value) => updateField("default_header_logo_enabled", value)} />
        </Field>

        <Field label="Footer Enabled">
          <Toggle checked={organization.default_footer_enabled} onChange={(value) => updateField("default_footer_enabled", value)} />
        </Field>
      </div>

      <Field label="Default Footer Text">
        <textarea value={organization.default_footer_text} onChange={(e) => updateField("default_footer_text", e.target.value)} />
      </Field>

      <Field label="Default Disclaimer">
        <textarea value={organization.default_disclaimer} onChange={(e) => updateField("default_disclaimer", e.target.value)} />
      </Field>
    </div>
  );
}
