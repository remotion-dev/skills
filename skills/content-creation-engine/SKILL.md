---
name: content-creation-engine
description: "Bay Area / East Palo Alto real estate content creation engine for Graeham Watts (REALTOR, Intero Real Estate, DRE# 01466876). Use this skill ANY time the user mentions: content creation engine, content engine, create content, newsletter content, blog post, ad copy, social media content, video script, content for [topic], what should I post, generate content, video scripts, video ideas, content ideas, weekly content, content calendar, YouTube, Reels, Shorts, TikTok, AI avatar script, listing video, market update video, BOFU content, TOFU content, MOFU content, funnel content, lead gen content, Bay Area real estate content, East Palo Alto content, Redwood City content, Palo Alto content, Menlo Park content, San Mateo County content, Peninsula content, Reddit ideation, Apify scrape, content scoring, content pillars, GHL keyword capture, AB 1482, relocation content, first-time-buyer content, layoff content, seller content, transcribe YouTube video, YouTube transcript, analyze this video, use this video as inspiration, run research, what should I post this week, content opportunities, what's happening in EPA, find me topics, content intelligence, weekly research, I need content, what's new in East Palo Alto, market research, research first, topic discovery, or anything related to generating inbound real-estate content for Graeham's markets. Also trigger when the user uploads MLS data or a new listing and wants a content package for it, asks what they should post this week, or pastes a YouTube URL and wants to transcribe, analyze, or draw content ideas from it."
---

# Content Creation Engine

Modular real estate content generation system for Graeham Watts. Turns a single prompt into a scored, funnel-tagged, multi-platform content package grounded in live Bay Area buyer and seller questions.

**This skill is RESEARCH-FIRST.** The primary workflow starts with data collection and opportunity scoring before any content is written. Every piece of content Graeham publishes should be grounded in evidence of real audience demand, live market data, or timely local events — not guesswork.

## Before You Start — Read These

1. **`CLAUDE.md`** (bundled with this skill) — full orchestrator / project instructions. Read this first for the complete workflow, Fair Housing compliance section, lead capture keyword matrix, and data source strategy.
2. **`references/market-config.md`** — Graeham's agent identity, primary/secondary markets, CRM config, lead magnets, content pillars, jurisdiction-specific process terms. This grounds every piece of generated content in Graeham's real market context.
3. **`references/research-sources.md`** — Complete documentation of every data source used in Phase R (Research & Discover), including what to pull, how to pull it, what to look for, and the scoring rubric.
4. **Shared Branding** — Before generating any client-facing output, read the shared branding reference at `../shared-references/branding.md` for consistent colors, fonts, and UI components.

## Agent Identity

You are generating content as Graeham Watts — REALTOR at Intero Real Estate, DRE# 01466876. Primary market is East Palo Alto. Secondary markets are Redwood City, Palo Alto, Menlo Park, San Mateo County, and the Peninsula. CRM is GoHighLevel with comment-keyword lead capture configured for SELL, BUY, COSTS, OPTIONS, and 1482 triggers.

## Production Rules (Non-Negotiable)

These rules exist because ignoring them caused real bugs in production on April 18, 2026. Every one has a specific failure mode attached. Follow them every time.

### Rule 1: HTML Generation Safety — Use Python, Not Bash Heredoc

NEVER use `cat > file << 'EOF'` bash heredoc to write HTML files. Bash silently escapes `\!` characters in HTML comments to `\\!`, which breaks comment parsing and leaks raw visible text onto the rendered page.

ALWAYS write HTML via Python `Path.write_text()`:

```python
from pathlib import Path
Path("content-calendars/my-dashboard.html").write_text(html_content, encoding="utf-8")
```

After writing, VERIFY with: `grep -c '<\\\!--' file.html` — must return 0. Reject and rewrite if non-zero.

**Failure mode this prevents:** April 18, 2026 dashboard had 20+ visible escaped comment strings rendered as text on the page.

### Rule 2: Mandatory Screenshot-Loop After HTML Output

After writing any HTML to `content-calendars/` or `emails/`, read `skills/website-builder/references/screenshot-loop.md` and execute it BEFORE `git push`. Minimum 1 iteration, target 3.

Sandbox Chromium install often fails. Fallback: push to GitHub Pages first, then use Claude-in-Chrome MCP to navigate to the live URL and screenshot. If bugs found, fix locally, push again, re-verify.

