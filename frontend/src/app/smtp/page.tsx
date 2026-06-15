"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import { Activity, Pause, Play, RefreshCw, RotateCcw, Send, TestTube2 } from "lucide-react";

import { usePlatform } from "@/components/platform-context";
import shared from "@/styles/shared.module.css";
import styles from "./Smtp.module.css";

type SmtpConfig = {
  id: string;
  name?: string;
  smtp_type?: string;
  host?: string;
  port?: number;
  username?: string;
  use_tls?: boolean;
  use_ssl?: boolean;
  from_email?: string;
  from_name?: string;
  reply_to_email?: string;
  priority?: number;
  is_active?: boolean;
  is_default?: boolean;
  daily_limit?: number;
  hourly_limit?: number;
  minute_limit?: number;
  sent_today?: number;
  sent_this_hour?: number;
  sent_this_minute?: number;
  daily_remaining?: number;
  hourly_remaining?: number;
  minute_remaining?: number;
  failure_count?: number;
  success_count?: number;
  health_score?: number;
  cooldown_until?: string | null;
  is_in_cooldown?: boolean;
  last_used_at?: string | null;
  last_tested_at?: string | null;
  last_test_status?: string;
  last_test_message?: string;
  allowed_email_types?: string[];
};

type SmtpSummary = {
  total: number;
  active: number;
  inactive: number;
  cooling_down: number;
  total_sent_today: number;
  total_sent_hour: number;
  avg_health: number;
  total_failures: number;
};

const EMPTY_FORM = {
  name: "Primary SMTP",
  smtp_type: "custom",
  host: "smtp.gmail.com",
  port: 587,
  username: "",
  password: "",
  use_tls: true,
  use_ssl: false,
  from_email: "",
  from_name: "",
  reply_to_email: "",
  priority: 10,
  daily_limit: 300,
  hourly_limit: 50,
  minute_limit: 5,
  is_active: true,
  allowed_email_types: ["campaign", "transactional", "otp", "notification", "custom"],
};

