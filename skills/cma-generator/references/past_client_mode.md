# Past-Client Mode — Home Value Update Layer

This layer turns the standard CMA into a warm, personalized **home-value update for an existing owner** who is NOT selling. It sits on top of the normal cma-generator methodology (same data rigor, same brand, same charts) but changes the framing, section set, and voice so it reads like a personal note from their agent — not a listing presentation or a buyer offer analysis.

Use it whenever the CMA is for a past client: PCFS cadence, "home value update," "equity update," anniversary touch, "keep them posted," or any owner who isn't actively listing.

---

## BANNED in every past-client report (hard rule, 2026-06-08)

NEVER include data-source apologies or MLS-access caveats in the client output. Specifically banned (verbatim and paraphrased): "built from public data / Redfin / Zillow because MLS was not signed in," "public data is less precise than the MLS," "treat as a solid estimate rather than an exact figure," "let me run a full MLS-verified version," "marked N/A and flagged," a "Notes and Honest Caveats" section, a "Data source" disclaimer, "No agenda here," "I have not been inside recently," "this is simply a where-you-stand update," and any "About this analysis" line that blames the data source for lower confidence. The only allowed disclaimer is one clean line: "Professional opinion of value, not a formal appraisal." Source/tooling notes go to Graeham privately, never in the report. For off-MLSListings markets (Alameda County: Union City, Fremont, Hayward) source comps from public data and present them confidently with the MLS-only columns omitted, not flagged. END the report on a warm referral CTA, not a caveat (see cma-generator SKILL.md). Include the months-of-inventory metric AND chart like every other mode.

**ALSO banned (Graeham feedback 2026-06-11, Basswood CMA):**
- ANY "no agenda" phrasing, anywhere in the report or email: "no agenda attached," "no agenda here," "with no agenda," "no-pressure update," "nothing being pitched," "I like to check in with past clients now and then." Graeham: "That's a little too salesy." The correct register is plain: "Here is an update on your home, just keeping you informed."
- A "Notes & Caveats" closing section in ANY form, even when MLS data was full-confidence. That includes the cards "About this analysis," "What would sharpen this further," and "Condition matters." Condition nuance lives INSIDE the three value-range card descriptions ("top of range if updated, floor if dated"), never as a standalone caveat card. Graeham: "We don't need these notes for sending a client an email on property values."
- An apologetic comp table: never print N/A columns. If a column's data is unavailable, OMIT the column.

---

## MANDATORY CHECKLIST — every Past-Client CMA must include ALL of these

Past-Client Mode inherits the standard cma-generator rigor in full. Every "REQUIRED" item in `cma-generator/SKILL.md` applies — past-client mode changes the *story and labels*, not the *data discipline or visual completeness*. If any single item below is missing from the published HTML, the CMA is incomplete and must be regenerated before sending.

This checklist was added 2026-05-26 after auditing the autobuild outputs for Ravi Indurkar (347 Avenida Pinos), Viduishi Jain (939 Runnymede), and Narasimha Subraveti (1515 Treviso). Those three were missing 4 of the 5 required charts, the Interest Rate Environment section, the Original-List/Reductions/L-to-S columns, the branded nav, and used em-dashes throughout. Do not repeat that pattern.

### Brand & styling (non-negotiable)

- [ ] Graeham Watts realtor nav bar fixed at the top (logo + page links: Home, Buy, Sell, Buying in the Bay, The Bay Market, Neighborhoods, Blogs, About, Reviews, Contact). Logo: `https://images.leadconnectorhq.com/image/f_webp/q_80/r_1200/u_https://assets.cdn.filesafe.space/6wuU3haUH7uNeT20E3UZ/media/691256870b647e40e3c2e105.png`. Nav background `#343955`.
- [ ] Brand colors throughout: black `#1A1A1A`, gold `#C5A55A`, white `#FFFFFF`. NOT a generic Tailwind/grey template.
- [ ] DRE **#01466876** in header and footer. **Read from `shared-references/identity.json` — never type from memory** (one specific other DRE has been blocklisted and leaks 10+ times running).
- [ ] Premium typography (Inter / Montserrat via Google Fonts), card layouts with gold dividers and shadows. NOT plain markdown-style.

### Charts — SAME chart set as listing presentations and buyer offers (Graeham rule, 2026-06-11)

