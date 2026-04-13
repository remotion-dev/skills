#\!/usr/bin/env python3
"""
One-shot orchestrator: script → MP3 → asset → video → downloaded MP4.

Usage:
    python3 full_render.py --script path/to/script.ssml.txt --slug "my-video"
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

def run(cmd, **kwargs):
    print(f"+ {' '.join(cmd)}", flush=True)
    return subprocess.run(cmd, check=True, text=True, capture_output=True, **kwargs)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--script", required=True, help="Path to V6 SSML script file")
    p.add_argument("--slug", required=True)
    p.add_argument("--aspect", default="9:16")
    p.add_argument("--resolution", default="720p")
    p.add_argument("--output-root", default="/sessions/jolly-adoring-albattani/mnt/outputs/renders")
    args = p.parse_args()

    out_root = Path(args.output_root)
    out_root.mkdir(parents=True, exist_ok=True)
    mp3_path = out_root / f"{args.slug}.mp3"
    mp4_path = out_root / f"{args.slug}.mp4"

    # 1. TTS
    run(["python3", str(SCRIPT_DIR / "synthesize_voice.py"),
         "--text-file", args.script, "--out", str(mp3_path)])

    # 2. Upload
    import json as _json
    r = run(["python3", str(SCRIPT_DIR / "upload_asset.py"), str(mp3_path)])
    asset = _json.loads(r.stdout.strip().splitlines()[-1])
    asset_id = asset["asset_id"]
    print(f"asset_id={asset_id}")

    # 3. Create video
    r = run(["python3", str(SCRIPT_DIR / "render_video.py"),
             "--audio-asset-id", asset_id,
             "--title", args.slug,
             "--aspect", args.aspect,
             "--resolution", args.resolution])
    vid = _json.loads(r.stdout.strip().splitlines()[-1])["video_id"]
    print(f"video_id={vid}")

    # 4. Poll + download
    subprocess.run(["python3", str(SCRIPT_DIR / "poll_and_download.py"),
                    "--video-id", vid, "--out", str(mp4_path)],
                   check=True)
    print(f"DONE: {mp4_path}")

if __name__ == "__main__":
    main()
