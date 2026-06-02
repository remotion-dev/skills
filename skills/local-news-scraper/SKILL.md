---
name: local-news-scraper
description: Local news scraper for Graeham Watts' Bay Area markets. Pulls news headlines, press releases, and permit/zoning updates from official city websites (cityofepa.org, redwoodcity.org, cityofpaloalto.org, menlopark.gov, smcgov.org) and regional outlets (SF Chronicle, Mercury News, KTVU, Palo Alto Weekly, Daily Post). Use ANY time the user mentions: pull local news, find news stories for this week, scan city websites, news for EPA / RWC / PA / MP, city council approvals, new development permits, press releases, timeliness research, news hook for video, refresh local news feed. Also trigger when a day view or weekly calendar shows "Demo Data" on the Local News card and user wants it live, OR when content-calendar's Timeliness scoring needs fresh input.
---

# Local News Scraper

> **Scope.** Pulls news items relevant to Graeham's Bay Area markets (EPA, RWC, PA, MP, SMC) via WebFetch + RSS where available. Outputs structured JSON for the Opportunity Score's Timeliness criterion to consume. For social distribution it also pulls broader state/national market news (Tier 4) and tags each item with a geo_scope (see the geo-targeting rule).

## Purpose

Weekly content planning requires a news hook for timely topics. Currently the "Local News" research cards show demo data. This skill replaces demo with live news.

## When to trigger

- "pull local news for this week"
- "what happened in EPA / RWC / PA / MP last week?"
- "refresh the news feed for the calendar"
- "any permits or council approvals we should cover?"
- day view shows "Demo Data" on news card and user wants live

## Source list

### Tier 1 — City official sites (highest priority)
- cityofepa.org (Press releases, City Council minutes, Planning Commission agendas)
- redwoodcity.org/city-government (same subpaths)
- cityofpaloalto.org/news
- menlopark.gov
- smcgov.org (County-level)

### Tier 2 — Regional news outlets
- SF Chronicle (sfchronicle.com — search for city names)
- Mercury News (mercurynews.com)
- KTVU (ktvu.com — local segment scrapes)
- Palo Alto Weekly (paloaltoonline.com)
- The Daily Post (padailypost.com)
- Embarcadero Media properties

### Tier 3 — Industry / rates
- Freddie Mac weekly rate survey (freddiemac.com/pmms)
- Mortgage Bankers Association (mba.org)
- Bankrate daily rate feed
- Bay Area Council press releases

### Tier 4 — Broader market (for IG/FB reach — NEW)
Local-only stories (e.g. "East Palo Alto") are too small to earn shares on IG/FB. For social reach, also pull state + national real-estate news that can be framed broadly:
- California: CA Association of Realtors (car.org), LA Times real estate, OC Register real estate, SF Chronicle real estate (statewide angle)
- National: CNBC Real Estate, Realtor.com News, Redfin News, Bankrate, NAR (nar.realtor) — rates, prices, policy, mortgage products, "what $X buys" pieces

## Geo targeting for social distribution (IG / FB)
Tag every item with a `geo_scope` and follow this rule:
- **IG / FB cards + reels:** frame at the BROADEST geo the story honestly supports (local -> Bay Area -> California -> national) UNLESS it's a major metro (SF, NY, LA) that already gets enough volume on its own. A "Bay Area" or "California" frame will out-reach an "East Palo Alto" frame every time.
- **Blog / GMB / email / website:** keep the HYPER-LOCAL frame (local SEO + market authority live here).
- One news item therefore yields two framings: broad (social) + local (owned channels). Pass both to content-creation-engine.

## Workflow

### Step 1: Determine time window

Default: last 7 days. Override via args: `--since 2026-04-10` or `--days 14`.

### Step 2: Pull each Tier 1 source

Use WebFetch to get the press-release page, City Council minutes, Planning Commission agendas. Extract:
- Date
- Headline / action taken
- Brief summary (2-3 sentences)
- Source URL (specific to the item)

### Step 3: Pull Tier 2 where relevant

Search regional outlets for: `{city name} real estate`, `{city name} development`, `{city name} council`, `{city name} safety`. Extract top 5 results per city per source.

### Step 4: Pull Tier 3 rates weekly

Freddie Mac weekly rate (30yr fixed + 15yr fixed, WoW change), MBA application index, Bankrate daily spread.

### Step 5: Filter + deduplicate

- De-dupe by headline similarity (edit distance < 10)
- Filter to items relevant to real estate / housing / development / rates / safety
- Discard political commentary, unrelated crime blotter, sports, etc.

### Step 6: Output

Write to:
```
outputs/local-news-{YYYY-MM-DD}.json
```

Schema:
```json
{
  "pulled_at": "ISO8601",
  "window_start": "2026-04-16",
  "window_end": "2026-04-23",
  "items": [
    {
      "date": "2026-04-17",
      "market": "EPA",
      "geo_scope": "local | regional | state | national",
      "tier": 1,
      "source": "cityofepa.org",
      "category": "press_release | council_approval | permit | market_rate | news",
      "headline": "...",
      "summary": "...",
      "url": "https://...",
      "relevance_tags": ["safety", "home-values", "community-milestone"]
    }
  ]
}
```

### Step 7: Hand-off

Content-calendar's Timeliness scoring reads this file. News items from the last 7 days boost Timeliness to 5; items 7-14 days old get Timeliness 3; older = 1.

Day-view `research-news-*.html` pages read this JSON and populate the news cards live.

## Fair Housing guardrails

When categorizing news:
- DO include: development approvals, rate changes, city council decisions, community milestones, market stats
- DO NOT include: school ranking news, demographic commentary, neighborhood "safety rankings", steering-adjacent content

If an item has Fair Housing risk, flag `"fair_housing_flag": true` in the item object — content-calendar will skip scoring it.

## Errors

- **Site unreachable:** log, skip, continue
- **Parse failure:** capture raw HTML for debugging, skip
- **Rate-limited:** back off, retry once
- **No items found for a source:** empty results acceptable

## Future additions

- RSS feed subscriptions for faster pulls
- Sentiment analysis per item
- Automatic cross-reference to MLS data when news mentions home values
