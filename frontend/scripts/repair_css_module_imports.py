from pathlib import Path
import re

ROOTS = [Path("src/app"), Path("src/components")]

CSS_IMPORT_RE = re.compile(
    r'^\s*import\s+(shared|styles)\s+from\s+["\']([^"\']+\.module\.css)["\'];\s*$'
)

PAGE_STYLE_MAP = {
    "src/app/login/page.tsx": './Auth.module.css',
    "src/app/register/page.tsx": './Auth.module.css',
    "src/app/forgot-password/page.tsx": './Auth.module.css',
    "src/app/reset-password/page.tsx": './Auth.module.css',
    "src/app/verify-email/page.tsx": './Auth.module.css',
    "src/app/account/page.tsx": './Account.module.css',
    "src/app/campaigns/page.tsx": './Campaigns.module.css',
    "src/app/smtp/page.tsx": './Smtp.module.css',
    "src/app/instant-send/page.tsx": './InstantSend.module.css',
    "src/app/contacts/page.tsx": './Contacts.module.css',
    "src/app/links/page.tsx": './Links.module.css',
    "src/app/webhooks/page.tsx": './Webhooks.module.css',
    "src/app/email-history/page.tsx": './EmailHistory.module.css',
    "src/app/settings/organization/page.tsx": './OrganizationSettings.module.css',
}

def find_import_insert_index(lines):
    """
    Insert after all import statements, including multiline imports.
    Preserves "use client" at the top.
    """
    i = 0
    last_import_end = -1

    while i < len(lines):
        stripped = lines[i].strip()

        if stripped in ['"use client";', "'use client';'] or stripped == "":
            i += 1
            continue

        if stripped.startswith("import "):
            # Multiline import until semicolon
            while i < len(lines):
                if ";" in lines[i]:
                    last_import_end = i
                    i += 1
                    break
                i += 1
            continue

        break

    return last_import_end + 1 if last_import_end >= 0 else 0

for root in ROOTS:
    for path in root.rglob("*.tsx"):
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()

        # Remove all CSS module imports wherever they were inserted
        cleaned = []
        removed = []
        for line in lines:
            match = CSS_IMPORT_RE.match(line)
            if match:
                removed.append((match.group(1), match.group(2)))
                continue
            cleaned.append(line)

        text_without_css_imports = "\n".join(cleaned) + "\n"

        imports_to_add = []

        # Add shared only if shared. is used
        if "shared." in text_without_css_imports:
            imports_to_add.append('import shared from "@/styles/shared.module.css";')

        # Add page-local styles only if styles. is used
        page_key = str(path)
        if "styles." in text_without_css_imports and page_key in PAGE_STYLE_MAP:
            imports_to_add.append(f'import styles from "{PAGE_STYLE_MAP[page_key]}";')

        # Component-local styles
        if "styles." in text_without_css_imports and path.name == "Topbar.tsx":
            imports_to_add.append('import styles from "./Topbar.module.css";')

        if "styles." in text_without_css_imports and path.name == "Sidebar.tsx":
            imports_to_add.append('import styles from "./Sidebar.module.css";')

        if "styles." in text_without_css_imports and path.name == "platform-shell.tsx":
            imports_to_add.append('import styles from "@/components/PlatformShell.module.css";')

        # Avoid duplicates
        unique_imports = []
        for item in imports_to_add:
            if item not in unique_imports:
                unique_imports.append(item)

        final_lines = text_without_css_imports.splitlines()
        insert_at = find_import_insert_index(final_lines)

        if unique_imports:
            final_lines[insert_at:insert_at] = unique_imports

        new_text = "\n".join(final_lines) + "\n"

        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print(f"Repaired imports: {path}")
