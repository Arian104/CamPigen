"use client";

import { Contact, ContactFieldDefinition, Tag } from "./types";

type Props = {
  contacts: Contact[];
  fields: ContactFieldDefinition[];
  tags: Tag[];
  selectedIds: string[];
  onToggleSelect: (id: string) => void;
  onOpenContact: (contact: Contact) => void;
  onDelete: (id: string) => Promise<void>;
  loading: boolean;
};

export function ContactDirectory({
  contacts,
  fields,
  tags,
  selectedIds,
  onToggleSelect,
  onOpenContact,
  onDelete,
  loading,
}: Props) {
  const visibleFields = fields.filter((field) => field.is_visible_in_table);

  function tagName(id: string) {
    return tags.find((tag) => tag.id === id)?.name ?? id;
  }

  return (
    <section className="card">
      <div className="flexBetween">
        <div>
          <h2>Contact Directory</h2>
          <p className="muted">{contacts.length} contacts loaded.</p>
        </div>
      </div>

      <div className="cdpContactGrid">
        {contacts.length === 0 ? (
          <div className="emptyCanvas">No contacts found.</div>
        ) : (
          contacts.map((contact) => (
            <article key={contact.id} className="cdpContactCard">
              <div className="cdpContactTop">
                <input
                  type="checkbox"
                  checked={selectedIds.includes(contact.id)}
                  onChange={() => onToggleSelect(contact.id)}
                />

                <div className="cdpAvatar">
                  {(contact.first_name?.[0] || contact.email?.[0] || "C").toUpperCase()}
                </div>

                <div>
                  <strong>{contact.full_name || `${contact.first_name ?? ""} ${contact.last_name ?? ""}`.trim() || "Unnamed Contact"}</strong>
                  <p className="muted small">{contact.email}</p>
                </div>
              </div>

              <div className="cdpContactMeta">
                <span>{contact.lifecycle_stage || "subscriber"}</span>
                <span>Lead {contact.lead_score ?? 0}</span>
                <span>Eng {contact.engagement_score ?? 0}</span>
              </div>

              <div className="cdpMiniInfo">
                <p><strong>Company:</strong> {contact.company || "-"}</p>
                <p><strong>Location:</strong> {[contact.city, contact.country].filter(Boolean).join(", ") || "-"}</p>
                <p><strong>Source:</strong> {contact.source || "-"}</p>
              </div>

              {visibleFields.length > 0 ? (
                <div className="cdpCustomPreview">
                  {visibleFields.slice(0, 4).map((field) => (
                    <span key={field.id}>
                      {field.label}: {String(contact.custom_fields?.[field.field_key] ?? "-")}
                    </span>
                  ))}
                </div>
              ) : null}

              {contact.tag_ids?.length ? (
                <div className="cdpTags">
                  {contact.tag_ids.slice(0, 5).map((id) => (
                    <span key={id}>{tagName(id)}</span>
                  ))}
                </div>
              ) : null}

              <div className="actions">
                <button type="button" className="secondaryButton" onClick={() => onOpenContact(contact)}>
                  View / Edit
                </button>

                <button
                  type="button"
                  className="dangerButton"
                  disabled={loading}
                  onClick={() => onDelete(contact.id)}
                >
                  Delete
                </button>
              </div>
            </article>
          ))
        )}
      </div>
    </section>
  );
}
