"use client";

import { ReactNode } from "react";

export function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <label className="formField">
      <span>{label}</span>
      {children}
    </label>
  );
}

export function Toggle({
  checked,
  onChange,
}: {
  checked: boolean;
  onChange: (value: boolean) => void;
}) {
  return (
    <button
      type="button"
      className={checked ? "toggle active" : "toggle"}
      onClick={() => onChange(!checked)}
    >
      <span>{checked ? "Enabled" : "Disabled"}</span>
    </button>
  );
}

export function PlanCard({ label, value }: { label: string; value: string | number }) {
  return (
    <article className="planCard">
      <span>{label}</span>
      <strong>{value}</strong>
    </article>
  );
}
