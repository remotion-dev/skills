#!/usr/bin/env python3
"""
Extract PAI 2.0 clip URLs from the canvas/timeline and download them.

Run this AFTER all 8 scenes have rendered in PAI. Two modes:

Mode 1 — paste-the-URLs:
    python3 extract_and_download.py \
        --urls "url1,url2,url3,url4,url5,url6,url7,url8" \
        --out-dir ./

Mode 2 — give it a manifest JSON:
    python3 extract_and_download.py --manifest manifest.json --out-dir ./

Manifest format:
    {
      "clips": [
        {"name": "scene1-cold-open.mp4", "url": "https://storage.googleapis.com/..."},
        {"name": "scene2-arrival.mp4",   "url": "https://storage.googleapis.com/..."},
        ...
      ]
    }

Browser console one-liner to extract from PAI's canvas/timeline:
    [...new Set([...document.querySelectorAll('video')].map(v => v.src || v.currentSrc).filter(Boolean))]

Click through each rendered clip in PAI's UI (Video tab in timeline view), then run that
JS in the console to grab the live video URLs. Copy them into a JSON manifest or pass
to --urls comma-separated.
"""
import argparse, json, sys, urllib.request
from pathlib import Path

DEFAULT_SCENE_NAMES = [
    "scene1-cold-open.mp4",
    "scene2-arrival.mp4",
    "scene3-war-room.mp4",
    "scene4-hustle-montage.mp4",
    "scene5-buyer-couple.mp4",
    "scene6-crisis-desk.mp4",
    "scene7-kitchen-resolution.mp4",
    "scene8-title-card.mp4",
]

def download(url: str, out_path: Path) -> int:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    out_path.write_bytes(data)
    return len(data)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--urls", help="Comma-separated list of clip URLs (must be 8 in script order)")
    p.add_argument("--manifest", help="JSON manifest with 'clips' array")
    p.add_argument("--out-dir", required=True, help="Output directory")
    args = p.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.manifest:
        manifest = json.loads(Path(args.manifest).read_text())
        clips = [(c["name"], c["url"]) for c in manifest["clips"]]
    elif args.urls:
        urls = [u.strip() for u in args.urls.split(",") if u.strip()]
        if len(urls) != len(DEFAULT_SCENE_NAMES):
            sys.exit(f"Expected {len(DEFAULT_SCENE_NAMES)} URLs, got {len(urls)}")
        clips = list(zip(DEFAULT_SCENE_NAMES, urls))
    else:
        sys.exit("Pass --urls or --manifest")

    for name, url in clips:
        out_path = out_dir / name
        try:
            size = download(url, out_path)
            print(f"OK    {name}  {size/1024/1024:.1f}MB")
        except Exception as e:
            print(f"FAIL  {name}  {type(e).__name__}: {str(e)[:80]}")

if __name__ == "__main__":
    main()
