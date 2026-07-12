from __future__ import annotations
import json, pathlib, py_compile, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]

def fail(message: str):
    print(f"ERROR: {message}")
    return 1

def main() -> int:
    errors = 0
    required = [
        ".claude-plugin/plugin.json",
        "skills/unity-meshy-studio/SKILL.md",
        "LICENSE", "NOTICE.md", "SECURITY.md", "README.md"
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            errors += fail(f"Missing {rel}")

    try:
        manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        for key in ("name", "version", "description", "author", "license"):
            if key not in manifest:
                errors += fail(f"plugin.json missing {key}")
    except Exception as exc:
        errors += fail(f"Invalid plugin.json: {exc}")

    for py in ROOT.rglob("*.py"):
        if "__pycache__" in py.parts:
            continue
        try:
            py_compile.compile(str(py), doraise=True)
        except Exception as exc:
            errors += fail(f"Python compile failed for {py}: {exc}")

    key_pattern = re.compile(r"\bmsy_[A-Za-z0-9_-]{8,}\b")
    for path in ROOT.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".zip", ".dll"}:
            continue
        text = path.read_text(errors="ignore")
        if key_pattern.search(text):
            errors += fail(f"Possible Meshy key in {path.relative_to(ROOT)}")

    if errors:
        print(f"Release validation failed with {errors} error(s).")
        return 1
    print("Release validation passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
