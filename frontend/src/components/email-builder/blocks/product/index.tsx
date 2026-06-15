"use client";

import { EmailBlock } from "../../types";
import { font, px, htmlFont, htmlSize } from "../../blockUtils";
import { SettingsGroup, TextField, TextStyleControls, ColorField, SetProp } from "../../PropertyControls";

export function renderProduct(block: EmailBlock) {
  const p = block.props;

  return (
    <div className="emailProductBlock" style={{ background: p.backgroundColor || "#ffffff" }}>
      <h3 style={{ color: p.titleColor || "#111827", fontFamily: font(p.titleFontFamily), fontSize: px(p.titleFontSize, "18") }}>
        {p.title}
      </h3>

      <strong style={{ color: p.priceColor || "#2563eb", fontFamily: font(p.priceFontFamily), fontSize: px(p.priceFontSize, "24") }}>
        {p.price}
      </strong>

      <p style={{ color: p.textColor || "#6b7280", fontFamily: font(p.textFontFamily), fontSize: px(p.textFontSize, "14") }}>
        {p.description}
      </p>

      <span style={{ background: p.buttonBackgroundColor || "#2563eb", color: p.buttonTextColor || "#ffffff", fontFamily: font(p.buttonFontFamily), fontSize: px(p.buttonFontSize, "14") }}>
        {p.buttonText}
      </span>
    </div>
  );
}

export function ProductProperties({ block, set }: { block: EmailBlock; set: SetProp }) {
  const p = block.props;

  return (
    <>
      <SettingsGroup title="Product Title">
        <TextField label="Title" value={p.title} onChange={(v) => set("title", v)} />
        <TextStyleControls block={block} prefix="Title" colorKey="titleColor" fontKey="titleFontFamily" sizeKey="titleFontSize" defaultColor="#111827" defaultSize="18" set={set} />
      </SettingsGroup>

      <SettingsGroup title="Description">
        <TextField label="Description" value={p.description} onChange={(v) => set("description", v)} textarea />
        <TextStyleControls block={block} prefix="Description" colorKey="textColor" fontKey="textFontFamily" sizeKey="textFontSize" defaultColor="#6b7280" defaultSize="14" set={set} />
      </SettingsGroup>

      <SettingsGroup title="Price">
        <TextField label="Price" value={p.price} onChange={(v) => set("price", v)} />
        <TextStyleControls block={block} prefix="Price" colorKey="priceColor" fontKey="priceFontFamily" sizeKey="priceFontSize" defaultColor="#2563eb" defaultSize="24" set={set} />
      </SettingsGroup>

      <SettingsGroup title="Button">
        <TextField label="Button Text" value={p.buttonText} onChange={(v) => set("buttonText", v)} />
        <TextField label="Button URL" value={p.buttonUrl} onChange={(v) => set("buttonUrl", v)} />
        <TextStyleControls block={block} prefix="Button Text" colorKey="buttonTextColor" fontKey="buttonFontFamily" sizeKey="buttonFontSize" defaultColor="#ffffff" defaultSize="14" set={set} />
        <ColorField label="Button Background" value={p.buttonBackgroundColor || "#2563eb"} onChange={(v) => set("buttonBackgroundColor", v)} />
      </SettingsGroup>

      <SettingsGroup title="Background">
        <ColorField label="Background" value={p.backgroundColor || "#ffffff"} onChange={(v) => set("backgroundColor", v)} />
      </SettingsGroup>
    </>
  );
}

export function productHtml(block: EmailBlock) {
  const p = block.props;

  return `
    <div style="background:${p.backgroundColor || "#ffffff"}; border:1px solid #e5e7eb; border-radius:14px; padding:20px; text-align:center;">
      <h3 style="margin:0; color:${p.titleColor || "#111827"}; font-family:${htmlFont(p.titleFontFamily)}; font-size:${htmlSize(p.titleFontSize, "18")};">
        ${p.title || ""}
      </h3>

      <h2 style="margin:12px 0; color:${p.priceColor || "#2563eb"}; font-family:${htmlFont(p.priceFontFamily)}; font-size:${htmlSize(p.priceFontSize, "24")};">
        ${p.price || ""}
      </h2>

      <p style="color:${p.textColor || "#6b7280"}; font-family:${htmlFont(p.textFontFamily)}; font-size:${htmlSize(p.textFontSize, "14")};">
        ${p.description || ""}
      </p>

      <a href="${p.buttonUrl || "#"}" style="display:inline-block; background:${p.buttonBackgroundColor || "#2563eb"}; color:${p.buttonTextColor || "#ffffff"}; font-family:${htmlFont(p.buttonFontFamily)}; font-size:${htmlSize(p.buttonFontSize, "14")}; padding:12px 20px; border-radius:10px; text-decoration:none; font-weight:bold;">
        ${p.buttonText || "View"}
      </a>
    </div>
  `;
}
