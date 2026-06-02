# Market Update Narrative Module

Engine-internal module. Used by `content-creation-engine` Phase G (Generate Content) when the topic is a **market update** — weekly/monthly market reports, seasonal analyses, neighborhood market reads, "is now a good time to buy/sell" content, year-over-year comparisons, or any content where the deliverable is built around MLS data.

This module is the *narrative framing* layer. It does NOT analyze MLS data from scratch — that's `cma-generator`'s job (for valuations) or Phase R's job (for per-topic research data). This module turns analyzed numbers into the story arc that backs a market update.

> **Boundary check vs cma-generator:** `cma-generator` produces a branded valuation report for a specific property. This module produces narrative content (blog / newsletter / script) about market conditions for an audience. They share comp data sources but their outputs are unrelated.

---

## When This Module Fires

`content-creation-engine` invokes this module when ANY of these are true for the topic being produced:

- Topic type is "market update," "monthly market report," "weekly market report," "year-end recap," "seasonal analysis," "market forecast"
- Topic touches buyer/seller decision questions backed by data ("is now a good time to buy in EPA," "where are prices going in San Mateo County," "what does the spring market look like in Redwood City")
- Listing-spotlight content needs market context as supporting evidence
- A `content-calendar` weekly topic was scored highly on the Search Demand criterion AND the topic is data-driven

If the topic is purely education (e.g., "what is escrow") or purely emotional (e.g., "buying a house with student loans"), this module does NOT fire — the standard Phase 5 script-writer handles those.

---

## Inputs

The module receives:

1. **Topic title + slug** (from `content-calendar` or direct user ask)
2. **Audience focus** — buyers, sellers, investors, relocations, or general
3. **Market scope** — single neighborhood, city, county, region, or metro
4. **Time window** — current week, current month, YTD, YoY, custom
5. **Analyzed MLS data** — comes from one of:
   - Phase R's `outputs/research-{topic-slug}-{ts}.json` (per-topic research)
   - A recent `cma-generator` output for the area (if the data is fresh enough)
   - Direct MLSListings data pull via Chrome (if no fresh research/CMA exists)
6. **Format target** — blog post / newsletter section / video script / social post / multi-format

---

## Step 1: Read the Numbers

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

## Step 2: Find the Story

Statistics are not a narrative. The narrative emerges from the *change* and the *divergence* in the numbers. Look for:

### Direction
Is median trending up, down, or flat compared to the prior period? By how much? Is the change accelerating or decelerating?

### Speed Changes
Are DOM getting shorter or longer? Is there a divergence between price ranges (entry-level selling fast while luxury sits)?

### List-to-Sale Pattern by Price Bracket
Homes under $1.5M might be selling at 102% while homes over $3M sell at 95%. That divergence IS the story.

### Expired/Withdrawn Rate
A high rate of unsold listings signals overpricing or weak demand in a specific segment. Pair with active-listing analysis to identify which segment.

### Seasonal Patterns
If the data spans multiple months, note seasonal shifts. Bay Area has distinct spring (peak), summer (steady), fall (mini-peak), winter (slowdown) patterns — but these have been disrupted by rate environment in recent years.

### Neighborhood Divergence
If the data covers multiple neighborhoods, compare them. "Crescent Park is up 8% YoY while Downtown North is flat" is an insight that backs a content piece. "North-of-Highway-101 vs south-of-Highway-101 in Redwood City" is another classic Bay Area divergence.

### Price-per-sqft Anomalies
If the median sale price is up but price-per-sqft is flat, the mix shifted (bigger homes selling). Don't confuse a mix shift for a price increase.

---

## Step 3: Frame for the Audience

The same data tells different stories to different audiences. The module routes the narrative based on the audience input.

### For Buyers

Lead with what gives them advantage or urgency. Example narrative arcs:

- **"Inventory is up X% YoY, which means more choices and less competition"** (favorable conditions)
- **"DOM stretched from X to Y days, which means buyers have time to think"** (favorable conditions)
- **"Sold-above-list rate dropped from X% to Y%, you don't need to overpay anymore"** (favorable conditions)
- **"Inventory is the lowest in Z years, plan for competition"** (unfavorable, but actionable)

Avoid: "now is a great time to buy" (sounds salesy and dates poorly). Use specific data points instead.

### For Sellers

Lead with what supports their position or sets expectation. Example narrative arcs:

- **"Median sold price up X% YoY in [market], with sale-to-list ratio at Y% — sellers in [area] are getting their asking price"** (favorable)
- **"DOM stretched from X to Y days, plan for a longer marketing window"** (cooling)
- **"Price reductions on active listings up X% MoM, sellers who price aggressively are sitting"** (cooling — actionable advice)

Avoid: "sellers should rush to list before the market changes" (urgency tactics). Frame data as helping sellers position correctly.

### For Both / General Audience

Lead with the single most surprising or actionable stat. Frame it neutrally and let buyer/seller readers self-select what it means for them.

### For Investors / Specific Subsegments

If the topic targets investors, relocators, first-time buyers, downsizers, or other specific segments, narrow the data to what's relevant for them — investors care about cap rates and rental yield, relocators care about housing costs vs origin city, first-time buyers care about price tier they can access.

---

## Step 4: Output Format

The module returns a **structured narrative outline** the script-writer Phase 5 then renders into the final format (blog / newsletter / video script / social).

### Narrative Outline JSON Shape

```json
{
  "topic_slug": "epa-market-update-april-2026",
  "topic_title": "East Palo Alto Market Update — April 2026",
  "audience": "sellers",
  "market_scope": "East Palo Alto",
  "time_window": "last 30 days vs prior 30 days",
  "data_source": "research-{topic-slug}-{ts}.json",
  "headline_metric": {
    "metric": "median_sale_price",
    "current": "$1.42M",
    "prior": "$1.36M",
    "delta": "+4.4%",
    "narrative_anchor": "EPA's median ticked up 4.4% MoM, the third consecutive monthly gain."
  },
  "supporting_metrics": [
    { "metric": "DOM", "current": "16 days", "prior": "21 days", "story": "shortening" },
    { "metric": "list_to_sale_ratio", "current": "104%", "prior": "101%", "story": "buyers competing" },
    { "metric": "active_inventory", "current": "12 listings", "prior": "8 listings", "story": "modest inventory recovery" }
  ],
  "the_story": "EPA's seller market is tightening even as inventory loosens slightly. Median up, DOM down, sale-to-list above 100% — and 4 more active listings doesn't break the seller-favorable pattern.",
  "the_angle": "Three months of consecutive median gains in EPA tells sellers: pricing aggressively in this market is leaving money on the table.",
  "audience_specific_takeaway": "If you're considering selling in EPA in the next 90 days, the current sale-to-list ratio of 104% means well-priced homes are getting bid above list — but the modest inventory uptick suggests the spring window is opening, not closing.",
  "compliance_check": {
    "fair_housing": "passed",
    "data_sources_cited": true,
    "no_fabricated_stats": true
  }
}
```

This JSON feeds Phase 5's script-writer, which renders it into the final format with the engine's voice, AEO statements, GHL keyword CTAs, and platform-specific structure.

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
- Date-stamp every stat ("As of April 2026, EPA median is $1.42M...") for AEO citation durability

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

Created Phase 4 of skills roadmap, replacing the standalone `mls-data-analyzer` import from Pantana's package. This module pulls Pantana's "find the story" + "frame for audience" logic into the engine where it integrates with the engine's voice, scoring, and output pipeline rather than duplicating those capabilities.
