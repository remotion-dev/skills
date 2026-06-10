# Output Formats & Quality Control Verification — moved verbatim from `cma-generator/SKILL.md` (2026-06-09 refactor)

## Output Formats

The CMA can be delivered in three formats. Ask the user which they prefer, or generate all three.

### 1. Interactive HTML Report (Recommended Primary)
- Single self-contained .html file that opens in any browser
- Uses Chart.js via CDN for interactive charts with tooltips, hover effects, animations
- Modern web design: sticky nav, animated counters, card layouts, glassmorphism, gradient backgrounds
- Google Fonts (Inter/Montserrat) for premium typography
- Smooth scroll navigation between sections
- Sortable comp tables, collapsible sections
- Fully responsive (works on desktop, tablet, mobile)
- Best for: sending as an attachment clients can open in browser, presentations on screen, sharing via link
- This is the format that looks the most impressive and professional

### 2. Email-Safe HTML
- Stripped-down HTML with ALL inline styles (no external CSS, no JavaScript, no CDN links)
- Table-based layout for Gmail/Outlook/Apple Mail compatibility
- Charts as base64-embedded matplotlib PNG images
- 600px max-width for email rendering
- System font stack (no Google Fonts)
- Condensed version: property summary, top 8 comps, pricing strategy, recommendation
- Best for: pasting into Gmail, sending directly to clients, quick follow-ups
- Can be sent via Gmail API or copy-pasted into email client

### 3. PDF Report (Generated from HTML)
- Use WeasyPrint or xhtml2pdf to convert a print-optimized HTML to PDF
- Alternatively, fall back to ReportLab + matplotlib if HTML-to-PDF tools aren't available
- Charts as static matplotlib images embedded as base64
- CSS @media print rules for proper page breaks
- Removes interactive elements (sticky nav, animations, scroll effects)
- Keeps premium CSS styling (gradients, shadows, card layouts)
- Best for: printing, formal email attachments, archiving
- Install: `pip install weasyprint --break-system-packages` (preferred) or `pip install xhtml2pdf --break-system-packages` (fallback)

---

## Quality Control Verification (MANDATORY)

**This step is not optional.** Before delivering any CMA report, you MUST run a full verification pass. A CMA with wrong comps, bad math, or unsupported pricing recommendations can cost a client tens of thousands of dollars — either by pricing too high and sitting on market, or pricing too low and leaving money on the table. Every report must be checked before it goes out.

### The Verification Process

After generating the report, perform a distinct second pass. Do NOT just re-read what you wrote — go back to the source data (MLS exports, comp details) and cross-check against the report.

### What the Verification Checks

**1. Comp Selection Accuracy**
- Re-verify every comp meets the search criteria: within 1 mile (or justified expansion), same city (city boundaries override radius), reasonable sqft range, appropriate time frame
- Check that no comp from a different city was included without being explicitly flagged
- If a comp is in the "Most Similar" tier, verify it truly is the most comparable — right sqft range, similar condition, same city
- If fewer than 3 primary comps, verify the report flags "Limited data — use with caution"

**2. Data Accuracy**
- Spot-check at least 5 comp entries against the source MLS data: sold price, list price, sqft, lot size, bed/bath count, DOM, sold date
- Verify $/sqft calculations: sold price ÷ sqft = $/sqft (check at least 5 comps)
- Verify list-to-sale ratios: sold price ÷ list price × 100 (check at least 5 comps)
- Verify all summary statistics (median price, average price, average DOM, etc.) by recalculating from the comp data
- Check that no comp appears twice in the tables

**3. Pricing Recommendation Accuracy**
- Verify each pricing range (Conservative, Competitive, Stretch) is actually supported by the comp data
- The Conservative range should align with the lower tier of comparable sales
- The Competitive range should align with the cluster of most similar comps
- The Stretch range should have at least some data support — not just wishful thinking
- Cross-check: does the recommended $/sqft fall within the range shown by comps?
- If strategies reference specific comps ("like 123 Main St which sold for $X"), verify those numbers match

**4. Chart and Visual Accuracy**
- Verify that all charts render correctly (no broken images, no empty charts)
- Check that chart data matches the tables — if the table shows 12 comps, the chart should show 12 data points
- Verify the Subject Property Positioning bubble/chart places the subject correctly relative to comp data
- Check that the List-to-Sale Ratio visual shows bars in the correct direction (over asking = right/gold, under asking = left/coral)
- Verify price distribution histogram bins are reasonable and don't hide outliers

