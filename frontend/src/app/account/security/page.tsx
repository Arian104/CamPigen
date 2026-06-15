"use client";

import { FormEvent, useState } from "react";
import { KeyRound, MailCheck, Send, ShieldCheck } from "lucide-react";

import { usePlatform } from "@/components/platform-context";
import shared from "@/styles/shared.module.css";
import styles from "../Account.module.css";

export default function AccountSecurityPage() {
  const { request } = usePlatform();

  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [newPasswordConfirm, setNewPasswordConfirm] = useState("");
  const [message, setMessage] = useState("Manage password and email verification.");
  const [loading, setLoading] = useState(false);

  async function changePassword(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);

    const result = await request("/v1/accounts/change-password/", {
      method: "POST",
      body: JSON.stringify({
        old_password: oldPassword,
        new_password: newPassword,
        new_password_confirm: newPasswordConfirm,
      }),
    });

    if (result.ok) {
      setOldPassword("");
      setNewPassword("");
      setNewPasswordConfirm("");
      setMessage("Password changed successfully.");
    } else {
      setMessage(`Password change failed: ${JSON.stringify(result.body)}`);
    }

    setLoading(false);
  }

  async function sendVerificationEmail() {
    setLoading(true);

    const result = await request("/v1/accounts/send-verification-email/", {
      method: "POST",
    });

    if (result.ok) {
      setMessage("Verification email sent.");
    } else {
      setMessage("Could not send verification email.");
    }

    setLoading(false);
  }

  return (
    <main className={shared.page}>
      <section className={styles.hero}>
        <div>
          <p className={shared.eyebrow}>Security Center</p>
          <h1>Account Security</h1>
          <p>{message}</p>
        </div>

        <div className={styles.securityBadge}>
          <ShieldCheck size={34} />
          <strong>Security Settings</strong>
          <span>Password, verification, and access protection.</span>
        </div>
      </section>

      <section className={styles.accountGrid}>
        <form className={shared.card} onSubmit={changePassword}>
          <div>
            <h2>Change Password</h2>
            <p className={shared.muted}>Use a strong password that you do not use elsewhere.</p>
          </div>

          <label className={shared.formField}>
            <span>Current Password</span>
            <input
              type="password"
              value={oldPassword}
              onChange={(event) => setOldPassword(event.target.value)}
              required
            />
          </label>

          <label className={shared.formField}>
            <span>New Password</span>
            <input
              type="password"
              value={newPassword}
              onChange={(event) => setNewPassword(event.target.value)}
              required
            />
          </label>

          <label className={shared.formField}>
            <span>Confirm New Password</span>
            <input
              type="password"
              value={newPasswordConfirm}
              onChange={(event) => setNewPasswordConfirm(event.target.value)}
              required
            />
          </label>

          <button type="submit" disabled={loading}>
            <KeyRound size={16} />
            Change Password
          </button>
        </form>

        <section className={shared.card}>
          <div>
            <h2>Email Verification</h2>
            <p className={shared.muted}>Send a verification email to confirm your account identity.</p>
          </div>

          <button type="button" onClick={sendVerificationEmail} disabled={loading}>
            <Send size={16} />
            Send Verification Email
          </button>

          <div className={styles.infoBox}>
            <MailCheck size={20} />
            <span>
              Verification links are sent to your account email and expire automatically.
            </span>
          </div>
        </section>
      </section>
    </main>
  );
}
