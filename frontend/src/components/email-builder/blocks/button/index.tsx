"use client";

import { EmailBlock } from "../../types";
import { font, px, htmlFont, htmlSize } from "../../blockUtils";
import { SettingsGroup, TextField, TextStyleControls, ColorField, SetProp } from "../../PropertyControls";

export function renderButton(block: EmailBlock) {
  const p = block.props;

  return (
    <div className="emailButtonBlock" style={{ background: "#ffffff" }}>
      <span style={{ background: p.backgroundColor || "#2563eb", color: p.textColor || "#ffffff", fontFamily: font(p.buttonFontFamily), fontSize: px(p.buttonFontSize, "14") }}>
        {p.text}
      </span>
    </div>
  );
}

export function ButtonProperties({ block, set }: { block: EmailBlock; set: SetProp }) {
  const p = block.props;

  return (
    <SettingsGroup title="Button">
      <TextField label="Text" value={p.text} onChange={(v) => set("text", v)} />
      <TextField label="URL" value={p.url} onChange={(v) => set("url", v)} />
      <TextStyleControls block={block} prefix="Text" colorKey="textColor" fontKey="buttonFontFamily" sizeKey="buttonFontSize" defaultColor="#ffffff" defaultSize="14" set={set} />
      <ColorField label="Background" value={p.backgroundColor || "#2563eb"} onChange={(v) => set("backgroundColor", v)} />
    </SettingsGroup>
  );
}

export function buttonHtml(block: EmailBlock) {
  const p = block.props;

  return `
    <div style="background:#ffffff; text-align:center; padding:16px; border-radius:14px;">
      <a href="${p.url || "#"}" style="display:inline-block; background:${p.backgroundColor || "#2563eb"}; color:${p.textColor || "#ffffff"}; font-family:${htmlFont(p.buttonFontFamily)}; font-size:${htmlSize(p.buttonFontSize, "14")}; padding:14px 28px; border-radius:10px; text-decoration:none; font-weight:bold;">
        ${p.text || "Click Here"}
      </a>
    </div>
  `;
}
