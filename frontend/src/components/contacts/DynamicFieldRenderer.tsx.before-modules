"use client";

import { ContactFieldDefinition } from "./types";

type Props = {
  field: ContactFieldDefinition;
  value: unknown;
  onChange: (key: string, value: string | number | boolean | string[]) => void;
};

export function DynamicFieldRenderer({ field, value, onChange }: Props) {
  const key = field.field_key;
  const stringValue = typeof value === "string" || typeof value === "number" ? String(value) : "";

  if (field.field_type === "textarea") {
    return (
      <label>
        {field.label}
        <textarea
          rows={4}
          value={stringValue}
          placeholder={field.placeholder || field.label}
          onChange={(event) => onChange(key, event.target.value)}
        />
      </label>
    );
  }

  if (field.field_type === "number" || field.field_type === "decimal") {
    return (
      <label>
        {field.label}
        <input
          type="number"
          value={stringValue}
          placeholder={field.placeholder || field.label}
          onChange={(event) => onChange(key, Number(event.target.value))}
        />
      </label>
    );
  }

  if (field.field_type === "date" || field.field_type === "datetime") {
    return (
      <label>
        {field.label}
        <input
          type={field.field_type === "datetime" ? "datetime-local" : "date"}
          value={stringValue}
          onChange={(event) => onChange(key, event.target.value)}
        />
      </label>
    );
  }

  if (field.field_type === "boolean") {
    return (
      <label className="checkboxRow">
        <input
          type="checkbox"
          checked={Boolean(value)}
          onChange={(event) => onChange(key, event.target.checked)}
        />
        <span>{field.label}</span>
      </label>
    );
  }

  if (field.field_type === "select") {
    return (
      <label>
        {field.label}
        <select value={stringValue} onChange={(event) => onChange(key, event.target.value)}>
          <option value="">Select {field.label}</option>
          {(field.options ?? []).map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      </label>
    );
  }

  if (field.field_type === "multi_select") {
    const values = Array.isArray(value) ? value.map(String) : [];

    return (
      <label>
        {field.label}
        <select
          multiple
          value={values}
          onChange={(event) =>
            onChange(
              key,
              Array.from(event.target.selectedOptions).map((option) => option.value),
            )
          }
        >
          {(field.options ?? []).map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      </label>
    );
  }

  return (
    <label>
      {field.label}
      <input
        type={field.field_type === "email" ? "email" : field.field_type === "url" ? "url" : "text"}
        value={stringValue}
        placeholder={field.placeholder || field.label}
        required={field.is_required}
        onChange={(event) => onChange(key, event.target.value)}
      />
      {field.help_text ? <span className="muted small">{field.help_text}</span> : null}
    </label>
  );
}
