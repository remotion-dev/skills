#\!/usr/bin/env python3
"""
Poll HeyGen /v1/video_status.get until status == completed, then download MP4.

Usage:
    python3 poll_and_download.py --video-id <id> --out outputs/renders/slug.mp4
"""
import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

CRED_DIR = Path(os.environ.get(
    "CLAUDE_CREDENTIALS_DIR",
    "/sessions/jolly-adoring-albattani/mnt/outputs/.claude-credentials"
))

def load_key():
    return (CRED_DIR / "heygen-key.txt").read_text().strip()

def status(video_id):
    req = urllib.request.Request(
        f"https://api.heygen.com/v1/video_status.get?video_id={video_id}",
        headers={"X-Api-Key": load_key()},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def download(url, out_path):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=180) as r, open(out_path, "wb") as f:
        while True:
            chunk = r.read(65536)
            if not chunk:
                break
            f.write(chunk)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--video-id", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--interval", type=int, default=15)
    p.add_argument("--max-wait", type=int, default=600)
    args = p.parse_args()

    elapsed = 0
    while elapsed < args.max_wait:
        resp = status(args.video_id)
        data = resp.get("data", {})
        s = data.get("status")
        print(f"[{elapsed}s] status={s}", flush=True)
        if s == "completed":
            url = data.get("video_url")
            if not url:
                sys.exit("completed but no video_url returned")
            download(url, args.out)
            meta_path = Path(args.out).with_suffix(".meta.json")
            meta_path.write_text(json.dumps({
                "video_id": args.video_id,
                "video_url": url,
                "thumbnail_url": data.get("thumbnail_url"),
                "duration": data.get("duration"),
                "completed_at": int(time.time()),
            }, indent=2))
            print(json.dumps({"out": args.out, "meta": str(meta_path)}))
            return
        if s == "failed":
            sys.exit(f"render failed: {data.get('error')}")
        time.sleep(args.interval)
        elapsed += args.interval

    sys.exit(f"timeout after {args.max_wait}s — video still {s}")

if __name__ == "__main__":
    main()
