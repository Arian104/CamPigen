"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import {
  Mail,
  Send,
  User,
  Users,
  Server,
  Sparkles,
  ShieldCheck,
  Zap,
} from "lucide-react";

import { usePlatform } from "@/components/platform-context";
import shared from "@/styles/shared.module.css";
import styles from "./InstantSend.module.css";

type Contact = {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
};

type SMTPConfig = {
  id: string;
  name: string;
  host: string;
  from_email?: string;
  is_active?: boolean;
};

export default function InstantSendPage() {
  const { request } = usePlatform();

  const [contacts, setContacts] = useState<Contact[]>([]);
  const [smtpConfigs, setSmtpConfigs] = useState<SMTPConfig[]>([]);

  const [selectedContact, setSelectedContact] = useState("");
  const [recipientEmail, setRecipientEmail] = useState("");

  const [selectedSMTP, setSelectedSMTP] = useState("");

  const [subject, setSubject] = useState("");
  const [htmlBody, setHtmlBody] = useState(
    `<h1>Hello</h1><p>Instant email from dashboard.</p>`
  );

  const [priority, setPriority] = useState(5);

  const [loading, setLoading] = useState(false);

  const [message, setMessage] = useState(
    "Send direct emails through your SMTP infrastructure."
  );

  useEffect(() => {
    void loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function loadData() {
    const [contactsRes, smtpRes] = await Promise.all([
      request("/v1/contacts/"),
      request("/v1/smtp-configs/"),
    ]);

    const contactsBody = Array.isArray(contactsRes.body)
      ? contactsRes.body
      : contactsRes.body?.results || [];

    const smtpBody = Array.isArray(smtpRes.body)
      ? smtpRes.body
      : smtpRes.body?.results || [];

    setContacts(contactsBody);
    setSmtpConfigs(smtpBody);

    if (smtpBody.length > 0) {
      setSelectedSMTP(smtpBody[0].id);
    }
  }

  useEffect(() => {
    const contact = contacts.find((c) => c.id === selectedContact);

    if (contact?.email) {
      setRecipientEmail(contact.email);
    }
  }, [selectedContact, contacts]);

  const selectedSMTPObject = useMemo(() => {
    return smtpConfigs.find((smtp) => smtp.id === selectedSMTP);
  }, [smtpConfigs, selectedSMTP]);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setLoading(true);

    const result = await request(
      "/send-email/",
      {
        method: "POST",
        body: JSON.stringify({
          recipient_email: recipientEmail,
          subject,
          html_body: htmlBody,
          email_type: "custom",
          priority,
          smtp_config_id: selectedSMTP || null,
        }),
      },
      true
    );

    if (result.ok) {
      setMessage("Email queued successfully.");
      setSubject("");
    } else {
      setMessage("Failed to queue email.");
    }

    setLoading(false);
  }

  return (
    <main className={`${shared.page} ${styles.page}`}>
      <section className={styles.hero}>
        <div>
          <p className={shared.eyebrow}>DIRECT DELIVERY</p>

          <h1>Instant Email Dispatch</h1>

          <p>
            Send transactional or manual emails directly through your SMTP
            infrastructure with queue priority, contact integration, and custom
            routing.
          </p>

          <div className={styles.heroMeta}>
            <span>
              <Zap size={15} />
              Real-time queue
            </span>

            <span>
              <ShieldCheck size={15} />
              Organization scoped
            </span>

            <span>
              <Server size={15} />
              SMTP routed
            </span>
          </div>
        </div>

        <div className={styles.heroCard}>
          <Sparkles size={24} />

          <strong>
            {smtpConfigs.length} SMTP
            {smtpConfigs.length !== 1 ? "s" : ""} available
          </strong>

          <span>
            Connected to your delivery infrastructure and organization routing
            system.
          </span>
        </div>
      </section>

      <section className={styles.grid}>
        <section className={`${shared.card} ${styles.formCard}`}>
          <div className={shared.flexBetween}>
            <div>
              <h2>Compose Email</h2>
              <p className={shared.muted}>
                Send an instant email without creating a campaign.
              </p>
            </div>

            <div className={`${shared.statusPill} ${shared.statusActive}`}>
              <Mail size={14} />
              Queue Ready
            </div>
          </div>

          <form className={styles.modernForm} onSubmit={onSubmit}>
            <div className={styles.formGrid}>
              <label className={shared.formField}>
                <span>Select Contact</span>

                <select
                  value={selectedContact}
                  onChange={(event) =>
                    setSelectedContact(event.target.value)
                  }
                >
                  <option value="">Manual Recipient</option>

                  {contacts.map((contact) => (
                    <option key={contact.id} value={contact.id}>
                      {contact.first_name || contact.last_name
                        ? `${contact.first_name || ""} ${
                            contact.last_name || ""
                          }`
                        : contact.email}
                    </option>
                  ))}
                </select>
              </label>

              <label className={shared.formField}>
                <span>Recipient Email</span>

                <input
                  type="email"
                  placeholder="recipient@example.com"
                  value={recipientEmail}
                  onChange={(event) =>
                    setRecipientEmail(event.target.value)
                  }
                  required
                />
              </label>

              <label className={shared.formField}>
                <span>SMTP Configuration</span>

                <select
                  value={selectedSMTP}
                  onChange={(event) =>
                    setSelectedSMTP(event.target.value)
                  }
                >
                  {smtpConfigs.map((smtp) => (
                    <option key={smtp.id} value={smtp.id}>
                      {smtp.name} • {smtp.host}
                    </option>
                  ))}
                </select>
              </label>
            </div>

            <label className={shared.formField}>
              <span>Subject</span>

              <input
                placeholder="Email subject"
                value={subject}
                onChange={(event) => setSubject(event.target.value)}
                required
              />
            </label>

            <label className={shared.formField}>
              <span>HTML Email Body</span>

              <textarea
                rows={14}
                value={htmlBody}
                onChange={(event) => setHtmlBody(event.target.value)}
                placeholder="<h1>Hello</h1>"
              />
            </label>

            <div className={styles.bottomGrid}>
              <label className={shared.formField}>
                <span>Queue Priority</span>

                <input
                  type="number"
                  min={1}
                  max={10}
                  value={priority}
                  onChange={(event) =>
                    setPriority(Number(event.target.value))
                  }
                />
              </label>

              <div className={styles.infoCard}>
                <div>
                  <strong>Selected SMTP</strong>

                  <span>
                    {selectedSMTPObject?.name || "No SMTP selected"}
                  </span>
                </div>

                <div>
                  <strong>From Address</strong>

                  <span>
                    {selectedSMTPObject?.from_email ||
                      "No sender configured"}
                  </span>
                </div>
              </div>
            </div>

            <div className={styles.actionBar}>
              <div className={styles.statusText}>
                <strong>Status</strong>
                <span>{message}</span>
              </div>

              <button type="submit" disabled={loading}>
                <Send size={16} />
                {loading ? "Queueing..." : "Send Instantly"}
              </button>
            </div>
          </form>
        </section>

        <section className={`${shared.card} ${styles.sideCard}`}>
          <h2>Quick Overview</h2>

          <div className={styles.miniCard}>
            <div className={styles.miniIcon}>
              <Users size={18} />
            </div>

            <div>
              <strong>{contacts.length}</strong>
              <span>Contacts available</span>
            </div>
          </div>

          <div className={styles.miniCard}>
            <div className={styles.miniIcon}>
              <Server size={18} />
            </div>

            <div>
              <strong>{smtpConfigs.length}</strong>
              <span>SMTP pools connected</span>
            </div>
          </div>

          <div className={styles.guide}>
            <User size={18} />

            <div>
              <strong>Contact Linked Sending</strong>

              <p>
                Emails sent using selected contacts can later be connected with
                analytics, tracked links, opens, clicks, and webhooks.
              </p>
            </div>
          </div>

          <div className={styles.guide}>
            <Zap size={18} />

            <div>
              <strong>Priority Queue</strong>

              <p>
                Higher priority emails are processed earlier by the email engine
                and SMTP router.
              </p>
            </div>
          </div>
        </section>
      </section>
    </main>
  );
}
