#!/usr/bin/env python3
"""
Local transcription CLI — runs on the USER'S Windows machine (NOT the Cowork sandbox).

Why this exists: The Cowork bash sandbox cannot reach YouTube, Instagram, Deepgram,
or HuggingFace. So transcription has to happen OUTSIDE the sandbox. This script does
that on Graeham's actual computer using his Deepgram key, and writes the result into
the Documents\\Claude\\Skills\\_inbox\\ folder where Cowork can read it.

Setup (one-time, on each machine that will use this):
    pip install yt-dlp httpx
    Set DEEPGRAM_API_KEY environment variable (or pass --key)

Usage:
    python transcribe_local.py --url "https://www.youtube.com/watch?v=..."
    python transcribe_local.py --url "https://instagram.com/reel/..." --tier premium
    python transcribe_local.py --file "C:\\path\\to\\audio.mp3"

The output lands in Documents\\Claude\\Skills\\_inbox\\transcript-{slug}-{ts}.txt
plus a manifest .json with metadata. Cowork picks it up from there.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


# Where transcripts land on the user's machine — Cowork can read this folder
INBOX_DIR = Path.home() / "Documents" / "Claude" / "Skills" / "_inbox"


def slugify(text: str, maxlen: int = 40) -> str:
    import re
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text[:maxlen] or "transcript"


def detect_platform(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if "youtube.com" in host or "youtu.be" in host: return "youtube"
    if "instagram.com" in host: return "instagram"
    if "tiktok.com" in host: return "tiktok"
    if "twitter.com" in host or "x.com" in host: return "x"
    if "vimeo.com" in host: return "vimeo"
    if "facebook.com" in host or "fb.watch" in host: return "facebook"
    return "unknown"


def check_dependencies():
    missing = []
    try:
        import yt_dlp  # noqa
    except ImportError:
        missing.append("yt-dlp")
    try:
        import httpx  # noqa
    except ImportError:
        missing.append("httpx")
    if missing:
        print(f"Missing dependencies: {missing}", file=sys.stderr)
        print(f"Install with: pip install {' '.join(missing)}", file=sys.stderr)
        sys.exit(2)


def get_video_metadata(url: str) -> dict:
    import yt_dlp
    opts = {"quiet": True, "no_warnings": True, "skip_download": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title", ""),
                "uploader": info.get("uploader") or info.get("channel", ""),
                "duration_sec": int(info.get("duration") or 0),
            }
        except Exception as e:
            print(f"⚠ Metadata fetch failed: {e}", file=sys.stderr)
            return {"title": "", "uploader": "", "duration_sec": 0}


def download_audio(url: str, workdir: Path) -> Path:
    import yt_dlp
    out_template = str(workdir / "audio.%(ext)s")
    opts = {
        "format": "bestaudio/best",
        "outtmpl": out_template,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    for ext in ("mp3", "m4a", "opus", "wav", "webm"):
        p = workdir / f"audio.{ext}"
        if p.exists():
            return p
    raise FileNotFoundError(f"yt-dlp ran but no audio file produced in {workdir}")


def transcribe_deepgram(audio_path: Path, api_key: str) -> dict:
    import httpx
    url = "https://api.deepgram.com/v1/listen"
    params = {
        "model": "nova-3",
        "smart_format": "true",
        "punctuate": "true",
        "paragraphs": "true",
    }
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "audio/mp3",
    }
    with open(audio_path, "rb") as f:
        audio_data = f.read()
    with httpx.Client(timeout=300.0) as client:
        r = client.post(url, params=params, headers=headers, content=audio_data)
    if r.status_code != 200:
        raise RuntimeError(f"Deepgram error {r.status_code}: {r.text[:200]}")
    data = r.json()
    text = data["results"]["channels"][0]["alternatives"][0]["transcript"].strip()
    return {"text": text, "raw": data}


def main():
    parser = argparse.ArgumentParser(description="Local transcription CLI for Watts content pipeline")
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--url", help="Video URL (any yt-dlp supported site)")
    src.add_argument("--file", help="Local audio file path")
    parser.add_argument("--tier", choices=["premium"], default="premium",
                        help="Currently only premium (Deepgram) supported — Whisper local needs separate install")
    parser.add_argument("--key", help="Deepgram API key (defaults to DEEPGRAM_API_KEY env var)")
    parser.add_argument("--inbox", default=str(INBOX_DIR),
                        help=f"Where to write the transcript (default: {INBOX_DIR})")
    parser.add_argument("--slug", help="Override the auto-generated slug")
    args = parser.parse_args()

    check_dependencies()

    api_key = args.key or os.environ.get("DEEPGRAM_API_KEY", "")
    if not api_key:
        # Try loading from the Documents persistence path
        persistent_key = Path.home() / "Documents" / "Claude" / "Skills" / "deepgram-key.txt"
        if persistent_key.exists():
            api_key = persistent_key.read_text().strip()
    if not api_key:
        print("✗ No Deepgram API key found. Pass --key or set DEEPGRAM_API_KEY env var,", file=sys.stderr)
        print(f"  or save the key to {persistent_key}", file=sys.stderr)
        sys.exit(3)

    inbox = Path(args.inbox)
    inbox.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M")

    is_url = bool(args.url)
    source = args.url or args.file

    print(f"→ Source: {source}")
    print(f"→ Tier: {args.tier} (Deepgram Nova-3)")
    print(f"→ Output inbox: {inbox}")

    metadata = {"title": "", "uploader": "", "duration_sec": 0}
    platform = "local-file"

    with tempfile.TemporaryDirectory() as tmpdir:
        workdir = Path(tmpdir)

        if is_url:
            platform = detect_platform(source)
            print(f"→ Platform: {platform}")
            print(f"→ Fetching metadata...")
            metadata = get_video_metadata(source)
            if metadata["title"]:
                print(f"  Title: {metadata['title']}")
            if metadata["duration_sec"]:
                mins = metadata["duration_sec"] // 60
                secs = metadata["duration_sec"] % 60
                print(f"  Duration: {mins}m{secs}s")
            print(f"→ Downloading audio...")
            t0 = time.time()
            audio_path = download_audio(source, workdir)
            print(f"  Done in {time.time() - t0:.1f}s — {audio_path.stat().st_size // 1024} KB")
        else:
            audio_path = Path(source)
            if not audio_path.exists():
                print(f"✗ Audio file not found: {audio_path}", file=sys.stderr)
                sys.exit(4)
            print(f"→ Using local audio file: {audio_path.stat().st_size // 1024} KB")

        print(f"→ Transcribing via Deepgram Nova-3...")
        t0 = time.time()
        result = transcribe_deepgram(audio_path, api_key)
        elapsed = time.time() - t0
        print(f"  Done in {elapsed:.1f}s")

    transcript_text = result["text"]
    word_count = len(transcript_text.split())

    # Generate slug from title or URL
    slug = args.slug or slugify(metadata.get("title") or (urlparse(source).path.split("/")[-2] if is_url else "local"))

    # Write transcript text file
    transcript_path = inbox / f"transcript-{slug}-{ts}.txt"
    transcript_path.write_text(transcript_text, encoding="utf-8")

    # Write manifest JSON for Cowork to read
    manifest = {
        "transcript_file": transcript_path.name,
        "source_url": source if is_url else None,
        "source_file": source if not is_url else None,
        "source_platform": platform,
        "title": metadata["title"],
        "uploader": metadata["uploader"],
        "duration_sec": metadata["duration_sec"],
        "word_count": word_count,
        "tier": "deepgram-nova-3",
        "transcribed_at": datetime.now().isoformat(),
        "transcribe_seconds": round(elapsed, 1),
        "status": "ready-for-cowork",
    }
    manifest_path = inbox / f"transcript-{slug}-{ts}.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print()
    print(f"✓ Transcript ready ({word_count} words)")
    print(f"  Text:     {transcript_path}")
    print(f"  Manifest: {manifest_path}")
    print()
    print("Next: In Cowork, say 'Repurpose the latest from my inbox' and the skill takes over.")


if __name__ == "__main__":
    main()
