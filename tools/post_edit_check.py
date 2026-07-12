from __future__ import annotations
import json, sys
def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    tool_input = payload.get("tool_input") or {}
    path = str(tool_input.get("file_path") or tool_input.get("path") or "")
    if path.endswith((".cs", ".shader", ".shadergraph", ".uxml", ".uss", ".prefab", ".unity")):
        print("Unity file changed: validate compilation, serialization, references, and relevant tests.")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
