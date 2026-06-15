from pathlib import Path

ROOT = Path("src")

for path in ROOT.rglob("*.tsx"):
    backup = path.with_suffix(path.suffix + ".before-modules")
    if not backup.exists():
        backup.write_text(path.read_text(), encoding="utf-8")
        print(f"Backed up: {path} -> {backup}")
    else:
        print(f"Backup exists: {backup}")
