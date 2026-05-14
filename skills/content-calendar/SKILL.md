---
name: content-calendar
description: >
  Data-Driven Content Intelligence Calendar & Social Media Performance Analyzer for Graeham Watts.
  Generates a scored weekly content calendar by cross-referencing social performance, Search Console
  queries, Reddit demand, and competitor analysis — AND runs the full weekly social media analytics
  pipeline (performance dashboards, competitor research, data validation, week-over-week trending).
  Use ANY time the user mentions: content calendar, what should I post, weekly content plan, content
  strategy, content schedule, content ideas, what topics to cover, posting schedule, editorial calendar,
  social media calendar, content prioritization, topic scoring, content gap analysis, competitors posting,
  trending topics, or deciding WHAT to create and WHEN. Also trigger for: social media analytics,
  post performance, engagement metrics, social media review, weekly social report, Instagram analytics,
  YouTube analytics, Facebook analytics, Google Business Profile reviews, content performance,
  social media ROI, post comparison, week-over-week social metrics, social media coaching review,
  marketing performance, content strategy review, social media audit, channel performance, how are
  my posts doing, what content is performing best, review social metrics with coach, run/check/update
  the weekly social report. Also trigger for data-driven content plans, topic prioritization, or
  "plan my content this week." This is the DECISION LAYER — it tells you what to create AND the
  ANALYTICS LAYER — it tells you how your content performed. Hand topics to content-creation-engine
  for scripts or cinematic-hooks for AI video prompts.
---

# Content Intelligence Calendar

> **Absorbed on 2026-05-12:** `social-media-analyzer` was merged into this skill. All capabilities of `social-media-analyzer` — STEP 0 Connection Health Check, multi-source data collection (Windsor + Apify + GHL), YouTube Shorts blind spot handling, data validation rules (Never Fabricate, Cross-Validate, Verify Totals, Check Missing, Caption QA), 7-tab V12 dashboard architecture, week-over-week JSON storage and trending, status ratings (🟢🟡🔴⚪), top performer analysis, CRM intelligence, competitive research (3-tier Apify + Supadata + Chrome), Organic SEO vs LLM Search optimization framework, and Apify automation scheduling — now live here in the PERFORMANCE ANALYSIS LAYER section below. The folder `skills/social-media-analyzer/` was deleted in the same commit. If you find any reference to `skills/social-media-analyzer/` anywhere in this repo, that reference is a bug — it should point here.

## Scope Boundary (Who Owns What)

> **Updated April 2026 to resolve overlap with `content-creation-engine`.** **Updated May 2026: absorbed `social-media-analyzer` — this skill now handles both Rearview Mirror (performance analytics, was `social-media-analyzer`, absorbed May 2026) AND Weekly Planning (always was this skill).**

This skill is the **WEEKLY PLANNING + PERFORMANCE ANALYTICS** layer. Its job is to (1) pull and analyze social media performance data across all channels, run competitor research, generate analytics dashboards and reports, and (2) use those analytics as input to output a prioritized 5-day production calendar (one week at a time) — who to publish on what day, what funnel tier, what GHL keyword, what format mix.

Once the weekly calendar is approved, this skill HANDS OFF to `content-creation-engine` which owns **PER-TOPIC PRODUCTION**. That skill takes a single topic and generates the full content package (14 formats, 14 prompts, 14 pre-generated deliverables, research data panel, shot list, SSML, editing notes, AI video prompts, SEO package, alt hooks, HeyGen render hand-off).

| Layer | Skill | Scope | Output |
|-------|-------|-------|--------|
| **Weekly Planning** | `content-calendar` (this skill) | 7 days, 5+ topics | Weekly production calendar HTML with per-day topic cards |
| **Per-Topic Production** | `content-creation-engine` | 1 topic, multi-format | Single-topic dashboard HTML with 14 prompts + 14 pre-generated deliverables |

Research that supports WEEKLY planning (trend analysis, competitor scraping, scoring across many topics) lives here. Research that supports ONE TOPIC (the specific stats, news, quotes for that one video/blog/email) lives in `content-creation-engine`'s Phase R and is surfaced on the single-topic dashboard's Show Full Research Data panel.



