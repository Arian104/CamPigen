from pathlib import Path

APP_DIR = Path("src/app")

SHARED_IMPORT = 'import shared from "@/styles/shared.module.css";'

REPLACEMENTS = {
    'className="page"': 'className={shared.page}',
    'className="card"': 'className={shared.card}',
    'className="grid"': 'className={shared.grid}',
    'className="muted"': 'className={shared.muted}',
    'className="small"': 'className={shared.small}',
    'className="flexBetween"': 'className={shared.flexBetween}',
    'className="actions"': 'className={shared.actions}',
    'className="centerText"': 'className={shared.centerText}',

    'className="tableWrap"': 'className={shared.tableWrap}',
    'className="dataTable"': 'className={shared.dataTable}',

    'className="buttonLink"': 'className={shared.buttonLink}',
    'className="primaryButton"': 'className={shared.primaryButton}',
    'className="secondaryButton"': 'className={shared.secondaryButton}',
    'className="ghostButton"': 'className={shared.ghostButton}',
    'className="smallButton"': 'className={shared.smallButton}',
    'className="dangerButton"': 'className={shared.dangerButton}',
    'className="dangerSmall"': 'className={shared.dangerSmall}',

    'className="formField"': 'className={shared.formField}',
    'className="checkboxRow"': 'className={shared.checkboxRow}',
    'className="settingsFull"': 'className={shared.full}',

    'className="settingsGridTwo"': 'className={shared.gridTwo}',
    'className="settingsGridThree"': 'className={shared.gridThree}',
    'className="settingsGridFour"': 'className={shared.gridFour}',

    'className="statusPill"': 'className={shared.statusPill}',
    'className="rolePill"': 'className={shared.rolePill}',
    'className="planPill"': 'className={shared.planPill}',
    'className="featurePill"': 'className={shared.featurePill}',

    'className="chipGroup"': 'className={shared.chipGroup}',
    'className="chip"': 'className={shared.chip}',

    'className="pageHero"': 'className={shared.pageHero}',
    'className="heroActions"': 'className={shared.heroActions}',
    'className="heroMeta"': 'className={shared.heroMeta}',
    'className="eyebrow"': 'className={shared.eyebrow}',

    'className="muted centerText"': 'className={`${shared.muted} ${shared.centerText}`}',
    'className="smallButton dangerSmall"': 'className={`${shared.smallButton} ${shared.dangerSmall}`}',
    'className="statusPill active"': 'className={`${shared.statusPill} ${shared.statusActive}`}',
    'className="statusPill suspended"': 'className={`${shared.statusPill} ${shared.statusDanger}`}',
    'className="featurePill enabled"': 'className={`${shared.featurePill} ${shared.featureEnabled}`}',
    'className="featurePill disabled"': 'className={`${shared.featurePill} ${shared.featureDisabled}`}',
}


def add_import(text: str) -> str:
    if SHARED_IMPORT in text:
        return text

    lines = text.splitlines()
    last_import_index = -1

    for i, line in enumerate(lines):
        if line.startswith("import "):
            last_import_index = i

    if last_import_index >= 0:
        lines.insert(last_import_index + 1, SHARED_IMPORT)
        return "\n".join(lines) + "\n"

    return SHARED_IMPORT + "\n" + text


for path in APP_DIR.rglob("page.tsx"):
    text = path.read_text(encoding="utf-8")
    original = text

    used = False
    for old, new in REPLACEMENTS.items():
        if old in text:
            text = text.replace(old, new)
            used = True

    if used:
        text = add_import(text)
        path.write_text(text, encoding="utf-8")
        print(f"Updated shared classes: {path}")
    else:
        print(f"No shared class changes: {path}")
