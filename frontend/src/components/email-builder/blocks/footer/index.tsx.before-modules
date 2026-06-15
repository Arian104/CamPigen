"use client";

import { EmailBlock } from "../../types";
import { font, px, htmlFont, htmlSize } from "../../blockUtils";
import { SettingsGroup, TextField, TextStyleControls, ColorField, SetProp } from "../../PropertyControls";

export function renderFooter(block: EmailBlock) {
  const p = block.props;

  return (
    <div className="emailFooterBlock" style={{ background: p.backgroundColor || "#f9fafb", color: p.textColor || "#6b7280", fontFamily: font(p.textFontFamily), fontSize: px(p.textFontSize, "13") }}>
      <strong>{p.companyName}</strong>
      <p>{p.footerText}</p>
    </div>
  );
}

export function FooterProperties({ block, set }: { block: EmailBlock; set: SetProp }) {
  const p = block.props;

  return (
    <>
      <SettingsGroup title="Company">
        <TextField label="Company Name" value={p.companyName} onChange={(v) => set("companyName", v)} />
        <TextStyleControls block={block} prefix="Company" colorKey="textColor" fontKey="textFontFamily" sizeKey="textFontSize" defaultColor="#6b7280" defaultSize="13" set={set} />
      </SettingsGroup>

      <SettingsGroup title="Footer Text">
        <TextField label="Footer Text" value={p.footerText} onChange={(v) => set("footerText", v)} textarea />
      </SettingsGroup>

      <SettingsGroup title="Background">
        <ColorField label="Background" value={p.backgroundColor || "#f9fafb"} onChange={(v) => set("backgroundColor", v)} />
      </SettingsGroup>
    </>
  );
}

export function footerHtml(block: EmailBlock) {
  const p = block.props;

  return `
    <div style="background:${p.backgroundColor || "#f9fafb"}; text-align:center; color:${p.textColor || "#6b7280"}; font-family:${htmlFont(p.textFontFamily)}; font-size:${htmlSize(p.textFontSize, "13")}; padding:24px; border-radius:14px;">
      <strong>${p.companyName || ""}</strong><br/>
      ${p.footerText || ""}
    </div>
  `;
}
