---
name: transcript-repurposer
description: "Transcript-to-script repurposing engine for Graeham Watts. Takes a downloaded transcript from SurfFast (or any source — Instagram, TikTok, YouTube, podcast, .srt, .vtt, .txt, pasted text) and rebuilds it as a Graeham-voiced, data-backed, multi-platform content package with stronger hooks, real research, and HeyGen + Higgsfield handoff prompts. Use ANY time the user mentions: SurfFast, downloaded transcript, transcribed video, transcript file, repurpose this video, rewrite this Instagram, rewrite this TikTok, rewrite this YouTube, take this script and make it mine, redo this hook, repurpose this transcript, .srt, .vtt, subtitle file, pasted transcript, 'I downloaded this', 'transcribe and rewrite', or hands over text that's clearly a transcript and wants a Graeham-style version. Also trigger when the user uploads a .txt / .srt / .vtt / .mp3 / .mp4 file and asks for a rewritten script. Auto-runs the humanizer skill on the final output. This skill is the CORRECT CHOICE when the input is an EXISTING TRANSCRIPT — do not use video-script-creation-engine (that's for original content from scratch)."
---

# Transcript Repurposer

Take a transcript from anywhere — SurfFast download, manual paste, .srt file, .vtt file, podcast transcript, YouTube auto-captions — and turn it into a Graeham-voiced, data-backed content package with stronger hooks, real research grounding, and production-ready handoff to HeyGen and Higgsfield.

This skill is the **transcript-first cousin** of `video-script-creation-engine`. The Content Engine builds scripts from scratch starting at audience demand research. This skill starts from an existing transcript and rebuilds it — same data/research quality, but skipping the BOFU query generator and Reddit ideation phases because the source video already supplies the topic and angle.

## When this skill fires vs. video-script-creation-engine

| Situation | Use |
|---|---|
| User pastes a transcript or uploads .srt/.vtt/.txt and wants their own version | **This skill** |
| User says "I downloaded this Instagram, rewrite it for me" | **This skill** |
| User says "SurfFast pulled this — make it mine" | **This skill** |
| User says "give me content ideas for this week" | `video-script-creation-engine` |
| User says "write me a script about AB 1482" (no source video) | `video-script-creation-engine` |
| User has a YouTube URL but NO transcript yet | `video-script-creation-engine` (it has its own YouTube transcriber in Phase 0) |

The distinguishing signal: **does the user already have the words?** If yes, this skill. If no, the Content Engine.

## The 7-Phase Pipeline

Run these in order. Don't skip ahead. Each phase has a clear input and output so you can hand off to the next phase cleanly.

### Phase 1 — Ingest the Transcript

**Read:** `references/01-ingest.md` for full input handling.

Accept any of these inputs and normalize to a single clean text block:

- **Pasted text** — strip any quote markers, timestamps, speaker labels
- **`.txt` file** — read as-is
- **`.srt` / `.vtt` subtitle file** — strip timing cues and sequence numbers, keep only spoken text
- **`.json` from SurfFast** — extract the `text` field, ignore metadata unless it tells us the source platform (which we want for context)
- **Audio file (`.mp3`, `.wav`, `.m4a`)** — tell the user we need a transcript first. SurfFast downloads audio but doesn't transcribe; for transcription, point to the Content Engine's `youtube_transcriber.py` Whisper script or have the user paste a transcript.

**Output of Phase 1:** A clean `source_text` string and a one-paragraph `source_metadata` (platform if known, approximate length, any creator/handle visible).

### Phase 2 — Analyze the Source

**Read:** `references/02-analyze.md` for the analysis framework.

Decompose the source transcript along these axes so we know what to keep, what to throw out, and what to upgrade:

1. **Core claim** — In one sentence, what is the video actually saying?
2. **Hook strategy used** — What pattern interrupt did the original creator open with? (See `references/hook-frameworks.md` for the 8 patterns.)
3. **Evidence quality** — Does the source cite data, anecdotes, or just opinion? Flag any specific numbers, dates, or claims that need fact-checking.
4. **Structure** — Hook → setup → payoff → CTA? Or list format? Or story format? Tag the structure.
5. **Target audience signal** — Who is the original creator talking to? First-time buyers? Investors? Renters? General audience?
6. **Length and pace** — Word count, approximate spoken duration, density of ideas per 30 seconds.
7. **Localization need** — Is this topic real-estate adjacent / Bay Area relevant, or universal? This drives Phase 4.

**Output of Phase 2:** A `source_brief` markdown block with all 7 fields filled in.

### Phase 3 — Decide the Repurpose Angle

**Read:** `references/03-angle.md` for the angle-selection logic.

Don't just rewrite the same video. Decide HOW Graeham's version is going to be different and better. Pick ONE of these angles (or hybrid two):

