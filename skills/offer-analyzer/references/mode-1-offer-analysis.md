# Mode 1: Full Offer Analysis — Detailed Steps

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

### Output 3: Interactive HTML Page (Email-Ready, Hosted on GitHub Pages)

This is the premium output — the one the seller sees when the agent sends them a link. It needs to feel like a polished web app, not a basic HTML page. Sellers will view this on their phone during dinner, so mobile experience is paramount.

**Single self-contained HTML file. All CSS and JS inline. No localStorage. Google Fonts (Inter) is the only external dependency allowed.**

**The output MUST match the Graeham Watts brand system used in CMA reports.** Read `references/email_branding.md` before generating this output — it contains the full brand specification (gold/black palette, CMA-style cover header, site nav bar, full-width layout, typography). Do not invent your own color palette or header design.

**Page Layout (top to bottom):**

**A. Site Nav Bar (sticky top — matches CMA reports)**
- Background: `#343955` (graehamwatts.com nav color)
- Height: 72px, padding: 0 32px, sticky at top
- Logo on the left: `https://images.leadconnectorhq.com/image/f_webp/q_80/r_1200/u_https://assets.cdn.filesafe.space/6wuU3haUH7uNeT20E3UZ/media/691256870b647e40e3c2e105.png` (height 44px), wrapped in `<a href="https://www.graehamwatts.com/">` opening in new tab
- Right side: nav links to Home, Buy, Sell, Buying in the Bay, The Bay Market, Blog, About, Contact (white text, 13px, 22px gap)
- On mobile (<880px): hide nav links, keep logo
- This nav bar is identical to what CMA reports use — sellers should immediately recognize it as Graeham's content

**B. Cover / Hero Header (CMA-style: black background, gold text)**
- Background: `#1A1A1A` (Primary Black), padding 56px 48px 48px, text-align center
- Bottom border: 4px solid `#C5A55A` (gold accent rule)
- "GRAEHAM WATTS" in 28px, font-weight 800, color `#C5A55A`, letter-spacing 0.18em — ALL CAPS
- "R E A L T O R" below in 11px, color `#C5A55A`, letter-spacing 0.4em
- Gold horizontal rule (80px wide × 2px, color `#C5A55A`)
- Report type tag: "OFFER COMPARISON" in 14px, color `#C5A55A`, letter-spacing 0.25em, font-weight 600
- Property address as h1: 38px, font-weight 700, white, line-height 1.15
- City/State/Zip subhead: 18px, light gray (`#cccccc`)
- Meta line: "X OFFERS RECEIVED · PREPARED [DATE] · LISTED AT $X,XXX,XXX" in 13px, gray with gold "X OFFERS RECEIVED" emphasis
- Bottom contact strip (separated by gold-tinted border): "INTERO REAL ESTATE SERVICES | DRE #01466876 | 650-308-4727" in 11px gold

**C. Full-Width Page Container**
- The cover and the content container BOTH go full browser width — there is NO 600px or 720px email-style centering. The email is meant to be opened in a browser as a hosted GitHub Pages link, not pasted into Gmail.
- Inner container: `max-width: 1320px`, centered horizontally, white background, padding 48px on desktop (32px 20px on mobile)
- Outer page background: `#FAFAFA` (light off-white) so the white container has subtle definition

**D. Section Headers (CMA-style: black bar with gold text)**
- Background: `#1A1A1A`, color `#C5A55A`, padding 14px 24px, font-size 13px, letter-spacing 0.2em, text-transform UPPERCASE, font-weight 700
- Left border accent: 4px solid `#C5A55A`
- Used for "The Offers, At a Glance", "Contingencies & Key Terms", "Estimated Net Sheets", "My Recommendation"

