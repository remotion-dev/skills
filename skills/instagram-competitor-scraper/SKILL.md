---
name: instagram-competitor-scraper
description: "Instagram competitive intelligence scraper for Graeham Watts. Pulls top-engagement posts by hashtag and by competitor handle via Apify, returns ranked metadata (URL, creator, views, likes, comments, engagement rate, caption, post date). Standalone callable, also called by content-creation-engine for weekly market signal, and by video-to-obsidian for vault logging. Use this skill ANY time the user mentions: scrape Instagram, competitor analysis, top performing posts, what's working on Instagram, find viral reels, hashtag scrape, competitor monitoring, IG market signal, content benchmarking, what are competitors posting, find me the top reels for [hashtag], who's crushing it in my niche, build a swipe file, defensible content strategy, find replicable content, or any time they want to see top-engagement Instagram content in a niche. Always preserves the source URL in every result — non-negotiable, because Instagram is a visual medium and the user needs to click back to see the actual treatment."
---

# Instagram Competitor Scraper

> **One job:** find the top-engagement Instagram posts in your niche right now and return clean metadata. Optionally pipe results into `video-to-obsidian` to log them to the vault.

## Why this exists

Most realtors fly blind on what's actually working in their market. This skill produces a weekly signal of what's crushing it in Bay Area / Peninsula real estate (or any niche you point it at), so content planning becomes evidence-based instead of vibes-based.

It's the missing piece between "watch competitors manually" (slow, biased toward what you remember) and "guess at content angles" (most agents' default).

## Who calls this

1. **Graeham directly** — "scrape Instagram for top real-estate reels this week"
2. **`content-creation-engine`** — weekly market-signal phase, alongside Reddit, GSC, RSS
3. **`video-to-obsidian`** — when results need to be logged with transcripts into the Obsidian vault

## How to invoke

Simplest form — just say what you want:

```
scrape top reels for #bayarearealestate this week
who's crushing it on @some_competitor right now
find me the top 20 real estate hooks in the Peninsula
```

CLI form for scripts:

```bash
python3 scripts/scrape.py --hashtags bayarearealestate,peninsulahomes --handles competitor1,competitor2 --top 20 --days 30
python3 scripts/scrape.py --hashtags bayarearealestate --top 25 --json --save
python3 scripts/scrape.py --handles competitor1 --top 50 --pipe-to-obsidian
```

## What it does

1. **Reads `APIFY_API_TOKEN`** from `Documents/Claude/Skills/.env`
2. **Calls Apify** via the unified `apify/instagram-scraper` actor for both hashtags and profiles
3. **Filters** to posts within the time window (default 30 days)
4. **Sorts by engagement rate** (likes + comments) / views — fairer than raw views because it doesn't punish small accounts
5. **Returns top N** with all metadata preserved
6. **Optional:** pipes each result through `video-to-obsidian` to log to vault with transcript

## Output schema (per post)

```json
{
  "url": "https://www.instagram.com/reel/ABC123/",
  "creator": "@username",
  "creator_followers": 12500,
  "post_type": "reel",
  "post_date": "2026-05-12",
  "caption": "First 500 chars of caption...",
  "duration_sec": 47,
  "engagement": {
    "views": 184000,
    "likes": 12400,
    "comments": 387,
    "saves": null,
    "engagement_rate": 6.94
  },
  "discovered_via": "hashtag:bayarearealestate"
}
```

**The `url` field is required and never null.** If a result comes back from Apify without a URL, the scraper drops it rather than logging an unreachable note. Visual content without a clickable source is dead data.

## Cost model

| Run size | Hashtags | Handles | Posts pulled | Apify cost |
|---|---|---|---|---|
| Test | 1 | 1 | ~50 | ~$0.10 |
| Weekly standard | 3 | 5 | ~250 | ~$0.50 |
| Full sweep | 8 | 15 | ~800 | ~$1.50 |

Pricing is the Apify standard for Instagram actors. Cheap. The expensive part is video transcription when piping to vault, and that's local Whisper = free.

## Integration with `content-creation-engine`

When the engine runs its weekly market-signal phase, it calls this skill with the standard Bay Area / Peninsula hashtag and handle list (kept in `references/standard-targets.md`). Results feed into the topic-scoring layer alongside Reddit demand signals and GSC query trends.

See `references/content-engine-integration.md` for the full integration plan.

## Integration with `video-to-obsidian`

When `--pipe-to-obsidian` is set, the scraper hands each post to `video-to-obsidian`, which:
- Transcribes the video
- Auto-categorizes content type + hook pattern
- Writes a note to the right folder in `Obsidian/Instagram Saves/`
- Preserves the source URL in frontmatter

This lets one weekly run both feed the content engine AND build up the swipe file vault. Same data, two consumers.

## Pattern extraction, not content copying

This skill helps you study what's working — hook patterns, topic angles, format choices. It does NOT exist to rewrite competitor captions verbatim. Pattern extraction is defensible content strategy. Verbatim rewriting invites copyright issues and dilutes your brand voice. The `cinematic-hooks` skill is the right tool to consume scraper output for pattern analysis.

## Failure handling

| Failure | What the skill does |
|---|---|
| `APIFY_API_TOKEN` missing | Errors immediately with the path to `.env` |
| Actor returns 0 results for a hashtag | Logs a warning, continues with other targets |
| Rate limit hit | Backs off 60 sec, retries once |
| Result missing `url` field | Drops it, logs to stderr (don't write unreachable notes) |
| Network failure | Retries once with 10-sec backoff, then reports |

## What this skill does NOT do

- It does not log in to Instagram (no auth credentials touched)
- It does not access your own saves (that's a separate Chrome-based skill — saves require authenticated session)
- It does not transcribe videos (that's `video-transcriber`)
- It does not write to Obsidian by itself (that's `video-to-obsidian`)

One job, called by others. That's the design.

## Standard targets (Bay Area)

Default list lives in `references/standard-targets.md`. Edit it to evolve your scrape scope without touching the script.

## Maintenance

If Apify changes actor IDs or input schemas, update the `SCRAPER_ACTOR` constant in `scripts/scrape.py`. The skill description and CLI surface stay the same.
