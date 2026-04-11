---
name: video-script-creation-engine
description: >
  Bay Area / East Palo Alto real estate content + video script engine for
  Graeham Watts (REALTOR, Intero Real Estate, DRE# 02015066). Use this skill
  ANY time the user mentions: video scripts, video ideas, content ideas,
  weekly content, content calendar, YouTube, Reels, Shorts, TikTok, AI avatar
  script, listing video, market update video, BOFU content, TOFU content,
  MOFU content, funnel content, lead gen content, Bay Area real estate
  content, East Palo Alto content, Redwood City content, Palo Alto content,
  Menlo Park content, San Mateo County content, Peninsula content, Reddit
  ideation, Apify scrape, content scoring, content pillars, GHL keyword
  capture, SELL/BUY/COSTS/OPTIONS/1482 comment triggers, AB 1482, relocation
  content, first-time-buyer content, layoff content, seller content, or
  anything related to generating inbound real-estate video/content for
  Graeham's markets. Also trigger when the user uploads MLS data or a new
  listing and wants a content package for it. This is a multi-phase engine
  with five sub-skills (bofu-query-generator, content-ideation-engine,
  bofu-scorer, funnel-tagger, script-writer) wired together by CLAUDE.md.
---

# Video Script Creation Engine

Modular real estate content generation system for Graeham Watts. Turns a
single prompt into a scored, funnel-tagged, multi-platform content package
grounded in live Bay Area buyer/seller questions.

## How to Run This Skill

**Step 1 — Load the orchestrator.** Before doing anything else, read
`CLAUDE.md` at the root of this skill folder. It contains the full project
instructions: market config, inquiry types, the 5-phase workflow, Fair
Housing guardrails, lead capture keyword matrix, and the data source
strategy.

**Step 2 — Load the market config.** Read `references/market-config.md` for
Graeham's agent identity, primary/secondary markets, CRM details, lead
magnets, content pillars, and jurisdiction-specific process terms.

**Step 3 — Run the phased workflow.** The five sub-skills in `skills/` are
phase-locked — use them in order, do not improvise:

1. `skills/bofu-query-generator/SKILL.md` — Phase 1: generate 230+ localized
   BOFU query patterns.
2. `skills/content-ideation-engine/SKILL.md` — Phase 2: live Reddit data via
   `scripts/run_reddit_ideation.py` (Apify residential proxy). Supplement
   with Claude web search and browser deep dives.
3. `skills/bofu-scorer/SKILL.md` — Phase 4: apply the 5-criteria scoring
   framework (inquiry type, Intent Matrix, source confirmation, emotional
   temperature, local relevance).
4. `skills/funnel-tagger/SKILL.md` — tag topics TOFU / MOFU / BOFU. Default
   mix: 40/30/30 unless the user specifies otherwise.
5. `skills/script-writer/SKILL.md` — final phase: multi-platform content
   packages wired to Graeham's GHL comment-keyword lead capture (SELL, BUY,
   COSTS, OPTIONS, 1482, etc.).

**Step 4 — Deliver.** Drop the final content package into the user's
selected folder (or the Cowork outputs folder) and provide computer:// links.

## Key Files

- `CLAUDE.md` — full orchestrator / project instructions (read first)
- `README.md` — project overview and architecture
- `references/market-config.md` — Graeham's market + identity config
- `scripts/run_reddit_ideation.py` — Apify Reddit scraper wrapper
- `skills/` — the five phase sub-skills
- `examples/` — 3 worked examples (BOFU trigger, TOFU lifestyle, AEO legal)

## Data Sources (current state)

- **Primary:** Apify `trudax/reddit-scraper-lite` with residential proxy
  (~$0.30–$2.50 per run depending on tier). Requires `APIFY_API_TOKEN` in
  `.env`.
- **Pending:** Reddit Official API (ticket submitted 2026-04-10, 3–14 day
  approval window). Once approved, PRAW becomes primary and Apify becomes
  fallback.
- **Supplementary:** Claude web search + browser deep dives (Google PAA,
  YouTube comments, Zillow Q&A, City-Data, BiggerPockets).

## Fair Housing Guardrails

NEVER generate topics that describe neighborhoods by demographics, use
"safe" / "good areas" / "family-friendly" proxies, rank schools as a
selling point, or promote kickback arrangements. Neighborhood content is
limited to property features, price ranges, market trends, lot sizes,
amenities, architecture, housing stock age, HOA structure, and new
development. See `CLAUDE.md` for the full compliance section.

## Output Locations

- Raw scrapes → `outputs/ideation-raw-tier-{1,2,3}-{timestamp}.json`
- Scored/tagged topics → `outputs/scored-topics-{timestamp}.json`
- Final content packages → `outputs/content-package-{timestamp}.md`

## Example Prompts

- "Give me this week's content — focus on lead gen for East Palo Alto sellers."
- "Generate 5 BOFU videos about AB 1482 for Bay Area landlords."
- "What should I post this week based on what's trending in Redwood City?"
- "I just got a new listing in Menlo Park at $2.1M — give me the full content package."
- "Make me a TOFU reel about East Palo Alto."
