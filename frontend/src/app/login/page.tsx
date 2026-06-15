"use client";
import Image from "next/image";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import {
  ArrowRight,
  CheckCircle2,
  LockKeyhole,
  Mail,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

import { usePlatform } from "@/components/platform-context";
import styles from "./Auth.module.css";

export default function LoginPage() {
  const router = useRouter();
  const { login } = usePlatform();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setLoading(true);
    setError("");

    const ok = await login(email, password);

    if (!ok) {
      setError("Invalid email or password.");
      setLoading(false);
      return;
    }

    router.push("/");
    setLoading(false);
  }

  return (
    <main className={styles.page}>
      <section className={styles.shell}>
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
              Modern email operations
            </span>

            <h1>Manage campaigns, contacts, SMTP, and analytics from one place.</h1>

            <p>
              Sign in to continue managing your organization, email delivery,
              templates, contacts, links, and automation dashboard.
            </p>
          </div>

          <div className={styles.featureList}>
            <div>
              <CheckCircle2 size={18} />
              Campaign scheduling and delivery tracking
            </div>
            <div>
              <CheckCircle2 size={18} />
              Organization-based SaaS workspace
            </div>
            <div>
              <CheckCircle2 size={18} />
              SMTP pool, analytics, contacts, and templates
            </div>
          </div>
        </aside>

        <section className={styles.formPanel}>
          <div className={styles.formHeader}>
            <div className={styles.icon}>
              <ShieldCheck size={24} />
            </div>

            <div>
              <h2>Welcome back</h2>
              <p className={styles.switchText}>
                Sign in to access your enterprise dashboard.
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

            <label className={styles.inputField}>
              <span>Password</span>
              <div>
                <LockKeyhole size={18} />
                <input
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  placeholder="Enter your password"
                  type="password"
                  required
                />
              </div>
            </label>

            <div className={styles.formMeta}>
              <label className={styles.remember}>
                <input type="checkbox" />
                Remember me
              </label>

              <Link href="/forgot-password">Forgot password?</Link>
            </div>

            <button type="submit" className={styles.submitButton} disabled={loading}>
              {loading ? "Signing in..." : "Sign in"}
              <ArrowRight size={18} />
            </button>
          </form>

          {error ? <p className={styles.error}>{error}</p> : null}

          <p className={styles.switchText}>
            New here? <Link href="/register">Create an account</Link>
          </p>
        </section>
      </section>
    </main>
  );
}
