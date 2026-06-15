"use client";

import { FormEvent, useEffect, useState } from "react";

import { Contact, ContactFieldDefinition, ContactPayload } from "./types";
import { DynamicFieldRenderer } from "./DynamicFieldRenderer";

type Props = {
  contact: Contact | null;
  fields: ContactFieldDefinition[];
  loading: boolean;
  onClose: () => void;
  onUpdate: (id: string, payload: ContactPayload) => Promise<void>;
};

export function ContactDrawer({
  contact,
  fields,
  loading,
  onClose,
  onUpdate,
}: Props) {
  const [standard, setStandard] = useState<ContactPayload>({});
  const [customFields, setCustomFields] = useState<
    Record<string, string | number | boolean | string[]>
  >({});

  useEffect(() => {
    if (!contact) return;

    setStandard({
      email: contact.email ?? "",
      first_name: contact.first_name ?? "",
      last_name: contact.last_name ?? "",
      phone: contact.phone ?? "",
      company: contact.company ?? "",
      job_title: contact.job_title ?? "",
      city: contact.city ?? "",
      country: contact.country ?? "",
      source: contact.source ?? "",
      lifecycle_stage: contact.lifecycle_stage ?? "subscriber",
      consent_status: contact.consent_status ?? "unknown",
      lead_score: contact.lead_score ?? 0,
      engagement_score: contact.engagement_score ?? 0,
    });

    setCustomFields(contact.custom_fields ?? {});
  }, [contact]);

  if (!contact) return null;

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

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    await onUpdate(contact.id, {
      ...standard,
      custom_fields: customFields,
    });

    onClose();
  }

  return (
    <div className="cdpDrawerOverlay">
      <aside className="cdpDrawer">
        <div className="cdpDrawerHeader">
          <div>
            <h2>Edit Contact</h2>
            <p className="muted">{contact.email}</p>
          </div>

          <button type="button" className="ghostButton" onClick={onClose}>
            Close
          </button>
        </div>

        <form onSubmit={submit} className="grid">
          <section className="settingsGroup">
            <h4>Profile</h4>

            <div className="cdpGridTwo">
              <input
                type="email"
                value={String(standard.email ?? "")}
                onChange={(e) => setField("email", e.target.value)}
                placeholder="Email"
                required
              />

              <input
                value={String(standard.phone ?? "")}
                onChange={(e) => setField("phone", e.target.value)}
                placeholder="Phone"
              />

              <input
                value={String(standard.first_name ?? "")}
                onChange={(e) => setField("first_name", e.target.value)}
                placeholder="First name"
              />

              <input
                value={String(standard.last_name ?? "")}
                onChange={(e) => setField("last_name", e.target.value)}
                placeholder="Last name"
              />

              <input
                value={String(standard.company ?? "")}
                onChange={(e) => setField("company", e.target.value)}
                placeholder="Company"
              />

              <input
                value={String(standard.job_title ?? "")}
                onChange={(e) => setField("job_title", e.target.value)}
                placeholder="Job title"
              />

              <input
                value={String(standard.city ?? "")}
                onChange={(e) => setField("city", e.target.value)}
                placeholder="City"
              />

              <input
                value={String(standard.country ?? "")}
                onChange={(e) => setField("country", e.target.value)}
                placeholder="Country"
              />

              <input
                value={String(standard.source ?? "")}
                onChange={(e) => setField("source", e.target.value)}
                placeholder="Source"
              />

              <select
                value={String(standard.lifecycle_stage ?? "subscriber")}
                onChange={(e) => setField("lifecycle_stage", e.target.value)}
              >
                <option value="subscriber">Subscriber</option>
                <option value="lead_new">New Lead</option>
                <option value="lead_warm">Warm Lead</option>
                <option value="lead_hot">Hot Lead</option>
                <option value="customer">Customer</option>
                <option value="inactive">Inactive</option>
                <option value="churn_risk">Churn Risk</option>
              </select>

              <select
                value={String(standard.consent_status ?? "unknown")}
                onChange={(e) => setField("consent_status", e.target.value)}
              >
                <option value="unknown">Unknown</option>
                <option value="subscribed">Subscribed</option>
                <option value="unsubscribed">Unsubscribed</option>
                <option value="bounced">Bounced</option>
                <option value="complained">Complained</option>
                <option value="suppressed">Suppressed</option>
              </select>

              <input
                type="number"
                value={Number(standard.lead_score ?? 0)}
                onChange={(e) => setField("lead_score", Number(e.target.value))}
                placeholder="Lead score"
              />

              <input
                type="number"
                value={Number(standard.engagement_score ?? 0)}
                onChange={(e) => setField("engagement_score", Number(e.target.value))}
                placeholder="Engagement score"
              />
            </div>
          </section>

          <section className="settingsGroup">
            <h4>Custom Fields</h4>

            {fields.length === 0 ? (
              <p className="muted">No custom fields created yet.</p>
            ) : (
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
            )}
          </section>

          <section className="settingsGroup">
            <h4>Current Tags</h4>
            <div className="cdpTags">
              {contact.tag_names?.length ? (
                contact.tag_names.map((tag) => <span key={tag}>{tag}</span>)
              ) : (
                <p className="muted">No tags applied.</p>
              )}
            </div>
          </section>

          <div className="actions">
            <button type="submit" disabled={loading}>
              Save Contact
            </button>

            <button type="button" className="ghostButton" onClick={onClose}>
              Cancel
            </button>
          </div>
        </form>
      </aside>
    </div>
  );
}
