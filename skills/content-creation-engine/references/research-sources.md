# Research Sources — Content Opportunity Discovery

This document defines every data source the Content Creation Engine taps during Phase R (Research & Discover). Each source includes: what to pull, how to pull it, what to look for, and how findings feed into the Content Opportunity Report.

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
- Via Chrome: Log into MLSListings.com → Market Statistics → Select each market area
- Pull current month stats + prior month + same month last year for trend analysis

**What to look for:**
- Any metric that moved ≥5% MoM or ≥10% YoY — that's a content trigger
- Inventory spikes or drops (signals shifting market conditions)
- Sale-to-list ratio above 100% (bidding wars) or below 95% (price reductions)
- DOM changes — getting faster = hot market, slower = cooling

**Emoji:** 📊

---

## 2. Google Search Console

**What:** What people are actually searching to find Graeham's website.
**How to pull:**
- Via Windsor MCP: `get_data` with connector `searchconsole`, account_id `sc-domain:graehamwatts.com`
- Pull: top queries by clicks AND impressions, last 7 days
- Compare to prior 7-day period to identify rising queries

**What to look for:**
- Rising queries (impressions up ≥20% week-over-week) — people want this content
- High-impression / low-click queries — Graeham ranks but the content isn't compelling enough (rewrite opportunity)
- New queries that weren't appearing before — emerging demand
- Location-specific queries ("homes for sale in [city]", "[city] real estate market")

**Emoji:** 🔍

---

## 3. Local Government (City of East Palo Alto)

**What:** City council actions, development projects, zoning changes, permits — anything that affects property values or neighborhood character.

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

**Emoji:** 🏛️

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

**Emoji:** 📰

---

## 5. Social Performance Data

**What:** Which of Graeham's recent posts performed best — and what patterns emerge.

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
- Comment sentiment — what questions are people asking?
- Time-of-day and day-of-week patterns

**Emoji:** 📱

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

**Emoji:** 📈

---

## 7. BOFU Keyword Data

**What:** Bottom-of-funnel keywords from the content engine's existing keyword database.

**How to pull:**
- Read `references/phases/bofu-query-generator/instructions.md` for the full keyword matrix
- Cross-reference with Search Console data to see which BOFU terms are actually driving traffic
- Check `references/topic-history.json` for recently covered BOFU topics (avoid repeats)

**What to look for:**
- High-intent keywords not yet covered by existing content
- BOFU keywords with rising Search Console impressions (demand growing)
- Keywords aligned with current market conditions (e.g., "sell my house fast in EPA" during a hot market)
- Seasonal BOFU terms (tax implications content in Q1, school-district content in spring)

**Emoji:** 🎯

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

**Emoji:** 🕵️

---

## Content Opportunity Scoring Rubric

Each finding from the sources above is scored on a 1-10 scale:

| Criterion | Max Points | Scoring Guide |
|---|---|---|
| **Timeliness** | 3 | Breaking/this-week = 3, This month = 2, Evergreen = 1 |
| **Audience Relevance** | 3 | Direct property value impact = 3, Lifestyle/community = 2, Tangential = 1 |
| **Content Gap** | 2 | Never covered = 2, Covered >4 weeks ago = 1, Recently covered = 0 |
| **Engagement Potential** | 2 | Similar topics got high engagement = 2, Average = 1, Low-engagement pattern = 0 |

**Threshold:** Items scoring ≥7 get ⭐ RECOMMENDED tag in the Content Opportunity Report.

---

## Source Reliability Notes

- **MLS data** is the gold standard — always trust MLS stats over news articles or anecdotal reports
- **Search Console** reflects actual demand from real people — weight it heavily
- **Local government** sources are high-value but low-frequency — a single city council vote can be a week's worth of content
- **News** is supplementary — verify facts against primary sources before building content
- **Social performance** tells you what works, not what's new — use it to inform format choices, not topic choices
- **Google Trends** is directional, not precise — a spike means "more interest than usual," not "everyone is searching this"
- **BOFU keywords** are strategic, not reactive — use them to fill gaps between timely topics
- **Competitor analysis** is inspiration, not imitation — identify gaps they're missing, don't copy their content
