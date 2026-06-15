from pathlib import Path
import re

FILES = [
    "src/components/email-builder/EmailBuilder.tsx",
    "src/components/email-builder/BlockSidebar.tsx",
    "src/components/email-builder/BuilderCanvas.tsx",
    "src/components/email-builder/PropertyPanel.tsx",
    "src/components/email-builder/PropertyControls.tsx",
    "src/components/email-builder/SortableEmailBlock.tsx",
    "src/components/email-builder/blockRegistry.tsx",
    "src/components/email-builder/blocks/hero/index.tsx",
    "src/components/email-builder/blocks/text/index.tsx",
    "src/components/email-builder/blocks/button/index.tsx",
    "src/components/email-builder/blocks/image/index.tsx",
    "src/components/email-builder/blocks/card/index.tsx",
    "src/components/email-builder/blocks/product/index.tsx",
    "src/components/email-builder/blocks/coupon/index.tsx",
    "src/components/email-builder/blocks/divider/index.tsx",
    "src/components/email-builder/blocks/footer/index.tsx",
    "src/components/email-builder/blocks/social/index.tsx",
    "src/components/email-builder/blocks/spacer/index.tsx",
]

STYLE_IMPORT = 'import styles from "./EmailBuilder.module.css";'
BLOCK_STYLE_IMPORT = 'import styles from "../../EmailBuilder.module.css";'

CLASS_REPLACEMENTS = {
    'className="emailBuilderShell"': 'className={`${styles.shell} emailBuilderShell`}',
    'className="builderSidebar"': 'className={`${styles.sidebar} builderSidebar`}',
    'className="builderCanvas"': 'className={`${styles.canvas} builderCanvas`}',
    'className="propertyPanel"': 'className={`${styles.propertyPanel} propertyPanel`}',
    'className="builderBlockList"': 'className={`${styles.blockList} builderBlockList`}',
    'className="builderBlockButton"': 'className={`${styles.blockButton} builderBlockButton`}',
    'className="emailCanvasFrame"': 'className={`${styles.canvasFrame} emailCanvasFrame`}',
    'className="emptyCanvas"': 'className={`${styles.emptyCanvas} emptyCanvas`}',
    'className="sortableEmailBlock"': 'className={`${styles.emailBlock} sortableEmailBlock`}',
    'className="blockToolbar"': 'className={`${styles.blockToolbar} blockToolbar`}',
    'className="builderSaveBar"': 'className={`${styles.saveBar} builderSaveBar`}',
    'className="settingsGroup"': 'className={`${styles.settingsGroup} settingsGroup`}',
}

def has_style_usage(text: str) -> bool:
    return "styles." in text

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

for file_name in FILES:
    path = Path(file_name)

    if not path.exists():
        print("missing:", file_name)
        continue

    text = path.read_text(encoding="utf-8")
    original = text

    for old, new in CLASS_REPLACEMENTS.items():
        text = text.replace(old, new)

    # Also handle selected sortable pattern if it exists
    text = text.replace(
        'className={selected ? "sortableEmailBlock selected" : "sortableEmailBlock"}',
        'className={selected ? `${styles.emailBlock} ${styles.selected} sortableEmailBlock selected` : `${styles.emailBlock} sortableEmailBlock`}',
    )

    text = text.replace(
        'className={isSelected ? "sortableEmailBlock selected" : "sortableEmailBlock"}',
        'className={isSelected ? `${styles.emailBlock} ${styles.selected} sortableEmailBlock selected` : `${styles.emailBlock} sortableEmailBlock`}',
    )

    text = text.replace(
        'className={active ? "sortableEmailBlock selected" : "sortableEmailBlock"}',
        'className={active ? `${styles.emailBlock} ${styles.selected} sortableEmailBlock selected` : `${styles.emailBlock} sortableEmailBlock`}',
    )

    if has_style_usage(text):
        if "/blocks/" in file_name:
            text = add_import_after_imports(text, BLOCK_STYLE_IMPORT)
        else:
            text = add_import_after_imports(text, STYLE_IMPORT)

    if text != original:
        path.write_text(text, encoding="utf-8")
        print("updated:", file_name)
    else:
        print("unchanged:", file_name)
