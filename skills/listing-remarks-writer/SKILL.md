---
name: listing-remarks-writer
description: "MLS listing remarks writer optimized for AI-powered home search (ChatGPT with Zillow, Perplexity, Google AI Overviews) and Bay Area buyers. Walks the buyer through the property as if touring it, adapts framing to property condition (fixer / mid / move-in ready), and produces noun-dense AI-searchable copy. Use this skill ANY time the user asks to: write listing remarks, write MLS description, draft listing copy, write property remarks, write the public remarks for [address], rewrite a stale listing, optimize listing for AI search / ChatGPT / Zillow, write the public remarks section for a new listing, draft remarks for a fixer, draft remarks for a renovated home, or improve an existing listing description. Trigger when the user uploads listing photos and asks for the description, mentions a new listing, or pastes property details and asks for the listing description. Localized for Graeham's Bay Area markets (East Palo Alto, Redwood City, Palo Alto, Menlo Park, San Mateo County) with default California-specific framing."
---

# Listing Remarks Writer

Write MLS listing descriptions that surface in AI-powered home search. Buyers increasingly search through ChatGPT (with Zillow integration), Perplexity, Google AI Overviews, and similar — and these platforms can ONLY read the public remarks text. They cannot interpret photos, 3D tours, video tours, or captions. Every feature you don't name in the remarks is invisible to AI search.

This skill produces noun-dense, AI-searchable MLS copy. Walks the buyer through the property as if touring it, adapts framing to property condition, and stays inside Fair Housing / RESPA guardrails by design.

---

## Before You Start — Read These

1. **`../shared-references/identity.json`** — Graeham's brand identity. NEVER hardcode contact details, DRE, or brokerage from memory. Read this file first.
2. **`../content-creation-engine/references/market-config.md`** (optional) — full neighborhood list, jurisdiction terms, content pillars. Use when writing for one of Graeham's primary markets.

---

## Fair Housing + RESPA Guardrails (Non-Negotiable)

NEVER write remarks that:
- Reference race, religion, national origin, family status, disability, or sex
- Use coded language: "safe neighborhood," "good area," "family-friendly," "up-and-coming," "exclusive community," "great for families," "perfect for empty nesters"
- **Mention school quality, ratings, rankings, awards, or "improving" / "concerning" framing.** This is the most common Fair Housing trap in real estate marketing. School quality language has been treated by HUD as a demographic proxy. NAR Code of Ethics Article 10 prohibits it explicitly.
  - You MAY factually name the school district ("Property is in Ravenswood City School District") if it adds material clarity — but most agents skip this since the district shows in the MLS metadata anyway.
  - You MAY note distance to a specific school as a walkability fact ("within 0.4 miles of Costaño Elementary").
  - You may NOT call schools "top-rated," "blue ribbon," "award-winning," "highly rated," "improving," or use any quality assessment whatsoever — positive OR negative.
- Promote kickback arrangements with lenders, inspectors, title companies, or other vendors (RESPA violation)
- Imply preference for or steering toward specific buyers based on protected characteristics

When referencing neighborhoods or location: stick to property types, price tiers, lot sizes, proximity to amenities (parks, transit, dining, retail, employers), architectural styles, age of housing stock, HOA structure, and walkability/commute facts. This is both the law (Fair Housing Act, RESPA, NAR Code of Ethics) and Graeham's brand standard.

---

## Truth-in-Advertising Rules (Non-Negotiable)

These prevent claims that get agents into civil liability or DRE complaints, separate from Fair Housing.

**ADU language — only when verified.** NEVER write "ADU potential," "ADU-ready," "buildable lot," "can add a unit," "JADU possible," or any similar claim unless the agent has confirmed:
1. Local zoning permits an ADU on this lot type, AND
2. The lot meets minimum setback / size requirements for the jurisdiction, AND
3. There are no HOA / CC&R / easement restrictions that would block it

If any of those three are unverified, **omit ADU language entirely.** Cities in the Bay Area have wildly different ADU rules — what's allowed in unincorporated San Mateo County may not be allowed in Palo Alto, and the rules change yearly. Speculation is false advertising.