**5. Narrative Consistency**
- Read the Market Story (Section 3) and verify every claim is supported by the data in subsequent sections
- If the narrative says "most homes sold over asking" verify the list-to-sale data actually shows this
- If the narrative mentions a trend ("prices are rising"), verify the data supports it (compare recent vs older comp prices)
- Make sure the narrative and the pricing recommendation tell the same story — they shouldn't contradict each other

**6. Formatting and Branding**
- Verify brand colors are correct: black (#1A1A1A), gold (#C5A55A), white (#FFFFFF)
- Check that Graeham's name, DRE number, and contact info are correct throughout
- Verify the report renders properly at different screen widths if it's HTML
- Check for typos in property addresses and dollar amounts (these are the most embarrassing errors)

### Verification Output

Fix any errors found during verification. If a pricing range changed, a comp was removed, or a statistic was corrected, mention the correction to the user so they know the report was refined.

**Only deliver the report after verification is complete.**

### 7. Humanizer Pass on Narrative Sections (Mandatory)

After the data verification pass and BEFORE pushing to GitHub Pages or delivering to the client, run every prose section of the CMA through the `humanizer` skill. CMA narrative is what wins or loses listing presentations — sellers can tell when the Market Story sounds like a model wrote it, and the trust drop kills the listing appointment before pricing even comes up.

**What gets humanized:**
- Section 3: The Market Story (4-6 paragraphs) — this is the highest-stakes prose in the report
- Section 4: The 2-3 sentence comp explanations for each primary comp
- Section 5: The "Key insight" paragraph interpreting market conditions
- Section 6: The 3-4 sentence narrative for each of the three pricing strategies
- Section 7: The "Recommended strategy" paragraph
- Section 8: Each 2-3 sentence Special Considerations impact note
- Section 9: The professional but warm closing sentence

**What does NOT get humanized:**
- All comp tables, stat boxes, and numerical data (sold prices, $/sqft, DOM, list-to-sale ratios, percentages)
- Section headers and labels ("PRICING STRATEGY ANALYSIS", "RECOMMENDED LIST PRICE", etc. — locked brand structure)
- Property template fields (address, beds, baths, sqft, etc.)
- The DRE# 01466876, brokerage name, contact info, and legal disclaimer (exact required text)
- Chart legends and axis labels
- Cover/Hero section text (locked brand layout)

**Voice calibration:** Graeham's CMA voice is honest, direct, data-backed, human — not corporate, not stiff. No dashes as punctuation, no hedging ("it appears"), no cliches ("priced to sell"). The humanizer pass should preserve every specific number and citation in the narrative while removing AI tells (em-dash overuse, "stands as a testament," rule-of-three, "compelling opportunity," significance inflation around comps, etc.).

**How to invoke:**
1. Generate the full report draft with all sections per the structure above.
2. Complete the data verification pass (steps 1-6).
3. Separate the narrative prose from the data, tables, and charts.
4. Pass the narrative to the humanizer skill with the voice note: "Graeham Watts CMA narrative — honest, direct, data-backed, human, no hedging, no cliches, preserve all specific numbers and comp citations exactly."
5. Replace the original narrative with the humanized version.
6. Verify no specific numbers, comp addresses, or pricing ranges were altered.
7. Re-stitch the humanized narrative back into the HTML template.
8. Run the brand-integrity check (DRE blocklist).
9. Push to GitHub Pages via Composio.

**Failure mode this prevents:** CMA narrative that triggers the seller's "this is ChatGPT" reaction during the listing presentation. The data can be perfect; if the prose around the data sounds AI-generated, the seller stops trusting the pricing recommendation.

### Common Pitfalls

- **City boundary violations**: The #1 most common error. A comp 0.3 miles away in a different city can have wildly different market dynamics. Always verify city boundaries, especially in the EPA/Menlo Park/Palo Alto border areas.
- **Confusing list price with sold price**: Easy to mix up in MLS data. The report should clearly show both, and all pricing analysis should be based on SOLD prices, not list prices.
- **$/sqft outliers**: One comp with a much higher or lower $/sqft can
