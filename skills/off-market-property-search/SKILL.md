---
name: off-market-property-search
description: "Off-Market Property Search & Branded Report Generator for Graeham Watts. Use this skill ANY time the user mentions: off-market properties, members only listings, MLS members only, pocket listings, off-market search, exclusive listings, agent-only listings, properties not on Zillow, hidden listings, off-market report, find me off-market, pull off-market, off-market in [city], MLS Members Only, run the off-market search, what's off market in [city], properties not syndicated, or anything related to finding and presenting MLS Members-Only properties as a branded report. This skill logs into MLSListings.com via the already-authenticated browser, filters for Members Only listings (red-circled M or green M indicators), extracts property details and photos, and produces a premium branded HTML report (and optional PDF) in Graeham's black-and-gold visual style that looks like the agent's own research — NOT an MLS printout. No MLS numbers, no MLS branding, prices shown as 'Estimated price around $X'."
---

# Off-Market Property Search — Graeham Watts | Intero Real Estate

This skill finds **Members Only (off-market)** listings on MLSListings.com — properties that are listed through the MLS but withheld from public syndication (Zillow, Redfin, Realtor.com). It then produces a premium branded HTML report that presents these properties as if they came from Graeham's own research network, **not** as an MLS printout.

**Why this exists:** Members Only listings are one of the most valuable things a buyer's agent can offer — properties the client literally cannot find on Zillow. This skill lets Graeham deliver that list in a polished, on-brand format that reinforces his value to the client.

**Before generating a report, read these reference files:**
- `../website-builder/references/realtor-brand-kit.md` — **canonical brand reference** (palette, logo, voice, contact footer)
- `references/branding.md` — HTML-report-specific overrides (Google Fonts stack, card shadow, price-framing language)
- `references/mls_navigation.md` — How to drive MLSListings.com, identify the Members Only indicators, and extract fields
- `references/html_template.md` — Structure of the final HTML report

---

## Workflow

1. **Collect search parameters** from the user (see "Input" below)
2. **Navigate to MLSListings.com** via Claude in Chrome (user should already be logged in; if not, tell them to log in first — do NOT attempt to handle credentials)
3. **Run the search** for the target city with any filters the user specified
4. **Filter results to Members Only listings only** — these are marked with the red/outlined M or green M icons on each listing card in the results grid (see `references/mls_navigation.md` for exact visual indicators)
5. **For each Members Only property, extract:**
   - Front / primary photo URL (required)
   - 1–2 additional photo URLs if easily available (optional)
   - Full street address
   - Beds, baths, square footage, lot size, year built
   - List price (for internal use only — the report shows an "estimated price around" value, not the MLS number)
6. **Generate the branded HTML report** using `assets/report_template.html` and the card pattern in `references/html_template.md`
7. **Save to outputs** and share a `computer://` link with the user
8. **Offer to generate a PDF version** using WeasyPrint (preferred) or xhtml2pdf fallback

---

## Input — What to Ask the User

Always ask for these (city is required, the rest are optional filters):

```
REQUIRED
- City (e.g., "Menlo Park, CA")

OPTIONAL FILTERS
- Beds (min, or exact)
- Baths (min, or exact)
- Min square footage
- Max square footage
- Min lot size (in sqft or acres)
- Max lot size
- Min price
- Max price
- Property type (SFR, condo, townhome, multi-family) — defaults to SFR if not specified
```

If the user hasn't given a city, ask for it before doing anything else. If they gave a city and nothing else, **proceed** — don't pester them for every filter.

---

## Running the MLSListings Search

**Assume the user is already logged in.** Cowork has access to the user's authenticated Chrome session via the `mcp__Claude_in_Chrome__*` tools. Do not attempt to handle a username/password.

### Step-by-step browser flow

1. `mcp__Claude_in_Chrome__navigate` → `https://pro.mlslistings.com/` (or `https://mlslistings.com/` and follow the login link if needed)
2. Confirm the user is logged in (dashboard visible). If a login page appears, stop and tell the user: *"Looks like you're not logged in to MLSListings.com. Please log in in your browser, then tell me to continue."*
3. Go to the search / map search tool
4. Enter the city name and apply any filters provided by the user
5. Run the search and load the results grid/list
6. Before extracting, **filter or sort results to Members Only only**. The platform has a filter toggle for "Members Only" status. If that toggle isn't available, filter visually by the Members Only icon on each card (see next section).

See `references/mls_navigation.md` for UI-specific tips if the layout has changed.

---

## Identifying Members Only Listings

Members Only listings are visually marked in MLSListings.com with one of two small badges in the corner of the listing card:

- A **red / dark-outlined "M"** (sometimes shown as a red-circled M)
- A **green "M"** icon

Both indicate the listing is NOT syndicated to public sites like Zillow / Redfin / Realtor.com and is visible only to MLS members. **Either variant counts as Members Only** — include both in the report.

If the platform exposes a status field like `Members Only`, `MBR`, or `Private Listing Network` in the property detail view, use that as a secondary confirmation.

**Do not include** listings that are clearly public (no M badge, standard "Active" status). The whole point of the report is properties the buyer cannot find on Zillow.

---

## Extracting Property Data

For each Members Only listing, collect:

| Field | Notes |
|------|-------|
| Front photo URL | The primary / cover photo. Required. |
| Additional photos (1–2) | Optional. Only grab if easily available in the card or detail view. |
| Street address | Full address (e.g., "123 Main St, Menlo Park, CA 94025") |
| Beds | Integer |
| Baths | Decimal allowed (e.g., 2.5) |
| Square footage | Integer, show as "1,850 sqft" |
| Lot size | Show as "6,250 sqft lot" or "0.25 acre lot" depending on how MLS displays it |
| Year built | Optional but preferred |
| List price | For INTERNAL reference only — used to generate the "estimated price around" figure |

