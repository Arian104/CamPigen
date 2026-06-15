"use client";

import { FormEvent, useState } from "react";
import { ContactFieldDefinition } from "./types";

type Props = {
  fields: ContactFieldDefinition[];
  loading: boolean;
  onCreate: (payload: Partial<ContactFieldDefinition>) => Promise<void>;
};

export function FieldManager({ fields, loading, onCreate }: Props) {
  const [label, setLabel] = useState("");
  const [fieldKey, setFieldKey] = useState("");
  const [fieldType, setFieldType] = useState<ContactFieldDefinition["field_type"]>("text");
  const [optionsText, setOptionsText] = useState("");
  const [isVisible, setIsVisible] = useState(true);
  const [isFilterable, setIsFilterable] = useState(true);
  const [isRequired, setIsRequired] = useState(false);

  function autoKey(value: string) {
    return value.toLowerCase().trim().replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "");
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    await onCreate({
      label,
      field_key: fieldKey || autoKey(label),
      field_type: fieldType,
      options: optionsText
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean),
      is_visible_in_table: isVisible,
      is_filterable: isFilterable,
      is_required: isRequired,
      is_importable: true,
      is_active: true,
      order: fields.length + 1,
    });

    setLabel("");
    setFieldKey("");
    setFieldType("text");
    setOptionsText("");
    setIsVisible(true);
    setIsFilterable(true);
    setIsRequired(false);
  }

  return (
    <section className="card">
      <h2>Custom Fields</h2>
      <p className="muted">
        Create organization-specific fields for cafe, gym, education, visa consulting, ecommerce, or any business type.
      </p>

      <form className="grid" onSubmit={submit}>
        <div className="cdpGridTwo">
          <input value={label} onChange={(e) => setLabel(e.target.value)} placeholder="Label e.g. HSC Batch" required />
          <input value={fieldKey} onChange={(e) => setFieldKey(autoKey(e.target.value))} placeholder="Field key e.g. hsc_batch" />

          <select value={fieldType} onChange={(e) => setFieldType(e.target.value as ContactFieldDefinition["field_type"])}>
            <option value="text">Text</option>
            <option value="textarea">Textarea</option>
            <option value="number">Number</option>
            <option value="decimal">Decimal</option>
            <option value="date">Date</option>
            <option value="datetime">DateTime</option>
            <option value="boolean">Boolean</option>
            <option value="select">Select</option>
            <option value="multi_select">Multi Select</option>
            <option value="email">Email</option>
            <option value="phone">Phone</option>
            <option value="url">URL</option>
          </select>

          <input
            value={optionsText}
            onChange={(e) => setOptionsText(e.target.value)}
            placeholder="Options for select: Canada, USA, UK"
          />
        </div>

        <div className="cdpCheckGrid">
          <label><input type="checkbox" checked={isVisible} onChange={(e) => setIsVisible(e.target.checked)} /> Visible in table</label>
          <label><input type="checkbox" checked={isFilterable} onChange={(e) => setIsFilterable(e.target.checked)} /> Filterable</label>
          <label><input type="checkbox" checked={isRequired} onChange={(e) => setIsRequired(e.target.checked)} /> Required</label>
        </div>

        <button type="submit" disabled={loading}>Create Field</button>
      </form>

      <div className="tableWrap">
        <table className="dataTable">
          <thead>
            <tr>
              <th>Label</th>
              <th>Key</th>
              <th>Type</th>
              <th>Visible</th>
              <th>Filterable</th>
            </tr>
          </thead>

          <tbody>
            {fields.length === 0 ? (
              <tr><td colSpan={5} className="centerText muted">No fields created.</td></tr>
            ) : (
              fields.map((field) => (
                <tr key={field.id}>
                  <td>{field.label}</td>
                  <td>{field.field_key}</td>
                  <td>{field.field_type}</td>
                  <td>{field.is_visible_in_table ? "Yes" : "No"}</td>
                  <td>{field.is_filterable ? "Yes" : "No"}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
