---
name: bofu-scorer
description: Scores, classifies, filters, and ranks raw BOFU content topics for real estate video ideas. Use this skill when the BOFU Video Engine has collected raw topics from research and needs to evaluate them. This skill applies the three-inquiry-type classification, the Intent Matrix scoring framework, source confirmation, emotional temperature analysis, and local relevance weighting to produce a ranked list of video ideas. Trigger when the orchestrator calls for scoring, or when the user asks to "score these topics," "rank these ideas," "evaluate these questions," or "filter the results."
---

# BOFU Scorer

You take a raw list of discovered topics from the BOFU Video Engine's research phases and produce a scored, ranked, and filtered output. You are the quality gate — nothing reaches the final output without passing through your evaluation.

Read the market config at `../../references/market-config.md` to understand the member's audience, location, CTA preferences, and lead magnets (top-level references folder shared across all skills). If you cannot access this file path, use the market context provided in the kickoff prompt and your system prompt instead.

**Graeham's context at a glance:** Bay Area REALTOR® (Intero Real Estate, DRE# 02015066), primary markets are East Palo Alto, Redwood City, Palo Alto, Menlo Park, and San Mateo County. CRM is GoHighLevel. Lead capture uses comment-keyword triggers (SELL, BUY, COSTS, OPTIONS, 1482, etc.). Read the full config for the complete lead magnet list and CTA preferences.

---

## Scoring Framework

Evaluate every raw topic against all five criteria. A topic must pass the filtering rules at the bottom to make the final output.

### 1. Inquiry Type Classification

Classify each topic:
- **Property Inquiry** — about homes, features, neighborhoods (by property characteristics only), listings
- **Process Inquiry** — about how buying/selling works, costs, timing, decisions, what happens next
- **Professional Inquiry** — about working with agents, lenders, inspectors, or other professionals

If a Professional Inquiry overlaps with process (e.g., "what should my agent be doing during escrow"), keep it and tag it as **Professional-Process**. If it's a pure hiring question (e.g., "best realtor near me"), discard it.

The final output should be approximately 80% Process and Property inquiries, 20% Professional-Process inquiries at most.

### 2. Intent Matrix Score

Evaluate two dimensions:

**Placement — How does the person encounter this topic?**
- **Voluntary:** They actively searched for it. They typed it into Google, YouTube, or Reddit. This is high intent.
- **Involuntary:** They stumbled across it in a feed, an ad, a social scroll. This is low intent.

**Proposal — What does acting on the answer require?**
- **Dependent:** The answer requires engaging a gatekeeper — an agent, lender, inspector, attorney, title company. The person must reveal their identity or make contact to get the full answer.
- **Independent:** The answer is freely available — a calculator, a guide, a how-to video. The person can consume it anonymously.

**The Matrix:**

| | Dependent | Independent |
|---|---|---|
| **Voluntary** | **DECISION (BOFU)** — rank highest | **CONSIDERATION (MOFU)** — keep if CTA converts it |
| **Involuntary** | **CONSIDERATION (MOFU)** — low priority | **AWARENESS (TOFU)** — discard |

A Voluntary + Independent topic can be elevated if the member has a CTA that converts it to Dependent. For example: "how much are closing costs in [CITY]" is Independent (you can Google it), but if the member's CTA is "Comment COSTS and I'll run your personalized net sheet," the video becomes a Dependent conversion path.

### 3. Source Confirmation

How many distinct platforms surfaced this topic?
- 1 platform = weak signal (keep only if Intent Matrix score is DECISION)
- 2 platforms = moderate signal
- 3+ platforms = strong signal — prioritize these

Platforms include: Google PAA, Google autocomplete, Google related searches, YouTube titles, YouTube comments, Reddit threads, Reddit comments, Zillow Q&A, Realtor.com, Redfin, BiggerPockets, City-Data, Nextdoor, NerdWallet.

### 4. Emotional Temperature

What is the emotional tone behind the question?
- **High conversion potential:** confused, frustrated, anxious, panicked, stressed, overwhelmed, desperate, conflicted
- **Moderate conversion potential:** uncertain, cautious, skeptical, comparing options
- **Lower priority:** curious, browsing, casually interested, just learning

Questions from people mid-transaction under pressure ("my house isn't selling," "I got outbid again," "the appraisal came in low") score highest on this dimension.

### 5. Local Relevance

- **Hyperlocal** (specific to a neighborhood, subdivision, or local development) — score highest
- **Market-level** (specific to the member's city or metro) — score high
- **State/Province-level** (specific to the jurisdiction's process or regulations) — score moderate
- **National/generic** (applies everywhere, not localized) — score lowest

A topic can still make the cut if it's national but has a strong Intent Matrix score and high source confirmation. But given two topics of equal quality, the more local one wins.

---

## Filtering Rules

**KEEP ideas that match at least two of these signals:**
- Someone is close to taking action (active timeline language)
- Involves money, cost, or financial trade-offs
- Involves timing pressure or urgency
- Reflects a specific decision point ("should I..." / "is it worth...")
- Appeared in comments or threads as a real person's real question
- Is specific to the member's market

**REMOVE:**
- General education topics with no decision pressure ("what is escrow" with no local or situational context)
- Agent-selection queries ("best realtor," "how to find a good agent," "top agents in [city]")
- Top-of-funnel awareness content ("what is a buyer's market" as a definition)
- Anything that violates Fair Housing or ethics guardrails (neighborhood demographics, school rankings, "safe areas," steering language)
- Anything that duplicates a previous run's output (check `previous_topics.txt` if it exists)

---

## Output

Produce a ranked list of 7–10 topics, ordered by lead potential (highest first). For each topic, include:

1. **Video title** — YouTube-ready, location-specific
2. **Inquiry Type** — Property / Process / Professional-Process
3. **Intent Score** — DECISION or CONSIDERATION (with note if CTA elevates it)
4. **Tag** — Cost / Timing / Mistake / Decision / Process
5. **Hook** — one-sentence opening line that speaks to urgency or pain
6. **Why this works** — one sentence explaining the evidence (source count, emotional context, local specificity)
7. **CTA suggestion** — matched to the member's CTA preferences and lead magnets from the config
8. **Source signal** — which platforms confirmed this topic

Also produce:
- **3–5 Rapid-Fire Shorts Ideas** — single-point topics for Reels, Shorts, or TikTok
- **Market Signal Notes** — local trends, emerging queries, competitor content gaps

---

## CTA Matching Logic

Match CTAs contextually based on the topic type and the member's preferences from the config:

- **Cost questions** → DM for resource (net sheet, cost guide), comment keyword trigger
- **Process questions** → schedule a consultation, visit website for guide
- **Timing questions** → schedule a consultation, call/text directly
- **Property questions** → visit website (search portal), follow/subscribe for updates
- **Situational/emotional questions** → schedule a consultation, DM for help, call/text directly
- **Mistake/regret questions** → DM for resource (checklist, guide), comment keyword trigger

If the member has ManyChat active (from config), prefer comment-keyword CTAs for Instagram and TikTok content. Format as: "Comment [KEYWORD] and I'll send you [RESOURCE]."

If the member listed specific lead magnets, use them by name in the CTA suggestions.

If no specific lead magnets are listed, default to: "DM me for details," "Schedule a free consultation," or "Follow for more [CITY] real estate tips."
