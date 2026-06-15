"use client";

type Props = {
  templateName: string;
  setTemplateName: (value: string) => void;
  templateSubject: string;
  setTemplateSubject: (value: string) => void;
  templateType: string;
  setTemplateType: (value: string) => void;
  templateStatus: string;
  setTemplateStatus: (value: string) => void;
};

export function TemplateMetaForm({
  templateName,
  setTemplateName,
  templateSubject,
  setTemplateSubject,
  templateType,
  setTemplateType,
  templateStatus,
  setTemplateStatus,
}: Props) {
  return (
    <div className="builderMetaGrid">
      <input
        value={templateName}
        onChange={(e) => setTemplateName(e.target.value)}
        placeholder="Template name"
      />

      <input
        value={templateSubject}
        onChange={(e) => setTemplateSubject(e.target.value)}
        placeholder="Email subject"
      />

      <select value={templateType} onChange={(e) => setTemplateType(e.target.value)}>
        <option value="marketing">Marketing</option>
        <option value="transactional">Transactional</option>
        <option value="otp">OTP / Verification</option>
        <option value="welcome">Welcome</option>
        <option value="newsletter">Newsletter</option>
        <option value="custom">Custom</option>
      </select>

      <select value={templateStatus} onChange={(e) => setTemplateStatus(e.target.value)}>
        <option value="draft">Draft</option>
        <option value="active">Active</option>
        <option value="archived">Archived</option>
      </select>
    </div>
  );
}