**Square footage** — state recorded square footage from county records or MLS. Never round up. Never combine living + non-living square footage (garage, basement, sunroom) without labeling it.

**Lot size** — state recorded lot size from county records. Don't estimate from photos.

**Year built** — state recorded year built. If extensively renovated, you may say "originally built [year], renovated [year]" but never imply newer construction than the records show.

**Solar / EV / smart home features** — only mention if currently installed and operational. "Solar-ready" is OK if the panel is pre-wired; "solar-equipped" requires panels actively producing.

**Permits** — never call something "permitted" unless permits are confirmed in county records. Many additions and remodels in the Bay Area are unpermitted; misrepresenting them creates liability.

When in doubt, omit. A factually accurate listing with fewer claims is always better than an enthusiastic one with one false claim.

---

## Core Principle: Nouns Over Pronouns

AI search engines match buyer queries to listing text through nouns, verbs, and modifiers — not vague pronouns or generic filler. Every sentence should contain specific, searchable terms.

**Weak:** "This beautiful home has been lovingly updated throughout."

**Strong:** "Renovated 4-bedroom Colonial in West Menlo Park with quartz countertops, white oak hardwood floors, and a screened-in porch overlooking a fenced backyard."

The strong version contains 12+ searchable nouns. The weak version contains zero.

**Test:** Could ChatGPT, Perplexity, or Google's AI Overview cite this sentence as a direct answer to a buyer's question? If not, rewrite.

---

## Writing Framework

### Nouns (What it is and where it is)
- **Property type:** Eichler, ranch, contemporary, Mediterranean, craftsman, mid-century, Spanish revival, transitional, traditional, modern farmhouse, townhouse, condo, duplex, multi-unit
- **Location specifics:** neighborhood name, subdivision, city, ZIP, proximity landmarks ("two blocks from Cooley Landing," "walking distance to downtown Redwood City," "five-minute drive to Stanford")
- **Features:** specific materials, room names, upgrades, systems
- **Nearby amenities:** parks, retail, transit (Caltrain stations especially), employers (Meta, Google, Stanford, SLAC, etc.) — name them factually, don't rank them

### Verbs (What it offers)
- features, overlooks, includes, connects to, opens to, sits on, backs to, offers, provides, anchored by, stretches across, leads to, opens onto

### Modifiers (What makes it searchable)
- **Use:** renovated, updated, turnkey, open-concept, move-in ready, low-maintenance, energy-efficient, single-level, two-story, gated, corner lot, end-unit, top-floor, ground-floor, solar-equipped, EV-charger-installed
- **Avoid:** stunning, gorgeous, amazing, dream home, must-see, breathtaking, one-of-a-kind, rare opportunity (these are zero-information words AI search ignores)

---

## Bay Area Context (Default Localization)

When the listing is in one of Graeham's primary markets, weave in regionally-meaningful details that buyers are actually searching for:

**East Palo Alto (EPA):**
- Proximity to Meta HQ (1 Hacker Way), Stanford Research Park, Cooley Landing, Bay Trail
- Neighborhoods: Woodland Park, Weeks neighborhood, Gardens, Westside, University Village
- Caltrain access via Palo Alto or Redwood City stations
- 101 / Dumbarton Bridge access
- School district: Ravenswood City School District (factual mention only)

**Redwood City (RWC):**
- Caltrain station (downtown), Highway 101, walkability to Courthouse Square, dining
- Neighborhoods: Mt. Carmel, Stambaugh-Heller, Friendly Acres, Centennial, Roosevelt, Edgewood Park, Emerald Hills
- Proximity to Oracle, Box, Electronic Arts

**Palo Alto (PA):**
- Stanford University, downtown University Avenue, Caltrain (downtown + California Ave stations)
- Neighborhoods: Crescent Park, Old Palo Alto, Professorville, Community Center, Midtown, Barron Park, Greenmeadow
- Proximity to Menlo Park / Sand Hill Road employers

**Menlo Park (MP):**
- Sand Hill Road (VC corridor), Stanford, downtown Santa Cruz Avenue
- Neighborhoods: West Menlo, Allied Arts, Linfield Oaks, Sharon Heights, Belle Haven, Willows
- Caltrain station

