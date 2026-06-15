"use client";

import { useEffect, useMemo, useState } from "react";

import { useOrganization } from "@/components/organization-context";
import { usePlatform } from "@/components/platform-context";

import { CampaignForm } from "@/components/campaigns/CampaignForm";
import { CampaignList } from "@/components/campaigns/CampaignList";
import { TemplateEditor } from "@/components/campaigns/TemplateEditor";
import { TemplatePreview } from "@/components/campaigns/TemplatePreview";
import {
  Campaign,
  Contact,
  ContactList,
  OrganizationTemplateData,
  Template,
} from "@/components/campaigns/CampaignTypes";
import {
  buildPreviewContext,
  contextToJson,
  pickPreviewContact,
} from "@/components/campaigns/previewContext";
import shared from "@/styles/shared.module.css";
import styles from "./Campaigns.module.css";

export default function CampaignsPage() {
  const { request } = usePlatform();
  const { activeOrganization } = useOrganization();

  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [templates, setTemplates] = useState<Template[]>([]);
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [contactLists, setContactLists] = useState<ContactList[]>([]);
  const [organizationData, setOrganizationData] =
    useState<OrganizationTemplateData | null>(null);

  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);
  const [isEditingTemplate, setIsEditingTemplate] = useState(false);

  const [editingCampaign, setEditingCampaign] = useState<Campaign | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [showTemplates, setShowTemplates] = useState(false);

  const [message, setMessage] = useState("No campaign activity yet.");
  const [loading, setLoading] = useState(false);

  const previewContextRaw = useMemo(() => {
    return contextToJson(
      buildPreviewContext(organizationData, pickPreviewContact(contacts)),
    );
  }, [organizationData, contacts]);

  async function loadOrganizationDetails() {
    const result = await request("/v1/organizations/current/");

    if (result.ok && typeof result.body === "object" && result.body) {
      setOrganizationData(result.body as OrganizationTemplateData);
    } else if (activeOrganization) {
      setOrganizationData(activeOrganization as OrganizationTemplateData);
    }
  }

  async function loadCampaigns() {
    const result = await request("/v1/campaigns/");

    if (result.ok) {
      const data = result.body as { results?: Campaign[] } | Campaign[];
      const rows = Array.isArray(data) ? data : data.results ?? [];
      setCampaigns(rows);
    }
  }

  async function loadTemplates() {
    const result = await request("/v1/templates/");

    if (result.ok) {
      const data = result.body as { results?: Template[] } | Template[];
      const rows = Array.isArray(data) ? data : data.results ?? [];
      setTemplates(rows);
    }
  }

  async function loadContacts() {
    const result = await request("/v1/contacts/");

    if (result.ok) {
      const data = result.body as { results?: Contact[] } | Contact[];
      const rows = Array.isArray(data) ? data : data.results ?? [];
      setContacts(rows);
    }
  }

  async function loadContactLists() {
    const result = await request("/v1/contact-lists/");

    if (result.ok) {
      const data = result.body as { results?: ContactList[] } | ContactList[];
      const rows = Array.isArray(data) ? data : data.results ?? [];
      setContactLists(rows);
    }
  }

  async function refreshAll() {
    setLoading(true);

    await Promise.all([
      loadOrganizationDetails(),
      loadCampaigns(),
      loadTemplates(),
      loadContacts(),
      loadContactLists(),
    ]);

    setMessage("Campaign workspace refreshed with organization data.");
    setLoading(false);
  }

  function openCreate() {
    setEditingCampaign(null);
    setShowCreate((current) => !current);
    setShowTemplates(false);
  }

  function openEdit(campaign: Campaign) {
    setEditingCampaign(campaign);
    setShowCreate(true);
    setShowTemplates(false);
    setMessage(`Editing campaign: ${campaign.name}`);
  }

  function cancelEdit() {
    setEditingCampaign(null);
    setShowCreate(false);
    setMessage("Campaign edit cancelled.");
  }

  useEffect(() => {
    if (!activeOrganization) return;
    void refreshAll();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeOrganization?.id]);

  return (
    <main className={shared.page}>
      <section className={`${shared.card} ${shared.flexBetween}`}>
        <div>
          <h1>Campaign Studio</h1>
          <p className={shared.muted}>
            Create, preview, edit, and monitor campaigns for{" "}
            <strong>
              {organizationData?.brand_name ||
                activeOrganization?.name ||
                "selected organization"}
            </strong>.
          </p>
          <p className={`${shared.muted} ${shared.small}`}>{message}</p>
        </div>

        <div className={shared.actions}>
          <button type="button" className={shared.primaryButton} onClick={openCreate}>
            {showCreate ? "Close Create" : "Create Campaign"}
          </button>

          <button
            type="button"
            className={shared.secondaryButton}
            onClick={() => {
              setShowTemplates((current) => !current);
              setShowCreate(false);
              setEditingCampaign(null);
            }}
          >
            {showTemplates ? "Close Templates" : "Manage Templates"}
          </button>
        </div>
      </section>

      {showCreate ? (
        <CampaignForm
          templates={templates}
          contacts={contacts}
          contactLists={contactLists}
          organizationData={organizationData}
          loading={loading}
          editingCampaign={editingCampaign}
          onTemplateSelected={setSelectedTemplate}
          onCancelEdit={cancelEdit}
          onCreated={async () => {
            setMessage(
              editingCampaign
                ? "Campaign updated successfully."
                : "Campaign created successfully.",
            );
            setShowCreate(false);
            setEditingCampaign(null);
            await refreshAll();
          }}
        />
      ) : null}

      {showTemplates ? (
        <TemplateEditor
          templates={templates}
          contacts={contacts}
          organizationData={organizationData}
          selectedTemplate={selectedTemplate}
          setSelectedTemplate={setSelectedTemplate}
          isEditing={isEditingTemplate}
          setIsEditing={setIsEditingTemplate}
          loading={loading}
          onSaved={async () => {
            setMessage("Template saved successfully.");
            await refreshAll();
          }}
        />
      ) : null}

      {!showTemplates && selectedTemplate ? (
        <TemplatePreview
          template={selectedTemplate}
          previewContextRaw={previewContextRaw}
          isEditing={isEditingTemplate}
          onEdit={() => {
            setShowTemplates(true);
            setShowCreate(false);
            setEditingCampaign(null);
            setIsEditingTemplate(true);
          }}
        />
      ) : null}

      <CampaignList campaigns={campaigns} onEdit={openEdit} />
    </main>
  );
}
