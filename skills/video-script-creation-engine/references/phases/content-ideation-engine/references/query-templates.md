# Query Templates

Pre-built search queries for the Apify Reddit scraper's `searches` field, organized by use case.

These are alternatives to the `startUrls` subreddit-browse approach — use these when the user wants to hunt for specific trigger events across ALL of Reddit, not just our curated subreddit list.

---

## When to use `startUrls` vs `searches`

- **`startUrls` (default):** Scrape specific subreddits. Best for weekly "what's happening in my markets" runs. See `subreddit-list.md`.
- **`searches` (targeted):** Hunt for specific topics across ALL of Reddit. Best for trigger-event content or ad-hoc research.

**Note from the Apify actor docs:** You can't mix `startUrls` and `searches` in one run. Pick one. If both are present, `searches` is ignored.

---

## Template 1: Layoff trigger events (BOFU gold)

```json
{
  "searches": [
    "Meta layoff sell house Bay Area",
    "Google layoff selling home Peninsula",
    "Apple severance real estate California",
    "tech layoff downsizing Bay Area",
    "Meta RIF housing Menlo Park"
  ],
  "type": "post",
  "sort": "new",
  "time": "month",
  "maxItems": 50
}
```

**Use when:** A layoff wave is in the news and you want to find affected homeowners asking for advice.

**Funnel target:** BOFU (score 3 on Axis 1)
**Lead capture keyword:** OPTIONS or SELL
**Estimated cost:** ~$0.17

---

## Template 2: First-time buyer research (MOFU/BOFU)

```json
{
  "searches": [
    "first time buyer Bay Area",
    "first time homebuyer Peninsula",
    "buying first house East Palo Alto",
    "first house Redwood City",
    "mortgage Bay Area first time"
  ],
  "type": "post",
  "sort": "new",
  "time": "week",
  "maxItems": 50
}
```

**Use when:** Building out the First-Time Buyer content pillar.

**Funnel target:** MOFU/BOFU
**Lead capture keyword:** CHECKLIST or READY
**Estimated cost:** ~$0.17

---

## Template 3: AB 1482 / Rent control legal questions (MOFU — Pillar 4 evergreen)

```json
{
  "searches": [
    "AB 1482 Bay Area",
    "AB 1482 California landlord",
    "rent control California 1482",
    "California rent increase limit"
  ],
  "type": "post",
  "sort": "new",
  "time": "month",
  "maxItems": 40
}
```

**Use when:** Refreshing the AB 1482 evergreen content (the Example #3 asset from Phase 1).

**Funnel target:** MOFU
**Lead capture keyword:** 1482
**Estimated cost:** ~$0.14

---

## Template 4: Relocation inbound (MOFU — Pillar 5/7)

```json
{
  "searches": [
    "moving to Bay Area from",
    "relocating Peninsula jobs",
    "moving to Palo Alto",
    "moving to Redwood City",
    "moving to Menlo Park",
    "where to live Bay Area tech"
  ],
  "type": "post",
  "sort": "new",
  "time": "month",
  "maxItems": 60
}
```

**Use when:** Hunting for inbound relocation prospects.

**Funnel target:** TOFU → MOFU
**Lead capture keyword:** RELOCATING or EPA/RWC/PA/MP
**Estimated cost:** ~$0.21

---

## Template 5: Inherited property / life events (BOFU — Pillar 8 trigger)

```json
{
  "searches": [
    "inherited house California sell",
    "inherited property Bay Area probate",
    "divorce house California",
    "downsizing empty nest Bay Area"
  ],
  "type": "post",
  "sort": "new",
  "time": "month",
  "maxItems": 40
}
```

**Use when:** Hunting for life-event trigger moments.

**Funnel target:** BOFU
**Lead capture keyword:** OPTIONS or SELL
**Estimated cost:** ~$0.14

---

## Template 6: Investment / rental property (BOFU — Pillar 9)

```json
{
  "searches": [
    "Bay Area rental property investment",
    "buying rental EPA",
    "ADU East Palo Alto",
    "cash flow property California Peninsula",
    "house hack Bay Area"
  ],
  "type": "post",
  "sort": "new",
  "time": "month",
  "maxItems": 40
}
```

**Use when:** Feeding the investor-audience content pillar.

**Funnel target:** BOFU
**Lead capture keyword:** INVEST or NUMBERS
**Estimated cost:** ~$0.14

---

## Template 7: Market timing sentiment (MOFU trend tracking)

```json
{
  "searches": [
    "Bay Area housing market 2026",
    "Peninsula home prices dropping",
    "should I sell Bay Area",
    "should I buy Bay Area now",
    "interest rates housing California"
  ],
  "type": "post",
  "sort": "new",
  "time": "week",
  "maxItems": 50
}
```

**Use when:** Taking the temperature of the market. Good weekly pulse check.

**Funnel target:** MOFU
**Lead capture keyword:** MARKET or NUMBERS
**Estimated cost:** ~$0.17

---

## How to use a template

Pick the template that matches what the user is asking for, substitute it into the Apify actor input, and run it via the `run_reddit_ideation.py` helper script. The helper script accepts a `--template` argument (e.g. `--template layoff`, `--template first-time-buyer`) that loads one of these presets.

If the user asks for a search that doesn't match any template, write a custom `searches` list using these templates as a reference for format and keyword style. Keep total searches per run to 5 or fewer to control cost.

---

## Custom query style guide

When writing new searches:

1. **Use natural language.** Reddit's search is more like Google than a database. "Meta layoff Bay Area" works better than "layoffs:meta location:bayarea".
2. **Include geography.** Generic queries return national noise. Always add a Bay Area / Peninsula / city qualifier.
3. **Avoid generic words.** "house" alone is too broad. "buying house Peninsula" is targeted.
4. **Test one query first.** If a new query is expensive or returns garbage, kill the run and iterate before scaling.
5. **Prefer `sort: "new"` for trigger events** (you want fresh signal) and `sort: "hot"` for trending topics (you want what's engaging).
