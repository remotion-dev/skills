---
name: format-ranker
description: Ranks content formats (YouTube Long, YT Short, IG Reel, TikTok, Carousel, Blog, GBP, Facebook, Email) for each scored topic so the script-writer knows which derivatives to produce first. Use this skill after the bofu-scorer (Phase 4) and funnel-tagger (Phase 5) have run, before script-writer (Phase 6). Trigger when the orchestrator calls for format ranking, or when the user asks "which platforms should this topic go on" or "rank the formats for this topic."
---

# Format Ranker

You take a scored, funnel-tagged topic and output a ranked list of which content FORMATS to produce for it, and in what order. This is the bridge between scoring (which topics are worth making) and production (how each topic gets made).

This phase runs AFTER bofu-scorer (Phase 4) and funnel-tagger (Phase 5), and BEFORE script-writer (Phase 6). The output of this phase is consumed by script-writer to decide which derivatives to actually generate.

**Aligned with PropOS Content Intelligence v1.0 Format Type Scoring Formula.**

---

## When to run this skill

- After each topic has Tier 1 base score (≥18/25), Tier 2 Impact + Ease scores, funnel stage tag, workflow assignment (1-5), and gap type tag from prior phases
- Before script-writer generates the actual content derivatives
- Skip this skill ONLY if the user has explicitly requested a single specific format (e.g., "just make me the YouTube Long for this topic")

---

## Inputs (per topic)

Each topic arriving at this phase should already have these fields populated:

- `topic_title` (string)
- `funnel_stage` (TOFU / MOFU / BOFU)
- `workflow_assignment` (1-5, per cross-posting-matrix)
- `production_route` (PropCast / Human / Hybrid)
- `gap_type` (Pure / No-video / Better-than / Format mismatch / Frequency / Voice / Audience segment / None)

You will additionally assess these 5 inputs per topic:

| Input | Range | How to measure |
|---|---|---|
| Topic complexity | 1-5 | 1 = stat dump or single-fact ("median price dropped 4.2%"). 3 = moderate explanation needed ("how escrow works"). 5 = legal/regulatory explainer ("AB 1482 owner-occupied duplex exemption"). |
| Visual potential | 1-5 | 1 = pure talking head ("here's a tip"). 3 = some B-roll helps ("market update with chart overlays"). 5 = heavily visual ("property tour", "neighborhood drone shot"). |
| Audience attention budget | TOFU / MOFU / BOFU | Already tagged in Phase 5. TOFU = short attention. MOFU = moderate. BOFU = willing to watch long. |
| Search demand | 1-5 | Volume estimate from Google Trends, GSC (when integrated), YouTube search. 1 = thin search. 5 = high-volume query. |
| Trending status | true/false | Is there a trend angle right now? (Layoff wave, legislation change, viral local news, seasonal moment.) |

---

## The Formula

For each format, compute a `format_score` (0-100):

```
format_score = (complexity_fit × 30) +
               (visual_fit × 25) +
               (funnel_fit × 20) +
               (search_demand_fit × 15) +
               (trending_fit × 10)
```

Each `_fit` is a 0.0-1.0 multiplier specific to that format. See the per-format fit tables below.

---

## Per-Format Fit Tables

### YouTube Long (8-15 min)

| Input | Fit calculation |
|---|---|
| complexity_fit | (topic complexity / 5) — YT Long rewards complexity. Complexity 5 → 1.0; Complexity 1 → 0.2 |
| visual_fit | (visual potential / 5) — Helps but not required. Visual 5 → 1.0; Visual 1 → 0.4 (talking head still works on YT Long) |
| funnel_fit | TOFU = 0.4, MOFU = 0.8, BOFU = 1.0 |
| search_demand_fit | (search demand / 5) — high search makes YT Long valuable. Search 5 → 1.0; Search 1 → 0.2 |
| trending_fit | trending → 0.6 (YT Long is too slow for pure trend), evergreen → 1.0 |

### YouTube Short (30-59 sec)

| Input | Fit calculation |
|---|---|
| complexity_fit | inverse of complexity. Complexity 1 → 1.0; Complexity 5 → 0.2 |
| visual_fit | (visual potential / 5) × 0.8 |
| funnel_fit | TOFU = 1.0, MOFU = 0.7, BOFU = 0.5 |
| search_demand_fit | (search demand / 5) × 0.7 (Shorts titles are searchable but Shorts are reach-first) |
| trending_fit | trending → 1.0, evergreen → 0.6 |

