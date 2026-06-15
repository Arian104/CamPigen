"use client";

import { EmailBlock } from "../../types";
import { font, px, htmlFont, htmlSize } from "../../blockUtils";
import { SettingsGroup, TextField, TextStyleControls, ColorField, SetProp } from "../../PropertyControls";

export function renderSocial(block: EmailBlock) {
  const p = block.props;

  return (
    <div className="emailSocialBlock" style={{ background: p.backgroundColor || "#ffffff", color: p.textColor || "#2563eb", fontFamily: font(p.textFontFamily), fontSize: px(p.textFontSize, "14") }}>
      <span>Facebook</span>
      <span>Instagram</span>
      <span>LinkedIn</span>
    </div>
  );
}

export function SocialProperties({ block, set }: { block: EmailBlock; set: SetProp }) {
  const p = block.props;

  return (
    <>
      <SettingsGroup title="Links">
        <TextField label="Facebook URL" value={p.facebook} onChange={(v) => set("facebook", v)} />
        <TextField label="Instagram URL" value={p.instagram} onChange={(v) => set("instagram", v)} />
        <TextField label="LinkedIn URL" value={p.linkedin} onChange={(v) => set("linkedin", v)} />
      </SettingsGroup>

      <SettingsGroup title="Text Style">
        <TextStyleControls block={block} prefix="Link" colorKey="textColor" fontKey="textFontFamily" sizeKey="textFontSize" defaultColor="#2563eb" defaultSize="14" set={set} />
      </SettingsGroup>

      <SettingsGroup title="Background">
        <ColorField label="Background" value={p.backgroundColor || "#ffffff"} onChange={(v) => set("backgroundColor", v)} />
      </SettingsGroup>
    </>
  );
}

export function socialHtml(block: EmailBlock) {
  const p = block.props;

  return `
    <div style="background:${p.backgroundColor || "#ffffff"}; text-align:center; padding:18px; border-radius:14px; font-family:${htmlFont(p.textFontFamily)}; font-size:${htmlSize(p.textFontSize, "14")};">
      <a href="${p.facebook || "#"}" style="margin:0 8px; color:${p.textColor || "#2563eb"};">Facebook</a>
      <a href="${p.instagram || "#"}" style="margin:0 8px; color:${p.textColor || "#2563eb"};">Instagram</a>
      <a href="${p.linkedin || "#"}" style="margin:0 8px; color:${p.textColor || "#2563eb"};">LinkedIn</a>
    </div>
  `;
}
