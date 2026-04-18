#!/usr/bin/env python3
"""
youtube_transcriber.py
-----------------------
Two-tier YouTube transcription utility for the Bay Area Content Engine.

Tier 1: Pull existing captions/auto-captions via youtube-transcript-api (free, instant).
Tier 2: Download audio via yt-dlp → transcribe with OpenAI Whisper (free, local, ~1-3 min).

Usage:
    # Single video — tries captions first, falls back to Whisper
    python youtube_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID"

    # Force Whisper (skip caption check)
    python youtube_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID" --force-whisper

    # Entire channel (pulls latest N videos)
    python youtube_transcriber.py "https://www.youtube.com/@ChannelName" --channel --limit 10

    # Output as JSON instead of plain text
    python youtube_transcriber.py "URL" --format json

    # Custom output directory
    python youtube_transcriber.py "URL" --output-dir ./my_transcripts

Output: transcript-{video_id}-{timestamp}.txt (or .json) in outputs/transcripts/

Requires:
    Tier 1: pip install youtube-transcript-api --break-system-packages
    Tier 2: pip install yt-dlp openai-whisper --break-system-packages
            (also needs ffmpeg: apt install ffmpeg)

Cost: $0. Both tiers are completely free.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------
# Dependency checks
# ---------------------------------------------------------------

def check_tier1_deps():
    """Check if youtube-transcript-api is available."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        return True
    except ImportError:
        return False


def check_tier2_deps():
    """Check if yt-dlp and whisper are available."""
    has_ytdlp = False
    has_whisper = False
    try:
        import yt_dlp
        has_ytdlp = True
    except ImportError:
        pass
    try:
        import whisper
        has_whisper = True
    except ImportError:
        pass
    return has_ytdlp, has_whisper


# ---------------------------------------------------------------
# URL parsing
# ---------------------------------------------------------------