### Instagram Reel (30-60 sec)

| Input | Fit calculation |
|---|---|
| complexity_fit | inverse of complexity. Complexity 1 → 1.0; Complexity 5 → 0.2 |
| visual_fit | (visual potential / 5) — Reels reward visual content strongly |
| funnel_fit | TOFU = 1.0, MOFU = 0.8, BOFU = 0.6 |
| search_demand_fit | (search demand / 5) × 0.4 (Reels are not search-driven) |
| trending_fit | trending → 1.0, evergreen → 0.7 |

### TikTok (30-60 sec)

| Input | Fit calculation |
|---|---|
| complexity_fit | inverse of complexity, harsher. Complexity 1 → 1.0; Complexity 5 → 0.1 (TikTok punishes complex content) |
| visual_fit | (visual potential / 5) |
| funnel_fit | TOFU = 1.0, MOFU = 0.6, BOFU = 0.3 |
| search_demand_fit | (search demand / 5) × 0.3 |
| trending_fit | trending → 1.0, evergreen → 0.4 (TikTok strongly rewards trend) |

### Instagram Carousel (5-10 slides)

| Input | Fit calculation |
|---|---|
| complexity_fit | (topic complexity / 5) × 0.8 — Carousels handle complexity well via slides |
| visual_fit | 0.6 across the board (carousels are text+graphics, not video) |
| funnel_fit | TOFU = 0.6, MOFU = 1.0, BOFU = 0.9 (MOFU saveable content shines here) |
| search_demand_fit | (search demand / 5) × 0.4 |
| trending_fit | trending → 0.7, evergreen → 0.8 |

### Blog Post (800-2,500 words)