**E. Offer Cards (FIRST VISUAL — immediately after intro)**
- Grid on desktop (3 columns for 3 offers), stack vertically on mobile (<880px)
- Ranked best to worst (#1 on left)
- Each card contains:
  - Rank badge (`#1`, `#2`, `#3` — 36px circular, black bg with gold text; #1 inverts to gold bg with black text)
  - Buyer name (14px, bold, dark)
  - **Offer price (32px, font-weight 800, black, letter-spacing -0.02em — this is the lead number)**
  - "Est. Net to Seller: $X,XXX,XXX" underneath in 13px, color `#A88B3D` (dark gold), font-weight 600
  - Three meta lines (13px gray, separated by thin border): "Conv. 80% LTV · 20% down" / "Close: 30 days" / "Buyer's agent: [Name]"
  - **Badges row**: pill-shaped tags. Use brand-aligned variants ONLY:
    - `badge-gold` (gold bg #C5A55A, black text) for top positives ("HIGHEST NET", "ALL CASH", "WAIVED CONTINGENCIES")
    - `badge-cream` (cream bg #F5EFDC, black text, gold border) for secondary positives ("FASTEST CLOSE")
    - `badge-amber` (amber #FEF3C7 bg, brown text) for "worth discussing" items ("95% LTV", "ACTIVE LOAN CONT.")
    - `badge-gray` (light gray bg, gray text) for neutral items
- The #1 card gets a 2px gold border, gold drop shadow, and a "RECOMMENDED" gold tag pinned to the top-left corner
- **Do NOT include a separate bar chart or "net proceeds comparison" section.** The cards already show both price and net clearly.

**F. Contingency & Terms Data Table**
- Table: white background, 1px border `#E5E5E5`, rounded corners
- Header row: black (`#1A1A1A`) with gold (`#C5A55A`) text, 11px UPPERCASE, letter-spacing 0.1em
- Body rows: alternating white / `#FAFAFA`
- "Waived" gets a gold pill (`pill-gold`)
- Short contingencies (≤5 days) get a cream pill (`pill-cream`)
- Standard (7-14 days) plain text
- Long (17+ days) get an amber pill (`pill-amber`)
- "None" for seller credits = cream pill
- Dollar amounts for credits = amber pill

**G. Net Sheets (Side-by-Side Comparison Table — NOT Tabbed)**
- For multi-offer analyses: render ALL net sheets in a single side-by-side table where line items are rows and offers are columns. Do NOT use a tabbed view that requires the seller to click between offers — sellers want to compare line by line at a glance.
- Header row: "Line Item" on left, then one column per offer with buyer name + offer price + rank (e.g., `Krishnan / $1,125,000 · #1`)
- The #1 ranked offer column gets the gold treatment:
  - Header cell: gold (`#C5A55A`) background with black text
  - Body cells in that column: subtle cream tint (`#FFFBEF`) background on `.recommended-col`
  - Footer "ESTIMATED NET TO SELLER" cell: solid gold background with black text, 17px
- Other offer columns: standard alternating white / `#FAFAFA` rows, black footer with gold text
- "Debits" section divider row: cream background (`#F0EBD8`), black uppercase text, 2px gold top + 1px gold bottom borders
- Credits/positive values in black, debits in red (`#B91C1C`) with parentheses, zeros in gray (`#999999`)
- Final footer row "ESTIMATED NET TO SELLER" spans all columns: black bg + gold text by default; recommended column inverts to gold bg + black text
- Wrap the table in `<div class="net-sheet-wrapper">` with `overflow-x: auto` so it scrolls horizontally on mobile rather than getting truncated
- For single-offer analyses: render the net sheet as a normal vertical table (item label on left, amount on right) — no comparison table needed
- This format makes it trivial for the seller to scan: "I get $X with Krishnan, $Y with Ortega, $Z with Oakwood — and here's exactly which line items differ."

**H. Recommendation Box**
- Black background (`#1A1A1A`) with white text
- 6px gold left border
- Padding 32px 36px, border-radius 8px
- "RECOMMENDED: [BUYER] — $X,XXX,XXX" label in gold uppercase
- Body paragraphs in cream (`#F5EFDC`) text, 15px, line-height 1.7
- Bold key terms inside paragraphs use gold

**I. Footer**
- Black background, padding 36px 48px, text-align center
- "GRAEHAM WATTS" wordmark in gold, 14px, letter-spacing 0.15em
- Contact line: "Intero Real Estate Services | DRE #01466876 | 650-308-4727 | graehamwatts@gmail.com" in light gray (13px)
- Disclaimer (max-width 720px, centered): explains estimates, transfer tax basis, title company will provide final figures

**Styling Details (mandatory brand palette):**
- Primary Black: `#1A1A1A` — headers, section bars, footer, recommendation box
- Primary Gold: `#C5A55A` — accents, borders, top badges, rule lines, headline text on dark bg
- White: `#FFFFFF` — content backgrounds
- Light Gold / Cream: `#F5EFDC` — secondary backgrounds, alternating rows, secondary badge bg
- Dark Gold: `#A88B3D` — net-to-seller emphasis, secondary accent
- Light Gray: `#F0F0F0`, `#FAFAFA` — alternating rows, page background
- Amber (caution): `#FEF3C7` bg / `#92400E` text — used sparingly for "worth discussing"
- Soft Red (debits): `#B91C1C` — net sheet debit amounts only
- Typography: Inter from Google Fonts (`@import https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap`), system stack fallback
- Badges/pills: rounded corners (border-radius: 9999px), small text (10-11px), uppercase, letter-spacing 0.05em, padding 4px 10px
- Cards: white background, 1px border, rounded 8px, hover lift (transform: translateY(-2px))
- Mobile: cards stack vertically, comparison table scrolls horizontally with sticky first column, nav links hide
- Print: good print stylesheet, no shadows/gradients, clean black & gold
- Transitions: 0.15s ease on hover effects
- NO teal, NO navy, NO generic email-blue — those are NOT the Graeham Watts brand. If you find yourself using `#0d9488`, `#1e293b`, or `#1e3a5f`, stop and re-read `references/email_branding.md`.

**File Naming (REQUIRED for hosted URL):**
- Format: `Offer_[street_number]_[street_name_underscored].html`
- Strip special characters, replace spaces with underscores
- Examples: `Offer_828_Weeks_St.html`, `Offer_3712_Bayshore_Way.html`
- This naming matches the `CMA_*` convention so all listing assets live alongside each other in `Graehamwatts/online-content`

## Publishing via Composio (canonical pattern)

> **Read first:** [`shared-references/publishing-via-composio.md`](../shared-references/publishing-via-composio.md) — single source of truth for ALL skills.

After generating the offer-analysis HTML output, publish via Composio to `Graehamwatts/online-content` so the agent gets a permanent hosted URL.

**Account:** `github_spar-devata`  
**Owner:** `Graehamwatts`  
**Repo:** `online-content`  
**Branch:** `main`  
**Path pattern:** `offers/Offer_[address].html`  
**Hosted URL pattern:** `https://graehamwatts.github.io/online-content/offers/Offer_[address].html`

**Tool to use:** `GITHUB_COMMIT_MULTIPLE_FILES` (atomic commit, retry-safe).

```python
result, error = run_composio_tool(
    tool_slug='GITHUB_COMMIT_MULTIPLE_FILES',
    arguments={
        'owner': 'Graehamwatts',
        'repo': 'online-content',
        'branch': 'main',
        'message': 'descriptive commit message',
        'upserts': [{'path': 'offers/Offer_[address].html', 'content': html_content, 'encoding': 'utf-8'}]
    },
    account='github_spar-devata'
)
```

**HARD RULES:**
- Do NOT use the legacy GitHub Contents API with PAT or `javascript_tool` chunked uploads (replaced 2026-05-03).
- Do NOT use GitHub Desktop or `git push` from the agent sandbox.
- Run the brand-integrity check before push (see shared doc — blocks DRE# 01 leaks).
- After commit, give the user BOTH the hosted URL and the local `computer://` link.

See `shared-references/publishing-via-composio.md` for full details, common pitfalls, and verification flow.


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

