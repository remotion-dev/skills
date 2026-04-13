#\!/usr/bin/env python3
"""
Create a HeyGen avatar video using a pre-uploaded audio asset (voice_type: audio).
Uses HeyGen v3 /videos endpoint via the CLI.

Usage:
    python3 render_video.py --audio-asset-id <id> --title "..." [--avatar-id <id>]
Prints: video_id on stdout
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

CRED_DIR = Path(os.environ.get(
    "CLAUDE_CREDENTIALS_DIR",
    "/sessions/jolly-adoring-albattani/mnt/outputs/.claude-credentials"
))
REGISTRY = Path(__file__).parent.parent / "references" / "registry.json"

def load_key():
    return (CRED_DIR / "heygen-key.txt").read_text().strip()

def load_defaults():
    if REGISTRY.exists():
        return json.loads(REGISTRY.read_text()).get("defaults", {})
    return {
        "heygen_avatar_id": "9a3600b16f604059b6ab8b9a55e29ea9",
    }

def create(audio_asset_id, title, avatar_id=None, aspect="9:16", resolution="720p"):
    env = os.environ.copy()
    env["HEYGEN_API_KEY"] = load_key()
    env["PATH"] = os.path.expanduser("~/.local/bin") + ":" + env.get("PATH", "")

    avatar_id = avatar_id or load_defaults()["heygen_avatar_id"]
    payload = {
        "type": "avatar",
        "avatar_id": avatar_id,
        "audio_asset_id": audio_asset_id,
        "aspect_ratio": aspect,
        "resolution": resolution,
        "title": title,
    }

    result = subprocess.run(
        ["heygen", "video", "create", "-d", "-"],
        input=json.dumps(payload), env=env,
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0:
        sys.exit(f"video create failed: {result.stderr}")

    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("{"):
            data = json.loads(line)
            return data.get("data", {}).get("video_id")
    sys.exit(f"could not parse create response: {result.stdout}")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--audio-asset-id", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--avatar-id")
    p.add_argument("--aspect", default="9:16", choices=["9:16", "16:9"])
    p.add_argument("--resolution", default="720p", choices=["720p", "1080p", "4k"])
    args = p.parse_args()

    vid = create(args.audio_asset_id, args.title, args.avatar_id, args.aspect, args.resolution)
    print(json.dumps({"video_id": vid}))

if __name__ == "__main__":
    main()
