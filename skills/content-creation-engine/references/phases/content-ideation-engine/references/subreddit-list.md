# Curated Subreddit List

Ranked by signal quality for Graeham's primary (EPA) and secondary (Peninsula + Bay Area) markets.

Grouped into three tiers so we can control cost vs. coverage.

---

## Tier 1 — CORE (always scrape, highest signal density)

These 5 subreddits are the highest-ROI sources. They have active Bay Area real estate conversation and consistent weekly volume. Tier 1 alone is enough to produce 3-5 content opportunities per weekly run.

1. **r/BayArea** — the big general Bay Area community. High volume, full spectrum of TOFU → BOFU signals. EPA and Peninsula mentions appear here frequently.
2. **r/bayarearealestate** — specifically about Bay Area housing. Almost every post is MOFU or BOFU. Highest signal-to-noise ratio of any sub on this list.
3. **r/RealEstate** — national but lots of Bay Area threads. Good for generic buyer/seller questions that can be answered with local data.
4. **r/FirstTimeHomeBuyer** — pure MOFU/BOFU signal from the audience Graeham most wants to reach (first-time buyers who need education).
5. **r/Layoffs** — critical for BOFU trigger-event content. When a Meta/Google/Apple layoff wave hits, this is where affected homeowners go to vent and ask "do I need to sell?"

**Estimated weekly scrape cost (Tier 1 only):** ~$0.26 at maxItems=75.

---

## Tier 2 — PENINSULA & PRIMARY MARKETS

City-specific subreddits for Graeham's core geographic target area. Lower volume than Tier 1 but 10x more local relevance when something does surface.

6. **r/PaloAlto** — primary market
7. **r/MenloPark** — primary market (includes West Menlo, Sharon Heights, etc.)
8. **r/RedwoodCity** — primary market
9. **r/SanMateo** — San Mateo County hub
10. **r/Burlingame** — Peninsula
11. **r/SanCarlos** — Peninsula (small but active)
12. **r/Belmont** — Peninsula (small)
13. **r/FosterCity** — Peninsula
14. **r/HalfMoonBay** — Peninsula / Coastside
15. **r/DalyCity** — Peninsula / SF border
16. **r/SouthSanFrancisco** — Peninsula / SF border

**Note on East Palo Alto:** There is no active r/EastPaloAlto subreddit with meaningful traffic. EPA-specific conversations happen inside r/BayArea, r/RedwoodCity, and r/MenloPark threads. We catch EPA signal through those Tier 1 and Tier 2 subs, NOT through a dedicated EPA community (which doesn't exist).

**Estimated weekly scrape cost (Tier 1 + Tier 2):** ~$0.77 at maxItems=225.

---

## Tier 3 — SOUTH BAY & SILICON VALLEY SPILLOVER

For tech worker relocation content and cross-Peninsula migration signals. Only scrape these if the user explicitly asks for the full run or if we're specifically hunting for relocation/trigger-event content.

17. **r/MountainView** — tech hub, relocation source
18. **r/Sunnyvale** — tech hub
19. **r/Cupertino** — Apple HQ
20. **r/SantaClara** — South Bay
21. **r/SanJose** — South Bay hub
22. **r/RealEstateInvesting** — investor audience (BOFU for investment pillar content)

**Estimated weekly scrape cost (Tier 1 + 2 + 3):** ~$1.36 at maxItems=400.

---

## How to use this list in Apify input

Convert the subreddit list to `startUrls` format for the `trudax/reddit-scraper-lite` actor:

```json
"startUrls": [
  {"url": "https://www.reddit.com/r/BayArea/hot/"},
  {"url": "https://www.reddit.com/r/bayarearealestate/new/"},
  {"url": "https://www.reddit.com/r/RealEstate/hot/"},
  {"url": "https://www.reddit.com/r/FirstTimeHomeBuyer/new/"},
  {"url": "https://www.reddit.com/r/Layoffs/hot/"}
]
```

**Sort strategy per subreddit:**
- Tier 1 general subs (r/BayArea, r/RealEstate) → `/hot/` (what's currently engaging)
- Tier 1 niche subs (r/bayarearealestate, r/FirstTimeHomeBuyer) → `/new/` (don't miss anything)
- Tier 2 small city subs → `/new/` (low volume, want everything)
- Tier 3 → `/hot/` (only care about what's actually getting traction)

---

## Adding new subreddits in the future

When Graeham expands to a new market, add the new city's subreddit here under the appropriate tier. No code changes needed — the orchestrator reads this file at runtime.

**Candidates to evaluate later:**
- r/Oakland (East Bay expansion)
- r/Berkeley (East Bay expansion)
- r/Fremont (East Bay / South Bay hinge)
- r/Alameda (East Bay)
- r/Peninsula (regional catch-all if it has volume)

---

## Subreddits we explicitly DO NOT scrape

- **r/sanfrancisco** — SF-specific, mostly tourist/nightlife content, low real estate signal
- **r/politics**, **r/news** — noise
- Any subreddit under 5K members — too quiet to be worth the scrape cost
