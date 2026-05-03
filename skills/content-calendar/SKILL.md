---
name: content-calendar
description: >
  Data-Driven Content Intelligence Calendar for Graeham Watts — generates a scored weekly
  content calendar by cross-referencing social performance, Search Console queries, Reddit
  demand, and competitor analysis. Use ANY time the user mentions: content calendar, what
  should I post, weekly content plan, content strategy, content schedule, content ideas,
  what topics to cover, posting schedule, editorial calendar, social media calendar,
  content prioritization, topic scoring, content gap analysis, competitors posting,
  trending topics, or deciding WHAT to create and WHEN. Also trigger for data-driven
  content plans, topic prioritization, or "plan my content this week." This is the
  DECISION LAYER — it tells you what to create. Hand topics to content-creation-engine
  for scripts or cinematic-hooks for AI video prompts.
---

# Content Intelligence Calendar

## Scope Boundary (Who Owns What)

> **Updated April 2026 to resolve overlap with `content-creation-engine`.**

This skill is the **WEEKLY PLANNING** layer. Its job is to analyze data across multiple sources and output a prioritized 5-day production calendar (one week at a time) — who to publish on what day, what funnel tier, what GHL keyword, what format mix.

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
| **Rearview Mirror** | `social-media-analyzer` | Pulls performance data, generates weekly analytics reports, runs competitor scraping |
| **GPS (this skill)** | `content-calendar` | Analyzes all data sources, scores topics, outputs a prioritized weekly calendar |
| **Engine** | `content-creation-engine` | Takes a topic and produces full scripts, captions, hashtags, cross-post plans |
| **Cinematic Layer** | `cinematic-hooks` | Takes a concept and produces AI video generator prompts for Seedance/Higgsfield |

Typical workflow: Run `social-media-analyzer` (or use its most recent report) → Run `content-calendar` to decide what to create → Hand topics to `content-creation-engine` for scripts → Optionally use `cinematic-hooks` for AI video ad prompts.

You can also run this skill standalone — it will pull the data it needs directly from Windsor,
Search Console, and other connected sources.

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
- See the social-media-analyzer skill for the full list of known data quirks

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

The social-media-analyzer skill now includes a three-tier competitor scraping system:

**Tier 1: Apify datasets** (if scheduled scrapes are running for competitors)
**Tier 2: Supadata transcript extraction** for competitors' top videos
**Tier 3: Claude in Chrome** for manual verification and channels without scrapers

If a recent competitor analysis exists from the social-media-analyzer's weekly report, use that
data. Don't duplicate the work.

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

## The Scoring Engine — Opportunity Score

> **Scoring Architecture (Updated April 2026).** This skill owns the **Opportunity Score** — the 25-pt rubric that decides "should we cover this topic THIS WEEK vs other candidates?" A separate score, the **Intent Score**, lives in `skills/bofu-intent-scorer/` (standalone skill) and answers "what's the BOFU intent of this topic (DECISION / CONSIDERATION / AWARENESS)?" — used downstream for funnel-mix and CTA decisions. Both scores appear on the single-topic dashboard's Scoring Architecture panel. See `content-creation-engine/SKILL.md` → Scoring Architecture for the full model.

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

## Calendar Output Format — V6 Production Bible

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

**Derivative Format System (CRITICAL V6 FEATURE):**
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

