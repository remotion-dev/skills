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

## Narrative — REQUIRED, and it is NOT optional prose

The charts alone are not enough. Graeham's standing instruction (2026-06-23): every chart in this section must be followed by a **plain-language written summary on the sheet** so a reader gets the whole story without interpreting a graph. Three written pieces are MANDATORY:

### A. "Reading the numbers" block (a readable card directly beneath the charts/table)
Walk through each group in plain sentences with the counts AND outcomes, as a short bullet list. Use this exact shape:

> Of the [N] [market] homes that sold in the last 12 months:
> - **[a] homes ([x]%) priced it to sell** and sold over their original ask, a median of $[…] (about [+p]% over), in a median of just **[d] days**.
> - **[b] homes ([y]%) priced at market** and sold right at asking, in about [d2] days.
> - **[c] homes ([z]%) overpriced** and sold below their original ask. They started highest (median list $[…]) but sold lowest (median $[…], about [-p]% under), and took **[d3] days**, [k]x as long.
> - **[r] homes ([rr]%) had to cut their price** at least once before selling.

Every number here is a real computed value, not a placeholder. Spell out the counts (24 homes), not just the percentages.

### B. "Why is the market pricing this way?" — answer the reason, do not just report
Graeham specifically wants the WHY behind the split (e.g., why are most selling under ask). Give a short, honest read of the dynamic, e.g. an anchoring/discipline gap: most sellers anchor to the optimistic end (a top neighbor sale, a Zestimate, the number they want to net) and the market corrects them down over weeks, while the disciplined minority who price at/under true value get bid up. Tie the explanation to the data you just showed (homes still sell fast when priced right → it is not a weak market, it is a pricing-discipline gap).

### C. "What this all means" closing note (end of the section)
A short interpretive wrap-up labeled plainly (e.g. **What this all means.**) that says, in one tight paragraph: which behavior the market punishes vs rewards, and exactly what the subject should do because of it. Connect it to the recommended list price explicitly. This is the "here are the notes, this is what it means" summary Graeham asks for.

Then the recommended list price must follow what the data says the market rewards, and the report must say so out loud.

## Guardrails
- Small sample (< 8 comps with original-list data): label the read as **directional**, not definitive.
- Never present LSR vs final list as if it were vs original list — they tell different stories.
- No em dashes in output prose. Compute every percentage and median in Python.
- This section sits in the report AFTER the comps and market data, and FEEDS the Pricing Strategy / Recommended List Price sections (it is the evidence behind them).

## Plain-language labeling and honesty rules (added 2026-06-26, Fugu review)

These were flagged when the 2896 Illinois build shipped a confusing/inaccurate label. Apply every time:

- **Never label the correlation "Price vs Days Correlation."** The x-axis is the sale price as a percent of the ORIGINAL list, not "price." That label is wrong and confuses readers. Use a plain-English label such as **"Longer on market = bigger discount"** (for a negative r) and show the number quietly (e.g. `-0.44`).
- **Always caption the scatter in one plain sentence**, e.g. "Homes that took longer to sell generally closed farther below their original asking price (correlation -0.44, a moderate pattern, not a guarantee for any single home)." Define what the dot means (sale as % of original list vs DOM).
- **r is a tendency, not a prediction.** State it is moderate/strong/weak and does not predict any one home.
- **This pricing-behavior section is ADDITIVE, not a replacement.** It does NOT substitute for the required chart set (`trendPrice`, `trendLS`, `newList`, `monthsInv`, `compBar`, `priceDom`, `priceJourney`, `$/sqft`) or the full comp-table columns. A report must contain BOTH the required charts/columns AND this section. Do not drop required charts to make room.
- **Equity vs gross appreciation.** Never call (today's value minus purchase price) "equity." Equity requires subtracting loan payoff and selling costs, which we usually do not have. Label it **"gross appreciation"** or **"value gained since purchase, before payoff and selling costs."** Only say "equity" if you actually have payoff + cost figures.
- **Data source for the comp pricing fields.** Original List, Final List, Sold, DOM, Close Date, Lot, Year all come cleanly from the MLS **"Appraiser Form 1004MC Detailed" export** (Results → select all → Export → that format → CSV). Beds/baths, exact # of price reductions (vs the orig-minus-final approximation), condition notes, and active-inventory counts (for `newList`/`monthsInv`) are NOT in that export and need a separate pull or the MLS Stats tool. If those are unavailable, state it rather than faking them.
