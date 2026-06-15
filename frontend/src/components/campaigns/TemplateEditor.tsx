"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

import { usePlatform } from "@/components/platform-context";
import { EmailBuilder } from "@/components/email-builder/EmailBuilder";
import { EmailBuilderSchema } from "@/components/email-builder/types";
import { compileEmailHtml } from "@/components/email-builder/compileEmailHtml";

import { Contact, OrganizationTemplateData, Template } from "./CampaignTypes";
import { buildPreviewContext, pickPreviewContact } from "./previewContext";
import { TemplateList } from "./template-editor/TemplateList";
import { TemplateMetaForm } from "./template-editor/TemplateMetaForm";
import { TemplatePreviewPanel } from "./template-editor/TemplatePreviewPanel";
import { TemplateSaveBar } from "./template-editor/TemplateSaveBar";
import { PreviewVariables } from "./template-editor/PreviewVariables";
import {
  cloneDefaultSchema,
  normalizeTemplateSchema,
  renderPreview,
} from "./template-editor/templateUtils";
import shared from "@/styles/shared.module.css";
import componentStyles from "./CampaignComponents.module.css";

type Props = {
  templates: Template[];
  contacts: Contact[];
  organizationData: OrganizationTemplateData | null;
  selectedTemplate: Template | null;
  setSelectedTemplate: (template: Template | null) => void;
  isEditing: boolean;
  setIsEditing: (value: boolean) => void;
  loading: boolean;
  onSaved: () => Promise<void> | void;
};

