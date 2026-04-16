# MLSListings.com — Navigation Playbook

This file captures how to drive MLSListings.com through Claude in Chrome to extract Members Only listings. The UI changes occasionally; when in doubt, fall back to the visual-badge method at the bottom.

## Prerequisite

Graeham should already be logged in to MLSListings.com in his Chrome session. Do **not** attempt to handle credentials. If the browser lands on a login page, stop and tell the user to log in, then resume.

## Likely URLs

MLSListings.com routes Pro users through a few different domains depending on the search tool:

- `https://pro.mlslistings.com/` — Pro portal dashboard (most common entry)
- `https://pro.mlslistings.com/search` or `/homes` — main search tool
- `https://mlslistings.com/` — public portal (not what we want for Members Only)

Navigate to `https://pro.mlslistings.com/` first; if it redirects to a login, the user isn't authenticated.

## Running a Search

1. Find the search bar (usually at the top of the Pro portal, or behind a "Search" / "New Search" nav item)
2. Enter the city name exactly as the user provided, e.g. `Menlo Park, CA`
3. Open the filters / refine panel
4. Apply user-provided filters:
   - Property type (default: Single Family Residential — "SFR" or "Residential")
   - Status: include `Active`, `Coming Soon` (both can be Members Only)
   - Beds / Baths / SqFt / Lot Size / Price — enter the user's min/max values
5. **Look for a "Members Only" status filter.** On the Pro portal this is usually under a "Listing Type" or "Status" filter group. It may be labeled:
   - `Members Only`
   - `Private Listing Network`
   - `MLN` (Members Listing Network)
   - `Off-Market` or `Pocket`

   Check that filter if available. This is the cleanest way to restrict results.

6. Submit the search and wait for results to render.

## Identifying Members Only Listings (Visual Badge Method)

If the filter isn't findable, fall back to visual badge detection on each listing card in the results grid.

Members Only listings are marked with one of these small badges in the upper corner of the listing card:

- A **red outlined "M"** — looks like a red-bordered square with an "M" inside (sometimes circled)
- A **green "M"** — a green-tinted "M" badge, slightly different style

**Both variants mean "Members Only" — include either.** Listings without any M badge are standard public listings and should be skipped.

Other signals that confirm Members Only in the detail page:
- A `Members Only` or `MBR` label in the status field
- Absence of public-facing syndication links (no "View on Zillow" buttons, etc.)
- A note in the listing description / internal remarks mentioning MLN / private listing network

Ignore listings marked `Sold`, `Closed`, `Withdrawn`, or `Expired` — we only want active off-market inventory.

## Extracting Data from a Listing Card / Detail Page

For each Members Only listing:

1. Click into the detail view (or hover the card if the summary shows enough detail)
2. Capture these fields — the labels may vary slightly:

| Target field | Likely MLS label(s) |
|--------------|---------------------|
| Address | "Address", "Street Address", top-of-page heading |
| Beds | "Bedrooms", "Beds", "BR" |
| Baths | "Bathrooms", "Baths", "BA" |
| SqFt | "Living Area", "SqFt", "Sq Ft", "Square Feet" |
| Lot size | "Lot Size", "Lot SqFt", "Lot Acres" |
| Year built | "Year Built", "Built" |
| List price | "List Price", "Current Price", "Price" |
| Photos | Main carousel — grab the first image as the hero, and optionally images 2 and 3 |

3. If the detail page has a map / street view, skip those — we only need the photos that look marketable.

## Tools to Use

Use Claude in Chrome's tool suite — the user's already logged in, so work with their existing session:

- `mcp__Claude_in_Chrome__navigate` — go to a URL
- `mcp__Claude_in_Chrome__read_page` — dump the rendered page text / structure
- `mcp__Claude_in_Chrome__find` — locate interactive elements
- `mcp__Claude_in_Chrome__form_input` — type into filter fields
- `mcp__Claude_in_Chrome__computer` — click, scroll, navigate the UI
- `mcp__Claude_in_Chrome__javascript_tool` — read DOM data directly if the structure is messy (useful for grabbing a whole card's data as JSON)
- `mcp__Claude_in_Chrome__read_network_requests` — inspect XHR traffic if the UI loads results via API (often faster than scraping the DOM)

The `read_network_requests` + `javascript_tool` combo is the most reliable approach: many MLS portals load results via JSON XHR calls you can inspect directly.

## If the UI has moved / broken

If you can't find the search or the Members Only filter:

1. Tell the user plainly what you're seeing
2. Ask them to walk you through one manual search so you can observe the current flow
3. Update this reference file with what you learned so next time works

Don't guess and don't fabricate results. A report with zero properties is better than a report with wrong data.

## Rate / Volume Etiquette

MLSListings.com is not rate-limited to human speed, but don't hammer it:
- Don't paginate through 50 result pages if the user only needs the first screen
- Don't open more than ~10 detail pages in parallel — walk through them sequentially
- If a request fails, back off before retrying
