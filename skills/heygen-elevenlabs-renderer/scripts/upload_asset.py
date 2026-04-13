#\!/usr/bin/env python3
"""
HeyGen asset uploader — wraps `heygen asset create --file` for audio MP3s.
CLI is required because api.heygen.com upload endpoint may not be fully allowlisted
in the sandbox; CLI handles the upload path under the hood.

Usage:
    python3 upload_asset.py path/to/audio.mp3
Prints: asset_id on stdout
"""
import json
import os
import subprocess
import sys
from pathlib import Path

CRED_DIR = Path(os.environ.get(
    "CLAUDE_CREDENTIALS_DIR",
    "/sessions/jolly-adoring-albattani/mnt/outputs/.claude-credentials"
))

def load_key():
    return (CRED_DIR / "heygen-key.txt").read_text().strip()

def upload(path):
    env = os.environ.copy()
    env["HEYGEN_API_KEY"] = load_key()
    env["PATH"] = os.path.expanduser("~/.local/bin") + ":" + env.get("PATH", "")

    result = subprocess.run(
        ["heygen", "asset", "create", "--file", str(path)],
        env=env, capture_output=True, text=True, timeout=120,
    )
    # CLI writes posthog warnings to stderr — ignore
    if result.returncode != 0:
        sys.exit(f"asset upload failed: {result.stderr}")

    # Find the JSON line in stdout
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("{"):
            data = json.loads(line)
            asset = data.get("data", {})
            return asset.get("asset_id"), asset.get("url")
    sys.exit(f"could not parse asset response: {result.stdout}")

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: upload_asset.py <audio.mp3>")
    asset_id, url = upload(sys.argv[1])
    print(json.dumps({"asset_id": asset_id, "url": url}))

if __name__ == "__main__":
    main()