export default function SmtpPage() {
  const { request } = usePlatform();

  const [configs, setConfigs] = useState<SmtpConfig[]>([]);
  const [summary, setSummary] = useState<SmtpSummary | null>(null);
  const [form, setForm] = useState({ ...EMPTY_FORM });
  const [editingId, setEditingId] = useState<string | null>(null);
  const [testEmail, setTestEmail] = useState("");
  const [message, setMessage] = useState("No SMTP activity yet.");
  const [loading, setLoading] = useState(false);

  const activeCount = summary?.active ?? configs.filter((item) => item.is_active).length;
  const avgHealth = summary?.avg_health ?? 0;

  const sortedConfigs = useMemo(() => {
    return [...configs].sort((a, b) => {
      const pA = a.priority ?? 10;
      const pB = b.priority ?? 10;
      if (pA !== pB) return pA - pB;
      return (b.health_score ?? 0) - (a.health_score ?? 0);
    });
  }, [configs]);

  function updateForm(key: keyof typeof EMPTY_FORM, value: string | number | boolean | string[]) {
    setForm((current) => ({
      ...current,
      [key]: value,
    }));
  }

  async function loadConfigs() {
    setLoading(true);

    const [configsRes, summaryRes] = await Promise.all([
      request("/v1/smtp-configs/"),
      request("/v1/smtp-configs/summary/"),
    ]);

    if (configsRes.ok) {
      const data = configsRes.body as { results?: SmtpConfig[] } | SmtpConfig[];
      const rows = Array.isArray(data) ? data : data.results ?? [];
      setConfigs(rows);
      setMessage(`Loaded ${rows.length} SMTP configurations.`);
    } else {
      setMessage("Failed to load SMTP configurations.");
    }

    if (summaryRes.ok && typeof summaryRes.body === "object" && summaryRes.body) {
      setSummary(summaryRes.body as SmtpSummary);
    }

    setLoading(false);
  }

  async function saveConfig(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);

    const payload = {
      ...form,
      port: Number(form.port),
      priority: Number(form.priority),
      daily_limit: Number(form.daily_limit),
      hourly_limit: Number(form.hourly_limit),
      minute_limit: Number(form.minute_limit),
    };

    if (!payload.password) {
      delete (payload as Partial<typeof payload>).password;
    }

    const endpoint = editingId ? `/v1/smtp-configs/${editingId}/` : "/v1/smtp-configs/";
    const method = editingId ? "PATCH" : "POST";

    const result = await request(endpoint, {
      method,
      body: JSON.stringify(payload),
    });

    if (result.ok) {
      setMessage(editingId ? "SMTP configuration updated." : "SMTP configuration saved.");
      setEditingId(null);
      setForm({ ...EMPTY_FORM, password: "" });
      await loadConfigs();
    } else {
      setMessage(`SMTP save failed: ${JSON.stringify(result.body)}`);
    }

    setLoading(false);
  }

  function startEdit(config: SmtpConfig) {
    setEditingId(config.id);
    setForm({
      name: config.name || "",
      smtp_type: config.smtp_type || "custom",
      host: config.host || "",
      port: config.port || 587,
      username: config.username || "",
      password: "",
      use_tls: Boolean(config.use_tls),
      use_ssl: Boolean(config.use_ssl),
      from_email: config.from_email || "",
      from_name: config.from_name || "",
      reply_to_email: config.reply_to_email || "",
      priority: config.priority ?? 10,
      daily_limit: config.daily_limit ?? 300,
      hourly_limit: config.hourly_limit ?? 50,
      minute_limit: config.minute_limit ?? 5,
      is_active: Boolean(config.is_active),
      allowed_email_types: config.allowed_email_types?.length
        ? config.allowed_email_types
        : EMPTY_FORM.allowed_email_types,
    });
    setMessage(`Editing ${config.name || config.host}`);
  }

  async function runAction(id: string, action: "test" | "pause" | "resume" | "reset_counters") {
    setLoading(true);

    const body = action === "test" ? JSON.stringify({ recipient_email: testEmail }) : undefined;

    const result = await request(`/v1/smtp-configs/${id}/${action}/`, {
      method: "POST",
      body,
    });

    if (result.ok) {
      setMessage(`${action.replace("_", " ")} completed.`);
      await loadConfigs();
    } else {
      setMessage(`${action.replace("_", " ")} failed: ${JSON.stringify(result.body)}`);
    }

    setLoading(false);
  }

  useEffect(() => {
    void loadConfigs();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <main className={shared.page}>
      <section className={`${shared.card} ${shared.flexBetween}`}>
        <div>
          <h1>SMTP Infrastructure</h1>
          <p className={shared.muted}>
            Manage SMTP pools, limits, rotation priority, health, cooldown, and sending capacity.
          </p>
          <p className={`${shared.muted} ${shared.small}`}>{message}</p>
        </div>

        <button type="button" className={shared.secondaryButton} onClick={() => void loadConfigs()}>
          <RefreshCw size={16} />
          Refresh
        </button>
      </section>

      <section className={`${shared.card} ${styles.statGrid}`}>
        <Stat title="Total SMTP" value={summary?.total ?? configs.length} />
        <Stat title="Active" value={activeCount} />
        <Stat title="Cooling Down" value={summary?.cooling_down ?? 0} />
        <Stat title="Sent Today" value={summary?.total_sent_today ?? 0} />
        <Stat title="Avg Health" value={`${avgHealth}%`} />
      </section>

      <section className={shared.card}>
        <div className={shared.flexBetween}>
          <div>
            <h2>{editingId ? "Edit SMTP Config" : "Add SMTP Config"}</h2>
            <p className={shared.muted}>
              Limits are used by the automatic SMTP router before choosing the best SMTP.
            </p>
          </div>

          {editingId ? (
            <button
              type="button"
              className={shared.secondaryButton}
              onClick={() => {
                setEditingId(null);
                setForm({ ...EMPTY_FORM });
              }}
            >
              Cancel Edit
            </button>
          ) : null}
        </div>

        <form onSubmit={saveConfig} className={styles.settingsForm}>
          <div className={shared.gridThree}>
            <Field label="Name">
              <input value={form.name} onChange={(e) => updateForm("name", e.target.value)} />
            </Field>

            <Field label="Provider Type">
              <select value={form.smtp_type} onChange={(e) => updateForm("smtp_type", e.target.value)}>
                <option value="custom">Custom</option>
                <option value="gmail">Gmail</option>
                <option value="brevo">Brevo</option>
                <option value="ses">Amazon SES</option>
                <option value="sendgrid">SendGrid</option>
              </select>
            </Field>

            <Field label="Priority">
              <input
                type="number"
                value={form.priority}
                onChange={(e) => updateForm("priority", Number(e.target.value))}
              />
            </Field>

            <Field label="Host">
              <input value={form.host} onChange={(e) => updateForm("host", e.target.value)} />
            </Field>

            <Field label="Port">
              <input
                type="number"
                value={form.port}
                onChange={(e) => updateForm("port", Number(e.target.value))}
              />
            </Field>

            <Field label="Username">
              <input value={form.username} onChange={(e) => updateForm("username", e.target.value)} />
            </Field>

            <Field label={editingId ? "Password / App Password (leave blank to keep old)" : "Password / App Password"}>
              <input
                type="password"
                value={form.password}
                onChange={(e) => updateForm("password", e.target.value)}
              />
            </Field>

            <Field label="From Name">
              <input value={form.from_name} onChange={(e) => updateForm("from_name", e.target.value)} />
            </Field>

            <Field label="From Email">
              <input value={form.from_email} onChange={(e) => updateForm("from_email", e.target.value)} />
            </Field>

            <Field label="Reply-To Email">
              <input value={form.reply_to_email} onChange={(e) => updateForm("reply_to_email", e.target.value)} />
            </Field>

            <Field label="Daily Limit">
              <input
                type="number"
                value={form.daily_limit}
                onChange={(e) => updateForm("daily_limit", Number(e.target.value))}
              />
            </Field>

            <Field label="Hourly Limit">
              <input
                type="number"
                value={form.hourly_limit}
                onChange={(e) => updateForm("hourly_limit", Number(e.target.value))}
              />
            </Field>

            <Field label="Minute Limit">
              <input
                type="number"
                value={form.minute_limit}
                onChange={(e) => updateForm("minute_limit", Number(e.target.value))}
              />
            </Field>
          </div>

          <div className={styles.toggleRow}>
            <Toggle label="Use TLS" checked={form.use_tls} onChange={(value) => updateForm("use_tls", value)} />
            <Toggle label="Use SSL" checked={form.use_ssl} onChange={(value) => updateForm("use_ssl", value)} />
            <Toggle label="Active" checked={form.is_active} onChange={(value) => updateForm("is_active", value)} />
          </div>

          <button type="submit" disabled={loading}>
            {editingId ? "Update SMTP Config" : "Save SMTP Config"}
          </button>
        </form>
      </section>

      <section className={shared.card}>
        <div className={shared.flexBetween}>
          <div>
            <h2>SMTP Pool</h2>
            <p className={shared.muted}>Automatic rotation uses priority, health, usage counters, and cooldown.</p>
          </div>

          <Field label="Test recipient">
            <input
              value={testEmail}
              onChange={(e) => setTestEmail(e.target.value)}
              placeholder="Optional test email"
            />
          </Field>
        </div>

        <div className={shared.tableWrap}>
          <table className={`${shared.dataTable} ${styles.smtpTable}`}>
            <thead>
              <tr>
                <th>Name</th>
                <th>Provider</th>
                <th>Host</th>
                <th>Priority</th>
                <th>Usage</th>
                <th>Health</th>
                <th>Cooldown</th>
                <th>Last Test</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>
              {sortedConfigs.length === 0 ? (
                <tr>
                  <td colSpan={10} className={`${shared.muted} ${shared.centerText}`}>
                    No SMTP configuration found.
                  </td>
                </tr>
              ) : (
                sortedConfigs.map((config) => (
                  <tr key={config.id}>
                    <td>
                      <strong>{config.name || "-"}</strong>
                      <span className={`${shared.muted} ${shared.small}`}>{config.username}</span>
                    </td>

                    <td>{config.smtp_type || "custom"}</td>
                    <td>
                      {config.host}:{config.port}
                    </td>
                    <td>{config.priority ?? "-"}</td>

                    <td>
                      <div className={styles.usage}>
                        <span>Day: {config.sent_today ?? 0}/{config.daily_limit ?? 0}</span>
                        <span>Hour: {config.sent_this_hour ?? 0}/{config.hourly_limit ?? 0}</span>
                        <span>Min: {config.sent_this_minute ?? 0}/{config.minute_limit ?? 0}</span>
                      </div>
                    </td>

                    <td>
                      <HealthBadge score={config.health_score ?? 0} failures={config.failure_count ?? 0} />
                    </td>

                    <td>
                      {config.is_in_cooldown ? (
                        <span className={`${shared.statusPill} ${shared.statusDanger}`}>Cooling</span>
                      ) : (
                        <span className={`${shared.statusPill} ${shared.statusActive}`}>Ready</span>
                      )}
                    </td>

                    <td>
                      <div className={styles.usage}>
                        <span>{config.last_test_status || "Not tested"}</span>
                        <span className={`${shared.muted} ${shared.small}`}>{formatDate(config.last_tested_at)}</span>
                      </div>
                    </td>

                    <td>
                      {config.is_active ? (
                        <span className={`${shared.statusPill} ${shared.statusActive}`}>Active</span>
                      ) : (
                        <span className={`${shared.statusPill} ${shared.statusDanger}`}>Paused</span>
                      )}
                    </td>

                    <td>
                      <div className={styles.actions}>
                        <button type="button" className={shared.smallButton} onClick={() => startEdit(config)}>
                          Edit
                        </button>

                        <button type="button" className={shared.smallButton} onClick={() => void runAction(config.id, "test")}>
                          <TestTube2 size={14} />
                        </button>

                        {config.is_active ? (
                          <button type="button" className={shared.smallButton} onClick={() => void runAction(config.id, "pause")}>
                            <Pause size={14} />
                          </button>
                        ) : (
                          <button type="button" className={shared.smallButton} onClick={() => void runAction(config.id, "resume")}>
                            <Play size={14} />
                          </button>
                        )}

                        <button type="button" className={shared.smallButton} onClick={() => void runAction(config.id, "reset_counters")}>
                          <RotateCcw size={14} />
                        </button>
                      </div>
                    </td>
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

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className={shared.formField}>
      <span>{label}</span>
      {children}
    </label>
  );
}

function Toggle({
  label,
  checked,
  onChange,
}: {
  label: string;
  checked: boolean;
  onChange: (value: boolean) => void;
}) {
  return (
    <button
      type="button"
      className={checked ? "toggle active" : "toggle"}
      onClick={() => onChange(!checked)}
    >
      <span>{label}: {checked ? "Yes" : "No"}</span>
    </button>
  );
}

function Stat({ title, value }: { title: string; value: string | number }) {
  return (
    <article className={styles.statItem}>
      <h3>{title}</h3>
      <p>{value}</p>
    </article>
  );
}

function HealthBadge({ score, failures }: { score: number; failures: number }) {
  let status = "Good";
  let className = `${shared.statusPill} ${shared.statusActive}`;

  if (score < 70) {
    status = "Weak";
    className = `${shared.statusPill} ${shared.statusDanger}`;
  } else if (score < 90) {
    status = "Watch";
    className = shared.statusPill;
  }

  return (
    <div className={styles.usage}>
      <span className={className}>
        <Activity size={13} />
        {status} {Math.round(score)}%
      </span>
      <span className={`${shared.muted} ${shared.small}`}>Failures: {failures}</span>
    </div>
  );
}

function formatDate(value?: string | null) {
  if (!value) return "-";

  try {
    return new Date(value).toLocaleString();
  } catch {
    return "-";
  }
}
