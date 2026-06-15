from pathlib import Path
import re

FILES = [
    "src/app/page.tsx",
    "src/app/login/page.tsx",
    "src/app/register/page.tsx",
    "src/app/forgot-password/page.tsx",
    "src/app/reset-password/page.tsx",
    "src/app/verify-email/page.tsx",
    "src/app/account/page.tsx",
    "src/app/account/activity/page.tsx",
    "src/app/account/security/page.tsx",
    "src/app/account/sessions/page.tsx",
    "src/app/campaigns/page.tsx",
    "src/app/contacts/page.tsx",
    "src/app/email-history/page.tsx",
    "src/app/instant-send/page.tsx",
    "src/app/links/page.tsx",
    "src/app/settings/organization/page.tsx",
    "src/app/smtp/page.tsx",
    "src/app/webhooks/page.tsx",
]

LOCAL_MODULES = {
    "src/app/page.tsx": "./Dashboard.module.css",
    "src/app/login/page.tsx": "./Auth.module.css",
    "src/app/register/page.tsx": "./Auth.module.css",
    "src/app/forgot-password/page.tsx": "./Auth.module.css",
    "src/app/reset-password/page.tsx": "./Auth.module.css",
    "src/app/verify-email/page.tsx": "./Auth.module.css",
    "src/app/account/page.tsx": "./Account.module.css",
    "src/app/account/activity/page.tsx": "../Account.module.css",
    "src/app/account/security/page.tsx": "../Account.module.css",
    "src/app/account/sessions/page.tsx": "../Account.module.css",
    "src/app/campaigns/page.tsx": "./Campaigns.module.css",
    "src/app/contacts/page.tsx": "./Contacts.module.css",
    "src/app/email-history/page.tsx": "./EmailHistory.module.css",
    "src/app/instant-send/page.tsx": "./InstantSend.module.css",
    "src/app/links/page.tsx": "./Links.module.css",
    "src/app/settings/organization/page.tsx": "./OrganizationSettings.module.css",
    "src/app/smtp/page.tsx": "./Smtp.module.css",
    "src/app/webhooks/page.tsx": "./Webhooks.module.css",
}

SHARED = {
    "page": "shared.page",
    "card": "shared.card",
    "grid": "shared.grid",
    "muted": "shared.muted",
    "small": "shared.small",
    "eyebrow": "shared.eyebrow",
    "flexBetween": "shared.flexBetween",
    "actions": "shared.actions",
    "centerText": "shared.centerText",
    "tableWrap": "shared.tableWrap",
    "dataTable": "shared.dataTable",
    "buttonLink": "shared.buttonLink",
    "primaryButton": "shared.primaryButton",
    "secondaryButton": "shared.secondaryButton",
    "ghostButton": "shared.ghostButton",
    "smallButton": "shared.smallButton",
    "dangerButton": "shared.dangerButton",
    "dangerSmall": "shared.dangerSmall",
    "formField": "shared.formField",
    "checkboxRow": "shared.checkboxRow",
    "settingsFull": "shared.full",
    "settingsGridTwo": "shared.gridTwo",
    "settingsGridThree": "shared.gridThree",
    "settingsGridFour": "shared.gridFour",
    "statusPill": "shared.statusPill",
    "rolePill": "shared.rolePill",
    "planPill": "shared.planPill",
    "featurePill": "shared.featurePill",
    "chipGroup": "shared.chipGroup",
    "chip": "shared.chip",
    "pageHero": "shared.pageHero",
    "heroActions": "shared.heroActions",
    "heroMeta": "shared.heroMeta",
}