def extract_video_id(url: str) -> str | None:
    """Extract YouTube video ID from various URL formats."""
    patterns = [
        r'(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
        r'(?:shorts/)([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    # Maybe it's just a video ID by itself
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
        return url
    return None


def is_channel_url(url: str) -> bool:
    """Check if URL is a channel/playlist rather than a single video."""
    channel_patterns = [
        r'youtube\.com/@',
        r'youtube\.com/c/',
        r'youtube\.com/channel/',
        r'youtube\.com/user/',
        r'youtube\.com/playlist',
    ]
    return any(re.search(p, url) for p in channel_patterns)


def get_channel_video_ids(url: str, limit: int = 10) -> list[str]:
    """Use yt-dlp to get video IDs from a channel or playlist."""
    try:
        import yt_dlp
    except ImportError:
        print("ERROR: yt-dlp required for channel scraping. Run: pip install yt-dlp --break-system-packages")
        sys.exit(1)

    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'no_warnings': True,
        'playlistend': limit,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if 'entries' in info:
            video_ids = []
            for entry in info['entries']:
                if entry and entry.get('id'):
                    video_ids.append(entry['id'])
                if len(video_ids) >= limit:
                    break
            return video_ids
        elif info.get('id'):
            return [info['id']]
    return []


def get_video_title(video_id: str) -> str:
    """Try to get video title via yt-dlp (best-effort)."""
    try:
        import yt_dlp
        ydl_opts = {'quiet': True, 'no_warnings': True, 'skip_download': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            return info.get('title', video_id)
    except Exception:
        return video_id


# ---------------------------------------------------------------
# Tier 1: Caption-based transcription (free, instant)
# ---------------------------------------------------------------

def transcribe_via_captions(video_id: str, languages: list[str] = None) -> dict | None:
    """
    Pull transcript from YouTube's caption system.
    Uses youtube-transcript-api v1.2+ (instance-based API).
    Tries: requested languages → English → auto-generated → any available.
    Returns dict with 'text', 'segments', 'method', 'language' or None if unavailable.
    """
    from youtube_transcript_api import YouTubeTranscriptApi

    if languages is None:
        languages = ['en']

    ytt = YouTubeTranscriptApi()

    try:
        # Step 1: List available transcripts to find the best one
        transcript_list = ytt.list(video_id)
        lang_used = None
        chosen = None

        # Search through available transcripts
        for t in transcript_list:
            t_lang = t.language_code if hasattr(t, 'language_code') else str(t)
            t_is_generated = t.is_generated if hasattr(t, 'is_generated') else False

            # Prefer manual transcripts in requested language
            if t_lang in languages and not t_is_generated:
                chosen = t
                lang_used = f"{t_lang} (manual)"
                break

        # Fall back to auto-generated in requested language
        if chosen is None:
            for t in transcript_list:
                t_lang = t.language_code if hasattr(t, 'language_code') else str(t)
                if t_lang in languages:
                    chosen = t
                    t_is_generated = t.is_generated if hasattr(t, 'is_generated') else True
                    lang_used = f"{t_lang} ({'auto-generated' if t_is_generated else 'manual'})"
                    break

        # Fall back to any available transcript
        if chosen is None:
            for t in transcript_list:
                chosen = t
                t_lang = t.language_code if hasattr(t, 'language_code') else 'unknown'
                t_is_generated = t.is_generated if hasattr(t, 'is_generated') else True
                lang_used = f"{t_lang} ({'auto-generated' if t_is_generated else 'manual'})"
                break

        if chosen is None:
            print(f"  [!] No transcripts found for {video_id}")
            return None

        # Step 2: Fetch the actual transcript content
        try:
            fetch_lang = chosen.language_code if hasattr(chosen, 'language_code') else languages[0]
            result = ytt.fetch(video_id, languages=[fetch_lang])
        except Exception:
            result = ytt.fetch(video_id)

        # Step 3: Parse the result into segments
        normalized_segments = []
        texts = []

        snippets = result if hasattr(result, '__iter__') else getattr(result, 'snippets', [result])

        for seg in snippets:
            if isinstance(seg, dict):
                text = seg.get('text', '')
                start = seg.get('start', 0)
                duration = seg.get('duration', 0)
            else:
                text = getattr(seg, 'text', str(seg))
                start = getattr(seg, 'start', 0)
                duration = getattr(seg, 'duration', 0)

            texts.append(text.strip())
            normalized_segments.append({
                'text': text.strip(),
                'start': float(start),
                'duration': float(duration),
            })

        full_text = ' '.join(texts)

        return {
            'text': full_text,
            'segments': normalized_segments,
            'method': 'captions',
            'language': lang_used,
            'video_id': video_id,
        }

    except Exception as e:
        print(f"  [!] Captions unavailable for {video_id}: {e}")
        return None


# ---------------------------------------------------------------
# Tier 2: Whisper-based transcription (free, local, slower)
# ---------------------------------------------------------------

def transcribe_via_whisper(video_id: str, model_size: str = "base") -> dict | None:
    """
    Download audio via yt-dlp, transcribe with OpenAI Whisper.
    model_size options: tiny, base, small, medium, large
    'base' is the sweet spot for speed vs accuracy on most content.
    Returns dict with 'text', 'segments', 'method', 'language' or None on failure.
    """
    try:
        import yt_dlp
    except ImportError:
        print("ERROR: yt-dlp not installed. Run: pip install yt-dlp --break-system-packages")
        return None

    try:
        import whisper
    except ImportError:
        print("ERROR: whisper not installed. Run: pip install openai-whisper --break-system-packages")
        print("       Also needs ffmpeg: apt install ffmpeg (Linux) or brew install ffmpeg (Mac)")
        return None

    url = f"https://www.youtube.com/watch?v={video_id}"

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, "audio.mp3")

        # Download audio only
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(tmpdir, 'audio.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
            'quiet': True,
            'no_warnings': True,
        }

        print(f"  [*] Downloading audio for {video_id}...")
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"  [!] Failed to download audio: {e}")
            return None

        # Find the downloaded file
        audio_files = list(Path(tmpdir).glob("audio.*"))
        if not audio_files:
            print("  [!] No audio file found after download")
            return None
        audio_path = str(audio_files[0])

        # Transcribe with Whisper
        print(f"  [*] Transcribing with Whisper ({model_size} model)...")
        try:
            model = whisper.load_model(model_size)
            result = model.transcribe(audio_path)
        except Exception as e:
            print(f"  [!] Whisper transcription failed: {e}")
            return None

        segments = [
            {
                'text': seg['text'].strip(),
                'start': seg['start'],
                'duration': seg['end'] - seg['start'],
            }
            for seg in result.get('segments', [])
        ]

        return {
            'text': result['text'].strip(),
            'segments': segments,
            'method': 'whisper',
            'language': result.get('language', 'unknown'),
            'model': model_size,
            'video_id': video_id,
        }


# ---------------------------------------------------------------
# Main transcription logic (two-tier)
# ---------------------------------------------------------------

def transcribe_video(video_id: str, force_whisper: bool = False,
                     whisper_model: str = "base",
                     languages: list[str] = None) -> dict | None:
    """
    Two-tier transcription:
    1. Try captions (free, instant)
    2. Fall back to Whisper if no captions (free, slower)

    Returns dict with transcript data or None if both fail.
    """
    title = get_video_title(video_id)
    print(f"\n{'='*60}")
    print(f"Transcribing: {title}")
    print(f"Video ID: {video_id}")
    print(f"{'='*60}")

    result = None

    # Tier 1: Captions
    if not force_whisper and check_tier1_deps():
        print("  [*] Tier 1: Checking for captions...")
        result = transcribe_via_captions(video_id, languages)
        if result:
            print(f"  [✓] Got transcript via captions ({result['language']})")
            print(f"  [✓] Length: {len(result['text'])} chars, {len(result['segments'])} segments")

    # Tier 2: Whisper fallback
    if result is None:
        has_ytdlp, has_whisper = check_tier2_deps()
        if has_ytdlp and has_whisper:
            print("  [*] Tier 2: Downloading audio + Whisper transcription...")
            result = transcribe_via_whisper(video_id, whisper_model)
            if result:
                print(f"  [✓] Got transcript via Whisper ({result['language']})")
                print(f"  [✓] Length: {len(result['text'])} chars, {len(result['segments'])} segments")
        elif not has_whisper:
            print("  [!] Tier 2 unavailable: openai-whisper not installed")
            print("      To enable: pip install openai-whisper --break-system-packages")
        elif not has_ytdlp:
            print("  [!] Tier 2 unavailable: yt-dlp not installed")

    if result is None:
        print(f"  [✗] Could not transcribe {video_id} via any method")
        return None

    result['title'] = title
    return result


