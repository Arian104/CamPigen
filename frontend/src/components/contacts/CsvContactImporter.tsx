"use client";

import { ChangeEvent, useMemo, useState } from "react";

import { ContactFieldDefinition, ContactPayload, Tag, ContactList } from "./types";

type Props = {
  loading: boolean;
  fields: ContactFieldDefinition[];
  tags: Tag[];
  lists: ContactList[];
  onImport: (contacts: ContactPayload[], tagIds: string[], listId?: string) => Promise<void>;
};

type Mapping = Record<string, string>;

const STANDARD_FIELDS = [
  "email",
  "first_name",
  "last_name",
  "phone",
  "company",
  "job_title",
  "city",
  "country",
  "source",
];

function parseCsvLine(line: string): string[] {
  const values: string[] = [];
  let current = "";
  let insideQuotes = false;

  for (let i = 0; i < line.length; i += 1) {
    const char = line[i];
    const nextChar = line[i + 1];

    if (char === '"' && insideQuotes && nextChar === '"') {
      current += '"';
      i += 1;
    } else if (char === '"') {
      insideQuotes = !insideQuotes;
    } else if (char === "," && !insideQuotes) {
      values.push(current.trim());
      current = "";
    } else {
      current += char;
    }
  }

  values.push(current.trim());
  return values;
}

function parseCsv(text: string): Record<string, string>[] {
  const lines = text.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  if (lines.length < 2) return [];

  const headers = parseCsvLine(lines[0]);

  return lines.slice(1).map((line) => {
    const values = parseCsvLine(line);
    const row: Record<string, string> = {};
    headers.forEach((header, index) => {
      row[header] = values[index] ?? "";
    });
    return row;
  });
}

export function CsvContactImporter({ loading, fields, tags, lists, onImport }: Props) {
  const [headers, setHeaders] = useState<string[]>([]);
  const [rows, setRows] = useState<Record<string, string>[]>([]);
  const [mapping, setMapping] = useState<Mapping>({});
  const [tagId, setTagId] = useState("");
  const [listId, setListId] = useState("");
  const [message, setMessage] = useState("Upload a CSV and map columns.");

  const previewRows = useMemo(() => rows.slice(0, 5), [rows]);

  async function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;

    const text = await file.text();
    const parsedRows = parseCsv(text);

    if (parsedRows.length === 0) {
      setHeaders([]);
      setRows([]);
      setMapping({});
      setMessage("No valid rows found.");
      return;
    }

    const parsedHeaders = Object.keys(parsedRows[0]);
    setHeaders(parsedHeaders);
    setRows(parsedRows);

    const guessed: Mapping = {};
    [...STANDARD_FIELDS, ...fields.map((field) => `custom:${field.field_key}`)].forEach((fieldKey) => {
      const cleanKey = fieldKey.replace("custom:", "");
      const match = parsedHeaders.find((header) => header.toLowerCase().replace(/\s+/g, "_") === cleanKey);
      if (match) guessed[fieldKey] = match;
    });

    setMapping(guessed);
    setMessage(`Loaded ${parsedRows.length} rows.`);
  }

  function updateMapping(field: string, csvColumn: string) {
    setMapping((current) => ({
      ...current,
      [field]: csvColumn,
    }));
  }

  function get(row: Record<string, string>, csvColumn?: string) {
    if (!csvColumn) return "";
    return row[csvColumn] ?? "";
  }

  async function submitImport() {
    if (!mapping.email) {
      setMessage("Email column is required.");
      return;
    }

    const contacts: ContactPayload[] = rows
      .map((row) => {
        const custom_fields: Record<string, string> = {};

        fields.forEach((field) => {
          const column = mapping[`custom:${field.field_key}`];
          if (column) custom_fields[field.field_key] = get(row, column);
        });

        return {
          email: get(row, mapping.email),
          first_name: get(row, mapping.first_name),
          last_name: get(row, mapping.last_name),
          phone: get(row, mapping.phone),
          company: get(row, mapping.company),
          job_title: get(row, mapping.job_title),
          city: get(row, mapping.city),
          country: get(row, mapping.country),
          source: get(row, mapping.source) || "csv",
          custom_fields,
        };
      })
      .filter((contact) => contact.email);

    await onImport(contacts, tagId ? [tagId] : [], listId || undefined);
    setMessage(`Submitted ${contacts.length} contacts.`);
  }

  function renderSelect(label: string, fieldKey: string, required = false) {
    return (
      <label>
        {label}{required ? " *" : ""}
        <select value={mapping[fieldKey] ?? ""} onChange={(e) => updateMapping(fieldKey, e.target.value)}>
          <option value="">Do not import</option>
          {headers.map((header) => (
            <option key={`${fieldKey}-${header}`} value={header}>{header}</option>
          ))}
        </select>
      </label>
    );
  }

  return (
    <section className="card">
      <h2>CSV Import</h2>
      <p className="muted">Map any CSV format to standard fields, custom fields, tags, and lists.</p>

      <input type="file" accept=".csv" onChange={handleFileChange} disabled={loading} />
      <p className="muted">{message}</p>

      {headers.length > 0 ? (
        <>
          <div className="cdpGridTwo">
            {renderSelect("Email", "email", true)}
            {renderSelect("First name", "first_name")}
            {renderSelect("Last name", "last_name")}
            {renderSelect("Phone", "phone")}
            {renderSelect("Company", "company")}
            {renderSelect("Job title", "job_title")}
            {renderSelect("City", "city")}
            {renderSelect("Country", "country")}
            {renderSelect("Source", "source")}

            {fields.map((field) => renderSelect(`Custom: ${field.label}`, `custom:${field.field_key}`))}

            <label>
              Apply tag
              <select value={tagId} onChange={(e) => setTagId(e.target.value)}>
                <option value="">No tag</option>
                {tags.map((tag) => (
                  <option key={tag.id} value={tag.id}>{tag.name}</option>
                ))}
              </select>
            </label>

            <label>
              Add to list
              <select value={listId} onChange={(e) => setListId(e.target.value)}>
                <option value="">No list</option>
                {lists.map((list) => (
                  <option key={list.id} value={list.id}>{list.name}</option>
                ))}
              </select>
            </label>
          </div>

          <button type="button" disabled={loading} onClick={submitImport}>
            Import Contacts
          </button>

          <h3>Preview</h3>

          <div className="tableWrap">
            <table className="dataTable">
              <thead>
                <tr>{headers.map((header) => <th key={header}>{header}</th>)}</tr>
              </thead>
              <tbody>
                {previewRows.map((row, index) => (
                  <tr key={index}>
                    {headers.map((header) => <td key={header}>{row[header] || "-"}</td>)}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      ) : null}
    </section>
  );
}
