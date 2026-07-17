---
name: video-transcriber
description: "Universal video-to-text transcriber for Graeham's team (Peter, Ellie, John, Adrian). Hand it any video — paste a URL (YouTube, Facebook, Instagram, TikTok, Vimeo, Twitter/X, Reddit, LinkedIn) OR upload/point to a local video file (.mp4, .mov, .m4a, .mp3, .wav) — and get a clean transcript back. Auto-detects whether the input is a URL or a local file, then picks the cheapest working backend: free caption pull first, then local faster-whisper on Graeham's Windows machine for everything else. Trigger on: transcribe, transcript, get the transcript, video to text, captions, subtitles, what does this video say, YouTube/Reel/Short/TikTok transcript, transcribe this file, transcribe this video I uploaded. Also triggers when user just pastes a video URL or uploads a video file with no other context. Pairs with video-watcher (visual analysis) when full A+V breakdown needed."
---

# Video Transcriber

> **One job, one skill.** Hand it a video — by URL or by file — get the transcript back. That's it.

This skill exists because Peter, Ellie, John, and Adrian shouldn't have to remember which Python script lives where or which Apify actor handles which platform. They drop in a URL or a file, and the right thing happens automatically.

## Who uses this and how

**Peter and Ellie** (video editors): use this to pull transcripts of:
- Competitor videos they're studying for shot ideas
- Reference videos Graeham sends them as "make ours like this"
- Long-form interviews where they need to find specific quotes for cuts
- Client testimonial videos that need to be transcribed for captions
- Local screen recordings or Zoom exports sitting in Downloads

**John** (Blog Track): use this to:
- Convert Graeham's recorded YouTube videos into blog-post source material
- Pull transcripts of industry videos and webinars for cite-ready statistics

**Adrian** (Client Care): use this to:
- Transcribe client video messages for record-keeping
- Convert market-update videos into text summaries for clients

**Graeham**: invoke directly when prepping content or reviewing reference material. Frequently uploads webinar or Zoom recordings he's just attended.

## How to invoke

Any of these work:

1. **Just paste the URL**, nothing else:
   ```
   https://www.youtube.com/watch?v=PYMsmSx8Tyw
   ```

2. **Paste the URL with a verb**:
   ```
   transcribe this: https://www.facebook.com/.../videos/123456789
   ```

3. **Upload a local video file** in Cowork or paste a local path:
   ```
   transcribe this video
   [uploaded file: webinar-recording.mp4]
   ```
   ```
   transcribe C:\Users\Graeham Watts\Downloads\zoom-call.mp4
   ```

4. **Multiple inputs at once** (processed in turn — URLs and files can be mixed):
   ```
   transcribe all three:
   https://www.youtube.com/watch?v=AAA
   C:\path\to\local.mp4
   https://www.instagram.com/reel/BBB/
   ```

The skill auto-detects URL vs local path and routes to the right backend.

## Decision tree — when to use which path

```
INPUT
│
├── Local file path (or uploaded file) ──────────────→ PATH B (Windows local faster-whisper)
│
└── URL
    ├── YouTube or other platform with captions
    │   └── Try PATH A (caption pull) first
    │       ├── Captions exist → return transcript ✓
    │       └── No captions → fall through to PATH B
    │
    └── Any other URL (Instagram, TikTok, Facebook, etc.)
        └── PATH B (Windows downloads via yt-dlp, then faster-whisper)
```

## PATH A — Caption pull (free, instant, ~1–3 sec)

Runs in the Cowork sandbox. Works for any URL where the platform exposes captions (almost all YouTube videos, some Vimeo, some others).

```bash
python3 scripts/transcribe.py "<URL>" --prefer-captions
```

Returns in ~1–3 seconds. Costs $0. This is always the first try for URL inputs.

## PATH B — Windows local faster-whisper (free, ~5–15 min for an hour-long video)

This is the workhorse for everything caption pull can't handle, and the only path for local files.

