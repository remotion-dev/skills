---
name: price-reduction-angle-generator
description: "Generates data-backed positioning for the price reduction conversation — the hardest conversation in real estate. Produces a seller-facing angle (2–3 sentences), supporting data points (3–4 receipts), and a suggested next step. Grounded in real comparable data, not gut feel. Use this skill ANY time the user asks to: prepare a price reduction talk, build the price reduction angle, write a price reduction script, draft the price drop email, position a price adjustment, talk to a seller about lowering price, justify a price reduction with data, write the price reduction conversation, or build the case for adjusting list price. Trigger when the user mentions: stale listing, low showings, no offers, sitting on market, overpriced listing, price drop, price adjustment, price reduction, or seller convo on lowering price. Pulls comp data from MLSListings exports, cma-generator output, manual paste, or Apify Zillow scraper. Bay Area / Peninsula market localization built in."
---

# Price Reduction Angle Generator

Help the agent have the hardest conversation in the business — "we need to reduce the price" — with data behind every word. This skill does NOT write a script. It produces the **positioning statement** and **supporting receipts** the agent uses in person, on the phone, in a text, or in an email.

The output is the talking point the agent walks in with — not a sales pitch and not a script to read. It's grounded in the data the agent provides, never in fabricated market conditions.

---

## Before You Start — Read These

1. **`../shared-references/identity.json`** — Graeham's brand identity. Never hardcode contact info, DRE, or brokerage from memory.
2. **`../cma-generator/SKILL.md`** (optional) — if a CMA was recently generated for this property, the comp analysis is already done. Pull from `cma-reports/cmas/CMA_[address].html` rather than re-analyzing comps from scratch.
3. **`../content-creation-engine/references/market-config.md`** (optional) — Bay Area market config for context.

---

## Fair Housing + RESPA Guardrails (Non-Negotiable)

Even in a private seller conversation, the angle and receipts must:
- NEVER reference demographic shifts in the neighborhood as a reason for the price adjustment
- NEVER suggest "the buyer pool has changed" in a way that implies protected-class characteristics
- NEVER use school quality, school district shifts, or demographic data as a market-condition argument
- NEVER blame buyers, neighbors, or anyone else — frame as market alignment, not blame
- NEVER recommend specific lenders, inspectors, or vendors as part of the next-step action (RESPA)

When discussing buyer behavior or market conditions, stick to: list-to-sale ratios, days on market, price-per-square-foot trends, inventory levels, comparable sale activity, showing counts, and offer counts. These are the data points buyers and sellers respond to without crossing legal lines.

---

## The Three-Strategy Honesty Rule

Graeham's CMA methodology uses a three-strategy pricing framework. The price reduction conversation is the *follow-up* to that framework when the listing has stalled:

1. **Aspirational price** — what the seller hoped for (often what was originally listed at)
2. **Market-aligned price** — what the data supports given current comps and conditions
3. **Move-it price** — the price that triggers offers within a reasonable timeline

The price reduction angle is fundamentally a recommendation to **shift from Strategy 1 (aspirational, where the listing currently sits) to Strategy 2 (market-aligned, where the data points)**, occasionally to Strategy 3 if the data is severe.

The angle must be honest about which strategy the new recommended price represents. Don't dress up a Strategy 3 move as a Strategy 2 nudge — sellers can tell, and it damages trust for the rest of the transaction.

---

## Intake (Ask in One Message)

Collect the following before generating the angle:

1. **Subject property:** address, current list price, total days on market (DOM)
2. **Property details:** beds, baths, square footage, year built, lot size, condition tier, key features or recent upgrades
3. **Listing history:**
   - Original list price (if different from current)
   - Any prior price reductions (date and amount)
   - Listing date
4. **Market activity to date:**
   - Total showings (or showing count for last 2 weeks)
   - Total offers received (or "zero")
   - Showing feedback (paste any agent feedback received)
   - Buyer agent comments / common objections
