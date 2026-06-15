"use client";

import { useEffect, useState } from "react";
import { Activity, Clock3 } from "lucide-react";

import { usePlatform } from "@/components/platform-context";
import { AccountActivity } from "@/types/account";
import shared from "@/styles/shared.module.css";
import styles from "../Account.module.css";

function formatDate(value?: string | null) {
  if (!value) return "-";
  return new Date(value).toLocaleString();
}

export default function AccountActivityPage() {
  const { request } = usePlatform();

  const [rows, setRows] = useState<AccountActivity[]>([]);
  const [message, setMessage] = useState("Review recent account activity.");
  const [loading, setLoading] = useState(true);

  async function loadActivity() {
    setLoading(true);

    const result = await request("/v1/accounts/activity/");

    if (result.ok && Array.isArray(result.body)) {
      setRows(result.body as AccountActivity[]);
      setMessage(`Loaded ${result.body.length} activity logs.`);
    } else {
      setMessage("Could not load account activity.");
    }

    setLoading(false);
  }

  useEffect(() => {
    void loadActivity();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <main className={shared.page}>
      <section className={`${shared.card} ${shared.flexBetween}`}>
        <div>
          <p className={shared.eyebrow}>Audit Trail</p>
          <h1>Account Activity</h1>
          <p className={shared.muted}>{message}</p>
        </div>
      </section>

      <section className={shared.card}>
        <div className={styles.timeline}>
          {loading ? (
            <p className={shared.muted}>Loading activity...</p>
          ) : rows.length === 0 ? (
            <p className={shared.muted}>No activity found.</p>
          ) : (
            rows.map((row) => (
              <article key={row.id} className={styles.timelineItem}>
                <div className={styles.timelineIcon}>
                  <Activity size={17} />
                </div>

                <div>
                  <strong>{row.action.replaceAll("_", " ")}</strong>
                  <p>{row.description || "No description."}</p>

                  <div className={styles.timelineMeta}>
                    <span>
                      <Clock3 size={13} />
                      {formatDate(row.created_at)}
                    </span>
                    <span>{row.organization_name || "No organization"}</span>
                    <span>{row.ip_address || "No IP"}</span>
                  </div>
                </div>
              </article>
            ))
          )}
        </div>
      </section>
    </main>
  );
}
