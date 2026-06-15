from pathlib import Path

path = Path("src/app/email-history/page.tsx")

path.write_text('''"use client";

import { useEffect, useState } from "react";

import { usePlatform } from "@/components/platform-context";
import { useOrganization } from "@/components/organization-context";

import shared from "@/styles/shared.module.css";
import styles from "./EmailHistory.module.css";

type EmailJob = {
  id: string | number;
  recipient_email?: string;
  subject_snapshot?: string;
  status?: string;
  scheduled_at?: string;
  sent_at?: string;
  error_message?: string;
};

function formatDate(value?: string) {
  if (!value) return "-";

  try {
    return new Date(value).toLocaleString();
  } catch {
    return "-";
  }
}

function statusClass(status?: string) {
  const normalized = (status || "").toLowerCase();

  if (["done", "sent", "completed", "success"].includes(normalized)) {
    return `${shared.statusPill} ${shared.statusActive}`;
  }

  if (["failed", "error", "bounced"].includes(normalized)) {
    return `${shared.statusPill} ${shared.statusDanger}`;
  }

  return shared.statusPill;
}

export default function EmailHistoryPage() {
  const { request } = usePlatform();
  const { activeOrganization } = useOrganization();

  const [jobs, setJobs] = useState<EmailJob[]>([]);
  const [message, setMessage] = useState("No email job activity yet.");

  async function loadJobs() {
    const result = await request("/v1/email-jobs/");

    if (result.ok) {
      const data = result.body as { results?: EmailJob[] } | EmailJob[];
      const rows = Array.isArray(data) ? data : data.results ?? [];
      setJobs(rows);
      setMessage(`Loaded ${rows.length} email jobs.`);
    } else {
      setMessage("Failed to load email jobs.");
    }
  }

  useEffect(() => {
    if (!activeOrganization) return;
    void loadJobs();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeOrganization?.id]);

  return (
    <main className={shared.page}>
      <section className={shared.pageHero}>
        <div>
          <p className={shared.eyebrow}>Delivery Operations</p>
          <h1>Email History</h1>
          <p>
            Track sent, queued, failed, and scheduled email jobs with delivery
            status visibility.
          </p>

          <div className={shared.heroMeta}>
            <span>{message}</span>
          </div>
        </div>

        <div className={shared.heroActions}>
          <button type="button" className={shared.secondaryButton} onClick={() => void loadJobs()}>
            Refresh
          </button>
        </div>
      </section>

      <section className={shared.card}>
        <div className={shared.flexBetween}>
          <div>
            <h2>Delivery Timeline</h2>
            <p className={shared.muted}>
              Recent email jobs from the queue and scheduler.
            </p>
          </div>

          <div className={styles.actions}>
            <button type="button" className={shared.secondaryButton} onClick={() => void loadJobs()}>
              Reload
            </button>
          </div>
        </div>

        <div className={shared.tableWrap}>
          <table className={shared.dataTable}>
            <thead>
              <tr>
                <th>Recipient</th>
                <th>Subject</th>
                <th>Status</th>
                <th>Scheduled</th>
                <th>Sent</th>
              </tr>
            </thead>

            <tbody>
              {jobs.length === 0 ? (
                <tr>
                  <td colSpan={5} className={`${shared.muted} ${shared.centerText}`}>
                    No email jobs found.
                  </td>
                </tr>
              ) : (
                jobs.map((job) => (
                  <tr key={String(job.id)}>
                    <td>{job.recipient_email ?? "-"}</td>
                    <td>
                      <strong>{job.subject_snapshot ?? "-"}</strong>

                      {job.error_message ? (
                        <div className={styles.errorBox}>{job.error_message}</div>
                      ) : null}
                    </td>
                    <td>
                      <span className={statusClass(job.status)}>
                        {job.status ?? "-"}
                      </span>
                    </td>
                    <td>{formatDate(job.scheduled_at)}</td>
                    <td>{formatDate(job.sent_at)}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
''', encoding="utf-8")

print("Updated src/app/email-history/page.tsx")