5. **Seller context:**
   - Timeline pressure (relocation deadline, dual mortgage, etc.)
   - Emotional sensitivities (inheritance, divorce, recent passing, health)
   - History of price-conversation pushback
   - Communication preference (in-person, phone, text, email)
6. **Comparable data — pick one:**
   - Upload an MLS export (CSV, XLSX) of recently sold + active comps in the area
   - Reference a recent CMA: "We ran a CMA for this property on [date]" — I'll pull from `cma-reports/cmas/`
   - Paste comp data directly
   - Provide MLSListings search criteria — I'll guide you through the Chrome pull

**Hard requirement: comp data is required.** This skill is only useful when grounded in real numbers. If comps aren't provided, ask for them — do not proceed.

**Time window:** comps should be from the last 30–90 days, same area, similar property type. Adjust window if the market is fast-moving (30 days) or slow (90+ days).

---

## Analysis Process

### Step 1: What's Moving

From the comp data, identify properties that **sold** (closed) recently. Note:
- Price range where closings are concentrated (median, 25th/75th percentile)
- Average DOM for sold properties vs. the subject's DOM
- List-to-sale ratio for sold properties (selling at, above, or below list?)
- Features or price brackets that sold fastest
- Any properties that received multiple offers (these are the market-aligned comps)

### Step 2: What's Sitting

Identify **active listings** that have been on market for 30+ days (or the equivalent threshold for the local market velocity). Note:
- Price points where stale listings cluster
- How they compare to the subject in features and price-per-square-foot
- Pattern in what's not selling (overpriced per sqft, missing key features, wrong price tier for the condition tier)

### Step 3: Where the Subject Fits

