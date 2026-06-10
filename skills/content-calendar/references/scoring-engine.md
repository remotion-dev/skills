# Scoring Engine — moved verbatim from `content-calendar/SKILL.md` (2026-06-09 refactor)

## The Scoring Engine — Opportunity Score

> **Scoring Architecture (Updated April 2026).** This skill owns the **Opportunity Score** — the 25-pt rubric that decides "should we cover this topic THIS WEEK vs other candidates?" A separate score, the **Intent Score**, lives in `content-creation-engine/references/phases/bofu-intent-scorer.md` (absorbed into content-creation-engine May 2026; formerly the `bofu-intent-scorer` standalone skill) and answers "what's the BOFU intent of this topic (DECISION / CONSIDERATION / AWARENESS)?" — used downstream for funnel-mix and CTA decisions. Both scores appear on the single-topic dashboard's Scoring Architecture panel. See `content-creation-engine/SKILL.md` → Scoring Architecture for the full model.

Every potential topic gets scored on 5 criteria. This prevents gut-feel content decisions and ensures the calendar is data-backed.

### Scoring Criteria (25 points max)

| Criterion | Weight | What It Measures |
|-----------|--------|-----------------|
| **Performance Signal** | 0-5 | Does your historical data show this type of content performs well? Top-performing format/topic = 5, average = 3, underperforming = 1 |
| **Search Demand** | 0-5 | Is there search volume for this topic? Rising GSC query = 5, steady query = 3, no search data = 1 |
| **Audience Intent** | 0-5 | Does Reddit/social data show people actively asking about this? Multiple sources confirming demand = 5, one source = 3, assumption only = 1 |
| **Competitive Gap** | 0-5 | Are competitors covering this? Competitors NOT covering it (blue ocean) = 5, covering it but poorly = 3, already saturated = 1 |
| **Timeliness** | 0-5 | Is there a current event or seasonal hook? Breaking news/rate change = 5, seasonal relevance = 3, evergreen = 1 |

**Threshold:** Topics scoring 18+ are "Must Create This Week." Topics scoring 13-17 are
"Strong Candidates." Below 13, save for later or skip.

### Funnel Position Tag

Every topic also gets tagged with its funnel position. This ensures the calendar has a healthy
mix — not all top-of-funnel awareness content and not all bottom-of-funnel sales content.

| Tag | What It Means | Target Mix |
|-----|--------------|------------|
| **TOFU** (Top of Funnel) | Awareness — attracts new eyeballs. Lifestyle, neighborhood tours, market trends | 30-40% |
| **MOFU** (Middle of Funnel) | Consideration — educates active searchers. How-to guides, process explainers, comparison content | 25-30% |
| **BOFU** (Bottom of Funnel) | Decision — converts to leads. Specific listings, pricing guides, "call me" CTAs | 30-40% |

Adjust the mix based on Graeham's current priority:
- **Lead gen focus:** Shift to 20/30/50 (heavy BOFU)
- **Audience growth focus:** Shift to 50/25/25 (heavy TOFU)
- **New listing launch:** One BOFU piece for the listing + normal mix for everything else
