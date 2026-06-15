from pathlib import Path

REPLACEMENTS = {
    '"accountTab active"': '`${styles.tab} ${styles.tabActive}`',
    '"accountTab"': 'styles.tab',

    '"settingsTab active"': '`${styles.tab} ${styles.tabActive}`',
    '"settingsTab"': 'styles.tab',
    '"orgTab active"': '`${styles.tab} ${styles.tabActive}`',
    '"orgTab"': 'styles.tab',

    '"statusPill active"': '`${shared.statusPill} ${shared.statusActive}`',
    '"statusPill suspended"': '`${shared.statusPill} ${shared.statusDanger}`',
    '"statusPill"': 'shared.statusPill',

    '"featurePill enabled"': '`${shared.featurePill} ${shared.featureEnabled}`',
    '"featurePill disabled"': '`${shared.featurePill} ${shared.featureDisabled}`',
    '"featurePill"': 'shared.featurePill',

    '"authStatusIcon success"': '`${styles.statusIcon} ${styles.success}`',
    '"authStatusIcon failed"': '`${styles.statusIcon} ${styles.failed}`',
    '"authStatusIcon"': 'styles.statusIcon',
}

TARGETS = [
    Path("src/app/account/page.tsx"),
    Path("src/app/settings/organization/page.tsx"),
    Path("src/app/verify-email/page.tsx"),
    Path("src/app/campaigns/page.tsx"),
    Path("src/app/smtp/page.tsx"),
    Path("src/app/contacts/page.tsx"),
]

for path in TARGETS:
    if not path.exists():
        continue

    text = path.read_text(encoding="utf-8")
    original = text

    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)

    if text != original:
        path.write_text(text, encoding="utf-8")
        print("fixed:", path)
