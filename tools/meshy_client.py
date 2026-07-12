from __future__ import annotations
import argparse
import json
import time
from pathlib import Path
from urllib.parse import urlparse, urlsplit, urlunsplit
import requests
from credential_store import get_key

BASE = "https://api.meshy.ai"
PROMPT_LIMIT = 600

def require_spend_confirmation(args, operation: str) -> None:
    if not getattr(args, "confirm_spend", False):
        raise RuntimeError(
            f"{operation} may consume Meshy credits. Review the operation and "
            "current balance, obtain explicit user approval, then rerun with "
            "--confirm-spend."
        )

def sanitize_url(value: str) -> str:
    parts = urlsplit(value)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))

def sanitize_metadata(value):
    if isinstance(value, dict):
        return {k: sanitize_metadata(v) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize_metadata(v) for v in value]
    if isinstance(value, str) and value.startswith(("http://", "https://")):
        return sanitize_url(value)
    return value

class MeshyClient:
    def __init__(self) -> None:
        key = get_key()
        if not key:
            raise RuntimeError("Not authenticated. Run: python tools/meshy_auth.py login")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "User-Agent": "unity-meshy-studio/1.0.0",
        })

    def request(self, method: str, path: str, **kwargs):
        response = self.session.request(method, f"{BASE}{path}", timeout=60, **kwargs)
        if response.status_code in (401, 403):
            raise RuntimeError("Meshy authentication failed. Check or rotate the API key.")
        response.raise_for_status()
        if not response.content:
            return {}
        return response.json()

    def balance(self):
        return self.request("GET", "/openapi/v1/balance")

    def preview(self, prompt: str, model_type: str, target_polycount: int | None):
        prompt = prompt.strip()
        if not prompt:
            raise ValueError("Prompt cannot be empty.")
        if len(prompt) > PROMPT_LIMIT:
            raise ValueError(f"Prompt exceeds Meshy's {PROMPT_LIMIT}-character limit.")
        payload = {
            "mode": "preview",
            "prompt": prompt,
            "model_type": model_type,
            "ai_model": "latest",
            "should_remesh": model_type != "lowpoly",
        }
        if target_polycount is not None and model_type != "lowpoly":
            payload["target_polycount"] = target_polycount
        return self.request("POST", "/openapi/v2/text-to-3d", json=payload)

    def refine(self, preview_task_id: str):
        return self.request(
            "POST",
            "/openapi/v2/text-to-3d",
            json={"mode": "refine", "preview_task_id": preview_task_id},
        )

    def task(self, kind: str, task_id: str):
        version = "v2" if kind == "text-to-3d" else "v1"
        return self.request("GET", f"/openapi/{version}/{kind}/{task_id}")

    def wait(self, kind: str, task_id: str, timeout_seconds: int = 1800):
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            data = self.task(kind, task_id)
            status = str(data.get("status", "")).upper()
            print(f"{task_id}: {status or 'UNKNOWN'}")
            if status == "SUCCEEDED":
                return data
            if status in {"FAILED", "CANCELED", "CANCELLED", "EXPIRED"}:
                raise RuntimeError(json.dumps(sanitize_metadata(data), indent=2))
            time.sleep(10)
        raise TimeoutError(f"Task did not finish within {timeout_seconds} seconds.")

def download_urls(data: dict, output: Path) -> list[Path]:
    output.mkdir(parents=True, exist_ok=True)
    candidates: list[tuple[str, str]] = []
    model_urls = data.get("model_urls") or {}
    if isinstance(model_urls, dict):
        candidates.extend((name, url) for name, url in model_urls.items() if isinstance(url, str))
    for i, entry in enumerate(data.get("texture_urls") or []):
        if isinstance(entry, str):
            candidates.append((f"texture_{i}", entry))
        elif isinstance(entry, dict):
            candidates.extend(
                (f"{name}_{i}", url)
                for name, url in entry.items()
                if isinstance(url, str)
            )

    saved: list[Path] = []
    for label, url in candidates:
        suffix = Path(urlparse(url).path).suffix or ".bin"
        target = output / f"{label}{suffix}"
        with requests.get(url, stream=True, timeout=120) as response:
            response.raise_for_status()
            with target.open("wb") as handle:
                for chunk in response.iter_content(1024 * 1024):
                    if chunk:
                        handle.write(chunk)
        saved.append(target)
    return saved

def add_spend_flag(parser):
    parser.add_argument(
        "--confirm-spend",
        action="store_true",
        help="Confirms explicit user approval for this credit-consuming operation.",
    )

def main() -> int:
    parser = argparse.ArgumentParser(description="Meshy REST fallback client")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("balance")

    preview = sub.add_parser("text-to-3d-preview")
    preview.add_argument("--prompt", required=True)
    preview.add_argument("--model-type", choices=("standard", "lowpoly"), default="standard")
    preview.add_argument("--target-polycount", type=int)
    add_spend_flag(preview)

    refine = sub.add_parser("text-to-3d-refine")
    refine.add_argument("--preview-task-id", required=True)
    add_spend_flag(refine)

    task = sub.add_parser("task")
    task.add_argument("--kind", default="text-to-3d")
    task.add_argument("--id", required=True)

    wait = sub.add_parser("wait")
    wait.add_argument("--kind", default="text-to-3d")
    wait.add_argument("--id", required=True)
    wait.add_argument("--timeout", type=int, default=1800)

    download = sub.add_parser("download")
    download.add_argument("--kind", default="text-to-3d")
    download.add_argument("--id", required=True)
    download.add_argument("--output", required=True)

    args = parser.parse_args()
    client = MeshyClient()

    if args.command == "balance":
        print(json.dumps(client.balance(), indent=2))
    elif args.command == "text-to-3d-preview":
        require_spend_confirmation(args, "Text-to-3D preview")
        print("Current balance:", json.dumps(client.balance()))
        print(json.dumps(client.preview(args.prompt, args.model_type, args.target_polycount), indent=2))
    elif args.command == "text-to-3d-refine":
        require_spend_confirmation(args, "Text-to-3D refinement")
        print("Current balance:", json.dumps(client.balance()))
        print(json.dumps(client.refine(args.preview_task_id), indent=2))
    elif args.command == "task":
        print(json.dumps(sanitize_metadata(client.task(args.kind, args.id)), indent=2))
    elif args.command == "wait":
        print(json.dumps(sanitize_metadata(client.wait(args.kind, args.id, args.timeout)), indent=2))
    elif args.command == "download":
        data = client.wait(args.kind, args.id)
        output = Path(args.output)
        saved = download_urls(data, output)
        metadata = output / "task.json"
        metadata.write_text(
            json.dumps(sanitize_metadata(data), indent=2),
            encoding="utf-8",
        )
        print("\n".join(str(path) for path in [*saved, metadata]))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