You are a data-driven content strategist for Graeham Watts (REALTOR, Intero Real Estate,
DRE# 01466876, Bay Area / East Palo Alto). Your job is to analyze what's working, what the
audience wants, and what competitors are doing — then produce a scored, prioritized content
calendar for the coming week.

This skill is an orchestration layer. It doesn't collect data itself — it pulls from existing
data sources that are already connected. Think of it as the "brain" that connects the dots
between performance data, audience demand, and competitive intelligence to make smart content
decisions.

## How This Skill Relates to Other Skills

The content ecosystem has three layers. Understanding which skill does what prevents confusion
and duplication:

| Layer | Skill | What It Does |
|-------|-------|-------------|
| **Rearview Mirror + GPS (this skill)** | `content-calendar` | Pulls performance data, generates weekly analytics reports, runs competitor scraping, analyzes all data sources, scores topics, outputs a prioritized weekly calendar |
| **Engine** | `content-creation-engine` | Takes a topic and produces full scripts, captions, hashtags, cross-post plans |
| **Cinematic Layer** | `cinematic-hooks` | Takes a concept and produces AI video generator prompts for Seedance/Higgsfield |

Typical workflow: Run `content-calendar` (which handles both analytics and planning) to see what performed and decide what to create → Hand topics to `content-creation-engine` for scripts → Optionally use `cinematic-hooks` for AI video ad prompts.

This skill pulls all data directly from Windsor, Search Console, Apify, GHL, and other connected sources.

## Data Sources (What You Pull From)

All of these are already connected. You don't need to set up anything new.

### Source 1: Your Performance Data (via Windsor MCP)

Pull the last 7-14 days of your own content performance. This tells you what's working NOW.

**What to pull:**
- **Instagram:** `date, media_caption, media_type, media_product_type, media_reach, media_engagement, media_like_count, media_comments_count, media_shares, media_saved, media_views, media_permalink` — Windsor connector `instagram`, account `17841411632681720`, preset `last_7d`
- **Facebook:** `date, post_message_oneline, type, post_impressions, post_clicks, post_reactions_total, post_comments_total, post_video_views` — Windsor connector `facebook_organic`, account `375568976359198`, preset `last_7d`
- **YouTube:** `date, video_title, views, likes, comments, shares, subscribers_gained, estimated_minutes_watched, average_view_duration, average_view_percentage` — Windsor connector `youtube`, account `6631`, preset `last_7d` then `last_30d` if empty
- **Search Console:** `date, query, page, impressions, clicks, ctr, position` — Windsor connector `searchconsole`, account `sc-domain:graehamwatts.com`, preset `last_7d`

**Known Windsor issues (critical — read these):**
- YouTube subscriber_count returns 0 — use Apify dataset (account 60) for subscriber count
- Instagram `follower_count` doesn't exist — use `media_reach` for post reach
- Instagram `media_impressions` returns NULL from the API — do NOT request this field
- YouTube daily views often return 0 — try `last_30d` fallback, then Apify dataset
- YouTube often returns only 1 video in 30 days — cross-reference with Apify for fuller data
- See the PERFORMANCE ANALYSIS LAYER section below for the full list of known data quirks

**MoM Comparison Methodology:**
For the Analytics tab, pull TWO date ranges and compare:
- Current 30d: today minus 30 days → today
- Prior 30d: today minus 60 days → today minus 31 days
Calculate delta percentages for reach, engagement, video views, and followers.
Also compute a **Content Type Performance Matrix** — tag each post by content category
(Discovery, Listing/Promo, Data/Market, Engagement, Educational) and calculate average
reach per category to identify what's working at the content-type level.

**What you're looking for:**
- Your top 3 performing posts by engagement rate (not just raw reach)
- Content types that outperform (Reels vs carousels vs static)
- Posting times that correlate with higher engagement
- Topics/themes that consistently perform above your average
- Topics/themes that consistently underperform (stop doing these)

### Source 2: Search Demand Signals (via Windsor — Search Console)

This is one of the most valuable inputs. Search Console shows you exactly what people are
Googling that leads them to your site — and more importantly, queries where you're CLOSE to
ranking but not quite there (page 2 = easy wins).

**What to pull:**
Windsor connector `searchconsole`, account `sc-domain:graehamwatts.com`
Fields: `query, impressions, clicks, ctr, position`
Preset: `last_7d` AND `last_28d` (compare for trends)

**What you're looking for:**
- **Rising queries:** Queries where impressions are increasing week-over-week. These are topics
  gaining search interest — create content NOW before competitors do.
- **Page 2 opportunities:** Queries where your average position is 11-20. You're almost on page 1.
  A video targeting this exact query could push you over.
- **High impression / low click queries:** You're showing up but people aren't clicking. The
  content exists but the title/thumbnail needs improvement, or you need a more targeted piece.
- **New queries:** Queries that appeared this week but weren't in last week's data. These
  represent emerging interest.
- **Local intent queries:** Anything containing city names (East Palo Alto, Menlo Park, Palo Alto,
  Redwood City, San Mateo) — these are your highest-value targets.

### Source 3: Audience Demand Signals (via Apify Reddit Scraping)

`content-creation-engine` Phase 2 (the `content-ideation-engine` sub-skill) owns the Reddit scrape pipeline using Apify `trudax/reddit-scraper-lite`. That pipeline produces the raw audience-demand feed that content-calendar consumes here.

**If a recent scrape exists** (check `outputs/ideation-topics-*.json` or `outputs/ideation-raw-*.json`), use that data. Don't re-scrape unnecessarily — it costs Apify credits.

**If no recent scrape exists** (older than 7 days), trigger a refresh by invoking `content-creation-engine/references/phases/content-ideation-engine/instructions.md` or running `skills/content-creation-engine/scripts/run_reddit_ideation.py` directly.

**Target subreddits** (configured in content-creation-engine's Phase 2):
r/bayarea, r/SanJose, r/oakland, r/SiliconValleyRealEstate, r/RealEstate,
r/FirstTimeHomeBuyer, r/PersonalFinance (housing threads), r/AskSF

**What you're looking for:**
- Questions that come up repeatedly (signals strong demand)
- Questions where the existing answers are wrong or outdated (opportunity to be the expert)
- Emotional topics (layoffs, rent increases, first-time buyer anxiety) — these drive engagement
- Hyper-local questions ("is East Palo Alto safe?" → reframe as Fair Housing compliant content)

### Source 4: Competitor Intelligence

This skill includes a three-tier competitor scraping system (absorbed from social-media-analyzer, May 2026):

**Tier 1: Apify datasets** (if scheduled scrapes are running for competitors)
**Tier 2: Supadata transcript extraction** for competitors' top videos
**Tier 3: Claude in Chrome** for manual verification and channels without scrapers

If a recent competitor analysis exists from a prior weekly run, use that data. Don't duplicate the work.

**What you're looking for:**
- Topics competitors covered this week that Graeham hasn't touched (content gaps)
- Competitor videos that got 10x+ their average views (something hit — replicate the topic angle)
- Formats competitors use that Graeham doesn't (e.g., "day in the life", property walkthroughs)
- Transcript insights: how competitors structure their hooks, what questions they answer

### Source 5: Market Context (via Web Search)

Quick web search for current market conditions that create timely content opportunities:
- Latest mortgage rate changes
- Local market inventory levels
- Recent tech layoffs or hiring surges in the Bay Area
- New housing policy or zoning changes
- Seasonal factors (spring buying season, back-to-school, year-end tax planning)

This doesn't need a dedicated data pipeline — a quick web search at calendar generation time
is sufficient. The goal is to catch timely hooks that make content feel current.

---

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

---

## The Scoring Engine — Opportunity Score

> **Scoring Architecture (Updated April 2026).** This skill owns the **Opportunity Score** — the 25-pt rubric that decides "should we cover this topic THIS WEEK vs other candidates?" A separate score, the **Intent Score**, lives in `content-creation-engine/references/phases/bofu-intent-scorer.md` (absorbed into content-creation-engine May 2026; formerly the `bofu-intent-scorer` standalone skill) and answers "what's the BOFU intent of this topic (DECISION / CONSIDERATION / AWARENESS)?" — used downstream for funnel-mix and CTA decisions. Both scores appear on the single-topic dashboard's Scoring Architecture panel. See `content-creation-engine/SKILL.md` → Scoring Architecture for the full model.

Every potential topic gets scored on 5 criteria. This prevents gut-feel content decisions and ensures the calendar is data-backed.

### Scoring Criteria (25 points max)

| Criterion | Weight | What It Measures |
|-----------|--------|-----------------|
| **Performance Signal** | 0-5 | Does your historical data show this type of content performs well? Top-performing format/topic = 5, average = 3, underperforming = 1 |
| **Search Demand** | 0-5 | Is there search volume for this topic? Rising GSC query = 5, steady query = 3, no search data = 1 |
| **Audience Intent** | 0-5 | Does Reddit/social data show people actively asking about this? Multiple sources confirming demand = 5, one source = 3, assumption only = 1 |
| **Competitive Gap** | 0-5 | Are competitors covering this? Competitors NOT covering it (blue ocean) = 5, covering it but poorly = 3, already saturated = 1 |
| **Timeliness** | 0-5 | Is there a current event or seasonal hook? Breaking news/rate change = 5, seasonal relevance = 3, evergreen = 1 |

**Threshold:** Topics scoring 18+ are "Must Create This Week." Topics scoring 13-17 are
"Strong Candidates." Below 13, save for later or skip.

### Funnel Position Tag

Every topic also gets tagged with its funnel position. This ensures the calendar has a healthy
mix — not all top-of-funnel awareness content and not all bottom-of-funnel sales content.

| Tag | What It Means | Target Mix |
|-----|--------------|------------|
| **TOFU** (Top of Funnel) | Awareness — attracts new eyeballs. Lifestyle, neighborhood tours, market trends | 30-40% |
| **MOFU** (Middle of Funnel) | Consideration — educates active searchers. How-to guides, process explainers, comparison content | 25-30% |
| **BOFU** (Bottom of Funnel) | Decision — converts to leads. Specific listings, pricing guides, "call me" CTAs | 30-40% |

Adjust the mix based on Graeham's current priority:
- **Lead gen focus:** Shift to 20/30/50 (heavy BOFU)
- **Audience growth focus:** Shift to 50/25/25 (heavy TOFU)
- **New listing launch:** One BOFU piece for the listing + normal mix for everything else

## Calendar Output Format — v5.4 Production Bible

The final deliverable is a **hosted HTML Production Calendar** — a single-page web app that
serves as a complete production bible for the video editor (Jason). It gets pushed to GitHub
Pages at `Graehamwatts/online-content/dashboards/weekly-calendars/YYYY-MM-DD-production-calendar-v6.html`.

The HTML calendar has **three tabs**: Analytics, Production Map, and Copy Bank.

### Tab 1: Analytics Dashboard

Month-over-month performance comparison showing:
- **MoM Metrics Table:** Current 30d vs prior 30d for reach, engagement, followers, video views
- **Content Type Performance Matrix:** Average reach by content category (Discovery, Listing/Promo,
  Data/Market, Engagement, Educational) with sample size and top performer
- **Engagement Details Table:** Per-post breakdown with reach, likes, comments, shares, saves,
  engagement rate, and content type tag
- **Visual Bar Chart:** CSS-only bar chart comparing post reach across the period
- **GSC Query Analysis:** Top search queries by impressions, rising queries, page-2 opportunities,
  and query cluster analysis (e.g., "AB 1482 cluster = X impressions")

### Tab 2: Production Map (Main Calendar)

**Intelligence Stack Panel** at the top showing:
- Every data source used (Windsor IG, Windsor YT, Windsor GSC, Windsor FB, Apify Reddit, Web Search)
- Status of each source (connected/partial/unavailable) with percentage of data coverage
- Which skills were used in generation (content-calendar, content-creation-engine, cinematic-hooks)
- Transparent about what data was NOT available

**Day Cards** — One expandable accordion card per content day (typically 5 content days + 1 email
newsletter day). Each day card shows:

```
[DAY] — [Date]
TOPIC: [Specific topic with angle]
TITLE: [SEO-optimized title, <60 chars]
FORMAT: [Primary format — YouTube Long / Reel / Short / etc.]
PLATFORM: [Primary] → [Cross-post targets]
FUNNEL: [TOFU / MOFU / BOFU]
SEARCH TARGET: [Organic SEO / LLM Search / Both]
SCORE: [X/25] — [Brief justification]
SOURCE BADGE: [Where the idea came from — GSC Query, IG Performance, News Cycle, Reddit, Trend]
HOOK (first 3 sec): "[Specific opening line or visual hook]"
POSTING TIME: [Recommended time based on engagement data]
CTA: [Specific call-to-action + GHL keyword trigger if applicable]
```

**Derivative Format System (CRITICAL v5.4 FEATURE):**
Each day card contains a **horizontal row of clickable format buttons**:
YouTube Long | YT Short | IG Reel #1 | IG Reel #2 | IG Carousel | TikTok | Blog | GMB | FB

Clicking any button reveals a **derivative panel** with the COMPLETE production package for that
specific format, including:
- Full script (with inline shot direction tags)
- Platform-specific specs (duration, aspect ratio, resolution)
- Caption with hashtags
- Description / SEO metadata
- Posting instructions
- GHL keyword CTA

The core asset (usually YouTube Long) panel also includes:
- **Inline Shot Direction Tags:** `[B-ROLL: description]`, `[TALKING HEAD]`, `[TEXT OVERLAY: text]`,
  `[DRONE: description]`, `[SCREEN RECORD: description]` embedded directly in the script
- **Editing Notes for Jason:** Yellow block with B-roll shot list, text overlay timing, pacing notes,
  thumbnail concept, music/SFX direction
- **ElevenLabs SSML Block:** Full `<speak>`, `<prosody>`, `<break>` markup for AI avatar voice
  generation, ready to paste into ElevenLabs
- **AI Video Prompts:** Seedance 2.0 / Kling-ready prompts for hook shots and B-roll sequences,
  with camera movement, lighting, and duration specs
- **Edit Button:** Toggle `contentEditable` on script sections for in-browser editing (local only,
  resets on refresh)

### Tab 3: Copy Bank

Pre-written copy blocks for quick use:
- Email newsletter template for the week
- Social media captions (per platform)
- Blog post outline
- Each block has a **copy-to-clipboard button**

### Visual Design Requirements (Light Theme)

The calendar MUST use a light color scheme matching Graeham's brand:
```
--bg: #f4f5f7 (light gray page background)
--card: #ffffff (white cards)
--navy: #1B2A4A (primary text, headers, nav)
--gold: #C5A258 (accents, badges, active states)
--text: #2d3748 (body text)
--muted: #718096 (secondary text)
```
Fonts: Plus Jakarta Sans (headings) + DM Sans (body) via Google Fonts import.
**DO NOT use dark mode.** The user has explicitly rejected dark themes.

### Source Badges

Every day card gets a source provenance badge showing where the topic idea came from:
- `.src-gsc` — Google Search Console query cluster (blue)
- `.src-reddit` — Reddit audience demand signal (orange)
- `.src-news` — Current news/event cycle (red)
- `.src-perf` — Own performance data showing topic works (green)
- `.src-trend` — Market trend or seasonal hook (purple)

### Key CSS Classes (for consistent rendering)

```css
.dir { /* Inline shot direction tags — blue background */ }
.sm { /* Section markers — bold navy */ }
.edit-notes { /* Yellow editing notes blocks for Jason */ }
.el-block { /* Purple ElevenLabs SSML blocks */ }
.vid-prompt { /* Green AI video prompt blocks */ }
.flow-card / .deriv-panel { /* Clickable derivative format system */ }
.edit-btn { /* In-browser script editing toggle */ }
.src-badge { /* Source provenance badges */ }
.isp / .isp-card { /* Intelligence Stack panel */ }
```

### Key JavaScript Functions

```javascript
showTab(id)           // switches main tabs (analytics/calendar/copy bank)
toggleDay(id)         // opens/closes day accordion cards
showDeriv(dayId, fmt) // switches between derivative format panels within a day
toggleEdit(btn)       // toggles contentEditable on script boxes
copyText(btn)         // copies text to clipboard from copy bank
toggleCheck(el)       // toggles deliverable checkboxes
```

### Full Auto-Render Button + Dashboard Links (v6.2 — Apr 2026)

Every core asset derivative panel MUST include a "🚀 Full Auto-Render" button directly under the ElevenLabs SSML block. Clicking this button triggers the `heygen-elevenlabs-renderer` skill and produces a delivered MP4 with zero manual steps.

**v6.2 upgrade:** every calendar now displays a persistent "Where did my render go?" banner at the top of the Production Map tab, and after each render completes the button reveals three quick-links — the local MP4, the HeyGen video page (`https://app.heygen.com/videos/<id>`), and the ElevenLabs generation history. Graeham should never have to ask "where is this stored?" again.

**How the button works:**

The button POSTs to a local Flask webhook handler (`heygen-elevenlabs-renderer/references/webhook_handler.py`) running on `http://127.0.0.1:7788`. The handler receives `{slug, script_path}` and runs `full_render.py` in the background. The button polls `/status/<job_id>` every 10s. When the render completes, the webhook returns a `dashboards` object containing `heygen_video_page`, `local_mp4`, `elevenlabs_history`, and `elevenlabs_voice_library` — the button wires those straight into the three quick-link `<a>` tags. No regex-scraping of stdout.

**Required button markup + banner** — copy verbatim from `skills/heygen-elevenlabs-renderer/references/v54_auto_render_button.html`. That file is the canonical source and already contains the button block, the styles, the JS, AND the `#auto-render-banner` element. Do not re-implement by hand.

**Injection points:**
- Button markup block → inside every core asset `.deriv-panel`, under the `.el-block`. Set `data-slug="{SLUG}"` and `data-script-path="{ABS_PATH_TO_SSML_FILE}"`.
- Style block → inside the calendar `<style>`.
- JS block → once, at the bottom of `<body>`.
- Banner element → once, at the top of the Production Map tab (pings `/health` on load).

**Upstream requirement:** The calendar generator MUST also write a `.ssml.txt` file per day at a known path (`outputs/scripts/{slug}.ssml.txt`) and set `data-script-path` on each button to that absolute path. Without that file on disk, the renderer has nothing to ingest.

**Where renders + voices live (surfaced in the banner and button):**

| What | Where | URL |
|---|---|---|
| Finished video | HeyGen project page | `https://app.heygen.com/videos/<video_id>` (click-through from button) |
| All renders | HeyGen projects list | `https://app.heygen.com/projects` |
| Voice generations | ElevenLabs history | `https://elevenlabs.io/app/speech-synthesis/history` |
| Graeham cloned voice | ElevenLabs Voice Library | `https://elevenlabs.io/app/voice-library` |
| Local MP4 | `outputs/renders/<slug>.mp4` | `file:///` link rendered in the button |
| Render metadata | `outputs/renders/<slug>.meta.json` | absolute path in the `meta` field |

**Prerequisite for the user:** `python3 skills/heygen-elevenlabs-renderer/references/webhook_handler.py` must be running in a separate terminal. The banner pings `/health` on page load — if offline, it turns red and instructs the user to start the handler, but still shows the dashboard links so they can check manually.

### GitHub Pages Hosting

After generating the HTML file, push it to the `Graehamwatts/skills` repo under:
`online-content/dashboards/weekly-calendars/YYYY-MM-DD-production-calendar-v6.html`

The hosted URL will be:
`https://graehamwatts.github.io/online-content/dashboards/weekly-calendars/YYYY-MM-DD-production-calendar-v6.html`

### Weekly Email Format (for the Blog Producer) — Three-Tier Topic Options (April 2026)

In addition to the hosted HTML calendar above, content-calendar produces a **Monday email** for the blog producer (the publishing team member who actually posts content) and **daily emails** each weekday morning. The email is the *trigger*; the hosted dashboard is the *action surface*.

**Why this exists:** Blog Track doesn't need the full production calendar (that's for Jason and Peter). Blog Track needs a quick decision surface: "what should I post this week, and where do I grab it?" The email gives him three tiers of topic options, each with a deep-link to the relevant section of the hosted dashboard where the Copy Content button lives.

#### Three-Tier Structure

The Monday email displays the week's topics in three tiers based on the Opportunity Score (25 pts):

| Tier | Score range | Threshold label | Count |
|---|---|---|---|
| **Top tier** | 22-25 | `must_create` | 1-2 topics — the highest-scoring topics this week |
| **Next tier** | 17-21 | `strong` | 2-3 topics — solid alternates if top tier doesn't resonate |
| **Third tier** | 12-16 | `consider` | 1-2 topics — backup options |

Topics scoring below 12 (`skip` threshold) are NOT included in the email. They're excluded entirely.

#### Why Links Instead of In-Email Copy Buttons

**Email clients (Gmail, Outlook, Apple Mail) strip JavaScript from HTML emails for security.** The Copy Content / Copy Script Prompt / Copy Production Prompt buttons documented in `content-creation-engine/references/single-topic-dashboard-rules.md` Rule 3 cannot work inside the email itself — the JS that copies to clipboard would be removed before Blog Track ever opened the email.

Instead, each topic in the email links directly to its section in the hosted dashboard (where the buttons DO work). The flow:

1. Blog Track opens Monday email
2. Picks the topic he wants to post today
3. Clicks "Open in dashboard" link
4. Dashboard opens at that topic's day card
5. Blog Track clicks Copy Content button → content copied → Blog Track pastes into the publishing platform

#### Linking Convention (Deep-Link Anchors)

For the email's links to work, the hosted production calendar must include stable section IDs:

- Each day card: `<section id="day-{day-name}">` (e.g., `id="day-monday"`)
- Each topic within a day: `<div id="topic-{slug}">` (e.g., `id="topic-epa-market-update-april-2026"`)

Email link format: `https://graehamwatts.github.io/online-content/dashboards/weekly-calendars/{YYYY-MM-DD}-production-calendar-v6.html#topic-{slug}`

When the dashboard renders, ALL topics across all three tiers must have stable IDs even if they don't appear in the day-card layout (third-tier topics might live in a "Backup Options" section that's expanded by default but doesn't have its own day slot).

#### Monday Email HTML Template

Email-safe HTML — table-based layout, inline styles, no external CSS, no JS. Tested in Gmail, Outlook, Apple Mail.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Your Content Week — [DATE RANGE]</title>
</head>
<body style="margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f4f5f7;color:#2d3748;">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width:640px;margin:0 auto;background:#ffffff;">
    <!-- Header -->
    <tr>
      <td style="padding:32px 32px 16px;background:#1B2A4A;color:#ffffff;">
        <h1 style="margin:0;font-size:20px;font-weight:700;letter-spacing:-0.5px;">Your Content Week — [DATE RANGE]</h1>
        <p style="margin:8px 0 0;font-size:13px;color:rgba(255,255,255,0.7);">[N] topics scored. Pick from any tier — top tier is the data's strongest pick this week.</p>
      </td>
    </tr>

    <!-- Top Tier -->
    <tr>
      <td style="padding:24px 32px 8px;">
        <div style="display:inline-block;padding:4px 10px;background:#C5A258;color:#1B2A4A;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;border-radius:4px;">TOP TIER · MUST CREATE</div>
        <p style="margin:8px 0 16px;font-size:13px;color:#718096;">Highest Opportunity Score (22-25). The data's strongest pick.</p>
      </td>
    </tr