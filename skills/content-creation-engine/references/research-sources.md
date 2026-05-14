# Research Sources â Per-Topic Phase R

> **SCOPE CLARIFICATION (April 2026).** Phase R runs **per-topic**, AFTER a topic has been selected (either from `content-calendar`'s weekly Opportunity Score or directly by Graeham). This document describes the data sources Phase R pulls for ONE topic. It is NOT a weekly multi-topic scoring framework â weekly ranking lives in `content-calendar` with its 25-pt Opportunity Score.

> **Integration details live in `../../shared-references/integrations.md`** (the canonical integration matrix for ALL skills, not just this engine). That file documents every connector, account, auth path, the Windsor + Direct parallel-pull rule, pending integrations (Reddit official API, county records), and per-skill integration ownership. Read it before troubleshooting any integration issue.

This document defines every data source the Content Creation Engine taps during Phase R (Per-Topic Research & Discover). Each source includes: what to pull, how to pull it, what to look for, and how findings feed into the per-topic research JSON (`outputs/research-{topic-slug}-{ts}.json`).

---

## 1. MLS Market Stats

**What:** Latest market statistics for Graeham's primary markets.
**Markets:** East Palo Alto, Redwood City, Palo Alto, Menlo Park, San Mateo County, Santa Clara County.
**Key Metrics:**
- Median sale price (MoM and YoY change)
- Days on market (DOM)
- Sale-to-list price ratio
- Active inventory count
- New listings this week
- Pending sales
- Months of supply

**How to pull:**
- Via Chrome: Log into MLSListings.com â Market Statistics â Select each market area
- Pull current month stats + prior month + same month last year for trend analysis

**What to look for:**
- Any metric that moved â¥5% MoM or â¥10% YoY â that's a content trigger
- Inventory spikes or drops (signals shifting market conditions)
- Sale-to-list ratio above 100% (bidding wars) or below 95% (price reductions)
- DOM changes â getting faster = hot market, slower = cooling

**Emoji:** ð

---

## 2. Google Search Console

**What:** What people are actually searching to find Graeham's website.
**How to pull:**
- Via Windsor MCP: `get_data` with connector `searchconsole`, account_id `sc-domain:graehamwatts.com`
- Pull: top queries by clicks AND impressions, last 7 days
- Compare to prior 7-day period to identify rising queries

**What to look for:**
- Rising queries (impressions up â¥20% week-over-week) â people want this content
- High-impression / low-click queries â Graeham ranks but the content isn't compelling enough (rewrite opportunity)
- New queries that weren't appearing before â emerging demand
- Location-specific queries ("homes for sale in [city]", "[city] real estate market")

**Emoji:** ð

---

## 3. Local Government (City of East Palo Alto)

**What:** City council actions, development projects, zoning changes, permits â anything that affects property values or neighborhood character.

**How to pull:**
- Via Chrome: Navigate to https://www.cityofepa.org
  - City Council agendas and minutes
  - Planning Commission agendas
  - Building permit applications
- Also check: https://www.cityofepa.org/communitydevelopment for active development projects

**What to look for:**
- Upcoming city council votes on development/zoning
- New building permit applications (especially multi-unit or commercial)
- Infrastructure projects (roads, parks, utilities)
- Rent control / tenant protection discussions
- Environmental or flood zone changes
- Annexation or boundary discussions
- Community development grants or programs

**Emoji:** ðï¸

---

## 4. Web Research (News & Market Context)

**What:** Recent news, market reports, and expert commentary relevant to Graeham's markets.

**How to pull:**
- Via web search, run these queries (limit to last 7 days where possible):
  1. "East Palo Alto news"
  2. "East Palo Alto development"
  3. "San Mateo County real estate news"
  4. "Bay Area housing market [current month] [current year]"
  5. "California housing market [current month] [current year]"
  6. "Peninsula real estate [current month] [current year]"

**What to look for:**
- Breaking news affecting local property values
- Tech company expansions or layoffs (direct buyer/seller impact)
- Interest rate changes or mortgage market shifts
- New legislation (state or local) affecting real estate
- Infrastructure or transit announcements
- School district changes
- Major employer moves (Meta, Google, Stanford, etc.)

**Emoji:** ð°

---

## 5. Social Performance Data

**What:** Which of Graeham's recent posts performed best â and what patterns emerge.

**How to pull:**
- Via Windsor MCP: Pull Instagram and Facebook post performance data
  - Metrics: reach, impressions, engagement rate, saves, shares, comments
  - Timeframe: last 30 days
  - Sort by engagement rate descending

**What to look for:**
- Content types that consistently outperform (talking head vs. B-roll vs. carousel vs. text overlay)
- Topics that got unusually high engagement (signals audience interest)
- Posts with high saves (signals high-value content worth repeating)
- Posts with high shares (signals viral potential in that topic)
- Comment sentiment â what questions are people asking?
- Time-of-day and day-of-week patterns

**Emoji:** ð±

---

## 6. Google Trends

**What:** Search interest trends for real estate terms in Graeham's markets.

**How to pull:**
- Via web search, check trends.google.com interest data for:
  1. "East Palo Alto real estate"
  2. "Bay Area home prices"
  3. "California housing market"
  4. "[city] homes for sale" for each primary market
  5. Any trending real estate terms nationally

**What to look for:**
- Spikes in search interest (breakout topics = content opportunities)
- Seasonal patterns approaching (spring buying season, tax season, etc.)
- Declining interest in previously hot topics (stop creating that content)
- Comparison between markets (which city is getting more search attention?)

**Emoji:** ð

---

## 7. BOFU Keyword Data

**What:** Bottom-of-funnel keywords from the content engine's existing keyword database.

**How to pull:**
- Read `references/phases/bofu-query-generator.md` for the full keyword matrix (absorbed into content-creation-engine May 2026)
- Cross-reference with Search Console data to see which BOFU terms are actually driving traffic
- Check `references/topic-history.json` for recently covered BOFU topics (avoid repeats)

**What to look for:**
- High-intent keywords not yet covered by existing content
- BOFU keywords with rising Search Console impressions (demand growing)
- Keywords aligned with current market conditions (e.g., "sell my house fast in EPA" during a hot market)
- Seasonal BOFU terms (tax implications content in Q1, school-district content in spring)

**Emoji:** ð¯

---

## 8. Competitor Analysis (Apify Scrapers)

**What:** What competing agents and real estate creators are posting about.

**How to pull:**
- Via Windsor MCP or Apify: Pull latest scraper datasets for competitor content
- Monitor competitors' YouTube channels, Instagram accounts, and blogs
- See `references/phases/content-ideation-engine/references/apify-actors.md` for actor config

**What to look for:**
- Topics competitors are covering that Graeham hasn't touched
- Content formats competitors are using that perform well
- Gaps in competitor coverage (topics no one is covering = opportunity)
- Competitor content that got high engagement (validate topic demand)
- Competitor mistakes or misinformation (opportunity for authoritative correction)

**Emoji:** ðµï¸

---

## 9. YouTube Channel Enumeration & Shorts (Composio YouTube Data API)

**What:** Direct enumeration of any YouTube channel's full upload history â including Shorts â via the Composio YouTube Data API connector. This is the canonical way to close the YouTube Shorts blind spot left by the Apify YouTube scraper (which does NOT capture Shorts), and to pull live competitor stats without going through Windsor.

**When to use this source:**
- Topic-matched competitor video research â find every Short a competitor posted on the topic.
- Channel-level audit of Graeham's own Shorts performance (cross-channel comparison to long-form).
- Generating URL lists for `yt-dlp` bulk download (clip harvest, transcript prep, B-roll mining).
- As a parallel pull alongside section 8 (Apify-driven competitor analysis) â Apify gives long-form, this gives Shorts.

**How to pull (3-step pattern):**

1. **Resolve channel â uploads playlist ID.** Every YouTube channel has an auto-generated uploads playlist whose ID is the channel ID with `UC` â `UU`. Graeham's channel `UCFHqB0L2C4aJVksMKkg_ukw` â uploads playlist `UUFHqB0L2C4aJVksMKkg_ukw`. If you only have a handle, resolve via `YOUTUBE_GET_CHANNEL_ID_BY_HANDLE`.

2. **Walk the uploads playlist.** Paginate `YOUTUBE_LIST_PLAYLIST_ITEMS` (max 50/page) until `nextPageToken` is absent. Collect `items[].snippet.resourceId.videoId`. Dedupe.

3. **Batch-fetch stats + duration.** Chunk video IDs into 50-id batches and call `YOUTUBE_GET_VIDEO_DETAILS_BATCH` with `parts: ["snippet","statistics","contentDetails"]`. The response gives view / like / comment counts and an ISO-8601 duration like `PT45S`, `PT2M13S`.

**Shorts detection logic.** A YouTube video is a Short if its duration is â¤ 60 seconds. Parse the ISO-8601 duration:

```python
import re

def iso8601_to_seconds(s: str) -> int:
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s or "PT0S")
    if not m:
        return 0
    h, mn, sec = (int(g) if g else 0 for g in m.groups())
    return h * 3600 + mn * 60 + sec

shorts = [v for v in videos
          if iso8601_to_seconds(v["contentDetails"]["duration"]) <= 60]
```

Canonical Short URL: `https://www.youtube.com/shorts/{videoId}` â same underlying video, different surface.

**Composio accounts (verified 2026-05-13):**
- Graeham's channel: `youtube_manor-maki` (alias `graehamwatts-active`), channel ID `UCFHqB0L2C4aJVksMKkg_ukw`, handle `@graehamwatts`. Active connection.
- Competitor channels: resolved per-pull via `YOUTUBE_GET_CHANNEL_ID_BY_HANDLE`. Public reads, no extra connection required.

**What to look for:**
- Shorts that broke 10K views on a competitor channel â the topic hit, replicate the angle.
- Competitor Shorts clusters â three or more Shorts on the same topic from one creator signals demand.
- Graeham's underperforming Shorts (views < median Ã 0.3) â kill that format/angle next cycle.
- Recently-published Shorts (< 7 days) covering topics on this week's calendar â speed-to-publish opportunity.

**Bulk download for B-roll harvest (when you need the MP4, not just the metadata):**

| Tier | Method | Cost | When to use |
|---|---|---|---|
| Primary | `yt-dlp` driven from the URL list this section produces | Free | Default. Supports `--download-sections` for clipped extracts. Scriptable from n8n / Python. |
| Fallback | SurFast Video Downloader (desktop GUI, batch up to 50 URLs) | One-time license | When yt-dlp is blocked/rate-limited, or restricted-source content. Manual handoff â agent prepares URL list, user pastes into SurFast and clicks Start; downloads land in `~/Documents/SurFast/` for the agent to read. |

**Cost & quotas:** Free â public YouTube Data API reads via Composio. `YOUTUBE_GET_VIDEO_DETAILS_BATCH` uses 1 quota unit per 50 IDs, so a typical competitor's full channel pull is well under daily quota.

**Common pitfalls:**
- `YOUTUBE_LIST_CHANNEL_VIDEOS` returns playlistItem-shaped rows â videoId is at `items[].snippet.resourceId.videoId`, NOT `items[].id`.
- `YOUTUBE_GET_CHANNEL_ID_BY_HANDLE` expects `@`-style handles; unknown handles return zero items WITHOUT raising an error.
- The Apify YouTube actor still doesn't capture Shorts as of 2026-05-13 â do NOT claim "channel X posted no Shorts this week" based on the Apify pull alone. Run this section's enumeration before making that claim.

**Emoji:** â¶ï¸

**Canonical competitor channels (verified 2026-05-13 via this exact pattern):**

| Channel | Handle | Channel ID | Subs | Videos | Lifetime Views | Notes |
|---|---|---|---|---:|---:|---|
| Transform Real Estate | `@transformrealestate` | `UC0mezb8Y6esTvBieHKgfR2w` | 89,100 | 1,100 | 12,876,748 | Elisa. Bio: "laid off from 6-figure tech job, went all-in on flipping." DIRECT audience validation for the layoff angle. |
| Selling Silicon Valley TV (Danny Gould) | `@sellingsiliconvalleytv` | `UCDRaF4uyW73_jq98GOyv-6g` | 3,080 | 551 | 585,475 | eXp Realty / Gould Luxe Estates. **Latest upload: 2025-10-16 — DARK for 7+ months.** Content-gap opportunity. |

When running competitor enumeration for any weekly calendar, walk both channels via uploads playlists (`UU` + suffix). Add new entries here as new competitors are discovered + verified.

---

## Content Opportunity Scoring Rubric

Each finding from the sources above is scored on a 1-10 scale:

| Criterion | Max Points | Scoring Guide |
|---|---|---|
| **Timeliness** | 3 | Breaking/this-week = 3, This month = 2, Evergreen = 1 |
| **Audience Relevance** | 3 | Direct property value impact = 3, Lifestyle/community = 2, Tangential = 1 |
| **Content Gap** | 2 | Never covered = 2, Covered >4 weeks ago = 1, Recently covered = 0 |
| **Engagement Potential** | 2 | Similar topics got high engagement = 2, Average = 1, Low-engagement pattern = 0 |

**Threshold:** Items scoring â¥7 get â­ RECOMMENDED tag in the Content Opportunity Report.

---

## Source Reliability Notes

- **MLS data** is the gold standard â always trust MLS stats over news articles or anecdotal reports
- **Search Console** reflects actual demand from real people â weight it heavily
- **Local government** sources are high-value but low-frequency â a single city council vote can be a week's worth of content
- **News** is supplementary â verify facts against primary sources before building content
- **Social performance** tells you what works, not what's new â use it to inform format choices, not topic choices
- **Google Trends** is directional, not precise â a spike means "more interest than usual," not "everyone is searching this"
- **BOFU keywords** are strategic, not reactive â use them to fill gaps between timely topics
- **Competitor analysis** is inspiration, not imitation â identify gaps they're missing, don't copy their content
