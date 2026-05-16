#!/usr/bin/env python3
"""
Shared transcription module for Graeham's skills ecosystem.

Single source of truth: any skill that needs to turn a video URL into text
calls this script. Two-tier transcription:

  Default tier: yt-dlp (audio download) + OpenAI Whisper (local in sandbox)
                Free. ~95% accuracy. 2-5 min per typical short video.

  Premium tier: yt-dlp (audio download) + Deepgram Nova-3 API
                $0.0043/min. 98%+ accuracy. Real-time for short videos.
                Requires DEEPGRAM_API_KEY env var.

Caches results by URL hash so the same URL never re-transcribes.

Usage from any skill:
    python3 transcribe.py --url <video_url>
    python3 transcribe.py --url <video_url> --premium
    python3 transcribe.py --file /path/to/local/audio.mp3
    python3 transcribe.py --url <url> --output /path/to/transcript.txt

Output: JSON to stdout with structure:
    {
      "transcript": "<clean text>",
      "source_url": "<url>",
      "source_platform": "youtube|instagram|tiktok|...",
      "duration_sec": 47,
      "word_count": 142,
      "tier": "whisper|deepgram",
      "cached": false,
      "cache_path": "<path to cached JSON>",
      "errors": []
    }
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import urlparse

# ---------- Cache ----------

CACHE_DIR = Path.home() / ".cache" / "graeham-transcripts"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def cache_key(source: str, tier: str) -> str:
    """Hash the source + tier so the same URL on different tiers caches separately."""
    h = hashlib.sha256(f"{source}|{tier}".encode("utf-8")).hexdigest()
    return h[:16]


def cache_get(key: str):
    path = CACHE_DIR / f"{key}.json"
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def cache_put(key: str, data: dict):
    path = CACHE_DIR / f"{key}.json"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return str(path)


# ---------- Platform detection ----------

def detect_platform(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if "youtube.com" in host or "youtu.be" in host:
        return "youtube"
    if "instagram.com" in host:
        return "instagram"
    if "tiktok.com" in host:
        return "tiktok"
    if "twitter.com" in host or "x.com" in host:
        return "x"
    if "vimeo.com" in host:
        return "vimeo"
    if "facebook.com" in host or "fb.watch" in host:
        return "facebook"
    return "unknown"


# ---------- Download (yt-dlp) ----------

def ensure_yt_dlp():
    """Verify yt-dlp is installed; install via pip if missing."""
    if shutil.which("yt-dlp"):
        return
    print("Installing yt-dlp...", file=sys.stderr)
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--break-system-packages",
         "--quiet", "yt-dlp"],
        check=True,
    )


def download_audio(url: str, workdir: Path) -> Path:
    """Download audio-only via yt-dlp to a temp dir. Returns the .mp3 path."""
    ensure_yt_dlp()
    out_template = str(workdir / "audio.%(ext)s")
    cmd = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "-o", out_template,
        "--no-warnings",
        "--quiet",
        url,
    ]
    subprocess.run(cmd, check=True)
    # Find the resulting audio file
    for ext in ("mp3", "m4a", "opus", "wav"):
        p = workdir / f"audio.{ext}"
        if p.exists():
            return p
    raise FileNotFoundError(f"yt-dlp ran but no audio file found in {workdir}")


def get_video_metadata(url: str) -> dict:
    """Pull duration + title from yt-dlp without downloading."""
    ensure_yt_dlp()
    try:
        result = subprocess.run(
            ["yt-dlp", "--dump-json", "--no-warnings", "--quiet", url],
            check=True, capture_output=True, text=True,
        )
        meta = json.loads(result.stdout)
        return {
            "duration_sec": int(meta.get("duration") or 0),
            "title": meta.get("title", ""),
            "uploader": meta.get("uploader", ""),
        }
    except Exception:
        return {"duration_sec": 0, "title": "", "uploader": ""}


# ---------- Tier 1: Whisper local ----------

def ensure_whisper():
    try:
        import whisper  # noqa: F401
        return
    except ImportError:
        pass
    print("Installing openai-whisper (this can take a minute)...", file=sys.stderr)
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--break-system-packages",
         "--quiet", "openai-whisper"],
        check=True,
    )


def transcribe_whisper(audio_path: Path, model_name: str = "base") -> str:
    """
    Transcribe with local Whisper.

    Model size tradeoff:
      tiny   ~75MB,  fastest, ~85% accuracy
      base   ~150MB, balanced, ~92% accuracy  (default)
      small  ~500MB, slower, ~95% accuracy
      medium ~1.5GB, much slower, ~97% accuracy

    The sandbox can handle base on CPU; larger models possible but slow.
    """
    ensure_whisper()
    import whisper
    model = whisper.load_model(model_name)
    result = model.transcribe(str(audio_path), fp16=False)
    return result["text"].strip()


# ---------- Tier 2: Deepgram API ----------

def transcribe_deepgram(audio_path: Path, api_key: str) -> str:
    """Transcribe with Deepgram Nova-3 (premium tier)."""
    # Use httpx for the API call; install if missing
    try:
        import httpx
    except ImportError:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--break-system-packages",
             "--quiet", "httpx"],
            check=True,
        )
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

    with httpx.Client(timeout=120.0) as client:
        response = client.post(url, params=params, headers=headers, content=audio_data)

    if response.status_code != 200:
        raise RuntimeError(
            f"Deepgram API error {response.status_code}: {response.text[:200]}"
        )

    data = response.json()
    # Pull the transcript from the standard response shape
    try:
        return data["results"]["channels"][0]["alternatives"][0]["transcript"].strip()
    except (KeyError, IndexError):
        raise RuntimeError(f"Unexpected Deepgram response shape: {json.dumps(data)[:300]}")


# ---------- Orchestrator ----------

def transcribe(
    source: str,
    is_url: bool,
    premium: bool = False,
    deepgram_key: str = None,
    whisper_model: str = "base",
) -> dict:
    tier = "deepgram" if premium else "whisper"

    # Cache check (URLs only — local files re-transcribe each time)
    cache_path = None
    if is_url:
        ck = cache_key(source, tier)
        cached = cache_get(ck)
        if cached:
            cached["cached"] = True
            cached["cache_path"] = str(CACHE_DIR / f"{ck}.json")
            return cached

    errors = []

    with tempfile.TemporaryDirectory() as tmpdir:
        workdir = Path(tmpdir)

        # Step 1: get audio
        if is_url:
            try:
                audio_path = download_audio(source, workdir)
            except subprocess.CalledProcessError as e:
                return {
                    "transcript": "",
                    "errors": [f"yt-dlp download failed: {e}"],
                    "cached": False,
                }
            meta = get_video_metadata(source)
            platform = detect_platform(source)
        else:
            audio_path = Path(source)
            meta = {"duration_sec": 0, "title": "", "uploader": ""}
            platform = "local-file"

        # Step 2: transcribe
        start_time = time.time()
        try:
            if premium:
                if not deepgram_key:
                    errors.append("Premium tier requested but DEEPGRAM_API_KEY not set. "
                                  "Falling back to Whisper.")
                    transcript = transcribe_whisper(audio_path, whisper_model)
                    tier = "whisper"
                else:
                    transcript = transcribe_deepgram(audio_path, deepgram_key)
            else:
                transcript = transcribe_whisper(audio_path, whisper_model)
        except Exception as e:
            return {
                "transcript": "",
                "errors": errors + [f"Transcription failed: {e}"],
                "cached": False,
            }
        elapsed = time.time() - start_time

    word_count = len(transcript.split())

    result = {
        "transcript": transcript,
        "source_url": source if is_url else None,
        "source_file": source if not is_url else None,
        "source_platform": platform,
        "title": meta.get("title", ""),
        "uploader": meta.get("uploader", ""),
        "duration_sec": meta.get("duration_sec", 0),
        "word_count": word_count,
        "tier": tier,
        "transcribe_seconds": round(elapsed, 1),
        "cached": False,
        "errors": errors,
    }

    if is_url:
        cp = cache_put(cache_key(source, tier), result)
        result["cache_path"] = cp

    return result


def main():
    parser = argparse.ArgumentParser(description="Transcribe a video URL or audio file.")
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--url", help="Video URL (YouTube, Instagram, TikTok, etc.)")
    src.add_argument("--file", help="Local audio file path")
    parser.add_argument("--premium", action="store_true",
                        help="Use Deepgram API (requires DEEPGRAM_API_KEY)")
    parser.add_argument("--whisper-model", default="base",
                        choices=["tiny", "base", "small", "medium"],
                        help="Whisper model size (default: base)")
    parser.add_argument("--output", help="Write transcript text to this file path")
    parser.add_argument("--json", action="store_true",
                        help="Output full JSON result (default: transcript text only)")
    args = parser.parse_args()

    is_url = bool(args.url)
    source = args.url or args.file

    deepgram_key = os.environ.get("DEEPGRAM_API_KEY", "")

    result = transcribe(
        source=source,
        is_url=is_url,
        premium=args.premium,
        deepgram_key=deepgram_key,
        whisper_model=args.whisper_model,
    )

    if args.output:
        Path(args.output).write_text(result.get("transcript", ""), encoding="utf-8")
        print(f"Transcript written to {args.output}", file=sys.stderr)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result.get("transcript", ""))

    return 0 if not result.get("errors") else 1


if __name__ == "__main__":
    sys.exit(main())
