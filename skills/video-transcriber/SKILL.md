---
name: video-transcriber
description: "Universal video transcription skill for Graeham Watts's team. Paste any video URL — YouTube, Facebook, Instagram, TikTok, Vimeo, Twitter/X, Reddit, LinkedIn, or a direct video file URL — and the skill returns a clean transcript. Use this skill ANY time the user or one of Graeham's assistants (Peter, Ellie, John, Adrian) mentions: transcribe, transcript, transcription, get the transcript, pull the transcript, video to text, audio to text, caption, captions, subtitle, subtitles, what does this video say, what's said in this video, video text extraction, YouTube transcript, Facebook video transcript, Instagram Reel transcript, TikTok transcript, Reels transcript, Shorts transcript. Also trigger when the user simply pastes a video URL with no other context (e.g., 'https://youtube.com/watch?v=…' on its own line, 'https://facebook.com/…/videos/…', 'https://instagram.com/reel/…', 'https://tiktok.com/@…/video/…') and the action is implied. The skill auto-detects the platform, picks the cheapest working backend (free caption pull first, paid Whisper fallback if needed), and returns the transcript as clean prose with optional timestamps. Built for fast-turnaround video editing reference: pulling quotes for shot lists, sourcing B-roll inspiration from competitor videos, transcribing client interviews, or feeding scripts into the content-creation-engine."
---

# Video Transcriber

> **One job, one skill.** Paste a video URL. Get the transcript back. That's it.

This skill exists because Peter, Ellie, John, and Adrian shouldn't have to remember which Python script lives where or which Apify actor handles which platform. They paste a URL, and the right thing happens automatically.

## Who uses this and how

**Peter and Ellie** (video editors): use this to pull transcripts of:
- Competitor videos they're studying for shot ideas
- Reference videos Graeham sends them as "make ours like this"
- Long-form interviews where they need to find specific quotes for cuts
- Client testimonial videos that need to be transcribed for captions

**John** (Blog Track): use this to:
- Convert Graeham's recorded YouTube videos into blog-post source material
- Pull transcripts of industry videos for cite-ready statistics

**Adrian** (Client Care): use this to:
- Transcribe client video messages for record-keeping
- Convert market-update videos into text summaries for clients

**Graeham**: invoke directly when prepping content or reviewing reference material.

## How to invoke

The simplest possible UX. Any of these work:

1. **Just paste the URL**, with nothing else:
   ```
   https://www.youtube.com/watch?v=PYMsmSx8Tyw
   ```

2. **Paste the URL with a verb**:
   ```
   transcribe this: https://www.facebook.com/.../videos/123456789
   ```

3. **Multiple URLs at once** (skill processes each in turn):
   ```
   transcribe all three:
   https://www.youtube.com/watch?v=AAA
   https://www.instagram.com/reel/BBB/
   https://www.tiktok.com/@user/video/CCC
   ```

The skill auto-detects the platform from the URL and routes to the right backend. The user doesn't need to specify the platform or backend.

## Supported platforms

The primary engine is **yt-dlp**, which natively supports 1,800+ video platforms. The most relevant for Graeham's team:

| Platform | URL pattern | Best path |
|---|---|---|
| YouTube (standard, Shorts, live) | `youtube.com/watch?v=…`, `youtu.be/…`, `youtube.com/shorts/…` | Caption API first (free, instant), then yt-dlp + Whisper if no captions |
| Facebook video | `facebook.com/…/videos/…`, `fb.watch/…` | yt-dlp + Whisper |
| Instagram (Reels, posts, IGTV) | `instagram.com/reel/…`, `instagram.com/p/…`, `instagram.com/tv/…` | yt-dlp + Whisper |
| TikTok | `tiktok.com/@…/video/…`, `vm.tiktok.com/…` | yt-dlp + Whisper |
| Vimeo | `vimeo.com/…` | Caption API first, then yt-dlp + Whisper |
| Twitter / X video | `twitter.com/…/status/…`, `x.com/…/status/…` | yt-dlp + Whisper |
| LinkedIn video | `linkedin.com/posts/…`, `linkedin.com/feed/update/…` | yt-dlp + Whisper |
| Reddit video | `reddit.com/r/…/comments/…` | yt-dlp + Whisper |
| Direct file URL | `…/video.mp4`, `…/audio.m4a` | ffmpeg + Whisper directly |

If the URL is from an unlisted platform, the skill still tries yt-dlp (often works). If yt-dlp doesn't support it, the skill reports back with the platform name and asks Graeham to confirm an alternate path.

## The two-tier transcription path

### Tier 1: Caption pull (free, instant)

Always try this first. Works for any platform that has captions available (almost all YouTube, some Vimeo, some others).

```bash
python3 scripts/transcribe.py "<URL>" --prefer-captions
```

Returns in ~1-3 seconds. Costs $0.

### Tier 2: yt-dlp + Whisper (free, ~30 sec – 3 min depending on video length)

Used when Tier 1 returns no captions (most Facebook, Instagram, TikTok, and YouTube videos without auto-captions).

The script downloads the audio via yt-dlp, then transcribes locally with OpenAI Whisper (open source, runs on the Cowork sandbox CPU). Costs $0.

```bash
python3 scripts/transcribe.py "<URL>"
```

If Whisper isn't installed on the sandbox, the skill auto-installs it on first run (`pip install yt-dlp openai-whisper --break-system-packages`). Subsequent runs are immediate.

