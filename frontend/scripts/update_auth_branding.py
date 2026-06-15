from pathlib import Path
import re

AUTH_PAGES = [
    Path("src/app/login/page.tsx"),
    Path("src/app/register/page.tsx"),
    Path("src/app/forgot-password/page.tsx"),
    Path("src/app/reset-password/page.tsx"),
    Path("src/app/verify-email/page.tsx"),
]

LOGO_BLOCK = """<div className={styles.brandLogo}>
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
            </div>"""

def is_use_client_line(line):
    stripped = line.strip()
    return stripped.startswith('"use client"') or stripped.startswith("'use client'")

def add_image_import(text):
    if 'from "next/image"' in text:
        return text

    lines = text.splitlines()
    insert_at = 0

    for index, line in enumerate(lines):
        if is_use_client_line(line):
            insert_at = index + 1
            break

    lines.insert(insert_at, 'import Image from "next/image";')
    return "\n".join(lines) + "\n"

for path in AUTH_PAGES:
    if not path.exists():
        print("Missing:", path)
        continue

    text = path.read_text(encoding="utf-8")
    original = text

    text = add_image_import(text)

    text = re.sub(
        r'<div className=\{styles\.brandMark\}>.*?</div>',
        LOGO_BLOCK,
        text,
        flags=re.DOTALL,
    )

    replacements = {
        "<strong>Email Platform</strong>": "<strong>CamPigen</strong>",
        "<span>Enterprise Suite</span>": "<span>Let your campaigns take flight.</span>",
        "<span>Start your workspace</span>": "<span>Let your campaigns take flight.</span>",
        "<span>Account recovery</span>": "<span>Let your campaigns take flight.</span>",
        "<span>Password reset</span>": "<span>Let your campaigns take flight.</span>",
        "<span>Email verification</span>": "<span>Let your campaigns take flight.</span>",
        "Email Platform": "CamPigen",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    if text != original:
        path.write_text(text, encoding="utf-8")
        print("Updated branding:", path)
    else:
        print("No changes needed:", path)