**San Mateo County:**
- Highway 101, 280, Caltrain spine, SFO access
- Cities: San Mateo, Burlingame, Foster City, San Carlos, Belmont, Half Moon Bay

For any market, name nearby Caltrain station, freeway access, and major employers when present — Bay Area buyers prioritize commute facts.

---

## The Walkthrough Structure (How To Sequence the Description)

Write the remarks as if walking the buyer through the property. Order the description in the sequence a buyer would experience the home, not as a feature dump. This is more readable for humans AND scans more naturally for AI search engines.

Standard sequence (adjust to property type — condos and lofts may skip outdoor sections, multi-units may emphasize layout differently):

1. **Opening line — what it is + where it is.** [Condition modifier] [property type] + [bed/bath] + [lot or square footage] + in the [specific neighborhood] of [city, state]. Front-load the most searchable terms here. AI platforms truncate or summarize — the first 50 words carry the most weight.

2. **Approach + curb appeal.** Street position, exterior architecture, landscaping, driveway, entry. Physical only — no neighborhood-quality language. ("Sits on a quiet residential street with mature trees" is OK. "Located in a great neighborhood" is not.)

3. **Entry + main living areas.** Foyer, then the flow through living, dining, and kitchen. Kitchen is the hero of most listings — name materials (quartz, granite, butcher block), appliance details (gas range, double oven, wine fridge), and layout features (island with seating, walk-in pantry, breakfast nook).

4. **Primary suite.** Bedroom features (vaulted ceiling, walk-in closet) + bathroom features (tiled shower, double vanity, soaking tub). Note location within the home (rear for privacy, upper level, separate wing).

5. **Secondary bedrooms + bathrooms.** Number, layout, any standout features. Shared bath details if applicable.

6. **Outdoor space.** Yard size, hardscape (patio, deck, pool), landscaping, fencing. Garage details (attached/detached, capacity, EV charging if installed). ADU only if verified per Truth-in-Advertising rules above.

7. **Systems + recent upgrades.** Year-stamped: HVAC, roof, solar, electrical, plumbing, windows. Buyers searching "recently renovated" or "new HVAC" need these named explicitly.

8. **Location context.** Nearby Caltrain station, freeway access, employer proximity, parks/Bay Trail/landmarks. Close with the city, county, and ZIP repeated for AI search anchoring.

Not every section needs equal weight. A turnkey home spends most of its character budget on finishes and recent upgrades. A fixer spends most of its budget on lot size, location, and bones. (See Condition-Aware Framing below.)

---

## Condition-Aware Framing

Adapt emphasis based on the property's condition. Get the condition tier from the agent at intake — don't guess from photos.

| Condition tier | Emphasize | De-emphasize |
|---|---|---|
| **Fixer / poor condition / contractor special** | Lot size, location, bones (foundation, roof structure, layout potential), square footage, neighborhood demand, recent comparable sale prices in the area as honest market context. Use "investment opportunity," "bring your contractor," "blank canvas," "value-add potential" framing carefully — only when factually accurate. | Cosmetic finishes (kitchen, bath, flooring) — these are being replaced anyway. Don't name dated finishes by material; just acknowledge the home is dated. |
| **Mid-range / lived-in / livable but dated** | Honest condition, square footage, layout flow, location, any genuine standout features (large lot, recently updated kitchen, recent roof). Acknowledge what's been updated and what hasn't — buyers can read between the lines. | Generic "lovingly maintained" language that signals nothing. Don't oversell mid-range as turnkey. |
| **Move-in ready / well-maintained / recent updates** | Recent upgrades with year stamps (kitchen 2023, HVAC 2024, roof 2022), finish materials by name, system updates, turnkey framing, professional landscaping. | Areas that haven't been touched in years — if the bathrooms are original to a 1970s build, leave them out and let photos speak. |
| **Renovated / fully remodeled** | Full feature stack with material specifics (quartz brand, hardwood species, appliance brands), down-to-the-studs framing if accurate, smart home integration, EV charging, solar production. | Pretending it's not a flip if it is — buyers can tell. Honest framing builds more trust than aspirational positioning. |
| **New construction** | Year built, builder/developer name, warranty status, energy-efficiency ratings, smart home pre-wiring, finish package level. | Comparing favorably to older neighbors. |