**Required button markup + banner** — copy verbatim from `skills/heygen-elevenlabs-renderer/references/v6_auto_render_button.html`. That file is the canonical source and already contains the button block, the styles, the JS, AND the `#auto-render-banner` element. Do not re-implement by hand.

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
    </tr>
    <!-- Topic card (repeat per top-tier topic) -->
    <tr>
      <td style="padding:0 32px 16px;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="border:1px solid #e2e5ea;border-radius:8px;">
          <tr>
            <td style="padding:16px 18px;">
              <div style="font-size:11px;color:#C5A258;font-weight:700;letter-spacing:0.5px;text-transform:uppercase;">[Day] · Score [N]/25 · [Funnel: BOFU/MOFU/TOFU]</div>
              <h2 style="margin:6px 0 4px;font-size:17px;line-height:1.3;color:#1B2A4A;">[Topic title with angle]</h2>
              <p style="margin:0 0 12px;font-size:13px;color:#4a5568;">[1-sentence "why this works" — data citation. e.g., "GSC rising query +180% WoW + matches recent EPA permit news."]</p>
              <a href="https://graehamwatts.github.io/online-content/dashboards/weekly-calendars/[DATE]-production-calendar-v6.html#topic-[slug]" style="display:inline-block;padding:10px 18px;background:#C5A258;color:#1B2A4A;text-decoration:none;font-size:13px;font-weight:700;border-radius:6px;">Open in dashboard →</a>
            </td>
          </tr>
        </table>
      </td>
    </tr>

    <!-- Next Tier -->
    <tr>
      <td style="padding:16px 32px 8px;border-top:1px solid #e2e5ea;">
        <div style="display:inline-block;padding:4px 10px;background:#1B2A4A;color:#ffffff;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;border-radius:4px;">NEXT TIER · STRONG ALTS</div>
        <p style="margin:8px 0 16px;font-size:13px;color:#718096;">Solid backup options (Score 17-21). Use if top tier doesn't fit your week.</p>
      </td>
    </tr>
    <!-- Repeat topic card pattern for next-tier topics -->

    <!-- Third Tier -->
    <tr>
      <td style="padding:16px 32px 8px;border-top:1px solid #e2e5ea;">
        <div style="display:inline-block;padding:4px 10px;background:#718096;color:#ffffff;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;border-radius:4px;">THIRD TIER · CONSIDER</div>
        <p style="margin:8px 0 16px;font-size:13px;color:#718096;">Below the strong threshold but still data-backed (Score 12-16). Use if you want variety.</p>
      </td>
    </tr>
    <!-- Repeat topic card pattern for third-tier topics -->

    <!-- Footer -->
    <tr>
      <td style="padding:24px 32px;background:#f4f5f7;border-top:1px solid #e2e5ea;">
        <p style="margin:0;font-size:12px;color:#718096;">Need the full production calendar (Jason/Peter view)? <a href="https://graehamwatts.github.io/online-content/dashboards/weekly-calendars/[DATE]-production-calendar-v6.html" style="color:#1B2A4A;text-decoration:underline;">Open the dashboard</a>.</p>
      </td>
    </tr>
  </table>
</body>
</html>
```

#### Daily Email Format

Sent each weekday morning (Mon-Fri). Single topic — today's. Plus tomorrow's preview.

```
Subject: Today's content topic — [Topic Title]

Today's pick (from this week's calendar):
• [Topic title]
• Score [N]/25 · [Funnel] · [Format]
• Why: [1-sentence data citation]
• [Open in dashboard →]