LOCAL = {
    "dashboardPage": "styles.dashboardPage",
    "dashboardKpiGrid": "styles.kpiGrid",
    "dashboardKpiCard": "styles.kpiCard",
    "dashboardKpiIcon": "styles.kpiIcon",
    "dashboardChartGrid": "styles.chartGrid",
    "dashboardTwoCol": "styles.twoCol",
    "dashboardChartCard": "styles.chartCard",
    "dashboardListRow": "styles.listRow",
    "dashboardRateRow": "styles.rateRow",
    "quickGrid": "styles.quickGrid",
    "tileLink": "styles.tileLink",

    "authPage": "styles.page",
    "authShell": "styles.shell",
    "reverse": "styles.reverse",
    "compact": "styles.compact",
    "authBrandPanel": "styles.brandPanel",
    "authBrandTop": "styles.brandTop",
    "authBrandMark": "styles.brandMark",
    "authBrandContent": "styles.brandContent",
    "authBadge": "styles.badge",
    "authFeatureList": "styles.featureList",
    "authFormPanel": "styles.formPanel",
    "authFormHeader": "styles.formHeader",
    "center": "styles.formHeaderCenter",
    "authIcon": "styles.icon",
    "authStatusIcon": "styles.statusIcon",
    "success": "styles.success",
    "failed": "styles.failed",
    "authForm": "styles.form",
    "authTwoCol": "styles.twoCol",
    "authInputField": "styles.inputField",
    "authFormMeta": "styles.formMeta",
    "authRemember": "styles.remember",
    "authSubmitButton": "styles.submitButton",
    "authSwitchText": "styles.switchText",
    "errorText": "styles.error",
    "authError": "styles.error",

    "accountPage": "styles.page",
    "accountHero": "styles.hero",
    "accountHeroModern": "styles.hero",
    "accountHeroMeta": "styles.heroMeta",
    "accountAvatarCard": "styles.avatarCard",
    "accountAvatarPreview": "styles.avatarPreview",
    "accountAvatarActions": "styles.avatarActions",
    "avatarUploadButton": "styles.avatarUpload",
    "accountOverviewGrid": "styles.overviewGrid",
    "accountMiniCard": "styles.miniCard",
    "accountProgressBar": "styles.progressBar",
    "accountTabsCard": "styles.tabsCard",
    "accountTabs": "styles.tabs",
    "accountTab": "styles.tab",
    "accountGrid": "styles.accountGrid",
    "accountInfoBox": "styles.infoBox",
    "accountTimeline": "styles.timeline",
    "accountTimelineItem": "styles.timelineItem",
    "accountTimelineIcon": "styles.timelineIcon",
    "accountTimelineMeta": "styles.timelineMeta",
    "accountQuickLinks": "styles.quickLinks",

    "settingsLayout": "styles.layout",
    "orgShell": "styles.layout",
    "settingsSidebar": "styles.tabs",
    "orgTabs": "styles.tabs",
    "settingsTab": "styles.tab",
    "orgTab": "styles.tab",
    "settingsContent": "styles.content",
    "orgPanel": "styles.panel",
    "settingsSection": "styles.section",
    "settingsPanel": "styles.panel",
    "brandPreview": "styles.brandPreview",
    "brandPreviewCard": "styles.brandPreview",
    "brandPreviewLogo": "styles.brandLogo",
    "socialGrid": "styles.socialGrid",
    "presetGrid": "styles.presetGrid",
    "planGrid": "styles.planGrid",
    "featureGrid": "styles.featureGrid",
    "limitGrid": "styles.limitGrid",
    "presetCard": "styles.presetCard",
    "featureCard": "styles.featureCard",
    "limitCard": "styles.limitCard",
    "planCard": "styles.planCard",
    "memberAddBox": "styles.memberAddBox",
    "memberFormGrid": "styles.memberFormGrid",

    "splitPane": "styles.splitPane",
    "templateGrid": "styles.templateGrid",
    "campaignFormGrid": "styles.formGrid",
    "campaignListSelector": "styles.listSelector",
    "campaignSubmitBar": "styles.submitBar",
    "previewPane": "styles.previewPane",
    "previewBody": "styles.previewBody",
    "templateList": "styles.templateList",
    "modernTemplateCard": "styles.templateCard",
    "templateCard": "styles.templateCard",
    "templateCardIcon": "styles.templateIcon",
    "templateCardMain": "styles.templateMain",
    "templateCardTop": "styles.templateTop",
    "templateCardMeta": "styles.templateMeta",
    "templatePreviewPanel": "styles.previewPanel",
    "variableGrid": "styles.variableGrid",

    "smtpPage": "styles.page",
    "smtpLayout": "styles.layout",
    "smtpSideCard": "styles.sideCard",
    "smtpGuide": "styles.guide",
    "smtpCardGrid": "styles.cardGrid",
    "smtpPoolCard": "styles.poolCard",
    "smtpPoolHeader": "styles.poolHeader",
    "smtpPoolFooter": "styles.poolFooter",
    "smtpMetaGrid": "styles.metaGrid",
    "smtpMetaItem": "styles.metaItem",
    "smtpLimitBars": "styles.limitBars",
    "smtpLimitTrack": "styles.limitTrack",
    "smtpFormGrid": "styles.formGrid",
    "smtpToggleRow": "styles.toggleRow",

    "instantPage": "styles.page",
    "instantGrid": "styles.grid",
    "instantSideCard": "styles.sideCard",
    "instantGuide": "styles.guide",
    "instantMiniCard": "styles.miniCard",
    "instantFormGrid": "styles.formGrid",
    "instantBottomGrid": "styles.bottomGrid",
    "instantActionBar": "styles.actionBar",
    "instantHeroCard": "styles.heroCard",

    "cdpTabs": "styles.tabs",
    "cdpSearch": "styles.search",
    "cdpGridTwo": "styles.gridTwo",
    "cdpContactGrid": "styles.contactGrid",
    "cdpTagGrid": "styles.tagGrid",
    "cdpContactCard": "styles.contactCard",
    "cdpTagCard": "styles.tagCard",
    "cdpContactTop": "styles.contactTop",
    "cdpAvatar": "styles.avatar",
    "cdpMiniInfo": "styles.miniInfo",
    "cdpTagDot": "styles.tagDot",
    "cdpBulkBar": "styles.bulkBar",
    "cdpDrawerOverlay": "styles.drawerOverlay",
    "cdpDrawer": "styles.drawer",
    "cdpDrawerHeader": "styles.drawerHeader",

    "linkActions": "styles.actions",
    "urlCell": "styles.urlCell",
    "linkKpiGrid": "styles.kpiGrid",
    "linkKpiCard": "styles.kpiCard",

    "webhookEvents": "styles.events",
    "webhookEventGrid": "styles.eventGrid",
    "eventChip": "styles.eventChip",
    "webhookActions": "styles.actions",
    "deliveryGrid": "styles.deliveryGrid",
    "deliveryCard": "styles.deliveryCard",

    "jobMeta": "styles.jobMeta",
    "errorBox": "styles.errorBox",
    "filters": "styles.filters",
}

