"use client";

import { EmailBlock } from "../../types";
import { SettingsGroup, ColorField, SetProp } from "../../PropertyControls";

export function renderDivider(block: EmailBlock) {
  const p = block.props;
  return <div className="emailDividerBlock" style={{ background: p.lineColor || "#e5e7eb" }} />;
}

export function DividerProperties({ block, set }: { block: EmailBlock; set: SetProp }) {
  const p = block.props;

  return (
    <SettingsGroup title="Divider">
      <ColorField label="Line Color" value={p.lineColor || "#e5e7eb"} onChange={(v) => set("lineColor", v)} />
      <ColorField label="Background" value={p.backgroundColor || "#ffffff"} onChange={(v) => set("backgroundColor", v)} />
    </SettingsGroup>
  );
}

export function dividerHtml(block: EmailBlock) {
  const p = block.props;
  return `<hr style="border:0; border-top:1px solid ${p.lineColor || "#e5e7eb"};" />`;
}
