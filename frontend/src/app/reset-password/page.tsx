"use client";
import Image from "next/image";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useSearchParams } from "next/navigation";
import { ArrowRight, CheckCircle2, KeyRound, LockKeyhole, Sparkles } from "lucide-react";
import shared from "@/styles/shared.module.css";
import styles from "./Auth.module.css";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000/api";

export default function ResetPasswordPage() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token") || "";

  const [newPassword, setNewPassword] = useState("");
  const [newPasswordConfirm, setNewPasswordConfirm] = useState("");

  const [message, setMessage] = useState("Enter and confirm your new password.");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");

    const response = await fetch(`${API_BASE.replace(/\/$/, "")}/v1/accounts/reset-password/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        token,
        new_password: newPassword,
        new_password_confirm: newPasswordConfirm,
      }),
    });

    const body = await response.json().catch(() => null);

    if (response.ok) {
      setSuccess(true);
      setMessage(body?.message || "Password reset successfully.");
    } else {
      setError(JSON.stringify(body) || "Password reset failed.");
    }

    setLoading(false);
  }

  return (
    <main className={styles.page}>
      <section className={`${styles.shell} ${styles.compact}`}>
        <aside className={styles.brandPanel}>
          <div className={styles.brandTop}>
            <div className={styles.brandLogo}>
              <Image
                src="/campigen-logo.png"
                alt="CamPigen logo"
                width={52}
                height={52}
                priority
                className={styles.lightLogo}
              />
              <Image
                src="/image.png"
                alt="CamPigen logo"
                width={52}
                height={52}
                priority
                className={styles.darkLogo}
              />
            </div>
            <div>
              <strong>CamPigen</strong>
              <span>Create a new password</span>
            </div>
          </div>

          <div className={styles.brandContent}>
            <div className={styles.badge}>
              <Sparkles size={15} />
              Protected reset
            </div>

            <h1>Set a new password for your account.</h1>

            <p>
              Use a strong password to protect your organization dashboard and email
              operations.
            </p>
          </div>
        </aside>

        <section className={styles.formPanel}>
          <div className={styles.formHeader}>
            <div className={styles.icon}>
              {success ? <CheckCircle2 size={24} /> : <KeyRound size={24} />}
            </div>

            <div>
              <p className={shared.eyebrow}>Account Recovery</p>
              <h2>{success ? "Password changed" : "Reset password"}</h2>
              <p className={shared.muted}>{message}</p>
            </div>
          </div>

          {!success ? (
            <form className={styles.form} onSubmit={submit}>
              <label className={styles.inputField}>
                <span>New Password</span>
                <div>
                  <LockKeyhole size={18} />
                  <input
                    type="password"
                    placeholder="New password"
                    value={newPassword}
                    onChange={(event) => setNewPassword(event.target.value)}
                    required
                  />
                </div>
              </label>

              <label className={styles.inputField}>
                <span>Confirm New Password</span>
                <div>
                  <LockKeyhole size={18} />
                  <input
                    type="password"
                    placeholder="Confirm password"
                    value={newPasswordConfirm}
                    onChange={(event) => setNewPasswordConfirm(event.target.value)}
                    required
                  />
                </div>
              </label>

              <button type="submit" className={styles.submitButton} disabled={loading || !token}>
                {loading ? "Resetting..." : "Reset password"}
                <ArrowRight size={17} />
              </button>
            </form>
          ) : (
            <Link href="/login" className={styles.submitButton}>
              Go to login
              <ArrowRight size={17} />
            </Link>
          )}

          {error ? <p className={styles.error}>{error}</p> : null}

          {!token ? <p className={styles.error}>Reset token is missing.</p> : null}
        </section>
      </section>
    </main>
  );
}
