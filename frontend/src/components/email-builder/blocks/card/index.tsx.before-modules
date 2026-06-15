"use client";

import { EmailBlock } from "../../types";
import { font, px, htmlFont, htmlSize } from "../../blockUtils";
import { SettingsGroup, TextField, TextStyleControls, ColorField, SetProp } from "../../PropertyControls";

export function renderCard(block: EmailBlock) {
  const p = block.props;

  return (
    <div className="emailCardBlock" style={{ background: p.backgroundColor || "#ffffff" }}>
      <h3 style={{ color: p.titleColor || "#111827", fontFamily: font(p.titleFontFamily), fontSize: px(p.titleFontSize, "18") }}>
        {p.title}
      </h3>

      <p style={{ color: p.textColor || "#6b7280", fontFamily: font(p.textFontFamily), fontSize: px(p.textFontSize, "14") }}>
        {p.content}
      </p>
    </div>
  );
}

export function CardProperties({ block, set }: { block: EmailBlock; set: SetProp }) {
  const p = block.props;

  return (
    <>
      <SettingsGroup title="Title">
        <TextField label="Title" value={p.title} onChange={(v) => set("title", v)} />
        <TextStyleControls block={block} prefix="Title" colorKey="titleColor" fontKey="titleFontFamily" sizeKey="titleFontSize" defaultColor="#111827" defaultSize="18" set={set} />
      </SettingsGroup>

      <SettingsGroup title="Body">
        <TextField label="Content" value={p.content} onChange={(v) => set("content", v)} textarea />
        <TextStyleControls block={block} prefix="Body" colorKey="textColor" fontKey="textFontFamily" sizeKey="textFontSize" defaultColor="#6b7280" defaultSize="14" set={set} />
      </SettingsGroup>

      <SettingsGroup title="Background">
        <ColorField label="Background Color" value={p.backgroundColor || "#ffffff"} onChange={(v) => set("backgroundColor", v)} />
      </SettingsGroup>
    </>
  );
}

export function cardHtml(block: EmailBlock) {
  const p = block.props;

  return `
    <div style="background:${p.backgroundColor || "#ffffff"}; border:1px solid #e5e7eb; border-radius:14px; padding:20px;">
      <h3 style="margin:0 0 10px; color:${p.titleColor || "#111827"}; font-family:${htmlFont(p.titleFontFamily)}; font-size:${htmlSize(p.titleFontSize, "18")};">
        ${p.title || ""}
      </h3>

      <p style="margin:0; color:${p.textColor || "#6b7280"}; font-family:${htmlFont(p.textFontFamily)}; font-size:${htmlSize(p.textFontSize, "14")}; line-height:1.7;">
        ${p.content || ""}
      </p>
    </div>
  `;
}
