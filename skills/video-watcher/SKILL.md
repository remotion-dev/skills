---
name: video-watcher
description: "AI video analysis skill for Graeham Watts's team. Paste any video URL and the system WATCHES the video frame-by-frame using vision AI, returning a structured blueprint — shot list, on-screen text catalog, production style fingerprint, and a Replicate-This Brief for recreating it with HeyGen + Higgsfield + Remotion. Pairs with video-transcriber for complete A+V understanding. Use this skill ANY time the user mentions: watch this video, analyze this video, video analysis, visual analysis, shot list, shot breakdown, scene breakdown, video blueprint, recreate this video, make ours like this, how is this video made, B-roll catalog, B-roll breakdown, on-screen text, text overlays in video, video production style, video editing style, cut analysis, pacing analysis, frame-by-frame analysis, reference video, competitor video. Also trigger when the user pastes a video URL and asks for a breakdown or description. Distinct from video-transcriber: transcriber extracts WORDS only; video-watcher extracts VISUAL structure."
---

# Video Watcher

> **One job:** Watch any video with AI vision. Output a literal blueprint of how to recreate it.

This skill exists because the transcript of a video only tells you what was *said* — it tells you nothing about what was *shown*. For Peter and Ellie editing video content, the visual structure matters as much as the script. video-watcher closes that gap.

## The two-skill split (read this first)

This skill pairs with `video-transcriber`. They're standalone but compose naturally:

| Skill | What it captures |
|---|---|
| **video-transcriber** | What was SAID — every word, timestamped |
| **video-watcher** | What was SHOWN — every visual beat, timestamped |

