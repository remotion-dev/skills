# Market Update Narrative Module

Engine-internal module. Used by `content-creation-engine` Phase G (Generate Content) when the topic is a **market update** — weekly/monthly market reports, seasonal analyses, neighborhood market reads, "is now a good time to buy/sell" content, year-over-year comparisons, or any content where the deliverable is built around MLS data.

This module is the *narrative framing* layer. It does NOT analyze MLS data from scratch — that's `cma-generator`'s job (for valuations) or Phase R's job (for per-topic research data). This module turns analyzed numbers into the story arc that backs a market update.

> **Boundary check vs cma-generator:** `cma-generator` produces a branded valuation report for a specific property. This module produces narrative content (blog / newsletter / script) about market conditions for an audience. They share comp data sources but their outputs are unrelated.

---

## ⚠️ STOP — Run the Freshness Gate Before Anything Else

**This is the most important section in this module. Read it before touching any data.**

Before generating any market update, run this four-step check:

**Step 1 — Find the last market update for this market scope**
Open `references/topic-history.json`. Search `history` AND `in_production` for any topic with `type: "market_recap"` or `angle: "market-update"` for the same geographic scope (EPA, Peninsula, San Mateo County, etc.).

**Step 2 — Check what data period it used**
Look for the `data_period` field on that entry (e.g., `"as_of": "2026-03"`). If the entry doesn't have one, check the script itself for the stat dates.

**Step 3 — Check what data period you have NOW**
What MLS period does the user's data actually cover? If they're providing data and haven't specified, ask: "What time period does this MLS data cover?" Do not assume.

**Step 4 — Compare and route**

| Data period comparison | Verdict | Action |
|---|---|---|
| Data period IS NEW (different period than last recap) | ✅ Proceed with Recap | Run Steps 1-4 below, write the narrative outline |
| Data period IS THE SAME as last recap | 🚫 Block Recap | Route to Deep-Dive mode (see Deep-Dive Angle Bank section) |
| No prior recap exists for this market | ✅ Proceed with Recap | No prior anchor to compare against |
| Data period is ambiguous | ⚠️ Ask before generating | "What month does this data cover?" |

**Why this gate exists:** EPA doesn't generate enough new closings each month for a reliable fresh recap. The May 2026 recap used March 2026 data. Running a "June 2026 Market Update" with the same March numbers and putting June's date on it misleads homeowners. A deep-dive on a specific angle from the May recap is more accurate, more useful, and entirely distinct content — it doesn't need new data.

---

## Market Update Format Taxonomy

Two fundamentally different content types share the "market update" label. The gate above determines which one you're producing.

### Format 1: Quarterly Recap
**When to use:** A new MLS data period has closed that wasn't covered in the last recap. Meaningful calendar shift (end of quarter, rate move, seasonal inflection). Data is genuinely fresh.

**What it covers:** Full stat roundup — median sale price, DOM, list-to-sale ratio, inventory, price per sqft, YoY comparisons. The "whole picture" update.

**Audience:** Anyone thinking about buying or selling in the next 90 days.

**Frequency:** Once per quarter, or when data materially changes. NOT monthly unless monthly data is genuinely fresh.

**Generates:** 3-5 deep-dive angles as a byproduct (see rotation enforcement below).

### Format 2: Monthly Deep-Dive
**When to use:** Last recap's data period hasn't changed. OR the user wants to go deeper on one angle the recap surfaced. No new MLS data required.

**What it covers:** ONE data story from the recap, explored in full. Context, implications, buyer/seller action. NOT a re-run of the whole stat sheet.

**Audience:** Specific — sellers, buyers, landlords, or investors depending on the angle.

**Frequency:** Every month between quarterly recaps. The deep-dive queue (see topic-history.json `upcoming_deep_dives`) tells you which angle to use.

**Examples of valid deep-dives:**
- Pricing split: why some homes sell in 32 days and others sit at 66
- EPA value hold: how EPA held value while San Mateo County median fell
- AB 1482 landlord exemption: the exact lease language that preserves the SFR exemption
- Rent-vs-sell math: running the numbers on a specific price tier
- Entry-price window: what's actually available and moving at $700K–$900K in EPA

