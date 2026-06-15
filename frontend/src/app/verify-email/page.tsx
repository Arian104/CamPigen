"use client";
import Image from "next/image";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { ArrowRight, CheckCircle2, MailCheck, Sparkles, XCircle } from "lucide-react";
import shared from "@/styles/shared.module.css";
import styles from "./Auth.module.css";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000/api";

export default function VerifyEmailPage() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");

  const [status, setStatus] = useState<"loading" | "success" | "failed">("loading");
  const [message, setMessage] = useState("Verifying your email address...");

  useEffect(() => {
    async function verify() {
      if (!token) {
        setStatus("failed");
        setMessage("Verification token is missing.");
        return;
      }

      const response = await fetch(`${API_BASE.replace(/\/$/, "")}/v1/accounts/verify-email/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ token }),
      });

      const body = await response.json().catch(() => null);

      if (response.ok) {
        setStatus("success");
        setMessage(body?.message || "Email verified successfully.");
      } else {
        setStatus("failed");
        setMessage(body?.message || "Email verification failed.");
      }
    }

    void verify();
  }, [token]);

  const success = status === "success";

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
            <div className={styles.badge}>
              <Sparkles size={15} />
              Account protection
            </div>

            <h1>Verify your email to secure your account.</h1>

            <p>
              Verified accounts can receive security alerts, password reset emails,
              and trusted workspace notifications.
            </p>
          </div>
        </aside>

        <section className={styles.formPanel}>
          <div className={success ? `${styles.statusIcon} ${styles.success}` : `${styles.statusIcon} ${styles.failed}`}>
            {status === "loading" ? (
              <MailCheck size={34} />
            ) : success ? (
              <CheckCircle2 size={34} />
            ) : (
              <XCircle size={34} />
            )}
          </div>

          <div className={`${styles.formHeader} ${styles.formHeaderCenter}`}>
            <div>
              <p className={shared.eyebrow}>Email Verification</p>
              <h2>{success ? "Email verified" : status === "loading" ? "Verifying..." : "Verification failed"}</h2>
              <p className={shared.muted}>{message}</p>
            </div>
          </div>

          <Link href="/login" className={styles.submitButton}>
            Go to login
            <ArrowRight size={17} />
          </Link>
        </section>
      </section>
    </main>
  );
}