### Price presentation rule

**Never** display the raw MLS list price in the report. Show it as:

> "Estimated price around $X"

where `X` is the list price rounded to a reasonable marketing number:
- Under $2M → round to nearest $25,000
- $2M–$5M → round to nearest $50,000
- Over $5M → round to nearest $100,000

Examples: $1,485,000 → "Estimated price around $1,475,000". $3,172,000 → "Estimated price around $3,150,000". $7,950,000 → "Estimated price around $8,000,000".

This framing makes it look like our own research estimate rather than an MLS print, which (a) keeps compliance cleaner and (b) reinforces the "we did the digging for you" brand story.

### Photo handling

Download each photo URL locally (or reference the MLSListings CDN URL directly in the HTML if the image hotlinks resolve in a browser). If the image is behind an auth wall and won't render outside MLSListings, download to `outputs/off-market-<city>-<date>/images/` and reference by relative path.

---

## Generating the Report

Produce a single self-contained HTML file named:

```
Off_Market_<City_Underscored>_<DD-MM-YYYY>.html
```

Example: `Off_Market_Menlo_Park_16-04-2026.html`

Use `assets/report_template.html` as the base. Follow `references/html_template.md` for the card layout and structural rules.

### Non-negotiable design rules

- **Colors:** Black `#1A1A1A` backgrounds (header, footer, section bars), gold `#C5A55A` accents (lines, card borders, highlights), white `#FFFFFF` text on dark, dark body text `#1A1A1A` on white
- **Fonts (via Google Fonts CDN):** `Montserrat` (700 / 600) for headers and callouts; `Inter` (400 / 500) for body
- **Header:** "GRAEHAM WATTS" in gold ALL-CAPS Montserrat, "R E A L T O R" below in spaced letters, then "OFF-MARKET PROPERTIES — [CITY NAME]" and the date
- **Intro paragraph** (always include, verbatim or a near-variant):

  > "As part of our ongoing market research, we've identified the following properties that are not yet available to the general public. These off-market opportunities are exclusively available through agent networks."

- **Property cards:**
  - Large front photo at top (16:10 or 4:3 aspect)
  - Address in Montserrat Bold
  - Stat row: Beds • Baths • SqFt • Lot • Year Built (separated by gold dots or thin gold pipes)
  - "Estimated price around $X" in gold, larger font
  - Optional 1–2 thumbnail photos below the main one
  - Card: white background, subtle drop shadow, thin gold top or left border accent
- **Footer on every visual "page" of the report:**

  > Graeham Watts | Intero Real Estate | DRE #01466876 | 650-308-4727 | graehamwatts@gmail.com | www.graehamwatts.com

- **No MLS branding anywhere.** No MLS numbers, no "Courtesy of..." disclaimers, no MLS logos, no agent-remarks language. This is Graeham's research, not an MLS printout.
- **Generous white space.** Don't cram. Cards get breathing room.

### Empty-result handling

If the search returns zero Members Only listings in that city, still generate the report with the header, the intro paragraph, and a single centered card-style block that says:

> "No off-market properties matched your criteria in [City] as of [date]. I'll keep watching the network — off-market inventory moves fast, and I'll reach out as soon as something fits."

Don't just bail silently; the user may want to send this to a client to show they're looking.

---

## PDF Generation (Optional)

After the HTML is done, offer the user a PDF. If they say yes:

```bash
pip install weasyprint --break-system-packages
```

Then render:

```python
from weasyprint import HTML
HTML('/path/to/Off_Market_<City>_<date>.html').write_pdf('/path/to/Off_Market_<City>_<date>.pdf')
```

Fallback if WeasyPrint fails (it sometimes has system-library issues): `pip install xhtml2pdf --break-system-packages` and use `xhtml2pdf.pisa.CreatePDF`.

---

## Output

Save all files to the outputs folder under a subfolder per run:

```
outputs/
  off-market-<city-slug>-<DD-MM-YYYY>/
    Off_Market_<City>_<date>.html
    Off_Market_<City>_<date>.pdf    (if requested)
    images/                          (if photos were downloaded)
      1_main.jpg
      1_alt.jpg
      2_main.jpg
      ...
```

Then share `computer://` links to both the HTML and (if generated) the PDF. Don't write a long postamble — the user can open and read the report themselves.

---

## Edge Cases & Honest Limitations

- **Not logged in.** If the browser session isn't authenticated to MLSListings, stop and tell the user. Don't try to handle credentials.
- **UI changes.** MLSListings.com revamps its UI periodically. If the search flow or the Members Only filter has moved, fall back to finding listings that visually show the M icon in results. If the UI is unrecognizable, tell the user what's happening and ask them to walk through one search with you so the skill can be updated.
- **No Members Only listings available.** See "Empty-result handling" above.
- **Photos won't load.** If the CDN blocks hotlinking, download the images locally and reference them from a sibling `images/` folder. Don't ship a broken-image report.
- **Compliance.** Never include MLS numbers, "Listing courtesy of..." text, or agent-remarks fields that are MLS-restricted. The report must look like it came from Graeham's own research, not an MLS export.

---

## Triggers — When to Use This Skill

Use this skill whenever the user says any of:
- "What's off market in [city]"
- "Run the off-market search"
- "Find me off-market in [city]"
- "Pull Members Only in [city]"
- "Off-market report for [client]"
- "Show me pocket listings in [city]"
- "Agent-only listings in [city]"
- "Properties not on Zillow in [city]"
- Any mention of "Members Only", "MLS Members Only", "pocket listing", "off-market", "exclusive listing", "hidden listing" paired with a city or buyer context

If it's a simple informational question ("what IS a pocket listing?"), just answer normally — don't invoke the browser flow.
