"use client";

import { Field } from "../FormControls";
import { Organization, Preset, UpdateOrganizationField } from "../types";

export function PresetsSection({
  organization,
  presets,
  selectedPreset,
  updateField,
  applyPreset,
}: {
  organization: Organization;
  presets: Preset[];
  selectedPreset?: Preset;
  updateField: UpdateOrganizationField;
  applyPreset: () => void;
}) {
  return (
    <div>
      <h2>CDP Presets</h2>
      <p className="muted">Presets create industry-specific contact fields, tags, and lists.</p>

      <div className="formGrid">
        <Field label="Contact Schema Preset">
          <select
            value={organization.contact_schema_preset}
            onChange={(e) => updateField("contact_schema_preset", e.target.value)}
          >
            <option value="custom">Custom</option>
            {presets.map((preset) => (
              <option key={preset.key} value={preset.key}>
                {preset.label}
              </option>
            ))}
          </select>
        </Field>

        <Field label="Preset Applied">
          <input value={organization.preset_applied ? "Yes" : "No"} disabled />
        </Field>
      </div>

      {selectedPreset ? (
        <div className="presetPreview">
          <h3>{selectedPreset.label} Preset</h3>

          <div>
            <strong>Fields</strong>
            <div className="chipGroup">
              {selectedPreset.fields.map((field) => (
                <span key={field.key} className="chip">
                  {field.name}
                </span>
              ))}
            </div>
          </div>

          <div>
            <strong>Tags</strong>
            <div className="chipGroup">
              {selectedPreset.tags.map((tag) => (
                <span key={tag} className="chip">
                  {tag}
                </span>
              ))}
            </div>
          </div>

          <div>
            <strong>Lists</strong>
            <div className="chipGroup">
              {selectedPreset.lists.map((list) => (
                <span key={list} className="chip">
                  {list}
                </span>
              ))}
            </div>
          </div>

          <button type="button" className="buttonLink" onClick={applyPreset}>
            Apply Preset
          </button>
        </div>
      ) : null}
    </div>
  );
}
