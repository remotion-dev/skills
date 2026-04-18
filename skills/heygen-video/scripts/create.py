#!/usr/bin/env python3
"""
create.py — Submit a HeyGen avatar video for Graeham Watts.

Does NOT wait for completion. Returns video_id + dashboard URL immediately,
so the caller can report back to the user and poll separately via status.py.

Usage:
    python3 create.py --script "Hello world" [--look digital_twin] [--aspect 9:16] [--title "..."]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import shutil
import subprocess
import sys

# --- Graeham's 6 looks (see references/avatars.md for rationale) ---
# Two Graeham voice clones exist; we default to "Graeham Watts Voice Clone" globally.
# Override with --voice on a per-video basis.
VOICE_CLONE_PRIMARY = "717249201f7745988219b9aeb9041b42"   # "Graeham Watts Voice Clone" — DEFAULT
VOICE_CLONE_TWIN    = "7739db30ae554014a7b93a59a134640e"   # "Graeham Watts -- 142" — paired with digital_twin

LOOKS: dict[str, dict] = {
    "digital_twin":       {"id": "159cd7b883724fdb9a51b97dec94df89", "orientation": "portrait",  "avatar_type": "video"},
    "casual_chic":        {"id": "afdc7e3e9f0c45de896fa687c594a216", "orientation": "portrait",  "avatar_type": "photo"},
    "freshly_ironed":     {"id": "09fed5d2c0b74376b6e7313cbb888c86", "orientation": "portrait",  "avatar_type": "photo"},
    "fashion_flip":       {"id": "b0644e6b20ba414981b7821d88caf675", "orientation": "portrait",  "avatar_type": "photo"},
    "bespectacled":       {"id": "1b25c855f03b471da5bacb918c4acbc0", "orientation": "portrait",  "avatar_type": "photo"},
    "suburban_serenity":  {"id": "bbc381b39e0f458e8d274cf1ac2c38ba", "orientation": "landscape", "avatar_type": "photo"},
}
DEFAULT_ASPECT = "9:16"
DEFAULT_VOICE = VOICE_CLONE_PRIMARY  # "Graeham Watts Voice Clone" — used across all looks unless --voice overrides
JOB_LOG_DIR = pathlib.Path("/tmp/heygen_jobs")


def die(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Submit a HeyGen avatar video for Graeham Watts.",
        epilog="You MUST specify the avatar via --avatar-id or --look; there is no default. "
               "The skill enforces this so the user is always asked before a video is submitted.",
    )
    p.add_argument("--script", required=True, help="Text script for the avatar to speak.")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--avatar-id", default=None,
                       help="Raw HeyGen avatar look ID (32-char hex). Preferred when the user pastes an ID.")
    group.add_argument("--look", default=None, choices=LOOKS.keys(),
                       help=f"Named Graeham look. One of: {', '.join(LOOKS.keys())}.")
    p.add_argument("--aspect", default=None, choices=["9:16", "16:9"],
                   help="Aspect ratio. Defaults to 9:16 for portrait, 16:9 when --look suburban_serenity.")
    p.add_argument("--title", default=None, help="Dashboard title. Defaults to 'Graeham Watts - <date>'.")
    p.add_argument("--voice", default=DEFAULT_VOICE,
                   help=f"Voice ID. Defaults to Voice Clone ({DEFAULT_VOICE}). "
                        f"Twin voice: {VOICE_CLONE_TWIN}. Any valid HeyGen voice_id accepted.")
    p.add_argument("--resolution", default="1080p", choices=["4k", "1080p", "720p"],
                   help="Output resolution (default: 1080p).")
    p.add_argument("--background-hex", default="#1a1a2e",
                   help="Solid-color background as hex (default: #1a1a2e = deep navy).")
    return p.parse_args()


def ensure_prereqs() -> None:
    if not os.environ.get("HEYGEN_API_KEY"):
        die("HEYGEN_API_KEY is not set. Export it first.")
    if not shutil.which("heygen"):
        # Try adding ~/.local/bin to PATH in case setup was just run
        local_bin = str(pathlib.Path.home() / ".local" / "bin")
        os.environ["PATH"] = f"{local_bin}:{os.environ.get('PATH', '')}"
        if not shutil.which("heygen"):
            die("heygen CLI not found on PATH. Run scripts/setup.sh first.")


def resolve_avatar(args: argparse.Namespace) -> tuple[str, str, str]:
    """
    Returns (avatar_id, orientation, avatar_type).
    - If --look was used, pull from LOOKS dict.
    - If --avatar-id was used, we don't know orientation/type in advance; default to portrait/video.
    """
    if args.look:
        look = LOOKS[args.look]
        return look["id"], look["orientation"], look["avatar_type"]
    # Raw avatar_id path — we don't know its metadata, so assume portrait + video avatar.
    # Photo-avatar-only fields (expressiveness) will be skipped in payload to be safe.
    return args.avatar_id, "portrait", "unknown"


def pick_aspect(orientation: str, cli_arg: str | None) -> str:
    if cli_arg is not None:
        return cli_arg
    return "16:9" if orientation == "landscape" else DEFAULT_ASPECT


def build_payload(args: argparse.Namespace, avatar_id: str, avatar_type: str, aspect: str, title: str) -> dict:
    payload: dict = {
        "type": "avatar",
        "avatar_id": avatar_id,
        "script": args.script,
        "voice_id": args.voice,
        "aspect_ratio": aspect,
        "output_format": "mp4",
        "resolution": args.resolution,
        "title": title,
        "background": {"type": "color", "value": args.background_hex},
    }
    # expressiveness is photo_avatar-only. Only set it when we're sure.
    if avatar_type == "photo":
        payload["expressiveness"] = "medium"
    return payload


def submit(payload: dict) -> dict:
    """Invoke heygen CLI; return parsed JSON response."""
    proc = subprocess.run(
        ["heygen", "video", "create", "-d", json.dumps(payload)],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        die(f"heygen video create failed (exit {proc.returncode}):\nstdout: {proc.stdout}\nstderr: {proc.stderr}")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        die(f"Could not parse CLI output as JSON:\n{proc.stdout}")


def log_job(video_id: str, record: dict) -> pathlib.Path:
    JOB_LOG_DIR.mkdir(parents=True, exist_ok=True)
    path = JOB_LOG_DIR / f"{video_id}.json"
    path.write_text(json.dumps(record, indent=2))
    return path


def main() -> int:
    args = parse_args()
    ensure_prereqs()

    avatar_id, orientation, avatar_type = resolve_avatar(args)
    aspect = pick_aspect(orientation, args.aspect)
    title = args.title or f"Graeham Watts - {dt.date.today().isoformat()}"
    payload = build_payload(args, avatar_id, avatar_type, aspect, title)

    # Human-friendly label for the printed summary
    avatar_label = args.look if args.look else f"raw id: {avatar_id}"

    print(f"Submitting HeyGen video:")
    print(f"  avatar:     {avatar_label}")
    print(f"  voice:      {args.voice}"
          f"{' (default clone)' if args.voice == DEFAULT_VOICE else ''}"
          f"{' (twin voice)' if args.voice == VOICE_CLONE_TWIN else ''}")
    print(f"  aspect:     {aspect}")
    print(f"  resolution: {args.resolution}")
    print(f"  title:      {title}")
    print(f"  script:     {args.script[:80]}{'...' if len(args.script) > 80 else ''}")
    print()

    response = submit(payload)
    data = response.get("data", response)
    video_id = data.get("video_id")
    if not video_id:
        die(f"No video_id in response: {response}")

    dashboard_url = f"https://app.heygen.com/videos/{video_id}"
    record = {
        "video_id": video_id,
        "submitted_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "payload": payload,
        "dashboard_url": dashboard_url,
    }
    log_path = log_job(video_id, record)

    print(f"✓ Submitted.")
    print(f"  video_id:  {video_id}")
    print(f"  dashboard: {dashboard_url}")
    print(f"  log:       {log_path}")
    print()
    print("HeyGen typically takes 2–10 minutes for short scripts.")
    print("Check status: python3 scripts/status.py --video-id " + video_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