1. **Same claim, better evidence** — Original makes a point, Graeham backs it with real data, dates, and citations.
2. **Contrarian take** — Original says X, Graeham respectfully argues why X is incomplete or wrong with his market expertise.
3. **Local lens** — Original is a universal real estate take, Graeham reframes it for Bay Area / Peninsula specifically.
4. **Deeper expert breakdown** — Original is surface-level, Graeham goes one layer deeper as a working agent.
5. **Personal story wrapper** — Original is informational, Graeham frames it around a real client situation he's seen.

**Output of Phase 3:** A single sentence — `Repurpose Angle: <angle name> — <one-sentence rationale>`.

### Phase 4 — Research & Data Injection (the part the Content Engine has that SurfFast doesn't)

**Read:** `references/04-research.md` for the research playbook.

This is the phase that fixes the problem you flagged. SurfFast's default output gives you the words but none of the substance. This phase injects the data layer.

**If real-estate / Bay Area adjacent:**

- Pull market stats from `video-script-creation-engine/references/market-config.md` if relevant (price ranges, days on market, etc. — date-stamp everything)
- Reference AB 1482 / California-specific rules where applicable, with current year date anchor
- If a specific neighborhood is named, pull the right talking points (zoning, housing stock, commute, walkability — never demographics, see Fair Housing block below)
- If the topic appears in `video-script-creation-engine/references/topic-history.json`, link to or note Graeham's prior coverage

**If universal (non-real-estate):**

- Run web search for current data, statistics, expert sources relevant to the claim
- Verify any numerical claims from the source transcript before repeating them — flag if they're stale or wrong
- Cite sources inline so the script reads as authoritative

**Output of Phase 4:** A `research_pack` markdown block with 3-7 cite-ready facts, each with source and date stamp.

### Phase 5 — Hook Generation (3 Variants + Score)

**Read:** `references/hook-frameworks.md` for the 8 patterns and scoring rubric.

Generate THREE hook variants drawn from different frameworks. Score each on the 4-criteria rubric (Pattern Interrupt, Curiosity Gap, Specificity, Graeham Voice Fit). Recommend the winning hook with a 1-line rationale.

The hook is the single highest-leverage improvement we can make over the source video. Spend real effort here — don't just rephrase the original opener.

**Output of Phase 5:** Three labeled hook variants with scores and a recommendation.

### Phase 6 — Script Writing (Multi-Platform Derivatives)

**Read:** `references/06-script-writing.md` for the script structure templates and the platform spec matrix.

Produce the full content package with these derivatives:

| Format | Specs | What to include |
|---|---|---|
| **YouTube Long** | 8-15 min, 16:9 | Fullest version with inline shot direction tags `[TALKING HEAD]`, `[B-ROLL]`, `[TEXT OVERLAY]`, full editing notes block |
| **YouTube Short** | 30-59 sec, 9:16 | Tightest version — hook, one insight, CTA |
| **IG Reel** | 30-60 sec, 9:16 | Hook-first, face-to-camera friendly, caption-overlay friendly |
| **TikTok** | 30-60 sec, 9:16 | More casual cadence, trending-audio-compatible if relevant |
| **Caption + hashtags** | Per-platform | One caption set tuned to each platform |
| **GHL keyword CTA** | One per script | Use the active keyword set listed below |

**Inline shot direction tags** — embed these directly in the script text the same way the Content Engine does. Don't separate them into their own section. Format examples in `references/06-script-writing.md`.

**Voice & style** — Match Graeham's voice and style guide. Reference `video-script-creation-engine/references/phases/script-writer/references/voice-and-style.md` if available — same voice rules apply.

**Active GHL keywords** — `SELL`, `BUY`, `COSTS`, `OPTIONS`, `1482`, `EPA`, `VALUE`, `READY`, `INVEST`, `NUMBERS`, `RELOCATING`, `MARKET`, `CHECKLIST`, `WATCH`, `RWC`, `PA`, `MP`, `SF`. Format CTA as: "Comment [KEYWORD] below and I'll send you [lead magnet]."

**Output of Phase 6:** Full content package markdown block.

### Phase 7 — Production Handoff (HeyGen + Higgsfield + ElevenLabs)

**Read:** `references/07-handoff.md` for handoff format details.

Produce three production-ready handoff blocks:

**A. HeyGen Avatar Script Block**

Format the script ready to paste into HeyGen. Recommend an avatar look from Graeham's set (see `heygen-video/references/avatars.md`) based on the topic and tone. Note: HeyGen skill requires Graeham to confirm the avatar — list 2-3 recommendations with rationale, don't pick silently.

```
HEYGEN-READY SCRIPT
Recommended look: <look_name> (rationale: <one line>)
Backup look: <look_name> (rationale: <one line>)
Aspect: 9:16 or 16:9 (portrait looks = 9:16, landscape looks = 16:9)
Script:
<paste-ready script with no shot direction tags>
```

