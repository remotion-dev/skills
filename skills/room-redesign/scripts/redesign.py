#!/usr/bin/env python3
"""
room-redesign: Direct Gemini image API caller for real estate virtual staging
and room redesign. No third-party wrappers. Reads GEMINI_API_KEY from env,
posts to generativelanguage.googleapis.com, saves returned images locally.

Usage:
    python3 redesign.py --image /path/room.jpg --prompt "Stage this living room..." --output-dir ./out

Optional:
    --count N        How many variations to request (default 1, max 4 per call)
    --model NAME     Override model (default: gemini-2.5-flash-image-preview)

Env vars:
    GEMINI_API_KEY      (required)
    GEMINI_IMAGE_MODEL  (optional, overrides --model default)
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import mimetypes
import os
import pathlib
import sys
import time

try:
    import requests
except ImportError:
    sys.stderr.write(
        "ERROR: 'requests' is not installed. Run:\n"
        "    pip3 install requests --break-system-packages\n"
    )
    sys.exit(2)


DEFAULT_MODEL = "gemini-2.5-flash-image"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


def guess_mime(path: pathlib.Path) -> str:
    mime, _ = mimetypes.guess_type(path.name)
    if mime is None:
        # Default to JPEG for unknown extensions to avoid API rejection
        return "image/jpeg"
    return mime


def encode_image(path: pathlib.Path) -> dict:
    """Return the `inlineData` dict Gemini expects for an input image."""
    raw = path.read_bytes()
    return {
        "inlineData": {
            "mimeType": guess_mime(path),
            "data": base64.b64encode(raw).decode("ascii"),
        }
    }


def build_payload(image_path: pathlib.Path, prompt: str) -> dict:
    """Build a Gemini generateContent request for image output."""
    return {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    encode_image(image_path),
                ],
            }
        ],
        "generationConfig": {
            # Tell the model we want an image back, not just text.
            "responseModalities": ["IMAGE", "TEXT"],
        },
    }


def call_gemini(api_key: str, model: str, payload: dict) -> dict:
    url = f"{API_BASE}/{model}:generateContent"
    resp = requests.post(
        url,
        params={"key": api_key},
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=120,
    )
    if resp.status_code != 200:
        # Surface the exact error so the caller knows what went wrong.
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        raise SystemExit(
            f"Gemini API error (HTTP {resp.status_code}):\n"
            f"{json.dumps(detail, indent=2) if isinstance(detail, dict) else detail}"
        )
    return resp.json()


def extract_images(response: dict) -> list[tuple[str, bytes]]:
    """Pull inline image bytes out of a generateContent response.

    Returns a list of (mime_type, raw_bytes) tuples. Empty list if no image
    came back (e.g. safety filter blocked it or prompt was text-only).
    """
    out = []
    for cand in response.get("candidates", []):
        content = cand.get("content") or {}
        for part in content.get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                mime = inline.get("mimeType") or inline.get("mime_type") or "image/png"
                out.append((mime, base64.b64decode(inline["data"])))
    return out


def extract_text(response: dict) -> str:
    """Concatenate any text the model returned alongside the image."""
    chunks = []
    for cand in response.get("candidates", []):
        content = cand.get("content") or {}
        for part in content.get("parts", []):
            if "text" in part and part["text"]:
                chunks.append(part["text"])
    return "\n".join(chunks).strip()


def extension_for_mime(mime: str) -> str:
    return {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/webp": ".webp",
    }.get(mime.lower(), ".png")


def run(args: argparse.Namespace) -> int:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        sys.stderr.write(
            "ERROR: GEMINI_API_KEY is not set.\n"
            "Get a free key at https://aistudio.google.com/ and export it:\n"
            "    export GEMINI_API_KEY='AIzaSy...'\n"
        )
        return 2

    model = (
        args.model
        or os.environ.get("GEMINI_IMAGE_MODEL", "").strip()
        or DEFAULT_MODEL
    )

    image_path = pathlib.Path(args.image).expanduser().resolve()
    if not image_path.is_file():
        sys.stderr.write(f"ERROR: input image not found: {image_path}\n")
        return 2

    out_dir = pathlib.Path(args.output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    prompt = args.prompt.strip()
    if not prompt:
        sys.stderr.write("ERROR: --prompt cannot be empty.\n")
        return 2

    count = max(1, min(int(args.count), 4))

    print(f"model     : {model}")
    print(f"image in  : {image_path}")
    print(f"output dir: {out_dir}")
    print(f"count     : {count}")
    print(f"prompt    : {prompt[:120]}{'...' if len(prompt) > 120 else ''}")
    print("-" * 60)

    payload = build_payload(image_path, prompt)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    saved_paths: list[pathlib.Path] = []
    any_text = []

    for i in range(1, count + 1):
        print(f"[{i}/{count}] calling Gemini...")
        response = call_gemini(api_key, model, payload)
        images = extract_images(response)
        text = extract_text(response)
        if text:
            any_text.append(text)

        if not images:
            print(f"[{i}/{count}] WARNING: no image in response.")
            if text:
                print(f"    model said: {text[:240]}")
            continue

        for j, (mime, data) in enumerate(images, 1):
            ext = extension_for_mime(mime)
            suffix = f"-{j}" if len(images) > 1 else ""
            fname = f"redesign-{stamp}-{i:02d}{suffix}{ext}"
            fpath = out_dir / fname
            fpath.write_bytes(data)
            saved_paths.append(fpath)
            print(f"[{i}/{count}] saved: {fpath}")

        # tiny pause to be polite to the API on multi-gen runs
        if i < count:
            time.sleep(0.5)

    print("-" * 60)
    if any_text:
        print("Model notes:")
        for t in any_text:
            print(f"  - {t}")

    if not saved_paths:
        sys.stderr.write("No images were generated. Check the prompt / quota / model.\n")
        return 1

    # Last line is machine-readable so the caller can parse it
    print("SAVED_IMAGES=" + "|".join(str(p) for p in saved_paths))
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Redesign a room photo via Gemini.")
    parser.add_argument("--image", required=True, help="Path to the source room photo")
    parser.add_argument("--prompt", required=True, help="Describe the redesign")
    parser.add_argument("--output-dir", required=True, help="Where to save the results")
    parser.add_argument("--count", default="1", help="How many variations (1-4)")
    parser.add_argument("--model", default="", help=f"Override model (default {DEFAULT_MODEL})")
    args = parser.parse_args(argv)
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