CLASS_RE = re.compile(r'className="([^"]+)"')

def is_use_client_line(line):
    stripped = line.strip()
    if stripped == "":
        return True
    if stripped.startswith('"use client"'):
        return True
    if stripped.startswith("'use client'"):
        return True
    return False

def convert_class_string(value):
    tokens = value.split()
    refs = []

    for token in tokens:
        if token in LOCAL:
            refs.append(LOCAL[token])
        elif token in SHARED:
            refs.append(SHARED[token])
        else:
            return None

    if len(refs) == 1:
        return "{" + refs[0] + "}"

    joined = " ".join("${" + ref + "}" for ref in refs)
    return "{`" + joined + "`}"

def add_imports(file_name, text, needs_shared, needs_styles):
    lines = text.splitlines()

    cleaned = []
    for line in lines:
        if re.match(r'^\s*import\s+shared\s+from\s+["\']@/styles/shared\.module\.css["\'];\s*$', line):
            continue
        if re.match(r'^\s*import\s+styles\s+from\s+["\'][^"\']+\.module\.css["\'];\s*$', line):
            continue
        cleaned.append(line)

    imports = []

    if needs_shared:
        imports.append('import shared from "@/styles/shared.module.css";')

    if needs_styles and file_name in LOCAL_MODULES:
        imports.append('import styles from "' + LOCAL_MODULES[file_name] + '";')

    if not imports:
        return "\n".join(cleaned) + "\n"

    index = 0
    last_import_end = -1

    while index < len(cleaned):
        stripped = cleaned[index].strip()

        if is_use_client_line(cleaned[index]):
            index += 1
            continue

        if stripped.startswith("import "):
            while index < len(cleaned):
                if ";" in cleaned[index]:
                    last_import_end = index
                    index += 1
                    break
                index += 1
            continue

        break

    insert_at = last_import_end + 1 if last_import_end >= 0 else 0
    cleaned[insert_at:insert_at] = imports

    return "\n".join(cleaned) + "\n"

for file_name in FILES:
    path = Path(file_name)

    if not path.exists():
        continue

    text = path.read_text(encoding="utf-8")
    original = text

    needs_shared = "shared." in text
    needs_styles = "styles." in text

    def replace_match(match):
        value = match.group(1)
        converted = convert_class_string(value)

        if converted is None:
            return match.group(0)

        replace_match.needs_shared = replace_match.needs_shared or "shared." in converted
        replace_match.needs_styles = replace_match.needs_styles or "styles." in converted

        return "className=" + converted

    replace_match.needs_shared = needs_shared
    replace_match.needs_styles = needs_styles

    text = CLASS_RE.sub(replace_match, text)

    text = add_imports(
        file_name,
        text,
        replace_match.needs_shared,
        replace_match.needs_styles,
    )

    if text != original:
        path.write_text(text, encoding="utf-8")
        print("migrated:", file_name)
    else:
        print("unchanged:", file_name)
