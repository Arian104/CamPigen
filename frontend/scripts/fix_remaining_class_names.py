from pathlib import Path

replacements = {
    "src/app/settings/organization/page.tsx": {
        'className="card noticeCard"': 'className={`${shared.card} ${styles.noticeCard}`}',
    },

    "src/app/links/page.tsx": {
        'className="card statGrid"': 'className={`${shared.card} ${styles.statGrid}`}',
        'className="settingsForm"': 'className={styles.settingsForm}',
        'className="dataTable linksTable"': 'className={`${shared.dataTable} ${styles.linksTable}`}',
        'className="linkMiniStats"': 'className={styles.linkMiniStats}',
        'className="statItem"': 'className={styles.statItem}',
    },

    "src/app/smtp/page.tsx": {
        'className="card statGrid"': 'className={`${shared.card} ${styles.statGrid}`}',
        'className="settingsForm"': 'className={styles.settingsForm}',
        'className="dataTable smtpTable"': 'className={`${shared.dataTable} ${styles.smtpTable}`}',
        'className="smtpUsage"': 'className={styles.usage}',
        'className="smtpActions"': 'className={styles.actions}',
        'className="statItem"': 'className={styles.statItem}',
    },

    "src/app/instant-send/page.tsx": {
        'className="instantHero"': 'className={styles.hero}',
        'className="instantHeroMeta"': 'className={styles.heroMeta}',
        'className="card instantFormCard"': 'className={`${shared.card} ${styles.formCard}`}',
        'className="instantModernForm"': 'className={styles.modernForm}',
        'className="instantInfoCard"': 'className={styles.infoCard}',
        'className="instantStatusText"': 'className={styles.statusText}',
        'className="instantMiniIcon"': 'className={styles.miniIcon}',
    },

    "src/app/campaigns/page.tsx": {
        'className="actionGroup"': 'className={shared.actions}',
    },

    "src/app/account/security/page.tsx": {
        'className="accountSecurityBadge"': 'className={styles.securityBadge}',
    },

    "src/app/webhooks/page.tsx": {
        'className="card statGrid"': 'className={`${shared.card} ${styles.statGrid}`}',
        'className="settingsForm"': 'className={styles.settingsForm}',
        'className="dataTable webhookTable"': 'className={`${shared.dataTable} ${styles.webhookTable}`}',
        'className="miniStack"': 'className={styles.miniStack}',
        'className="statItem"': 'className={styles.statItem}',
    },

    "src/app/page.tsx": {
        'className="dashboardHero"': 'className={shared.pageHero}',
        'className="dashboardHeroMeta"': 'className={shared.heroMeta}',
        'className="dashboardHeroActions"': 'className={shared.heroActions}',
        'className="card dashboardActivityCard"': 'className={`${shared.card} ${styles.activityCard}`}',
        'className="card dashboardRatesCard"': 'className={`${shared.card} ${styles.ratesCard}`}',
        'className="dashboardListIcon"': 'className={styles.listIcon}',
    },
}

for file_name, file_replacements in replacements.items():
    path = Path(file_name)

    if not path.exists():
        print("missing:", file_name)
        continue

    text = path.read_text()
    original = text

    for old, new in file_replacements.items():
        text = text.replace(old, new)

    if text != original:
        path.write_text(text)
        print("fixed:", file_name)
    else:
        print("no changes:", file_name)
