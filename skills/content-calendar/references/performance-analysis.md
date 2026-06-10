# Performance Analysis Layer — moved verbatim from `content-calendar/SKILL.md` (2026-06-09 refactor)

## PERFORMANCE ANALYSIS LAYER (absorbed from social-media-analyzer, May 2026)

> This entire section was the `social-media-analyzer` skill. It is now part of `content-calendar` because both are weekly-scope: this layer looks backward (how did content perform?) and feeds directly into the Scoring Engine below (what should we create next?). Running them as one skill eliminates the handoff gap.

### Graeham's Channels

| Platform | Handle / URL | Windsor Account ID | Apify Dataset ID |
|----------|-------------|-------------------|------------------|
| Instagram | @graeham.watts | `17841411632681720` | `dsq8nWfQuIMD7JS0e` |
| Facebook | /GraehamWattsRealtor | `375568976359198` | `gvteaTX1cX726dq9K` |
| YouTube | graehamwatts@gmail.com | `6631` | `Cj2FhJAe9nynZa372` |
| Google My Business | Graeham Watts - Realtor | `locations/2259460849528074465` | N/A |
| Google Search Console | graehamwatts.com | `sc-domain:graehamwatts.com` | N/A |
| GoHighLevel CRM | Intero Real Estate | `6wuU3haUH7uNeT20E3UZ` | N/A |

### Report Recipients

- **TO:** graehamwattsmarketing@gmail.com
- **CC:** graehamwattsclientcare@gmail.com, graehamwatts@gmail.com

Always include all three addresses on reports.

### STEP 0: Connection Health Check (MUST RUN FIRST — EVERY TIME)

Before pulling any data, run this health check. If any connector fails, fix it or document
the gap BEFORE building the report. Never skip this step — it's what prevents the recurring
field-name errors and null-data bugs that plagued earlier report versions.

**Health check procedure:**

1. Call `get_connectors` — verify all 7 connectors are present and have accounts:
   - `instagram` (account `17841411632681720`)
   - `facebook_organic` (account `375568976359198`)
   - `youtube` (account `6631`)
   - `google_my_business` (account `locations/2259460849528074465`)
   - `searchconsole` (account `sc-domain:graehamwatts.com`)
   - `gohighlevel` (account `6wuU3haUH7uNeT20E3UZ`)
   - `apify_dataset` (accounts `58`, `59`, `60`)

2. For EACH connector, run a small test pull with known-good fields:
   - `instagram`: `["date", "media_reach", "reach"]` with `last_7d`
   - `facebook_organic`: `["date", "page_impressions", "page_fans"]` with `last_7d`
   - `youtube`: `["date", "views", "likes"]` with `last_7d`
   - `google_my_business`: `["date", "impressions"]` with `last_7d`
   - `searchconsole`: `["date", "impressions", "clicks", "query"]` with `last_7d`
   - `gohighlevel`: `["contact_source", "contact_email", "pipeline_name"]` with `last_30d`
   - `apify_dataset`: `["item_collection__data"]` with account `58`

3. Log results in a health check table at the top of the report's Data Source Notes:
   | Connector | Status | Records | Notes |
   |-----------|--------|---------|-------|
   | Instagram | ✅ / ❌ | N rows | Any issues |
   | Facebook  | ✅ / ❌ | N rows | Any issues |
   | etc.      |        |         |       |

4. If a connector returns an error:
   - Call `get_options` for that connector to check if field names have changed
   - Try alternative field names from the `get_options` output
   - If the connector itself is missing, note it as a RED alert in the report
   - NEVER proceed with fabricated data — show "Data unavailable" for that source

5. If a field returns all nulls or zeros (like YouTube subscriber_count):
   - Document it in the health check table
   - Use the fallback source (Apify for YT, Claude in Chrome for GMB reviews, etc.)
   - Note which source the final number came from

### Performance Data Collection — Multi-Source Strategy

The report pulls from multiple data pipelines. Using all available sources is essential because
each has different strengths and blind spots.

#### Source P1: Windsor.ai MCP Connector (aggregate daily metrics)

Windsor provides daily aggregate metrics for each platform. Use the `get_data` tool from the
Windsor MCP connector. Always call `get_connectors` first to confirm what's available, and
call `get_options` for any connector where you're unsure of available fields.

**Key Windsor fields by platform:**