---

### Format 3: Bi-Monthly Market Update (Bay Area + EPA Combined)

**When to use:** Every two months, on a fixed cadence (June, August, October, December, February, April). Covers BOTH Bay Area (San Mateo County / Peninsula) AND East Palo Alto in a single production dashboard. Each update uses a DIFFERENT ANGLE from the Bi-Monthly Angle Rotation Bank — never the same angle two updates in a row.

**What it covers:** Two videos in one production run — one Bay Area video, one EPA video. Each video has a completely distinct hook, data story, and audience frame. They may share the same production shoot day but ship as separate YouTube uploads.

**Audience:** Varies by angle assignment from the rotation bank. The angle bank pre-assigns audience for each slot in the rotation.

**Frequency:** Every two months. Check `topic-history.json → bi_monthly_history` for the last angle used and the next angle due.

**Key rule — the Imagination Check:** Before generating any bi-monthly script, run the Bi-Monthly Freshness Gate (below). The gate rejects any angle that's been used in the last 3 bi-monthly updates AND requires the creative execution (hook phrasing, visual approach, stat emphasis) to be meaningfully different even when using data from the same time period.

**Gemini Visual System:** Every bi-monthly update includes a Gemini-generated thumbnail concept, a Gemini-generated research visual brief (infographic layout), and Gemini multimodal verification that the new dashboard is visually distinct from the prior one. See the Gemini Visual System section below.

---

## ⚠️ Bi-Monthly Freshness Gate (Format 3 Only)

**Run this BEFORE generating any bi-monthly market update script.** This is the equivalent of the Quarterly Recap freshness gate but for the bi-monthly format.

**Step 1 — Check bi_monthly_history in topic-history.json**
Open `references/topic-history.json` → `bi_monthly_history`. This array tracks every bi-monthly update produced, newest first. Note the `angle_id` of the last 3 entries.

**Step 2 — Check the Bi-Monthly Angle Rotation Bank**
Read `references/bi-monthly-angle-bank.md`. The bank has 6 angles numbered B1–B6. Find the next angle in rotation that does NOT appear in the last 3 `bi_monthly_history` entries.

**Step 3 — Run the Imagination Check**
For the selected angle, verify the CREATIVE EXECUTION will be different from any previous use of that angle. Specifically check:
- Is the hook phrasing distinct from the last time this angle ran?
- Is the primary statistic different (even if the angle type is the same)?
- Is the visual approach (thumbnail concept, B-roll direction) different?
- Is the Gemini thumbnail concept new?

If all three are distinct → ✅ proceed. If any match too closely → pick a fresh variation within the same angle or bump to the next angle in rotation.

**Step 4 — Run the Gemini Imagination Prompt**
Before writing the script, call the Gemini Visual System (see below) to generate:
1. A unique thumbnail concept for this update
2. A unique visual hook description (the first 2 seconds of the video)
3. A "visual differentiation check" comparing this update's visual approach to the previous bi-monthly dashboard

**Step 5 — After generating, log to bi_monthly_history**
Append to `topic-history.json → bi_monthly_history`:
```json
{
  "date": "2026-06-01",
  "slug": "bimonthly-jun-2026-buyer-behavior",
  "angle_id": "B1",
  "angle_name": "buyer-behavior",
  "ba_hook": "First 10 words of Bay Area hook used",
  "epa_hook": "First 10 words of EPA hook used",
  "primary_stat_ba": "104.1% sale-to-list",
  "primary_stat_epa": "14 new listings in May",
  "gemini_thumbnail_concept": "brief description of thumbnail generated",
  "dashboard_url": "https://graehamwatts.github.io/online-content/dashboards/single-topic/..."
}
```

---

## Bi-Monthly Angle Rotation Bank

Six angles. Each bi-monthly update uses the next angle not used in the last 3 updates. Full detail for each angle is in `references/bi-monthly-angle-bank.md`. Summary:

| ID | Angle Name | Bay Area Hook Direction | EPA Hook Direction | Primary Audience | GHL Keywords |
|---|---|---|---|---|---|
| **B1** | Buyer Behavior | What separates winning buyers from losing buyers in the current market | Who is actually buying in EPA and what they're doing differently | Active buyers | MARKET, BUY |
| **B2** | Seller Timing + Pricing | The optimal list date and pricing strategy for the current seasonal window | Why EPA sellers who price within 3% of comp close 2x faster | Thinking-about-selling homeowners | SELL, READY |
| **B3** | Rate Sensitivity | How a 0.25pt rate move changes the qualified buyer pool at each Peninsula price tier | Rate sensitivity at EPA price points vs. the county median | Rate-watching buyers and sellers | NUMBERS, COSTS |
| **B4** | Equity + Wealth Position | Long-term Peninsula homeowner equity analysis; refinance vs. sell math at current prices | EPA homeowners who bought 2012–2018: where their equity actually stands | Long-term owners, move-up sellers | EQUITY, OPTIONS |
| **B5** | Supply Constraint + Inventory | Why Peninsula inventory stays structurally low; Prop 13, zoning, lock-in; what shakes it loose | EPA's new listing count trend + what it would take to rebalance | Buyers frustrated by lack of inventory | EPA, VALUE |
| **B6** | Seasonal Inflection | What this season historically means for Bay Area — and where 2026 is deviating from the pattern | EPA's seasonal pattern vs. county — and the windows buyers/sellers often miss | All audiences, broad awareness | MARKET, WATCH |

**Rotation rule:** Never use the same angle_id as the immediately preceding update OR the one before that. The sequence must have at least 2 different angles between any two uses of the same angle_id.

**Creativity rule:** Even when revisiting an angle (e.g., B1 appears again after 4 updates), the hook phrasing, primary stat, thumbnail visual, and script structure must be materially different. The angle is a FRAME, not a template. Use your imagination within it.

---

## Gemini Visual System (Bi-Monthly Format)

Every bi-monthly market update dashboard includes Gemini-generated visual content. This is what makes each update feel fresh even when the underlying market data moves slowly.

### What Gemini generates for each bi-monthly update:

