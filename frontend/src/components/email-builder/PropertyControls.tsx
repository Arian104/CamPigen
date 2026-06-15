"use client";

import { EmailBlock } from "./types";
import styles from "./EmailBuilder.module.css";

export const FONT_OPTIONS = [
  "Arial, Helvetica, sans-serif",
  "Inter, Arial, sans-serif",
  "Georgia, serif",
  "Times New Roman, serif",
  "Verdana, Geneva, sans-serif",
  "Tahoma, Geneva, sans-serif",
];

const QUICK_COLORS = ["#111827", "#2563eb", "#16a34a", "#f59e0b"];

export type SetProp = (key: string, value: string) => void;

export function SettingsGroup({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className={`${styles.settingsGroup} settingsGroup`}>
      <h4>{title}</h4>
      <div className="grid">{children}</div>
    </div>
  );
}

export function TextField({
  label,
  value,
  onChange,
  textarea = false,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  textarea?: boolean;
}) {
  return (
    <label className="builderField">
      <span>{label}</span>
      {textarea ? (
        <textarea rows={4} value={value ?? ""} onChange={(e) => onChange(e.target.value)} />
      ) : (
        <input value={value ?? ""} onChange={(e) => onChange(e.target.value)} />
      )}
    </label>
  );
}

export function ColorField({
  label,
  value,
  onChange,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
}) {
  const currentColor = value || "#ffffff";

  return (
    <div className="builderField">
      <span>{label}</span>

      <div className="compactColorRow">
        <label
          className="selectedColorCircle"
          style={{ backgroundColor: currentColor }}
          title={currentColor}
        >
          <input
            type="color"
            value={currentColor}
            onChange={(e) => onChange(e.target.value)}
            className="hiddenColorPicker"
          />
        </label>

        {QUICK_COLORS.map((color) => (
          <button
            key={color}
            type="button"
            className={
              currentColor.toLowerCase() === color.toLowerCase()
                ? "quickColorCircle active"
                : "quickColorCircle"
            }
            style={{ backgroundColor: color }}
            onClick={() => onChange(color)}
            title={color}
          />
        ))}

        <input
          value={currentColor}
          onChange={(e) => onChange(e.target.value)}
          className="compactColorValue"
        />
      </div>
    </div>
  );
}

export function FontField({
  label,
  value,
  onChange,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <label className="builderField">
      <span>{label}</span>
      <select value={value || FONT_OPTIONS[0]} onChange={(e) => onChange(e.target.value)}>
        {FONT_OPTIONS.map((font) => (
          <option key={font} value={font}>
            {font.split(",")[0]}
          </option>
        ))}
      </select>
    </label>
  );
}

export function FontSizeField({
  label,
  value,
  onChange,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <label className="builderField">
      <span>{label}</span>
      <div className="fontSizeRow">
        <input
          type="range"
          min={10}
          max={56}
          value={Number(value || 16)}
          onChange={(e) => onChange(e.target.value)}
        />

        <input
          type="number"
          min={10}
          max={80}
          value={value || "16"}
          onChange={(e) => onChange(e.target.value)}
        />

        <span>px</span>
      </div>
    </label>
  );
}

export function TextStyleControls({
  block,
  prefix,
  colorKey,
  fontKey,
  sizeKey,
  defaultColor,
  defaultSize,
  set,
}: {
  block: EmailBlock;
  prefix: string;
  colorKey: string;
  fontKey: string;
  sizeKey: string;
  defaultColor: string;
  defaultSize: string;
  set: SetProp;
}) {
  const p = block.props;

  return (
    <>
      <ColorField
        label={`${prefix} Color`}
        value={p[colorKey] || defaultColor}
        onChange={(v) => set(colorKey, v)}
      />

      <FontField
        label={`${prefix} Font`}
        value={p[fontKey] || FONT_OPTIONS[0]}
        onChange={(v) => set(fontKey, v)}
      />

      <FontSizeField
        label={`${prefix} Size`}
        value={p[sizeKey] || defaultSize}
        onChange={(v) => set(sizeKey, v)}
      />
    </>
  );
}