| Platform | Fields to Pull | Date Preset |
|----------|---------------|-------------|
| `instagram` | `date, media_caption, media_type, media_product_type, media_permalink, likes, comments, shares, saves, media_reach, media_engagement, media_views, media_reel_video_views, media_reel_total_interactions, media_reel_avg_watch_time, follower_count_1d, reach_1d` | `last_7d` |
| `facebook_organic` | `date, post_message, type, permalink_url, post_reactions_total, post_comments_total, post_clicks, post_impressions, post_impressions_unique, post_impressions_organic, page_impressions, page_impressions_organic, page_engaged_users, page_fans, page_post_engagements, page_views_total, page_follows` | `last_7d` |
| `youtube` | `date, video_title, videourl, views, likes, comments, shares, estimated_minutes_watched, average_view_duration, subscriber_count, subscribers_gained, subscribers_lost` | `last_7d` first, then `last_30d` if empty |
| `searchconsole` | `date, query, page, impressions, clicks, ctr, position` | `last_7d` |
| `google_my_business` (daily metrics) | `date, impressions, clicks, direction_requests, call_clicks, website_clicks, conversations` | `last_7d` |
| `google_my_business` (reviews) | `review_total_count, review_average_rating_total, review_count, review_average_rating, review_comment, review_star_rating, review_create_time, review_reviewer, review_reply_comment` | `date_from` 12+ months back |
| `gohighlevel` (contacts) | `contact_id, contact_first_name, contact_last_name, contact_source, contact_date_added, contact_tags, opportunity_name, opportunity_status, opportunity_monetary_value, opportunity_created_at, pipeline_name, opportunity_pipeline_stage_id, opportunity_source, contact_lead_source` | `last_30d` |
| `gohighlevel` (pipelines) | `pipeline_id, pipeline_name, pipeline_stages` | No date filter |

**Critical: GMB reviews require a SEPARATE wide-range pull.** The 7-day daily metrics pull
will return null for all review fields. You MUST make a second call with `date_from` going back
at least 12 months to get review history.

**Known Windsor data issues (verified April 2026 audit):**

- **YouTube subscriber_count returns 0.** Known Windsor bug. Use Apify for subscriber count.
- **YouTube daily views/likes often return 0.** Windsor YouTube connector is unreliable for daily metrics. Try `last_30d` as fallback. If still empty, rely on Apify dataset (account 60).
- **Instagram `follower_count` field DOES NOT EXIST.** Use `reach` for daily profile reach. Use `media_reach` for individual post reach. `impressions` is deprecated and returns null.
- **GMB `search_impressions` and `review_rating` DO NOT EXIST.** Use `impressions` for search+maps impressions. `review_count` exists but returns null on 7-day pulls — MUST use 12+ month date range.
- **GHL field names are NOT what you'd guess.** Correct field names (verified): `contact_first_name`, `contact_last_name` (NOT `contact_name`), `pipeline_name` (NOT `pipeline`), `opportunity_status` (NOT `pipeline_stage`), `opportunity_pipeline_stage_id` (gives stage UUID — cross-reference with `pipeline_stages` from a separate pipeline pull to get stage names). GHL has 200+ fields — run `get_options` if unsure.
- **GHL returns 1,200+ contact records** — always gets saved to temp file. Use Python/jq to extract summaries.
- **Apify `apify_dataset` connector via Windsor DOES NOT expose individual item fields.** Fields like `title`, `viewCount` cause 500 errors. Use `item_collection__data` (JSON blob) or access Apify API directly: `curl "https://api.apify.com/v2/datasets/{ID}/items?limit=50"`
- **Instagram reel_video_views** can show numbers in the millions while actual reach is under 200. These are cumulative algorithmic impression counts, NOT unique viewers. Always flag this discrepancy. Use `media_reach` as the real audience size metric.

#### Source P2: Apify Datasets via Windsor `apify_dataset` Connector (post-level data)

Apify scrapers run weekly (Sunday 11pm PT) and store post-level data in datasets.

| Platform | Windsor Account ID | Contains |
|----------|-------------------|----------|
| Instagram | `58` (dataset dsq8nWfQuIMD7JS0e) | Full post data: caption, likesCount, commentsCount, videoViewCount, videoPlayCount, timestamp, type, productType |
| Facebook | `59` (dataset gvteaTX1cX726dq9K) | Post data: text, likes, shares, topReactionsCount, viewsCount, time, media |
| YouTube | `60` (dataset Cj2FhJAe9nynZa372) | Video data: title, viewCount, likes, commentsCount, date, numberOfSubscribers, duration |

**CRITICAL: YouTube Shorts Blind Spot.** The current Apify YouTube scraper does NOT capture
YouTube Shorts — it only scrapes regular video uploads. The report must handle this honestly:

1. State this limitation clearly in the Data Source Notes section
2. Do NOT claim "zero uploads this week" — there are likely Shorts that the scrapers can't see
3. Instead say: "YouTube Shorts data is not captured by current scrapers. [X] regular video uploads detected."
4. If Claude in Chrome tools are available, navigate to the YouTube channel's Shorts tab to verify
5. Flag in recommendations that the Apify scraper needs a Shorts-specific actor added

**YouTube Shorts Data Collection Methods:**

