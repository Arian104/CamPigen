"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import { CalendarClock, CheckCircle2, Mail, Send, Users } from "lucide-react";

import { usePlatform } from "@/components/platform-context";
import {
  Campaign,
  Contact,
  ContactList,
  OrganizationTemplateData,
  Template,
} from "./CampaignTypes";

type Props = {
  templates: Template[];
  contacts: Contact[];
  contactLists: ContactList[];
  organizationData: OrganizationTemplateData | null;
  loading: boolean;
  editingCampaign?: Campaign | null;
  onTemplateSelected: (template: Template | null) => void;
  onCancelEdit?: () => void;
  onCreated: () => Promise<void>;
};

function toDatetimeLocalValue(utcValue?: string | null) {
  if (!utcValue) return "";

  const date = new Date(utcValue);
  const offsetMs = date.getTimezoneOffset() * 60 * 1000;
  const localDate = new Date(date.getTime() - offsetMs);

  return localDate.toISOString().slice(0, 16);
}

function localDatetimeToUtcIso(localValue: string) {
  if (!localValue) return null;
  return new Date(localValue).toISOString();
}

export function CampaignForm({
  templates,
  contactLists,
  organizationData,
  loading,
  editingCampaign,
  onTemplateSelected,
  onCancelEdit,
  onCreated,
}: Props) {
  const { request } = usePlatform();

  const isEditing = Boolean(editingCampaign?.id);

  const [name, setName] = useState("");
  const [subject, setSubject] = useState("");
  const [templateId, setTemplateId] = useState("");
  const [scheduledAt, setScheduledAt] = useState("");
  const [selectedListIds, setSelectedListIds] = useState<string[]>([]);
  const [fromName, setFromName] = useState("");
  const [fromEmail, setFromEmail] = useState("");
  const [replyTo, setReplyTo] = useState("");
  const [formMessage, setFormMessage] = useState("Select a template, contact list, and schedule time.");

  const selectedTemplate = useMemo(() => {
    return templates.find((template) => template.id === templateId) ?? null;
  }, [templates, templateId]);

  const selectedLists = useMemo(() => {
    return contactLists.filter((list) => selectedListIds.includes(list.id));
  }, [contactLists, selectedListIds]);

  const totalRecipients = useMemo(() => {
    return selectedLists.reduce((sum, list) => sum + Number(list.total_contacts ?? 0), 0);
  }, [selectedLists]);

  useEffect(() => {
    if (editingCampaign) {
      setName(editingCampaign.name || "");
      setSubject(editingCampaign.subject || "");
      setTemplateId(editingCampaign.template || "");
      setScheduledAt(toDatetimeLocalValue(editingCampaign.scheduled_at));
      setSelectedListIds(editingCampaign.target_lists || []);
      setFromName(editingCampaign.from_name || organizationData?.default_from_name || "");
      setFromEmail(editingCampaign.from_email || organizationData?.default_from_email || "");
      setReplyTo(editingCampaign.reply_to || organizationData?.default_reply_to_email || "");
      setFormMessage("Editing campaign. Update details and save changes.");
      return;
    }

    setName("");
    setSubject("");
    setTemplateId("");
    setScheduledAt("");
    setSelectedListIds([]);
    setFromName(organizationData?.default_from_name || "");
    setFromEmail(organizationData?.default_from_email || "");
    setReplyTo(organizationData?.default_reply_to_email || "");
    setFormMessage("Select a template, contact list, and schedule time.");
  }, [editingCampaign, organizationData]);

  useEffect(() => {
    onTemplateSelected(selectedTemplate);

    if (selectedTemplate && !subject && !isEditing) {
      setSubject(selectedTemplate.subject || "");
    }
  }, [selectedTemplate, subject, isEditing, onTemplateSelected]);

  function toggleList(listId: string) {
    setSelectedListIds((current) => {
      if (current.includes(listId)) {
        return current.filter((id) => id !== listId);
      }

      return [...current, listId];
    });
  }

  async function submitCampaign(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!name.trim()) {
      setFormMessage("Campaign name is required.");
      return;
    }

    if (!subject.trim()) {
      setFormMessage("Subject is required.");
      return;
    }

    if (!templateId) {
      setFormMessage("Select an email template.");
      return;
    }

    if (!scheduledAt) {
      setFormMessage("Select schedule date and time.");
      return;
    }

    if (selectedListIds.length === 0) {
      setFormMessage("Select at least one contact list.");
      return;
    }

    const payload = {
      name: name.trim(),
      subject: subject.trim(),
      template: templateId,
      scheduled_at: localDatetimeToUtcIso(scheduledAt),
      target_lists: selectedListIds,
      from_name: fromName.trim(),
      from_email: fromEmail.trim(),
      reply_to: replyTo.trim(),
      status: "scheduled",
    };

    const endpoint = isEditing
      ? `/v1/campaigns/${editingCampaign?.id}/`
      : "/v1/campaigns/";

    const method = isEditing ? "PATCH" : "POST";

    const result = await request(endpoint, {
      method,
      body: JSON.stringify(payload),
    });

    if (!result.ok) {
      setFormMessage(`Campaign save failed: ${JSON.stringify(result.body)}`);
      return;
    }

    setFormMessage(isEditing ? "Campaign updated successfully." : "Campaign created successfully.");
    await onCreated();
  }

  return (
    <section className="card campaignFormCard">
      <div className="flexBetween">
        <div>
          <p className="eyebrow">{isEditing ? "Edit Campaign" : "Create Campaign"}</p>
          <h2>{isEditing ? "Update Campaign Schedule" : "New Campaign"}</h2>
          <p className="muted">{formMessage}</p>
        </div>

        {isEditing ? (
          <button type="button" className="secondaryButton" onClick={onCancelEdit}>
            Cancel Edit
          </button>
        ) : null}
      </div>

      <form className="campaignModernForm" onSubmit={submitCampaign}>
        <div className="campaignFormGrid">
          <label className="formField">
            <span>Campaign Name</span>
            <input
              value={name}
              onChange={(event) => setName(event.target.value)}
              placeholder="May newsletter"
              required
            />
          </label>

          <label className="formField">
            <span>Subject</span>
            <input
              value={subject}
              onChange={(event) => setSubject(event.target.value)}
              placeholder="Email subject"
              required
            />
          </label>

          <label className="formField">
            <span>Schedule Time</span>
            <input
              type="datetime-local"
              value={scheduledAt}
              onChange={(event) => setScheduledAt(event.target.value)}
              required
            />
          </label>
        </div>

        <div className="campaignFormGrid">
          <label className="formField">
            <span>Email Template</span>
            <select
              value={templateId}
              onChange={(event) => setTemplateId(event.target.value)}
              required
            >
              <option value="">Select template</option>
              {templates.map((template) => (
                <option key={template.id} value={template.id}>
                  {template.name}
                </option>
              ))}
            </select>
          </label>

          <label className="formField">
            <span>From Name</span>
            <input
              value={fromName}
              onChange={(event) => setFromName(event.target.value)}
              placeholder="Brand name"
            />
          </label>

          <label className="formField">
            <span>From Email</span>
            <input
              type="email"
              value={fromEmail}
              onChange={(event) => setFromEmail(event.target.value)}
              placeholder="verified@example.com"
            />
          </label>
        </div>

        <label className="formField">
          <span>Reply-To Email</span>
          <input
            type="email"
            value={replyTo}
            onChange={(event) => setReplyTo(event.target.value)}
            placeholder="support@example.com"
          />
        </label>

        <div className="campaignRecipientPanel">
          <div className="flexBetween">
            <div>
              <h3>Target Contact Lists</h3>
              <p className="muted">
                Campaigns send through contact lists. Selected lists create email jobs for their members.
              </p>
            </div>

            <div className="statusPill active">
              <Users size={14} />
              {totalRecipients} recipients
            </div>
          </div>

          {contactLists.length === 0 ? (
            <div className="emptyState">
              <Users size={28} />
              <strong>No contact list found.</strong>
              <span>Create a contact list first from the Contacts module.</span>
            </div>
          ) : (
            <div className="campaignListSelector">
              {contactLists.map((list) => {
                const selected = selectedListIds.includes(list.id);

                return (
                  <button
                    key={list.id}
                    type="button"
                    className={selected ? "campaignListCard selected" : "campaignListCard"}
                    onClick={() => toggleList(list.id)}
                  >
                    <div className="campaignListIcon">
                      {selected ? <CheckCircle2 size={20} /> : <Users size={20} />}
                    </div>

                    <div>
                      <strong>{list.name}</strong>
                      <span>
                        {list.total_contacts ?? 0} contacts · {list.list_type || "static"}
                      </span>
                    </div>
                  </button>
                );
              })}
            </div>
          )}
        </div>

        <div className="campaignSubmitBar">
          <div className="campaignSubmitMeta">
            <span>
              <Mail size={15} />
              Template: {selectedTemplate?.name || "Not selected"}
            </span>
            <span>
              <CalendarClock size={15} />
              Local time selected, UTC sent to backend
            </span>
          </div>

          <button type="submit" disabled={loading}>
            <Send size={16} />
            {isEditing ? "Save Campaign" : "Create Campaign"}
          </button>
        </div>
      </form>
    </section>
  );
}
