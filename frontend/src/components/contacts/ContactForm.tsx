"use client";

import { FormEvent, useState } from "react";

import { ContactFieldDefinition, ContactPayload } from "./types";
import { DynamicFieldRenderer } from "./DynamicFieldRenderer";

type Props = {
  loading: boolean;
  fields: ContactFieldDefinition[];
  onCreate: (payload: ContactPayload) => Promise<void>;
};

export function ContactForm({ loading, fields, onCreate }: Props) {
  const [standard, setStandard] = useState<ContactPayload>({
    email: "",
    first_name: "",
    last_name: "",
    phone: "",
    company: "",
    job_title: "",
    city: "",
    country: "",
    source: "",
    lifecycle_stage: "subscriber",
    consent_status: "unknown",
    lead_score: 0,
    engagement_score: 0,
  });

  const [customFields, setCustomFields] = useState<Record<string, string | number | boolean | string[]>>({});

  function setField(key: keyof ContactPayload, value: string | number | boolean) {
    setStandard((current) => ({
      ...current,
      [key]: value,
    }));
  }

  function setCustomField(key: string, value: string | number | boolean | string[]) {
    setCustomFields((current) => ({
      ...current,
      [key]: value,
    }));
  }

  function resetForm() {
    setStandard({
      email: "",
      first_name: "",
      last_name: "",
      phone: "",
      company: "",
      job_title: "",
      city: "",
      country: "",
      source: "",
      lifecycle_stage: "subscriber",
      consent_status: "unknown",
      lead_score: 0,
      engagement_score: 0,
    });
    setCustomFields({});
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    await onCreate({
      ...standard,
      custom_fields: customFields,
      metadata: {
        source: String(standard.source ?? ""),
      },
    });

    resetForm();
  }

  return (
    <section className="card">
      <h2>Create Contact</h2>
      <p className="muted">
        Add standard profile data and organization-specific custom fields.
      </p>

      <form onSubmit={handleSubmit} className="grid">
        <div className="cdpGridTwo">
          <input
            type="email"
            value={String(standard.email ?? "")}
            onChange={(event) => setField("email", event.target.value)}
            placeholder="Email"
            required
          />

          <input
            value={String(standard.phone ?? "")}
            onChange={(event) => setField("phone", event.target.value)}
            placeholder="Phone"
          />

          <input
            value={String(standard.first_name ?? "")}
            onChange={(event) => setField("first_name", event.target.value)}
            placeholder="First name"
          />

          <input
            value={String(standard.last_name ?? "")}
            onChange={(event) => setField("last_name", event.target.value)}
            placeholder="Last name"
          />

          <input
            value={String(standard.company ?? "")}
            onChange={(event) => setField("company", event.target.value)}
            placeholder="Company"
          />

          <input
            value={String(standard.job_title ?? "")}
            onChange={(event) => setField("job_title", event.target.value)}
            placeholder="Job title"
          />

          <input
            value={String(standard.city ?? "")}
            onChange={(event) => setField("city", event.target.value)}
            placeholder="City"
          />

          <input
            value={String(standard.country ?? "")}
            onChange={(event) => setField("country", event.target.value)}
            placeholder="Country"
          />

          <input
            value={String(standard.source ?? "")}
            onChange={(event) => setField("source", event.target.value)}
            placeholder="Source"
          />

          <select
            value={String(standard.lifecycle_stage ?? "subscriber")}
            onChange={(event) => setField("lifecycle_stage", event.target.value)}
          >
            <option value="subscriber">Subscriber</option>
            <option value="lead_new">New Lead</option>
            <option value="lead_warm">Warm Lead</option>
            <option value="lead_hot">Hot Lead</option>
            <option value="customer">Customer</option>
            <option value="inactive">Inactive</option>
            <option value="churn_risk">Churn Risk</option>
          </select>
        </div>

        {fields.length > 0 ? (
          <>
            <h3>Custom Fields</h3>
            <div className="cdpGridTwo">
              {fields
                .filter((field) => field.is_active !== false)
                .map((field) => (
                  <DynamicFieldRenderer
                    key={field.id}
                    field={field}
                    value={customFields[field.field_key]}
                    onChange={setCustomField}
                  />
                ))}
            </div>
          </>
        ) : (
          <p className="muted">No custom fields yet. Create fields from the Fields tab.</p>
        )}

        <button type="submit" disabled={loading}>
          Create Contact
        </button>
      </form>
    </section>
  );
}