Place the subject property in context:
- Is it priced above, at, or below the range where properties are actually closing?
- Price-per-square-foot vs. sold comps?
- Feature gaps that explain low activity (no garage in an area where every sold comp had one, fixer in an area where renovated comps are moving, etc.)?
- What price position would the data suggest for offers within [seller's timeline]?

### Step 4: Pick the Strategy

Based on Steps 1–3, decide which strategy the recommended new price represents:
- **Strategy 2 (Market-Aligned):** subject is overpriced by 5–10% vs sold comps. Adjustment brings it to the range where buyers are actively engaging.
- **Strategy 3 (Move-It):** subject is overpriced by 10%+ vs sold comps OR has feature gaps OR seller has hard timeline pressure. Adjustment goes below the median sold range to trigger offers fast.

Be honest about which strategy you're recommending — both internally in the analysis and externally when you present it.

---

## Output

Produce three things, in this order:

### 1. The Angle (2–3 sentences)

A clear, seller-facing positioning statement. This is the talking point the agent walks in with. It must:
- Reference a **specific data point**, not a feeling
- Frame the adjustment as **market-alignment strategy**, not concession or defeat
- Avoid blame, pressure, urgency, or fear language
- Avoid the words "lower," "drop," or "reduce" if possible — use "reposition," "align," "adjust to where buyers are engaging"

**Example (Strategy 2 — market-aligned):**
> "The homes that sold in your neighborhood this month all closed between $1.45M and $1.58M. At $1.65M, your home is priced above every comparable that actually went under contract. Repositioning to $1.55M places you at the top of the range buyers are actively choosing from — competitive, not desperate."

**Example (Strategy 3 — move-it):**
> "Five comparable homes sold in the last 60 days, all between $1.40M and $1.55M, with a median DOM of 14 days. Your listing has been at $1.65M for 47 days with two showings in the last two weeks. The data is telling us we're priced outside the active buyer range. A move to $1.49M positions you mid-range where the recent buyer activity has been concentrated, and would likely generate showings within the first week."

### 2. Supporting Data Points (3–4 bullets)

Specific numbers from the comp analysis that back up the angle. These are the receipts the agent shows the seller if they push back. Format each as a single line:

```
- Sold comps last 60 days: median sale $1.49M, median DOM 14 days, list-to-sale ratio 102%
- Subject listing: 47 days on market at $1.65M, 2 showings in last 2 weeks, 0 offers
- Active competitors at $1.6M+: 4 listings, average DOM 38 days — also not moving
- Price per square foot: sold comps $920–$1,010/sqft, subject currently $1,082/sqft
```

Each bullet is a data point, not commentary. Numbers, not adjectives.

### 3. Suggested Next Step (1 sentence)

A single-sentence recommended action. Pick from:
- **Adjust to a specific price range** — if the seller is open to repositioning
- **Schedule a strategy call** — if the seller needs to hear it from the agent in person
- **Run a fresh comp analysis after [N] more weeks** — if the seller wants to wait
- **Reframe marketing without price change** — if the issue is exposure, not price (rare; only suggest if data supports it)

The next step is concrete and time-bound. "Let's discuss" is not a next step — "Let's adjust to $1.55M effective Monday and revisit in 14 days if showings don't increase" is a next step.

---

## Tone Rules

- **Empathetic but honest.** The agent's credibility depends on telling the truth without being harsh.
- **Never use urgency or fear tactics** ("if you don't reduce now, you'll never sell").
- **Never reference the seller's personal situation in the positioning statement** — that's for the agent to manage in conversation. The data speaks for itself.
- **Never imply the home is "too good" for the market** — that frames the seller as the victim and undermines the data.
- **Never blame the staging, the photos, the season, or the agents who showed it without an offer** — unless that's specifically what the data points to AND the agent wants to address marketing rather than price.

---

## Bay Area / Peninsula Market Notes

When the subject is in Graeham's primary markets, factor in market-velocity norms:

- **Hot Bay Area markets (EPA, RWC, MP, PA at certain price points):** sold-DOM under 21 days is normal. A listing at 30+ DOM signals price misalignment, not just slow market.
- **Mid-velocity markets (most of San Mateo County):** sold-DOM 21–45 days is normal. 60+ DOM signals price misalignment.
- **Slower markets (luxury $3M+, certain unincorporated areas):** sold-DOM 60–90 days can be normal. Adjust thresholds.

Recent rate environment: in higher-rate environments, list-to-sale ratios compress and DOM extends across all tiers. Note this in the angle if relevant ("market velocity has slowed across the Peninsula since [period]") — but don't use it as an excuse for the listing's specific underperformance.

---

## Integration With Other Skills

- **`cma-generator`** — if a CMA was generated for this property in the last 60 days, use that comp set as the starting point. Don't re-analyze comps from scratch.
- **`mls-data-analyzer`** (when built — Phase 4 of the skills roadmap) — pulls market context narrative for the angle's framing.
- **`content-creation-engine`** — does NOT use this skill directly. The price-reduction conversation is private seller communication, not marketing content. Stay separate.
- **Apify Zillow scraper** — useful for active competitor analysis ("here's what's also sitting on the market at this price point") if MLS data is incomplete.

---

## Output Delivery

Default delivery is plaintext, ready for the agent to copy into a phone-call notes app or paste into an email/text draft.

If the user requests:
- **Email format** — wrap the angle as the email body, the receipts as a bulleted list below, and the next step as the closing CTA
- **Text/SMS format** — collapse to under 320 characters, lead with the angle's first sentence, end with the next step
- **In-person talking points** — present as a numbered talking-point list with the receipts annotated as "if seller pushes back on this point, show: [receipt]"

After delivery, optionally provide:
- **Compliance check** — confirm no Fair Housing language, no demographic references, no fabricated stats
- **Confidence note** — flag any data point in the angle that came from a small sample size (fewer than 5 comparable sales) or an outlier-prone metric

---

## Used By

- **Standalone** — agent has a stale listing and needs the price-reduction conversation framed.
- **Triggered by signals from `social-media-analyzer` or `content-calendar`** (future) — if a listing has been on market past its market-velocity threshold and is showing performance signals consistent with overpricing, those skills could surface the listing for a price-reduction angle review. Manual trigger only for now.
