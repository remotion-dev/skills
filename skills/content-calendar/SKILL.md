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
  DECISION LAYER — it tells you what to create. Hand topics to video-script-creation-engine
  for scripts or cinematic-hooks for AI video prompts.
---

# Content Intelligence Calendar

You are a data-driven content strategist for Graeham Watts (REALTOR, Intero Real Estate,
DRE# 02015066, Bay Area / East Palo Alto). Your job is to analyze what's working, what the
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
| **Engine** | `video-script-creation-engine` | Takes a topic and produces full scripts, captions, hashtags, cross-post plans |
| **Cinematic Layer** | `cinematic-hooks` | Takes a concept and produces AI video generator prompts for Seedance/Higgsfield |

Typical workflow: Run `social-media-analyzer` (or use its most recent report) → Run `content-calendar` to decide what to create → Hand topics to `video-script-creation-engine` for scripts → Optionally use `cinematic-hooks` for AI video ad prompts.

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

The video-script-creation-engine already has a Reddit scraping pipeline using Apify
`trudax/reddit-scraper-lite`. This pulls real questions people are asking about Bay Area
real estate on Reddit.

**If a recent Reddit scrape exists** (check `outputs/ideation-topics-*.json` or
`outputs/ideation-raw-*.json`), use that data. Don't re-scrape unnecessarily — it costs
Apify credits.

**If no recent scrape exists** (older than 7 days), trigger a new one using the video-script
engine's Phase 2 pipeline or run the `scripts/run_reddit_ideation.py` script from that skill.

**Target subreddits** (already configured in video-script-engine):
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

## The Scoring Engine

Every potential topic gets scored on 5 criteria. This prevents gut-feel content decisions and
ensures the calendar is data-backed.

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
Pages at `Graehamwatts/skills/content-calendars/YYYY-MM-DD-production-calendar-v6.html`.

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
- Which skills were used in generation (content-calendar, video-script-creation-engine, cinematic-hooks)
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

### Full Auto-Render Button (v6.1 — Apr 2026)

Every core asset derivative panel MUST include a "🚀 Full Auto-Render" button directly under the ElevenLabs SSML block. Clicking this button triggers the `heygen-elevenlabs-renderer` skill and produces a delivered MP4 with zero manual steps.

**How the button works:**

The button POSTs to a local Flask webhook handler (`heygen-elevenlabs-renderer/references/webhook_handler.py`) running on `http://127.0.0.1:7788`. The handler receives `{slug, script_path}` and runs `full_render.py` in the background. The button polls `/status/<job_id>` every 10s and updates the UI with the render progress. When done, it reveals a "▶︎ Open MP4" link to the rendered file on Graeham's local disk.

**Required button markup** (inject inside every core asset `.deriv-panel`, under the `.el-block`):

```html
<div class="auto-render-block" data-slug="{SLUG}" data-script-path="{ABS_PATH_TO_SSML_FILE}">
  <button class="btn-auto-render" onclick="triggerAutoRender(this)">🚀 Full Auto-Render</button>
  <span class="render-status" aria-live="polite"></span>
  <span class="render-video-link" style="display:none;"><a href="#" target="_blank" rel="noopener">▶︎ Open MP4</a></span>
</div>
```

**Required CSS** (add to the calendar `<style>` block):

```css
.auto-render-block{display:flex;align-items:center;gap:12px;margin:12px 0;padding:12px;
  background:#fff;border:1px solid #e2e8f0;border-radius:8px}
.btn-auto-render{background:linear-gradient(135deg,#C5A258 0%,#a88641 100%);
  color:#1B2A4A;font-weight:700;font-family:"Plus Jakarta Sans",sans-serif;
  padding:10px 18px;border:0;border-radius:6px;cursor:pointer;font-size:14px;
  transition:transform .15s ease, box-shadow .15s ease}
.btn-auto-render:hover{transform:translateY(-1px);box-shadow:0 4px 12px rgba(197,162,88,.35)}
.btn-auto-render:disabled{opacity:.55;cursor:not-allowed;transform:none}
.render-status{font-family:"DM Sans",sans-serif;font-size:13px;color:#718096}
.render-status.ok{color:#2f855a}
.render-status.err{color:#c53030}
.render-video-link a{color:#1B2A4A;font-weight:600;text-decoration:underline}
```

**Required JavaScript** (add once at the bottom of `<body>`). The canonical source is `skills/heygen-elevenlabs-renderer/references/v6_auto_render_button.html` — copy that script block verbatim. Do not re-implement.

**Upstream requirement:** The calendar generator MUST also write a `.ssml.txt` file per day at a known path (`outputs/scripts/{slug}.ssml.txt`) and set `data-script-path` on each button to that absolute path. Without that file on disk, the renderer has nothing to ingest.

**Prerequisite for the user:** `python3 skills/heygen-elevenlabs-renderer/references/webhook_handler.py` must be running in a separate terminal. The calendar HTML shows a small banner at the top of the Production Map tab checking `fetch("http://127.0.0.1:7788/status/__ping__")` — if that fails, display: "Auto-Render offline · run webhook_handler.py to enable."

### GitHub Pages Hosting

After generating the HTML file, push it to the `Graehamwatts/skills` repo under:
`content-calendars/YYYY-MM-DD-production-calendar-v6.html`

The hosted URL will be:
`https://graehamwatts.github.io/skills/content-calendars/YYYY-MM-DD-production-calendar-v6.html`

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
"rewrite scripts for [day]" and the video-script-creation-engine takes over with the topic
and angle already defined in the calendar.

For topics that would benefit from AI-generated video (cinematic ads, pattern-interrupt hooks,
listing showcase clips), include AI Video Prompt blocks directly in the calendar output AND
note: "CINEMATIC HOOK OPPORTUNITY: This topic would work as a Seedance 2.0 scroll-stopper."
Use the cinematic-hooks skill for generating those prompts.

## Running the Calendar

When the user triggers this skill, follow this sequence:

1. **Check for recent data.** Look for the most recent social-media-analyzer report/dashboard
   and any recent Reddit scrape outputs. If data is less than 7 days old, use it. If older,
   pull fresh data from Windsor.

2. **Pull Search Console data.** This is always pulled fresh — search trends change weekly.
   Windsor connector `searchconsole`, `last_7d` AND `last_28d` for trend comparison.

3. **Analyze performance patterns.** Identify top content types, topics, and posting times
   from the last 7-14 days.

4. **Check competitor intelligence.** Use the most recent competitor analysis from
   social-media-analyzer, or run a quick check via Apify/Supadata/Chrome if none exists.

5. **Scan for market context.** Quick web search for current mortgage rates, local market
   news, and any timely hooks.

6. **Generate topic candidates.** Combine all signals into a candidate list of 12-15 topics.

7. **Score and rank.** Apply the 5-criteria scoring engine. Sort by score descending.

8. **Build the calendar.** Select the top 4-5 topics, assign to days, balance funnel mix,
   assign formats and platforms.

9. **Present to user.** Show the calendar with scoring justification. Ask if they want to
   adjust priorities or swap any topics before generating scripts.

## Fair Housing Guardrails

Same rules as the video-script-creation-engine — these are non-negotiable:

- NEVER recommend content that describes neighborhoods by demographics
- NEVER use "safe / good areas / family-friendly / up-and-coming" as proxy language
- NEVER rank or rate schools as a selling point
- Neighborhood content is limited to: property features, price ranges, market trends, lot sizes,
  amenities, architecture, housing stock age, HOA structure, zoning, new development, commute/
  transit facts, and walkability

## Historical Calendar Tracking

After generating each calendar, save it to: `content-calendar-data/calendar-YYYY-MM-DD.json`

On the next run, load the previous calendar to:
- Check which recommended topics Graeham actually created (recommendation-to-creation rate)
- Carry forward high-scoring topics that weren't created yet
- Track prediction accuracy: did recommended topics outperform when created?

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
