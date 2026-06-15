"use client";

import { PlanCard } from "../FormControls";
import { Organization } from "../types";

export function PlanAccessSection({ organization }: { organization: Organization }) {
  return (
    <div>
      <h2>Plan & Access</h2>

      <div className="planGrid">
        <PlanCard label="Plan" value={organization.plan} />
        <PlanCard label="Max Users" value={organization.max_users} />
        <PlanCard label="Max Contacts" value={organization.max_contacts} />
        <PlanCard label="Max Templates" value={organization.max_templates} />
        <PlanCard label="Max Segments" value={organization.max_segments} />
        <PlanCard label="Automation" value={organization.automation_enabled ? "Enabled" : "Disabled"} />
        <PlanCard label="Advanced Segmentation" value={organization.advanced_segmentation_enabled ? "Enabled" : "Disabled"} />
        <PlanCard label="Webhooks" value={organization.webhooks_enabled ? "Enabled" : "Disabled"} />
        <PlanCard label="AI Features" value={organization.ai_features_enabled ? "Enabled" : "Disabled"} />
        <PlanCard label="Custom Branding" value={organization.custom_branding_enabled ? "Enabled" : "Disabled"} />
      </div>

      <p className="muted smallNote">
        Plan values are read-only here. Later, billing/admin logic can control these fields.
      </p>
    </div>
  );
}
