---
name: video-script-creation-engine
description: "Bay Area / East Palo Alto real estate content and video script engine for Graeham Watts (REALTOR, Intero Real Estate, DRE# 02015066). Use this skill ANY time the user mentions: video scripts, video ideas, content ideas, weekly content, content calendar, YouTube, Reels, Shorts, TikTok, AI avatar script, listing video, market update video, BOFU content, TOFU content, MOFU content, funnel content, lead gen content, Bay Area real estate content, East Palo Alto content, Redwood City content, Palo Alto content, Menlo Park content, San Mateo County content, Peninsula content, Reddit ideation, Apify scrape, content scoring, content pillars, GHL keyword capture, AB 1482, relocation content, first-time-buyer content, layoff content, seller content, transcribe YouTube video, YouTube transcript, analyze this video, use this video as inspiration, or anything related to generating inbound real-estate video content for Graeham's markets. Also trigger when the user uploads MLS data or a new listing and wants a content package for it, asks what they should post this week, or pastes a YouTube URL and wants to transcribe, analyze, or draw content ideas from it."
---

# Video Script Creation Engine

Modular real estate content generation system for Graeham Watts. Turns a single prompt into a scored, funnel-tagged, multi-platform content package grounded in live Bay Area buyer and seller questions.

This skill runs a 5-phase pipeline. The phases are sequential — run them in order, don't skip ahead. The point of the pipeline is to ground every piece of content in evidence of real audience demand before writing any script, so Graeham isn't guessing about what the market wants to hear.

## Before You Start — Read These

1. **`CLAUDE.md`** (bundled with this skill) — full orchestrator / project instructions. Read this first for the complete workflow, Fair Housing compliance section, lead capture keyword matrix, and data source strategy.
2. **`references/market-config.md`** — Graeham's agent identity, primary/secondary markets, CRM config, lead magnets, content pillars, jurisdiction-specific process terms. This grounds every piece of generated content in Graeham's real market context.

## Agent Identity

You are generating content as Graeham Watts — REALTOR at Intero Real Estate, DRE# 02015066. Primary market is East Palo Alto. Secondary markets are Redwood City, Palo Alto, Menlo Park, San Mateo County, and the Peninsula. CRM is GoHighLevel with comment-keyword lead capture configured for SELL, BUY, COSTS, OPTIONS, and 1482 triggers.

## Fair Housing Guardrails (Non-Negotiable)

NEVER generate content that:
- Describes neighborhoods by demographics (race, religion, national origin, family status, disability)
- Uses "safe / good areas / family-friendly / up-and-coming" as a proxy for demographic signaling
- Ranks or rates schools as a primary selling point for a neighborhood
- Promotes kickback arrangements with lenders, inspectors, or other vendors

Neighborhood content is limited to: property features, price ranges, market trends, lot sizes, amenities, architecture, housing stock age, HOA structure, zoning, new development, commute/transit facts, and walkability. When in doubt, reframe or drop the topic. This is both the law and Graeham's brand standard.

## The 6-Phase Workflow (Phase 0 + Phases 1–5)

Each phase has its own detailed instruction file in `references/phases/`. Read the phase file before executing that phase.

### Phase 0 — Source Ingestion (YouTube Transcription) ✦ NEW

**Read:** `references/phases/source-ingestion/instructions.md`

**When to use:** Run this phase FIRST when the user provides a YouTube video or channel URL as source material. This transcribes external video content and produces a Source Ingestion Brief that feeds into later phases.

**How it works:** Two-tier transcription system — tries free caption pull first (instant), falls back to OpenAI Whisper (free, local, ~1-3 min) for videos without captions. Run `scripts/youtube_transcriber.py` for the transcription.

**After Phase 0:** If the user provided a source video, skip Phases 1-2 (the source video replaces ideation) and jump to Phase 3 (BOFU Scorer) with the Source Ingestion Brief, or go directly to Phase 5 (Script Writer) for a quick script.

**Skip this phase** when the user is asking for original content ideas with no external video source — go straight to Phase 1.

Output: `outputs/transcripts/transcript-{video_id}-{timestamp}.txt` + Source Ingestion Brief.

### Phase 1 — BOFU Query Generator

**Read:** `references/phases/bofu-query-generator/instructions.md`

Generate 230+ localized bottom-of-funnel query patterns across 5 inquiry types (SELL, BUY, COSTS, OPTIONS, 1482). Output: `outputs/bofu-queries-{timestamp}.json`.

### Phase 2 — Content Ideation Engine

