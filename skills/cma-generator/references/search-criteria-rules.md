# Search Criteria Rules — moved verbatim from `cma-generator/SKILL.md` (2026-06-09 refactor)

## Search Criteria — Follow These Rules Exactly

### Listing Status — ALWAYS pull Active + Pending + Sold (default)
Unless the user explicitly says otherwise, EVERY CMA pulls all three statuses, because each answers a different question:
- **Sold** (last 3–6 months) — what the home is actually worth (the value comps).
- **Pending** — where the market just moved (the freshest read on buyer behavior).
- **Active** — the live competition the home will be priced against right now.
A Listing CMA in particular MUST present Active + Pending as "your competition," not just Sold — pricing strategy is built against the active field, not only against closed sales. Only narrow to one status when the user specifically asks (e.g., "just sold comps"). Past-Client / Home-Value-Update mode may lead with Sold but should still note current Active/Pending context. Never silently drop Active/Pending.

### NEVER lean out the format (2026-06-07 rule — violated once, never again)
The full canonical format applies to EVERY CMA mode — listing CMAs, value checks, pre-market reviews, sell-vs-rent reviews, past-client updates. "It's just a quick value check" is NOT a reason to drop the cohort table, the trend charts, the market story, or the market-direction section. A leaned-out report shipped on 2026-06-07 (missing actives/pendings, trend graphs, new-listings chart, L/S data) and the user caught it immediately and ordered a rebuild. If the session lacks context budget to build the full format, STOP and hand off to a fresh session with a handoff doc rather than shipping a thin report. Minimum mandatory sections in every report: market story narrative, full Sold + Active + Pending cohort table (dated as of the pull), trendPrice + trendLS + newListings charts, price-reduction history, market-direction read, range-based pricing with DOM estimates.

### Market Trend & Comp Weighting — hedge for shifting markets (REQUIRED)
Sold comps LAG the market (deals struck 1–3 months ago). Actives and pendings are the leading edge. Always reconcile them and hedge:
- **Active-vs-Sold gap:** if comparable ACTIVES are sitting (elevated DOM) at prices BELOW recent solds, the market has softened since those solds closed — weight value toward the active/pending level, NOT the solds. **Pendings** (just went under contract) are the single best read on current accepted price — isolate them and weight them most.
- **Do NOT linearly extrapolate $/sqft.** A larger home is not worth (cohort $/sqft × its larger sqft), especially when the matching cohort is small and smaller-sqft. Buyers pay for the home, not pure footage. Use comparable SOLD PRICES with only a modest size adjustment, and flag low confidence when the cohort is thin (under ~5 truly-similar comps).
- **Rate / trend hedge:** assess the interest-rate environment and the DOM/absorption trend. In a rising-rate or slowing market, apply and DISCLOSE a downward hedge (typically 3–6%) to the comp-derived value, and recommend a list that prices slightly ahead of a falling market rather than chasing it down.
- Add a short **"Market Conditions"** section to the report for the seller: rate environment, DOM/absorption trend, the active-vs-sold gap, and the explicit hedge applied — so the pricing rationale is transparent.

