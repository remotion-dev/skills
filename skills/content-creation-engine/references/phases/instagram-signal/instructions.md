---
name: instagram-signal
description: Instagram competitor + hashtag signal ingestion for content-creation-engine. Calls the standalone instagram-competitor-scraper skill, pulls the top-engagement posts in Graeham's niche from the last 7 days, and writes outputs/instagram-signal-{timestamp}.json. The output feeds into content-calendar's Opportunity Scorer alongside Reddit (Phase 2) and GSC signal. Also pipes results to the Obsidian vault via video-to-obsidian so historical analysis is possible later. Trigger when content-creation-engine's weekly market-signal step runs, or when the user directly asks to "scrape Instagram for content signal," "refresh the Instagram feed," or "pull what's working on IG this week."
---

# Instagram Signal (Phase IG of content-creation-engine)

> **SCOPE CLARIFICATION.** This phase is a **data-ingestion step**, not a scoring or opportunity-ranking step. Its job is to pull the top-engagement Instagram posts from Graeham's niche (Bay Area / Peninsula real estate + EPA-specific community accounts) and hand them to downstream scoring. Per-topic scoring belongs to `content-calendar`. Per-post hook pattern extraction belongs to `cinematic-hooks` (consumes vault output later).

## Purpose

This phase is the **Instagram-signal slice** of the weekly market-data pull. Where `content-ideation-engine` provides Reddit demand signal (what people are asking), this phase provides Instagram performance signal (what's actually working as published content right now).

The combination is powerful: Reddit tells you what people want to know, Instagram tells you what format / hook / angle is currently getting attention. The engine uses both when scoring weekly topic candidates.

## When to trigger

- `content-creation-engine` weekly market-signal pass — runs this in parallel with `content-ideation-engine`
- `content-calendar` needs fresh competitive content data and asks for a refresh
- User directly: "scrape Instagram for content signal", "what's working on Instagram this week", "pull top competitor reels"
- **Do NOT trigger on**: "what should I post this week" (routes to `content-calendar`) or "transcribe this reel" (routes to `video-transcriber` directly)

## Required setup

1. `.env` with `APIFY_API_TOKEN`
2. `python-dotenv` + `apify-client` installed
3. Standalone skills must exist: `instagram-competitor-scraper`, `video-to-obsidian`
4. Obsidian vault folder at `Documents/Obsidian/Instagram Saves/`

If missing, halt and tell the user exactly what to fix.

## Workflow

### Step 1: Load standard targets

Read `Skills/skills/instagram-competitor-scraper/references/standard-targets.md` for the hashtag and handle lists.

If the file has placeholder handles (e.g., `@PLACEHOLDER_1`), halt and ask the user to fill it in before running.

### Step 2: Call the scraper script via the wrapper

```bash
python3 scripts/run_instagram_signal.py --days 7 --top 30 --pipe-to-obsidian
```

Flags: `--days 7` for fresh signal, `--top 30` for scoring layer, `--pipe-to-obsidian` for vault logging, `--output` to override default JSON path.

### Step 3: Hand off to content-calendar

Downstream scoring reads the JSON file. Each post becomes a candidate topic, weighted by engagement rate. Hook pattern + topic tags from the scraper feed into format decisions.

## Cost expectations

Weekly run: ~$0.50 in Apify credits, ~$2/mo. If user requests daily, push back — IG trends move week-over-week.

## Filter axes

The scraper already filters by engagement rate, recency, and URL validity. This phase does NOT re-filter — trusts the output, hands downstream.

## Failure handling

Missing script / token / targets — halt with clear error. 0 results — return empty JSON, downstream handles empty case. Vault pipe fails for one post — continue with others, JSON output still valid.

## Output schema

`outputs/instagram-signal-{timestamp}.json` is a JSON array of post objects. See `Skills/skills/instagram-competitor-scraper/SKILL.md` for full schema. Required fields downstream: url, creator, creator_followers, engagement.engagement_rate, caption, hook_pattern, content_type, discovered_via.
