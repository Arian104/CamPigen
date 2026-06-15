import { DEFAULT_SCHEMA, EmailBuilderSchema } from "@/components/email-builder/types";
import { Template } from "../CampaignTypes";

export function cloneDefaultSchema(): EmailBuilderSchema {
  return JSON.parse(JSON.stringify(DEFAULT_SCHEMA));
}

export function isValidSchema(schema: unknown): schema is EmailBuilderSchema {
  return (
    typeof schema === "object" &&
    schema !== null &&
    "blocks" in schema &&
    Array.isArray((schema as EmailBuilderSchema).blocks)
  );
}

export function normalizeTemplateSchema(template: Template | null): EmailBuilderSchema {
  if (template && isValidSchema(template.builder_schema)) {
    return {
      columns: 3,
      blocks: template.builder_schema.blocks.map((block) => ({
        ...block,
        span: block.span ?? 3,
        props: block.props ?? {},
      })),
    };
  }

  return cloneDefaultSchema();
}

export function renderPreview(html: string, context: Record<string, unknown>) {
  let output = html || "";

  Object.entries(context).forEach(([key, rawValue]) => {
    const value = rawValue === null || rawValue === undefined ? "" : String(rawValue);
    output = output.replaceAll(`{{ ${key} }}`, value);
    output = output.replaceAll(`{{${key}}}`, value);
  });

  return output;
}
