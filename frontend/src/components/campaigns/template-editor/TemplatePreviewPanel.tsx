"use client";

import { Template } from "../CampaignTypes";

type Props = {
  template: Template | null;
  html: string;
  title?: string;
  subject?: string;
  showEditButton?: boolean;
  onEdit?: () => void;
};

export function TemplatePreviewPanel({
  template,
  html,
  title,
  subject,
  showEditButton = false,
  onEdit,
}: Props) {
  if (!template && !html) return null;

  return (
    <section className="templatePreviewPanel">
      <div className="previewHeader flexBetween">
        <div>
          <h3>{title ?? template?.name ?? "Live Preview"}</h3>
          <p className="muted">{subject ?? template?.subject ?? "No subject"}</p>
        </div>

        {showEditButton && onEdit ? (
          <button type="button" className="primaryButton" onClick={onEdit}>
            Edit Template
          </button>
        ) : null}
      </div>

      <div className="previewBody" dangerouslySetInnerHTML={{ __html: html }} />
    </section>
  );
}
