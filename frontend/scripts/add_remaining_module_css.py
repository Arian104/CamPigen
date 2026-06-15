from pathlib import Path

def append_once(path_str, marker, css):
    path = Path(path_str)
    text = path.read_text()

    if marker in text:
        print("already exists:", marker, "in", path_str)
        return

    path.write_text(text.rstrip() + "\n\n" + css.strip() + "\n")
    print("updated:", path_str)

append_once(
    "src/app/Dashboard.module.css",
    "/* Remaining dashboard classes */",
    """
/* Remaining dashboard classes */
.activityCard,
.ratesCard {
  min-height: 320px;
}

.listIcon {
  width: 38px;
  height: 38px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  color: var(--primary);
  background: var(--primary-soft);
  flex-shrink: 0;
}
"""
)

append_once(
    "src/app/instant-send/InstantSend.module.css",
    "/* Remaining instant send classes */",
    """
/* Remaining instant send classes */
.hero {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
  padding: 30px;
  border-radius: 30px;
  color: #ffffff;
  box-shadow: var(--shadow-lg);
  background:
    radial-gradient(circle at top left, color-mix(in srgb, var(--primary) 38%, transparent), transparent 38%),
    radial-gradient(circle at bottom right, rgba(37, 99, 235, 0.24), transparent 34%),
    linear-gradient(135deg, var(--hero-dark-1) 0%, var(--hero-dark-2) 54%, var(--hero-dark-3) 100%);
}

.hero h1 {
  margin: 6px 0 10px;
  color: #ffffff;
  font-size: clamp(2rem, 4vw, 3.1rem);
  line-height: 1.05;
  letter-spacing: -0.06em;
}

.hero p {
  max-width: 780px;
  margin: 0;
  color: rgba(255, 255, 255, 0.76);
  line-height: 1.7;
}

.heroMeta {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 18px;
}

.heroMeta span {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 8px 12px;
  border-radius: 999px;
  color: rgba(255, 255, 255, 0.82);
  background: rgba(255, 255, 255, 0.1);
  font-size: 0.84rem;
}

.formCard {
  min-height: 520px;
}

.modernForm {
  display: grid;
  gap: 18px;
}

.infoCard {
  padding: 16px;
  border-radius: 18px;
  background: var(--surface-muted);
  border: 1px solid var(--border);
  color: var(--text-soft);
}

.statusText {
  color: var(--muted);
  font-size: 0.9rem;
  font-weight: 800;
}

.miniIcon {
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  border-radius: 16px;
  color: var(--primary);
  background: var(--primary-soft);
}

@media (max-width: 760px) {
  .hero {
    display: grid;
    grid-template-columns: 1fr;
    padding: 20px;
    border-radius: 24px;
  }

  .hero h1 {
    font-size: 2rem;
  }
}
"""
)

append_once(
    "src/app/links/Links.module.css",
    "/* Remaining links classes */",
    """
/* Remaining links classes */
.statGrid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}

.statItem {
  padding: 18px;
  border-radius: 22px;
  background: var(--surface-solid);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
}

.statItem span {
  color: var(--muted);
  font-size: 0.78rem;
  font-weight: 900;
  text-transform: uppercase;
}

.statItem strong {
  color: var(--text);
  font-size: 1.6rem;
}

.settingsForm {
  display: grid;
  gap: 18px;
}

.linksTable {
  min-width: 980px;
}

.linkMiniStats {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  color: var(--muted);
  font-size: 0.8rem;
}

@media (max-width: 760px) {
  .statGrid {
    grid-template-columns: 1fr;
  }
}
"""
)

append_once(
    "src/app/smtp/Smtp.module.css",
    "/* Remaining SMTP classes */",
    """
/* Remaining SMTP classes */
.statGrid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}

.statItem {
  padding: 18px;
  border-radius: 22px;
  background: var(--surface-solid);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
}

.statItem span {
  color: var(--muted);
  font-size: 0.78rem;
  font-weight: 900;
  text-transform: uppercase;
}

.statItem strong {
  color: var(--text);
  font-size: 1.6rem;
}

.settingsForm {
  display: grid;
  gap: 18px;
}

.smtpTable {
  min-width: 1060px;
}

.usage {
  display: grid;
  gap: 8px;
  min-width: 140px;
}

.actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

@media (max-width: 760px) {
  .statGrid {
    grid-template-columns: 1fr;
  }
}
"""
)

append_once(
    "src/app/webhooks/Webhooks.module.css",
    "/* Remaining webhooks classes */",
    """
/* Remaining webhooks classes */
.statGrid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}

.statItem {
  padding: 18px;
  border-radius: 22px;
  background: var(--surface-solid);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
}

.statItem span {
  color: var(--muted);
  font-size: 0.78rem;
  font-weight: 900;
  text-transform: uppercase;
}

.statItem strong {
  color: var(--text);
  font-size: 1.6rem;
}

.settingsForm {
  display: grid;
  gap: 18px;
}

.webhookTable {
  min-width: 1060px;
}

.miniStack {
  display: grid;
  gap: 4px;
}

@media (max-width: 760px) {
  .statGrid {
    grid-template-columns: 1fr;
  }
}
"""
)

append_once(
    "src/app/settings/organization/OrganizationSettings.module.css",
    "/* Remaining organization classes */",
    """
/* Remaining organization classes */
.noticeCard {
  border-color: color-mix(in srgb, var(--primary) 28%, var(--border));
  background:
    radial-gradient(circle at top right, color-mix(in srgb, var(--primary) 8%, transparent), transparent 28%),
    var(--surface);
}
"""
)

append_once(
    "src/app/account/Account.module.css",
    "/* Remaining account classes */",
    """
/* Remaining account classes */
.securityBadge {
  width: 290px;
  flex: 0 0 auto;
  display: grid;
  place-items: center;
  text-align: center;
  gap: 10px;
  padding: 22px;
  border-radius: 26px;
  background: rgba(255, 255, 255, 0.09);
  border: 1px solid rgba(255, 255, 255, 0.13);
  backdrop-filter: blur(14px);
}

.securityBadge strong {
  color: #ffffff;
}

.securityBadge span {
  color: rgba(255, 255, 255, 0.72);
  font-size: 0.88rem;
}

@media (max-width: 760px) {
  .securityBadge {
    width: 100%;
  }
}
"""
)
