# Security policy

## Supported release

Security fixes are provided for the latest published release.

## Credentials

- Never commit a Meshy API key.
- Never place a Meshy key in a Unity scene, prefab, ScriptableObject, build,
  browser bundle, mobile application, or other distributed client.
- Prefer `MESHY_API_KEY` supplied by a shell, CI secret, or secret manager.
- The optional Python `keyring` integration stores credentials through the
  operating system's credential service when available.
- Revoke a key immediately in Meshy settings if it is exposed.

## Reporting

Please report security issues privately to steeleschauer@gmail.com rather than
opening a public issue containing exploit details or credentials.
