"use client";

import { FormEvent, useState } from "react";
import { ContactList, Tag, ContactFieldDefinition } from "./types";

type Props = {
  lists: ContactList[];
  tags: Tag[];
  fields: ContactFieldDefinition[];
  loading: boolean;
  onCreate: (payload: Partial<ContactList>) => Promise<void>;
};

export function ListManager({ lists, tags, fields, loading, onCreate }: Props) {
  const [name, setName] = useState("");
  const [listType, setListType] = useState<ContactList["list_type"]>("static");
  const [description, setDescription] = useState("");
  const [includeTag, setIncludeTag] = useState("");
  const [customKey, setCustomKey] = useState("");
  const [customValue, setCustomValue] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    await onCreate({
      name,
      list_type: listType,
      description,
      filter_criteria:
        listType === "dynamic"
          ? {
              include_tags: includeTag ? [includeTag] : [],
              custom_fields: customKey && customValue ? { [customKey]: customValue } : {},
              exclude_unsubscribed: true,
            }
          : {},
      is_active: true,
    });

    setName("");
    setListType("static");
    setDescription("");
    setIncludeTag("");
    setCustomKey("");
    setCustomValue("");
  }

  return (
    <section className="card">
      <h2>Lists & Segments</h2>
      <p className="muted">Create static lists, dynamic segments, suppression lists, and seed lists.</p>

      <form className="grid" onSubmit={submit}>
        <div className="cdpGridTwo">
          <input value={name} onChange={(e) => setName(e.target.value)} placeholder="List or segment name" required />

          <select value={listType} onChange={(e) => setListType(e.target.value as ContactList["list_type"])}>
            <option value="static">Static List</option>
            <option value="dynamic">Dynamic Segment</option>
            <option value="suppression">Suppression List</option>
            <option value="seed">Seed List</option>
          </select>

          <input value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Description" />

          {listType === "dynamic" ? (
            <>
              <select value={includeTag} onChange={(e) => setIncludeTag(e.target.value)}>
                <option value="">Include tag</option>
                {tags.map((tag) => (
                  <option key={tag.id} value={tag.id}>{tag.name}</option>
                ))}
              </select>

              <select value={customKey} onChange={(e) => setCustomKey(e.target.value)}>
                <option value="">Custom field rule</option>
                {fields.filter((field) => field.is_filterable).map((field) => (
                  <option key={field.id} value={field.field_key}>{field.label}</option>
                ))}
              </select>

              <input value={customValue} onChange={(e) => setCustomValue(e.target.value)} placeholder="Custom field value" />
            </>
          ) : null}
        </div>

        <button type="submit" disabled={loading}>Create List / Segment</button>
      </form>

      <div className="tableWrap">
        <table className="dataTable">
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Total</th>
              <th>Description</th>
            </tr>
          </thead>

          <tbody>
            {lists.length === 0 ? (
              <tr><td colSpan={4} className="centerText muted">No lists created.</td></tr>
            ) : (
              lists.map((list) => (
                <tr key={list.id}>
                  <td>{list.name}</td>
                  <td>{list.list_type}</td>
                  <td>{list.contact_count ?? list.total_contacts ?? 0}</td>
                  <td>{list.description || "-"}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
