"use client";

import { Template } from "../CampaignTypes";

type Props = {
  templates: Template[];
  onPreview: (template: Template) => void;
  onEdit: (template: Template) => void;
  onDelete: (template: Template) => void;
};

export function TemplateList({
  templates,
  onPreview,
  onEdit,
  onDelete,
}: Props) {
  if (templates.length === 0) {
    return <p className="muted">No templates available. Create one to start.</p>;
  }

  return (
    <div className="templateList">
      {templates.map((template) => (
        <div key={template.id} className="templateCard modernTemplateCard">
          <div className="templateCardIcon">
            {template.name?.slice(0, 2).toUpperCase() || "TP"}
          </div>

          <div className="templateCardMain">
            <div className="templateCardTop">
              <div>
                <strong>{template.name}</strong>
                <p className="muted">{template.subject}</p>
              </div>

              <span className="templateStatusPill">
                {template.status ?? "draft"}
              </span>
            </div>

            <div className="templateCardMeta">
              <span>{template.template_type ?? "marketing"}</span>
              <span>{template.builder_schema?.blocks?.length ?? 0} blocks</span>
            </div>

            <div className="actions templateActions">
              <button type="button" className="secondaryButton" onClick={() => onPreview(template)}>
                Preview
              </button>

              <button type="button" className="ghostButton" onClick={() => onEdit(template)}>
                Edit Builder
              </button>

              <button type="button" className="dangerButton" onClick={() => onDelete(template)}>
                Delete
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
