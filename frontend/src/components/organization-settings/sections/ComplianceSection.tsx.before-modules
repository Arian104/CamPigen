"use client";

import { Field, Toggle } from "../FormControls";
import { Organization, UpdateOrganizationField } from "../types";

export function ComplianceSection({
  organization,
  updateField,
}: {
  organization: Organization;
  updateField: UpdateOrganizationField;
}) {
  return (
    <div>
      <h2>Compliance</h2>

      <div className="formGrid">
        <Field label="Legal Company Name">
          <input value={organization.company_legal_name} onChange={(e) => updateField("company_legal_name", e.target.value)} />
        </Field>

        <Field label="Support Email">
          <input value={organization.support_email} onChange={(e) => updateField("support_email", e.target.value)} />
        </Field>

        <Field label="Business Phone">
          <input value={organization.business_phone} onChange={(e) => updateField("business_phone", e.target.value)} />
        </Field>

        <Field label="City">
          <input value={organization.city} onChange={(e) => updateField("city", e.target.value)} />
        </Field>

        <Field label="State">
          <input value={organization.state} onChange={(e) => updateField("state", e.target.value)} />
        </Field>

        <Field label="Postal Code">
          <input value={organization.postal_code} onChange={(e) => updateField("postal_code", e.target.value)} />
        </Field>

        <Field label="Unsubscribe Policy">
          <select value={organization.unsubscribe_policy} onChange={(e) => updateField("unsubscribe_policy", e.target.value)}>
            <option value="one_click">One Click</option>
            <option value="confirmation">Confirmation Page</option>
            <option value="preference_center">Preference Center</option>
          </select>
        </Field>

        <Field label="Physical Address Required">
          <Toggle checked={organization.physical_address_required} onChange={(value) => updateField("physical_address_required", value)} />
        </Field>

        <Field label="GDPR Enabled">
          <Toggle checked={organization.gdpr_enabled} onChange={(value) => updateField("gdpr_enabled", value)} />
        </Field>

        <Field label="Double Opt-In">
          <Toggle checked={organization.double_opt_in_enabled} onChange={(value) => updateField("double_opt_in_enabled", value)} />
        </Field>

        <Field label="Marketing Consent Required">
          <Toggle checked={organization.marketing_consent_required} onChange={(value) => updateField("marketing_consent_required", value)} />
        </Field>
      </div>

      <Field label="Business Address">
        <textarea value={organization.business_address} onChange={(e) => updateField("business_address", e.target.value)} />
      </Field>
    </div>
  );
}
