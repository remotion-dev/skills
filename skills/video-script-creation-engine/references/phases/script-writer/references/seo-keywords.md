# SEO / Search Console Keyword Clusters

This file captures Graeham's target keyword clusters for SEO/AEO content. In Phase 2, this will be dynamically updated from live Search Console data via the Windsor `searchconsole` connector. For now, these are the target clusters to design content around.

## How to Use This File

When generating BOFU or MOFU long-form content (YouTube or blog):

1. Pick the relevant cluster based on the content topic
2. Use the primary keyword in the title, URL slug, H1, first 100 words, and meta description
3. Use the secondary keywords naturally throughout the body
4. Use the long-tail variants as H2 headers (remember: question format per `aeo-geo-requirements.md`)

## Priority Cluster: Legal/Regulatory (HIGHEST VALUE)

This is Graeham's highest SEO value cluster because he already ranks position 13 for "ab 1482" with 130+ impressions. Close to page 1 with minimal effort.

**Primary keywords:**
- ab 1482
- california rent control
- ab 1482 exemptions
- ab 1482 notice requirements
- rent increase cap california

**Long-tail (H2 header material):**
- Is AB 1482 still in effect in California for 2026?
- What properties are exempt from AB 1482?
- How much can a landlord raise rent under AB 1482?
- What happens if a landlord violates AB 1482?
- Does AB 1482 apply to single-family homes?

**Lead capture keyword:** 1482

---

## Cluster: Market Updates (HIGH VOLUME)

Market update content is evergreen — people search for it every month. Must be produced monthly.

**Primary keywords:**
- bay area housing market
- east palo alto housing market
- palo alto real estate market
- redwood city home prices
- menlo park real estate
- silicon valley housing market [month] [year]

**Long-tail:**
- Is the Bay Area housing market slowing down?
- What is the median home price in East Palo Alto?
- Are home prices dropping in Palo Alto?
- What is the average days on market in Redwood City?
- How is the Menlo Park real estate market right now?

**Lead capture keyword:** MARKET

---

## Cluster: First-Time Buyer Education (HIGH VOLUME, HIGH INTENT)

**Primary keywords:**
- first time home buyer bay area
- how to buy a house in california
- bay area down payment assistance
- closing costs california
- home buying process california

**Long-tail:**
- How much do I need to buy a house in the Bay Area?
- What are closing costs really in California?
- What credit score do I need to buy in Silicon Valley?
- How long does it take to close on a Bay Area home?
- What's the first step to buying a house in East Palo Alto?

**Lead capture keyword:** READY

---

## Cluster: Seller Education (HIGH INTENT)

**Primary keywords:**
- how to sell a house in california
- cma bay area
- seller closing costs california
- when to sell a home bay area
- home prep for sale

**Long-tail:**
- How much does it cost to sell a house in the Bay Area?
- What are seller closing costs in California?
- When is the best time to sell a home in Palo Alto?
- Should I sell my house now or wait?
- How do I prepare my home for sale in the Bay Area?

**Lead capture keyword:** SELL or CHECKLIST

---

## Cluster: Investor / Investment Property (HIGH VALUE LEADS)

**Primary keywords:**
- bay area investment property
- silicon valley rental property
- east palo alto duplex
- bay area cap rate
- 1031 exchange california

**Long-tail:**
- What's the cap rate on a Bay Area rental?
- Is East Palo Alto a good investment in 2026?
- How do I buy a duplex in Silicon Valley?
- Can I 1031 exchange out of California?
- What does a cash-on-cash return look like in the Bay Area?

**Lead capture keyword:** INVEST

---

## Cluster: Trigger Event — Tech Layoffs (HIGHEST-CONVERTING)

**Primary keywords:**
- tech layoff home sale
- silicon valley layoff real estate
- bay area layoff home equity
- what to do with home after layoff
- selling home after job loss california

**Long-tail:**
- What should I do with my Bay Area home if I get laid off from Meta?
- Should I sell my house after losing my tech job?
- How much equity do I need to walk away from a Bay Area mortgage?
- What are my options if I can't afford my Bay Area home anymore?
- Can I short sale a house in California after a layoff?

**Lead capture keyword:** OPTIONS

---

## Cluster: Trigger Event — Relocation (INCOMING BUYERS)

**Primary keywords:**
- moving to the bay area
- relocating to silicon valley
- bay area tech relocation
- what $1m buys in the bay area
- bay area neighborhoods for families

**Long-tail:**
- What's it like moving to the Bay Area from [other city]?
- What neighborhoods should I consider when relocating to Silicon Valley?
- What does $1 million buy you in the Bay Area?
- Which Bay Area neighborhoods are best for tech workers?
- How do I find a home in the Bay Area before I move?

**Lead capture keyword:** RELOCATING

---

## Cluster: Trigger Event — Inherited Property

**Primary keywords:**
- inherited property california
- how to sell inherited house california
- inherited home property tax california
- prop 19 california
- step up basis inherited property

**Long-tail:**
- What do I do with an inherited house in California?
- How does Prop 19 affect inherited property in California?
- Do I pay capital gains on an inherited home?
- How do I sell my parents' house in the Bay Area?
- What is the step-up in basis for inherited property?

**Lead capture keyword:** OPTIONS or SELL

---

## Cluster: Rent vs. Buy (MOFU → BOFU CONVERSION)

**Primary keywords:**
- rent vs buy bay area
- is it worth buying in the bay area
- bay area rent increase
- should i buy or keep renting silicon valley

**Long-tail:**
- Is it smarter to rent or buy in the Bay Area in 2026?
- When does buying make more sense than renting in Silicon Valley?
- How much do I need to make to afford a Bay Area mortgage?
- What's the break-even point for buying vs renting in Palo Alto?

**Lead capture keyword:** NUMBERS

---

## Cluster: Neighborhood-Specific (HYPER-LOCAL SEO)

For each primary market, produce neighborhood-level content:

**East Palo Alto:**
- is east palo alto safe now
- east palo alto schools
- east palo alto vs palo alto
- what's it like living in east palo alto
- east palo alto gentrification

**Redwood City:**
- redwood city downtown
- redwood city vs san carlos
- best neighborhoods in redwood city
- redwood city schools ranking

**Palo Alto:**
- best neighborhoods in palo alto
- palo alto vs menlo park
- palo alto school districts
- old palo alto homes for sale

**Menlo Park:**
- menlo park vs atherton
- west menlo park homes
- sharon heights menlo park
- allied arts menlo park

**Lead capture keywords:** EPA, RWC, PA, MP (area-specific)

---

## Phase 2 Note

In Phase 2, the `content-ideation-engine` sub-skill will pull live Search Console data via the Windsor MCP `searchconsole` connector and dynamically update this file with:

- Queries where Graeham currently ranks position 10–30 (quick wins close to page 1)
- Queries with high impressions but low CTR (title/meta optimization opportunities)
- New query clusters Graeham hasn't targeted yet

Until then, use the static clusters above as the target.
