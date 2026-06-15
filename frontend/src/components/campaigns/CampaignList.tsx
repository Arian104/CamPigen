"use client";

import { Edit3, Mail, MousePointerClick } from "lucide-react";

import { Campaign } from "./CampaignTypes";

type Props = {
  campaigns: Campaign[];
  onEdit: (campaign: Campaign) => void;
};

function formatDate(value?: string | null) {
  if (!value) return "-";

  try {
    return new Date(value).toLocaleString();
  } catch {
    return "-";
  }
}

function statusClass(status?: string) {
  if (status === "completed" || status === "sent") return "statusPill active";
  if (status === "failed" || status === "cancelled") return "statusPill suspended";
  return "statusPill";
}

export function CampaignList({ campaigns, onEdit }: Props) {
  return (
    <section className="card">
      <div className="flexBetween">
        <div>
          <h2>Campaigns</h2>
          <p className="muted">
            Campaign schedule, status, delivery count, and edit actions.
          </p>
        </div>
      </div>

      <div className="tableWrap">
        <table className="dataTable campaignTable">
          <thead>
            <tr>
              <th>Campaign</th>
              <th>Status</th>
              <th>Scheduled</th>
              <th>Sent</th>
              <th>Clicks</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            {campaigns.length === 0 ? (
              <tr>
                <td colSpan={6} className="centerText muted">
                  No campaigns found.
                </td>
              </tr>
            ) : (
              campaigns.map((campaign) => (
                <tr key={campaign.id}>
                  <td>
                    <strong>{campaign.name || "Untitled campaign"}</strong>
                    <span>{campaign.subject || "No subject"}</span>
                  </td>

                  <td>
                    <span className={statusClass(campaign.status)}>
                      {campaign.status || "draft"}
                    </span>
                  </td>

                  <td>{formatDate(campaign.scheduled_at)}</td>

                  <td>
                    <div className="miniStack">
                      <span>
                        <Mail size={13} /> {campaign.total_sent ?? 0}
                      </span>
                    </div>
                  </td>

                  <td>
                    <div className="miniStack">
                      <span>
                        <MousePointerClick size={13} /> {campaign.total_clicks ?? 0}
                      </span>
                    </div>
                  </td>

                  <td>
                    <button
                      type="button"
                      className="smallButton"
                      onClick={() => onEdit(campaign)}
                    >
                      <Edit3 size={14} />
                      Edit
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