**1. Thumbnail Concept (required)**
Gemini generates a detailed thumbnail concept that's unique to this update's angle and data story. The concept specifies:
- Foreground element (Graeham's expression/pose direction)
- Background visual (neighborhood aerial, data graphic, lifestyle scene)
- Text overlay (3–5 words max, high contrast)
- Color temperature (warm/cool/neutral — must differ from last update)
- Emotional register (urgent, authoritative, curious, surprising)

**2. Hook Visual Brief (required)**
The first 2–3 seconds of each video are a pattern-interrupt visual. Gemini generates a description for the opening shot that's different from any prior bi-monthly update. This feeds directly into the Seedance 2.0 / Higgsfield AI video prompt.

**3. Research Visual Brief (optional but recommended)**
For the Research tab of the production dashboard, Gemini can generate:
- An infographic layout concept (stat arrangement, color coding, visual hierarchy)
- A chart type recommendation (bar, timeline, split comparison, before/after) that best communicates this update's story
- A "visual metaphor" that could be used in motion graphics (e.g., "a scale tipping" for the pricing split angle)

**4. Visual Differentiation Check (required)**
Before finalizing the dashboard, call Gemini with the previous bi-monthly dashboard's thumbnail concept and this update's concept. Gemini confirms they are visually distinct. If too similar, iterate on the thumbnail until Gemini passes the check.

### How to call Gemini (implementation):

Use the same Gemini API pattern as the `room-redesign` skill (`skills/room-redesign/SKILL.md`). The Gemini model for visual generation is `gemini-2.0-flash-exp` or `gemini-1.5-pro` for text-based visual briefs.

For thumbnail/image generation, use Google's **Imagen 3** via the Gemini API (`imagegeneration@006` or `imagen-3.0-generate-001` model). Pass the thumbnail concept as the prompt.

**Example Gemini prompt for thumbnail concept generation:**
```
You are a real estate content strategist creating a YouTube thumbnail concept for a bi-monthly Bay Area + East Palo Alto market update video.

This update's angle: [ANGLE_NAME]
Primary stat for Bay Area: [STAT]
Primary stat for EPA: [STAT]
Previous update's thumbnail concept: [PREVIOUS_CONCEPT]

Generate a thumbnail concept that:
1. Immediately communicates the angle without requiring the viewer to read text
2. Is visually distinct from the previous update's thumbnail (different color temperature, different background type, different layout)
3. Would stop a scroll in under 1 second
4. Works for both Bay Area and EPA versions (same concept, slightly different text overlay)

Return: (a) Thumbnail concept description, (b) Suggested text overlay (3-5 words), (c) Color palette, (d) Emotional register, (e) Why it's distinct from the previous concept.
```

**Example Gemini prompt for visual differentiation check:**
```
Here are two YouTube thumbnail concepts for consecutive bi-monthly market update videos.

Previous concept: [PREVIOUS_THUMBNAIL_CONCEPT]
New concept: [NEW_THUMBNAIL_CONCEPT]

Are these visually distinct enough that a viewer would immediately recognize them as different videos? Score visual differentiation 1-10 (10 = completely distinct). If below 7, identify what needs to change.
```

### Gemini Imagination Prompt (the creativity enforcement step):

Before writing ANY bi-monthly script, run this Gemini prompt to break out of template thinking:

```
You are a creative director for a real estate agent's bi-monthly market update video series.

Market: Bay Area (San Mateo County) + East Palo Alto, California
Angle for this update: [ANGLE_NAME]
Key data: [PRIMARY_STATS]
Last 3 updates used these hooks: [HOOK_LIST]

Generate 5 completely different opening hook concepts for this update. Each hook must:
1. Start with a specific number, a question, or a surprising statement — never a greeting
2. Be set up in under 15 words
3. Be impossible to confuse with any of the last 3 updates listed above
4. Work for a talking-head video format
5. Have a clear visual complement (what is on screen when this hook plays?)

Then recommend the strongest hook and explain why it would perform better than the others.
```

Use the recommended hook as the script's opening. This is the Imagination Check in practice.

---

## Recap Mode — Steps 1-4

*(Only run these if the Freshness Gate cleared you for a Recap.)*

### Step 1: Read the Numbers

Pull only the metrics relevant to the topic. Do NOT dump the full county stat sheet — narrative content suffers from too many numbers.

For a typical market update, the relevant metrics are:

- **Median sale price** — current period + prior period for direction
- **Median DOM** — current + prior for trend
- **List-to-sale ratio** — tells the story of bidding wars vs price reductions
- **Inventory count** — active vs closed, plus months of supply
- **Price per square foot** — median + range
- **Expired / withdrawn ratio** — signals overpricing or weak demand

Topic-specific drilldowns:
- **Price-direction story** → focus on YoY median change + price-per-sqft trend
- **Speed story** → focus on DOM change + multiple-offer frequency
- **Inventory story** → focus on active inventory MoM + new listing flow + months of supply
- **Bidding war story** → focus on sale-to-list ratio + offer counts + sold-above-list percentage
- **Price reduction wave story** → focus on expired/withdrawn rates + price-reduction frequency + median time-to-reduction

Prefer **median over average** — resists outlier distortion in expensive Bay Area markets where one $20M sale can pull the average up unrealistically.

---

### Step 2: Find the Story

Statistics are not a narrative. The narrative emerges from the *change* and the *divergence* in the numbers. Look for:

**Direction:** Is median trending up, down, or flat compared to the prior period? By how much? Is the change accelerating or decelerating?

**Speed Changes:** Are DOM getting shorter or longer? Is there a divergence between price ranges (entry-level selling fast while luxury sits)?

**List-to-Sale Pattern by Price Bracket:** Homes under $1.5M might be selling at 102% while homes over $3M sell at 95%. That divergence IS the story.

**Expired/Withdrawn Rate:** A high rate of unsold listings signals overpricing or weak demand in a specific segment. Pair with active-listing analysis to identify which segment.

**Seasonal Patterns:** If the data spans multiple months, note seasonal shifts. Bay Area has distinct spring (peak), summer (steady), fall (mini-peak), winter (slowdown) patterns — but these have been disrupted by rate environment in recent years.

**Neighborhood Divergence:** If the data covers multiple neighborhoods, compare them. "Crescent Park is up 8% YoY while Downtown North is flat" is an insight that backs a content piece.

**Price-per-sqft Anomalies:** If the median sale price is up but price-per-sqft is flat, the mix shifted (bigger homes selling). Don't confuse a mix shift for a price increase.

---

### Step 3: Frame for the Audience

The same data tells different stories to different audiences. The module routes the narrative based on the audience input.

**For Buyers:** Lead with what gives them advantage or urgency. Lead with specific data, not "now is a great time to buy" (sounds salesy and dates poorly).

Example arcs:
- "Inventory is up X% YoY, which means more choices and less competition"
- "DOM stretched from X to Y days, which means buyers have time to think"
- "Sold-above-list rate dropped from X% to Y%, you don't need to overpay anymore"
- "Inventory is the lowest in Z years, plan for competition"

**For Sellers:** Lead with what supports their position or sets expectation.

Example arcs:
- "Median sold price up X% YoY in [market], with sale-to-list ratio at Y% — sellers in [area] are getting their asking price"
- "DOM stretched from X to Y days, plan for a longer marketing window"
- "Price reductions on active listings up X% MoM, sellers who price aggressively are sitting"

Avoid urgency tactics ("sellers should rush to list before the market changes"). Frame data as helping sellers position correctly.

**For Both / General Audience:** Lead with the single most surprising or actionable stat. Frame it neutrally.

**For Investors / Specific Subsegments:** Narrow the data to what's relevant — investors care about cap rates and rental yield, relocators care about housing costs vs origin city, first-time buyers care about price tier they can access.

---

### Step 4: Output Format

The module returns a **structured narrative outline** the script-writer Phase 5 then renders into the final format (blog / newsletter / video script / social).

```json
{
  "topic_slug": "epa-market-update-q2-2026",
  "topic_title": "East Palo Alto Market Update — Q2 2026",
  "format": "quarterly_recap",
  "audience": "sellers",
  "market_scope": "East Palo Alto",
  "time_window": "Q1 2026 vs Q1 2025",
  "data_period": "2026-Q1",
  "data_source": "research-{topic-slug}-{ts}.json",
  "headline_metric": {
    "metric": "median_sale_price",
    "current": "$1.42M",
    "prior": "$1.36M",
    "delta": "+4.4%",
    "narrative_anchor": "EPA's median ticked up 4.4% YoY, even as San Mateo County overall slipped 8.4%."
  },
  "supporting_metrics": [
    { "metric": "DOM", "current": "32 days", "prior": "66 days", "story": "dramatically faster" },
    { "metric": "list_to_sale_ratio", "current": "104%", "prior": "101%", "story": "buyers competing" },
    { "metric": "active_inventory", "current": "12 listings", "prior": "8 listings", "story": "modest recovery" }
  ],
  "the_story": "EPA is one of the few Peninsula markets that didn't lose value year-over-year. Median up, DOM cut in half, sale-to-list above 100%.",
  "the_angle": "EPA held while the county slipped — and the homes selling fast vs sitting are in two entirely different categories based on pricing.",
  "audience_specific_takeaway": "Well-priced, well-staged homes in EPA are closing in 32 days. Everything else is sitting at 66. The gap between those two outcomes comes down to one decision made at listing.",
  "deep_dive_queue": [
    {
      "slug": "epa-pricing-split-deep-dive",
      "title": "Two Markets in EPA: The 32-Day Home vs the 66-Day Home",
      "angle": "pricing-split",
      "audience": "sellers",
      "ghl_keyword": "READY",
      "data_needed": "DOM by price bracket, sale-to-list by tier, price reduction frequency by days-on-market"
    },
    {
      "slug": "epa-value-hold-county-comparison",
      "title": "San Mateo County Is Down 8.4%. EPA Isn't. Here's Why.",
      "angle": "value-hold-story",
      "audience": "buyers-and-sellers",
      "ghl_keyword": "VALUE",
      "data_needed": "YoY median comparison EPA vs county, inventory levels, absorption rate"
    },
    {
      "slug": "ab1482-sfr-exemption-lease-language",
      "title": "The One Sentence in Your Lease That Keeps You Out of AB 1482",
      "angle": "ab1482-landlord-exemption",
      "audience": "landlords",
      "ghl_keyword": "1482",
      "data_needed": "Current AB 1482 exemption criteria, owner-intent clause requirements, sample lease language"
    }
  ],
  "compliance_check": {
    "fair_housing": "passed",
    "data_sources_cited": true,
    "no_fabricated_stats": true
  }
}
```

**After generating this outline:** Write the `deep_dive_queue` entries into `references/topic-history.json` under the `upcoming_deep_dives` field. These are the next 2-3 months of content — don't throw them away.

---

## Rotation Enforcement (Mandatory After Every Recap)

After completing a Recap, the engine MUST:

1. Log the recap in `topic-history.json` `history` with `type: "market_recap"` and `data_period` filled in
2. Write the `deep_dive_queue` from the narrative outline into `topic-history.json` `upcoming_deep_dives`
3. Set the `next_recap_eligible_after` field to the first month in which genuinely new MLS data would be available (typically 2-3 months out)

The ideation engine checks `upcoming_deep_dives` before any market-update request and serves the next queued deep-dive rather than defaulting to a recap shape.

---

## Deep-Dive Mode — Angle Bank

*(Use this when the Freshness Gate blocked the Recap, OR when `upcoming_deep_dives` has a queued angle.)*

Deep-dives don't need new MLS data. They need deeper analysis of ONE thing the recap surfaced. Each angle below has a distinct hook, audience, and GHL keyword — none of them require a fresh stat pull.

### 1. Pricing Split (BOFU — Sellers)
**Hook:** "There are two markets in EPA right now. One where homes sell in 32 days. One where they sit for 66."
**The question it answers:** What puts a home in the fast bucket vs the slow bucket?
**Data needed:** DOM comparison between well-priced vs mis-priced homes (use sale-to-list ratio by tier as proxy — no new data needed if you have last month's)
**What to go deep on:** The specific variables that predict fast sale — price-per-sqft relative to comp, condition, staging. The seller's checklist for getting into the 32-day bucket.
**GHL keyword:** READY
**CTA:** "Comment READY and I'll send you the pre-listing checklist."

### 2. EPA Value Hold vs County (MOFU — Buyers + Sellers)
**Hook:** "San Mateo County median dropped 8.4% year-over-year. EPA didn't. Here's why — and what it means if you're thinking about moving."
**The question it answers:** Is EPA's stability structural or a timing fluke? What makes EPA different?
**Data needed:** YoY comparison you already have from the recap — no new pull needed
**What to go deep on:** The supply constraint story (Prop 13, zoning, limited new construction). The commute/transit value prop for tech workers. Why EPA will likely hold better than less-constrained Peninsula submarkets.
**GHL keyword:** VALUE
**CTA:** "Comment VALUE and I'll send you the EPA vs. Peninsula market comparison."

### 3. AB 1482 SFR Exemption (BOFU — Landlords)
**Hook:** "Rent out your single-family home in California and miss one sentence in your lease — you just locked yourself into a 5% + CPI rent cap. Forever."
**The question it answers:** What exact language must an SFR landlord include to preserve the AB 1482 exemption?
**Data needed:** Current AB 1482 statutory language — no MLS data needed at all. Research-only piece.
**What to go deep on:** The owner-intent clause. The difference between SFR exempt and condo/multi-unit covered. The risk of accidentally triggering coverage if the notice isn't in writing. A sample clause.
**GHL keyword:** 1482
**CTA:** "Comment 1482 and I'll send you the exemption checklist."

### 4. Rent-vs-Sell Math (BOFU — Homeowners)
**Hook:** "Keep renting it or just sell? I ran the numbers on a $1.1M EPA home."
**The question it answers:** After taxes, mortgage payoff, and opportunity cost — which path generates more over 5 years?
**Data needed:** Current cap rate at $1.1M EPA price point. Current 30Y fixed rate. Basic 1031 exchange math. All derivable from recap data + public rate sources.
**What to go deep on:** The break-even point where rental income beats net proceeds invested. The tax drag of depreciation recapture on sale. When a 1031 makes sense vs just taking the gain.
**GHL keyword:** OPTIONS
**CTA:** "Comment OPTIONS and I'll run the rent-vs-sell math for your specific property."

### 5. Entry-Price Window (BOFU — First-Time Buyers)
**Hook:** "What can $700K–$900K actually get you in East Palo Alto in 2026? I looked at everything available."
**The question it answers:** What's the real inventory picture at the entry tier? What's moving vs sitting?
**Data needed:** Active listings + recent solds under $900K in EPA. Can be pulled from MLSListings in 10 minutes — no new monthly data package required.
**What to go deep on:** Condition breakdown (move-in ready vs fixer), price-per-sqft at this tier, DOM patterns (are entry-level homes actually moving faster?), neighborhoods within EPA where this budget goes furthest.
**GHL keyword:** BUY
**CTA:** "Comment BUY and I'll send you the current off-market and active listings under $900K."

---

## Bay Area / Peninsula Market Context

When framing the narrative for Graeham's primary markets, factor in regional context:

- **Tech-employer rate sensitivity** — Bay Area markets respond to Meta / Google / Stanford hiring patterns and stock-price moves on a faster lag than national markets.
- **Rate-environment disruption** — since 2022 rate hikes, traditional Bay Area seasonality has been muted. Don't assume "spring is hot" without checking current data.
- **Inventory floor** — most Bay Area markets have structurally low inventory due to Prop 13 and zoning. "Low inventory" is the baseline, not the story. The story is *change* in inventory.
- **Neighborhood-level price stratification** — Peninsula markets often have $500K+ price spread between adjacent neighborhoods. Always specify neighborhood, not just city.

---

## Fair Housing + Data Honesty Rules

- NEVER frame demographic shifts as the cause of price moves
- NEVER use school district shifts as a market-driver narrative
- NEVER fabricate, estimate, or supplement with assumed market knowledge — use ONLY the data provided
- Always specify date range and geographic scope so the user knows exactly what the data covers
- If the dataset is too small for reliable conclusions (fewer than 10 comparable records for a market-level story), say so in the narrative
- Don't provide formal appraisal values — frame all pricing as "market context" or "where the market is positioning"
- Date-stamp every stat ("As of Q1 2026, EPA median is $1.42M...") for AEO citation durability
- **NEVER label content as a "June Market Update" if the underlying data is from March. Either call it what it is ("EPA Market Data — Q1 2026") or run a deep-dive instead.**

---

## Integration With Other Skills

- **`cma-generator`** — separate skill for valuations of specific properties. This module never replaces it.
- **`content-creation-engine` Phase R** — pulls the per-topic research data this module renders into narrative.
- **`content-creation-engine` Phase 5** — receives the narrative outline JSON and renders into final format.
- **`content-calendar`** — when the weekly Opportunity Score selects a market-update topic, content-calendar passes the topic to the engine, which routes it through this module before Phase 5.
- **`price-reduction-angle-generator`** — separate skill for private seller conversations. NOT used for public content. Don't confuse the two.

---

## Used By

- `content-creation-engine` only. This is an engine-internal module, not a standalone skill.

---

## Status

Updated May 2026 to add Format Taxonomy, Freshness Gate, Deep-Dive Angle Bank, and Rotation Enforcement.

Updated May 2026 (v2) to add Format 3 (Bi-Monthly Market Update), the Bi-Monthly Freshness Gate, the Bi-Monthly Angle Rotation Bank (B1–B6), and the Gemini Visual System. These additions address a second production failure mode: bi-monthly updates defaulting to the same angle and visual execution even when the data changed. The fix enforces angle rotation at the module level, requires the Gemini Imagination Prompt before any bi-monthly script is written, and makes visual differentiation a required production step (not optional). Every bi-monthly update must pass the 5-step Bi-Monthly Freshness Gate before a word of script is written.
