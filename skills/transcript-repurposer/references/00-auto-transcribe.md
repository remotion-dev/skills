# Phase 0 — Auto-Transcribe from URL

This is the fully agentic path. User hands over a URL → I get the transcript without them lifting a finger.

## The shared transcription module

This skill does NOT have its own transcription logic. It calls the shared module at:

```
<Skills root>/skills/_shared/transcription/transcribe.py
```

In the bash sandbox, that path resolves to:

```
/sessions/*/mnt/Skills/skills/_shared/transcription/transcribe.py
```

The module handles yt-dlp installation, Whisper installation, Deepgram fallback, and result caching. Don't reinvent any of that here.

## Deciding the tier

| User signal | Tier to use |
|---|---|
| User pastes URL with no quality flag | Default (Whisper) |
| User says "premium quality", "high quality", "best transcription", "use Deepgram" | Premium |
| Video duration > 15 min (detected via yt-dlp metadata first) | Recommend premium, but ask the user before spending API credit |
| User says "free" / "no cost" | Default (Whisper), even if video is long |

For videos over 15 min, pull duration via `yt-dlp --dump-json` first (the module does this internally). If duration > 15 min and user didn't explicitly say "free," ask:

> "This video is <X> minutes long. Whisper local would take ~<estimate> min and be ~95% accurate. Deepgram premium would take ~<estimate> sec and cost ~$<amount>, with 98%+ accuracy. Which do you want?"

Default to recommending premium when over 30 min — at that point the time saved is worth more than the few dollars.

## Invocation

### Default tier (Whisper local)

```bash
python3 /sessions/*/mnt/Skills/skills/_shared/transcription/transcribe.py \
  --url "<video_url>" \
  --json
```

### Premium tier (Deepgram)

First load the Deepgram key. It lives next to the GitHub PAT:

```bash
DEEPGRAM_KEY=$(head -n 1 /sessions/*/mnt/outputs/.claude-credentials/deepgram-key.txt 2>/dev/null | tr -d '[:space:]')
if [ -z "$DEEPGRAM_KEY" ]; then
  echo "DEEPGRAM_KEY_NOT_SET"
fi
```

If `DEEPGRAM_KEY_NOT_SET`, tell the user:

> "Premium tier needs a Deepgram API key. Sign up at deepgram.com (you get $200 free trial credit on signup — covers ~45,000 minutes). Once you have it, I'll save it for future sessions. Or we can run the default Whisper tier now."

If the key is present:

```bash
DEEPGRAM_API_KEY="$DEEPGRAM_KEY" \
python3 /sessions/*/mnt/Skills/skills/_shared/transcription/transcribe.py \
  --url "<video_url>" \
  --premium \
  --json
```

## Reading the result

The module returns JSON to stdout. Parse it and extract:

```python
import json, subprocess
result = json.loads(subprocess.check_output([
  "python3", "/sessions/*/mnt/Skills/skills/_shared/transcription/transcribe.py",
  "--url", url, "--json"
]).decode())

source_text = result["transcript"]
platform = result["source_platform"]
duration = result["duration_sec"]
title = result["title"]
tier_used = result["tier"]
cached = result["cached"]
errors = result["errors"]
```

If `errors` is non-empty, the script may have:
- Failed to download (yt-dlp error — URL private, blocked, or extraction broken)
- Failed Whisper install (rare, sandbox issue)
- Failed Deepgram call (API key invalid or rate limited — script falls back to Whisper automatically and logs the warning in errors but still produces a transcript)

If `transcript` is empty AND errors is populated, fail clean — tell the user what went wrong and offer the manual paste path.

## Handling each platform

### YouTube (videos, Shorts, live VODs)

- Works reliably with yt-dlp
- Captions exist for most videos — you can use yt-dlp's `--write-auto-sub` to grab them in 5 seconds instead of audio-transcribing the whole video. This is an optimization the module doesn't yet implement; for now it always re-transcribes from audio for consistency
- Live streams: only works after the stream ends and the recording is available

### Instagram (Reels, posts, IGTV)

- yt-dlp works for **public** posts. Private accounts will fail with "Unsupported URL" or "Login required"
- Instagram rate-limits aggressively. If you hit a rate limit, the error will say "HTTP Error 429"
- For production-scale Instagram (Property OS team workflows), recommend Apify's Instagram Reel Scraper actor instead — more reliable, ~$0.50 per 1000 reels

### TikTok

- Works reliably with yt-dlp
- No watermark by default (audio extraction strips it)

### Twitter / X

- Works for public video tweets
- Some tweets require auth (especially Spaces); those fail cleanly

### Vimeo

- Works for public videos
- Password-protected videos require `--video-password` flag — module doesn't yet support that; ask user to remove password temporarily

### Facebook

- Works for public videos and pages
- Private posts: same story as Instagram

### Podcast hosts (Spotify, Apple Podcasts, Anchor, Buzzsprout, etc.)

- Works for direct audio URLs
- Spotify-hosted exclusives may block extraction — flag to user if extraction fails

## Output format for Phase 0

After the transcription succeeds, package the result for Phase 2's source brief:

```
## Phase 0 Result

Source URL: <url>
Platform: <platform>
Title: <video title from platform>
Uploader: <creator handle>
Duration: <seconds> seconds (~<minutes>:<seconds>)
Tier used: <whisper | deepgram>
Cached: <yes | no>
Transcription time: <seconds>

Transcript (passes to Phase 1 for normalization, then Phase 2):
<full transcript text>
```

Then proceed to Phase 1 (Ingest) — it will still clean any Whisper transcription artifacts.

## Speed expectations to communicate to the user

| Source length | Whisper local | Deepgram premium |
|---|---|---|
| 30-60 sec reel | 30-90 sec | ~5 sec |
| 5 min TikTok / Short | 1-3 min | ~10 sec |
| 15 min YouTube | 5-10 min | ~20 sec, $0.07 |
| 30 min podcast | 10-15 min | ~30 sec, $0.13 |
| 90 min interview | 30-45 min | ~60 sec, $0.39 |
| 3 hr long-form podcast | Too slow — escalate to Deepgram | ~2 min, $0.78 |

If a job will take more than 10 min on Whisper, tell the user upfront so they can decide if Deepgram is worth it.

## Caching behavior

Every successful transcription is cached at `~/.cache/graeham-transcripts/<hash>.json` keyed by (URL + tier). Re-running the same URL returns instantly. The cache survives across sandbox sessions because `~/.cache` is in the sandbox home directory.

If user says "re-transcribe this" or "do it fresh," they want to bypass cache. The module doesn't currently expose a `--no-cache` flag, so easiest workaround is to delete the cached file:

```bash
# Find and remove the specific cache entry
URL_HASH=$(echo -n "<url>|whisper" | sha256sum | cut -c1-16)
rm -f ~/.cache/graeham-transcripts/${URL_HASH}.json
```

This is a minor edge case — most of the time you want to use the cache.

## When NOT to use Phase 0

- User explicitly says "here's the transcript" and provides text → skip Phase 0, go to Phase 1
- User uploads a `.srt`, `.vtt`, or `.txt` file → skip Phase 0, go to Phase 1
- URL is to a non-video resource (article, image) → Phase 0 won't help; this skill can't repurpose non-video sources
