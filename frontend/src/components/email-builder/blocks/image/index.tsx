"use client";

import { EmailBlock } from "../../types";
import { SettingsGroup, TextField, ColorField, SetProp } from "../../PropertyControls";

export function renderImage(block: EmailBlock) {
  const p = block.props;

  return (
    <div className="emailImageBlock" style={{ background: p.backgroundColor || "#ffffff" }}>
      {p.src ? <img src={p.src} alt={p.alt || ""} /> : <span>Image URL missing</span>}
    </div>
  );
}

export function ImageProperties({ block, set }: { block: EmailBlock; set: SetProp }) {
  const p = block.props;

  return (
    <SettingsGroup title="Image">
      <TextField label="Image URL" value={p.src} onChange={(v) => set("src", v)} />
      <TextField label="Alt Text" value={p.alt} onChange={(v) => set("alt", v)} />
      <ColorField label="Background" value={p.backgroundColor || "#ffffff"} onChange={(v) => set("backgroundColor", v)} />
    </SettingsGroup>
  );
}

export function imageHtml(block: EmailBlock) {
  const p = block.props;

  return `
    <div style="background:${p.backgroundColor || "#ffffff"}; text-align:center; padding:16px; border-radius:14px;">
      <img src="${p.src || ""}" alt="${p.alt || ""}" style="max-width:100%; border-radius:14px; display:block; margin:0 auto;" />
    </div>
  `;
}
