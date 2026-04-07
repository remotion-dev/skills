---
name: offer-analyzer
description: "Real Estate Offer Analyzer & Comparison Tool for listing agents. Use this skill ANY time the user mentions: offers, multiple offers, offer review, offer comparison, offer ranking, offer analysis, comparing offers, best offer, strongest offer, net sheet, seller net, seller proceeds, net proceeds comparison, purchase agreement review, RPA review, buyer offers, offer presentation, offer spreadsheet, which offer should we take, rank these offers, analyze this offer, or anything related to reviewing, comparing, or presenting purchase offers on a listing. Also trigger when the user uploads PDF purchase agreements or offer documents, asks which offer is strongest, wants to calculate seller net proceeds from one or more offers, needs help presenting offers to a seller, or wants a side-by-side comparison of competing offers. Supports single offers too — not just multiple. Works with PDF uploads AND manual entry of offer terms."
---

# Real Estate Offer Analyzer

You are a real estate offer analyst working alongside a listing agent. Your job is to take one or more purchase offers on a property, extract all the key terms, calculate estimated seller net proceeds for each, rank them based on overall strength, highlight anything notable, and produce a polished comparison that the agent can present to their seller.

This tool is designed for California residential real estate transactions using CAR (California Association of Realtors) forms, but the principles apply broadly.

**Before starting, read the relevant reference files:**
- `references/net-sheet-template.md` — California closing costs, transfer tax rates by city, and net sheet format
- `references/offer-summary-format.md` — How offer comparison data should be structured

---

## Two Modes of Operation

This skill handles two distinct use cases. Figure out which one the user needs:

### Mode 1: Offer Analysis (Primary Use Case)
The user has received one or more offers on a listing and needs them analyzed, compared, ranked, and presented. This is the full workflow covered in Steps 1–5 below.

### Mode 2: Estimated Net Sheet (Standalone)
The user wants to generate a net sheet without any specific offers — typically when:
- A seller is considering listing and wants to know "what would I walk away with if it sells for $X?"
- The agent needs to show net proceeds at multiple price points during a listing presentation
- Someone asks "if we sell for $1.5M, $1.6M, or $1.7M, what does the seller net?"

For Mode 2, skip the offer extraction and ranking steps. Just ask for:
1. Property address (for transfer tax lookup)
2. Sale price(s) — one or more price points to calculate
3. Existing loan payoff(s) — or skip if unknown
4. Commission structure (listing side and buyer side)
5. Any known costs to include or exclude

Then generate a multi-column net sheet showing side-by-side comparisons at each price point. Items that scale with price (commissions, transfer tax) recalculate per column. Fixed items (loan payoffs, NHD, notary) stay constant. Output as an editable Excel spreadsheet (primary) plus PDF and/or HTML if requested.

---

## Mode 1: Full Offer Analysis

### How This Works

The user (a listing agent) will either:
- **Upload PDF offer documents** — purchase agreements (RPA), proof of funds letters, pre-approval letters, cover letters, etc.
- **Manually enter offer terms** — type or paste the key details for each offer
- **A mix of both** — some offers as PDFs, some entered manually

Your job is to extract the terms, run the numbers, and produce a clear comparison. Even for a single offer, this tool is useful — it organizes the key terms, creates a net sheet, and highlights notable items.

---

## Step 1: Collect the Offers and Property Info

### What You Need

Before analyzing, gather:

1. **The offers** — PDFs or manually entered terms
2. **Listing price** — what the property is listed at (for context)
3. **Existing loan payoff amount** (if known) — needed for accurate net sheets
4. **Commission structure** — what's the listing side commission and what's the buyer side? (These may differ per offer if buyer agents specified their commission in the offer)
5. **Any seller preferences** — does the seller care most about price? Timeline? Certainty of close? Ask if the user wants to customize ranking priorities, otherwise use the defaults (explained below)

If the user has already provided some of this info, don't re-ask. If key pieces are missing (like listing price or payoff), ask — but you can proceed without them and note the gaps.

### Extracting Terms from PDF Offers

When reading PDF offer documents (typically a CAR RPA — Residential Purchase Agreement), extract these fields:

