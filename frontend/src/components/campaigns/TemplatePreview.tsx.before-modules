"use client";

import { useMemo } from "react";
import { Template } from "./CampaignTypes";

type Props = {
  template: Template | null;
  htmlContent?: string;
  subject?: string;
  previewContextRaw: string;
  isEditing: boolean;
  onEdit: () => void;
};

function renderTemplate(html: string, context: Record<string, unknown>) {
  let output = html;

  Object.entries(context).forEach(([key, value]) => {
    const text = value === null || value === undefined ? "" : String(value);
    output = output.replaceAll(`{{ ${key} }}`, text);
    output = output.replaceAll(`{{${key}}}`, text);
  });

  return output;
}

export function TemplatePreview({
  template,
  htmlContent,
  subject,
  previewContextRaw,
  isEditing,
  onEdit,
}: Props) {
  const renderedHtml = useMemo(() => {
    const sourceHtml = htmlContent ?? template?.html_content ?? "";

    if (!sourceHtml) return "";

    let context: Record<string, unknown> = {};

    try {
      context = JSON.parse(previewContextRaw);
    } catch {
      return "<p>Invalid preview JSON context.</p>";
    }

    return renderTemplate(sourceHtml, context);
  }, [template, htmlContent, previewContextRaw]);

  if (!template && !htmlContent) {
    return null;
  }

  return (
    <section className="card">
      <div className="flexBetween">
        <div>
          <h2>Email Preview</h2>
          <p className="muted">
            {template?.name ?? "New Template"} — {subject || template?.subject || "No subject"}
          </p>
        </div>

        {template && !isEditing ? (
          <button type="button" className="secondaryButton" onClick={onEdit}>
            Edit Template
          </button>
        ) : null}
      </div>

      <div
        className="previewBody"
        dangerouslySetInnerHTML={{ __html: renderedHtml }}
      />
    </section>
  );
}
