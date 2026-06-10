---
name: content-calendar
description: "Data-Driven Content Intelligence Calendar & Social Media Performance Analyzer for Graeham Watts. Generates a scored weekly content calendar by cross-referencing social performance, Search Console queries, Reddit demand, and competitor analysis. Also runs the full weekly social media analytics pipeline (performance dashboards, competitor research, data validation, week-over-week trending). Use ANY time the user mentions: content calendar, what should I post, weekly content plan, content strategy, posting schedule, editorial calendar, content prioritization, topic scoring, content gap analysis, trending topics, social media analytics, post performance, engagement metrics, weekly social report, Instagram analytics, YouTube analytics, content performance, social media ROI, week-over-week social metrics, social media audit, or how content is performing. This is the DECISION LAYER (what to create and when) AND the ANALYTICS LAYER (how content performed). Hands topics to content-creation-engine for scripts."
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

> Read `references/performance-analysis.md` for the full PERFORMANCE ANALYSIS LAYER (absorbed social-media-analyzer) — channels table, report recipients, STEP 0 connection health check, multi-source data collection (Windsor/Apify/GHL), data validation rules, V12 7-tab dashboard architecture, status ratings, CRM intelligence, Apify automation, competitive research tiers, and the Organic SEO vs LLM Search framework.

> Read `references/scoring-engine.md` for the Scoring Engine — the 25-pt Opportunity Score rubric, scoring thresholds, and Funnel Position Tags (TOFU/MOFU/BOFU mix).

> Read `references/dashboard-architecture.md` for the Calendar Output Format (v5.4 Production Bible) — the 3-tab hosted HTML calendar structure, day cards, derivative format system, CSS/JS conventions, Full Auto-Render button, GitHub Pages hosting, and the three-tier Monday email format for the blog producer.

---

## MANDATORY GATES (automated 2026-06-09 — run, don't re-derive)

From `skills/content-creation-engine/` run, in this order around every weekly calendar:

1. **Before pushing the calendar:** `python scripts/weekly_overlap_check.py --calendar <calendar-json>` — exit 1 means a topic overlaps the last 4 weeks (history + in-production); replace it or justify the new angle in the calendar notes.
2. **Before sending/publishing anything:** `python scripts/verify_output_brand.py <output files>` — exit 2 means a blocked brand value or truncated file; never ship.
3. **After the calendar ships:** `python scripts/update_topic_history.py --calendar <calendar-json>` — writes the week into `references/topic-history.json` so next week's freshness penalty actually has data. Skipping this silently breaks the no-repeat system.

For routing between sibling skills, read `../shared-references/routing-decision-tree.md`.