**Failure mode this prevents:** Shipping broken HTML because nobody looked at the rendered page. Code review catches structure; screenshots catch vibe, color, hierarchy, and rendering bugs.

### Rule 3: PROMPT_LIBRARY Default for Multi-Format Dashboards

For any multi-format deliverable dashboard (single-topic OR weekly), use the `window.PROMPT_LIBRARY` JS object pattern with a Copy button per format. Each prompt includes Agent Identity + Fair Housing + DATE/YEAR QC + Timing Self-Check + Voice + Topic + AEO stats + Key Facts + GHL CTA + format-specific deliverable spec.

NEVER pre-generate full script/caption/blog content inline in the dashboard HTML. Reasons:
- Risks truncation on long outputs
- Burns context on content external AIs generate better
- Makes the dashboard hard to iterate on

Reference: `content-calendars/2026-04-20-production-calendar-v6.html`.

**Failure mode this prevents:** April 18, 2026 first attempt generated 10 inline scripts consuming 100K+ chars and still risking truncation.

### Rule 4: Timing Self-Check in Every Script Prompt

Every script-generation prompt MUST include this block (same enforcement as DATE/YEAR QC):

```
TIMING SELF-CHECK (FOR SCRIPT OUTPUTS ONLY):
Before emitting any script, calculate: (spoken_word_count / 150 WPM) * 1.15 = target_minutes.
Show the math in the output. NEVER default to generic durations like "8-10 min".
```

**Failure mode this prevents:** April 18, 2026 initial estimate of "8-10 min" for a 573-word script that was actually 4:30.

### Rule 5: Single-Topic Dashboard Output Format

Single-topic content packages go to:

```
content-calendars/YYYY-MM-DD-{slug}-production.html
```

NOT a markdown file. HTML goes to GitHub Pages for the live URL the production team uses. Same design language as weekly calendars (navy/gold palette, DM Sans + Plus Jakarta Sans, same component classes).

**Failure mode this prevents:** April 18, 2026 first output was a markdown file that wasn't accessible to the production team via a live URL.

### Rule 6: Gold Is A Brand Color — Use Sparingly

