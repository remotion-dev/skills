# Past-Client Mode — Home Value Update Layer

This layer turns the standard CMA into a warm, personalized **home-value update for an existing owner** who is NOT selling. It sits on top of the normal cma-generator methodology (same data rigor, same brand, same charts) but changes the framing, section set, and voice so it reads like a personal note from their agent — not a listing presentation or a buyer offer analysis.

Use it whenever the CMA is for a past client: PCFS cadence, "home value update," "equity update," anniversary touch, "keep them posted," or any owner who isn't actively listing.

---

## BANNED in every past-client report (hard rule, 2026-06-08)

NEVER include data-source apologies or MLS-access caveats in the client output. Specifically banned (verbatim and paraphrased): "built from public data / Redfin / Zillow because MLS was not signed in," "public data is less precise than the MLS," "treat as a solid estimate rather than an exact figure," "let me run a full MLS-verified version," "marked N/A and flagged," a "Notes and Honest Caveats" section, a "Data source" disclaimer, "No agenda here," "I have not been inside recently," "this is simply a where-you-stand update," and any "About this analysis" line that blames the data source for lower confidence. The only allowed disclaimer is one clean line: "Professional opinion of value, not a formal appraisal." Source/tooling notes go to Graeham privately, never in the report. For off-MLSListings markets (Alameda County: Union City, Fremont, Hayward) source comps from public data and present them confidently with the MLS-only columns omitted, not flagged. END the report on a warm referral CTA, not a caveat (see cma-generator SKILL.md). Include the months-of-inventory metric like every other mode.

---

## MANDATORY CHECKLIST — every Past-Client CMA must include ALL of these

Past-Client Mode inherits the standard cma-generator rigor in full. Every "REQUIRED" item in `cma-generator/SKILL.md` applies — past-client mode changes the *story and labels*, not the *data discipline or visual completeness*. If any single item below is missing from the published HTML, the CMA is incomplete and must be regenerated before sending.

This checklist was added 2026-05-26 after auditing the autobuild outputs for Ravi Indurkar (347 Avenida Pinos), Viduishi Jain (939 Runnymede), and Narasimha Subraveti (1515 Treviso). Those three were missing 4 of the 5 required charts, the Interest Rate Environment section, the Original-List/Reductions/L-to-S columns, the branded nav, and used em-dashes throughout. Do not repeat that pattern.

### Brand & styling (non-negotiable)

- [ ] Graeham Watts realtor nav bar fixed at the top (logo + page links: Home, Buy, Sell, Buying in the Bay, The Bay Market, Neighborhoods, Blogs, About, Reviews, Contact). Logo: `https://images.leadconnectorhq.com/image/f_webp/q_80/r_1200/u_https://assets.cdn.filesafe.space/6wuU3haUH7uNeT20E3UZ/media/691256870b647e40e3c2e105.png`. Nav background `#343955`.
- [ ] Brand colors throughout: black `#1A1A1A`, gold `#C5A55A`, white `#FFFFFF`. NOT a generic Tailwind/grey template.
- [ ] DRE **#01466876** in header and footer. **Read from `shared-references/identity.json` — never type from memory** (one specific other DRE has been blocklisted and leaks 10+ times running).
- [ ] Premium typography (Inter / Montserrat via Google Fonts), card layouts with gold dividers and shadows. NOT plain markdown-style.

### Charts — all five Chart.js canvases required

- [ ] `trendPrice` — monthly Sale Price Avg, 5+ years of MLSListings Matrix Stats. Caption: "Source: MLSListings Matrix Stats, [filter], [N] listings."
- [ ] `trendLS` — monthly Sale/List Ratio over the same window.
- [ ] `priceJourney` — multi-line, Original → Final → Sold price for each of the closest 8-10 sold comps. Green up / coral down per direction.
- [ ] `domVsCut` — dual-axis bar showing DOM and $-cut per comp.
- [ ] `priceDom` — bubble scatter of full cohort: x = sold price, y = DOM, bubble size = sqft, color = status. OR geographic heat map if comp addresses geocode cleanly.
- [ ] Plus the existing `$/sqft chart` — keep it; do not replace the trend charts with it.

