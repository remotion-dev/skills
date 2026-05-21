# Shared Transcription Module

Single source of truth for video → text across all of Graeham's skills.

## Why this exists

Before this module: `content-creation-engine` had its own YouTube transcriber, the new `transcript-repurposer` was about to grow its own, and Property OS was on track to grow a third. Three different transcribers means three different sets of bugs, three different output formats, three different failure modes.

This module is the one place where transcription happens. Any skill that needs a transcript calls `transcribe.py` and gets back a consistent JSON result.

## Two tiers

| Tier | Engine | Cost | Speed | Accuracy | Trigger |
|---|---|---|---|---|---|
| Default | yt-dlp + OpenAI Whisper (local in sandbox) | Free | 30s-5min depending on length | ~95% | Default — no flag needed |
| Premium | yt-dlp + Deepgram Nova-3 API | $0.0043/min | ~real-time for short, ~10x for long | 98%+ | `--premium` flag + `DEEPGRAM_API_KEY` env var |

## Usage

From any skill (or the command line):

```bash
# Default: Whisper local, free
python3 transcribe.py --url "https://www.instagram.com/reel/..."

# Premium: Deepgram, higher accuracy
DEEPGRAM_API_KEY=your_key python3 transcribe.py --url "..." --premium

# Local audio file
python3 transcribe.py --file /path/to/podcast.mp3

# Get the full JSON result (default outputs transcript text only)
python3 transcribe.py --url "..." --json

# Write to a file
python3 transcribe.py --url "..." --output transcript.txt
```

## Caching

Every successful transcription is cached under `~/.cache/graeham-transcripts/<hash>.json`. Same URL + tier = same cache key. Re-running on a cached URL returns instantly.

Cache key hashes the source + tier — so the same URL transcribed via Whisper vs Deepgram are stored separately. Useful when you want to compare quality or upgrade a previous Whisper transcript to Deepgram.

## Supported sources

Anything yt-dlp supports — that's 1,000+ sites including:

- YouTube (videos, Shorts, live streams)
- Instagram (Reels, posts, IGTV)
- TikTok
- Twitter / X video posts
- Facebook video
- Vimeo
- Twitch VODs
- Most podcast hosting platforms
- Direct .mp3 / .mp4 / .m4a file URLs

For full list: `yt-dlp --list-extractors`.

## Output JSON shape

```json
{
  "transcript": "Clean spoken text...",
  "source_url": "https://...",
  "source_platform": "youtube|instagram|tiktok|x|vimeo|facebook|unknown",
  "title": "<video title from platform>",
  "uploader": "<creator handle>",
  "duration_sec": 47,
  "word_count": 142,
  "tier": "whisper|deepgram",
  "transcribe_seconds": 84.3,
  "cached": false,
  "cache_path": "/home/user/.cache/graeham-transcripts/a1b2c3d4.json",
  "errors": []
}
```

## When Deepgram falls back to Whisper

If you pass `--premium` but no `DEEPGRAM_API_KEY` is set, the module logs a warning to the `errors` array and falls back to Whisper. It does NOT fail silently. Check `tier` in the result to know which engine actually ran.

## Whisper model sizes

Default is `base` (~150MB, ~92% accuracy, balanced). Override with `--whisper-model`:

| Model | Size | Accuracy | Speed (CPU sandbox) | When to use |
|---|---|---|---|---|
| `tiny` | 75MB | ~85% | Fastest | Throwaway drafts, very short clips |
| `base` | 150MB | ~92% | Balanced | **Default** — most cases |
| `small` | 500MB | ~95% | Slow | Higher accuracy needed but no Deepgram key |
| `medium` | 1.5GB | ~97% | Very slow | Rare — usually better to just use Deepgram |

The `large` and `large-v3` models exist but are ~3GB and too slow on sandbox CPU. Use Deepgram for that tier.

## Integration points

| Skill | How it uses this module |
|---|---|
| `transcript-repurposer` | Phase 0 — auto-transcribes any URL the user provides, then runs Phases 1-8 |
| `content-creation-engine` | Phase 0 source ingestion — replace its existing `youtube_transcriber.py` with calls here |
| Future: Property OS backend | Server-side worker calls the same Python module (or its logic ported to Node) |

## Setting up Deepgram

1. Sign up at https://deepgram.com (currently $200 free trial credit on signup — ~45,000 minutes of transcription at the Nova-3 rate)
2. Create an API key in the Deepgram dashboard
3. Store the key persistently. Two options:

   a) **Per-session in bash:** `export DEEPGRAM_API_KEY=...` before running the script
   b) **Persisted alongside the GitHub PAT:** save it to `outputs/.claude-credentials/deepgram-key.txt` and update each skill that calls this module to source it from there

Recommend option (b) so it works across sessions.

## What this module does NOT do

- **It does not push transcripts anywhere.** Skills that call this module are responsible for storing/displaying the result.
- **It does not handle Instagram authentication.** Instagram fights yt-dlp regularly. Public Reels work; private accounts don't. For production Property OS, use Apify's Instagram scrapers instead — they cost more but are stable.
- **It does not transcribe live streams in real-time.** It downloads the recorded stream after it ends.
- **It does not do speaker diarization.** All speech comes back as one continuous transcript. If you need "who said what," use AssemblyAI instead of Deepgram.

## Updating

This module is the canonical location. To change transcription behavior anywhere in Graeham's ecosystem, edit `transcribe.py` here. All skills that depend on it get the update automatically the next time they run.
