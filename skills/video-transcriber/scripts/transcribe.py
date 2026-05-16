#!/usr/bin/env python3
"""
transcribe.py — Universal video transcriber for Graeham Watts's team.

Accepts a URL from any video platform (YouTube, Facebook, Instagram, TikTok,
Vimeo, Twitter/X, LinkedIn, Reddit, direct file, ~1,800+ supported by yt-dlp)
and returns a clean transcript.

Tier 1: Caption pull (free, instant, ~1-3 sec) — only YouTube + some others
Tier 2: yt-dlp audio download + Whisper transcription (free, local, ~30 sec – 3 min)

Usage:
    python3 transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID"
    python3 transcribe.py "https://www.instagram.com/reel/REEL_ID/" --json
    python3 transcribe.py "URL" --timestamps
    python3 transcribe.py "URL" --save  # write to outputs/transcripts/

Optional env vars:
    OPENAI_API_KEY  — use OpenAI Whisper API instead of local (faster, costs $0.006/min)
    APIFY_API_TOKEN — fallback for platforms yt-dlp doesn't support

No API keys required for the default free path.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------
# Platform detection
# ---------------------------------------------------------------

PLATFORM_PATTERNS = [
    ("youtube",   r"(?:youtube\.com|youtu\.be)"),
    ("facebook",  r"(?:facebook\.com|fb\.watch)"),
    ("instagram", r"instagram\.com"),
    ("tiktok",    r"tiktok\.com"),
    ("vimeo",     r"vimeo\.com"),
    ("twitter",   r"(?:twitter\.com|x\.com)"),
    ("linkedin",  r"linkedin\.com"),
    ("reddit",    r"reddit\.com"),
    ("direct",    r"\.(?:mp4|mov|m4a|mp3|wav|webm|mkv|avi)(?:\?|$)"),
]


def detect_platform(url: str) -> str:
    """Return platform name based on URL pattern."""
    for name, pattern in PLATFORM_PATTERNS:
        if re.search(pattern, url, re.IGNORECASE):
            return name
    return "unknown"


def youtube_video_id(url: str) -> str | None:
    """Extract YouTube video ID from various URL formats."""
    for pattern in [
        r"(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"(?:embed/|shorts/)([a-zA-Z0-9_-]{11})",
    ]:
        m = re.search(pattern, url)
        if m:
            return m.group(1)
    return None


# ---------------------------------------------------------------
# Dependency management
# ---------------------------------------------------------------

def ensure_pip_package(pkg_name: str, import_name: str | None = None) -> bool:
    """Install a pip package if it's not importable. Returns True on success."""
    mod = import_name or pkg_name.replace("-", "_")
    try:
        __import__(mod)
        return True
    except ImportError:
        pass

    print(f"[setup] Installing {pkg_name}...", file=sys.stderr)
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", pkg_name, "--break-system-packages", "--quiet"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"[setup] FAILED to install {pkg_name}: {result.stderr}", file=sys.stderr)
        return False
    return True


def ensure_ffmpeg() -> bool:
    """Verify ffmpeg is available."""
    result = subprocess.run(["which", "ffmpeg"], capture_output=True, text=True)
    if result.returncode == 0:
        return True
    print("[setup] ffmpeg not found — attempting apt install...", file=sys.stderr)
    subprocess.run(["apt-get", "install", "-y", "ffmpeg"], capture_output=True)
    return subprocess.run(["which", "ffmpeg"], capture_output=True).returncode == 0


# ---------------------------------------------------------------
# Tier 1: Caption pull
# ---------------------------------------------------------------

def caption_pull_youtube(video_id: str) -> dict | None:
    """Try to fetch existing YouTube captions via youtube-transcript-api. Returns transcript dict or None."""
    if not ensure_pip_package("youtube-transcript-api"):
        return None
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
    except ImportError:
        return None

    try:
        segments = YouTubeTranscriptApi.get_transcript(video_id)
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception as e:
        print(f"[tier1] caption pull failed: {e}", file=sys.stderr)
        return None

    text = " ".join(s["text"] for s in segments)
    return {
        "method": "caption_pull",
        "language": "en",  # api default; could be inspected for other langs
        "segments": [
            {"start": s["start"], "end": s["start"] + s["duration"], "text": s["text"]}
            for s in segments
        ],
        "transcript_plain": text,
    }


