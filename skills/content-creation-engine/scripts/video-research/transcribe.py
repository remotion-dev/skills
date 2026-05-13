#!/usr/bin/env python3
"""
transcribe.py — Three-tier transcript fetcher for video-research-engine.

Tier 0: DataForSEO via Composio MCP — $0.004/video, works without youtube.com allowlist
Tier 1: youtube-transcript-api — free, requires youtube.com allowlist
Tier 2: yt-dlp + local Whisper — free, requires youtube.com allowlist + Whisper installed

Tries them in order. First success wins.

Usage from inside Claude (since Composio is an MCP):
    Tier 0 is invoked by Claude itself via the mcp__c7e34fd4-..._COMPOSIO_MULTI_EXECUTE_TOOL.
    This script handles Tier 1 and Tier 2 only when called directly.
    For Tier 0, the calling code (Claude) does the MCP call and passes the result here for normalization.
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path


# -------------------------------------------------------------------
# URL parsing
# -------------------------------------------------------------------

def extract_video_id(url: str) -> str | None:
    """Extract YouTube video ID from various URL formats."""
    patterns = [
        r'(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
        r'(?:shorts/)([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        m = re.search(pattern, url)
        if m:
            return m.group(1)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
        return url
    return None


# -------------------------------------------------------------------
# Tier 0: DataForSEO normalizer
# -------------------------------------------------------------------

def normalize_dataforseo_response(response: dict) -> dict:
    """
    Take a DataForSEO YOUTUBE_VIDEO_SUBTITLES result and convert to our
    standard transcript format.

    Expected input shape (from DATAFORSEO_GET_SERP_YT_VIDEO_SUBTITLES_TASK_ADV_BY_ID):
        response.data.tasks[0].result[0].items = [
            {start_time, end_time, duration_time, text, ...}, ...
        ]

    Returns:
        {
            'method': 'dataforseo',
            'video_id': str,
            'title': str,
            'language': str,
            'segments': [{'t': float_seconds, 'text': str}, ...],
            'plain_text': str,
        }
    """
    try:
        result = response['data']['tasks'][0]['result'][0]
    except (KeyError, IndexError, TypeError) as e:
        raise ValueError(f"Unexpected DataForSEO response shape: {e}")

    items = result.get('items') or []
    segments = [
        {'t': float(it['start_time']), 'text': it['text'].strip()}
        for it in items
        if it.get('text')
    ]
    plain = ' '.join(s['text'] for s in segments)

    return {
        'method': 'dataforseo',
        'video_id': result.get('video_id'),
        'title': result.get('title'),
        'language': result.get('language_code', 'en'),
        'segment_count': len(segments),
        'segments': segments,
        'plain_text': plain,
    }


# -------------------------------------------------------------------
# Tier 1: youtube-transcript-api
# -------------------------------------------------------------------

def transcribe_via_captions(video_id: str, languages: list[str] = None) -> dict | None:
    """Pull transcript via YouTube's caption system. Requires youtube.com network access."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        return None

    if languages is None:
        languages = ['en']

    try:
        ytt = YouTubeTranscriptApi()
        transcript_list = ytt.list(video_id)
        chosen = None
        lang_used = None

        for t in transcript_list:
            t_lang = t.language_code if hasattr(t, 'language_code') else str(t)
            t_is_generated = t.is_generated if hasattr(t, 'is_generated') else False
            if t_lang in languages and not t_is_generated:
                chosen = t
                lang_used = f"{t_lang} (manual)"
                break
        if chosen is None:
            for t in transcript_list:
                t_lang = t.language_code if hasattr(t, 'language_code') else str(t)
                if t_lang in languages:
                    chosen = t
                    t_is_generated = t.is_generated if hasattr(t, 'is_generated') else True
                    lang_used = f"{t_lang} ({'auto-generated' if t_is_generated else 'manual'})"
                    break
        if chosen is None:
            for t in transcript_list:
                chosen = t
                t_lang = t.language_code if hasattr(t, 'language_code') else str(t)
                lang_used = f"{t_lang} (any)"
                break

        if chosen is None:
            return None

        fetched = chosen.fetch()
        segments = [{'t': float(seg.start), 'text': seg.text.strip()} for seg in fetched]
        plain = ' '.join(s['text'] for s in segments)

        return {
            'method': 'captions',
            'video_id': video_id,
            'language': lang_used,
            'segment_count': len(segments),
            'segments': segments,
            'plain_text': plain,
        }
    except Exception as e:
        print(f"  [!] Captions unavailable for {video_id}: {type(e).__name__}: {str(e)[:120]}", file=sys.stderr)
        return None


# -------------------------------------------------------------------
# Tier 2: yt-dlp + Whisper local
# -------------------------------------------------------------------

