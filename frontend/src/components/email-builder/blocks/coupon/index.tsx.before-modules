"use client";

import { EmailBlock } from "../../types";
import { font, px, htmlFont, htmlSize } from "../../blockUtils";
import { SettingsGroup, TextField, TextStyleControls, ColorField, SetProp } from "../../PropertyControls";

export function renderCoupon(block: EmailBlock) {
  const p = block.props;

  return (
    <div className="emailCouponBlock" style={{ background: p.backgroundColor || "#eef2ff" }}>
      <h3 style={{ color: p.titleColor || "#111827", fontFamily: font(p.titleFontFamily), fontSize: px(p.titleFontSize, "18") }}>
        {p.title}
      </h3>

      <strong style={{ color: p.codeColor || "#4f46e5", fontFamily: font(p.codeFontFamily), fontSize: px(p.codeFontSize, "22") }}>
        {p.code}
      </strong>

      <p style={{ color: p.textColor || "#6b7280", fontFamily: font(p.textFontFamily), fontSize: px(p.textFontSize, "14") }}>
        {p.description}
      </p>
    </div>
  );
}

export function CouponProperties({ block, set }: { block: EmailBlock; set: SetProp }) {
  const p = block.props;

  return (
    <>
      <SettingsGroup title="Title">
        <TextField label="Title" value={p.title} onChange={(v) => set("title", v)} />
        <TextStyleControls block={block} prefix="Title" colorKey="titleColor" fontKey="titleFontFamily" sizeKey="titleFontSize" defaultColor="#111827" defaultSize="18" set={set} />
      </SettingsGroup>

      <SettingsGroup title="Coupon Code">
        <TextField label="Coupon Code" value={p.code} onChange={(v) => set("code", v)} />
        <TextStyleControls block={block} prefix="Code" colorKey="codeColor" fontKey="codeFontFamily" sizeKey="codeFontSize" defaultColor="#4f46e5" defaultSize="22" set={set} />
      </SettingsGroup>

      <SettingsGroup title="Description">
        <TextField label="Description" value={p.description} onChange={(v) => set("description", v)} textarea />
        <TextStyleControls block={block} prefix="Description" colorKey="textColor" fontKey="textFontFamily" sizeKey="textFontSize" defaultColor="#6b7280" defaultSize="14" set={set} />
      </SettingsGroup>

      <SettingsGroup title="Background">
        <ColorField label="Background" value={p.backgroundColor || "#eef2ff"} onChange={(v) => set("backgroundColor", v)} />
      </SettingsGroup>
    </>
  );
}

export function couponHtml(block: EmailBlock) {
  const p = block.props;

  return `
    <div style="background:${p.backgroundColor || "#eef2ff"}; border:1px dashed #6366f1; border-radius:14px; padding:22px; text-align:center;">
      <h3 style="margin:0; color:${p.titleColor || "#111827"}; font-family:${htmlFont(p.titleFontFamily)}; font-size:${htmlSize(p.titleFontSize, "18")};">
        ${p.title || ""}
      </h3>

      <div style="margin:14px auto; display:inline-block; background:#ffffff; padding:10px 18px; border-radius:10px; font-family:${htmlFont(p.codeFontFamily)}; font-size:${htmlSize(p.codeFontSize, "22")}; font-weight:bold; color:${p.codeColor || "#4f46e5"};">
        ${p.code || ""}
      </div>

      <p style="margin:0; color:${p.textColor || "#6b7280"}; font-family:${htmlFont(p.textFontFamily)}; font-size:${htmlSize(p.textFontSize, "14")};">
        ${p.description || ""}
      </p>
    </div>
  `;
}