# ---------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------

def format_as_text(result: dict) -> str:
    """Format transcript as readable plain text with timestamps."""
    lines = []
    lines.append(f"TRANSCRIPT: {result.get('title', result['video_id'])}")
    lines.append(f"Video: https://www.youtube.com/watch?v={result['video_id']}")
    lines.append(f"Method: {result['method']} | Language: {result['language']}")
    lines.append(f"Transcribed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 60)
    lines.append("")

    for seg in result.get('segments', []):
        start = seg.get('start', 0)
        mins = int(start // 60)
        secs = int(start % 60)
        text = seg.get('text', '').strip()
        lines.append(f"[{mins:02d}:{secs:02d}] {text}")

    lines.append("")
    lines.append("=" * 60)
    lines.append(f"FULL TEXT ({len(result['text'])} chars):")
    lines.append("")
    lines.append(result['text'])

    return '\n'.join(lines)


def format_as_json(result: dict) -> str:
    """Format transcript as JSON."""
    output = {
        'title': result.get('title', ''),
        'video_id': result['video_id'],
        'url': f"https://www.youtube.com/watch?v={result['video_id']}",
        'method': result['method'],
        'language': result['language'],
        'transcribed_at': datetime.now().isoformat(),
        'text': result['text'],
        'segments': result.get('segments', []),
        'char_count': len(result['text']),
        'word_count': len(result['text'].split()),
    }
    return json.dumps(output, indent=2, ensure_ascii=False)


def save_transcript(result: dict, output_dir: Path, fmt: str = "text") -> Path:
    """Save transcript to file. Returns the file path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    vid = result['video_id']
    ext = "json" if fmt == "json" else "txt"
    filename = f"transcript-{vid}-{ts}.{ext}"
    out_path = output_dir / filename

    content = format_as_json(result) if fmt == "json" else format_as_text(result)

    with out_path.open("w", encoding="utf-8") as f:
        f.write(content)

    print(f"  [✓] Saved to {out_path}")
    return out_path


# ---------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Two-tier YouTube transcription: captions → Whisper fallback"
    )
    parser.add_argument("url", help="YouTube video URL, video ID, or channel URL")
    parser.add_argument("--force-whisper", action="store_true",
                        help="Skip caption check, go straight to Whisper")
    parser.add_argument("--whisper-model", default="base",
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper model size (default: base)")
    parser.add_argument("--channel", action="store_true",
                        help="Treat URL as a channel/playlist and transcribe multiple videos")
    parser.add_argument("--limit", type=int, default=10,
                        help="Max videos to transcribe from channel (default: 10)")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                        help="Output format (default: text)")
    parser.add_argument("--output-dir", type=str, default=None,
                        help="Output directory (default: outputs/transcripts/)")
    parser.add_argument("--languages", nargs="+", default=["en"],
                        help="Preferred languages for captions (default: en)")
    args = parser.parse_args()

    # Determine output dir
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = Path(__file__).resolve().parent.parent / "outputs" / "transcripts"

    # Check basic deps
    if not check_tier1_deps():
        print("WARNING: youtube-transcript-api not installed. Tier 1 (captions) unavailable.")
        print("         Run: pip install youtube-transcript-api --break-system-packages")

    # Channel mode
    if args.channel or is_channel_url(args.url):
        print(f"[*] Channel mode: fetching up to {args.limit} video IDs...")
        video_ids = get_channel_video_ids(args.url, args.limit)
        print(f"[*] Found {len(video_ids)} videos")
    else:
        video_id = extract_video_id(args.url)
        if not video_id:
            print(f"ERROR: Could not extract video ID from: {args.url}")
            sys.exit(1)
        video_ids = [video_id]

    # Transcribe each video
    results = []
    saved_files = []
    for vid in video_ids:
        result = transcribe_video(
            vid,
            force_whisper=args.force_whisper,
            whisper_model=args.whisper_model,
            languages=args.languages,
        )
        if result:
            results.append(result)
            path = save_transcript(result, output_dir, args.format)
            saved_files.append(str(path))

    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY: {len(results)}/{len(video_ids)} videos transcribed")
    for f in saved_files:
        print(f"  → {f}")
    print(f"{'='*60}")

    # If single video in JSON mode, also print to stdout for piping
    if len(results) == 1 and args.format == "json":
        print("\n--- JSON OUTPUT ---")
        print(format_as_json(results[0]))

    return results


if __name__ == "__main__":
    main()
