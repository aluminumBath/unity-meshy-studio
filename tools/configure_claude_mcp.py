from __future__ import annotations
import json
import os
from pathlib import Path
from credential_store import get_key

def main() -> int:
    key = get_key()
    if not key:
        print("Authenticate first: python tools/meshy_auth.py login")
        return 1

    # Project-local config deliberately references an environment variable
    # instead of persisting the secret in the repository.
    config_path = Path(".mcp.json")
    config = {}
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
        except Exception:
            backup = config_path.with_suffix(".json.backup")
            backup.write_text(config_path.read_text(encoding="utf-8"), encoding="utf-8")
            config = {}

    servers = config.setdefault("mcpServers", {})
    servers["meshy"] = {
        "command": "npx",
        "args": ["-y", "@meshy-ai/meshy-mcp-server"],
        "env": {"MESHY_API_KEY": "${MESHY_API_KEY}"}
    }
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

    print("Created/updated .mcp.json without storing the API key.")
    print("Export MESHY_API_KEY before starting Claude Code.")
    print("PowerShell: $env:MESHY_API_KEY = '<your key>'")
    print("macOS/Linux: export MESHY_API_KEY='<your key>'")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