**Special cases:**
- **Tenant-occupied:** must disclose tenancy. Frame as "currently tenant-occupied at $X/mo, lease terms available" — buyers underwriting on cash flow want this front and center.
- **Multi-unit / income property:** lead with unit mix, current rents, gross income, then property features.
- **Probate / trust sale:** mention if relevant to disclosures. Frame factually.
- **Short sale / REO:** disclose accurately. Don't dress up a distressed sale as standard.

---

## Phase 0 — Address-First Research (Optional, Opt-In)

> **This phase is OPTIONAL.** It's the address-first workflow adapted from Jason Pantana's Listing Remarks Writer. Use it when the property has prior online presence (relist, expired-then-renewed listing, property that was previously rented or sold) and you want the skill to pre-populate the intake from public data rather than typing it all in. Skip it for new construction, pocket listings, or any property with no online footprint.

### When to use Phase 0

**Use Phase 0 when:**
- The property has been listed before on MLS, Zillow, Redfin, or Realtor.com (relist or expired/renewed)
- You want to see how the home was previously described, especially if it failed to sell (so you can deliberately reframe)
- The agent only gave you an address and wants the skill to pull specs from public sources before they confirm
- You're rewriting a stale listing and want to compare your draft to the prior remarks before pushing

**Skip Phase 0 when:**
- New construction (no online history)
- Pocket / off-market listings the agent doesn't want indexed
- The agent has already provided all specs in the intake
- Time-sensitive turnaround where the web pull would slow things down

### How to invoke Phase 0

The agent triggers Phase 0 by giving you ONLY a property address with no specs, OR by explicitly saying "run Phase 0," "research the listing first," or "pull past data on this address."

### Phase 0 Steps

1. **Web-search the address** across Zillow, Redfin, Realtor.com, Compass, and the MLS syndicator network using the available browser/fetch tools (Claude in Chrome MCP if connected, WebFetch otherwise). Pull whatever's public:
   - Beds, baths, square footage, lot size, year built
   - Tax parcel info, property tax history, recent sales
   - HOA status and amenities (if applicable)
   - Architectural style, exterior features (porches, patios, landscaping)
   - Notable upgrades or renovations mentioned in any past listing
   - Photos (URLs only — for reference)

2. **Pull prior listing remarks** if the property was listed before:
   - Capture the verbatim public remarks from each prior listing (Zillow and Redfin both archive these)
   - Note the listing dates, list prices, sold prices (if sold), and DOM
   - Note if the listing expired, was withdrawn, sold, or is currently active

3. **Summarize prior listing themes** in 3-5 bullets:
   - What features did prior remarks emphasize?
   - What tone / voice did they use (luxury, family-friendly — note: avoid that descriptor in OUR output, but flag if prior remarks used it, investor-focused, lifestyle, factual)?
   - What was omitted that probably should have been mentioned?
   - Did prior remarks make any compliance-risky claims (Fair Housing proxies, unverified ADU language, school quality claims)? Flag these so we don't repeat the error.

4. **Present findings to the agent in TWO clearly-labeled sections** before writing anything:

   ```
   ## Specs Found Online
   [bulleted list of pulled property details with source]
   
   ## Themes / Remarks from Past Listings
   [3-5 bullets summarizing prior listing voice, emphasis, and any compliance flags]
   
   ## Confirm before I draft:
   - Are these specs still accurate, or have there been changes (new roof, new HVAC, updated kitchen, etc.)?
   - Condition tier (fixer / mid / move-in / renovated / new construction)?
   - Any standout features not in the online data that should be emphasized?
   - Style direction: do you want to match the prior listing voice, deliberately diverge from it, or use a different sample?
   ```

5. **Wait for agent confirmation** before proceeding to the Intake checklist below. The agent's confirmation populates the intake fields automatically — items 1-4 of the Intake should already be answered from Phase 0 + agent confirmation. The agent only needs to fill in items 5-12.

### Phase 0 Hard Rules