**B. Higgsfield B-Roll Prompt Pack**

For every `[B-ROLL: ...]` tag in the script, generate a paired Nano Banana Pro image prompt + Seedance/Kling motion prompt. See `higgsfield-video/SKILL.md` for the Nano Banana realism anchor stack (Gray Malin + Douglas Friedman + Kodak Portra 400 for real estate).

```
B-ROLL #1
Image prompt (Nano Banana Pro): <prompt>
Motion prompt (Seedance 2.0): <motion description>
Duration: 5s | 10s | 15s
Aspect: 9:16 or 16:9
Use in edit: <where this clip lands in the timeline>
```

**C. ElevenLabs SSML Block**

Wrap the script in `<speak>` tags with `<prosody>` and `<break>` markup so Graeham can paste directly into ElevenLabs. Same format as the Content Engine — see `video-script-creation-engine/references/phases/script-writer/references/elevenlabs-audio-tags.md` if it's available, otherwise apply the standard pattern: hook = faster/higher pitch, education = medium, CTA = slower/louder.

**Output of Phase 7:** All three handoff blocks appended to the content package.

### Phase 8 — Humanizer Pass (Auto, Required)

**Read:** `humanizer/SKILL.md` and `references/08-humanizer.md`.

This is the non-negotiable final step. Run the entire generated content package — every hook variant, the chosen script across all platform derivatives, captions, ElevenLabs SSML — through the humanizer's pattern list. The humanizer skill catches the AI-isms that quietly tank engagement: significance inflation, promotional language, AI vocabulary, em dash overuse, rule-of-three, sycophantic openings, generic conclusions.

**How to invoke:** After Phase 7 completes, invoke the `humanizer` skill on the final content package. Provide Graeham's voice-and-style reference (from the Content Engine) as the voice-matching sample so humanizer rewrites toward Graeham's actual cadence, not a generic "natural" voice.

Apply humanizer to:
- Hook variants (yes, before scoring — so we're scoring humanized versions)
- All script bodies (YouTube Long, Short, Reel, TikTok)
- Captions
- Editing notes prose (NOT the bracketed shot tags — those are intentionally structural)

Skip humanizer on:
- ElevenLabs SSML XML (it's machine-readable markup)
- HeyGen-ready script block (already the humanized script, no need to double-pass)
- Higgsfield image/motion prompts (those are technical generation prompts, not human-facing copy)

**Output of Phase 8:** A final, humanized content package saved to `outputs/transcript-repurpose-{slug}-{timestamp}.md`.

## Fair Housing Guardrails (Non-Negotiable)

When the repurposed topic touches real estate, the same Fair Housing rules from the Content Engine apply:

- NEVER describe neighborhoods by demographics (race, religion, national origin, family status, disability)
- NEVER use "safe / good areas / family-friendly / up-and-coming" as demographic proxies
- NEVER rank schools as a primary selling point for a neighborhood
- NEVER promote kickback arrangements with lenders, inspectors, or other vendors

Neighborhood content is limited to: property features, price ranges, market trends, lot sizes, amenities, architecture, housing stock age, HOA structure, zoning, new development, commute/transit facts, walkability.

**Critical for repurposing:** the source video may contain language that violates these rules. Strip it out — don't carry it forward into Graeham's version, even if the source had a similar phrase. Flag any source-video lines you removed so Graeham knows what was filtered and why.

## Date & Year Quality Control

Force every year reference in the output (text overlays, on-screen stats, captions, cite-ready statements) to match the current production year. Never carry a stale year forward from the source transcript without explicit historical framing.

Open every cite-ready / AEO statement with a date anchor: "As of <Month Year>...". Date-stamp every price/market stat. Self-scan the output before emitting and fix any bare-year drift from the source.

## Standard Output Path

Save the final humanized content package as:

```
outputs/transcript-repurpose-{slug}-{YYYYMMDD-HHMM}.md
```

Where `{slug}` is a short kebab-case identifier derived from the topic (e.g., `bay-area-mortgage-rates`, `epa-rent-control`, `first-time-buyer-myths`).

Provide the user a `computer://` link to the final file when delivering.

## Quick-Reference Index

| Reference file | Read when |
|---|---|
| `references/01-ingest.md` | Normalizing any input format |
| `references/02-analyze.md` | Decomposing the source transcript |
| `references/03-angle.md` | Picking the repurpose angle |
| `references/04-research.md` | Injecting data and citations |
| `references/hook-frameworks.md` | Generating and scoring hooks |
| `references/06-script-writing.md` | Writing multi-platform script bodies |
| `references/07-handoff.md` | Building HeyGen + Higgsfield + ElevenLabs handoff blocks |
| `references/08-humanizer.md` | Running the humanizer pass correctly |
| `examples/example-instagram-mortgage.md` | End-to-end worked example |