Past-client updates use the SAME graphs the listing-presentation and buyer-offer CMAs use. Do not invent a reduced or substitute chart set. Required canvases:

- [ ] `trendPrice` — monthly Sale Price Avg/Median trend. MLS source: 5+ years of MLSListings Matrix Stats, caption "Source: MLSListings Matrix Stats, [filter], [N] listings." Off-MLS markets: trailing 12 months from Redfin/Zillow market data, cited cleanly ("Source: Redfin market data"), no meta-commentary.
- [ ] `trendLS` — monthly Sale/List Ratio over the same window.
- [ ] `newList` — new listings per month (bar chart), same window.
- [ ] `monthsInv` — **months of inventory** (active listings ÷ monthly closed-sale pace), line chart with a dashed reference line at 3 months ("balanced market"). This is the chart Graeham flagged as missing 2026-06-11. Under ~3 months = seller's market; explain the read in one plain sentence in the prose.
- [ ] `compBar` — horizontal bar of comparable sold prices with the subject's most-likely value in black among gold bars (color-split by city when the cohort spans cities).
- [ ] `priceDom` — bubble scatter of full cohort: x = sold price, y = DOM (or y = $/sqft when DOM is unavailable for the market), subject as black/gold diamond.
- [ ] `priceJourney` — past-client bonus chart: purchase price → today's most-likely value with dashed low/high range lines (the "equity journey"). Keep it; it is the one chart unique to this mode.
- [ ] Plus the existing `$/sqft chart` — keep it; do not replace the trend charts with it.

A CMA with only the `$/sqft chart` (which is what the May 25 autobuilds shipped) is not complete. A CMA missing `monthsInv` or `newList` (the June 8 Basswood build) is not complete either.

### Comp table columns — every column required

| Column | Notes |
|---|---|
| Address | |
| Bed / Bath | |
| Sqft | |
| Lot size | |
| Year built | |
| **Original List Price** | from MLS History tab |
| **Final List Price** | last list before sale |
| **Sold Price** | bold |
| **# of Reductions** | count of price decreases between original list and sold |
| **$-cut from original list** | dollar amount |
| DOM | color-coded: green <15, gold 15-30, red >30 |
| Sold Date | |
| **List-to-Sale %** | sold ÷ original list × 100 |
| $/sqft | sold ÷ sqft |
| Condition note | plain language |

The bolded columns are the ones most commonly skipped and the ones the May 25 outputs omitted. They are non-optional.

### Required sections (in this order)

1. Hero — "HOME VALUE UPDATE" + subject address + "Prepared for [First name], [Month Year]"
2. Subject Property Summary — with **ownership context** (years owned, equity gained since purchase if COE date + estimated purchase price are known)
3. The Market Story / "Where the Market Is" — 4-6 paragraphs in **second person**, no commission math
4. Comp Cohort table (every column above)
5. Trend Context — `trendPrice`, `trendLS`, `newList`, and `monthsInv` charts (the same trend set as listing/buyer CMAs)
6. **Interest Rate Environment** — 4-source cross-reference (Mortgage News Daily, Freddie Mac PMMS, Bankrate California, Realtor.com local), one-line plain-English read on what it means for the owner's equity (NOT framed for selling)
7. Price-Reduction History table + `priceJourney` equity chart
8. `compBar` chart (comp sold prices with subject highlighted)
9. Subject vs Most Similar Comps comparison table (subject row highlighted with gold accent)
10. `priceDom` scatter or geographic heat map
11. **What Your Home Is Worth Today** — three range cards: Likely range / Most-likely value today / Top of range in strong condition, followed by the single disclaimer line "Professional opinion of value, not a formal appraisal."
12. Equity context paragraph (e.g., "you bought in 2020 for ~$X; comparable homes are now around $Y — roughly $Z appreciation")
13. Closing / Contact — warm referral CTA (see Voice rules). **NO Notes/Caveats section** (banned above); condition nuance lives inside the range cards.

### Voice & punctuation (auto-failing)

