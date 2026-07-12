from __future__ import annotations
import argparse
import base64
import json
import mimetypes
import time
from pathlib import Path
from urllib.parse import urlparse, urlsplit, urlunsplit
import requests
from credential_store import get_key

BASE = "https://api.meshy.ai"
PROMPT_LIMIT = 600

def image_value(value: str) -> str:
    """Accept an image as a URL, a data URI, or a local file path."""
    if value.startswith(("http://", "https://", "data:")):
        return value
    path = Path(value)
    if not path.is_file():
        raise ValueError(f"Image is neither a URL nor an existing file: {value}")
    mime = mimetypes.guess_type(path.name)[0]
    if mime not in ("image/jpeg", "image/png"):
        raise ValueError(f"Meshy accepts .jpg, .jpeg, or .png images, got: {path.name}")
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"

def style_prompt(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("Prompt cannot be empty.")
    if len(value) > PROMPT_LIMIT:
        raise ValueError(f"Prompt exceeds Meshy's {PROMPT_LIMIT}-character limit.")
    return value

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
        if response.status_code >= 400:
            detail = response.text[:2000]
            raise RuntimeError(f"Meshy API error {response.status_code} on {path}: {detail}")
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

    def image_to_3d(self, images: list[str], texture: bool, pbr: bool,
                    texture_prompt: str | None, target_polycount: int | None):
        payload: dict = {
            "ai_model": "latest",
            "should_texture": texture,
            "enable_pbr": pbr,
        }
        if texture_prompt:
            payload["texture_prompt"] = style_prompt(texture_prompt)
        if target_polycount is not None:
            payload["target_polycount"] = target_polycount
        if len(images) == 1:
            payload["image_url"] = image_value(images[0])
            return self.request("POST", "/openapi/v1/image-to-3d", json=payload)
        if len(images) > 4:
            raise ValueError("Multi-image-to-3D accepts at most 4 images.")
        payload["image_urls"] = [image_value(image) for image in images]
        return self.request("POST", "/openapi/v1/multi-image-to-3d", json=payload)

    def remesh(self, input_task_id: str | None, model_url: str | None,
               topology: str, target_polycount: int, target_formats: list[str]):
        payload: dict = {
            "topology": topology,
            "target_polycount": target_polycount,
            "target_formats": target_formats,
        }
        if input_task_id:
            payload["input_task_id"] = input_task_id
        elif model_url:
            payload["model_url"] = model_url
        else:
            raise ValueError("Provide --input-task-id or --model-url.")
        return self.request("POST", "/openapi/v1/remesh", json=payload)

    def retexture(self, input_task_id: str | None, model_url: str | None,
                  text_style: str | None, image_style: str | None,
                  original_uv: bool, pbr: bool):
        payload: dict = {
            "ai_model": "latest",
            "enable_original_uv": original_uv,
            "enable_pbr": pbr,
        }
        if input_task_id:
            payload["input_task_id"] = input_task_id
        elif model_url:
            payload["model_url"] = model_url
        else:
            raise ValueError("Provide --input-task-id or --model-url.")
        if text_style:
            payload["text_style_prompt"] = style_prompt(text_style)
        elif image_style:
            payload["image_style_url"] = image_value(image_style)
        else:
            raise ValueError("Provide --text-style-prompt or --image-style-url.")
        return self.request("POST", "/openapi/v1/retexture", json=payload)

    def rig(self, input_task_id: str | None, model_url: str | None, height_meters: float):
        payload: dict = {"height_meters": height_meters}
        if input_task_id:
            payload["input_task_id"] = input_task_id
        elif model_url:
            payload["model_url"] = model_url
        else:
            raise ValueError("Provide --input-task-id or --model-url.")
        return self.request("POST", "/openapi/v1/rigging", json=payload)

    def animate(self, rig_task_id: str, action_id: int, fps: int | None):
        payload: dict = {"rig_task_id": rig_task_id, "action_id": action_id}
        if fps is not None:
            payload["post_process"] = {"operation_type": "change_fps", "fps": fps}
        return self.request("POST", "/openapi/v1/animations", json=payload)

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

def url_suffix(url: str, fallback: str) -> str:
    return Path(urlparse(url).path).suffix or fallback

def collect_result_urls(node, prefix: str, out: list[tuple[str, str]]) -> None:
    if isinstance(node, str) and node.startswith(("http://", "https://")):
        out.append((prefix or "result", node))
    elif isinstance(node, dict):
        for key, value in node.items():
            label = key.removesuffix("_url")
            collect_result_urls(value, f"{prefix}_{label}" if prefix else label, out)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            collect_result_urls(value, f"{prefix}_{i}" if prefix else str(i), out)

def download_urls(data: dict, output: Path) -> list[Path]:
    output.mkdir(parents=True, exist_ok=True)
    asset_name = output.resolve().name or "model"
    # (filename, url, required) — optional files are skipped on fetch errors.
    candidates: list[tuple[str, str, bool]] = []
    def is_url(value) -> bool:
        # Meshy returns empty strings for formats a task did not produce.
        return isinstance(value, str) and value.startswith(("http://", "https://"))

    model_urls = data.get("model_urls") or {}
    if isinstance(model_urls, dict):
        for label, url in model_urls.items():
            if is_url(url):
                candidates.append((f"{asset_name}{url_suffix(url, f'.{label}')}", url, True))
    for i, entry in enumerate(data.get("texture_urls") or []):
        if is_url(entry):
            candidates.append((f"{asset_name}_texture_{i}{url_suffix(entry, '.bin')}", entry, True))
        elif isinstance(entry, dict):
            candidates.extend(
                (f"{asset_name}_{name}_{i}{url_suffix(url, '.bin')}", url, True)
                for name, url in entry.items()
                if is_url(url)
            )
    # Rigging and animation tasks return their files in a nested "result"
    # object (rigged_character_glb_url, basic_animations, animation_fbx_url…)
    # rather than model_urls. Walk it and download everything that is a URL.
    result_urls: list[tuple[str, str]] = []
    collect_result_urls(data.get("result"), "", result_urls)
    for label, url in result_urls:
        candidates.append((f"{asset_name}_{label}{url_suffix(url, '.bin')}", url, True))
    # thumbnail_url is signed like model_urls; usable here, but the signature
    # is stripped by sanitize_metadata before URLs are ever printed or saved.
    thumbnail_url = data.get("thumbnail_url")
    if isinstance(thumbnail_url, str) and thumbnail_url:
        candidates.append(
            (f"{asset_name}_thumbnail{url_suffix(thumbnail_url, '.png')}", thumbnail_url, False)
        )

    saved: list[Path] = []
    used: set[str] = set()
    for filename, url, required in candidates:
        if filename in used:
            stem = Path(filename).stem
            suffix = Path(filename).suffix
            filename = f"{stem}_{len(used)}{suffix}"
        used.add(filename)
        target = output / filename
        try:
            with requests.get(url, stream=True, timeout=120) as response:
                response.raise_for_status()
                with target.open("wb") as handle:
                    for chunk in response.iter_content(1024 * 1024):
                        if chunk:
                            handle.write(chunk)
        except requests.RequestException as error:
            if required:
                raise
            print(f"Skipping optional download {filename}: {error}")
            continue
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

    i23d = sub.add_parser("image-to-3d")
    i23d.add_argument("--image", action="append", required=True, dest="images",
                      help="URL, data URI, or local .jpg/.png path. Repeat for multi-image (max 4).")
    i23d.add_argument("--no-texture", action="store_true")
    i23d.add_argument("--enable-pbr", action="store_true")
    i23d.add_argument("--texture-prompt")
    i23d.add_argument("--target-polycount", type=int)
    add_spend_flag(i23d)

    remesh = sub.add_parser("remesh")
    remesh.add_argument("--input-task-id")
    remesh.add_argument("--model-url")
    remesh.add_argument("--topology", choices=("triangle", "quad"), default="triangle")
    remesh.add_argument("--target-polycount", type=int, default=30000)
    remesh.add_argument("--target-formats", nargs="+", default=["glb", "fbx"])
    add_spend_flag(remesh)

    retexture = sub.add_parser("retexture")
    retexture.add_argument("--input-task-id")
    retexture.add_argument("--model-url")
    retexture.add_argument("--text-style-prompt")
    retexture.add_argument("--image-style-url")
    retexture.add_argument("--enable-original-uv", action="store_true")
    retexture.add_argument("--enable-pbr", action="store_true")
    add_spend_flag(retexture)

    rig = sub.add_parser("rig")
    rig.add_argument("--input-task-id")
    rig.add_argument("--model-url")
    rig.add_argument("--height-meters", type=float, default=1.7)
    add_spend_flag(rig)

    animate = sub.add_parser("animate")
    animate.add_argument("--rig-task-id", required=True)
    animate.add_argument("--action-id", type=int, required=True,
                         help="From Meshy's animation library (0=Idle, 1=Walking…).")
    animate.add_argument("--fps", type=int, choices=(24, 25, 30, 60))
    add_spend_flag(animate)

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
    elif args.command == "image-to-3d":
        require_spend_confirmation(args, "Image-to-3D generation")
        print("Current balance:", json.dumps(client.balance()))
        print(json.dumps(client.image_to_3d(
            args.images, not args.no_texture, args.enable_pbr,
            args.texture_prompt, args.target_polycount), indent=2))
    elif args.command == "remesh":
        require_spend_confirmation(args, "Remesh")
        print("Current balance:", json.dumps(client.balance()))
        print(json.dumps(client.remesh(
            args.input_task_id, args.model_url, args.topology,
            args.target_polycount, args.target_formats), indent=2))
    elif args.command == "retexture":
        require_spend_confirmation(args, "Retexture")
        print("Current balance:", json.dumps(client.balance()))
        print(json.dumps(client.retexture(
            args.input_task_id, args.model_url, args.text_style_prompt,
            args.image_style_url, args.enable_original_uv, args.enable_pbr), indent=2))
    elif args.command == "rig":
        require_spend_confirmation(args, "Rigging")
        print("Current balance:", json.dumps(client.balance()))
        print(json.dumps(client.rig(
            args.input_task_id, args.model_url, args.height_meters), indent=2))
    elif args.command == "animate":
        require_spend_confirmation(args, "Animation")
        print("Current balance:", json.dumps(client.balance()))
        print(json.dumps(client.animate(args.rig_task_id, args.action_id, args.fps), indent=2))
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