A CMA with only the `$/sqft chart` (which is what the May 25 autobuilds shipped) is not complete.

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
5. Trend Context — the `trendPrice` and `trendLS` charts side by side
6. **Interest Rate Environment** — 4-source cross-reference (Mortgage News Daily, Freddie Mac PMMS, Bankrate California, Realtor.com local), one-line plain-English read on what it means for the owner's equity (NOT framed for selling)
7. Price-Reduction History table + `priceJourney` chart
8. `domVsCut` chart
9. Subject vs Most Similar Comps comparison table (subject row highlighted with gold accent)
10. `priceDom` scatter or geographic heat map
11. **What Your Home Is Worth Today** — three range cards: Likely range / Most-likely value today / Top of range in strong condition
12. Equity context paragraph (e.g., "you bought in 2020 for ~$X; comparable homes are now around $Y — roughly $Z appreciation")
13. Honest Notes / Caveats (data source, condition, market timing)
14. Closing / Contact (warm, no-agenda)

### Voice & punctuation (auto-failing)

- [ ] **Second-person voice throughout** — "your home," "where you stand." Never "the home" / "the client" / "the seller" / third-person references to the client by name inside body prose.
- [ ] **Zero em-dashes** (`—`, `&mdash;`, ` -- `) in published HTML. Use "to" (for ranges), commas, colons, parens. En-dashes for numeric ranges (1,500–2,000) are acceptable; prefer "1,500 to 2,000" in client-facing prose.
- [ ] No corporate filler ("nestled in," "comprehensive analysis," "compelling opportunity," "stands as a testament").
- [ ] Past-client framing only — never "let's list," "ready to sell?", "we should price at." One soft, low-key offer at the close is the maximum: "if you ever want to talk through what a sale would actually net you, I'm here."
- [ ] Final pass through the **humanizer** skill before publish. CMA narrative that sounds AI-generated kills trust the moment they read it.

### Data quality

- [ ] **Submarket boundary check** — if the cohort spans east-of-101 vs west-of-101 in EPA, school district lines, original-Eichler vs newer build, etc., identify which side the subject is on and flag any cross-boundary comp.
- [ ] If MLS was unavailable during the run: prominent "Public Data Notice" banner at top + recommendation for Graeham to re-run when MLS is back. All figures hard-flagged as directional only.
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
| Closing | Warm, no-agenda sign-off from Graeham |

If a section would only make sense to someone about to sell (staging advice, list-timing strategy, days-on-market targets framed as "to sell fast"), cut or re-frame it.

---

## Voice rules

- Address the client by **first name** in the email and, where natural, the report intro.
- **No sales push.** Never "let's list," "ready to sell?", "call me to get started." The one soft offer allowed mid-body: "if you ever want to talk through what a sale would actually net you, I'm here" — once, low-key.
- **Opener (required).** Open warm and unfussy, stating plainly that this is a quick market update sent to keep them in the loop. Use the spirit of: "Just sending over a quick comparative market analysis to keep you updated on [street / your area]." Do not over-explain or imply you've been "running numbers" for them.
- **Referral CTA (required, this is how the report ENDS).** Close on a warm referral ask, not a no-agenda line. Spirit of: "One quick ask — if you know anyone thinking about buying or selling, I'd be grateful for the introduction. Just reply with their name, forward them this update, or give me a call." Make it easy and specific (reply / forward / call). This replaces the old "no agenda at all" sign-off as the final beat.
- Lead with **equity and standing**, not price-to-list. If purchase price + date are known: "you bought in [year] for $X; comparable homes are now around $Y — that's roughly $Z in appreciation."
- Warm, plain, human. Run the final copy through the **humanizer** skill. No em-dash overuse, no "nestled," no corporate filler.
- Honesty intact: still flag thin comp data, condition unknowns, and "professional opinion of value, not a formal appraisal."

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
3. **Client email** — suggested subject with a 🔥 fire emoji, warm first-name greeting, 2-3 short paragraphs (market is good to you / where your home stands / quick equity context), the CMA as a **clickable link/button**, and a no-agenda close.

### Example client email body (adapt per client)

> Subject: 🔥 A quick update on your [City] home
>
> Hi [First name],
>
> Hope you and the family are doing well! Just sending over a quick comparative market analysis to keep you updated on [street].
>
> Short version: the market's been good to you. Homes like yours in [area] have been selling around [range], and based on the recent sales your place is most likely worth somewhere around **[most-likely value]** today[, with room toward [top] if it shows in top shape]. For perspective, that'