export function TemplateEditor({
  templates,
  contacts,
  organizationData,
  selectedTemplate,
  setSelectedTemplate,
  isEditing,
  setIsEditing,
  loading,
  onSaved,
}: Props) {
  const { request } = usePlatform();

  const [templateName, setTemplateName] = useState("");
  const [templateSubject, setTemplateSubject] = useState("");
  const [templateType, setTemplateType] = useState("marketing");
  const [templateStatus, setTemplateStatus] = useState("draft");

  const [builderSchema, setBuilderSchema] = useState<EmailBuilderSchema>(
    cloneDefaultSchema(),
  );
  const [compiledHtml, setCompiledHtml] = useState("");
  const [builderKey, setBuilderKey] = useState("new-builder");

  const [previewTemplate, setPreviewTemplate] = useState<Template | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [message, setMessage] = useState("");


  const previewContact = useMemo(
    () => pickPreviewContact(contacts),
    [contacts],
  );

  const previewData = useMemo(
    () => buildPreviewContext(organizationData, previewContact),
    [organizationData, previewContact],
  );

  const renderedHtml = useMemo(
    () => renderPreview(compiledHtml, previewData),
    [compiledHtml, previewData],
  );

  const selectedPreviewHtml = useMemo(() => {
    if (!previewTemplate) return "";
    return renderPreview(
      previewTemplate.html_content ?? "",
      previewTemplate.preview_data ?? previewData,
    );
  }, [previewTemplate, previewData]);

  const handleBuilderChange = useCallback((schema: EmailBuilderSchema, html: string) => {
    setBuilderSchema(schema);
    setCompiledHtml(html);
  }, []);

  async function hydrateTemplate(template: Template) {
    const result = await request(`/v1/templates/${template.id}/`);

    if (result.ok && typeof result.body === "object" && result.body) {
      return result.body as Template;
    }

    return template;
  }

  function loadTemplateIntoEditor(template: Template) {
    const schema = normalizeTemplateSchema(template);

    setTemplateName(template.name ?? "");
    setTemplateSubject(template.subject ?? "");
    setTemplateType(template.template_type ?? "marketing");
    setTemplateStatus(template.status ?? "draft");

    setBuilderSchema(schema);
    setCompiledHtml(template.html_content || compileEmailHtml(schema));
    setBuilderKey(`template-${template.id}-${Date.now()}`);
  }

  useEffect(() => {
    if (!selectedTemplate) return;
    loadTemplateIntoEditor(selectedTemplate);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedTemplate?.id]);

  function resetForm() {
    const schema = cloneDefaultSchema();

    setSelectedTemplate(null);
    setPreviewTemplate(null);

    setTemplateName("");
    setTemplateSubject("");
    setTemplateType("marketing");
    setTemplateStatus("draft");

    setBuilderSchema(schema);
    setCompiledHtml(compileEmailHtml(schema));
    setBuilderKey(`new-${Date.now()}`);

  }

  async function selectTemplate(template: Template) {
    const fullTemplate = await hydrateTemplate(template);

    setPreviewTemplate(fullTemplate);
    setSelectedTemplate(fullTemplate);

    setIsEditing(false);
    setIsCreating(false);
    setMessage("Preview loaded with organization/contact data.");
  }

  async function startEdit(template: Template) {
    const fullTemplate = await hydrateTemplate(template);

    setPreviewTemplate(null);
    setSelectedTemplate(fullTemplate);
    loadTemplateIntoEditor(fullTemplate);

    setIsEditing(true);
    setIsCreating(false);
    setMessage("Template loaded into builder.");
  }

  async function deleteTemplate(template: Template) {
    const ok = window.confirm(`Delete template "${template.name}"?`);
    if (!ok) return;

    const result = await request(`/v1/templates/${template.id}/`, {
      method: "DELETE",
    });

    if (result.ok) {
      setMessage("Template deleted.");
      setPreviewTemplate(null);

      if (selectedTemplate?.id === template.id) {
        setSelectedTemplate(null);
      }

      await onSaved();
    } else {
      setMessage(`Delete failed: ${JSON.stringify(result.body)}`);
    }
  }

  async function createTemplate() {
    if (!templateName || !templateSubject) {
      setMessage("Template name and subject are required.");
      return;
    }

    const result = await request("/v1/templates/", {
      method: "POST",
      body: JSON.stringify({
        name: templateName,
        subject: templateSubject,
        html_content: compiledHtml,
        text_content: "",
        template_type: templateType,
        status: templateStatus,
        variables: Object.keys(previewData),
        preview_data: previewData,
        builder_schema: builderSchema,
      }),
    });

    if (result.ok && typeof result.body === "object" && result.body) {
      const saved = result.body as Template;

      setSelectedTemplate(saved);
      setPreviewTemplate(saved);
      setMessage("Template created successfully.");

      setIsCreating(false);
      setIsEditing(false);

      await onSaved();
    } else {
      setMessage(`Failed: ${JSON.stringify(result.body)}`);
    }
  }

  async function saveTemplate() {
    if (!selectedTemplate) return;

    const result = await request(`/v1/templates/${selectedTemplate.id}/`, {
      method: "PATCH",
      body: JSON.stringify({
        name: templateName,
        subject: templateSubject,
        html_content: compiledHtml,
        text_content: "",
        template_type: templateType,
        status: templateStatus,
        variables: Object.keys(previewData),
        preview_data: previewData,
        builder_schema: builderSchema,
      }),
    });

    if (result.ok && typeof result.body === "object" && result.body) {
      const saved = result.body as Template;

      setSelectedTemplate(saved);
      setPreviewTemplate(saved);
      setMessage("Template saved successfully.");

      setIsEditing(false);
      setIsCreating(false);

      await onSaved();
    } else {
      setMessage(`Failed: ${JSON.stringify(result.body)}`);
    }
  }

  return (
    <section className={`${shared.card} ${componentStyles.editorRoot}`}>
      <div className={shared.flexBetween}>
        <div>
          <h2>Email Builder</h2>
          <p className={shared.muted}>
            Build reusable email templates using organization and contact variables.
          </p>
        </div>

        <button
          type="button"
          className={shared.primaryButton}
          onClick={() => {
            resetForm();
            setIsCreating(true);
            setIsEditing(false);
          }}
        >
          + Create Template
        </button>
      </div>

      {message ? <p className={shared.muted}>{message}</p> : null}

      {!isCreating && !isEditing ? (
        <TemplateList
          templates={templates}
          onPreview={(template) => void selectTemplate(template)}
          onEdit={(template) => void startEdit(template)}
          onDelete={(template) => void deleteTemplate(template)}
        />
      ) : null}

      {previewTemplate && !isCreating && !isEditing ? (
        <TemplatePreviewPanel
          template={previewTemplate}
          html={selectedPreviewHtml}
          showEditButton
          onEdit={() => void startEdit(previewTemplate)}
        />
      ) : null}

      {isCreating || isEditing ? (
        <>
          <TemplateSaveBar
            isCreating={isCreating}
            loading={loading}
            onCreate={() => void createTemplate()}
            onSave={() => void saveTemplate()}
            onCancel={() => {
              setIsEditing(false);
              setIsCreating(false);
            }}
          />

          <TemplateMetaForm
            templateName={templateName}
            setTemplateName={setTemplateName}
            templateSubject={templateSubject}
            setTemplateSubject={setTemplateSubject}
            templateType={templateType}
            setTemplateType={setTemplateType}
            templateStatus={templateStatus}
            setTemplateStatus={setTemplateStatus}
          />

          <EmailBuilder key={builderKey} initialSchema={builderSchema} onChange={handleBuilderChange} />

          <PreviewVariables previewData={previewData} />

          <TemplatePreviewPanel
            template={null}
            html={renderedHtml}
            title="Live Preview"
            subject={templateSubject || "No subject"}
          />

          <TemplateSaveBar
            isCreating={isCreating}
            loading={loading}
            onCreate={() => void createTemplate()}
            onSave={() => void saveTemplate()}
            onCancel={() => {
              setIsEditing(false);
              setIsCreating(false);
            }}
          />
        </>
      ) : null}
    </section>
  );
}