For very long videos (>30 min), the skill may prompt to confirm before transcribing — Whisper takes longer on long audio.

## Output format

By default, the skill returns clean prose:

```
Title: "Spring Housing Market 2026 Is Slowing Down Fast"
Platform: YouTube
Duration: 1:24
Language: English (auto-detected)

The spring housing market was supposed to be the big comeback season for 2026. Instead, a lot of markets are slowing down fast. Earlier this year, most people expected mortgage rates to ease and buyers to jump back in. Instead, rates moved higher again, consumer confidence weakened, and affordability got even tighter...
```

If the user asks for timestamps, the skill formats it as:

```
[00:00] The spring housing market was supposed to be the big comeback season for 2026.
[00:08] Instead, a lot of markets are slowing down fast.
[00:13] Earlier this year, most people expected mortgage rates to ease and buyers to jump back in.
...
```

If the user asks for JSON output, the skill returns:

```json
{
  "url": "https://www.youtube.com/watch?v=PYMsmSx8Tyw",
  "platform": "youtube",
  "title": "Spring Housing Market 2026 Is Slowing Down Fast",
  "duration_sec": 84,
  "language": "en",
  "transcription_method": "caption_pull",
  "transcript_plain": "The spring housing market...",
  "segments": [
    { "start": 0.0, "end": 8.2, "text": "The spring housing market..." },
    ...
  ]
}
```

## Optional flags the user can request

These are spoken-language flags, not command-line. The user just mentions what they want.

- **"with timestamps"** — include `[MM:SS]` markers per segment
- **"as JSON"** — structured output with segments array
- **"first 5 minutes only"** — only transcribe up to a time mark
- **"save to file"** — write to `outputs/transcripts/transcript-{platform}-{video_id}-{timestamp}.txt`
- **"summarize after"** — after producing the transcript, also generate a 3-bullet summary

## Workflow integration (optional)

This skill is **standalone**. It does not require the content-creation-engine, listing-remarks-writer, or any other skill to function. Paste a URL, get a transcript, done.

If the user wants the transcript fed into another workflow:

- **"and use it as the source for a blog post"** → after transcribing, hand the transcript off to `content-creation-engine`'s blog-generation flow
- **"and find the best 30-second clip"** → after transcribing, identify the highest-engagement segment for a Short/Reel cutdown (manual judgment — Claude scans and picks)
- **"and pull cite-ready stats"** → after transcribing, scan for date-anchored numerical claims for AEO blog content

These are optional follow-ons. The default behavior is: transcribe, return, done.

## Failure handling

| Failure | What the skill does |
|---|---|
| URL not recognized by yt-dlp | Reports the platform and asks user to confirm an alternate path (manual download, Apify actor, browser scrape) |
| Video is private or restricted | Reports the access error verbatim. Suggests user verify the URL is publicly viewable |
| Audio download fails (network) | Retries once with 5-second backoff. Reports if still failing |
| Whisper fails to install | Falls back to OpenAI Whisper API if `OPENAI_API_KEY` is set ($0.006/min). Otherwise reports the install error to the user |
| Caption pull returns no captions | Falls through to Tier 2 automatically (no user action needed) |
| Video is very long (>60 min) | Confirms with user before starting Whisper transcription (it'll take 5-10 min on long videos) |

## Setup requirements

The Cowork sandbox auto-installs these on first run:

```bash
pip install yt-dlp openai-whisper youtube-transcript-api --break-system-packages
apt install -y ffmpeg  # may already be installed
```

No API keys required for the default free path. **Optional** keys for faster/extended paths:

- `OPENAI_API_KEY` — if set, the skill uses OpenAI Whisper API instead of local Whisper. ~10x faster for long videos. Costs $0.006/min audio.
- `APIFY_API_TOKEN` — if set, the skill uses Apify actors as a fallback when yt-dlp fails on niche platforms.

Neither is required for the default workflow. YouTube + Facebook + Instagram + TikTok + Vimeo all work with the free local stack.

## Example: end-to-end run

**User pastes:**
```
https://www.instagram.com/reel/DXPuASugkgy/
```

**Skill flow:**
1. Detects platform: Instagram Reel
2. Tries caption pull → no captions on IG Reels → falls through to Tier 2
3. Runs `yt-dlp -x --audio-format mp3 -o /tmp/audio.mp3 <URL>` → downloads ~3 MB audio in 5 seconds
4. Runs Whisper on the audio → transcript in ~20 seconds (for a 30-second Reel)
5. Returns clean prose transcript to the user

Total: ~30 seconds, $0.

## Why this exists

Before this skill, transcription required: knowing which Python script (`youtube_transcriber.py` vs `transcribe.py` vs `run_reddit_ideation.py`), knowing which platform was supported by which script, knowing whether the sandbox had Whisper installed, and stitching the output together manually. That's friction the team shouldn't have to navigate.

This skill makes transcription a one-liner. Paste a URL. Get a transcript. Done.

## Maintenance

When yt-dlp's platform list expands, this skill's coverage expands automatically — no code change needed. When new transcription engines come out (e.g., faster open-source Whisper variants), update the Tier 2 backend in `scripts/transcribe.py` and the skill keeps working with no SKILL.md change required.

If a previously-working platform stops working: yt-dlp usually fixes it within a few days via `pip install -U yt-dlp`. The skill auto-runs this update if yt-dlp returns a "site supported but extractor broken" error.
