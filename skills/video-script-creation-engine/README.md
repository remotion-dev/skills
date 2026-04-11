# Video Script Generator — Bay Area & East Palo Alto Real Estate Content Engine

A modular real estate content generation system for **Graeham Watts** (REALTOR®, Intero Real Estate, DRE# 02015066). Primary market is the Bay Area Peninsula — East Palo Alto (home base), Redwood City, Palo Alto, Menlo Park, San Mateo County — with expansion into any specific sub-market Graeham targets.

Built as a set of cooperating Claude skills that turn a single prompt into a complete, multi-platform, funnel-tagged content package grounded in real buyer/seller questions scraped from live sources.

**Status (2026-04-10):**
- Phase 1 (foundation + orchestrator + 5 sub-skills): Complete
- Phase 2 (live Reddit ideation via Apify residential proxy): Working
- Phase 2b (Reddit Official API): Support ticket submitted 2026-04-10, awaiting approval
- Phase 2c (Zillow + City-Data scrapers): Planned
- Phase 3 (polish + GitHub push): Planned

---

## What This Does

You (or your assistant) type one prompt. The engine:

1. Generates 230+ localized BOFU search queries for Graeham's markets
2. Pulls live data from Bay Area real estate subreddits via Apify (residential proxy, ~85–95% reliability)
3. Optionally supplements with Claude's web search + browser deep dives (Google PAA, YouTube comments, Zillow Q&A)
4. Scores every topic against the 5-criteria framework (inquiry type, Intent Matrix, source confirmation, emotional temperature, local relevance)
5. Tags each topic by funnel stage (TOFU / MOFU / BOFU — default 40/30/30 mix)
6. Writes full multi-platform content packages — YouTube long-form, Reels, Shorts, TikTok, carousels, Facebook, Google Business Profile, blog, email snippets, AI avatar scripts — wired to Graeham's GHL comment-keyword lead capture (SELL, BUY, COSTS, OPTIONS, 1482, etc.)

**Example prompts:**

- *"Give me this week's content — focus on lead gen for East Palo Alto sellers."*
- *"Generate 5 BOFU videos about AB 1482 for Bay Area landlords."*
- *"What should I post this week based on what's trending in Redwood City?"*
- *"Make me a TOFU reel about East Palo Alto."*
- *"I just got a new listing in Menlo Park at $2.1M — give me the full content package."*

---

## Architecture

```
video-script-creation-engine-download/
├── CLAUDE.md                         ← Orchestrator / project instructions
├── README.md                         ← You are here
├── .env                              ← APIFY_API_TOKEN (gitignored)
├── .env.template                     ← Template for .env
├── .gitignore                        ← Protects .env and credentials
├── PUSH-TO-GITHUB.md                 ← One-time GitHub push instructions
│
├── references/
│   └── market-config.md              ← Graeham's agent identity, markets, CRM, lead magnets
│
├── scripts/
│   └── run_reddit_ideation.py        ← Apify Reddit scraper wrapper (residential proxy default)
│
├── skills/
│   ├── bofu-query-generator/         ← Phase 1: 230+ localized query patterns
│   ├── content-ideation-engine/      ← Phase 2: live Reddit data via Apify
│   ├── bofu-scorer/                  ← Phase 4: 5-criteria scoring framework
│   ├── funnel-tagger/                ← Phase 5: TOFU/MOFU/BOFU classification
│   └── script-writer/                ← Phase 6: multi-platform content packages
│
├── examples/                         ← 3 worked examples (BOFU, TOFU, AEO)
└── outputs/                          ← Scraped datasets + run logs (gitignored)
```

---

## Data Source Strategy

**Source A — Apify Reddit Scraper (primary, working today)**
Uses `trudax/reddit-scraper-lite` with RESIDENTIAL proxy group. ~$0.30–$1.00 per scrape depending on tier and bandwidth. Reliability ~85–95% first try, higher with built-in retries.

- Tier 1: 5 core subs (~$0.30, ~75 items)
- Tier 2: +10 Peninsula city subs (~$0.77, ~225 items)
- Tier 3: +6 South Bay subs (~$1.36, ~400 items)
- Templates: `layoff`, `first-time-buyer`, `ab1482`, `relocation`, `life-events`, `investment`, `market-timing`

**Source B — Reddit Official API (pending)**
Support ticket submitted 2026-04-10 (Reddit account `Maverickgk`, app type "script", under graehamwatts@gmail.com). Realistic approval window is 3–14 days. Once approved, PRAW becomes the primary data path (free, reliable, no 403s) and Apify becomes the fallback.

**Source C — Claude Web Search + Browser Deep Dives (supplementary)**
Google PAA, autocomplete, YouTube comments, Zillow Q&A, City-Data, BiggerPockets. Supplements Reddit — does not replace it.

---

## Quick Start

1. Drop your Apify token into `.env` (copy from `.env.template`)
2. Install deps:
   ```
   pip install python-dotenv apify-client --break-system-packages
   ```
3. Dry-run first (no cost, confirms config):
   ```
   python scripts\run_reddit_ideation.py --tier 1 --dry-run
   ```
4. Live Tier 1 scrape:
   ```
   python scripts\run_reddit_ideation.py --tier 1
   ```
5. Feed the resulting `outputs/ideation-raw-tier-1-*.json` into Claude with a prompt like *"Score these topics with the bofu-scorer skill and give me 7 ranked video ideas."*

---

## Fair Housing Guardrails

This engine enforces Fair Housing Act, RESPA, and Realtor Code of Ethics compliance at every phase. It will NEVER generate topics that describe neighborhoods by demographics, use "safe neighborhoods" / "good areas" / "family-friendly" or similar proxies, rank school quality as a selling point, or promote kickback arrangements.

Neighborhood content is limited to property features, price ranges, market trends, lot sizes, proximity to amenities, architectural styles, age of stock, HOA structures, and new development.

---

## Costs

| Action | Cost |
|---|---|
| Apify Tier 1 scrape | ~$0.30–$0.80 |
| Apify Tier 2 scrape | ~$0.77–$1.50 |
| Apify Tier 3 scrape | ~$1.36–$2.50 |
| Reddit Official API | Free (once approved) |
| Claude web search | Included |

---

## What This System Does NOT Do

- Post content to any platform (you publish manually or via a separate scheduler)
- Track post-publish performance metrics
- Replace keyword research tools — it adds intent-layer intelligence on top
- Claim 100% scraping reliability (web scraping never is; that's why the Reddit API fallback is queued up)
