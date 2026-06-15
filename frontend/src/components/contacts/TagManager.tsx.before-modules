"use client";

import { FormEvent, useState } from "react";
import { Tag } from "./types";

type Props = {
  tags: Tag[];
  loading: boolean;
  onCreate: (payload: Partial<Tag>) => Promise<void>;
};

export function TagManager({ tags, loading, onCreate }: Props) {
  const [name, setName] = useState("");
  const [tagType, setTagType] = useState("custom");
  const [color, setColor] = useState("#2563eb");
  const [description, setDescription] = useState("");

  function slugify(value: string) {
    return value.toLowerCase().trim().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    await onCreate({
      name,
      slug: slugify(name),
      tag_type: tagType,
      color,
      description,
      is_active: true,
    });

    setName("");
    setTagType("custom");
    setColor("#2563eb");
    setDescription("");
  }

  return (
    <section className="card">
      <h2>Tags</h2>
      <p className="muted">Create lifecycle, source, interest, behavior, campaign, suppression, and custom tags.</p>

      <form className="grid" onSubmit={submit}>
        <div className="cdpGridTwo">
          <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Tag name e.g. Warm Lead" required />

          <select value={tagType} onChange={(e) => setTagType(e.target.value)}>
            <option value="source">Source</option>
            <option value="lifecycle">Lifecycle</option>
            <option value="interest">Interest</option>
            <option value="behavior">Behavior</option>
            <option value="campaign">Campaign</option>
            <option value="suppression">Suppression</option>
            <option value="value">Value</option>
            <option value="geo">Geo</option>
            <option value="custom">Custom</option>
          </select>

          <input type="color" value={color} onChange={(e) => setColor(e.target.value)} />
          <input value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Description" />
        </div>

        <button type="submit" disabled={loading}>Create Tag</button>
      </form>

      <div className="cdpTagGrid">
        {tags.map((tag) => (
          <div key={tag.id} className="cdpTagCard">
            <span className="cdpTagDot" style={{ background: tag.color || "#2563eb" }} />
            <strong>{tag.name}</strong>
            <small>{tag.tag_type}</small>
            <p className="muted small">{tag.description || "No description"}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