### Active price-cut tracking — the "Which Way the Market Is Moving" section (REQUIRED, added 2026-06-07)
Closed sales lag the live market by 1–2 months; the leading indicator is what ACTIVE sellers are doing with their prices RIGHT NOW. Every CMA must include a market-direction section built from recent active-listing price reductions:
- **Detect the cuts.** Two methods, use both when possible: (1) diff the current active pull against a prior dated snapshot of the same cohort (keep dated active/pending snapshots in the `_workdata_*.md` file precisely so future CMAs can diff against them); (2) for each key active, open the listing and compare Orig Price vs current List Price (Matrix Listing tab), and check for delist/relist at a lower number (new MLS# on the same address = relaunch; note the prior price).
- **Present as a table:** Address | Was | Now | Cut | DOM | one-line read. Include brand-new listings that LAUNCHED below recent closed prices — a new seller pricing under the last solds is the same signal wearing a different hat.
- **Write the read:** which tier is cutting, how much (% off prior asks), what supply is doing (cite the new-listings chart), and what it means for THIS seller's pricing window. Real example (EPA, June 2026): closed sales still printed strong springs numbers while the $900K–$1M active tier cut 3–8% (Verbena 999→950, Wisteria 975→945, Ralmar 898→820, a relist 1,099→1,049) and a new listing launched at $925K below recent solds — the correct call was "price promptly in the competitive band, do not stretch into a softening tier." The market-direction read MUST shape the recommended band, not just decorate the report.
- **When the subject's tier is cutting, shift the ENTIRE pricing architecture below the AVM — do not anchor on it.** AVMs are trained on closed sales, so in a softening active tier the AVM reflects the market of 1–2 months ago, not today's. Precedent (2495 Gloria Way, 2026-06-07, Graeham's call): AVM $1,145,800, but with the active tier repricing ~5% down, all three bands moved DOWN $50K (recommended list $1,048,000–$1,099,000, deliberately under both the AVM and the closest sold twin), framed to the seller as "priced where the market is heading, not where it was — pricing slightly ahead of the move makes you the obvious value in the band." Shift the expected-clear ranges, the net sheet rows, and the scatter subject marker consistently with the bands; never leave a stale AVM-anchored number in one section after shifting another.

### Comp fields & report add-ons (REQUIRED + OPTIONAL)
- **List-to-Sale ratio — REQUIRED on every sold comp.** Pull each comp's ORIGINAL LIST PRICE and show List-to-Sale % (sold ÷ original list) in the comp table. This quantifies how far over/under asking the cohort actually sold and backs the pricing strategy with hard numbers. If original list isn't readily available, note it rather than omitting the column.
- **Pre-List Prep & ROI — OPTIONAL, only when requested.** Do NOT include a pre-list prep pricing section by default. If the seller explicitly asks for prep recommendations OR if the home obviously needs significant work to be market-ready (deferred maintenance, tenant damage, dated kitchen/bath), offer the section as an option. Default outputs should NOT include the contractor-style prep pricing table at the end of the report.
- **Net-to-Seller sheet — BANNED by default, NEVER include voluntarily (hard rule, reinforced 2026-06-08).** Do NOT add a seller net sheet / "Estimated Net to You" / proceeds table to ANY CMA in ANY mode unless Graeham EXPLICITLY asks for it in that specific request. It has been wrongly auto-included and he has banned it. There is no "offer it" step in the report; if you think it would help, leave it out and mention in chat that you can add one on request. If a draft or cached/template file already contains a net sheet, REMOVE it on sight before delivering. Default state: absent. Only when Graeham says "include a net sheet" do you add it (borrow offer-analyzer net-sheet logic).
- **Trend charts — REQUIRED, and they MUST come from real MLS data.** Include THREE trend visualizations in every CMA: (1) **Sale Price Average over time** for the cohort, (2) **Sale-to-List Price Ratio over time**, and (3) **New Listings per month** (supply trend — Matrix Stats Statistic: "New Listings, Number of"; this is the "homes coming on the market" chart and it powers the market-direction read). Source: MLSListings Matrix → Stats → Customize panel. Pull **monthly** granularity (Group By: Month), use the widest defensible time frame (Jan of the year five years back to current month), filter by Postal City + Property Sub Type. Capture either the chart image OR scrape the underlying Data tab values; do not smooth or invent. If the actual data shows monthly volatility (a sawtooth pattern, not a clean curve), the chart MUST reflect that volatility — a clients-eye-friendly smooth-line that doesn't match the real MLS chart undermines trust the moment they look it up themselves. Caption every chart with **"Source: MLSListings Matrix Stats, [filter description], [N] listings"** so the source is unambiguous. Only fall back to a flagged approximation if Matrix is genuinely unreachable in-session, and in that case caption it as APPROXIMATION and tell the user it needs a real MLS pull before sending.
- **Interest Rate context — REQUIRED, multi-source cross-referenced.** Include a brief **Interest Rate / Rate Environment** section in every CMA showing the current 30-year fixed mortgage rate, **cross-referenced across at least three sources** (do not lean on a single number): **Mortgage News Daily** (daily national 30-yr fixed), **Freddie Mac PMMS** (weekly survey), **Bankrate** (state-level — California for Bay Area work), and **Realtor.com** (local market average — East Palo Alto / Dublin / specific city). Include local lender quotes when meaningful (Zillow Home Loans, etc.) and APR alongside rate where available. Show the recent trajectory (last 6–12 months — rising, flat, falling), and a one-line read on what it means for the seller's market (rates up → thinner retail buyer pool, longer DOM, downward price pressure; rates down → activity warming; flat → status quo). Note that investor buyers (cap-rate-driven) are LESS rate-sensitive than retail (monthly-affordability-driven) — relevant when recommending marketing strategy. Where possible, include a small rate-trajectory chart alongside the trend charts. Always note "verify day-of via Mortgage News Daily before pricing finalization."

### Voice — write as if sending DIRECTLY to the client (second person)
Every CMA gets forwarded to the seller. Write ALL prose in **second person** ("you", "your") as if you are Graeham speaking to the seller directly. Never refer to the seller in third person ("he", "she", "his", "her", "the client", "Hu", "the seller") inside client-facing cards, paragraphs, or callouts.

The ONLY places third-person identifiers are acceptable:
- The subject-details factual table ("Owner: Li Hu") — that's a fact about the record, not prose
- The footer disclaimer (use "the owner of [address]" generically)
- The hero subtitle ("Prepared for [First Last], [Month Year]") — addressed TO them

Before publishing, scan the file for `\bhis\b`, `\bhim\b`, `\bher\b`, `\bshe\b`, `\bthe client\b`, `\bthe seller\b` in prose context and rewrite to second person. If a piece of advice would feel awkward in second person ("consult your CPA" is fine; "the seller should consult their CPA" is wrong), the prose is in the wrong voice.

This rule applies to all CMA modes (Listing / Buyer / Past-Client / Cash-Out Analysis).

### CANONICAL TEMPLATES — read the right one before building

Two locked canonical templates live in this skill's references folder:

- **`references/dashboard_template.html`** — LISTING mode reference (1030 Bradley CMA, May 2026)
- **`references/buyer_mode_template.html`** — BUYER mode reference (1430 Chilco buyer CMA, May 2026)

Before generating any CMA, identify the mode (Listing / Buyer / Past-Client) and `Read` the matching reference. Match the section order, voice, chart set, and HTML structure exactly. Replace only the property-specific data and the comp cohort.

**BUYER MODE structural differences vs Listing:**
- Section 2 is "Read the Listing Carefully" — flags structured offer processes (offer date, no preemptive offers, mission-driven sellers, disclosure timing)
- Three Paths are: Anchor + strong terms / Competitive market-aligned / Stretch + appraisal gap (NOT Sell+Redeploy / Prep+Timing / Hold+Rent)
- "Recommended Pricing" becomes "Recommended Offer Bands"
- "Net to Seller" becomes "Net Cost To You" (cash-to-close + monthly P+I at multiple offer prices)
- Add a "Terms Checklist" section with financing, EMD, contingencies, close timeline, possession, personal-letter guidance
- Calculate appraisal-gap threshold and flag explicitly
- Identify mission-driven sellers (nonprofits, estates, charities) and recommend personal-letter angle
- Pre-List Prep section is N/A

### CANONICAL DASHBOARD TEMPLATE — match this structure exactly
The locked reference template for ALL Listing CMAs lives at `references/dashboard_template.html` in this skill. **Before generating any new CMA, Read that file** to see the exact section order, chart set, voice, and HTML structure. The Bradley Way CMA (May 2026, Hu Li) is the gold-standard example.

**Canonical section order (DO NOT REORDER):**
1. Hero / Subject Property Summary
2. "Where the Market Is" — leads with market context (rates, cycle, broader cohort trend). NEVER with commission math.
3. The Market Story — closest comps + submarket boundary note (e.g., west-of-101 vs east-of-101 in EPA)
4. Comp Cohort table — Active + Pending + Sold, last 6 months
5. Trend Context — two Chart.js line charts: Sale Price Avg + L/S Ratio, monthly, 5+ years
6. Interest Rate Environment — 4-source cross-reference (MND, Bankrate, Realtor.com, Zillow)
7. Price-Reduction History table — Original/Final/Sold/Reductions/DOM for top sold comps
8. **Pricing Journey chart** — line chart, each comp Original→Final→Sold, green up / coral down
9. **DOM vs Cut chart** — dual-axis bar showing DOM and $-cut per comp
10. Three Paths Forward — Sell+Redeploy primary / Sell+CommissionLever / Hold+Rent (for long-term investors only)
11. Recommended Pricing — three tier RANGES (Conservative / Competitive / Ambitious)
12. Net-to-Seller table
13. Notes & Caveats

Pre-List Prep is NOT in the default flow. Add only if explicitly requested.

**Required Chart.js canvases (matching IDs):**
- `trendPrice` (monthly Sale Price Avg)
- `trendLS` (monthly Sale/List Ratio)
- `priceJourney` (multi-line, Original→Final→Sold per comp)
- `domVsCut` (dual-axis bar, DOM and $-cut per comp)
- `priceDom` (bubble scatter, full cohort)

If any of these charts is omitted, the CMA is not complete. Use the data scraped from MLSListings to populate; do not invent values.

### Recommended Pricing section is MANDATORY in every CMA, never drop it (reinforced 2026-06-08)
Every CMA, in EVERY mode and format (Listing, Buyer, Past-Client, Cash-Out, value review, AND dual/two-scenario reports), MUST contain a clearly-labeled **Recommended Pricing** section that states the recommended list price as a three-tier strategy (Conservative / Competitive-recommended / Stretch). This is the single most important section of the report and it has been accidentally dropped or buried when restructuring into scenario layouts. If the report uses scenario cards (e.g., as-recorded vs with-conversion), you STILL include a distinct Recommended Pricing section with the three strategy tiers and one bolded recommended list price line. Do not replace the three-strategy block with scenario cards alone. The reader must be able to find, in one obvious place, "here is what I recommend you list at, and here are the strategy options."

### Recommended Pricing must be PRICE RANGES, never single numbers
Every CMA's Recommended Pricing section (Conservative / Competitive / Ambitious, or whatever the three tiers are named for the situation) MUST show each tier as a RANGE, not a single number. A single number is false precision; a range is honest. Example formatting:
- Conservative (quick sale): **$830,000 to $870,000**
- Competitive (market read): **$880,000 to $920,000**
- Ambitious (tests ceiling): **$930,000 to $970,000**

The range width is informed by the comp cohort's actual variance and the confidence in the analysis. Tight cohort (5+ direct comps within 10%): ±2-3% range. Wider cohort or unique property: ±4-6%. Always state the "realistic clearing band" within each card so the seller knows what each list strategy is likely to actually transact at.

### Heat map / price-DOM visualization — REQUIRED
Every CMA MUST include a visualization that puts the comp cohort in spatial or behavioral context. Two options:
1. **Geographic heat map / scatter** — if comp addresses geocode cleanly, plot them on a map colored by $/sqft (or sold-vs-list ratio) so the seller can see how the cohort distributes around their property. Use a simple HTML5 canvas, Leaflet via CDN, or a static image.
2. **Price vs DOM scatter** — if a geographic map isn't practical, plot every comp as a bubble: x-axis = sold price (or list price for active), y-axis = days on market, bubble size = sqft, color = status (sold/active/pending). This visually shows the seller "homes that priced right sold fast; homes that priced too high sat." It is one of the most persuasive single charts in a listing CMA because it forecasts what will happen at each list price.

Include captions explaining the read. The price-DOM scatter is the right default when geocoding is unreliable or the cohort is small.

### Price-reduction history — REQUIRED in comp table for sold listings
Every sold comp in the cohort MUST show:
- Original List Price (first list price recorded)
- Final List Price (last list price before sale)
- Sold Price
- Number of Price Reductions (count of price decreases between original list and sold)
- Days on Market

This data is on the MLSListings History tab for each listing. Pull it for at least the top 8-10 closest comps. Add a column to the comp table called "Reductions" or "$ Cut" showing the dollar amount cut from original list. Then write a short paragraph correlating reductions to DOM, e.g., "Homes that priced honestly sold in 8 to 30 days; homes that overpriced sat 90 to 150 days and required 2+ reductions to clear." This is the single most persuasive piece of data when talking a seller down from an overpriced list.

If pulling original-list-price-history programmatically is hard in-session, at minimum click into the 4-6 closest comps and pull it manually. The data is too important to skip.

### Submarket awareness — REQUIRED in any cohort that spans known boundary lines
When the comp cohort spans a known submarket boundary (most commonly: east-of-101 vs west-of-101 in EPA/Menlo Park/Palo Alto, but also: Belle Haven vs the rest of Menlo Park; original Eichlers vs newer builds; specific school district lines), the CMA MUST:
1. Identify which side of the line the subject is on
2. Filter or flag comps that are on the OTHER side as different submarket
3. Never use a cross-boundary comp as a price anchor for the subject

Example: 1030 Bradley Way is east-of-101 in EPA. 2055 Oakwood Drive is west-of-101 in EPA (Menlo Park/Palo Alto adjacent). Oakwood pricing reflects the west-side premium and is NOT a valid comp for an east-side property. Footnote any such comp explicitly so the seller doesn't anchor on it.

### Listing CMA opening framing — lead with MARKET CONTEXT, not commission math
For listing CMAs, the section that opens the substantive analysis (sitting right after the Subject Property summary) MUST lead with market context: where we are in the cycle, recent rate moves, broader EPA trend, and what that means for the seller's home. Save all commission/friction math for a later "Three Paths" or "Net to Seller" section.

Reasoning: clients who see commission numbers at the top of the report fixate on them and miss the actual market story. They start negotiating commission before they understand what the market will pay. Lead with the market, build to the strategy, end with the math.

This rule is most important for break-even / cash-out / "I bought near the top" scenarios where the temptation is strongest to lead with the friction math to justify a paper loss. Don't.

### Capital deployment framing for cash-out sellers
When a seller's primary goal is "get out, take the cash, move on" (vs. "maximize this property's long-term value"), the CMA must frame the Three Paths around what the seller's CASH does next, not just what the property does:

- Path A (recommended for cash-out sellers): **Sell now, redeploy capital elsewhere.** Quantify the redeployment math at conservative (5%), moderate (7%), and stretch (10%) annual returns over 2 to 3 years. Compare to expected property appreciation over the same window. Be honest about whether the redeployment outperforms holding.
- Path B: Same outcome with commission lever for marginally better net.
- Path C: **Hold and rent for 5+ years.** Frame as explicitly for long-term real estate hold investors, NOT as a "wait for rates to drop" play. Most rate-cycle waits underperform when the cycle is long (3+ years of high rates) and the alternative is a diversified portfolio at the same risk level.

Never recommend "wait for the market to improve" without quantifying the opportunity cost. The honest math often favors selling and redeploying for sellers with sub-decade horizons.

### Opener and tone: calm and data-led, NEVER defensive or aggressive (hard rule, added 2026-06-08)
Client-facing CMA prose, and every client email, must open calmly and lead with the data, never with a defensive throat-clear. BANNED openers (verbatim AND paraphrased): "First of all," "I want to be straight with you," "Two things I want to be straight with you about up front," "Let me be honest," "To be blunt," "I'll be direct," "Real talk," or any variant that braces the reader for bad news. They read as aggressive and put the client on the defensive. Instead, open like you are simply walking them through what you found: "I reviewed the comparable sales, and here is what the data shows," "Here is where the market is and what recent sales tell us," "Walking through the numbers, here is the story." Present the comps, the story, and the numbers warmly and plainly. Lead with the facts, let them speak.

### Humanizer pass is MANDATORY on every CMA and email (reinforced 2026-06-08)
Every CMA narrative AND every client email MUST be run through the `humanizer` skill before publishing or drafting. This is required, not optional. Graeham has flagged the tone as stiff and off more than once. The humanizer pass removes AI tells AND the defensive/aggressive phrasing banned above. If the prose still sounds like a model wrote it, or braces the reader, it is not finished. No exceptions.

### NEVER include data-source or MLS-access caveats in client output (BANNED, hard rule, added 2026-06-08)
Client-facing CMAs, value reviews, and home-value updates must NEVER apologize about tooling or explain how the data was obtained. Graeham has banned this language repeatedly (347 Avenida Pinos email; this rule). The following are BANNED verbatim AND paraphrased, in any published HTML, PDF, or email:
- "built from public real estate data (Redfin, Zillow, public market reports) because MLS access was not signed in / was not signed in when this ran"
- "Public data is a good directional guide but it is less precise than the MLS" / "treat the numbers here as a solid estimate rather than an exact figure" / "let me run a full MLS-verified version any time you want a tighter read"
- "Anything below that depends on MLS-only listing history (original list price, price reductions, days on market) is marked N/A and flagged" (and printing "N/A" with an apology)
- a "Notes and Honest Caveats" section, a "Data source" disclaimer line, "No agenda here", "I have not been inside recently", "this is simply a where-you-stand update", "there is nothing being pitched"
- any "About this analysis" paragraph that names the data source as the reason for lower confidence
- ANY "no agenda" phrasing in any report or email (added 2026-06-11, Basswood feedback): "with no agenda attached", "no agenda here", "no-pressure update", "I like to check in with past clients now and then". Graeham: too salesy. Say it plainly instead: "Here is an update on your home, just keeping you informed."
- a "Notes & Caveats" closing section in ANY form, even on full-MLS runs, including the "About this analysis", "What would sharpen this further", and "Condition matters" cards (added 2026-06-11). Condition nuance goes inside the value-range card descriptions; sharpening/source notes go to Graeham internally. Reports end on the warm referral CTA, then the single disclaimer line.
The ONLY disclaimer allowed in client output is a single clean line: "Professional opinion of value, not a formal appraisal." Tooling and source limitations belong in INTERNAL notes to Graeham (chat or the GHL contact note), NEVER in the client report or email. If MLS-only fields are unavailable for an off-MLSListings market (Alameda County: Union City, Fremont, Hayward), omit those columns/sections cleanly and source comps and market stats from public data presented confidently, with no meta-commentary. Tell Graeham privately which fields came from where; the client sees a clean, confident report.

### Months of Inventory — REQUIRED metric AND chart (added 2026-06-08, chart made mandatory 2026-06-11)
Include months-of-inventory (absorption = active listings divided by the monthly closed-sale pace) as a market-health metric AND as a dedicated chart (`monthsInv`: monthly line with a dashed reference line at 3 months = balanced market) in EVERY CMA mode (Listing / Buyer / Past-Client / Cash-Out). Graeham flagged it missing from the 2026-06-08 Basswood past-client CMA; every mode uses the SAME trend chart set (trendPrice, trendLS, newList, monthsInv). Source: MLSListings Matrix Stats "Months of Inventory" preset; for off-MLS markets use a public market report (Redfin Data Center publishes months-of-supply by city). Read: under roughly 2 to 3 months = seller's market; rising months = softening. Pair it with the new-listings and active price-cut data to tell the market-direction story.

### Call-to-action on past-client / home-value updates — REQUIRED (added 2026-06-08)
Past-client value updates END on a warm, low-pressure call-to-action, never a disclaimer or hedge. Graeham's preferred default is a referral + availability ask, one or two lines, e.g.: "If you or someone you know is ever thinking about buying or selling, I would love to help, a quick call is always welcome." No hard sell and no "nothing to do here" language. A referral-style CTA is the default; a softer equity-aware line ("if you are ever curious what your equity could do for you, let's talk") fits clients with high equity.

### Em-dash / "AI tell" punctuation — BANNED in published output
Em-dashes (—, `&mdash;`) are the single biggest "this was written by AI" tell. Every CMA report MUST be em-dash-free in the published HTML and PDF. Use commas, periods, parentheses, colons, or "to" (for numeric ranges) instead. En-dashes for numeric ranges (1,500–2,000) are acceptable but plain "to" reads more naturally — prefer "to" in client-facing prose. Before publishing, scan the output for `&mdash;`, `—`, and ` -- ` and replace them. The humanizer skill is the right reference for what AI-tells look like; treat its rules as binding for CMA output, not optional.

### Re-doing a CMA for a previously-listed property
When re-running a CMA for a property that the agent (Graeham) already listed and didn't sell, the report goes to the SAME client. Never write language that retroactively criticizes the prior listing strategy ("mis-positioned for retail", "sharper targeting needed", "the marketing approach was wrong"). It reads as Graeham admitting he didn't know what he was doing the first time. The right framing is forward-looking: "the market told us X, so the next listing tests Y angle." Distinguish between what the **market** showed (factual: 50 DOM, no acceptable offers, feedback on tenant friction) and what **strategy** changes for the relist (forward-looking, optional). Also: do not recommend re-spending money the client already spent — if the home is already staged, don't recommend staging it again; if specific prep was done, don't recommend redoing it. Confirm prior spend with the agent before recommending any prep work.

### When direct comps don't exist (unique-property methodology) — REQUIRED for atypical homes
Some properties have NO recent comps that match cleanly — 2-on-1 dual homes, properties with permitted ADUs, unusual zoning, large-lot teardowns, custom builds, multi-unit on SFR APN, deed-restricted, etc. When that's the case:
- **Don't fake it.** State plainly that direct comps are unavailable and explain why. Never present an indirect cohort as if it were direct.
- **Triangulate from three angles, transparently:**
  1. **Adjacent-cohort baseline.** Closest "normal" cohort sale prices (e.g., same-area SFRs of similar combined sqft), then apply documented qualitative adjustments for the subject's unique features (extra lot, ADU, recent build cost, condition variance). State each adjustment.
  2. **Older similar-configuration comps with time-adjustments.** Find the closest historical similar-config sale (2–5+ years old is OK) and adjust for time using known area appreciation/depreciation factors between that sale date and now. Document the math: e.g., "sold $X in 2019, +18% appreciation to 2022 peak, then −10% to current = adjusted $Y." Use Case-Shiller / Zillow ZHVI / CAR area-level data when available; otherwise document the assumed rate.
  3. **Income approach.** For tenant-occupied or rentable properties, value via gross cap rate against current/market rents. Show 5% / 6% / 7% gross cap scenarios in a small table so the seller (and any investor buyer) can see the math.
- **Combine and reconcile.** Present a value range that all three approaches roughly support; flag where they diverge.
- **Cite the prior listing as a market test** when the subject was previously listed. Days on market, withdrawn vs sold, the offer pattern and feedback — these are real, property-specific data points and often the single strongest signal.
- **Marketing strategy follows the comp problem.** For investment-style unique homes, recommend marketing as multi-family / income property with cap-rate framing — that reaches the buyer pool that actually fits the property (investors underwriting at cap, not retail underwriting at monthly affordability).
- Be honest about the confidence band: unique-property analyses are wider than standard CMAs. Communicate that range explicitly.

### Radius
- 1-mile radius from subject
- **City boundaries override radius** — never include comps from a different city even if closer than 1 mile
- Flag borderline comps near city borders, let Graeham decide

### Square Footage
- Target: subject sqft +/- 200-300 sqft (flexible, not a hard cutoff)
- If market is thin, expand gradually and note why
- Bed/bath count matters but is not a disqualifier if sqft and condition match

### Condition Matching
Categories (plain language): Fully renovated/turnkey, Updated/partially renovated, Original condition/good bones, Fixer-upper/cosmetic, Major fixer, Tear-down/land value

### Time Frame
- Preferred: last 3 months
- Acceptable: last 6 months
- Extended: beyond 6 months only if needed — must flag, note market context, apply adjustment

### Sample Size
- Note comp count per strategy segment
- Flag if only 1-2 comps: "Limited data — use with caution"