# ---------------------------------------------------------------
# Tier 2: yt-dlp + Whisper
# ---------------------------------------------------------------

def download_audio(url: str, tmpdir: str) -> str | None:
    """Use yt-dlp to download the audio track. Returns path to mp3 file or None on failure."""
    if not ensure_pip_package("yt-dlp"):
        return None
    if not ensure_ffmpeg():
        print("[tier2] ffmpeg unavailable, cannot extract audio", file=sys.stderr)
        return None

    output_template = os.path.join(tmpdir, "audio.%(ext)s")
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "-x", "--audio-format", "mp3",
        "--audio-quality", "0",
        "-o", output_template,
        "--quiet", "--no-warnings",
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        # Try updating yt-dlp once and retry (handles broken extractors)
        print("[tier2] yt-dlp failed, updating and retrying...", file=sys.stderr)
        subprocess.run([sys.executable, "-m", "pip", "install", "-U", "yt-dlp", "--break-system-packages", "--quiet"], capture_output=True)
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[tier2] yt-dlp failed after retry: {result.stderr}", file=sys.stderr)
            return None

    audio_path = os.path.join(tmpdir, "audio.mp3")
    if not os.path.exists(audio_path):
        return None
    return audio_path


def whisper_transcribe(audio_path: str, model_size: str = "base") -> dict | None:
    """
    Transcribe audio with Whisper. Prefers OpenAI API if OPENAI_API_KEY is set
    (faster, ~$0.006/min); falls back to local Whisper otherwise (free, slower).
    """
    api_key = os.environ.get("OPENAI_API_KEY")

    if api_key:
        # OpenAI Whisper API path
        if not ensure_pip_package("openai"):
            api_key = None  # fall back to local
        else:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                with open(audio_path, "rb") as f:
                    resp = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=f,
                        response_format="verbose_json",
                        timestamp_granularities=["segment"],
                    )
                segments = [
                    {"start": s.start, "end": s.end, "text": s.text}
                    for s in (resp.segments or [])
                ]
                return {
                    "method": "openai_whisper_api",
                    "language": resp.language,
                    "segments": segments,
                    "transcript_plain": resp.text,
                }
            except Exception as e:
                print(f"[tier2] OpenAI API failed: {e}, falling back to local Whisper", file=sys.stderr)

    # Local Whisper path
    if not ensure_pip_package("openai-whisper", import_name="whisper"):
        return None
    import whisper
    print(f"[tier2] Loading Whisper '{model_size}' model (first run downloads ~140 MB)...", file=sys.stderr)
    model = whisper.load_model(model_size)
    print(f"[tier2] Transcribing... this can take 30 sec – 3 min depending on length", file=sys.stderr)
    result = model.transcribe(audio_path, verbose=False)
    segments = [
        {"start": s["start"], "end": s["end"], "text": s["text"].strip()}
        for s in result.get("segments", [])
    ]
    return {
        "method": "local_whisper",
        "language": result.get("language", "unknown"),
        "segments": segments,
        "transcript_plain": result.get("text", "").strip(),
    }


# ---------------------------------------------------------------
# Metadata extraction
# ---------------------------------------------------------------

def fetch_metadata(url: str) -> dict:
    """Use yt-dlp to grab title + duration without downloading the video."""
    if not ensure_pip_package("yt-dlp"):
        return {}
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--dump-single-json", "--no-warnings", "--skip-download",
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {}
    try:
        info = json.loads(result.stdout)
        return {
            "title": info.get("title"),
            "duration_sec": info.get("duration"),
            "uploader": info.get("uploader") or info.get("channel"),
            "upload_date": info.get("upload_date"),
        }
    except json.JSONDecodeError:
        return {}


# ---------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------

