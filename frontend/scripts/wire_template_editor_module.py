from pathlib import Path
import re

path = Path("src/components/campaigns/TemplateEditor.tsx")

if not path.exists():
    raise SystemExit("TemplateEditor.tsx not found")

text = path.read_text(encoding="utf-8")
original = text

def add_import_after_imports(text: str, import_line: str) -> str:
    if import_line in text:
        return text

    lines = text.splitlines()
    i = 0
    last_import_end = -1

    while i < len(lines):
        stripped = lines[i].strip()

        if stripped == "" or stripped.startswith('"use client"') or stripped.startswith("'use client'"):
            i += 1
            continue

        if stripped.startswith("import "):
            while i < len(lines):
                if ";" in lines[i]:
                    last_import_end = i
                    i += 1
                    break
                i += 1
            continue

        break

    insert_at = last_import_end + 1 if last_import_end >= 0 else 0
    lines.insert(insert_at, import_line)

    return "\n".join(lines) + "\n"

text = add_import_after_imports(text, 'import shared from "@/styles/shared.module.css";')
text = add_import_after_imports(text, 'import componentStyles from "./CampaignComponents.module.css";')

text = text.replace(
    '<section className="card">',
    '<section className={`${shared.card} ${componentStyles.editorRoot}`}>',
)

text = text.replace(
    '<div className="flexBetween">',
    '<div className={shared.flexBetween}>',
)

text = text.replace(
    '<p className="muted">',
    '<p className={shared.muted}>',
)

text = text.replace(
    '{message ? <p className="muted">{message}</p> : null}',
    '{message ? <p className={shared.muted}>{message}</p> : null}',
)

text = text.replace(
    'className="primaryButton"',
    'className={shared.primaryButton}',
)

if text != original:
    path.write_text(text, encoding="utf-8")
    print("Updated TemplateEditor.tsx")
else:
    print("No change needed")
