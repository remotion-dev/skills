#!/usr/bin/env python3
"""
Download a royalty-free cinematic trailer track from Pixabay.

Three known-good URLs are baked in as defaults. If you want a different vibe,
add more to KNOWN_GOOD or pass --url <pixabay-cdn-url> directly.

Pixabay license:
- Free for commercial use
- No attribution required
- Modify freely
- Source: https://pixabay.com/service/license-summary/
"""
import argparse, sys, urllib.request
from pathlib import Path

# Production-tested Pixabay CDN URLs (free, no attribution, commercial OK)
KNOWN_GOOD = [
    # Name                          # URL                                                       # Vibe
    ("epic-cinematic.mp3",          "https://cdn.pixabay.com/audio/2022/05/27/audio_1808fbf07a.mp3",  "Epic Drama - 2:27 cinematic trailer arc"),
]

def download(url: str, out_path: Path) -> int:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    out_path.write_bytes(data)
    return len(data)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out-dir", default="./edit", help="Output directory (default: ./edit)")
    p.add_argument("--url", help="Override URL — must be a direct .mp3 from Pixabay CDN")
    p.add_argument("--list", action="store_true", help="List known-good tracks and exit")
    args = p.parse_args()

    if args.list:
        for name, url, vibe in KNOWN_GOOD:
            print(f"  {name}\n    {vibe}\n    {url}\n")
        return

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.url:
        name = args.url.rsplit("/", 1)[-1] or "music.mp3"
        path = out_dir / name
        try:
            size = download(args.url, path)
            print(f"OK    {name}  {size/1024/1024:.1f}MB")
        except Exception as e:
            sys.exit(f"FAIL  {name}  {e}")
    else:
        # Download all known-good
        for name, url, vibe in KNOWN_GOOD:
            path = out_dir / name
            try:
                size = download(url, path)
                print(f"OK    {name}  {size/1024/1024:.1f}MB  ({vibe})")
            except Exception as e:
                print(f"FAIL  {name}  {type(e).__name__}")

if __name__ == "__main__":
    main()
