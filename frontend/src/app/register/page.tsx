"use client";
import Image from "next/image";

import Link from "next/link";
import { FormEvent, useState } from "react";
import {
  ArrowRight,
  Building2,
  CheckCircle2,
  LockKeyhole,
  Mail,
  Sparkles,
  User,
} from "lucide-react";

import styles from "./Auth.module.css";

export default function RegisterPage() {
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    username: "",
    email: "",
    password: "",
    confirm_password: "",
  });

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function updateField(name: string, value: string) {
    setForm((current) => ({
      ...current,
      [name]: value,
    }));
  }

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setLoading(true);
    setMessage("");
    setError("");

    if (form.password !== form.confirm_password) {
      setError("Passwords do not match.");
      setLoading(false);
      return;
    }

    try {
      const apiBase =
        process.env.NEXT_PUBLIC_API_BASE_URL ||
        window.localStorage.getItem("platform_api_base") ||
        "http://127.0.0.1:8000/api";

      const response = await fetch(`${apiBase.replace(/\/$/, "")}/v1/accounts/register/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      if (!response.ok) {
        const data = await response.json().catch(() => null);
        setError(data?.detail || "Registration failed.");
        setLoading(false);
        return;
      }

      setMessage("Account created successfully. You can now sign in.");
    } catch {
      setError("Could not connect to the backend.");
    }

    setLoading(false);
  }

  return (
    <main className={styles.page}>
      <section className={`${styles.shell} ${styles.reverse}`}>
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
              <Sparkles size={16} />
              SaaS-ready registration
            </span>

            <h1>Create your account and start managing email operations.</h1>

            <p>
              Register your user account, create your default organization, and
              prepare your dashboard for campaigns, contacts, SMTP, and analytics.
            </p>
          </div>

          <div className={styles.featureList}>
            <div>
              <CheckCircle2 size={18} />
              Organization workspace setup
            </div>
            <div>
              <CheckCircle2 size={18} />
              Profile and account personalization
            </div>
            <div>
              <CheckCircle2 size={18} />
              Email verification ready
            </div>
          </div>
        </aside>

        <section className={styles.formPanel}>
          <div className={styles.formHeader}>
            <div className={styles.icon}>
              <Building2 size={24} />
            </div>

            <div>
              <h2>Create account</h2>
              <p className={styles.switchText}>
                Fill in your details to create your SaaS workspace.
              </p>
            </div>
          </div>

          <form className={styles.form} onSubmit={onSubmit}>
            <div className={styles.twoCol}>
              <label className={styles.inputField}>
                <span>First name</span>
                <div>
                  <User size={18} />
                  <input
                    value={form.first_name}
                    onChange={(event) => updateField("first_name", event.target.value)}
                    placeholder="First name"
                  />
                </div>
              </label>

              <label className={styles.inputField}>
                <span>Last name</span>
                <div>
                  <User size={18} />
                  <input
                    value={form.last_name}
                    onChange={(event) => updateField("last_name", event.target.value)}
                    placeholder="Last name"
                  />
                </div>
              </label>
            </div>

            <label className={styles.inputField}>
              <span>Username</span>
              <div>
                <User size={18} />
                <input
                  value={form.username}
                  onChange={(event) => updateField("username", event.target.value)}
                  placeholder="username"
                  required
                />
              </div>
            </label>

            <label className={styles.inputField}>
              <span>Email address</span>
              <div>
                <Mail size={18} />
                <input
                  value={form.email}
                  onChange={(event) => updateField("email", event.target.value)}
                  placeholder="you@example.com"
                  type="email"
                  required
                />
              </div>
            </label>

            <div className={styles.twoCol}>
              <label className={styles.inputField}>
                <span>Password</span>
                <div>
                  <LockKeyhole size={18} />
                  <input
                    value={form.password}
                    onChange={(event) => updateField("password", event.target.value)}
                    placeholder="Password"
                    type="password"
                    required
                  />
                </div>
              </label>

              <label className={styles.inputField}>
                <span>Confirm password</span>
                <div>
                  <LockKeyhole size={18} />
                  <input
                    value={form.confirm_password}
                    onChange={(event) =>
                      updateField("confirm_password", event.target.value)
                    }
                    placeholder="Confirm"
                    type="password"
                    required
                  />
                </div>
              </label>
            </div>

            <button type="submit" className={styles.submitButton} disabled={loading}>
              {loading ? "Creating account..." : "Create account"}
              <ArrowRight size={18} />
            </button>
          </form>

          {message ? <p className={styles.switchText}>{message}</p> : null}
          {error ? <p className={styles.error}>{error}</p> : null}

          <p className={styles.switchText}>
            Already have an account? <Link href="/login">Sign in</Link>
          </p>
        </section>
      </section>
    </main>
  );
}