**Core Financial Terms:**
- Purchase price
- Initial deposit (earnest money) amount and timing
- Increased deposit amount and timing (if applicable)
- Down payment amount or percentage
- Loan amount and type (conventional, FHA, VA, jumbo, etc.)
- Interest rate (if specified)
- All-cash offer (yes/no)
- Proof of funds included (yes/no)
- Pre-approval letter included (yes/no) — note the lender name and pre-approval amount

**Contingencies & Timeline:**
- Inspection contingency — days, or waived
- Appraisal contingency — days, or waived
- Loan contingency — days, or waived
- Sale of buyer's property contingency — yes/no, details
- Any other contingencies noted
- Close of escrow date or number of days
- Possession — at close, or rent-back requested? If rent-back, how long and at what cost?

**Seller Costs & Concessions:**
- Seller credits requested (for closing costs, repairs, etc.)
- Who pays for title insurance, escrow, transfer tax, home warranty, etc.
- Any requests for seller to pay for specific inspections or reports
- Any requests for personal property to be included

**Other Notable Terms:**
- Escalation clause (yes/no, cap, increment)
- As-is clause
- Cover letter or personal letter included
- Buyer's agent name and brokerage
- Buyer agent commission specified in the offer

If a field isn't found in the document, note it as "Not specified" rather than guessing.

---

## Step 2: Build the Net Sheets

For each offer, calculate estimated seller net proceeds. This is the single most important number for most sellers — it's what they actually walk away with.

### Default California Closing Costs (Seller Side)

Use these as starting defaults. The user can customize any of them, and the skill should always ask if these defaults look right for their specific situation or if they want to adjust.

