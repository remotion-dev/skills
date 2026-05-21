# Content-Creation-Engine Integration Plan

How `instagram-competitor-scraper` plugs into `content-creation-engine` for weekly market signal.

## The big picture

Right now, content-creation-engine pulls signal from:
- Reddit (via `trudax/reddit-scraper-lite`)
- Google Search Console queries
- MLSListings.com market data

This integration adds a fourth signal: **what's actually working on Instagram in your niche this week**. Combined with the others, your weekly content plan stops being guesswork and becomes evidence-based.

## Architecture

```
                       content-creation-engine
                                |
            +-------------------+-------------------+
            |                   |                   |
        Reddit              GSC + MLS         instagram-competitor-scraper
       (existing)           (existing)              (NEW)
                                                       |
                                                       v
                                              [returns ranked posts]
                                                       |
                              +------------------------+----------------+
                              |                                         |
                              v                                         v
                   topic scoring layer                       video-to-obsidian
                  (informs weekly plan)              (logs to vault for future query)
```

**One scraper run, two consumers.** Content engine gets the signal for THIS week's planning. Vault gets the historical record for future cross-referencing.

## How content-creation-engine calls it

The wrapper script `scripts/run_instagram_signal.py` lives in content-creation-engine. It calls this scraper, optionally pipes results to vault, writes JSON output for the engine's scoring layer to consume.

```bash
python3 scripts/run_instagram_signal.py --days 7 --top 30 --pipe-to-obsidian
```

## Recommended schedule

- **Sunday 9 PM:** scraper runs with `--pipe-to-obsidian` (vault gets populated)
- **Monday 6 AM:** content-creation-engine weekly run calls scraper data (already cached) to inform topic scoring
- **Monday morning review:** read the dashboards in `_Dashboards/Recent High-Performers.md` to see what's worth replicating

Use the `scheduled-tasks` tool to wire this up.

## Cost model

| Cadence | Run size | Apify cost/run | Monthly cost |
|---|---|---|---|
| Weekly (recommended) | 3 hashtags, 5 handles, top 30 | ~$0.50 | ~$2.00/mo |
| 2x weekly | Same | $0.50 | ~$4.00/mo |
| Daily | Same | $0.50 | ~$15/mo |

Weekly is the right cadence. Instagram trends move slower than Twitter — checking daily wastes money and creates noise.

## Pattern extraction, not content copying

This integration helps the engine identify what's working — hook patterns, topic angles, format choices, hashtag clusters. It does NOT exist to plagiarize competitor captions verbatim into your scripts.

The right downstream flow:
1. Scraper finds top-performing posts
2. `cinematic-hooks` skill extracts the hook PATTERN (not the words)
3. `content-creation-engine` uses the pattern + your unique angle for your market to write an original script
4. Your output is original work informed by what's working — defensible content strategy

## Future expansions (not Phase 1)

- **TikTok scraper sibling** — same architecture, swap Apify actors. Cross-platform signal.
- **YouTube channel scraper** — for longer-form competitor monitoring.
- **RSS feed integration** — Bay Area city event signals (council meetings, housing policy changes) as a fifth signal alongside scraper data.
- **Competitor handle auto-discovery** — periodically scan top-engagement posts in your hashtags, identify creators who appear repeatedly, suggest adding them to standard-targets.md.

These are deliberately out of scope for the initial build. Walk before running.