Tomorrow's preview:
• [Tomorrow's topic title] — [Format]

[View full week →]
```

Same email-safe HTML structure as Monday email but condensed to one topic + tomorrow's preview.

#### Generation Timing

- **Monday email:** generated and sent Sunday night or Monday 6am Pacific by `scheduled-tasks` skill triggering `content-calendar` weekly run
- **Daily emails:** generated and sent each weekday at 6am Pacific by `scheduled-tasks` triggering a daily-email-only run that pulls from the existing weekly calendar JSON

The actual delivery (SMTP / Gmail API / SendGrid / etc.) is handled by a separate emailer. content-calendar's job is to GENERATE the email HTML and write it to a known path; the emailer picks it up and sends it.

Output paths:
- `outputs/emails/weekly-{YYYY-MM-DD}-blog.html` — Monday email
- `outputs/emails/daily-{YYYY-MM-DD}-blog.html` — Daily email

#### Implementation Status

The email format spec above is canonical (April 2026). The actual generation logic (Python script that produces the email HTML from the weekly calendar JSON) does NOT exist yet — flagged as a Phase 5 follow-on. When implemented, it should live at:
`skills/content-calendar/templates/weekly-email-builder.py`

Until that script exists, this section is a forward-looking spec. The hosted dashboard works today; the email is the next surface.

### Build Process (Bash `\!` Escaping Fix)

When building the HTML in bash, the `\!` character gets escaped to `\\!` inside heredocs. This breaks
`<\!DOCTYPE>` and `<\!-- -->` tags. **Always** run a Python post-processing cleanup step after assembly:
```python
content = content.replace('<\\\!', '<' + chr(33))
```
Use `chr(33)` for `\!` in Python string construction to avoid the issue entirely.

### Calendar Rules

- Plan 4-5 content pieces per week (Graeham's sustainable pace based on historical data)
- At least 3 should be Shorts/Reels (highest engagement format per benchmarks)
- At least 2 should target LLM Search (fact-dense, data-heavy — see social-media-analyzer
  skill for the full SEO vs LLM Search optimization breakdown)
- At least 1 should be inspired by a competitor video that performed well
- At least 1 should target a rising Search Console query
- Include at least 1 BOFU piece every week (this is what generates leads)
- Never recommend generic topics — every topic must have a local angle and data citation
- Carry forward unfulfilled high-scoring topics from last week's calendar
- Every day MUST have derivative scripts for ALL platforms (YT Long, YT Short, IG Reel x2,
  IG Carousel, TikTok, Blog, GMB, FB) — not just the core asset
- Every core asset script MUST include inline shot direction tags
- Every core asset MUST have an Editing Notes block for Jason
- Every core asset MUST have an ElevenLabs SSML block
- Every core asset MUST have a 🚀 Full Auto-Render button wired to the local webhook handler
- At least 2 days should include AI Video Prompts (Seedance 2.0 / Kling) for hook shots
- Include an email newsletter day summarizing the week's content themes

### Handoff to Script Writing

In V6, the calendar IS the script output — derivative scripts are generated inline for every
format, not as a separate step. The Production Map tab contains complete scripts, captions,
shot directions, SSML, and AI video prompts for every day and every platform.

However, if the user wants to regenerate or refine a specific day's scripts, they can say
"rewrite scripts for [day]" and the content-creation-engine takes over with the topic
and angle already defined in the calendar.

For topics that would benefit from AI-generated video (cinematic ads, pattern-interrupt hooks,
listing showcase clips), include AI Video Prompt blocks directly in the calendar output AND
note: "CINEMATIC HOOK OPPORTUNITY: This topic would work as a Seedance 2.0 scroll-stopper."
Use the cinematic-hooks skill for generating those prompts.

## Running the Calendar

When the user triggers this skill, follow this sequence:

1. **Goal Clarifier (ASK FIRST, before touching any data source).** Before pulling data or scoring, ask ONE question:

   > "Before I build the calendar, what's the goal this week?
   > (a) **Lead gen bias** — shift to 20/30/50 TOFU/MOFU/BOFU, prioritize high-intent GSC queries and CTA-friendly topics
   > (b) **Audience growth bias** — shift to 50/25/25, prioritize rising-trend topics and cinematic-hook opportunities
   > (c) **New listing launch** — one BOFU piece wraps around the listing, normal mix for the rest
   > (d) **Market education push** — balanced 35/35/30, lean into AB 1482 / market stats / legal explainers
   > (e) **Balanced default** — 40/30/30, follow what the scoring says"

   The answer changes funnel mix targets AND re-weights Criterion #1 (Performance Signal) and Criterion #3 (Audience Intent) in scoring. Do NOT run data pulls or scoring until this is answered. If the user says "just do the default," proceed with (e).

2. **Check for recent data.** Look for the most recent social-media-analyzer report/dashboard
   and any recent Reddit scrape outputs. If data is less than 7 days old, use it. If older,
   pull fresh data from Windsor.

3. **Pull Search Console data.** This is always pulled fresh — search trends change weekly.
   Windsor connector `searchconsole`, `last_7d` AND `last_28d` for trend comparison.

4. **Analyze performance patterns.** Identify top content types, topics, and posting times
   from the last 7-14 days.

5. **Check competitor intelligence.** Use the most recent competitor analysis from
   social-media-analyzer, or run a quick check via Apify/Supadata/Chrome if none exists.

6. **Scan for market context.** Quick web search for current mortgage rates, local market
   news, and any timely hooks.

7. **Generate topic candidates.** Combine all signals into a candidate list of 12-15 topics.

8. **Score and rank (Opportunity Score).** Apply the 5-criteria Opportunity Score rubric (25 pts max). Sort by score descending. **Re-weight per Goal Clarifier answer:**

   | Goal Answer | Performance Signal | Search Demand | Audience Intent | Competitive Gap | Timeliness |
   |---|---|---|---|---|---|
   | (a) Lead gen | ×1.3 | ×1.0 | ×1.3 | ×1.0 | ×1.0 |
   | (b) Audience growth | ×1.0 | ×1.3 | ×1.0 | ×1.3 | ×1.0 |
   | (c) Listing launch | ×1.0 | ×1.0 | ×1.0 | ×1.0 | ×1.3 |
   | (d) Market education | ×1.1 | ×1.2 | ×1.1 | ×1.0 | ×1.0 |
   | (e) Balanced | ×1.0 | ×1.0 | ×1.0 | ×1.0 | ×1.0 |

   After re-weighting, cap each criterion at 5 and total at 25.

9. **Compute priority axes (business / brand / engagement).** For each topic, derive three priority readouts (0-5 each) from the criteria so Graeham can see at a glance how each topic ladders up to his three goals:

   - `business_priority` = weighted_avg(Performance Signal × 0.3, Search Demand × 0.35, Audience Intent × 0.35)
   - `brand_priority` = weighted_avg(Competitive Gap × 0.5, Timeliness × 0.3, Local_relevance_from_intent × 0.2)
   - `engagement_priority` = weighted_avg(Performance Signal × 0.6, Timeliness × 0.4)

   Round to 1 decimal. These are READOUTS, not separate scores — they help Graeham pick between two topics with similar Opportunity totals but different strengths.

10. **Classify time-decay band.** Tag each topic with a `time_decay_band`:

    - `breaking_48hr` — news broke in last 2-3 days, story window closes fast. AUTO-BUMPS to Monday/Tuesday regardless of other scores.
    - `weekly_window` — relevant this week but fine through Friday (rate changes, seasonal events, listing launches).
    - `seasonal_4wk` — holds relevance for up to a month (market trend explainers, seasonal tips).
    - `evergreen` — no time pressure (buyer education, process guides).

    This is SEPARATE from the Timeliness score. A topic can be `weekly_window` with Timeliness=5 (high urgency this week) or `evergreen` with Timeliness=2 (no urgency ever).

11. **Detect cross-topic conflicts.** Before finalizing the plan, group topics by `pillar + market + primary_angle`. If any two topics in the top 5 share all three, flag `topic_conflict: true` on both and emit a conflict note. Graeham picks one or splits the angles.

12. **Build the calendar.** Select the top 4-7 topics (respect funnel mix from Goal Clarifier + `time_decay_band` ordering). Assign to days — breaking_48hr topics pin to Monday/Tuesday. Assign formats and platforms. Write:

    - JSON: `outputs/calendar-data/calendar-{YYYY-MM-DD}.json` (machine-readable, full scoring breakdown + priority axes + time_decay + conflicts)
    - HTML: `online-content/dashboards/weekly-calendars/{YYYY-MM-DD}-production-calendar-v6.html` per Rule 14 in `content-creation-engine/references/weekly-calendar-rules.md`

13. **Present to user + accept overrides.** Show the calendar with FULL scoring visible (per Rule 14). Ask: "Accept as-is, or override? Tell me which topics to swap, drop, or add." If Graeham overrides, capture it:

    ```json
    "user_override": {
      "original_rank": 3,
      "final_rank": 1,
      "reason": "faster to ship this week"
    }
    ```

    Write the override back into the topic's JSON record. This preserves the audit trail and lets next week's planner learn preferences over time.

14. **Hand off to content-creation-engine.** For each accepted topic, route to `content-creation-engine` Phase R (per-topic research) → Phase 3 (Intent Score) → Phase G (multi-platform package). The single-topic dashboard reads `calendar-{date}.json` to populate Rule 13's Table A.

## Fair Housing Guardrails

Same rules as the content-creation-engine — these are non-negotiable:

- NEVER recommend content that describes neighborhoods by demographics
- NEVER use "safe / good areas / family-friendly / up-and-coming" as proxy language
- NEVER rank or rate schools as a selling point
- Neighborhood content is limited to: property features, price ranges, market trends, lot sizes, amenities, architecture, housing stock age, HOA structure, zoning, new development, commute/transit facts, and walkability

## Historical Calendar Tracking

After generating each calendar, save it to: `outputs/calendar-data/calendar-{YYYY-MM-DD}.json`

On the next run, load the previous calendar to:
- Check which recommended topics Graeham actually created (recommendation-to-creation rate)
- Carry forward high-scoring topics that weren't created yet
- Track prediction accuracy: did recommended topics outperform when created?
- Read `user_override` fields to learn Graeham's preference patterns (which goal clarifier he tends to pick, which topics he tends to override up, which time-decay bands he prioritizes)

This feedback loop makes the calendar smarter over time.

## Example Prompts

- "What should I post this week?"
- "Plan my content calendar for the next 7 days"
- "What topics should I focus on based on my data?"
- "What are my competitors posting that I'm not?"
- "Give me a data-driven content plan"
- "What's trending in my market that I should cover?"
- "My engagement dropped last week — what should I change?"
- "Build me a content calendar focused on lead generation"
- "What content gaps do I have vs my competitors?"

---

## Publishing via Composio (canonical pattern)

> **Read first:** [`shared-references/publishing-via-composio.md`](../shared-references/publishing-via-composio.md) — single source of truth for ALL skills.

After generating the weekly-calendar dashboard HTML output, publish via Composio to `Graehamwatts/online-content` so the agent gets a permanent hosted URL.

**Account:** `github_spar-devata`  
**Owner:** `Graehamwatts`  
**Repo:** `online-content`  
**Branch:** `main`  
**Path pattern:** `dashboards/weekly-calendars/YYYY-MM-DD-production-calendar.html`  
**Hosted URL pattern:** `https://graehamwatts.github.io/online-content/dashboards/weekly-calendars/YYYY-MM-DD-production-calendar.html`

**Tool to use:** `GITHUB_COMMIT_MULTIPLE_FILES` (atomic commit, retry-safe).

```python
result, error = run_composio_tool(
    tool_slug='GITHUB_COMMIT_MULTIPLE_FILES',
    arguments={
        'owner': 'Graehamwatts',
        'repo': 'online-content',
        'branch': 'main',
        'message': 'descriptive commit message',
        'upserts': [{'path': 'dashboards/weekly-calendars/YYYY-MM-DD-production-calendar.html', 'content': html_content, 'encoding': 'utf-8'}]
    },
    account='github_spar-devata'
)
```

**HARD RULES:**
- Do NOT use the legacy GitHub Contents API with PAT or `javascript_tool` chunked uploads (replaced 2026-05-03).
- Do NOT use GitHub Desktop or `git push` from the agent sandbox.
- Run the brand-integrity check before push (see shared doc — blocks DRE# 01 leaks).
- After commit, give the user BOTH the hosted URL and the local `computer://` link.

See `shared-references/publishing-via-composio.md` for full details, common pitfalls, and verification flow.


## Canonical Weekly Calendar Template (v5.4 — locked in May 2026)

> **This is the format moving forward.** Live reference: [`Graehamwatts/online-content/dashboards/weekly-calendars/2026-05-11-production-calendar.html`](https://github.com/Graehamwatts/online-content/blob/main/dashboards/weekly-calendars/2026-05-11-production-calendar.html). Hosted at: https://graehamwatts.github.io/online-content/dashboards/weekly-calendars/YYYY-MM-DD-production-calendar.html

**Template structure (top to bottom):**

1. **Hero** — week date range, opportunity-score pill chips, BOFU mix label.
2. **Audience tabs** (sticky) — Research / Blog Track / Peter / Show Everything. Tab state persists in URL hash (`#audience-blog`, `#audience-peter`).
3. **Preview banner** — explains v5 features + auto-refresh time.
4. **Live Data Layer** — 8 source cards (Composio IG, Composio YT, DataForSEO, n8n Local News, GSC via Windsor, Reddit via Apify, YT Comment Mining, Zillow Q&A).
5. **Full Research Data panel** (collapsed by default; toggle to expand):
   a. **Brushable time-series charts** (ApexCharts via CDN):
      - Instagram Activity Over Time (weekly likes + posts, dual axis, drag bottom slider to zoom)
      - YouTube Activity Over Time (weekly views + videos, dual axis, drag bottom slider to zoom)
      - Engagement Rate Per Post Per Week (avg per-piece for IG + YT)
   b. Instagram 25/100-row table (live via Composio Meta Graph API)
   c. YouTube 15/50-video table with stats (live via YouTube Data API v3)
   d. GSC topic-targeted queries
   e. Reddit demand signals
   f. Zillow Q&A
   g. MLS pull
   h. Macro Rates & Permits
   i. DataForSEO SERP queue status
   j. Convergence — Why each day picked (with source counts and scores)
6. **5 Day Cards (week grid)** — clickable to filter Blog Track + Peter sections to one day.
7. **Weekly Strategy** — funnel mix bar + cross-platform handoff notes.
8. **Blog Track section** — 5 daily-items, each with prominent topic title + hook + format pill rows. Pills copy Claude-ready prompts.
9. **Peter section** — same pattern, video formats, with Image-Gen pills for carousels.
10. **Footer** — DRE 01466876, contact, refresh schedule, Composio commit reference.

**Hard rules (don't drift from this):**

- **Brand identity** — pull from `shared-references/identity.json`. Run the blocklist verifier before every push (see `scripts/verify_brand_identity.py` and `shared-references/publishing-via-composio.md`).
- **No "Eric" anywhere** — Eric is no longer with the team. Use "Blog Track" / "blog producer" for the role label.
- **Brand colors:** navy `#1B2A4A`, gold `#B8860B` (saturated v5.4), purple `#6a1b9a`, red `#9f1239`, blue `#2563EB`. Grid lines `#cbd5d8`.
- **Typography:** Plus Jakarta Sans (display), DM Sans (body).
- **Pill button mapping:** every `onclick="copyPrompt('id')"` must have a matching key in the `PROMPTS` JS object. The on-load audit logs missing IDs to the console — `[v5 audit] All N pill buttons have valid prompts.`
- **Audience tab state:** `#audience-blog`, `#audience-peter`, `#audience-research`, `#audience-all`. Anchor links in emails MUST use these.
- **Push via Composio** — see [`shared-references/publishing-via-composio.md`](../shared-references/publishing-via-composio.md). Never GitHub Desktop, never `git push` from sandbox.

**File path convention:**
- Active: `dashboards/weekly-calendars/YYYY-MM-DD-production-calendar.html` where `YYYY-MM-DD` = the Monday the calendar covers OR the Monday the auto-refresh fires.
- Old preview/single-topic dashboards have been deleted (May 2026 cleanup).

**When the Mon scheduled task runs**, it should write to this exact path and replace the previous week's file (or create the next-week file alongside if you want to keep a 2-week rolling history — your call).

---
