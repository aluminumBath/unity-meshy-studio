from __future__ import annotations
import argparse
import getpass
import sys
import webbrowser
import requests
from credential_store import get_key, set_key, delete_key

BASE = "https://api.meshy.ai"
LOGIN_URL = "https://www.meshy.ai/"
API_SETTINGS_URL = "https://www.meshy.ai/settings/api"

def masked(value: str) -> str:
    if len(value) < 12:
        return "****"
    return f"{value[:7]}…{value[-4:]}"

def verify(key: str) -> dict:
    response = requests.get(
        f"{BASE}/openapi/v1/balance",
        headers={"Authorization": f"Bearer {key}"},
        timeout=30,
    )
    if response.status_code in (401, 403):
        raise RuntimeError("Meshy rejected the API key.")
    response.raise_for_status()
    return response.json()

def login() -> int:
    print("Opening Meshy. Sign in or create an account in your browser.")
    webbrowser.open(LOGIN_URL)
    print("Opening Meshy API settings. Create or copy an API key.")
    webbrowser.open(API_SETTINGS_URL)

    key = getpass.getpass("Paste your Meshy API key (input is hidden): ").strip()
    if not key:
        print("No key entered.", file=sys.stderr)
        return 2
    if any(ch.isspace() for ch in key):
        print("The API key contains whitespace.", file=sys.stderr)
        return 2

    try:
        data = verify(key)
        set_key(key)
    except Exception as exc:
        print(f"Login failed: {exc}", file=sys.stderr)
        return 1

    balance = data.get("balance", data)
    print(f"Authenticated as key {masked(key)}. Current API balance: {balance}")
    print("The key was stored in your operating system credential store.")
    return 0

def status() -> int:
    key = get_key()
    if not key:
        print("Not authenticated. Run: python tools/meshy_auth.py login")
        return 1
    try:
        data = verify(key)
    except Exception as exc:
        print(f"Stored credential is not valid: {exc}", file=sys.stderr)
        return 1
    print(f"Authenticated with {masked(key)}. Balance: {data.get('balance', data)}")
    return 0

def logout() -> int:
    delete_key()
    print("Removed the stored Meshy credential. An exported MESHY_API_KEY is unchanged.")
    return 0

def main() -> int:
    parser = argparse.ArgumentParser(description="Secure Meshy authentication helper")
    parser.add_argument("command", choices=("login", "status", "logout"))
    args = parser.parse_args()
    return {"login": login, "status": status, "logout": logout}[args.command]()

if __name__ == "__main__":
    raise SystemExit(main())