**Why local Windows, not sandbox:** The Cowork sandbox only has ~1.4 GB free disk. Installing openai-whisper or even faster-whisper requires multiple GB of dependencies (PyTorch, CUDA libs). We tried — it doesn't fit. Graeham's Windows machine has faster-whisper installed locally and ffmpeg available, so all real transcription work runs there.

### How Claude drives PATH B

Claude writes the right command for the situation, then asks the user to paste it into PowerShell. We can't drive the terminal directly because Windows Terminal is granted at tier "click" (visible + clickable, but typing is blocked by security policy).

The script is at `scripts/transcribe_windows.py` and takes either a file path or a URL as its single argument:

```powershell
python "<path-to>\scripts\transcribe_windows.py" "C:\path\to\video.mp4"
python "<path-to>\scripts\transcribe_windows.py" "https://www.youtube.com/watch?v=..."
python "<path-to>\scripts\transcribe_windows.py" "C:\path\to\video.mp4" --model small.en --timestamps
```

The script:
- Detects URL vs local file
- For URLs: downloads audio via yt-dlp first (locally, fast)
- Loads faster-whisper with int8 quantization (CPU)
- Streams progress every ~20 segments so the user knows it's working
- Writes `{slug}_transcript.txt` and (if `--timestamps`) `{slug}_transcript_timestamped.txt` next to the source video (or to `--output-dir` if specified)

### Model size guidance

| Model | Speed (1hr audio, CPU) | Best for |
|---|---|---|
| `base.en` (default) | ~5–15 min | Default — fast, good enough for most speech |
| `small.en` | ~15–30 min | Better proper-noun accuracy; webinars with jargon |
| `medium.en` | ~30–60 min | Reference-quality; client testimonials going to print |

Tell the user the tradeoff if accuracy matters more than time. Don't silently bump the model — they're waiting on the result.

## Output format

By default, returns clean prose:

```
Transcript: webinar-recording.mp4
Duration: 1:08:26
Language: en
Model: faster-whisper base.en (int8)
======================================================================

The spring housing market was supposed to be the big comeback season for 2026. Instead, a lot of markets are slowing down fast. Earlier this year, most people expected mortgage rates to ease...
```

If the user asks for timestamps:

```
[0:00:00] The spring housing market was supposed to be the big comeback
[0:00:08] Instead, a lot of markets are slowing down fast.
[0:00:13] Earlier this year, most people expected mortgage rates to ease
...
```

## Optional flags the user can request (spoken-language)

- **"with timestamps"** — include `[MM:SS]` markers per segment
- **"better accuracy"** / **"use a bigger model"** → bump to `small.en` or `medium.en`
- **"summarize after"** — after producing the transcript, Claude generates a 3-bullet summary
- **"save to my Documents"** / **"save next to the video"** — choose output location

## Workflow integration

This skill is standalone. It does not require any other skill to function.

Common follow-ons the user may request after a transcript:

- **"and turn it into a blog post"** → hand transcript to `content-creation-engine`
- **"and find the best 30-second clip"** → scan for the highest-impact segment for a Short/Reel cutdown
- **"and pull cite-ready stats"** → scan for date-anchored numerical claims for AEO blog content
- **"and watch it too"** → fire `video-watcher` in parallel for full A+V breakdown

## Failure handling

| Failure | What the skill does |
|---|---|
| Local file path doesn't exist | Report the bad path. Ask if they meant a different file or want to re-upload. |
| URL not recognized by yt-dlp | Report the platform name. Ask Graeham to confirm an alternate path (manual download, Apify actor). |
| Video is private or restricted | Report the access error verbatim. Suggest verifying the URL is publicly viewable. |
| `pip install faster-whisper` fails on user's machine | Most common cause: very new Python version (3.14+) without wheels yet. Tell user to try `pip install faster-whisper --pre` or fall back to Python 3.12 in a venv. |
| Path contains `\U` or `\N` in a non-raw Python string | This actually happened. Always wrap Windows paths in raw strings (`r"..."`) or use forward slashes. Never put Windows paths in a docstring without escaping. |
| Video is very long (>60 min) | Tell the user the est. transcription time before kicking off, so they don't think it's stuck. |
| User has Python but no `faster-whisper` | Walk them through `pip install faster-whisper` first, then `python scripts/transcribe_windows.py ...` |