- **Method 1:** Set `"maxShorts": 30` in the existing Apify YouTube Channel Scraper actor
- **Method 2:** Add dedicated actor `streamers/youtube-shorts-scraper` targeting `https://www.youtube.com/@graehamwatts/shorts`
- **Method 3:** Claude in Chrome fallback — navigate to Shorts tab, capture titles and view counts

#### Source P3: GHL CRM Data

**Primary method:** Check if a direct LeadConnector MCP is available. The direct MCP URL is
`https://services.leadconnectorhq.com/mcp/` with Bearer token + LocationId header.

**If the direct MCP is NOT connected**, fall back to Windsor's `gohighlevel` connector and
document the limitation.

**Always pull pipeline structure separately** (fields: `pipeline_id, pipeline_name, pipeline_stages`)
with no date filter to get the actual stage names.

### MANDATORY: Data Validation & Quality Control

Every past report failure came from skipping validation. Complete ALL checks before building any
dashboard or report.

**Rule 1: Never Fabricate Data.** If you don't have a data point, report it as "N/A" or "Data not available." Past errors include: YouTube likes fabricated (reported 234, actual 8), video names invented, GMB reported as "no reviews" when there were 27 at 5.0 stars.

**Rule 2: Cross-Validate Across Sources.** When the same metric is available from multiple sources, compare them. Known discrepancies: YouTube subscriber_count (Windsor=0, Apify=real), Instagram reel_video_views vs reach, Facebook page_impressions vs post_impressions.

**Rule 3: Verify Totals and Calculations.** Sum daily values and verify they match totals. Confirm engagement rate denominators: reach for IG, followers for FB, views for YT.

**Rule 4: Check for Missing Data.** After all pulls, verify data exists for: Instagram (post + daily), Facebook (post + page), YouTube (Windsor + Apify + Shorts documented), GSC (query-level), GMB (daily + 12-month review pull!), GHL CRM (sources + pipeline + opportunities).

**Rule 5: Caption QA Check.** Scan published captions for: internal production notes left in, broken formatting, missing CTAs.

### Dashboard Philosophy: Marketing Intelligence, NOT Data Dump

Every metric must answer THREE questions or it doesn't belong: (1) What happened? (2) Is that good or bad? (3) What should Graeham DO about it?

**The Core Narrative:** Every report opens with a 3-4 sentence "The Story This Week" summary in plain English, as if a marketing coach is talking to Graeham.

### Trending & Comparison Requirements

**EVERY metric must show:** this week's value, last week's value (from saved JSON), % change with arrow (↑/↓), 4-week rolling average, plain-English verdict.

**Week-over-week data storage:** After every report, save `social-media-data/weekly-data-YYYY-MM-DD.json`. On next run, load the previous week's file to calculate deltas. Also maintain `social-media-data/monthly-rolling.json` for 4-week averages.

### Status Ratings

| Rating | Criteria | What It Means |
|--------|----------|---------------|
| 🟢 Excellent | Metrics trending up for 2+ weeks AND above benchmark | Keep doing what you're doing |
| 🟡 Moderate | Metrics flat OR within ±10% of benchmark | Room to improve with specific changes |
| 🔴 Needs Work | Metrics trending down for 2+ weeks OR below benchmark | Needs attention — specific changes recommended |
| ⚪ Insufficient Data | Less than 2 weeks of comparison data | Need more history to evaluate |

**The status must include a 1-sentence WHY.**

### Top Performers — Actionable Analysis

**This Week Only:** Show best-performing content from the current period. Compare engagement to 4-week average. Analyze WHY it worked (time, format, topic, audio). Give specific recommendation.

**All-Time (monthly or on-request only):** Pattern analysis connecting to content strategy decisions.

### CRM Intelligence

The CRM section must answer: Are leads converting? Which sources are worth it (rank by volume AND quality)? What's the trend? What should change?

### Analytics Dashboard Structure (V12 — 7 Tabs)

Generate a single-file HTML dashboard with 7 tab-based sections using Chart.js from CDN.
Every section follows the What Happened → Is That Good → What To Do framework.

**V12 DESIGN PRINCIPLE: Actions live NEXT TO the data, not in a separate tab.** Every finding
is followed by a gold-bordered ACTION box.

- **Tab 1: The Big Picture** — narrative, health score, platform status with What To Do column, week-over-week cards, top 3 wins, #1 priority action
- **Tab 2: Content Performance & What's Working** — this week's posts with inline ACTION boxes, content type analysis, Stop/Start/Continue
- **Tab 3: Platform Deep Dives** — collapsible per-platform sections (IG, FB, YT, GMB, GSC) with metrics + charts + inline ACTION boxes
- **Tab 4: CRM & Lead Intelligence** — source quality ranking with ACTION boxes, pipeline attribution with step-by-step fixes
- **Tab 5: Market Context & Trends** — search intent analysis, video opportunities with SEO/LLM target column, content gaps with FIX THIS WEEK boxes
- **Tab 6: Consolidated Checklist** — printable action summary, 7-day content calendar, success metrics
- **Tab 7: Data Sources & Connector Health** — connector status, fields used, known issues, workarounds