| Input | Fit calculation |
|---|---|
| complexity_fit | (topic complexity / 5) — blog rewards complexity |
| visual_fit | 0.4 (blog is text-first; images help but aren't core) |
| funnel_fit | TOFU = 0.3, MOFU = 0.8, BOFU = 1.0 |
| search_demand_fit | (search demand / 5) × 1.2 capped at 1.0 (blog is most search-driven format) |
| trending_fit | trending → 0.5, evergreen → 1.0 |

### Google Business Profile (GBP) Post

| Input | Fit calculation |
|---|---|
| complexity_fit | inverse of complexity. GBP posts are short. Complexity 1 → 1.0; Complexity 5 → 0.3 |
| visual_fit | 0.5 (GBP supports one image) |
| funnel_fit | TOFU = 0.6, MOFU = 0.8, BOFU = 1.0 |
| search_demand_fit | (search demand / 5) × 0.9 (GBP feeds local SEO/map pack) |
| trending_fit | trending → 0.5, evergreen → 1.0 |

### Facebook Post

| Input | Fit calculation |
|---|---|
| complexity_fit | (topic complexity / 5) × 0.6 |
| visual_fit | (visual potential / 5) × 0.8 (native video preferred) |
| funnel_fit | TOFU = 0.7, MOFU = 0.5, BOFU = 0.4 (FB is dying for Graeham's audience; only community/dev news still works) |
| search_demand_fit | (search demand / 5) × 0.2 |
| trending_fit | trending → 0.5, evergreen → 0.4 |

### Email Newsletter Snippet (150-250 words)

| Input | Fit calculation |
|---|---|
| complexity_fit | (topic complexity / 5) × 0.6 |
| visual_fit | 0.3 (email is text-first) |
| funnel_fit | TOFU = 0.4, MOFU = 0.8, BOFU = 1.0 |
| search_demand_fit | (search demand / 5) × 0.3 |
| trending_fit | trending → 0.7, evergreen → 0.8 |

---

## Workflow Constraint

After computing format scores, apply the workflow constraint from the topic's `workflow_assignment`:

- **Workflow 1 (Full Ecosystem):** Include all 10 derivatives. Rank by format score, produce top 7-8 first.
- **Workflow 2 (Short-Form Only):** Include ONLY IG Reel, YT Short, TikTok, Facebook. Drop Blog, Email, YT Long, GBP.
- **Workflow 3 (Property Tour Package):** Include YT walkthrough + Highlight Reel + IG Carousel + "What does $X buy?" Short + Blog + GBP + Email blast.
- **Workflow 4 (Market Data Series):** Include YT Long + 1 Short per city + IG Carousel + Hot-take Reel + Blog + Email + GBP posts.
- **Workflow 5 (Evergreen SEO):** Include Deep-dive YT Long + Blog (2,000-3,000 words) + 3-5 quick-tip Shorts + IG Carousel + Lead magnet PDF.

Format scores that fall outside the workflow's allowed list are dropped from the output even if their score is high.

---

## Production Route Constraint

If `production_route` = "Human", flag formats that require avatar generation (YT Long, IG Reel #1 with face-to-camera, TikTok) as human-production required. The script-writer will route accordingly.

If `production_route` = "PropCast", all formats run through the PropCast pipeline.

If `production_route` = "Hybrid", flag each format individually (e.g., Blog → PropCast, Reel → Human).

---

## Worked Example

**Topic:** "AB 1482 rent cap 2026 changes — what landlords need to know"
**Funnel stage:** BOFU
**Workflow assignment:** 5 (Evergreen SEO)
**Production route:** PropCast
**Gap type:** Pure (no Bay Area creator has a definitive 2026 video on this)
**Inputs:** complexity = 4 (legal explainer), visual = 2 (mostly talking head), search demand = 5 (high), trending = true (recent legislative update)

**Format scoring:**

| Format | complexity_fit | visual_fit | funnel_fit | search_demand_fit | trending_fit | Score |
|---|---|---|---|---|---|---|
| Blog | 0.8 | 0.4 | 1.0 | 1.0 | 0.5 | **86** |
| YT Long | 0.8 | 0.4 | 1.0 | 1.0 | 0.6 | **86** |
| GBP | 0.4 | 0.5 | 1.0 | 0.9 | 0.5 | **64** |
| Carousel | 0.64 | 0.6 | 0.9 | 0.4 | 0.7 | **64** |
| YT Short × 3-5 | 0.2 | 0.32 | 0.5 | 0.7 | 1.0 | **45** |
| Email | 0.48 | 0.3 | 1.0 | 0.3 | 0.7 | **57** |

**Workflow 5 filter:** keeps Blog, YT Long, YT Shorts (3-5 quick-tip), Carousel, Lead magnet PDF. Drops Reel, TikTok, FB, Email (not in Workflow 5).

**Final ranked output:**

```
1. Blog (1,500-2,500 words, AEO-optimized) — score 86 — produce FIRST
2. YT Long (8-12 min deep-dive) — score 86 — produce SECOND
3. GBP Post — score 64
4. IG Carousel (5-8 slides) — score 64
5. YT Shorts × 3-5 (one per sub-topic) — score 45 each
6. Lead magnet PDF — included per Workflow 5
```

Hand this ranked list to the script-writer phase. Script-writer produces in this order, or in parallel if production capacity allows.

---

## Output format

```markdown
### Topic: [topic title]
**Funnel stage:** [TOFU/MOFU/BOFU]
**Workflow:** [1-5]
**Production route:** [PropCast / Human / Hybrid]
**Gap type:** [type]
**Inputs:** complexity=[1-5], visual=[1-5], search=[1-5], trending=[bool]

**Ranked formats (within Workflow constraint):**

| # | Format | Score | Notes |
|---|--------|-------|-------|
| 1 | [Format] | [score] | [route: PropCast/Human] |
| 2 | [Format] | [score] | |
| ... | | | |

**Drop reasons (formats excluded by workflow constraint):**
- [Format]: [reason]
```

---

## Honesty check

Before handing off to script-writer:

1. **Does the top-ranked format actually make sense for this topic?** If the formula says "TikTok first" for a legal explainer, the formula is wrong — sanity check and override.
2. **Are any "must-have" formats missing because the workflow constraint dropped them?** If yes, note this and recommend the user reconsider the workflow assignment.
3. **Is the production route realistic?** If "PropCast" but the topic requires Graeham on-camera at a specific property, flip to "Human".

If anything feels off, surface it — don't blindly trust the formula.
