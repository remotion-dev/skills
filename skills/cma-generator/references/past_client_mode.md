# Past-Client Mode — Home Value Update Layer

This layer turns the standard CMA into a warm, personalized **home-value update for an existing owner** who is NOT selling. It sits on top of the normal cma-generator methodology (same data rigor, same brand, same charts) but changes the framing, section set, and voice so it reads like a personal note from their agent — not a listing presentation or a buyer offer analysis.

Use it whenever the CMA is for a past client: PCFS cadence, "home value update," "equity update," anniversary touch, "keep them posted," or any owner who isn't actively listing.

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

- [ ] **Second-person voice throughout** — "your home," "where you stand." Never "the home" / 