def transcribe_url(url: str) -> dict:
    """Top-level entry: detect platform, run the right tier, return a normalized dict."""
    platform = detect_platform(url)

    # Tier 1 for YouTube (fast, free, often works)
    if platform == "youtube":
        vid = youtube_video_id(url)
        if vid:
            t1 = caption_pull_youtube(vid)
            if t1:
                meta = fetch_metadata(url)
                return {
                    "url": url,
                    "platform": platform,
                    "tier": 1,
                    **meta,
                    **t1,
                }

    # Tier 2: yt-dlp + Whisper (works for all platforms yt-dlp supports)
    meta = fetch_metadata(url)
    with tempfile.TemporaryDirectory() as tmpdir:
        audio = download_audio(url, tmpdir)
        if not audio:
            return {
                "url": url,
                "platform": platform,
                "error": "audio_download_failed",
                "message": "yt-dlp could not download audio for this URL. The platform may be unsupported, the video may be private/restricted, or the extractor may need updating.",
            }
        t2 = whisper_transcribe(audio)
        if not t2:
            return {
                "url": url,
                "platform": platform,
                "error": "whisper_failed",
                "message": "Whisper transcription failed. Check OPENAI_API_KEY or local Whisper install.",
            }
        return {
            "url": url,
            "platform": platform,
            "tier": 2,
            **meta,
            **t2,
        }


# ---------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------

def format_timestamp(seconds: float) -> str:
    """Format seconds as MM:SS or HH:MM:SS."""
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def render_plain(result: dict, with_timestamps: bool = False) -> str:
    """Render the result as readable plain text."""
    if "error" in result:
        return f"ERROR: {result['error']} — {result.get('message', '')}\n"

    lines = []
    if result.get("title"):
        lines.append(f"Title: {result['title']}")
    lines.append(f"Platform: {result.get('platform', 'unknown')}")
    if result.get("duration_sec"):
        lines.append(f"Duration: {format_timestamp(result['duration_sec'])}")
    if result.get("uploader"):
        lines.append(f"Uploader: {result['uploader']}")
    lines.append(f"Language: {result.get('language', 'unknown')}")
    lines.append(f"Method: {result.get('method', 'unknown')}")
    lines.append("")

    if with_timestamps and result.get("segments"):
        for seg in result["segments"]:
            ts = format_timestamp(seg["start"])
            lines.append(f"[{ts}] {seg['text']}")
    else:
        lines.append(result.get("transcript_plain", ""))

    return "\n".join(lines) + "\n"


def save_to_file(result: dict, output_dir: Path, fmt: str = "txt", with_timestamps: bool = False) -> Path:
    """Persist the transcript to outputs/transcripts/ for later reference."""
    output_dir.mkdir(parents=True, exist_ok=True)
    platform = result.get("platform", "video")
    title_slug = re.sub(r"[^a-z0-9]+", "-", (result.get("title") or "untitled").lower()).strip("-")[:50]
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    filename = f"transcript-{platform}-{title_slug}-{ts}.{fmt}"
    path = output_dir / filename

    if fmt == "json":
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    else:
        path.write_text(render_plain(result, with_timestamps=with_timestamps), encoding="utf-8")
    return path


# ---------------------------------------------------------------
# CLI
# ---------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Universal video transcriber")
    parser.add_argument("url", help="Video URL (YouTube, Facebook, Instagram, TikTok, etc.)")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of plain text")
    parser.add_argument("--timestamps", action="store_true", help="Include [MM:SS] timestamps per segment")
    parser.add_argument("--save", action="store_true", help="Also save to outputs/transcripts/")
    parser.add_argument("--output-dir", default="outputs/transcripts", help="Output directory when --save is set")
    args = parser.parse_args()

    print(f"[transcribe] URL: {args.url}", file=sys.stderr)
    print(f"[transcribe] Platform detected: {detect_platform(args.url)}", file=sys.stderr)

    result = transcribe_url(args.url)

    if args.save:
        out_path = save_to_file(
            result,
            Path(args.output_dir),
            fmt="json" if args.json else "txt",
            with_timestamps=args.timestamps,
        )
        print(f"[transcribe] Saved to: {out_path}", file=sys.stderr)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render_plain(result, with_timestamps=args.timestamps))


if __name__ == "__main__":
    main()
