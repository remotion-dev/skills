---
name: content-ideation-engine
description: Data-driven content idea generator for Bay Area Content Engine. Pulls fresh signal from Reddit (and later Zillow reviews + City-Data forums) via Apify, then surfaces the highest-value content opportunities for Graeham Watts' real estate marketing. Use this skill ANY time the user asks "what should I post this week", "find me content ideas", "what are people talking about", "generate a content plan from data", "scrape Reddit for ideas", "run the ideation engine", or any variation of pulling market signal from live sources to feed the video-script-generator. Automatically triggered by the video-script-generator orchestrator when the user is in Mode A (data-driven) rather than Mode B (prompt-driven).
---

# Content Ideation Engine

## Purpose

This skill is the **data-driven half** of the Bay Area Content Engine. Where the main `video-script-generator` can work from a direct prompt ("make me a BOFU video about AB 1482"), this skill answers the harder question: **"what should I even be talking about this week?"**

It does that by pulling live signal from the communities where Graeham's actual and potential clients hang out, then surfacing the top content opportunities ranked by:
1. **Funnel relevance** (is this a BOFU trigger moment, or just noise?)
2. **Local specificity** (EPA/Peninsula mentions beat general Bay Area mentions)
3. **Engagement velocity** (is this thread blowing up or dying?)
4. **Content gap fit** (does it match one of Graeham's 9 pillars?)

## When to trigger this skill

- User says: "what should I post this week", "find me content ideas", "run the ideation engine", "what are people talking about on Reddit", "give me a weekly content plan from data", "what's trending in Bay Area real estate conversations"
- The main `video-script-generator` orchestrator detects Mode A (data-driven) and hands off here
- Any time fresh external signal is needed to fuel content creation

## Required setup (check before running)

1. **`.env` file exists** at the repo root with `APIFY_API_TOKEN` populated
2. **`python-dotenv`** and **`apify-client`** installed (`pip install python-dotenv apify-client --break-system-packages`)
3. **Apify Starter plan active** (or Free with small scrape limits)

If `.env` is missing or the token is blank, halt and tell the user exactly what to fix.

## Workflow

### Step 0: Load topic history and build exclusion list (MANDATORY — run before anything else)

Before reading reference files, scoring, or scraping, load the rolling topic history from `../../references/topic-history.json`. This file contains the last 4 weeks of generated content with titles, angles, pillars, markets, neighborhoods, and GHL keywords.

**Build three exclusion constraints from the history:**

1. **Angle exclusion list** — Extract every `angle` value from the last 2 weeks. These angles are OFF LIMITS for this run. Example: if `pricing-strategy` was used last week, do not generate any topic whose primary angle is pricing strategy. Related angles are fine (e.g., `pricing-strategy` is blocked but `tax-implications-of-selling` is allowed).

2. **Pillar balance scorecard** — Count how many times each of the 9 content pillars appeared in the last 2 weeks. Pillars with 2+ appearances are DEPRIORITIZED (not blocked — just ranked lower). Pillars with 0 appearances in the last 2 weeks get a BOOST in the scoring step.

3. **Market/neighborhood rotation** — Count market appearances in the last 2 weeks. If one market (e.g., EPA) appeared in 3+ of the last 2 weeks' topics, ACTIVELY SEEK content for underserved markets (RWC, PA, MP, SMC) this week. This doesn't mean avoid EPA entirely — it means at least 2 of the top 5 opportunities should target a different market.

**Print the exclusion list in the output** so the user can see what's being avoided and why:

```
FRESHNESS CONSTRAINTS (from topic-history.json):
  Blocked angles (last 2 weeks): pricing-strategy, trigger-event-layoff
  Deprioritized pillars (2+ recent): Pillar 4 (Buyer/Seller Education), Pillar 8 (Trigger Events)
  Boosted pillars (0 recent): Pillar 5 (Development & Local News), Pillar 9 (Investment Analysis)
  Overserved markets: EPA (4 of last 10 topics) — actively seeking RWC/PA/MP content
```

If `topic-history.json` doesn't exist or is empty, skip this step and proceed normally — note "No topic history found, generating without freshness constraints" at the top of the output.

### Step 1: Read all reference files first

Read these in order before doing anything else:

1. `references/apify-actors.md` — actor IDs, pricing, input schemas
2. `references/subreddit-list.md` — the curated subreddit list with tier assignments
3. `references/ideation-rubric.md` — how to score and rank raw posts into content opportunities
4. `references/query-templates.md` — canned search queries for BOFU trigger-event content

### Step 2: Confirm scope with the user

Before spending credits, confirm:
- **Time window:** last 7 days (default), last 30 days, or custom
- **Subreddit tier:** Tier 1 only (5 core, ~$0.75), Tier 1+2 (15 subs, ~$2.50), or full run (20+ subs, ~$5)
- **Include Zillow reviews?** (Phase 2b — only if user explicitly asks)
- **Include City-Data forums?** (Phase 2b — only if user explicitly asks)

Show the user the estimated cost BEFORE running. Never run a scrape that will cost more than $1 without explicit confirmation.

### Step 3: Run the Apify scrape

Call the Apify actor `trudax/reddit-scraper-lite` with this input template:

```json
{
  "startUrls": [
    {"url": "https://www.reddit.com/r/BayArea/hot/"},
    {"url": "https://www.reddit.com/r/bayarearealestate/new/"}
  ],
  "maxItems": 225,
  "maxPostCount": 15,
  "maxComments": 3,
  "sort": "hot",
  "time": "week",
  "proxy": {"useApifyProxy": true}
}
```

Use the Python helper script at `../scripts/run_reddit_ideation.py` to execute the run and save the dataset locally. The script reads the `.env` file, calls the Apify API, polls until the run completes, downloads the dataset as JSON, and writes it to `outputs/ideation-raw-{timestamp}.json`.

### Step 4: Score and rank the raw posts

Load the raw dataset and apply the rubric from `references/ideation-rubric.md`. For each post:
- Tag it with funnel stage (TOFU/MOFU/BOFU) using the `funnel-tagger` sub-skill logic
- Tag it with content pillar (1-9) from the main orchestrator's content-pillars reference
- Score it on the 4 axes (funnel relevance, local specificity, engagement velocity, content gap fit)
- Filter out noise (memes, off-topic, already-saturated topics)

### Step 5: Surface the top 5-10 opportunities

Format output as a ranked list with these fields per opportunity:

```markdown
## Opportunity #1 — [Short descriptive title]

**Source:** r/[subreddit] — [post title] ([URL])
**Funnel stage:** BOFU / MOFU / TOFU
**Content pillar:** #[N] — [Pillar name]
**Why it matters:** [1-2 sentences: what's the signal, why is this a buyer/seller moment]
**Recommended format:** YouTube Long-Form / Reel / Carousel / GBP Post / Blog / Email
**Suggested hook:** "[One-line hook for the video or post]"
**Lead capture keyword:** [SELL / OPTIONS / 1482 / etc. — see lead-capture-keywords.md]
**Estimated effort:** Low / Medium / High
```

### Step 6: Offer next steps

After showing the ranked list, ALWAYS end with:

> **Want me to generate the full content package for any of these? Just say the opportunity number (e.g. "do #1 and #3") and I'll pass them to the video-script-generator for multi-platform packaging.**

This keeps the human in the loop and prevents unnecessary Anthropic API spend on packages the user doesn't actually want.

### Step 7: Save the session artifact

Write the ranked opportunity list to:
`outputs/ideation-ranked-{timestamp}.md`

So the user can review it later or feed it back to the engine without re-scraping.

## Cost safeguards

**Hard rules:**
- NEVER run a scrape that will cost more than $5 without explicit user confirmation
- ALWAYS show estimated cost before running
- DEFAULT to Tier 1 (5 subreddits, ~$0.75) unless user asks for more
- USE `maxItems` to cap the scrape — never omit this parameter
- If a scrape returns >500 items, ABORT and tell the user the cap was hit

## Error handling

- **No Apify token:** Halt, tell user to check `.env`
- **Apify rate-limited:** Wait 60s, retry once, then halt
- **Scraper returns empty:** Could mean Reddit blocked the proxy or the subreddit has no recent posts. Report honestly, don't fabricate data.
- **Dataset too large:** Truncate to top 100 items by upvotes, tell the user

## Integration with the main orchestrator

The main `video-script-generator/SKILL.md` should reference this skill in Mode A. When the user asks "what should I post this week", the orchestrator:
1. Loads this skill
2. Runs the ideation workflow above
3. Receives the ranked opportunity list
4. Waits for the user to pick which ones to package
5. Hands the selected opportunities back to itself for multi-platform content generation

## Future additions (Phase 2b)

- Zillow neighborhood reviews actor integration
- City-Data forums actor integration
- Google Search Console top queries (via Windsor MCP if reliable)
- Instagram/YouTube engagement data (via social-media-analyzer if reliable)
