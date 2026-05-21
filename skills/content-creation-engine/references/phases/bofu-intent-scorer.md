---
name: bofu-intent-scorer
description: "Classifies real estate content topics by BOFU intent — DECISION / CONSIDERATION / AWARENESS — using Inquiry Type, Intent Matrix, Source Confirmation, Emotional Temperature, Local Relevance, and Freshness. Use this skill ANY time the user asks to: score topics by BOFU intent, classify content by funnel stage, rank topics by lead potential, evaluate which topics are decision-stage vs awareness-stage, filter content ideas by buyer/seller intent, or apply the Intent Matrix to a topic list. Output is a ranked list with intent classification, CTA suggestions, and source confirmation. Standalone use case: agent has a list of candidate topics and wants to know which are genuinely BOFU vs awareness fluff. Trigger on phrases like 'score these topics', 'classify by intent', 'rank by lead potential', 'which of these are BOFU', 'filter by intent', or when content-creation-engine references this skill from its Phase 3."
---

# BOFU Intent Scorer

> **This is the INTENT SCORE, not the OPPORTUNITY SCORE.** Its job is to classify a topic's BOFU intent (DECISION / CONSIDERATION / AWARENESS) for funnel-mix and CTA decisions — NOT to decide whether a topic is worth covering this week. Weekly opportunity ranking belongs to `content-calendar`'s 25-pt Opportunity Score (Performance Signal, Search Demand, Audience Intent, Competitive Gap, Timeliness). See the Scoring Architecture section in `content-creation-engine/SKILL.md` for the full two-score model.