- [ ] **Second-person voice throughout** — "your home," "where you stand." Never "the home" / "the client" / "the seller" / third-person references to the client by name inside body prose.
- [ ] **Zero em-dashes** (`—`, `&mdash;`, ` -- `) in published HTML. Use "to" (for ranges), commas, colons, parens. En-dashes for numeric ranges (1,500–2,000) are acceptable; prefer "1,500 to 2,000" in client-facing prose.
- [ ] No corporate filler ("nestled in," "comprehensive analysis," "compelling opportunity," "stands as a testament").
- [ ] Past-client framing only — never "let's list," "ready to sell?", "we should price at." One soft, low-key offer at the close is the maximum: "if you ever want to talk through what a sale would actually net you, I'm here."
- [ ] Final pass through the **humanizer** skill before publish. CMA narrative that sounds AI-generated kills trust the moment they read it.

### Data quality

- [ ] **Submarket boundary check** — if the cohort spans east-of-101 vs west-of-101 in EPA, school district lines, original-Eichler vs newer build, etc., identify which side the subject is on and flag any cross-boundary comp.
- [ ] If MLS was unavailable during the run: the client report stays clean and confident (public-data comps presented plainly, MLS-only columns omitted, NO banner, NO flags, NO N/A cells). The "PUBLIC-FALLBACK / re-run when MLS is back" notice goes ONLY in the internal section of the companion email to Graeham. (This replaces the old "Public Data Notice banner" rule, which contradicted the ban above and caused the 2026-06-08 Basswood miss.)
- [ ] All math recomputed in Python (`mcp__workspace__bash`) — never eyeballed.
- [ ] Mandatory QC verification pass per `cma-generator/SKILL.md` §Quality Control Verification before publish.

---

## The mindset shift

A listing CMA answers "what should I list this for?" A past-client update answers **"what is my home worth right now, and how's my equity doing?"** The owner asked for nothing — Graeham is proactively keeping them informed because that's what a good agent does between transactions. So nothing in the piece should feel like a pitch.

---

## Section changes vs the standard (listing) report

| Standard listing section | Past-Client Mode |
|---|---|
| Hero: "Listing Presentation" / "Buyer Offer Analysis" | **"Home Value Update"** |
| "Pricing Strategy Analysis" (below / at / above market) | **DELETE.** Replace with "What Your Home Is Worth Today" |
| "Recommended List Price" — Conservative / Competitive / Stretch | **"Your Home's Value Today"** — Likely range / Most-likely value today / Top of range in strong condition |
| "The Market Story" written toward a pricing decision | Same data, written toward *where the owner stands* |
| Subject summary | Keep — but add ownership context (years owned, equity gained) when known |
| Comparable sales + $/sqft chart | Keep as-is |
| Market data & trends | Keep as-is |
| Special considerations | Keep — frame as "things that affect your value," not "things to fix before listing" |
| Closing | Warm referral-CTA close from Graeham (never "no agenda" phrasing) |

If a section would only make sense to someone about to sell (staging advice, list-timing strategy, days-on-market targets framed as "to sell fast"), cut or re-frame it.

---

## Voice rules

- Address the client by **first name** in the email and, where natural, the report intro.
- **No sales push.** Never "let's list," "ready to sell?", "call me to get started." The one soft offer allowed mid-body: "if you ever want to talk through what a sale would actually net you, I'm here" — once, low-key.
- **Opener (required).** Open warm and unfussy, stating plainly that this is a quick market update sent to keep them in the loop. Use the spirit of: "Hi [First name], here is an update on your home, just keeping you informed." or "Just sending over a quick comparative market analysis to keep you updated on [street / your area]." Do not over-explain, do not imply you've been "running numbers" for them, and NEVER add "with no agenda attached," "no-pressure update," or "I like to check in with past clients now and then" — Graeham flagged all of those as too salesy (2026-06-11). Plain and straightforward wins.
- **Referral CTA (required, this is how the report ENDS).** Close on a warm referral ask, not a no-agenda line. Spirit of: "One quick ask — if you know anyone thinking about buying or selling, I'd be grateful for the introduction. Just reply with their name, forward them this update, or give me a call." Make it easy and specific (reply / forward / call). This replaces the old "no agenda at all" sign-off as the final beat.
- Lead with **equity and standing**, not price-to-list. If purchase price + date are known: "you bought in [year] for $X; comparable homes are now around $Y — that's roughly $Z in appreciation."
- Warm, plain, human. Run the final copy through the **humanizer** skill. No em-dash overuse, no "nestled," no corporate filler.
- Honesty intact, but quietly: thin comp data and condition assumptions are expressed inside the range-card descriptions and internal notes to Graeham, never as caveat cards or disclaimer sections. The one allowed disclaimer line: "Professional opinion of value, not a formal appraisal."

