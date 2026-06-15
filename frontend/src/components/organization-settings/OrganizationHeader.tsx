"use client";

import { RefreshCw, Save } from "lucide-react";

export function OrganizationHeader({
  saving,
  onRefresh,
  onSave,
}: {
  saving: boolean;
  onRefresh: () => void;
  onSave: () => void;
}) {
  return (
    <section className="card orgHeader">
      <div>
        <p className="eyebrow">Tenant Control Center</p>
        <h1>Organization Settings</h1>
        <p className="muted">
          Manage branding, campaign defaults, compliance, CDP presets, and team access.
        </p>
      </div>

      <div className="orgHeaderActions">
        <button type="button" className="secondaryButton" onClick={onRefresh}>
          <RefreshCw size={16} />
          Refresh
        </button>

        <button type="button" className="buttonLink" onClick={onSave}>
          <Save size={16} />
          {saving ? "Saving..." : "Save Changes"}
        </button>
      </div>
    </section>
  );
}