Use video-transcriber alone when you only need the words (pulling quotes for cuts, blog source material). Use video-watcher alone when you only need the visual blueprint (replicating a reference video's style). Use BOTH together when you need complete understanding of a video to recreate it end-to-end.

The user can invoke both at once by saying something like:
> "Watch and transcribe this video: [URL]"
or
> "Full breakdown of this video: [URL]"

In which case both skills fire in parallel and the output is interleaved.

## Who uses this

**Peter and Ellie** (video editors): use this when Graeham sends them a reference video saying "make ours like this." The skill returns a shot list with exact timestamps telling them what shot type to use when, where text overlays go, what B-roll to pull, what color grade to match, and what pacing to hit.

**Graeham**: use this to study any reference video personally — competitor analysis, "this viral Reel got 2M views, why" investigations, evaluating whether to commission a specific style for a new campaign.

**John** (Blog Track): use this to extract the visual structure of a video for blog posts that include "here's how this video is made" content.

**content-creation-engine**: uses this internally during Phase 0 Mode B (visual analysis pass) when generating new content from a reference video source. The engine no longer owns this code — it calls this skill as an external dependency.

## How to invoke

The simplest possible UX. Any of these work:

1. **Paste URL + watch verb**:
   ```
   watch this: https://www.youtube.com/watch?v=PYMsmSx8Tyw
   ```
2. **Reference replication phrase**:
   ```
   make ours like this: https://www.instagram.com/reel/DXPuASugkgy/
   ```
3. **Full breakdown request**:
   ```
   full breakdown of https://www.tiktok.com/@user/video/ABC
   ```
4. **Combined with transcriber**:
   ```
   watch AND transcribe: https://www.youtube.com/watch?v=...
   ```

The skill auto-detects the platform from the URL (yt-dlp supports 1,800+ sites) and routes through the right backend.

## What you get back

A structured markdown document with these sections:

```
TLDR
   3-4 sentences synthesizing the whole video. What it's
   trying to accomplish, who it's for, what it does well.

Hooks (0:00 - 0:10)
   The opening 10 seconds analyzed in detail because that's
   where scroll-stoppers live. Visual + audio + analysis.

Per-Scene Notes
   For each scene change (typically 8-80 frames per video):
     [Timestamp]
     On-screen text: exact transcription of any text overlay
     Visual: 1-2 sentences describing what's on screen
     Said: 1-line quote/paraphrase of the spoken line
     Synthesis: 1-2 sentences on why this beat matters

Key Concepts
   Bulleted list with timestamps. The 3-5 ideas the video
   communicates most clearly.

B-Roll Catalog
   Table of shot types with timestamps and rough %.
   Example: drone aerials 12%, talking head 60%, screen
   recording 8%, text-overlay-on-photo 20%.

On-Screen Text Catalog
   Table of every visible text overlay with timestamp,
   exact text, and styling notes (color, font feel, size).

Production Style Fingerprint
   Color grade, typography, motion graphics style, framing,
   any visible brand signals. What makes this video LOOK
   the way it does.

Code & Commands
   If any code, terminal output, or technical commands
   appear on screen, transcribed as fenced code blocks.

Replicate-This Brief        ← the killer output
   What you'd tell HeyGen + Higgsfield + Remotion + CapCut
   to recreate this video's structure. Concrete instructions.
   Example:
     - HeyGen avatar with warm desk look (Vaibhav template #3)
     - Higgsfield drone aerial of Palo Alto / Menlo Park
     - 3 Remotion stat-callout overlays at 0:08, 0:25, 0:42
     - Color grade: warm/teal split
     - Cut pacing: 8 cuts in 90 seconds

Open Questions
   Anything visible in the video that the analyzer couldn't
   fully interpret. (e.g., "What is that gold UI element at
   0:34? Looks like a custom branded watermark.")
```

This document IS the blueprint. Peter and Ellie can work directly from it.

## How the pipeline works (under the hood)

The skill chains four steps. The user doesn't see this — they just paste a URL and wait 30 sec to 5 min depending on video length.

```
1. download.py     yt-dlp pulls the video file
                   ↓
2. transcribe.py   Get the transcript (caption API or Whisper)
                   ↓
3. frames.py       Smart frame extraction — scene-change detection
                   + coverage floor (1 frame per N seconds).
                   Caps at 80 frames per video.
                   ↓
4. analyze.py      Builds a bundle pairing each frame with its
                   ±15-second transcript window. Claude (the
                   invoking skill) reads each frame as multimodal
                   vision input and writes the structured notes.
```

The vision pass uses Claude's built-in multimodal capability — same model that handles image uploads in chat. No separate API key required (the Cowork environment is already Claude-powered).

For videos longer than 10 minutes, the skill confirms with the user before starting the vision pass (cost ramps up with frame count).

## Trigger boundaries — when this skill fires vs siblings

| User says | Skill that fires |
|---|---|
| "transcribe this video" | video-transcriber only |
| "watch this video" | video-watcher only |
| "full breakdown" / "make ours like this" | video-watcher (often also pulls in transcriber for the audio side) |
| "what's in this video" | video-watcher (visual) — though if context suggests "what was said" then transcriber |
| URL alone with no verb | Default: video-transcriber (faster, cheaper, more common need). User can clarify "watch instead" to flip. |
| "generate a blog post from this video" | content-creation-engine (which internally may call video-watcher + video-transcriber) |

When in doubt: ask. Don't burn $0.80 of vision API on the wrong tool.

## Optional flags the user can request

- **"just the shot list"** — skip TLDR, hooks, etc. Return only the B-Roll Catalog + Per-Scene Notes
- **"just the Replicate-This brief"** — skip everything except the recreation instructions
- **"first 30 seconds only"** — analyze only the opening (cheap fast scan for hook study)
- **"save to file"** — write the analysis to `outputs/video-analysis/analysis-{slug}-{timestamp}.md`
- **"and find the cuts"** — produce a cut-list optimized for Premiere editing reference
- **"with the transcript inline"** — invoke video-transcriber too and interleave the spoken lines into the shot list

## Cost honesty

Vision API isn't free. Rough estimates per video:

| Video length | Frames extracted | Approx cost |
|---|---|---|
| 30-second Reel | 5-10 frames | $0.05-$0.15 |
| 90-second Short | 10-20 frames | $0.10-$0.30 |
| 5-minute video | 30-50 frames | $0.30-$0.80 |
| 30-minute interview | 60-80 frames (capped) | $0.50-$1.50 |

For Peter and Ellie running 2-3 reference videos per week: roughly $5-15/month total. For Graeham doing competitor sweeps: depends on volume.

The skill ALWAYS reports estimated frame count before kicking off the vision pass on long videos. The user can abort if the cost feels high.

## Setup requirements

The Cowork sandbox auto-installs these on first run:

```bash
pip install yt-dlp youtube-transcript-api openai-whisper --break-system-packages
apt install -y ffmpeg  # usually already installed
```

For Peter and Ellie's local installs, the skill auto-installs dependencies on first run too. They might see a one-time "installing yt-dlp..." message on the first invocation; subsequent runs are immediate.

**Optional env vars** (none required for the default flow):
- `OPENAI_API_KEY` — uses OpenAI Whisper API for faster transcription on long videos (the audio path costs $0.006/min)
- `APIFY_API_TOKEN` — fallback for niche platforms yt-dlp doesn't support
- `DATAFORSEO_LOGIN` + `DATAFORSEO_PASSWORD` — Tier 0 caption pull for YouTube videos (free per pull, $0.004 if used)

## Example: end-to-end run

**Peter pastes:**
```
make ours like this: https://www.instagram.com/reel/DXNXXXX/
```

**Skill flow:**
1. Detects: Instagram Reel
2. Estimates cost: ~15 frames × vision API ≈ $0.20
3. Asks Peter to confirm (auto-skips this prompt for short videos)
4. Runs yt-dlp to download the Reel (~20 MB, 5 sec)
5. Runs frames.py — extracts 12 frames at scene changes
6. Runs transcribe.py — pulls 90-second transcript
7. Runs analyze.py — builds the multimodal bundle
8. Claude reads each frame + surrounding transcript context
9. Writes the full structured markdown analysis
10. Returns to Peter as a clean document he can paste into Premiere notes

Total: ~90 seconds. Output: a blueprint he can shoot from tomorrow.

## How content-creation-engine uses this

The engine's Phase 0 (Source Ingestion) has two modes:
- **Mode A (transcript only)** — default for most content generation tasks
- **Mode B (transcript + visual analysis)** — invoked when the user wants to replicate a reference video's style, not just its message

In Mode B, content-creation-engine now calls `video-watcher` as an external skill instead of running the embedded analysis code. The output flows into the script-writer Phase to inform shot direction in the generated content package (which inline shot tags to use, what B-roll types to source, what production style fingerprint to match).

This means content-creation-engine becomes a *composer* of skills rather than an *owner* of code. It's cleaner architecture and makes each capability discoverable as its own skill.

## Failure handling

| Failure | What the skill does |
|---|---|
| URL not recognized by yt-dlp | Reports the platform, asks user to confirm an alternate path |
| Video is private or geo-blocked | Reports the access error verbatim |
| Frame extraction fails (corrupt video) | Falls back to coverage-floor sampling only (drop scene detection) |
| Vision API rate-limited | Backs off, retries; if persistent, falls back to text-only analysis using existing transcript + filename + duration |
| Video is very long (>30 min) | Confirms with user before kicking off (cost concern) |
| Network access blocked (Cowork sandbox firewall) | Reports the block honestly, suggests running locally on user's machine instead |

## Maintenance

The 6 Python scripts in `scripts/` were lifted from `content-creation-engine/scripts/video-research/` on 2026-05-15. They are now the canonical owners of this logic. If content-creation-engine still has copies, those are deprecated — refer here.

When yt-dlp's platform list expands, frame extraction expands automatically. When Claude's vision model improves, the analysis output improves automatically. No code changes needed in this skill.

## Why this exists (history)

Before this skill, visual analysis of a video required:
1. Knowing about content-creation-engine's Phase 0 Mode B (most users didn't)
2. Explicitly opting into Mode B in a content-engine invocation (most invocations didn't)
3. Going through all the content-engine ceremony just to get a shot list

That meant the capability existed in the codebase but was effectively dormant. Extracting it into a standalone skill with the right trigger keywords makes it discoverable and usable on its own. The 6 worker scripts (download/frames/transcribe/analyze/library/dataforseo) didn't change — only the wrapper changed.
