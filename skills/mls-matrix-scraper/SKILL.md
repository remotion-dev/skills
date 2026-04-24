---
name: mls-matrix-scraper
description: MLS Matrix Stats scraper for Graeham Watts. Logs in to MyMLS via Claude in Chrome and pulls real statistics from the Matrix → Stats → Customize panel (Sale Price Avg/Median, List-to-Sale Ratio, DOM, Active Inventory) for EPA, RWC, PA, MP, SMC. Use ANY time the user mentions: pull MLS stats, run MLS statistics, MLS Matrix data, Matrix stats customize, median sale price EPA, DOM Peninsula, active inventory Redwood City, real market data, live MLS pull, refresh MLS, verify market numbers. Also trigger when content-calendar or a day view shows a demo-data badge on an MLS card and the user asks to replace with live data.
---

# MLS Matrix Stats Scraper

> **Scope.** Chrome-driven live-data pull from MyMLS → Matrix → Stats. This skill does NOT handle user credentials (SSO via Graeham's Chrome profile) and does NOT store passwords. It drives a Chrome session that Graeham has already authenticated.

## Purpose

Content-calendar and single-topic day views currently show "demo data" placeholders on MLS cards. This skill replaces those with real numbers by driving MyMLS in a controlled Chrome session.

## When to trigger

- "pull live MLS stats for EPA"
- "refresh MLS data for this week's calendar"
- "run MLS statistics: Sale Price Avg, DOM, Sale/List Ratio, Active Inventory"
- "replace demo MLS numbers with live data"
- Day view's MLS research card shows "Demo Data" badge and user wants it live
- `weekly-calendar-builder.py` run flagged `mls_source: "demo"` in the JSON

## Workflow

### Step 0: Confirm Chrome session is authenticated

Take a screenshot of the current Chrome tab. Confirm:
- User is on MyMLS (or logged in to a page that routes there)
- If not logged in, STOP. Tell Graeham: "I need you to log in to MyMLS first, then rerun this skill."

### Step 1: Navigate to Matrix → Stats

From any MyMLS page, click Search → Matrix → Stats.

### Step 2: Open Customize panel

Click the "Customize" tab on the left side of the Stats page.

### Step 3: Set filters

Fill in the Customize form:

| Field | Value |
|---|---|
| Time Frame | Past 3 Years (or custom range from args) |
| Statistic | Sale Price Avg / Median / List-to-Sale Ratio / Days on Market (pick per request) |
| Chart Type | Smooth Line (UI only) |
| Group By | Month (default) or Quarter/Year per request |
| Location → City | EP (EPA) / RC (Redwood City) / PA (Palo Alto) / MP (Menlo Park) — per request |
| Property Type | Residential |
| Building Type | Single Family Home (default) — can add Condominium, Townhouse per request |
| Members Only | Do Not Show (we don't need restricted data) |

### Step 4: Generate and capture

Click "Generate" button (green, left panel). Wait for chart to render.

Click "Data" tab (top right) to see raw numbers.

Parse the data table — columns typically: Month, Metric Value (Avg Price, DOM, etc.), Count.

### Step 5: Export to JSON

Write structured output to:
```
outputs/mls-stats-{city}-{statistic}-{timestamp}.json
```

Schema:
```json
{
  "pulled_at": "ISO8601",
  "city": "EP",
  "statistic": "sale_price_avg",
  "time_frame": "past_3_years",
  "building_type": "single_family_home",
  "data": [
    {"period": "2024-01", "value": 925000, "count": 8},
    ...
  ]
}
```

### Step 6: Cross-reference

For each city pulled, also capture:
- Active inventory count (separate Stats query, Statistic = Active)
- Latest Sale/List Ratio
- Median DOM

Write all into `outputs/mls-snapshot-{date}.json` as a single file with all markets.

### Step 7: Hand-off

Return a summary to the user:
```
✓ Pulled MLS stats for EP, RC, PA, MP (4 cities × 4 statistics = 16 queries)
  Output: outputs/mls-snapshot-2026-04-23.json
  Next: re-run weekly-calendar-builder.py or refresh day-view research cards
```

## Fields supported

Per the Matrix Customize panel:

**Time Frame:** Past 1/3/5/10 Years, YTD, Custom Range
**Statistic:** Sale Price Avg / Sale Price Median / List Price Avg / List-to-Sale Price Ratio / Days on Market Avg / Days on Market Median / Active / Sold / New Listings / Pending
**Property Type:** Residential / Residential Income (1-4 units) / Commercial etc.
**Building Type:** Single Family Home / Condominium / Townhouse / Duet Home / Modular / Farm / Floating / Fractional / Other Residential / Studio

## Output paths

- Single city + stat: `outputs/mls-stats-{city}-{stat}-{timestamp}.json`
- Full snapshot: `outputs/mls-snapshot-{date}.json`

## Errors and edge cases

- **Not logged in:** STOP, notify user.
- **MyMLS changed UI:** screenshot the change, report to Graeham, don't guess.
- **No data for query:** write empty data array, note in summary.
- **Rate-limited:** pause 30s, retry once, then halt.

## Handoff to other skills

- `content-calendar` reads latest `mls-snapshot-{date}.json` for scoring context.
- Day-view `research-mls-*.html` pages read the snapshot JSON to populate the stats table live.

## Future additions

- CSV export in addition to JSON
- Neighborhood-level breakdowns (currently city only)
- Historical comps for specific properties (separate from stats)