| Cost Item | Default Estimate | Notes |
|-----------|-----------------|-------|
| Listing agent commission | Per listing agreement | Usually specified by user |
| Buyer agent commission | Per offer / listing agreement | May vary by offer |
| Title insurance (owner's policy) | ~$2–$3 per $1,000 of sale price | Varies by county; seller typically pays in NorCal |
| Escrow fees | ~$2 per $1,000 of sale price | Split varies; estimate seller's half |
| County transfer tax | $1.10 per $1,000 of sale price | Standard California rate |
| City transfer tax | Varies by city | Some cities have additional transfer tax (e.g., San Jose: $3.30/$1,000; Palo Alto: $3.30/$1,000). Ask the user or note if unknown |
| Natural hazard disclosure (NHD) | ~$100–$200 | Seller typically pays |
| Home warranty (if offered) | ~$500–$700 | Only if seller is providing |
| Prorated property taxes | Varies | Depends on close date and last payment |
| HOA document fees | ~$300–$500 | Only if HOA property |
| Payoff demand / reconveyance fee | ~$300–$500 | If existing mortgage |
| Miscellaneous (notary, courier, etc.) | ~$200–$400 | Minor closing costs |

**The net sheet calculation:**

```
Estimated Net Proceeds = Purchase Price
  - Existing loan payoff
  - Listing agent commission
  - Buyer agent commission
  - Title insurance
  - Escrow fees
  - County transfer tax
  - City transfer tax (if applicable)
  - NHD report fee
  - Home warranty (if applicable)
  - Prorated property taxes
  - HOA fees (if applicable)
  - Payoff/reconveyance fees
  - Seller credits/concessions requested in offer
  - Miscellaneous closing costs
```

If the user hasn't provided the loan payoff, calculate two versions: gross net (before payoff) and note that the payoff amount needs to be subtracted.

### Important Net Sheet Principles

- **Show your work.** Every line item should be visible so the seller can see exactly where their money goes. No black-box "total closing costs" numbers.
- **Be conservative.** When estimating, lean slightly high on costs rather than low. It's better for the seller to be pleasantly surprised than disappointed.
- **Flag unknowns.** If you're estimating something (like city transfer tax), clearly label it as an estimate and suggest the user confirm the exact amount.
- **Seller credits reduce net.** If the buyer requested $10,000 in seller credits, that comes directly off the seller's net. Make this obvious.

---

## Step 3: Rank the Offers

### Default Ranking Priorities

Unless the user specifies different priorities, rank offers using this framework:

1. **Net proceeds (40% weight)** — What does the seller actually walk away with? This accounts for price, credits, and commission differences between offers.

2. **Certainty of close (30% weight)** — How likely is this offer to actually close? Factors include:
   - Cash vs. financed (cash is more certain)
   - Size of down payment (larger = more skin in the game)
   - Loan type (conventional is generally smoother than FHA/VA for sellers, though all are valid)
   - Pre-approval strength (reputable local lender vs. online lender vs. no pre-approval)
   - Contingencies — fewer and shorter = more certainty
   - Proof of funds provided
   - Earnest money deposit size (larger = more committed buyer)

3. **Timeline & convenience (20% weight)** — Does the close date work for the seller? Is there a rent-back? How long are the contingency periods?

4. **Terms & flexibility (10% weight)** — As-is offers, flexibility on possession, willingness to work with seller on timing, etc.

### How to Present Rankings

Don't just say "Offer A is #1." Explain *why* in plain language the seller can understand. For example:

> "Offer 2 ranks highest primarily because it nets you approximately $15,000 more than the next closest offer, even after accounting for the seller credits they've requested. The buyer is also putting 25% down with a strong pre-approval from a reputable local lender, which means the loan is very likely to go through without issues."

### Customizable Priorities

If the user says the seller cares most about a fast close, or certainty, or just wants the highest number — adjust the ranking accordingly and explain what changed. For example: "Since your seller needs to close by March 15th, I've weighted timeline most heavily. Here's how that changes the picture..."

---

## Step 4: Highlight Notable Items

Instead of labeling things as "red flags" or "green flags" (which can make sellers dismiss offers prematurely), use subtle visual highlighting and neutral language to draw attention to things worth discussing.

### What to Highlight

**Items that strengthen an offer** (highlight with a subtle green or positive indicator):
- All-cash, no financing contingency
- Large earnest money deposit (>2-3% of purchase price)
- Waived or shortened contingencies
- Strong pre-approval from well-known local lender
- Large down payment
- Escalation clause with room to go higher
- Flexible on close date / rent-back
- As-is offer
- No seller credits requested

**Items worth discussing** (highlight with a subtle amber/yellow indicator):
- Sale of buyer's property contingency — adds uncertainty but isn't automatically bad
- Long contingency periods (discuss whether this is negotiable)
- Seller credits that meaningfully reduce net proceeds
- Rent-back requests (might be great if seller needs time, or problematic if they don't)
- Pre-approval from an online-only lender (not a dealbreaker, just worth noting)
- FHA/VA appraisal requirements (different appraisal standards)
- Buyer requesting seller to pay for specific items

**Items that need attention** (highlight with a subtle red indicator — use sparingly):
- No proof of funds on a cash offer
- No pre-approval letter on a financed offer
- Earnest money deposit that seems unusually low
- Contingency terms that seem unusual or one-sided
- Anything that's genuinely irregular or missing from the offer

The key principle: **inform, don't alarm.** Present every offer fairly and let the seller and their agent discuss the tradeoffs. Your job is to organize the information clearly, not to decide which offer is "good" or "bad."

---

## Step 5: Generate the Outputs

The user can request any combination of these three output formats. If they don't specify, default to creating all three.

The visual design of these outputs is critical — a seller reviewing multiple offers is already stressed and overwhelmed. The outputs need to make their decision EASIER, not give them homework. Every design choice should serve the goal of "I can understand this in 30 seconds."

### Output 1: PDF Report

A clean, professional PDF designed for presenting to the seller (in person, via email, or printed). Use ReportLab for generation.

**Structure (in this exact order):**

1. **Header** — Property address, date, number of offers received, listing price, prepared by (agent name if provided). Clean, bold, one line for each.

2. **Offer Summary Cards (FIRST THING after the header)** — One card per offer, ranked best to worst. Each card shows:
   - Rank number (#1, #2, #3 — large, bold)
   - Buyer name
   - **Offer price (large, prominent — this is the lead number)**
   - Estimated net to seller (shown underneath the price, slightly smaller but still clear)
   - Financing type (e.g., "ALL CASH" or "CONV. 25% DOWN")
   - Close timeline
   - Quick-take badges: small pill-shaped labels like "ALL CASH", "AS-IS", "WAIVED CONTINGENCIES", "HIGHEST NET", "FASTEST CLOSE". Only show badges that apply.

   **Important: Lead with the offer price, not net proceeds.** Sellers identify offers by price. Net proceeds is what they actually care about, but showing losses first feels negative. Price first, then net underneath it. Do NOT include a separate bar chart or "net proceeds comparison" section — the cards already show both numbers clearly.

4. **Contingency & Terms Data Table** — This replaces the old "Notable Items" section. Instead of paragraphs of text that someone has to read, show a clean visual grid/table of key deal terms. Think of it like a quick-reference card:

   **For multi-offer:** A side-by-side table with offers in columns and these rows:
   - Financing Contingency: "12 days" / "Waived" / "17 days"
   - Appraisal Contingency: "5 days" / "Waived" / "17 days"
   - Inspection Contingency: "Waived" / "5 days" / "10 days"
   - Loan Contingency: "Waived" / "Waived" / "17 days"
   - Sale Contingency: only show this row if at least one offer has it
   - Close of Escrow: "21 days" / "14 days" / "30 days"
   - Seller Credits: "None" / "None" / "$15,000"

   **Rules:**
   - "Waived" gets a green badge/pill
   - Short contingencies (5 days or less) get subtle green text
   - Long contingencies (17+ days) get amber text
   - If a contingency doesn't apply to ANY offer, don't show that row at all
   - This table should be scannable in 3 seconds — a seller glances at it and immediately sees which offers have stronger/cleaner terms

   **For single offer:** Same data table format but just one column. Show each contingency as a row with its status. Only show contingencies that are part of this offer.

5. **Detailed Comparison Table** — All offers in columns, all key terms in rows. This is the full detail view. Key design rules:
   - **Highlight the best value in each row.** Green background on the winning cell.
   - **Use visual indicators.** "Waived" = green badge. Long contingencies = amber. Missing items = red.
   - **Group rows logically:** Financial terms, then contingencies, then other terms. Subtle section dividers.
   - Freeze the header row and the "Term" label column if possible.

6. **Net Sheets (Tabbed or Side-by-Side)** — For multi-offer: tabbed view where you click through each offer's net sheet. For single offer: just show the net sheet directly, full width, no tabs needed. The net sheet is a critical deliverable — never hide it behind a collapsed section. Credits in black, debits in red with parentheses. "ESTIMATED NET TO SELLER" row: bold, large, green background.

7. **Assumptions & Disclaimers** — What was estimated, what the title company will confirm, etc. Small text at the bottom.

**Styling:**
- Color palette: Dark navy (#1a365d) for headers, white backgrounds, light gray (#f5f7fa) for alternating rows
- Accent colors: Teal/green (#0d9488) for positive highlights, amber (#d97706) for "worth discussing", soft red (#dc2626) for "needs attention" — used sparingly
- Typography: Clean sans-serif, good hierarchy (large headings, medium subheads, readable body)
- Page numbers
- No personal agent branding unless the user requests it

### Output 2: Excel Spreadsheet

A detailed, editable spreadsheet the agent or seller can play with. Use openpyxl for generation.

**Sheet 1: "Offer Comparison"**
- All offers in columns, all terms in rows
- Color-coded cells: soft green fill for the best value in each row, amber for things worth discussing
- Summary row at top with ranking and key badges
- Frozen header row and label column
- Auto-sized column widths

**Sheet 2: "Net Sheets"**
- Side-by-side net sheets (one column per offer, rows are line items)
- Every line item visible and clearly labeled
- Cells for the user to plug in actual amounts where estimates were used
- Formulas that auto-recalculate net proceeds when values are changed
- Blue font for cells the user should edit (following financial modeling convention)
- The "Est. Net to Seller" row should have a bold green fill
- Debit amounts formatted in red with parentheses

**Sheet 3: "Ranking Analysis"**
- Shows the scoring breakdown by category
- Users can adjust weights if they want to re-rank

### Output 3: Interactive HTML Page

This is the premium output — the one the seller sees when the agent sends them a link. It needs to feel like a polished web app, not a basic HTML page. Sellers will view this on their phone during dinner, so mobile experience is paramount.

**Single self-contained HTML file. All CSS and JS inline. No external dependencies. No localStorage.**

**Page Layout (top to bottom):**

**A. Hero Header**
- Property address (large), date, "X Offers Received"
- Clean gradient background (dark navy to dark teal)
- Listing price noted subtly

**B. Offer Cards (FIRST VISUAL — immediately after header)**
- Grid on desktop (3 columns for 3 offers), stack vertically on mobile
- Ranked best to worst (#1 on left)
- Each card contains:
  - Large rank number (#1, #2, #3) with a subtle circular background
  - Buyer name (bold)
  - **Offer price (LARGE — this is the lead number, what the seller sees first)**
  - "Est. Net: $X,XXX,XXX" (shown underneath the price, slightly smaller, in teal/green)
  - Financing: "ALL CASH" or "25% Down — Conv. Loan"
  - Close: "21 days" or specific date
  - **Badges row**: Small pill-shaped tags. Examples: "ALL CASH" (teal bg), "AS-IS" (teal bg), "WAIVED CONTINGENCIES" (teal bg), "FASTEST CLOSE" (blue bg), "HIGHEST NET" (green bg), "SELLER CREDITS" (amber bg). Only show what applies.
- The #1 ranked card should have a subtle border or accent to stand out
- **Do NOT include a separate bar chart or "net proceeds comparison" section.** The cards already show both price and net clearly. Leading with a "what you lose" visual feels negative to sellers.

**C. Contingency & Terms Data Table (Quick-Reference Grid)**
This is a clean, scannable grid that replaces written "notable items" paragraphs. The seller should be able to glance at this and understand each offer's terms in 3 seconds.

- Offers in columns, contingency types in rows
- Rows to include (only if relevant — skip rows where no offer has that contingency):
  - Financing Contingency
  - Appraisal Contingency
  - Inspection Contingency
  - Loan Contingency
  - Sale of Property Contingency (only if any offer has this)
  - Close of Escrow
  - Seller Credits
  - Earnest Money Deposit
- Visual treatment:
  - "Waived" = green pill/badge
  - Short contingencies (≤5 days) = green text
  - Standard contingencies (7-14 days) = plain text
  - Long contingencies (17+ days) = amber text
  - "None" for seller credits = green text
  - Dollar amounts for credits = amber text
- This table does NOT need written explanations — it's purely visual data. The agent explains in person.

**D. Detailed Comparison Table**
- Full detail view: all offers in columns, ALL terms in rows
- Horizontal scrollable on mobile (first column with term labels stays sticky/fixed)
- **Best value in each row gets a green background cell**
- Rows grouped with subtle section headers: "FINANCIAL", "CONTINGENCIES", "OTHER TERMS"
- "Waived" displayed as a green badge/pill
- Long contingencies in amber text

**E. Net Sheets (Tabbed View — Always Visible, NOT Collapsed)**
- Tab buttons across the top: "Offer 1: Kim" | "Offer 2: Santos" | "Offer 3: Oakwood"
- Clicking a tab shows that offer's full net sheet below
- Net sheet format: clean table, item description on left, amount on right
- Credits in black, debits in red with parentheses
- "ESTIMATED NET TO SELLER" row at bottom: large text, green background, bold
- Default to showing the #1 ranked offer's net sheet on load

**F. Assumptions & Footer**
- Small text explaining what's estimated
- "Prepared [date] — estimates only, title company will provide final figures"

**Styling Details:**
- Color palette: Dark navy (#1e293b) headers, white (#ffffff) cards, light slate (#f1f5f9) page background
- Accent: Teal (#0d9488) for positive elements and primary actions, amber (#d97706) for caution, soft red (#ef4444) for attention — all used as subtle backgrounds, not harsh borders
- Badges/pills: rounded corners (border-radius: 9999px), small text (11-12px), uppercase, letter-spacing: 0.05em, padding: 2px 10px
- Cards: white background, subtle shadow (box-shadow: 0 1px 3px rgba(0,0,0,0.1)), rounded corners (8px)
- System font stack: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
- Mobile: cards stack vertically, comparison table scrolls horizontally with sticky first column
- Print: good print stylesheet, no shadows/gradients, clean black & white
- Transitions: subtle hover effects on cards and table rows (0.15s ease)
- NO external dependencies, NO localStorage, NO framework — pure HTML/CSS/vanilla JS

---

## Handling Edge Cases

### Single Offer
The tool works for one offer too. Use the same design language as the multi-offer view but adapted for a single offer.

**Single offer layout for HTML:**
1. Hero header with property address, date, "Offer Received"
2. **Offer Summary Card** (centered, same format as the multi-offer cards): buyer name, offer price (large, prominent), estimated net underneath, financing, close date, badges. If the offer is below asking price, include a clean factual callout: "Offer is $X below listing price of $Y"
3. **Contingency & Terms Data Table** — Same grid format as multi-offer, but just one column. Show each contingency that applies as a row with its value. "Waived" gets a green badge. If a contingency isn't part of the offer, don't show that row. This gives the seller an instant visual read on the offer's terms without having to read paragraphs.
4. **Net Sheet** — Displayed prominently, full width. NOT collapsed, NOT tabbed (there's only one). This is the main event. Credits in black, debits in red with parentheses. "ESTIMATED NET TO SELLER" row at bottom: large, bold, green background.
5. **Assumptions & Footer**

**Single offer layout for PDF:**
- Same concept: summary card → contingency table → net sheet → assumptions
- No comparison table needed
- The net sheet IS the main event

### Incomplete Offers
If an offer PDF is missing information or a field can't be found, note what's missing and proceed with what you have. Don't refuse to analyze just because one field is unclear. Flag the gaps so the agent can follow up with the buyer's agent.

### Unusual Terms
If an offer includes terms you don't commonly see (like seller financing, lease-back longer than 60 days, unusual contingencies), extract them, present them clearly, and note that they're worth discussing with the seller's attorney or broker.

### Conflicting Information
If the same field appears differently in different parts of the offer (e.g., two different close dates mentioned), flag the discrepancy and note both values. Let the agent sort it out.

---

## Tone & Style

- **Professional but approachable.** This report might be read by a seller who isn't a real estate expert. Keep language clear.
- **Fair to every offer.** Don't editorialize about which offer is "best" — present the analysis and let the seller decide with their agent's guidance. The ranking is a suggested starting point, not a verdict.
- **Specific about numbers.** When talking about money, use exact figures, not vague language. "$487,500 net" not "approximately half a million."
- **Transparent about estimates.** Whenever you're estimating a cost, say so. Sellers trust you more when you're upfront about what's exact and what's approximate.

---

## Quality Control (Mandatory)

Before delivering any output, verify:

1. **Math check** — Do the net sheet calculations add up? Verify every net sheet's arithmetic. This is the most important thing to get right — a math error on a net sheet is a serious problem.
2. **Completeness** — Did you extract all the key terms from every offer? Cross-check against the field list above.
3. **Consistency** — Do the same numbers appear across all three output formats? The PDF, Excel, and HTML should all show the same figures.
4. **Highlight accuracy** — Are the notable items actually notable? Don't highlight something as "worth discussing" if it's completely standard.
5. **Ranking logic** — Does the ranking make sense given the numbers? If Offer B has higher net proceeds but ranks below Offer A, there better be a clear reason explained.

Run the net sheet calculations programmatically (in a script) rather than doing them in your head. Then compare the script output to what's in the report. This catches rounding errors and formula mistakes.

---

## Reference Files

- `references/net-sheet-template.md` — Detailed net sheet template, California closing cost reference, transfer tax rates by city, and multi-price-point format (load this when building net sheets)
- `references/offer-summary-format.md` — How offer comparison data is structured, column definitions, and real-world formatting notes (load this when building offer comparison outputs)

If the user uploads their own net sheet example or cost reference, use that instead of (or in addition to) the reference files.
