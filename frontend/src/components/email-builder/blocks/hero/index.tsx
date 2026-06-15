"use client";

import { EmailBlock } from "../../types";
import { font, px, htmlFont, htmlSize } from "../../blockUtils";
import { SettingsGroup, TextField, TextStyleControls, ColorField, SetProp } from "../../PropertyControls";

export function renderHero(block: EmailBlock) {
  const p = block.props;

  return (
    <div className="emailHeroBlock" style={{ background: p.backgroundColor || "#111827" }}>
      <h1 style={{ color: p.textColor || "#ffffff", fontFamily: font(p.titleFontFamily), fontSize: px(p.titleFontSize, "32") }}>
        {p.title || "Hero Title"}
      </h1>

      <p style={{ color: p.subTextColor || "#d1d5db", fontFamily: font(p.subtitleFontFamily), fontSize: px(p.subtitleFontSize, "16") }}>
        {p.subtitle || "Hero subtitle"}
      </p>

      {p.buttonText ? (
        <span style={{ background: p.buttonBackgroundColor || "#ffffff", color: p.buttonTextColor || "#111827", fontFamily: font(p.buttonFontFamily), fontSize: px(p.buttonFontSize, "14") }}>
          {p.buttonText}
        </span>
      ) : null}
    </div>
  );
}

export function HeroProperties({ block, set }: { block: EmailBlock; set: SetProp }) {
  const p = block.props;

  return (
    <>
      <SettingsGroup title="Title">
        <TextField label="Title Text" value={p.title} onChange={(v) => set("title", v)} />
        <TextStyleControls block={block} prefix="Title" colorKey="textColor" fontKey="titleFontFamily" sizeKey="titleFontSize" defaultColor="#ffffff" defaultSize="32" set={set} />
      </SettingsGroup>

      <SettingsGroup title="Subtitle">
        <TextField label="Subtitle Text" value={p.subtitle} onChange={(v) => set("subtitle", v)} textarea />
        <TextStyleControls block={block} prefix="Subtitle" colorKey="subTextColor" fontKey="subtitleFontFamily" sizeKey="subtitleFontSize" defaultColor="#dbeafe" defaultSize="16" set={set} />
      </SettingsGroup>

      <SettingsGroup title="Button">
        <TextField label="Button Text" value={p.buttonText} onChange={(v) => set("buttonText", v)} />
        <TextField label="Button URL" value={p.buttonUrl} onChange={(v) => set("buttonUrl", v)} />
        <TextStyleControls block={block} prefix="Button Text" colorKey="buttonTextColor" fontKey="buttonFontFamily" sizeKey="buttonFontSize" defaultColor="#111827" defaultSize="14" set={set} />
        <ColorField label="Button Background" value={p.buttonBackgroundColor || "#ffffff"} onChange={(v) => set("buttonBackgroundColor", v)} />
      </SettingsGroup>

      <SettingsGroup title="Background">
        <ColorField label="Background Color" value={p.backgroundColor || "#195ae6"} onChange={(v) => set("backgroundColor", v)} />
      </SettingsGroup>
    </>
  );
}

export function heroHtml(block: EmailBlock) {
  const p = block.props;

  return `
    <div style="background:${p.backgroundColor || "#111827"}; padding:44px 28px; text-align:center; border-radius:16px;">
      <h1 style="margin:0; color:${p.textColor || "#ffffff"}; font-family:${htmlFont(p.titleFontFamily)}; font-size:${htmlSize(p.titleFontSize, "32")};">
        ${p.title || ""}
      </h1>

      <p style="color:${p.subTextColor || "#d1d5db"}; font-family:${htmlFont(p.subtitleFontFamily)}; font-size:${htmlSize(p.subtitleFontSize, "16")}; line-height:1.7;">
        ${p.subtitle || ""}
      </p>

      ${
        p.buttonText
          ? `<a href="${p.buttonUrl || "#"}" style="display:inline-block; background:${p.buttonBackgroundColor || "#ffffff"}; color:${p.buttonTextColor || "#111827"}; font-family:${htmlFont(p.buttonFontFamily)}; font-size:${htmlSize(p.buttonFontSize, "14")}; padding:13px 24px; border-radius:10px; text-decoration:none; font-weight:bold;">${p.buttonText}</a>`
          : ""
      }
    </div>
  `;
}
