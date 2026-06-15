from pathlib import Path
import re

files = [
    "src/app/page.tsx",
    "src/app/login/page.tsx",
    "src/app/register/page.tsx",
    "src/app/forgot-password/page.tsx",
    "src/app/reset-password/page.tsx",
    "src/app/verify-email/page.tsx",
    "src/app/account/page.tsx",
    "src/app/campaigns/page.tsx",
    "src/app/contacts/page.tsx",
    "src/app/email-history/page.tsx",
    "src/app/instant-send/page.tsx",
    "src/app/links/page.tsx",
    "src/app/settings/organization/page.tsx",
    "src/app/smtp/page.tsx",
    "src/app/webhooks/page.tsx",
]

local_style_map = {
    "src/app/login/page.tsx": "./Auth.module.css",
    "src/app/register/page.tsx": "./Auth.module.css",
    "src/app/forgot-password/page.tsx": "./Auth.module.css",
    "src/app/reset-password/page.tsx": "./Auth.module.css",
    "src/app/verify-email/page.tsx": "./Auth.module.css",
    "src/app/account/page.tsx": "./Account.module.css",
    "src/app/campaigns/page.tsx": "./Campaigns.module.css",
    "src/app/contacts/page.tsx": "./Contacts.module.css",
    "src/app/email-history/page.tsx": "./EmailHistory.module.css",
    "src/app/instant-send/page.tsx": "./InstantSend.module.css",
    "src/app/links/page.tsx": "./Links.module.css",
    "src/app/settings/organization/page.tsx": "./OrganizationSettings.module.css",
    "src/app/smtp/page.tsx": "./Smtp.module.css",
    "src/app/webhooks/page.tsx": "./Webhooks.module.css",
}

css_import_pattern = re.compile(
    r'^\s*import\s+(shared|styles)\s+from\s+["\'][^"\']+\.module\.css["\'];\s*$'
)

def is_use_client(line: str) -> bool:
    value = line.strip()
    return value == '"use client";' or value == "'use client';"

def insert_imports_after_normal_imports(lines, imports):
    index = 0
    last_import_end = -1

    while index < len(lines):
        stripped = lines[index].strip()

        if is_use_client(lines[index]) or stripped == "":
            index += 1
            continue

        if stripped.startswith("import "):
            while index < len(lines):
                if ";" in lines[index]:
                    last_import_end = index
                    index += 1
                    break
                index += 1
            continue

        break

    insert_at = last_import_end + 1 if last_import_end >= 0 else 0
    return lines[:insert_at] + imports + lines[insert_at:]

for file_name in files:
    path = Path(file_name)

    if not path.exists():
        continue

    original_text = path.read_text(encoding="utf-8")
    original_lines = original_text.splitlines()

    # Remove any old/wrong CSS module imports from anywhere in file
    cleaned_lines = []
    for line in original_lines:
        if css_import_pattern.match(line):
            continue
        cleaned_lines.append(line)

    body = "\n".join(cleaned_lines)

    imports_to_add = []

    if "shared." in body:
        imports_to_add.append('import shared from "@/styles/shared.module.css";')

    if "styles." in body and file_name in local_style_map:
        imports_to_add.append(f'import styles from "{local_style_map[file_name]}";')

    # Deduplicate
    unique_imports = []
    for item in imports_to_add:
        if item not in unique_imports:
            unique_imports.append(item)

    if unique_imports:
        cleaned_lines = insert_imports_after_normal_imports(cleaned_lines, unique_imports)

    path.write_text("\n".join(cleaned_lines) + "\n", encoding="utf-8")
    print(f"fixed: {file_name}")
