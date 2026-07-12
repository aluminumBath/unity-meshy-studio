from __future__ import annotations
import os
from typing import Optional

SERVICE = "unity-meshy-studio"
USERNAME = "MESHY_API_KEY"

def get_key() -> Optional[str]:
    env = os.getenv("MESHY_API_KEY", "").strip()
    if env:
        return env
    try:
        import keyring
        value = keyring.get_password(SERVICE, USERNAME)
        return value.strip() if value else None
    except Exception:
        return None

def set_key(value: str) -> None:
    if not value or any(ch.isspace() for ch in value):
        raise ValueError("The Meshy API key is empty or contains whitespace.")
    try:
        import keyring
        keyring.set_password(SERVICE, USERNAME, value)
    except Exception as exc:
        raise RuntimeError(
            "Could not store the key in the OS credential store. "
            "Set MESHY_API_KEY through your shell or secret manager instead."
        ) from exc

def delete_key() -> None:
    try:
        import keyring
        keyring.delete_password(SERVICE, USERNAME)
    except Exception:
        pass