**Read:** `references/phases/content-ideation-engine/instructions.md` and its reference files:
- `references/phases/content-ideation-engine/references/apify-actors.md` — Apify actor config
- `references/phases/content-ideation-engine/references/subreddit-list.md` — target subreddits with priorities
- `references/phases/content-ideation-engine/references/query-templates.md` — search query templates
- `references/phases/content-ideation-engine/references/ideation-rubric.md` — what signals to extract

Pull live audience demand via Apify `trudax/reddit-scraper-lite` (primary) + Claude web search + browser deep dives (supplementary). Run `scripts/run_reddit_ideation.py` for the Reddit scrape. Requires `APIFY_API_TOKEN` in environment.

Output: `outputs/ideation-raw-{timestamp}.json` and `outputs/ideation-topics-{timestamp}.json`.

### Phase 3 — BOFU Scorer

**Read:** `references/phases/bofu-scorer/instructions.md`

Score each candidate topic on the 5-criteria rubric (Inquiry Type Match, Intent Matrix Position, Source Confirmation, Emotional Temperature, Local Relevance). Keep ≥18/25. Output: `outputs/scored-topics-{timestamp}.json`.

### Phase 4 — Funnel Tagger

**Read:** `references/phases/funnel-tagger/instructions.md`

Tag surviving topics TOFU / MOFU / BOFU. Default mix 40/30/30. Override based on user goal (lead gen bias = 20/30/50, audience growth bias = 60/25/15, fresh-listing bias = heavy BOFU for that listing's market). Output: `outputs/tagged-topics-{timestamp}.json`.

### Phase 5 — Script Writer

**Read:** `references/phases/script-writer/instructions.md` and its reference files:
- `references/phases/script-writer/references/content-pillars.md` — Graeham's content pillar framework
- `references/phases/script-writer/references/platform-specs.md` — per-platform length/format rules
- `references/phases/script-writer/references/cross-posting-matrix.md` — cross-post adaptation matrix
- `references/phases/script-writer/references/voice-and-style.md` — Graeham's voice guide
- `references/phases/script-writer/references/seo-keywords.md` — SEO keyword set
- `references/phases/script-writer/references/aeo-geo-requirements.md` — Answer Engine Optimization + Geo requirements
- `references/phases/script-writer/references/lead-capture-keywords.md` — GHL comment-keyword automation map

Produce multi-platform content packages: hook, short-form script, long-form script, caption, hashtags, comment-keyword CTA, cross-post matrix, AND an **ElevenLabs-Ready Variant** (v3 audio tags + v2 break-tag fallback + voice settings block) for every script so Graeham can paste directly into ElevenLabs with no guessing on inflection. See `references/phases/script-writer/references/elevenlabs-audio-tags.md`. Output: `outputs/content-package-{timestamp}.md`.

## V6 Production Bible Integration

When scripts are generated as part of a V6 Production Calendar (content-calendar skill), the
output format changes from standalone markdown to **embedded HTML derivative panels** inside the
hosted calendar page. This section documents the V6-specific requirements.

### Derivative Format System

Every content day MUST produce scripts for ALL of these platform formats:

| Format | Key Specs | Notes |
|--------|-----------|-------|
| **YouTube Long** | 8-15 min, 16:9, 1080p | Core asset — fullest script with all production details |
| **YouTube Short** | 30-59 sec, 9:16, 1080p | Strongest hook + one key insight + CTA |
| **IG Reel #1** | 30-60 sec, 9:16, 1080p | Hook-first, face-to-camera, caption overlay |
| **IG Reel #2** | 15-30 sec, 9:16, 1080p | Different angle/hook from Reel #1, B-roll heavy |
| **IG Carousel** | 5-10 slides, 1:1 or 4:5 | Key stats/facts as visual slides, swipe CTA |
| **TikTok** | 30-60 sec, 9:16, 1080p | More casual tone, trending audio hook if applicable |
| **Blog** | 800-1200 words, SEO-optimized | AEO-ready with cite-worthy key statements |
| **GMB (Google My Business)** | 100-300 words, 1 image | Local SEO post, location-tagged |
| **Facebook** | Cross-post from primary + FB-native caption | Longer caption OK, link in post |

Each derivative panel includes: full script, platform specs, caption with hashtags, description/
SEO metadata, posting instructions, and GHL keyword CTA.

### Inline Shot Direction Tags

Every script (especially the YouTube Long core asset) MUST include inline shot direction tags
embedded directly in the script text. These tell Jason (the video editor) exactly what visual
to use at each moment:

```
[TALKING HEAD] — Graeham speaking directly to camera
[B-ROLL: description of footage needed] — Overlay footage
[TEXT OVERLAY: "exact text to display"] — On-screen text/graphics
[DRONE: description of aerial shot] — Drone footage
[SCREEN RECORD: description of what to capture] — Screen recording
[TRANSITION: type] — Cut/dissolve/swipe transition
```

Place these INLINE within the script, not as a separate section. Example:
```
[TALKING HEAD] "If you own rental property in California, you need to know about AB 1482."
[TEXT OVERLAY: "AB 1482 — California Tenant Protection Act"]
[B-ROLL: California apartment complexes, rental signs]
"This law caps your annual rent increase at 5% plus CPI, or 10% — whichever is lower."
[TEXT OVERLAY: "Max Increase: 5% + CPI or 10%"]
```

### Editing Notes for Jason

Every core asset script MUST include an **Editing Notes** block — a dedicated section for the
video editor with production-specific instructions:

```
EDITING NOTES FOR JASON:
B-ROLL SHOT LIST:
- [List specific B-roll clips needed with descriptions]
- [Include stock footage suggestions if no original footage exists]

TEXT OVERLAY TIMING:
- [Timestamp] -> [Text to display] (duration: Xs)
- [Timestamp] -> [Text to display] (duration: Xs)

PACING NOTES:
- [Specific pacing instructions — fast cuts for hook, slower for education, etc.]

THUMBNAIL CONCEPT:
- [Describe the thumbnail — text, expression, background, colors]

MUSIC / SFX DIRECTION:
- [Music mood, tempo, genre suggestion]
- [Specific SFX moments — whoosh on transition, ding on stat, etc.]
```

### ElevenLabs SSML Blocks

Every core asset script MUST include a complete ElevenLabs SSML block — the full script
wrapped in `<speak>` tags with prosody and break markup so Graeham can paste it directly
into ElevenLabs for AI avatar voice generation:

```xml
<speak>
  <prosody rate="medium" pitch="medium">
    If you own rental property in California,
  </prosody>
  <break time="400ms"/>
  <prosody rate="slow" pitch="low" volume="loud">
    you need to know about AB 1482.
  </prosody>
  <break time="600ms"/>
  ...
</speak>
```

Use `<prosody>` for emphasis shifts, `<break>` for natural pauses, vary rate/pitch for
engagement. The hook should have higher energy (faster rate, higher pitch), educational
sections should be measured (medium rate), and CTAs should be emphatic (slower, louder).

### AI Video Prompts (Seedance 2.0 / Kling)

For content days that would benefit from AI-generated video (cinematic hooks, B-roll that
doesn't exist as footage, pattern-interrupt openers), include an **AI Video Prompt** block:

```
AI VIDEO PROMPT (Seedance 2.0):
SHOT: [Hook / B-Roll / Transition]
PROMPT: "Cinematic aerial drone shot of [description], golden hour lighting,
  slow dolly forward, shallow depth of field, 4K, [duration]s"
CAMERA: [Movement type — dolly, crane, orbit, static, handheld]
LIGHTING: [Golden hour / overcast / interior warm / etc.]
DURATION: [3-5 seconds typical]
USE IN EDIT: [Where this clip goes in the timeline]
```

Include 2-3 AI video prompts per content day where applicable. Focus on:
- Hook shots (first 2-3 seconds — the scroll-stopper)
- B-roll that would be expensive or impossible to film (aerials, time-lapses, cinematic establishing shots)
- Transition moments between script sections

### GHL Keyword Capture Integration

Every script CTA must include a GHL comment-keyword trigger. Current active keywords:
`SELL`, `BUY`, `COSTS`, `OPTIONS`, `1482`, `EPA`, `VALUE`, `READY`, `INVEST`, `NUMBERS`,
`RELOCATING`, `MARKET`, `CHECKLIST`, `WATCH`, `RWC`, `PA`, `MP`, `SF`

Format: "Comment [KEYWORD] below and I'll send you [lead magnet]"

### AEO (Answer Engine Optimization)

Every long-form script and blog derivative MUST include **cite-ready key statements** —
factual, data-heavy sentences that AI search engines (ChatGPT, Perplexity, Gemini) can
cite as authoritative answers. Format these as standalone declarative statements with
specific numbers, dates, or legal references.

## Examples

Three worked examples live in `examples/`:
- `example-1-bofu-trigger-event-tech-layoff.md` — BOFU response to a tech layoff trigger event
- `example-2-tofu-lifestyle-reel-epa-tacos.md` — TOFU lifestyle reel (East Palo Alto tacos)
- `example-3-aeo-legal-education-ab1482.md` — AEO-optimized legal education on AB 1482

Read these before writing new content packages — they show the expected output format and voice.

## Example Prompts

- "Give me this week's content — focus on lead gen for East Palo Alto sellers"
- "Generate 5 BOFU videos about AB 1482 for Bay Area landlords"
- "What should I post this week based on what's trending in Redwood City?"
- "I just got a new listing in Menlo Park at $2.1M — give me the full content package"
- "Make me a TOFU reel about East Palo Alto lifestyle"
- "The Bay Area just had a big tech layoff announcement — what should I post?"
- "Hey I saw this video, can we do something like this? https://youtube.com/watch?v=..."
- "Transcribe this YouTube video and tell me what ideas we can use"
- "Check out this channel — what topics are they covering that I should cover too? https://youtube.com/@..."
- "Here's a video about staging tips — adapt it for EPA sellers on a budget"

## Output Locations

All phase outputs save to the user's selected folder (or `outputs/` in Cowork). Provide `computer://` links to the final content package when delivering.

## Data Source Status

- **Primary:** Apify `trudax/reddit-scraper-lite` with residential proxy (~$0.30-$2.50 per run). Requires `APIFY_API_TOKEN`.
- **Supplementary:** Windsor MCP for Instagram, YouTube, Facebook, and Search Console performance data.
- **Supplementary:** Claude web search for market context, news events, and competitor research.

## Auto-Render Hand-off (v6.1 — Apr 2026)

Once a V6 script is finalized, it no longer needs to be manually copy-pasted into ElevenLabs and HeyGen. The `heygen-elevenlabs-renderer` skill owns the full render pipeline and this skill hands off to it.

### What this skill produces for the renderer

For every core asset script written, write out a companion SSML file next to the content package:

```
outputs/content-package-{timestamp}.md         (the full package — scripts, captions, etc.)
outputs/content-package-{timestamp}.ssml.txt   (just the <speak>…</speak> block, nothing else)
```

The `.ssml.txt` file is the raw input the renderer reads. It must contain only the SSML — no headers, no comments, no markdown fences, no "SCRIPT:" prefix. One file = one render.

### Known SSML quirks (read before hand-off)

ElevenLabs `eleven_multilingual_v2` does NOT fully honor `<prosody>`. Only `<break time="Xs"/>` produces audible effect. `<prosody rate="slow">` tags are accepted by the API but silently dropped — the inner text is still read, just at the default speed. So:

- KEEP `<prosody>` tags for human readability in the package file (they document intent)
- ALSO provide the `.ssml.txt` with the same tags (the renderer strips ineffective ones at TTS time)
- When you genuinely need rate/pitch change (e.g., whispered BOFU asides), use **ElevenLabs bracket audio tags** inside the text: `[whispers]`, `[excited]`, `[sarcastic]`, `[laughs]`. See the renderer skill's `references/elevenlabs-audio-tags.md`.

### Hand-off invocation (one command)

After this skill writes the package, the renderer takes over:

```bash
python3 skills/heygen-elevenlabs-renderer/scripts/full_render.py \
  --script outputs/content-package-{timestamp}.ssml.txt \
  --slug "{content-slug}" \
  --resolution 1080p \
  --aspect 9:16
```

The renderer: (1) synthesizes MP3 via ElevenLabs using Graeham's voice clone `Pa3vOYQHHpLJn1Tf7hnP`, (2) uploads MP3 to HeyGen, (3) creates an avatar video against Graeham's avatar `9a3600b16f604059b6ab8b9a55e29ea9`, (4) polls until complete, (5) downloads MP4 to `outputs/renders/{slug}.mp4` with a sibling `{slug}.meta.json` holding `video_id`, `video_url`, and duration.

### Dashboard locations (where rendered media lives)

After a render completes, the same files are available in three places:

| Where | URL | What you see |
|---|---|---|
| Local disk | `outputs/renders/{slug}.mp4` | The MP4 file, ready to upload anywhere |
| HeyGen dashboard | https://app.heygen.com/home (Projects tab) | The video by title, shareable link, re-render options |
| ElevenLabs history | https://elevenlabs.io/app/speech-synthesis/history | The raw MP3, downloadable again, with the SSML used |

The `{slug}.meta.json` file always contains the HeyGen `video_id` — that's the canonical identifier you can search for in the HeyGen dashboard to find any past render.

### Recommended resolution per format

| Format | Resolution | Why |
|---|---|---|
| Reels / Shorts / TikTok (9:16) | 1080p | Instagram/TikTok recompress hard; 720p looks noticeably blurry |
| YouTube Long (16:9) | 1080p | Minimum for YouTube's "HD" badge |
| Listing videos | 4k | Cuts down well for MLS and sold as premium |
| Quick internal tests | 720p | Saves HeyGen credits when iterating |
