# Market Pricing Behavior & the Days-on-Market Correlation

**Added 2026-06-23 (Graeham request).** A REQUIRED section in every listing/pre-market CMA, and encouraged in past-client mode. It answers, with hard local numbers, the three questions a seller actually has about pricing:

1. **How is this market pricing?** Are sellers listing UNDER market and getting bid up, or listing OVER and cutting?
2. **What actually happens?** Do homes sell over or under their original ask, and by how much?
3. **Is there a correlation between pricing and speed?** Does pricing sharp actually sell faster, in numbers?

This section is the persuasion engine of the CMA. It is how you move a seller off "let's just try a high number" — you show them what that move costs in this exact market, in days and in dollars.

---

## Data to pull (per sold comp, from the MLSListings History tab)

For at least the closest 12–20 sold comps (use the whole cohort if the pull allows):

| Field | Source |
|---|---|
| Original List Price | History tab, first list price recorded |
| Final List Price | History tab, last list price before sale |
| Sold (Close) Price | Sold price |
| Days on Market | DOM |
| # Price Reductions | count of decreases between original and final list |
| Close of Escrow date | for recency weighting |

Market-level cross-check: the MLS **Stats** tool has a **"Sale Price to Org Price Ratio"** statistic — use it to sanity-check the cohort's median against the whole submarket. (Per-comp original list still comes from the History tab.)

If original list is unavailable for some comps, compute the analysis on the subset that has it and SAY the sample size. Never fabricate an original list. Never silently fall back to final list — the whole point is original-vs-sold.

---

## Metrics (compute in Python, never eyeball)

- **LSR = Sold ÷ Original List × 100** — the list-to-sale ratio vs the ORIGINAL ask (not the final list). This is the number that captures the full pricing story.
- **Over / At / Under split:** % of comps with LSR > 101 (sold over), 99–101 (at), < 99 (under).
- **Median LSR** and **median DOM**.
- **Reduction rate:** % of comps with ≥1 price cut (final < original); median $ cut among those.
- **Correlation:** Pearson **r** between each comp's LSR and its DOM. Report the sign and rough strength in plain words ("r = −0.58, a clear negative correlation: the further over asking a home sold, the fewer days it took").
- **Bucketed outcomes** by how each home actually priced/sold:
  - **Priced to sell** = sold over original ask (LSR ≥ 101)
  - **Priced at market** = sold within ±1% (LSR 99–101)
  - **Overpriced** = sold under original ask (LSR < 99) and/or ≥1 reduction
  - For each bucket: count, median original list, median sold, median LSR, median (and avg) DOM.

---

## The four required visuals (Chart.js)

### 1. Over/Under split — the headline
A single horizontal stacked bar split into **Sold OVER / AT / UNDER original ask**, each segment labeled with its %. Green = over, gray = at, coral = under. Pair it with ONE big stat callout, e.g. *"71% of homes sold over their original asking price; the median home closed at 103% of original list."* This is the one-glance answer to "which way is the market going."

### 2. List-to-Sale ratio distribution
Vertical histogram. Buckets: `≤95%`, `95–99%`, `99–101%`, `101–105%`, `105%+` of original list. Count per bucket. Coral for the under-100 buckets, green for the over-100 buckets. Dashed vertical reference line at the median LSR; caption states the median.

### 3. List-to-Sale % vs Days on Market — THE correlation chart (the new one)
Scatter, one dot per sale: **x-axis = LSR % (sold vs original list), y-axis = days on market.** Add a linear trendline and annotate the correlation r in the caption. Color dots by bucket (green over / gray at / coral under). This is the chart that visually proves "homes that sold over asking sold fast; homes that sold under asking sat." It is the single most persuasive chart in the report — never omit it when original-list data exists.

> Chart.js: use a `scatter` type with a second `line` dataset for the trendline (compute slope/intercept in Python via least squares and pass the two endpoints). Tooltip shows address, LSR%, DOM.

### 4. Pricing-approach outcomes
Keep the existing **"Pricing Strategy Performance"** grouped bars (avg DOM + median LSR per bucket, numbers ON each bar via datalabels) AND add a small table:

| Approach | # of sales | Median orig list | Median sold | LSR | Median DOM |
|---|---|---|---|---|---|
| Priced to sell (sold over) | … | … | … | …% | … |
| Priced at market (±1%) | … | … | … | …% | … |
| Overpriced (cut / sold under) | … | … | … | …% | … |

---

## Narrative (3–5 sentences, answer Graeham's questions head-on)

Interpret the numbers for THIS market, plainly. Template:

> "In [market] right now, sellers are mostly pricing [UNDER / AT / OVER] market. [X]% of homes sold over their original ask, the median home closed at [Y]% of original list, and [Z]% needed a price cut. The payoff for pricing sharp is speed: homes that sold over asking took a median of [A] days, while the overpriced homes that had to cut sat [B] days and still closed below their first number. The correlation is [strong/clear/weak] (r = [r]) — in this market, a sharp, slightly-under list is what gets rewarded."

Then connect it to the subject's recommendation: the recommended list price should follow what the data says the market rewards, and the section should explicitly say so.

## Guardrails
- Small sample (< 8 comps with original-list data): label the read as **directional**, not definitive.
- Never present LSR vs final list as if it were vs original list — they tell different stories.
- No em dashes in output prose. Compute every percentage and median in Python.
- This section sits in the report AFTER the comps and market data, and FEEDS the Pricing Strategy / Recommended List Price sections (it is the evidence behind them).
