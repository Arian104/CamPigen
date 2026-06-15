"use client";

import { EmailBlock } from "../../types";
import { SettingsGroup, TextField, ColorField, SetProp } from "../../PropertyControls";

export function renderSpacer(block: EmailBlock) {
  const p = block.props;

  return (
    <div style={{ height: `${p.height || "32"}px`, background: p.backgroundColor || "#ffffff" }} />
  );
}

export function SpacerProperties({ block, set }: { block: EmailBlock; set: SetProp }) {
  const p = block.props;

  return (
    <SettingsGroup title="Spacing">
      <TextField label="Height" value={p.height} onChange={(v) => set("height", v)} />
      <ColorField label="Background" value={p.backgroundColor || "#ffffff"} onChange={(v) => set("backgroundColor", v)} />
    </SettingsGroup>
  );
}

export function spacerHtml(block: EmailBlock) {
  const p = block.props;
  return `<div style="height:${p.height || "32"}px; background:${p.backgroundColor || "#ffffff"};"></div>`;
}
