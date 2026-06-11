# Market Configuration — Graeham Watts

Pre-filled config for the chatgpt-ads skill. Brand identity fields mirror `../../shared-references/identity.json` — if they ever conflict, identity.json wins. Campaign Settings are per-run decisions; confirm with Graeham each campaign.

---

## The Agent
- Name: Graeham Watts
- Brokerage: Intero Real Estate (DRE# 01466876)
- Contact: graehamwatts@gmail.com · 650-308-4727
- Years in business: Licensed Peninsula agent since 2004
- Career volume: 429 closings, $354M career volume, peak years of 41 transactions
- Designations: Not specified — confirm
- Languages: English
- Primary website: https://graehamwatts.com
- Additional URLs: Published content hub at https://graehamwatts.github.io/online-content/ (CMAs, dashboards, newsletters)

## Market
- Primary city/metro: East Palo Alto, CA (San Francisco Peninsula)
- Country (2-letter code for ads): US
- State/province: California
- Active markets: East Palo Alto (primary); Redwood City, Palo Alto, Menlo Park, San Mateo County, broader Peninsula (secondary)
- Market dynamics: Per-run — pull current stats via the mls-matrix-scraper skill or recent MLS data rather than hardcoding here. Bay Area Peninsula market; EPA is the value-entry city surrounded by some of the most expensive zip codes in the country.
- Unique market factors: EPA rent control / AB 1482 questions, ADU potential on Peninsula lots, equity-rich long-time owners, tech-relocation demand, high-rate lock-in inventory dynamics

## Specializations
- Buyer/seller split: Both; seller-leaning in EPA farm
- Active niches: EPA homeowners/sellers, first-time buyers, equity/move-up sellers, landlords & AB 1482 owners, past clients, relocation
- Niches to grow: Seller listings in EPA + Peninsula, off-market/probate opportunities
- Niches to avoid: Not specified — confirm
- Typical price range: EPA roughly $700K–$1.3M; secondary markets to $3M+ — verify against current MLS data per run
- Luxury threshold: ~$3M (Palo Alto / Menlo Park context)

## Positioning
- Want to be known for: 20+ years of Peninsula expertise, data-driven pricing (CMA depth), hyperlocal EPA knowledge, direct honest guidance
- Landing pages available: graehamwatts.com pages — AUDIT PER RUN (Phase 2); home-value page is the workhorse CTA destination (also used by farming postcards via Switchy QR routing)
- Voice and tone notes: Direct, warm, expert without jargon. No hype, no Zillow-style genericisms. Sounds like a person, not a brand. See `../../shared-references/branding.md` and the humanizer skill conventions.

## Campaign Settings (per-run — confirm each campaign)
- Objective: Clicks (CPC) default, $3–5 starting max bid
- Budget total / type / dates: per run
- Brokerage ad review required: Confirm with Graeham/Intero before first launch

## Compliance Notes (US / California)
- Fair Housing Act: no targeting or implied preference by protected class; target the housing situation, never the household. No school-quality or "safe neighborhood" proxies (see content-creation-engine Fair Housing guardrails).
- RESPA: no referral kickbacks for settlement services.
- California DRE advertising rules: ads must identify the brokerage (Intero Real Estate) and license number (DRE# 01466876 — from identity.json, never from memory).
- Brokerage ad review per Intero policy.
