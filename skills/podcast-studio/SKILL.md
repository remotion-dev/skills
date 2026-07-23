---
name: podcast-studio
description: >
  Graeham Watts's personal podcast factory — produces the gym MP3s he listens to. A LIVING
  skill: it houses multiple named "shows," each with its own production spec, and grows as he
  adds new ones. Two-host NotebookLM-style dialogue (Brian + Matilda) by default, XML/SSML
  scripts for correct pacing/emphasis, rendered on ElevenLabs and delivered into his iTunes
  library. Use ANY time Graeham says: make a podcast, new episode, the podcast skill, podcast
  studio, Know Your Enemy, Competitor Radar, Weekly Market Brief, Pitch Gym, another episode of
  X, redo an episode, add a new show/podcast, or references any show listed in the SHOW REGISTRY
  below. Also trigger on: "generate this as a podcast", "make it audio", "put this on my iTunes".
---

# Podcast Studio — Graeham's gym-podcast factory

One skill, many shows. Each show is a named, repeatable format with its own rules. This file is
the source of truth and is meant to be edited: add a show, tweak a show, retire a show. Treat it
like a living organism — when something new comes up, alter the relevant show or add a new one.

## GLOBAL HARD RULES (apply to every show, no exceptions)

1. **Format = two-host dialogue** unless a show says otherwise. `A:` = Brian (lead explainer,
   grounded). `B:` = Matilda (sharp co-host, asks Graeham's question, clarifies, summarizes).
   Equals who both know the material — not interviewer/guest. Turns 1-4 sentences, strict
   alternation, `PAUSE` on its own line for a section beat.
2. **Concise, no fluff.** Graeham's calibrated note: past audio sounded "too automated / fake."
   Every concept explained once, cleanly, in spoken English (contractions, short sentences).
   No essay voice, no signposting, no rule-of-three padding. Detail-dense is good; padding is not.
3. **Humanizer pass is mandatory** on every finished script — load the `humanizer` skill and run
   it before rendering. No em dashes anywhere. Concreteness (real names, real numbers, real
   quotes) is what makes it sound real — favor specifics over generic phrasing.
4. **Research shows crawl FRESH every time.** Any show marked `research: fresh` below must pull
   live data at production time — load WebSearch/WebFetch via ToolSearch and use the
   `website-crawler` skill. NEVER script a research show from training memory or a prior run's
   findings. Cite sources; mark anything unverifiable as UNVERIFIED; never fabricate a number.
5. **Check the ElevenLabs quota before generating** and tell Graeham the number. Cost ≈ 1
   character per character of spoken text; a ~40-min episode ≈ 35-40k chars. If the batch exceeds
   the remaining quota, report it and either batch across the reset date or wait for his go.
   Key: `Documents\Skills LLMS\Claude\.heygen-credentials\elevenlabs-key.txt`. Quota check:
   GET `https://api.elevenlabs.io/v1/user/subscription` with header `xi-api-key`.
6. **Delivery is not done until it's on the phone.** The render engine writes MP3s to
   `C:\Users\Graeham Watts\Music\<Album>\` as `NN - Title.mp3` and does NOTHING else — iTunes
   ingestion is a DELIBERATE step, never auto-add. **Do NOT copy renders into the "Automatically
   Add to iTunes" folder** — for a RE-RENDER it creates a duplicate library entry (iTunes imports
   the auto-add copy into iTunes Media\Music as a second entry alongside the original). Instead:
   - **New album:** in iTunes, File > Add Folder to Library → `Music\<Album>\` (one time). Build its playlist.
   - **Re-render (replacing existing tracks):** overwriting the file in place already updates the
     existing library entry's audio — do nothing in iTunes except confirm no dupes.
   - If dupes ever appear, clean them with iTunes **File > Library > Show Duplicate Items** (check
     the file path via Get Info before deleting — keep the entry pointing at `Music\<Album>\`).
   Then (a) verify the audio itself (pitch check — Brian ~85-130 Hz, Matilda ~170-235 Hz — never
   trust metadata alone); (b) tell Graeham to plug in and sync. Replacing files on disk does NOT
   update his iPhone until a USB sync runs. See [[gym-podcast-preferences]].

## PRODUCTION PIPELINE

- **Voices:** Brian `nPczCjzI2devNBz1zQrb` (A), Matilda `XrExE9yKIg1WjnnlVkGX` (B),
  model `eleven_multilingual_v2`, stability 0.5, style 0.2, speaker-boost on, Brian speed 0.94 /
  Matilda 0.96.
- **Script format:** `scripts/dialogue-format.md` — one `A:`/`B:`/`PAUSE` per line. SSML/XML
  `<break time="0.6s"/>` tags are honored by ElevenLabs for deterministic pauses; `<prosody>` is
  accepted but NOT truly applied (see heygen-elevenlabs-renderer notes) so rely on `<break>` +
  wording for pacing, not prosody. Use bracket audio tags sparingly ([laughs] etc.) only if a
  show calls for it.
- **Render engine:** `scripts/synth_dialogue.py <script.txt> <album> <track#> "<title>"` —
  per-turn TTS (parallelized), 0.3s gaps between turns, 0.95s at PAUSE, ffmpeg concat, ID3 album
  tags, auto-copy into the iTunes auto-add folder. Renders are cached per-turn so re-runs are cheap.
- **Scripts live in the vault** so they persist and can be re-rendered/tweaked:
  `Documents\Obsidian\<Show>\` or the show's own folder as noted per show.

## SHOW REGISTRY

Each show: purpose · format · cadence · length · source · special rules · status.

### 1. The Owner's Manual — STATUS: DONE (10 eps)
Graeham's personality-assessment operating manual. Two-host. Source: `Documents\Personality Tests`.
Album `The Owner's Manual`. One-off series; complete.

### 2. PropIQ Academy — STATUS: DONE (62 eps)
Founder/AI/SaaS course + the "How to Explain PropertyIQ to Anyone" pitch episode. Two-host.
Source: `Documents\Obsidian\PropertyIQ Academy\Audio Scripts v2\`. Album `PropIQ Academy`.
Owned jointly with the `founder-academy` skill (that skill teaches; this one produces audio).

### 3. Know Your Enemy — STATUS: IN PRODUCTION · research: fresh
Competitor deep-dive series so Graeham can mine competitors (the Bill Gates move), guard against
the founder-in-love-with-the-idea blind spot, and know the landscape cold. Two-host, LONG
(30-45 min/episode — he's at the gym 90 min/day, longer is better). Album `Know Your Enemy`.
Planned episodes: (1) The Map — the whole landscape + the one thing none of them have (the
outcome graph); (2) The Legacy All-in-Ones (Lofty, BoldTrail/kvCORE, BoomTown); (3) Follow Up
Boss + Zillow; (4) Sierra & Viktor and the enterprise-agent frontier — what to steal for
Wattson/Chevy; (5) GoHighLevel — the engine he rents; (6) The AI Theater (Serhant, Luxury
Presence, "AI for AI's sake"); (7) The Scorecard — honest win/lose per player + build-first list.
Source of truth: `Documents\PropIQ\PropIQ\Competitor Research\` (research agents write here).
RULE: re-crawl before scripting; every claim sourced.

### 4. Competitor Radar — STATUS: PLANNED · recurring monthly · research: fresh
Standalone recurring show (separate from Know Your Enemy): what changed this month — launches,
funding rounds, CEO moves, new AI features across the tracked players. Two-host. Length: as long
as the month's news warrants (no artificial cap; longer is fine). Album `Competitor Radar`.
RULE: fresh crawl/search every run, date-stamped, sourced; diff against last month's file.

### 5. Weekly Market Brief — STATUS: PROPOSED · recurring weekly · research: fresh
10-20 min Monday brief from live data (rates, Bay Area / Peninsula / EPA stats, what's moving)
and what it means for the farm + active deals. Two-host. Album `Market Brief`. Can run as a
scheduled task. RULE: fresh data pull each week.

### 6. The Pitch Gym — STATUS: PROPOSED
Drill series that rehearses the pitches from PropIQ Academy ep 00. Matilda plays the hostile
room (investor / engineer / "can't Zillow build this"); Brian models the strong answer. Rehearsal
disguised as a podcast. Two-host. Album `Pitch Gym`.

### 7. The Machine (Technical Architecture) — STATUS: PROPOSED · source: doc audit
Explains PropertyIQ's actual stack (Temporal, Postgres, DigitalOcean, Supabase, model routing,
the Event Ledger) in listenable plain English — NOT a dry glossary; the terms get woven into a
narrated tour ("follow one lead through the machine"). Two-host. Album `The Machine`. Source:
`Documents\PropIQ\PropIQ\PropIQ Audit Reports\technical-architecture-audit-*.md`.
RULE: ground every technical claim in HIS docs, not generic knowledge; correct misconceptions.

## ADDING OR TWEAKING A SHOW
Append a new numbered entry to the SHOW REGISTRY with the same fields. If a show's rules change,
edit its entry in place. Keep the GLOBAL HARD RULES intact. When Graeham says "this came up, we
need a podcast on X" — add the show here first, then produce it.

## RELATED
[[gym-podcast-preferences]] (voice/format/delivery memory + the iPhone-sync gotcha) ·
`humanizer` skill (mandatory pass) · `website-crawler` skill (fresh research) ·
`founder-academy` skill (co-owns PropIQ Academy) · `heygen-elevenlabs-renderer` (SSML notes).
