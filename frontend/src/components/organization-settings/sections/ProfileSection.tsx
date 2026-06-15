"use client";

import { Field } from "../FormControls";
import { Organization, UpdateOrganizationField } from "../types";

export function ProfileSection({
  organization,
  updateField,
}: {
  organization: Organization;
  updateField: UpdateOrganizationField;
}) {
  return (
    <div>
      <h2>Profile</h2>

      <div className="formGrid">
        <Field label="Organization Name">
          <input value={organization.name} onChange={(e) => updateField("name", e.target.value)} />
        </Field>

        <Field label="Subdomain">
          <input value={organization.subdomain} disabled />
        </Field>

        <Field label="Industry">
          <select value={organization.industry_type} onChange={(e) => updateField("industry_type", e.target.value)}>
            <option value="custom">Custom</option>
            <option value="restaurant">Restaurant</option>
            <option value="cafe">Cafe</option>
            <option value="gym">Gym</option>
            <option value="education">Education</option>
            <option value="visa_consultant">Visa Consultant</option>
            <option value="ecommerce">Ecommerce</option>
            <option value="online_course">Online Course</option>
            <option value="agency">Agency</option>
            <option value="saas">SaaS</option>
          </select>
        </Field>

        <Field label="Website">
          <input value={organization.website} onChange={(e) => updateField("website", e.target.value)} />
        </Field>

        <Field label="Country">
          <input value={organization.country} onChange={(e) => updateField("country", e.target.value)} />
        </Field>

        <Field label="Timezone">
          <input value={organization.timezone} onChange={(e) => updateField("timezone", e.target.value)} />
        </Field>
      </div>
    </div>
  );
}