You take a topic (already selected via content-calendar's Opportunity Score, or directly provided by the user) and classify its BOFU intent. You are the funnel-position gate — you decide whether a topic is genuinely a decision-stage conversation, a consideration-stage conversation, or too top-of-funnel to serve BOFU goals.

---

## Before You Start — Read These

1. **`../shared-references/identity.json`** — single source of truth for Graeham's brand identity. NEVER hardcode brand details from memory. Read this file first.
2. **`../content-creation-engine/references/market-config.md`** — full market configuration including CTA preferences, lead magnets, and GHL keyword matrix.
3. **`../content-creation-engine/references/topic-history.json`** — read this for the freshness check (last 4 weeks of posted topics + in-production topics). If it doesn't exist, skip freshness scoring and note it in output.

If the user is scoring topics for a market that isn't Graeham's, ask them for: market name, audience focus, available CTAs/lead magnets, and any topic history they want to use for freshness checks.

---

## Fair Housing Guardrails (Non-Negotiable)

NEVER score a topic that:
- Describes neighborhoods by demographics
- Uses "safe / good areas / family-friendly / up-and-coming" as proxies for demographic signaling
- Ranks or rates schools as a primary selling point
- Promotes kickback arrangements (RESPA violation)

Topics that violate Fair Housing get auto-removed from output, NOT scored low. They don't appear in the result at all.

---

## Scoring Framework

Evaluate every topic against six criteria. Base score is out of 25 (5 criteria × 5 points). Freshness is applied AFTER base scoring as ±5 adjustment. Final threshold to keep: **≥18/25 after freshness.**

### 1. Inquiry Type Classification (5 pts)

Classify each topic:
- **Property Inquiry** — about homes, features, neighborhoods (by property characteristics only), listings
- **Process Inquiry** — about how buying/selling works, costs, timing, decisions, what happens next
- **Professional Inquiry** — about working with agents, lenders, inspectors, or other professionals

If a Professional Inquiry overlaps with process (e.g., "what should my agent be doing during escrow"), keep it and tag as **Professional-Process**. If it's a pure hiring question (e.g., "best realtor near me"), discard it.

The final output should be approximately 80% Process + Property, 20% Professional-Process at most.

### 2. Intent Matrix Score (5 pts)

Two dimensions:

**Placement — How does the person encounter this topic?**
- **Voluntary:** They actively searched for it (Google, YouTube, Reddit). High intent.
- **Involuntary:** They stumbled across it in a feed. Low intent.

**Proposal — What does acting on the answer require?**
- **Dependent:** The answer requires engaging a gatekeeper (agent, lender, inspector, attorney, title company). Person must reveal identity to get the full answer.
- **Independent:** Answer is freely available (calculator, guide, how-to video). Can consume anonymously.

**The Matrix:**

| | Dependent | Independent |
|---|---|---|
| **Voluntary** | **DECISION (BOFU)** — rank highest | **CONSIDERATION (MOFU)** — keep if CTA converts it |
| **Involuntary** | **CONSIDERATION (MOFU)** — low priority | **AWARENESS (TOFU)** — discard |

A Voluntary + Independent topic can be **elevated to Dependent** if the agent has a CTA that converts it. Example: "how much are closing costs in EPA" is Independent (Google-able), but if the CTA is "Comment COSTS and I'll run your personalized net sheet," the video becomes a Dependent conversion path.

### 3. Source Confirmation (5 pts)

How many distinct platforms surfaced this topic?
- 1 platform = weak signal (keep only if Intent Matrix score is DECISION)
- 2 platforms = moderate signal
- 3+ platforms = strong signal — prioritize

Platforms include: Google PAA, Google autocomplete, Google related searches, YouTube titles, YouTube comments, Reddit threads, Reddit comments, Zillow Q&A, Realtor.com, Redfin, BiggerPockets, City-Data, Nextdoor, NerdWallet.

### 4. Emotional Temperature (5 pts)

What's the emotional tone behind the question?
- **High conversion potential (5 pts):** confused, frustrated, anxious, panicked, stressed, overwhelmed, desperate, conflicted
- **Moderate conversion potential (3 pts):** uncertain, cautious, skeptical, comparing options
- **Lower priority (1 pt):** curious, browsing, casually interested, just learning

Questions from people mid-transaction under pressure ("my house isn't selling," "I got outbid again," "the appraisal came in low") score highest.

### 5. Local Relevance (5 pts)

- **Hyperlocal (5 pts):** specific to a neighborhood, subdivision, or local development
- **Market-level (4 pts):** specific to the agent's city or metro
- **State/Province-level (3 pts):** specific to jurisdictional process or regulations
- **National/generic (1 pt):** applies everywhere, not localized

A topic can still make the cut if national but with a strong Intent Matrix score and high source confirmation. Given two equal topics, the more local one wins.

### 6. Freshness Adjustment (±5 pts, applied AFTER base scoring)

Check the topic against `topic-history.json` (read both `history` for posted and `in_production` for shot-but-not-posted — the two-register check).

**Penalties (angle overlap, last 2 weeks):**
- Exact same angle (e.g., `pricing-strategy` again) → **-5 points** (almost always kills the topic)
- Closely related angle (e.g., `pricing-strategy` vs `CMA-explanation`) → **-3 points**
- Different angle, same pillar → **-1 point**
- Different pillar entirely → **no penalty**

**Penalties (market/neighborhood overlap):**
- Same market AND same pillar as a recent topic → **-2 points**
- Same market, different pillar → **no penalty**

**Penalties (GHL keyword overlap):**
- Same GHL keyword used 2+ times in last 2 weeks → **-1 point**

**Bonuses (reward novelty):**
- Pillar not covered in last 4 weeks → **+2 points**
- Market not covered in last 2 weeks → **+1 point**
- Completely novel angle (no semantic overlap with any recent topic) → **+2 points**

A topic with base 20/25 but freshness -5 = 15/25, falls below the 18/25 threshold and gets filtered out. Even great topics shouldn't run if stale.

If `topic-history.json` doesn't exist, skip freshness and note it in the output.

---

## Filtering Rules

**KEEP ideas that match at least two of these signals:**
- Someone is close to taking action (active timeline language)
- Involves money, cost, or financial trade-offs
- Involves timing pressure or urgency
- Reflects a specific decision point ("should I..." / "is it worth...")
- Appeared in comments or threads as a real person's real question
- Is specific to the agent's market

**REMOVE:**
- General education topics with no decision pressure ("what is escrow" with no local or situational context)
- Agent-selection queries ("best realtor," "how to find a good agent," "top agents in [city]")
- Top-of-funnel awareness content ("what is a buyer's market" as a pure definition)
- Anything that violates Fair Housing or RESPA
- Anything that duplicates a previous run's output

---

## Output

Produce a ranked list of 7–10 topics, ordered by lead potential (highest first). For each topic, include:

1. **Video title** — YouTube-ready, location-specific
2. **Inquiry Type** — Property / Process / Professional-Process
3. **Intent Score** — DECISION or CONSIDERATION (with note if CTA elevates it from Independent to Dependent)
4. **Tag** — Cost / Timing / Mistake / Decision / Process
5. **Hook** — one-sentence opening line that speaks to urgency or pain
6. **Why this works** — one sentence explaining the evidence (source count, emotional context, local specificity, freshness)
7. **CTA suggestion** — matched to the agent's CTA preferences and lead magnets from config
8. **Source signal** — which platforms confirmed this topic
9. **Score breakdown** — base score + freshness adjustment = final (e.g., "22/25 base −3 freshness = 19/25")

Also produce:
- **3–5 Rapid-Fire Shorts Ideas** — single-point topics for Reels, Shorts, TikTok
- **Market Signal Notes** — local trends, emerging queries, competitor content gaps
- **Filtered-out summary** — count of topics removed and dominant reasons (Fair Housing, hiring queries, freshness, low intent)

---

## CTA Matching Logic

Match CTAs contextually based on topic type and the agent's preferences from the config:

- **Cost questions** → DM for resource (net sheet, cost guide), comment keyword trigger
- **Process questions** → schedule consultation, visit website for guide
- **Timing questions** → schedule consultation, call/text directly
- **Property questions** → visit website (search portal), follow/subscribe for updates
- **Situational/emotional questions** → schedule consultation, DM for help, call/text directly
- **Mistake/regret questions** → DM for resource (checklist, guide), comment keyword trigger

For Graeham specifically, GHL comment-keyword CTAs are active for: SELL, BUY, COSTS, OPTIONS, 1482, EPA, VALUE, READY, INVEST, NUMBERS, RELOCATING, MARKET, CHECKLIST, WATCH, RWC, PA, MP, SF. Format: "Comment [KEYWORD] below and I'll send you [lead magnet]."

If no specific lead magnets are listed, default to: "DM me for details," "Schedule a free consultation," or "Follow for more [CITY] real estate tips."


---

## Tier 2: Impact + Ease Quadrant Ranking (aligned with PropOS Content Intelligence v1.0)

**Important:** Tier 2 is a RANKING layer that runs AFTER Tier 1 filters out bad topics. The 5-criteria framework above (Jason Pantana's BOFU methodology) stays exactly as-is and continues to be the quality gate. Tier 2 only sees topics that have already passed the 18/25 threshold.

The job of Tier 1 is filtering ("is this topic good enough to make?"). The job of Tier 2 is ranking ("of the good topics, which should we produce first, and where do they go in production?").

Tier 2 produces the data PropCast's Stage 2 expects, so the handoff from this content engine to PropCast works cleanly.

### Impact Score (0-100)

| Component | Points | Notes |
|---|---|---|
| Search Demand | 0-20 | Volume signal from search platforms |
| Audience Intent Strength | 0-20 | PropCast Track A/B/C `intent_score` (10-100) normalized into this slot |
| Macroeconomic Alignment | 0-10 | Match to current market posture |
| Funnel-Fit Bonus | 0-15 | BOFU = +15, MOFU = +10, TOFU = +5 |
| Competitor Gap Boost | 0-15 | `gap_exists` = true → +15. AI Detection conf ≥ 56 auto-promotes to Better-than gap. See ideation-rubric for 7-type classification. |
| Multi-Format Yield | 0-10 | Workflow 1 = 10, W4 = 8, W3 = 7, W5 = 6, W2 = 4 (per cross-posting-matrix) |
| Time Freshness Adjustment | -10 to +10 | From freshness criterion above, normalized |

**Impact Score = sum of components (max 100).**

### Ease Score (0-100)

| Component | Points | Notes |
|---|---|---|
| Inverse Competition Difficulty | 0-30 | 30 = no competitor covers this. 0 = saturated. |
| Content Gap Presence (qualitative) | 0-15 | Independent of competitor gap boolean |
| Format Match with Agent Assets | 0-20 | 20 = existing assets only. 15 = 1-2 new clips. 10 = new shoot. 5 = custom graphics. 0 = capability missing. |
| Production Complexity (inverse) | 0-20 | 20 = simple talking-head. 0 = complex multi-source. |
| Time-to-Publish from Current Pipeline | 0-15 | 15 = this week. 0 = >1 month. |

**Ease Score = sum of components (max 100).**

### The 2×2 Quadrant Matrix

|  | Easy (Ease ≥60) | Hard (Ease <60) |
|--|----------------|-----------------|
| **High Impact (≥60)** | **Q1: Quick Win** — top priority, produce first | **Q2: Strategic Bet** — produce if capacity allows |
| **Low Impact (<60)** | **Q3: Filler** — only if calendar gaps | **Q4: Avoid** — drop |

### Agent Preference Weights (applied AFTER quadrant placement)

- Seller-focused content × 1.5 multiplier on Impact Score
- Brand-focused (TOFU/MOFU) × 1.3 multiplier on Impact Score
- Fair Housing exclusions: dropped entirely
- Deprioritized pillars (per topic-history.json freshness): -10 Impact

### Production Routing Tag

Add `production_route` tag per topic:

- **PropCast** — educational, data-driven, avatar-friendly content
- **Human** — property tours, testimonials, lifestyle content with agent on-camera
- **Hybrid** — split derivatives between PropCast and human production

Default: personal/relationship/property-specific → Human. Educational/data-driven → PropCast. Otherwise Hybrid. PropCast Master Brain v1.0 targets a 90/10 PropCast/Human split.

This routing tag is consumed by the `format-ranker` phase and the `script-writer` phase.

---

## Output Location

When run standalone, save the scored list to:
`outputs/scored-topics-{market-slug}-{timestamp}.json`

When invoked from `content-creation-engine` Phase 3, the engine handles output naming.

---

## Used By

- `content-creation-engine` — Phase 3 of the per-topic content pipeline calls this skill to classify topic intent and decide funnel position before script generation.
- Standalone — agent or content team can score a topic list directly without running the full pipeline (useful when topics come from an external source like a coaching call, Q&A inbox, or competitor analysis).