def transcribe_via_whisper(video_id: str, model_size: str = "base") -> dict | None:
    """Download audio with yt-dlp, transcribe with local Whisper. Requires youtube.com network access."""
    try:
        import yt_dlp
        import whisper
    except ImportError:
        return None

    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        audio_path = Path(tmp) / f"{video_id}.m4a"
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(audio_path.with_suffix('.%(ext)s')),
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
        except Exception as e:
            print(f"  [!] yt-dlp download failed: {e}", file=sys.stderr)
            return None

        # Find the produced audio file
        candidates = list(Path(tmp).glob(f"{video_id}.*"))
        if not candidates:
            return None
        audio_file = candidates[0]

        try:
            model = whisper.load_model(model_size)
            result = model.transcribe(str(audio_file))
            segments = [
                {'t': float(s['start']), 'text': s['text'].strip()}
                for s in result.get('segments', [])
                if s.get('text')
            ]
            plain = ' '.join(s['text'] for s in segments)
            return {
                'method': 'whisper-local',
                'video_id': video_id,
                'language': result.get('language', 'unknown'),
                'segment_count': len(segments),
                'segments': segments,
                'plain_text': plain,
            }
        except Exception as e:
            print(f"  [!] Whisper failed: {e}", file=sys.stderr)
            return None


# -------------------------------------------------------------------
# Format helpers
# -------------------------------------------------------------------

def fmt_ts(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    return f"{m}:{s:02d}"


def to_markdown_lines(transcript: dict) -> list[str]:
    """Render the segments as [MM:SS] lines."""
    return [f"[{fmt_ts(s['t'])}] {s['text']}" for s in transcript.get('segments', [])]


# -------------------------------------------------------------------
# Public entry point
# -------------------------------------------------------------------

def transcribe(video_id: str,
               dataforseo_response: dict | None = None,
               force_whisper: bool = False,
               api_mode: str = "auto") -> dict | None:
    """
    Try transcript tiers in order:
        Tier 0 (DataForSEO) → Tier 1 (youtube-transcript-api) → Tier 2 (Whisper)

    Tier 0 has two backends, controlled by api_mode:
        'composio': Claude pre-calls the Composio MCP and passes the raw
                    response in `dataforseo_response`. Use from inside Cowork.
        'direct':   This script calls api.dataforseo.com directly via Basic Auth.
                    Requires credentials. Use from your local machine.
        'auto':     If `dataforseo_response` provided → use it (Composio path).
                    Else try direct API. Falls through silently if no creds.
    """
    # Tier 0 — Composio (pre-fetched response)
    if dataforseo_response is not None:
        try:
            return normalize_dataforseo_response(dataforseo_response)
        except ValueError:
            pass

    # Tier 0 — Direct API
    if api_mode in ("direct", "auto") and dataforseo_response is None:
        try:
            from dataforseo_direct import transcribe_via_direct_api
            raw = transcribe_via_direct_api(video_id)
            return normalize_dataforseo_response(raw)
        except Exception as e:
            if api_mode == "direct":
                raise
            print(f"  [i] Tier 0 direct skipped: {type(e).__name__}: {str(e)[:120]}", file=sys.stderr)

    # Tier 1
    if not force_whisper:
        result = transcribe_via_captions(video_id)
        if result and result.get('segments'):
            return result

    # Tier 2
    result = transcribe_via_whisper(video_id)
    if result and result.get('segments'):
        return result

    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Three-tier transcript fetcher')
    parser.add_argument('url_or_id', help='YouTube URL or video ID')
    parser.add_argument('--force-whisper', action='store_true')
    parser.add_argument('--dataforseo-response', help='Path to a JSON file containing a DataForSEO response')
    parser.add_argument('--api-mode', choices=['composio', 'direct', 'auto'], default='auto',
                        help='Tier 0 backend: composio (pre-fetched), direct (HTTP API), auto')
    parser.add_argument('--out', default=None, help='Output file path (markdown). Default: stdout.')
    args = parser.parse_args()

    vid = extract_video_id(args.url_or_id)
    if not vid:
        print(f"Could not extract video ID from: {args.url_or_id}", file=sys.stderr)
        sys.exit(1)

    df_resp = None
    if args.dataforseo_response:
        df_resp = json.loads(Path(args.dataforseo_response).read_text())

    result = transcribe(vid, dataforseo_response=df_resp, force_whisper=args.force_whisper, api_mode=args.api_mode)
    if result is None:
        print(f"All tiers failed for {vid}", file=sys.stderr)
        sys.exit(2)

    md = '\n'.join(to_markdown_lines(result))
    if args.out:
        Path(args.out).write_text(f"# Transcript ({result['method']})\n\n{md}\n")
        print(f"Wrote {args.out}")
    else:
        print(md)