## Setup requirements

**On the user's Windows machine (one-time):**

```powershell
pip install faster-whisper
```

ffmpeg must be on PATH. Graeham's lives at `C:\Users\Graeham Watts\Documents\Skills LLMS\Claude\ffmpegvideoprocessingengine\bin\` — the script adds this to PATH automatically.

**No API keys required.** Everything runs locally and free.

**Optional**: `OPENAI_API_KEY` if you want to use the OpenAI Whisper API (~10x faster, ~$0.006/min). Not currently wired into the Windows script — would need to be added if Graeham wants that path for super long videos.

## Future agentic enhancement: watch-folder workflow

The Windows script can be run from a "drop folder" pattern for fully hands-off transcription:

1. Create `C:\Users\Graeham Watts\Documents\Transcribe-Inbox\`
2. Create `C:\Users\Graeham Watts\Documents\Transcribe-Done\`
3. PowerShell script (saved separately, not in this skill) polls inbox every 60 sec, transcribes anything new, moves source to Done folder and transcript next to it.
4. Wire to Windows Task Scheduler to start on login.

This is NOT part of this skill yet — it's a separate setup. If Graeham asks for "drop folder transcription" or "agentic transcription," build that as a separate task.

## Example: end-to-end run (PATH B, local file)

**User uploads:** `webinar-recording.mp4` (68 min, 2.6 GB)

**Skill flow:**
1. Detects local file path, no URL
2. Skips PATH A entirely (no captions on a local file)
3. Claude writes the transcribe command for the user to paste:
   ```powershell
   python "C:\Users\Graeham Watts\Documents\Skills LLMS\Claude\Skills\skills\video-transcriber\scripts\transcribe_windows.py" "C:\Users\...\webinar-recording.mp4"
   ```
4. User pastes it, faster-whisper runs (~5–15 min)
5. Two text files appear next to the video: plain + timestamped (if requested)
6. Claude reads them, summarizes findings, suggests follow-ons

Total: ~10 minutes of compute, ~30 seconds of user time, $0.

## Companion skill: video-watcher

This skill captures **what was SAID** in a video. Its companion `video-watcher` captures **what was SHOWN** (frame-by-frame AI vision analysis — shot list, on-screen text catalog, production style fingerprint, Replicate-This Brief).

They're standalone but compose naturally:

- **"transcribe this video: [URL or file]"** → only video-transcriber fires (cheap, fast, words only)
- **"watch this video: [URL or file]"** → only video-watcher fires (vision analysis, costs API tokens)
- **"watch and transcribe"** / **"full breakdown of"** / **"make ours like this"** → BOTH fire in parallel and outputs are interleaved (audio transcript lines + visual shot-list notes, both timestamped)

When in doubt about which the user wants: default to this skill (cheaper, more common need). If they want visual analysis specifically, they'll say "watch" or "shot list" or "make ours like this."

## Why this exists

Before this skill, transcription required: knowing which Python script lived where, knowing which platform was supported by which backend, knowing whether the sandbox had Whisper (it doesn't — disk too small), and stitching the output together manually. That's friction nobody on the team should have to navigate.

This skill makes transcription a single move: drop a URL or a file, get a transcript. Done.

## Maintenance

- **yt-dlp updates**: When a platform's extractor breaks, `pip install -U yt-dlp` usually fixes it. The script can auto-run this when extractor failures are detected.
- **faster-whisper updates**: `pip install -U faster-whisper`. New model versions sometimes ship — re-download is automatic on first use of a new model name.
- **Python version drift**: Python 3.14 is fine but very new — some wheels lag. If `pip install faster-whisper` fails on a newer Python, fall back to a 3.12 venv.
- **Model storage**: Whisper models cache to `~/.cache/huggingface/hub/`. Each model is ~140–500 MB. Safe to delete if disk gets tight, will re-download on next use.