---

## Value section (replaces Pricing Strategy + Recommended List Price)

Header: **"What Your Home Is Worth Today"**. Three range cards, relabeled:

- **Likely range** (green accent) — the safe floor, accounting for condition/lot.
- **Most-likely value today** (gold accent) — anchored on the closest comps. This is the headline number.
- **Top of range in strong condition** (coral accent) — what it could reach if it shows turnkey.

Frame as current market value / equity, never as a list price. Keep the subject-positioning chart (where the home sits among comps).

---

## Companion email (for PCFS review-and-forward)

**As of 2026-05-26, the PCFS autobuild SENDS this email directly to Graeham + Adrian's clientcare inbox (no longer a draft).** Drafts were getting lost in the Drafts folder; direct sends land in the inbox where they'll be seen. The "never auto-send to the client" guardrail is preserved — the email goes only to Graeham + Adrian, who manually forward the bottom (client-facing) section after reviewing the top section.

Structure:

1. **Internal note** at top (clearly marked for deletion before forwarding): client's forward-to email shown prominently (`📧 FORWARD TO: client@email.com`), value range, live CMA link, data source (MLS-FULL vs PUBLIC-FALLBACK), QC caveats.
2. **Bold divider** — visually impossible-to-miss banner like `⬇️⬇️⬇️ DELETE EVERYTHING ABOVE THIS LINE BEFORE FORWARDING ⬇️⬇️⬇️` rendered as a colored HTML block in the styled body.
3. **Client email** — suggested subject with a 🔥 fire emoji, warm first-name greeting, 2-3 short paragraphs (market is good to you / where your home stands / quick equity context), the CMA as a **clickable link/button**, and a warm referral-CTA close. Run the client section through the **humanizer** skill before sending to Graeham. No "no agenda" / "no-pressure" phrasing anywhere in it.

### Example client email body (adapt per client)

> Subject: 🔥 A quick update on your [City] home
>
> Hi [First name],
>
> Hope you and the family are doing well! Just sending over a quick comparative market analysis to keep you updated on [street].
>
> Short version: the market's been good to you. Homes like yours in [area] have been selling around [range], and based on the recent sales your place is most likely worth somewhere around **[most-likely value]** today[, with room toward [top] if it shows in top shape]. For perspective, that's [equity context vs purchase].
>
> I put together a quick visual breakdown — recent comparable sales, the charts, and where your home lands:
>
> [View your home value update →](LIVE_LINK)
>
> One quick ask: if you know anyone thinking about buying or selling, I'd be grateful for the introduction — just reply with their name, forward them this update, or give me a call. Referrals from past clients mean the world.
>
> [Graeham sign-off + contact block]

### Past SELLER who no longer owns the subject property (rule hardened 2026-06-11)

**The CMA must be on a home the client currently OWNS. Never build or send a CMA on a property the client sold.** Graeham killed the old "former home / neighborhood market update" fallback on 2026-06-11 (Brandon Lewke / 101 Garden case): "the CMA should be on a home they own."

Decision tree for a past seller:
1. **Current home address known** (GHL, Master Past Clients sheet, Excel)? Build the CMA on the CURRENT home. The sold property is history; it may appear only as a one-line equity footnote if relevant.
2. **Current home address unknown?** Do NOT generate a CMA at all. HOLD the touch and trigger the address-lookup flow (Glide/SkySlope first; then title-plant request to Daniel Dietrich, danield@octitle.com, cc Giselle graehamwattstc@gmail.com — see PCFS claude-code-operations.md). Tell Graeham which clients are on hold and why. Resume once the address lands.
3. Never mail a physical note to the sold address (that goes to the new owner), and never email the client a report about the home they sold.

Before building ANY past-client CMA, verify ownership: confirm the subject property's last recorded sale is the client's purchase (not their sale to someone else). If the client appears on the SELL side of the last transaction, apply this decision tree.

---

## What stays identical to the standard skill

Brand (DRE #01466876 from `shared-references/identity.json`), the graehamwatts.com nav, Chart.js charts, comp-selection rules (1-mile / same-city / sqft range / recency), the mandatory QC verification pass, and GitHub Pages publishing. Past-Client Mode changes the *story and labels*, not the *data discipline*.
