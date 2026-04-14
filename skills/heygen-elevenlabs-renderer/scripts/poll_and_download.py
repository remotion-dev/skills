#\!/usr/bin/env python3
"""
Poll HeyGen /v1/video_status.get until status == completed, then download MP4.

Emits meta.json AND a single-line JSON to stdout with dashboard URLs so the
V6 calendar button can surface "where to find it" links (HeyGen video page,
ElevenLabs history page, local MP4) without regex-scraping stdout.

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

HEYGEN_DASHBOARD = "https://app.heygen.com/videos/{video_id}"
ELEVEN_HISTORY = "https://elevenlabs.io/app/speech-synthesis/history"
ELEVEN_VOICE_LIB = "https://elevenlabs.io/app/voice-library"

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
    p.add_argument("--elevenlabs-voice-id", default=None,
                   help="Pin the voice_id used so the meta surfaces its history link")
    args = p.parse_args()

    elapsed = 0
    s = None
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

            heygen_dashboard_url = HEYGEN_DASHBOARD.format(video_id=args.video_id)
            meta = {
                "video_id": args.video_id,
                "video_url": url,
                "thumbnail_url": data.get("thumbnail_url"),
                "duration": data.get("duration"),
                "completed_at": int(time.time()),
                "local_mp4": str(Path(args.out).resolve()),
                "dashboards": {
                    "heygen_video_page": heygen_dashboard_url,
                    "heygen_projects": "https://app.heygen.com/projects",
                    "elevenlabs_history": ELEVEN_HISTORY,
                    "elevenlabs_voice_library": ELEVEN_VOICE_LIB,
                },
            }
            if args.elevenlabs_voice_id:
                meta["dashboards"]["elevenlabs_voice"] = (
                    f"https://elevenlabs.io/app/voice-lab/share/{args.elevenlabs_voice_id}"
                )

            meta_path = Path(args.out).with_suffix(".meta.json")
            meta_path.write_text(json.dumps(meta, indent=2))

            # Single-line JSON the V6 button's JS can JSON.parse directly.
            print("RENDER_RESULT=" + json.dumps({
                "status": "completed",
                "video_id": args.video_id,
                "out": str(Path(args.out).resolve()),
                "meta": str(meta_path.resolve()),
                "heygen_dashboard_url": heygen_dashboard_url,
                "elevenlabs_history_url": ELEVEN_HISTORY,
            }))
            return
        if s == "failed":
            sys.exit(f"render failed: {data.get('error')}")
        time.sleep(args.interval)
        elapsed += args.interval

    sys.exit(f"timeout after {args.max_wait}s — video still {s}")

if __name__ == "__main__":
    main()
