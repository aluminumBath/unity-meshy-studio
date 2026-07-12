# Runtime dependencies

## Python

- Python 3.10 or newer
- `requests` 2.32.x — HTTPS REST requests
- `keyring` 25.x — optional operating-system credential storage

Install with:

```bash
python -m pip install -r tools/requirements.txt
```

Review dependency licenses and security advisories before redistributing a
modified package.

## Node.js / MCP

The optional Meshy MCP integration invokes:

```text
@meshy-ai/meshy-mcp-server
```

through `npx`. Node.js and npm are therefore required for MCP use. The REST
fallback client does not require Node.js.

## Unity

The included Editor scripts target contemporary Unity versions and should be
tested against the project's exact Unity editor version and render pipeline.
They are editor utilities, not a replacement for Meshy's official Unity plugin.
