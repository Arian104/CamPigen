from pathlib import Path

AUTH_PAGES = [
    Path("src/app/login/page.tsx"),
    Path("src/app/register/page.tsx"),
    Path("src/app/forgot-password/page.tsx"),
    Path("src/app/reset-password/page.tsx"),
    Path("src/app/verify-email/page.tsx"),
]

AUTH_IMPORT = 'import styles from "./Auth.module.css";'

REPLACEMENTS = {
    'className="authPage"': 'className={styles.page}',
    'className="authShell"': 'className={styles.shell}',
    'className="authShell reverse"': 'className={`${styles.shell} ${styles.reverse}`}',
    'className="authShell compact"': 'className={`${styles.shell} ${styles.compact}`}',

    'className="authBrandPanel"': 'className={styles.brandPanel}',
    'className="authBrandTop"': 'className={styles.brandTop}',
    'className="brandMark authBrandMark"': 'className={styles.brandMark}',
    'className="authBrandContent"': 'className={styles.brandContent}',
    'className="authBadge"': 'className={styles.badge}',
    'className="authFeatureList"': 'className={styles.featureList}',

    'className="authFormPanel"': 'className={styles.formPanel}',
    'className="authFormHeader"': 'className={styles.formHeader}',
    'className="authFormHeader center"': 'className={`${styles.formHeader} ${styles.formHeaderCenter}`}',
    'className="authIcon"': 'className={styles.icon}',
    'className="authStatusIcon"': 'className={styles.statusIcon}',
    'className="authStatusIcon success"': 'className={`${styles.statusIcon} ${styles.success}`}',
    'className="authStatusIcon failed"': 'className={`${styles.statusIcon} ${styles.failed}`}',

    'className="authForm"': 'className={styles.form}',
    'className="authTwoCol"': 'className={styles.twoCol}',
    'className="authInputField"': 'className={styles.inputField}',
    'className="authFormMeta"': 'className={styles.formMeta}',
    'className="authRemember"': 'className={styles.remember}',
    'className="authSubmitButton"': 'className={styles.submitButton}',
    'className="authSwitchText"': 'className={styles.switchText}',
    'className="errorText authError"': 'className={styles.error}',
    'className="authError"': 'className={styles.error}',
}


def add_import(text: str) -> str:
    if AUTH_IMPORT in text:
        return text

    lines = text.splitlines()
    last_import_index = -1

    for i, line in enumerate(lines):
        if line.startswith("import "):
            last_import_index = i

    if last_import_index >= 0:
        lines.insert(last_import_index + 1, AUTH_IMPORT)
        return "\n".join(lines) + "\n"

    return AUTH_IMPORT + "\n" + text


for path in AUTH_PAGES:
    if not path.exists():
        print(f"Missing: {path}")
        continue

    text = path.read_text(encoding="utf-8")
    original = text

    # Important: replace longer class names first
    for old, new in sorted(REPLACEMENTS.items(), key=lambda x: len(x[0]), reverse=True):
        text = text.replace(old, new)

    if text != original:
        text = add_import(text)
        path.write_text(text, encoding="utf-8")
        print(f"Updated auth page: {path}")
    else:
        print(f"No auth changes: {path}")