### Analytics Report Delivery

Save dashboard: `mnt/outputs/weekly-social-dashboard.html`
Save raw data: `social-media-data/weekly-data-{date}.json`

Draft email via Gmail MCP:
- TO: graehamwattsmarketing@gmail.com
- CC: graehamwattsclientcare@gmail.com, graehamwatts@gmail.com
- Subject: "Weekly Social Media Report — [DATE RANGE] — Health Score: [SCORE]/100"

### Visual Color Coding (Analytics)

| Color | Hex | Meaning |
|-------|-----|---------|
| Red | `#ff6b6b` | Needs attention, below benchmark |
| Green | `#4CAF50` | Healthy, at/above benchmark |
| Amber | `#ff9800` | Opportunity, moderate, watch |
| Navy | `#1B365D` | Neutral, branding |

Platform: IG `#C13584`, FB `#1877F2`, YT `#FF0000`, GMB `#34A853`, GSC `#FBBC04`
Brand: Navy `#1B365D`, Gold `#C5A258`, White `#FFFFFF`, Gray `#F5F5F5`
**Real estate benchmarks:** IG 1.5-3% good, FB 0.5-1% good, YT 2-5% good, GMB 4.0+ stars

### Apify Automation

- **Schedule:** Cron `0 23 * * 0` (Sunday 11pm PT)
- **Actors:** Instagram Post Scraper, Facebook Posts Scraper, YouTube Channel Scraper
- **YouTube Shorts fix:** Set `"maxShorts": 30` or add `streamers/youtube-shorts-scraper`
- **Competitor scrapes:** Add runs for Selling Silicon Valley, Transform Real Estate, Trung Lam & Evan RE Group on the same Sunday schedule

### Competitive Research & Video Content Strategy

Every weekly report MUST include a data-driven video content strategy section.

**Competitor Channels:**

| Channel | Handle | Subscribers | Why Track |
|---------|--------|-------------|-----------|
| Selling Silicon Valley | Danny Gould | ~3.1K | Direct market competitor |
| Transform Real Estate | Elisa | ~89K | High-growth, great Shorts strategy |
| Trung Lam & Evan RE Group | — | ~4.3K | Bay Area team, active Shorts |

**Three-tier research approach:**

- **Tier 1: Automated Apify scraping** — structured data from YouTube + Instagram scrapers
- **Tier 2: YouTube transcript extraction via Supadata** — `GET https://api.supadata.ai/v1/youtube/transcript?url={video_url}&text=true` with `x-api-key: sd_10e83042186ce9c2feb277088382fdb2` (free tier: 200/month, budget ~10-15/week on competitors)
- **Tier 3: Claude in Chrome** — fallback + verification, visit channels directly

**Competitor Instagram tracking:** @dannygould_realestate, @transformrealestate, @trunglam.realtor

**Competitor Analysis Output Format:**

For each competitor: posting frequency, top performer this week (title + views + why it worked), content themes (3-5 topics), what Graeham can learn (specific actionable takeaway), content gap, transcript insight.

### Organic SEO vs LLM Search Optimization Framework

Videos optimized for traditional Google/YouTube search and videos optimized for LLM-powered
search (ChatGPT, Perplexity, Claude, Google AI Overviews) are DIFFERENT. Each video recommendation
MUST specify which it targets.

**Organic SEO Videos** (targeting Google/YouTube search):
- Title: Keyword-front-loaded, match exact search queries from GSC data
- Description: Keyword-dense, 300+ words, timestamps, links
- Thumbnail: High-contrast, face + text overlay
- Content: Can be personality-driven, entertaining, opinion-heavy
- Success metric: CTR, watch time, YouTube search ranking

**LLM Search Videos** (targeting AI answer citations):
- Title: Clear, factual, question-answering format — NO clickbait
- Description: Structured data, specific numbers, dates, sources cited
- Content: Authoritative, fact-dense, answers questions directly in first 30 seconds
- Transcript/Captions: MUST be accurate — LLMs read transcripts, not thumbnails
- Success metric: Being cited in AI answers

**Weekly recommendation split:** At least 2 target LLM Search, at least 2 target Organic SEO, 1-2 dual-purpose.

### Video Recommendations Table (5-7 per week)

Each recommendation must include: Title (SEO-optimized, <60 chars), Format (Short/Long), Search Target (Organic SEO/LLM Search), Hook (first 3 seconds), Why this topic (data citation required), Target keyword, Best posting time, Cross-post plan. At least 3 must be Shorts.
