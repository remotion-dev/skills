# Phase 0 — Source Ingestion (YouTube Transcription)

**Purpose:** When the user provides a YouTube video or channel URL as source material, transcribe it and extract key ideas before entering the standard content pipeline (Phases 1–5). This phase converts external video content into structured input that the rest of the pipeline can use.

## When to Run Phase 0

Run this phase when the user:
- Pastes a YouTube URL and says something like "use this as inspiration" or "I saw this video"
- Asks to analyze a competitor's video content
- Wants to incorporate ideas from another creator's video into their own scripts
- Provides a channel URL and wants to study their content approach
- Says "transcribe this" or "what does this video say"

**Skip this phase** when the user is just asking for original content ideas with no external video source.

## How It Works — Two-Tier Transcription

The transcriber uses a cost-optimized two-tier approach. Both tiers are **completely free ($0)**.

### Tier 1: Caption Pull (instant, ~2 seconds)
- Uses `youtube-transcript-api` to pull YouTube's built-in captions
- Works on ~90% of YouTube videos (any video with manual OR auto-generated captions)
- Returns timestamped transcript segments
- **Always try this first**

### Tier 2: Whisper Fallback (~1-3 minutes per video)
- Downloads audio via `yt-dlp`, then transcribes locally with OpenAI Whisper
- Works on 100% of videos (as long as there's audio)
- Uses the `base` model by default (best speed/accuracy tradeoff)
- Only runs when Tier 1 finds no captions
- Requires `openai-whisper` and `ffmpeg` to be installed

### Running the Script

The transcriber script is at `scripts/youtube_transcriber.py`. It can be run directly or imported.

**Direct CLI usage:**
```bash
# Single video
python scripts/youtube_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Channel (latest 10 videos)
python scripts/youtube_transcriber.py "https://www.youtube.com/@ChannelName" --channel --limit 10

# JSON output (for programmatic use in later phases)
python scripts/youtube_transcriber.py "URL" --format json
```

**As an import (when Claude is running the pipeline):**
```python
from scripts.youtube_transcriber import transcribe_video, extract_video_id

video_id = extract_video_id("https://www.youtube.com/watch?v=VIDEO_ID")
result = transcribe_video(video_id)
# result = {'text': '...', 'segments': [...], 'method': 'captions', 'language': 'en', ...}
```

**When running from Cowork (most common):** Claude should use bash to run the script, or directly call the youtube-transcript-api from inline Python in bash. The sandbox may have network restrictions, so if the script can't reach YouTube, Claude should inform the user and offer to:
1. Use Claude in Chrome to navigate to the video and extract the transcript manually
2. Ask the user to paste the transcript directly

## Phase 0 Output

The transcript output is saved to `outputs/transcripts/transcript-{video_id}-{timestamp}.txt` and contains:

1. **Metadata header** — video title, URL, transcription method, language
2. **Timestamped segments** — `[MM:SS] text` format for easy scanning
3. **Full text block** — continuous text for analysis

## What to Do With the Transcript

After transcription, analyze the content and produce a **Source Ingestion Brief** before proceeding to Phase 1 or Phase 5. The brief should contain:

### 1. Content Summary (2-3 sentences)
What is this video about? What's the creator's main argument or message?

### 2. Key Ideas Worth Adapting (3-5 bullet points)
What specific ideas, frameworks, data points, or angles could Graeham adapt for his Bay Area real estate audience? Be specific — don't just say "good tips about staging." Say "The creator's 3-tier staging framework (declutter → depersonalize → style) could be adapted for EPA sellers who are owner-occupants on a budget."

### 3. Graeham's Unique Angle
How would Graeham's version differ? What local context, market data, or personal experience would he add? Remember Graeham's voice: direct, knowledgeable, Bay Area-specific, never generic.

### 4. Suggested Content Format
Based on the source material, what format(s) make sense?
- Short-form (Reel/Short/TikTok) — if the key idea can land in 30-60 seconds
- Long-form (YouTube) — if the topic needs depth
- Both — with hook from short driving to long

### 5. Funnel Position
TOFU, MOFU, or BOFU? Why?

### 6. Fair Housing Check
Does any of the source content touch on demographics, school ratings, neighborhood character, or other FHA-sensitive topics? If so, note what needs to be reframed or dropped.

## After Phase 0

Once the Source Ingestion Brief is complete, the workflow branches:

- **If user wants a full content package:** Feed the brief into Phase 3 (BOFU Scorer) → Phase 4 (Funnel Tagger) → Phase 5 (Script Writer). Skip Phases 1-2 since the source video replaces the ideation step.
- **If user just wants a quick script:** Jump directly to Phase 5 (Script Writer) with the brief as context.
- **If user just wanted the transcript:** Deliver the transcript and brief, done.

## Dependencies

```
# Tier 1 (required)
pip install youtube-transcript-api --break-system-packages

# Tier 2 (optional — only needed for videos without captions)
pip install yt-dlp openai-whisper --break-system-packages
apt install ffmpeg  # Linux
brew install ffmpeg  # Mac
```

## Cost

$0 total. Both tiers use free, open-source tools with no API keys or subscriptions required.