`--gold` (#C5A258) is Graeham's real estate brand color. Reserve for brand moments only. Maximum ~10 instances per dashboard.

**Gold is for:** Primary action buttons (Copy Prompt, primary CTA), Opportunity Score values and score badges, PICKED / SELECTED tags, small hero accents, CTA section headings.

**Gold is NOT for:** General UI borders (use `--navy`), callout boxes (use `--teal` for tips, `--orange` for warnings), table headers, shot number circles, hover states on general UI.

**Failure mode this prevents:** April 18, 2026 dashboard applied gold to general UI chrome (timing card, intelligence stack borders, flow card states, use-in callouts, hook cards) — diluting brand impact.

---

## Self-Check Before Shipping

Before declaring any content-creation task complete, run this checklist explicitly in your response before pushing:

1. [ ] Timing calculation shown with math (word_count / 150 * 1.15 = minutes)
2. [ ] Fair Housing check passed (no demographic code words, no school rankings)
3. [ ] DATE/YEAR QC applied (2026 everywhere, historical refs explicitly labeled)
4. [ ] AEO statements open with date anchor ("As of April 2026...")
5. [ ] GHL keyword is valid (in the keyword matrix)
6. [ ] HTML output: `grep -c '<\\\!--'` returns 0 (no escape bug)
7. [ ] HTML output: screenshot-loop executed, visual verified
8. [ ] HTML output: PROMPT_LIBRARY used (not inline pre-generated content)
9. [ ] HTML output: gold usage is brand-only (Rule 6)
10. [ ] Source citations included with clickable links
11. [ ] Single-topic output: saved to `content-calendars/` as HTML, pushed to GH Pages

---

## Fair Housing Guardrails (Non-Negotiable)

NEVER generate content that:
- Describes neighborhoods by demographics (race, religion, national origin, family status, disability)
- Uses "safe / good areas / family-friendly / up-and-coming" as a proxy for demographic signaling
- Ranks or rates schools as a primary selling point for a neighborhood
- Promotes kickback arrangements with lenders, inspectors, or other vendors

Neighborhood content is limited to: property features, price ranges, market trends, lot sizes, amenities, architecture, housing stock age, HOA structure, zoning, new development, commute/transit facts, and walkability. When in doubt, reframe or drop the topic. This is both the law and Graeham's brand standard.

---

## THE RESEARCH-FIRST WORKFLOW

This is the primary workflow. When Graeham says "I need content," "what should I post," "run research," "content this week," or any content-related trigger — START HERE, not at script writing.

### Phase R — Research & Discover (RUNS FIRST, ALWAYS)

**Read:** `references/research-sources.md` for full source documentation and scoring rubric.

This phase pulls from ALL available data sources simultaneously, analyzes findings, scores them, and presents a Content Opportunity Report. No content is generated until Graeham picks his topics.

#### Step R.1 — Pull Data from All Sources

Hit every source in parallel. Don't wait for one to finish before starting the next. If a source fails or returns nothing, note it and move on — partial data is better than no data.

**Source 1 — MLS Market Stats** 📊
Log into MLSListings.com via Chrome. Pull latest stats for EPA, San Mateo County, Santa Clara County. Key metrics: median price, DOM, sale-to-list ratio, inventory, month-over-month changes, year-over-year changes. Flag any metric that moved ≥5% MoM or ≥10% YoY.

**Source 2 — Google Search Console** 🔍
Via Windsor MCP: `get_data` with connector `searchconsole`, account_id `sc-domain:graehamwatts.com`. Pull top queries by clicks and impressions for last 7 days. Compare to prior period. Look for rising queries (higher impressions than last period) and high-impression/low-click queries (rewrite opportunities).

**Source 3 — Local Government** 🏛️
Via Chrome, navigate to https://www.cityofepa.org and scrape: upcoming city council meetings/agendas, recent meeting minutes for real estate/development/zoning items, building permit applications, planning commission items. Also check https://www.cityofepa.org/communitydevelopment for development projects.

**Source 4 — Web Research** 📰
Use web search for: "East Palo Alto news" (last 7 days), "East Palo Alto development", "San Mateo County real estate news", "Bay Area housing market [current month] [current year]". Summarize top 3-5 relevant findings.

**Source 5 — Social Performance** 📱
Via Windsor MCP, pull recent Instagram and Facebook post performance data. Identify which content types/topics got the highest engagement in last 30 days. Note what formats work best (talking head, B-roll, carousel, etc.).

**Source 6 — Google Trends** 📈
Via web search, check trends.google.com for: "East Palo Alto real estate", "Bay Area home prices", "California housing market". Note any spikes or unusual interest.

**Source 7 — BOFU Keyword Data** 🎯
Check if bottom-of-funnel keyword data exists in `references/phases/bofu-query-generator/instructions.md`. Cross-reference with Search Console to find high-intent keywords not yet covered. Check `references/topic-history.json` for recently covered topics.

**Source 8 — Competitor Analysis (Apify)** 🕵️
Via Windsor MCP or Apify, pull latest scraper datasets for competitor content analysis. See `references/phases/content-ideation-engine/references/apify-actors.md` for actor config.

#### Step R.2 — Analyze and Compile Findings

Compile all findings into a unified Content Opportunity Report. For each finding, identify: the source, a headline summary, why it matters for Graeham's audience, and suggested content formats.

#### Step R.3 — Score Each Opportunity

Score each finding on a 1-10 scale:

| Criterion | Max Points | Scoring Guide |
|---|---|---|
| **Timeliness** | 3 | Breaking/this-week = 3, This month = 2, Evergreen = 1 |
| **Audience Relevance** | 3 | Direct property value impact = 3, Lifestyle/community = 2, Tangential = 1 |
| **Content Gap** | 2 | Never covered = 2, Covered >4 weeks ago = 1, Recently covered = 0 |
| **Engagement Potential** | 2 | Similar topics got high engagement = 2, Average = 1, Low-engagement pattern = 0 |

Items scoring ≥7 get ⭐ RECOMMENDED tag.

#### Step R.4 — Present the Content Opportunity Report

Organize by source. Format each opportunity like this:

```
[EMOJI] FROM [SOURCE]: [Headline summary]
Score: [X]/10 ⭐ RECOMMENDED (if score >= 7)
→ Suggested formats:
  • [Format 1] ([Platform] — [style: talking head / cinematic / educational / carousel / etc.])
  • [Format 2] ([Platform] — [style])
  • [Format 3] ([Platform] — [style])
→ Why this matters: [1-sentence explanation of relevance to audience]
```

Use these emojis by source:
- 🏛️ City Council / Local Government
- 📊 MLS Market Data
- 🔍 Google Search Console
- 📰 Local News (web research)
- 📱 Social Performance Insights
- 📈 Google Trends
- 🎯 BOFU Keywords
- 🕵️ Competitor Analysis (Apify)

Top 3-5 scored items get ⭐ RECOMMENDED tag.

Also show sources that returned nothing noteworthy, e.g.: "📈 Google Trends: No unusual spikes this week — steady interest levels."

#### Step R.5 — Ask for Selection

End the report with: "Which opportunities do you want to pursue this week? I recommend the starred ones, but you pick."

---

### Phase S — Select & Plan

User picks 2-3 topics from the Content Opportunity Report. Engine confirms:
- Which formats to generate for each topic (video script, newsletter section, blog post, ad copy, social posts)
- Which platforms each format targets
- Funnel tier assignment (TOFU / MOFU / BOFU) for each topic
- Any dependencies (e.g., "this topic needs MLS data screenshots for the carousel")

Confirm the plan with Graeham before proceeding to generation.

---

### Phase G — Generate Content

For each selected topic, produce ALL relevant formats using the existing phase pipeline:

1. **Video Script** — Long-form + short-form with clear section headers (see Script Output Format below). Includes ElevenLabs SSML block, inline shot directions, editing notes for Jason, and AI video prompts.
2. **Newsletter Section** — HTML formatted per the newsletter module. See `modules/newsletter/` and `../newsletter-generator/SKILL.md`.
3. **Blog Post Draft** — SEO-optimized with AEO cite-ready statements, meta description, title tag, and target keywords.
4. **Ad Copy Variants** — If the topic lends itself to paid promotion: Facebook ad copy, Google ad copy, with multiple hook variants for A/B testing.
5. **Social Posts** — Platform-specific: IG caption with hashtags and GHL keyword CTA, Facebook post, LinkedIn post (if applicable), Google My Business post.

The generation phase uses the existing 6-phase pipeline (Phase 0 through Phase 5) documented below for the actual content creation logic. Phase R replaces the "what should I write about?" question — by the time we reach Phase G, we already know exactly what topics to cover and why.

---

### Phase A — Review & Approve

Present all generated content to Graeham (and Adrian if applicable) for approval. For each piece:
- Show the content with its section headers
- Note the source data that inspired it (from Phase R)
- Flag any items that need fact-checking or data verification
- Ask for approval, revision requests, or rejection

---

### Phase D — Distribute

Once approved:
- **Newsletter:** Assemble full newsletter from selected sections, draft in Gmail via Gmail MCP
- **Blog:** Ready-to-publish format with SEO metadata
- **Social:** Platform-specific posts queued for posting
- **Ads:** Ready for deployment with targeting recommendations
- **Video:** Hand off to heygen-elevenlabs-renderer for avatar video rendering (see Auto-Render Hand-off section below)

---

## THE CONTENT GENERATION PIPELINE (Used by Phase G)

The phases below contain the detailed content creation logic. During the Research-First workflow, these are invoked during Phase G (Generate Content) after topics have been selected. They can also be invoked directly when Graeham already knows exactly what topic he wants to cover and skips research.

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

---

## Video Duration Estimation (Mandatory Calculation)

NEVER guess or default to generic durations like "8-10 minutes." Every script MUST include an explicit timing calculation based on actual word count:

1. **Count the actual words** in the script body (exclude shot directions, editing notes, and metadata)
2. **Average speaking pace:** 150 words per minute for conversational delivery
3. **Add 15%** for pauses, transitions, and B-roll cuts
4. **Formula:** `(word_count / 150) × 1.15 = estimated minutes`
5. **The target duration in the section header MUST match this calculation**

Examples:
- 150-word script → (150/150) × 1.15 = ~1.15 minutes → "Target: ~1 minute"
- 750-word script → (750/150) × 1.15 = ~5.75 minutes → "Target: ~6 minutes"
- 1500-word script → (1500/150) × 1.15 = ~11.5 minutes → "Target: ~11-12 minutes"

If the script is only ~150 words, it is a 1-minute video, NOT an 8-minute video. Be accurate. Show the word count and calculation in a comment at the top of the script output so the estimate is verifiable.

## Script Output Format (Required Section Headers)

Every script output MUST use the following visually distinct section headers so that Adrian, Peter, or John can grab just their section without confusion. Each section is self-explanatory and separated by a clear visual divider:

```
═══════════════════════════════════════════════════
📹 LONG-FORM SCRIPT (YouTube — Target: [X] minutes)
Platform: YouTube | Format: Talking head + B-roll
═══════════════════════════════════════════════════

[script content here]

═══════════════════════════════════════════════════
📱 SHORT-FORM SCRIPT (Reels / Shorts / TikTok — Target: [X] seconds)
Platform: Instagram Reels, YouTube Shorts, TikTok
Cut from: Long-form timestamp [X:XX - X:XX] OR record separately
═══════════════════════════════════════════════════

[script content here]

═══════════════════════════════════════════════════
🎬 SHOT LIST — Hand to production team (Peter/John)
═══════════════════════════════════════════════════

[shot list here with numbered shots, each with: shot description, duration estimate, location/setup notes]
```

These headers are non-negotiable. Every script output — whether standalone or embedded in a V6 Production Calendar — MUST start each piece with its corresponding header block. Do not omit headers, do not merge sections, do not use plain markdown headers instead. The visual dividers (`═══`) ensure each section is scannable when printed or viewed on a phone.

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

## Production Calendar Hardening (v7.3 — Apr 2026)

The following requirements apply whenever scripts are produced as part of a V6/V7 Production Calendar. They exist to prevent three failure modes encountered in production: year-drift in on-screen text, output truncation on long-form deliverables, and week-to-week content duplication.

### Date & Year QC (mandatory self-check block)

Every prompt in `PROMPT_LIBRARY` MUST carry a `DATE & YEAR QUALITY CONTROL` block placed immediately after Fair Housing Guardrails and before Voice & Style. The block instructs the generating model to:

- Treat the calendar's publication week as the current production date (e.g., April 2026 for the Apr 20-26 calendar).
- Force every year reference — text overlays, graphic callouts, on-screen stats, captions, email subject lines — to match the production year. Never a past year unless explicitly framed as historical with clear labeling.
- Open every cite-ready / AEO statement with a date anchor ("As of April 2026...", "As of Q2 2026..."). This makes statements durable for AI search engines to cite by name months later.
- Date-stamp every price/market stat ("As of April 2026, 3-bed SFH in Woodland Park is $680K-$850K") rather than emitting bare numbers.
- Self-scan the output before emitting and fix any bare-year drift.

The v7.3 production calendar contains the exact block text — copy it verbatim when building future calendars. This QC block is required on every format (YT Long Pt 1/2, Shorts, Reels, TikTok, Carousel, Blog, GMB, Facebook, Email), not just long-form.

### Output Split Strategy (YouTube Long only)

A single YouTube Long prompt requesting 6 deliverables (Script + SSML + Editing Notes + AI Video Prompts + YouTube SEO Package + 3 Alt Hooks) produces roughly 40K-60K chars of output, which exceeds default `max_tokens` on most consumer AI tools and causes the model to truncate mid-Deliverable 4.

Split YouTube Long prompts into TWO buttons:

- **Pt 1 — Script + Voice** → Deliverables 1 (full timestamped script with inline shot tags) + 2 (complete ElevenLabs SSML block). Target output ~20-25K chars, fits in one response on any tool.
- **Pt 2 — Production Package** → Deliverables 3 (Editing Notes for Jason) + 4 (AI Video Prompts) + 5 (YouTube SEO Package) + 6 (3 Alt Hooks for A/B testing). Target output ~20-25K chars. Includes the standard 5-minute structure reference (hook / problem / core1 / core2 / advisory / CTA) so the production package works without pasting the script back in.

Both parts share the same preamble (Agent Identity + Fair Housing + DATE/YEAR QC + Voice + Topic + Funnel Tier + AEO + Key Facts + GHL Lead Capture). Only the deliverable list and output-mode header differ.

Short-form formats (YT Shorts, IG Reels, TikTok, Carousel, Blog, GMB, Facebook, Email newsletter) do NOT need splitting — their single output fits comfortably in one response.

### Week-over-Week Overlap Check (mandatory pre-ship)

Before shipping each weekly calendar, run an overlap comparison against the immediately preceding week's calendar. For each of the 5 daily topics plus the email newsletter, compare against the prior week's topics on:

- **Title** — substring match or semantic overlap (e.g., "EPA Homes Under $700K" vs "EPA Homes Under $1M" = HIGH overlap)
- **Slug** — exact or near-exact match
- **Neighborhood** — repeated primary-market focus on consecutive days
- **Funnel tier** — consecutive weeks of same tier + same topic cluster
- **GHL keyword** — keyword reuse across weeks

Classify each match as HIGH / MODERATE / LOW risk. Write a markdown comparison note (`YYYY-MM-DD-vs-PRIOR-content-overlap-check.md`) alongside the calendar HTML in `content-calendars/` and commit it to the repo. HIGH-risk overlaps MUST be resolved before shipping — reframe the angle, replace the topic, or defer a week.

**Future systematization**: add a `TOPIC_HISTORY` object to the calendar HTML containing the last 4 weeks of (title, slug, neighborhood, tier, ghl_keyword) tuples. Future calendar generation runs an automatic pre-publish check against that history and flags overlaps without a manual pass.


## Examples

Three worked examples live in `examples/`:
- `example-1-bofu-trigger-event-tech-layoff.md` — BOFU response to a tech layoff trigger event
- `example-2-tofu-lifestyle-reel-epa-tacos.md` — TOFU lifestyle reel (East Palo Alto tacos)
- `example-3-aeo-legal-education-ab1482.md` — AEO-optimized legal education on AB 1482

Read these before writing new content packages — they show the expected output format and voice.

## Example Prompts

- "I need content" → Triggers Phase R (Research & Discover) — pulls all sources, presents Content Opportunity Report
- "What should I post this week?" → Same as above — research first, then pick topics
- "Run research" → Runs Phase R only, presents findings without generating content
- "Content opportunities" → Same as "run research"
- "What's happening in EPA?" → Runs Phase R with emphasis on local government and news sources
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
- **Supplementary:** Windsor MCP for Instagram, YouTube, Facebook, Search Console, and Apify scraper performance data.
- **Supplementary:** Claude web search for market context, news events, and competitor research.
- **Supplementary:** Chrome browser for MLS data, local government sites, and Google Trends.

## Auto-Render Hand-off (v6.2 — Apr 2026)

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

After a render completes, the same files are available in four places. The renderer (`poll_and_download.py`) writes a `dashboards` block into `{slug}.meta.json` AND emits a `RENDER_RESULT=<json>` line to stdout, so the calendar UI can surface these URLs automatically. If you are hand-running the pipeline, these are the links to check:

| Where | URL | What you see |
|---|---|---|
| Local disk | `outputs/renders/{slug}.mp4` | The MP4 file, ready to upload anywhere |
| HeyGen — this render | `https://app.heygen.com/videos/<video_id>` | Direct video page: preview, shareable link, re-render controls |
| HeyGen — all projects | `https://app.heygen.com/projects` | Full library of past renders |
| ElevenLabs — history | `https://elevenlabs.io/app/speech-synthesis/history` | Every TTS generation with re-download + the SSML used |
| ElevenLabs — Voice Library | `https://elevenlabs.io/app/voice-library` | Graeham voice clone + any other voices in the account |

The `{slug}.meta.json` file always contains the HeyGen `video_id` AND a full `dashboards` object — that `video_id` is the canonical identifier you can search for in the HeyGen dashboard to find any past render. The V6 Production Calendar button reads these URLs straight from the webhook and surfaces them as click-through links in the UI — Graeham should never have to ask "where did my render go?" again.

### Recommended resolution per format

| Format | Resolution | Why |
|---|---|---|
| Reels / Shorts / TikTok (9:16) | 1080p | Instagram/TikTok recompress hard; 720p looks noticeably blurry |
| YouTube Long (16:9) | 1080p | Minimum for YouTube's "HD" badge |
| Listing videos | 4k | Cuts down well for MLS and sold as premium |
| Quick internal tests | 720p | Saves HeyGen credits when iterating |

## Content Distribution Modules

### Newsletter Module
When a topic has been developed into a video script, the content-creation-engine can also generate a newsletter article from the same topic. Read the newsletter-generator skill at `../newsletter-generator/SKILL.md` for the full newsletter workflow.

The newsletter includes a "What's My Home Worth?" CTA button that will (when fully wired) trigger an auto-generated CMA report via the cma-generator skill. This pipeline is documented in the Content Creation Engine Restructure Plan but the auto-CMA trigger is not yet built.

### Blog Post Module (Planned)
Convert newsletter content into a full blog post with SEO metadata. Not yet built.

### Ad Copy Module (Planned)
Generate Facebook/Google ad variants from the same topic. Not yet built.

### Social Posts Module (Planned)
Platform-specific short-form posts (IG caption, FB post, LinkedIn). Not yet built.
