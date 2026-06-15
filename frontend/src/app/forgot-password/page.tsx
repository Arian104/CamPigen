"use client";
import Image from "next/image";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { ArrowLeft, ArrowRight, Mail, ShieldCheck } from "lucide-react";

import styles from "./Auth.module.css";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setLoading(true);
    setMessage("");
    setError("");

    try {
      const apiBase =
        process.env.NEXT_PUBLIC_API_BASE_URL ||
        window.localStorage.getItem("platform_api_base") ||
        "http://127.0.0.1:8000/api";

      const response = await fetch(
        `${apiBase.replace(/\/$/, "")}/v1/accounts/password-reset/request/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email }),
        }
      );

      if (!response.ok) {
        const data = await response.json().catch(() => null);
        setError(data?.detail || "Could not send password reset email.");
        setLoading(false);
        return;
      }

      setMessage("If this email exists, a password reset link has been sent.");
    } catch {
      setError("Could not connect to the backend.");
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
              <span>Let your campaigns take flight.</span>
            </div>
          </div>

          <div className={styles.brandContent}>
            <span className={styles.badge}>
              <ShieldCheck size={16} />
              Secure reset
            </span>

            <h1>Reset your password and regain dashboard access.</h1>

            <p>
              Enter your account email address. If the account exists, you will
              receive a secure password reset link.
            </p>
          </div>

          <Link href="/login" className={styles.submitButton}>
            <ArrowLeft size={18} />
            Back to login
          </Link>
        </aside>

        <section className={styles.formPanel}>
          <div className={styles.formHeader}>
            <div className={styles.icon}>
              <Mail size={24} />
            </div>

            <div>
              <h2>Forgot password?</h2>
              <p className={styles.switchText}>
                Enter your email to request a reset link.
              </p>
            </div>
          </div>

          <form className={styles.form} onSubmit={onSubmit}>
            <label className={styles.inputField}>
              <span>Email address</span>
              <div>
                <Mail size={18} />
                <input
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  placeholder="you@example.com"
                  type="email"
                  required
                />
              </div>
            </label>

            <button type="submit" className={styles.submitButton} disabled={loading}>
              {loading ? "Sending..." : "Send reset link"}
              <ArrowRight size={18} />
            </button>
          </form>

          {message ? <p className={styles.switchText}>{message}</p> : null}
          {error ? <p className={styles.error}>{error}</p> : null}

          <p className={styles.switchText}>
            Remembered your password? <Link href="/login">Sign in</Link>
          </p>
        </section>
      </section>
    </main>
  );
}