- **Never fabricate specs.** If Zillow says 3 bed and Redfin says 4 bed, present both and ask the agent to confirm which is accurate. Don't silently pick one.
- **Never use prior listing remarks verbatim.** Always rewrite. Verbatim copying creates copyright issues and re-imports any compliance errors the prior agent made.
- **Always flag compliance issues in prior remarks.** If the prior listing said "great family neighborhood" or "blue ribbon schools," call it out so the agent knows we're not repeating that.
- **Phase 0 does NOT replace the agent's verification.** The web-pulled specs are a starting point; the agent confirms final accuracy. County records still trump web sources for legal numbers.

---

## Intake (Ask Before Writing)

> **If Phase 0 ran**, items 1-4 below are already answered from the web pull + agent confirmation. Skip to items 5-12. If Phase 0 was skipped, run the full intake.

Collect the following in one message if not already provided:

1. **Property address** (street, city, ZIP)
2. **Property type** (single-family, condo, townhouse, multi-unit, etc.)
3. **Beds / baths / square footage / lot size / year built** (from county records or MLS — verified)
4. **Condition tier** (fixer / mid / move-in / renovated / new construction)
5. **Recent upgrades with years** (kitchen 2023, HVAC 2024, roof 2022, etc.)
6. **Standout features the agent wants emphasized** (the "wow" factors visible in photos or known to the agent)
7. **Neighborhood / subdivision name**
8. **Nearby amenities the listing benefits from** (parks, transit stations, employers — factually named, not rated)
9. **MLS character limit** (default 1500 for MLSListings; ask if other MLS)
10. **ADU status** — if any ADU language is being considered: zoning permitted? lot meets requirements? HOA/CC&R checked? If any answer is "unsure," omit ADU language.
11. **Compliance flags** (HOA, Mello-Roos, flood zone, special assessments, easements, tenant occupancy) — must be referenced if material to listing accuracy
12. **Photos** (optional but useful) — if uploaded, use them to inform the walkthrough sequence and identify features the agent didn't mention

Don't proceed without items 1–4. Items 5–12 improve quality but aren't blockers.

---

## Example (East Palo Alto, Move-In Ready)

**Input:** 4 bed, 3 bath single-family, 2,400 sqft, 6,500 sqft lot, built 1962 / renovated 2023, Woodland Park neighborhood EPA, white oak floors, quartz kitchen, gas range, primary suite with walk-in closet, new HVAC + solar, two-car attached garage, near Cooley Landing + Bay Trail. Condition tier: move-in ready. ADU status: not verified (omit).

**Output (~1480 chars):**

Renovated 4-bedroom, 3-bathroom single-family home in the Woodland Park neighborhood of East Palo Alto, California. The 2,400-square-foot residence sits mid-block on a quiet residential street with mature trees and a recently replaced concrete driveway leading to a covered entry. Inside, the foyer opens to an open-concept main level with white oak hardwood floors throughout. The living room features oversized windows facing the front yard and connects to a dining area with contemporary lighting. The kitchen anchors the space with white quartz countertops, a five-burner gas range, stainless steel appliances, a tiled backsplash, and a center island with seating for four. A walk-in pantry sits just off the kitchen. The primary suite occupies the rear of the home with a vaulted ceiling, walk-in closet, tiled walk-in shower, and double vanity. Three additional bedrooms share two full bathrooms in a separate wing. The 6,500-square-foot lot offers a fenced backyard with a covered patio, mature fruit trees, and turf landscaping. A two-car attached garage provides direct interior access. A new HVAC system and roof-mounted solar panels installed in 2023 reduce monthly utility costs. Located approximately five minutes by car to Caltrain service at the Palo Alto station, with Highway 101 and Dumbarton Bridge access nearby. Meta's Menlo Park headquarters, Stanford University, and Cooley Landing are within a short drive. East Palo Alto, San Mateo County, 94303.

---

## Example (Same Property, Fixer Condition Tier)

**Input:** Same address. 4 bed, 3 bath, 2,400 sqft, 6,500 sqft lot, built 1962, NOT renovated — original kitchen, original baths, dated finishes, deferred maintenance. Condition tier: fixer.

**Output:**

Single-family home on a 6,500-square-foot lot in the Woodland Park neighborhood of East Palo Alto, California. The 2,400-square-foot residence offers 4 bedrooms, 3 bathrooms, and a flexible single-level floor plan with strong bones for ren