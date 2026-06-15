"use client";

import { useState } from "react";

import { Contact, ContactPayload } from "./types";

type ContactTableProps = {
  contacts: Contact[];
  loading: boolean;
  onUpdate: (id: string, payload: Omit<ContactPayload, "email">) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
};

export function ContactTable({
  contacts,
  loading,
  onUpdate,
  onDelete,
}: ContactTableProps) {
  const [editingId, setEditingId] = useState<string | null>(null);

  const [editingFirstName, setEditingFirstName] = useState("");
  const [editingLastName, setEditingLastName] = useState("");
  const [editingPhone, setEditingPhone] = useState("");
  const [editingCompany, setEditingCompany] = useState("");
  const [editingCity, setEditingCity] = useState("");
  const [editingCountry, setEditingCountry] = useState("");
  const [editingSource, setEditingSource] = useState("");
  const [editingNotes, setEditingNotes] = useState("");

  function startEdit(contact: Contact) {
    const metadata = contact.metadata ?? {};

    setEditingId(String(contact.id));
    setEditingFirstName(contact.first_name ?? "");
    setEditingLastName(contact.last_name ?? "");
    setEditingPhone(metadata.phone ?? "");
    setEditingCompany(metadata.company ?? "");
    setEditingCity(metadata.city ?? "");
    setEditingCountry(metadata.country ?? "");
    setEditingSource(metadata.source ?? "");
    setEditingNotes(metadata.notes ?? "");
  }

  async function saveEdit(id: string) {
    await onUpdate(id, {
      first_name: editingFirstName,
      last_name: editingLastName,
      metadata: {
        phone: editingPhone,
        company: editingCompany,
        city: editingCity,
        country: editingCountry,
        source: editingSource,
        notes: editingNotes,
      },
    });

    setEditingId(null);
  }

  return (
    <section className="card">
      <h2>Contact Directory</h2>

      <div className="tableWrap">
        <table className="dataTable">
          <thead>
            <tr>
              <th>Email</th>
              <th>Name</th>
              <th>Phone</th>
              <th>Company</th>
              <th>Location</th>
              <th>Source</th>
              <th>Notes</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {contacts.length === 0 ? (
              <tr>
                <td colSpan={9} className="muted centerText">
                  No contacts found.
                </td>
              </tr>
            ) : (
              contacts.map((contact) => {
                const metadata = contact.metadata ?? {};
                const isEditing = editingId === String(contact.id);

                return (
                  <tr key={String(contact.id)}>
                    <td>{contact.email ?? "-"}</td>

                    <td>
                      {isEditing ? (
                        <div className="grid">
                          <input
                            value={editingFirstName}
                            onChange={(event) =>
                              setEditingFirstName(event.target.value)
                            }
                            placeholder="First name"
                          />

                          <input
                            value={editingLastName}
                            onChange={(event) =>
                              setEditingLastName(event.target.value)
                            }
                            placeholder="Last name"
                          />
                        </div>
                      ) : (
                        `${contact.first_name ?? ""} ${contact.last_name ?? ""}`.trim() ||
                        "-"
                      )}
                    </td>

                    <td>
                      {isEditing ? (
                        <input
                          value={editingPhone}
                          onChange={(event) => setEditingPhone(event.target.value)}
                        />
                      ) : (
                        metadata.phone || "-"
                      )}
                    </td>

                    <td>
                      {isEditing ? (
                        <input
                          value={editingCompany}
                          onChange={(event) => setEditingCompany(event.target.value)}
                        />
                      ) : (
                        metadata.company || "-"
                      )}
                    </td>

                    <td>
                      {isEditing ? (
                        <div className="grid">
                          <input
                            value={editingCity}
                            onChange={(event) => setEditingCity(event.target.value)}
                            placeholder="City"
                          />

                          <input
                            value={editingCountry}
                            onChange={(event) =>
                              setEditingCountry(event.target.value)
                            }
                            placeholder="Country"
                          />
                        </div>
                      ) : (
                        [metadata.city, metadata.country].filter(Boolean).join(", ") ||
                        "-"
                      )}
                    </td>

                    <td>
                      {isEditing ? (
                        <input
                          value={editingSource}
                          onChange={(event) => setEditingSource(event.target.value)}
                        />
                      ) : (
                        metadata.source || "-"
                      )}
                    </td>

                    <td>
                      {isEditing ? (
                        <textarea
                          rows={3}
                          value={editingNotes}
                          onChange={(event) => setEditingNotes(event.target.value)}
                        />
                      ) : (
                        metadata.notes || "-"
                      )}
                    </td>

                    <td>
                      {contact.created_at
                        ? new Date(contact.created_at).toLocaleString()
                        : "-"}
                    </td>

                    <td>
                      <div className="actions">
                        {isEditing ? (
                          <>
                            <button
                              type="button"
                              onClick={() => saveEdit(String(contact.id))}
                              disabled={loading}
                            >
                              Save
                            </button>

                            <button
                              type="button"
                              className="ghostButton"
                              onClick={() => setEditingId(null)}
                            >
                              Cancel
                            </button>
                          </>
                        ) : (
                          <>
                            <button type="button" onClick={() => startEdit(contact)}>
                              Edit
                            </button>

                            <button
                              type="button"
                              className="dangerButton"
                              disabled={loading}
                              onClick={() => onDelete(String(contact.id))}
                            >
                              Delete
                            </button>
                          </>
                        )}
                      </div>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}