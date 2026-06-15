"use client";

import { EmailBlock } from "../../types";
import { font, px, htmlFont, htmlSize } from "../../blockUtils";
import { SettingsGroup, TextField, TextStyleControls, ColorField, SetProp } from "../../PropertyControls";

export function renderText(block: EmailBlock) {
  const p = block.props;

  return (
    <div className="emailTextBlock" style={{ background: p.backgroundColor || "#ffffff", color: p.textColor || "#374151", fontFamily: font(p.textFontFamily), fontSize: px(p.textFontSize, "16") }}>
      {p.content}
    </div>
  );
}

export function TextProperties({ block, set }: { block: EmailBlock; set: SetProp }) {
  const p = block.props;

  return (
    <>
      <SettingsGroup title="Text">
        <TextField label="Content" value={p.content} onChange={(v) => set("content", v)} textarea />
        <TextStyleControls block={block} prefix="Text" colorKey="textColor" fontKey="textFontFamily" sizeKey="textFontSize" defaultColor="#374151" defaultSize="16" set={set} />
      </SettingsGroup>

      <SettingsGroup title="Background">
        <ColorField label="Background Color" value={p.backgroundColor || "#ffffff"} onChange={(v) => set("backgroundColor", v)} />
      </SettingsGroup>
    </>
  );
}

export function textHtml(block: EmailBlock) {
  const p = block.props;

  return `
    <div style="background:${p.backgroundColor || "#ffffff"}; color:${p.textColor || "#374151"}; font-family:${htmlFont(p.textFontFamily)}; font-size:${htmlSize(p.textFontSize, "16")}; line-height:1.8; padding:18px; border-radius:14px;">
      ${p.content || ""}
    </div>
  `;
}
