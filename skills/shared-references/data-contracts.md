# Data Contracts — Content System

> **Shared reference across `content-creation-engine`, `content-calendar`, `content-ideation-engine`, and `heygen-elevenlabs-renderer`.** This file is the single source of truth for folder names, file naming, JSON schemas, and the two-score model. Updated April 2026 during the scoring-architecture streamline.

---

## The Four-Job Model

The content system has four distinct jobs. Each one has a specific owner skill and a specific output. Jobs are NOT interchangeable, and their outputs must NOT be merged.

| # | Job | Owner | Output file |
|---|---|---|---|
| 1 | Ingest raw audience signal from Reddit | `content-creation-engine/references/phases/content-ideation-engine/` (Phase 2) | `outputs/ideation-raw-{ts}.json`, `outputs/ideation-topics-{ts}.json` |
| 2 | Score topics for WEEKLY coverage (Opportunity Score, 25 pts) | `content-calendar` | `outputs/calendar-data/calendar-{YYYY-MM-DD}.json` + `online-content/dashboards/weekly-calendars/{YYYY-MM-DD}-production-calendar-v6.html` |
| 3 | Classify BOFU intent of ONE topic (Intent Score, 25 pts + freshness ±5) | `skills/bofu-intent-scorer/` (standalone, invoked from content-creation-engine Phase 3) | `outputs/scored-topics-{ts}.json` |
| 4 | Pull per-topic research citations (no scoring) | `content-creation-engine` Phase R | `outputs/research-{topic-slug}-{ts}.json` |

**Rule of thumb for routing:** "Which topic should I cover?" → Job 2. "What's the intent of this one topic?" → Job 3. "What stats/quotes back this specific topic?" → Job 4. "What are people talking about on Reddit?" → Job 1.

---

## Folder Naming (IMPORTANT — different repos, different purposes)

Hosted HTML dashboards and machine-readable JSON live in **different repos**. Don't confuse them.

| Folder | Repo | Purpose | Files inside |
|---|---|---|---|
| `dashboards/weekly-calendars/` | `Graehamwatts/online-content` (separate sister repo) | Hosted HTML weekly production calendars | `{YYYY-MM-DD}-production-calendar-v6.html` |
| `dashboards/single-topic/` | `Graehamwatts/online-content` (same sister repo) | Hosted HTML per-topic production dashboards | `{YYYY-MM-DD}-{slug}-production.html` |
| `outputs/calendar-data/` | `Graehamwatts/skills` (this repo, gitignored) | Machine-readable JSON — weekly planning data, used by future runs | `calendar-{YYYY-MM-DD}.json` |

**If you are writing HTML for a human to view in browser → `online-content/dashboards/{weekly-calendars,single-topic}/` (push to the sister repo).**
**If you are writing JSON for a future skill run to read → `outputs/calendar-data/` (stays local in skills repo, gitignored).**

> **Naming history:** The dashboards folders previously lived under `cma-reports/blog-dashboards/` (single folder, both file types mixed). Renamed and split 2026-05-01 — `cma-reports` repo retired in favor of `online-content`, and `blog-dashboards/` split into two cleaner subfolders to make the weekly-vs-single-topic distinction obvious from the filesystem.

The single-topic dashboard reads `outputs/calendar-data/calendar-{YYYY-MM-DD}.json` to pull the matching Opportunity Score for Rule 13's Scoring Architecture Panel. Without this file, Table A renders as "—" with an "ad-hoc topic" note.

---

## JSON Schemas

### 1. `outputs/ideation-raw-{ts}.json` (Phase 2 raw scrape output)

Raw Apify dataset, unfiltered. No schema changes allowed — this mirrors Apify's response.

```json
[
  {
    "id": "...",
    "parsedId": "...",
    "url": "https://www.reddit.com/r/...",
    "username": "...",
    "title": "...",
    "communityName": "r/...",
    "createdAt": "...",
    "numberOfComments": 0,
    "upVotes": 0,
    "body": "...",
    "comments": [ ... ]
  }
]
```

### 2. `outputs/ideation-topics-{ts}.json` (Phase 2 filtered output)

Phase 2's filter criteria applied. This is what content-calendar consumes.

```json
{
  "generated_at": "ISO8601",
  "source_platform": "reddit",
  "filter_config": {
    "subreddits": [...],
    "time_window": "last_7d",
    "min_upvotes": 5
  },
  "topics": [
    {
      "title": "...",
      "url": "...",
      "subreddit": "...",
      "upvotes": 0,
      "comments": 0,
      "funnel_relevance": 5,
      "local_specificity": 5,
      "engagement_velocity": 5,
      "content_gap_fit": 5,
      "filter_decision": "keep" | "drop",
      "drop_reason": "noise" | "off-topic" | "saturated" | null,
      "notes": "..."
    }
  ]
}
```

Filter axes (0-5 each) are for FILTERING, not scoring. They do not sum to an Opportunity Score.

### 3. `outputs/calendar-data/calendar-{YYYY-MM-DD}.json` (weekly plan)

```json
{
  "week_of": "YYYY-MM-DD",
  "generated_at": "ISO8601",
  "goal": "lead_gen" | "audience_growth" | "listing_launch" | "market_education" | "balanced",
  "funnel_mix": { "tofu": 0.40, "mofu": 0.30, "bofu": 0.30 },
  "topics": [
    {
      "slug": "epa-homicide-free-story",
      "title": "East Palo Alto Two Years Homicide-Free — What It Means For Home Values",
      "day": "Monday",
      "scheduled_date": "YYYY-MM-DD",
      "primary_format": "YouTube Long",
      "funnel_tier": "MOFU",
      "ghl_keyword": "EPA",
      "pillar": 5,
      "market": "EPA",
      "primary_angle": "community-milestone-home-value",
      "opportunity_score": {
        "performance_signal": 4,
        "search_demand": 5,
        "audience_intent": 4,
        "competitive_gap": 5,
        "timeliness": 5,
        "total": 23,
        "threshold_status": "must_create",
        "weighted_total": 24.4,
        "weighting_applied": "lead_gen"
      },
      "priority_axes": {
        "business_priority": 4.4,
        "brand_priority": 4.6,
        "engagement_priority": 4.4,
        "note": "Derived readouts, not separate scores. See content-calendar SKILL.md Step 9 for formulas."
      },
      "time_decay_band": "breaking_48hr" | "weekly_window" | "seasonal_4wk" | "evergreen",
      "time_decay_note": "Story broke April 17; ship by April 21 or lose news window.",
      "topic_conflict": false,
      "conflict_group": null,
      "source_badges": ["src-news", "src-gsc", "src-perf"],
      "justification_notes": "...",
      "user_override": null
    }
  ],
  "cut_topics": [
    {
      "slug": "...",
      "title": "...",
      "opportunity_score": { "total": 11, "threshold_status": "skip" },
      "cut_reason": "..."
    }
  ]
}
```

**Field notes:**
- `weighted_total` = base `total` × Goal Clarifier re-weighting (see `content-calendar/SKILL.md` Step 8 table). The base total is the unweighted 25-pt score; the weighted total is what actually ranks topics. Both are stored for transparency.
- `priority_axes` are READOUTS, not separate scores. Formulas: `business_priority` = weighted_avg(Performance Signal ×0.3, Search Demand ×0.35, Audience Intent ×0.35). `brand_priority` = weighted_avg(Competitive Gap ×0.5, Timeliness ×0.3, Local Relevance ×0.2). `engagement_priority` = weighted_avg(Performance Signal ×0.6, Timeliness ×0.4).
- `time_decay_band` is SEPARATE from the Timeliness score. A `breaking_48hr` topic pins to Monday/Tuesday regardless of ranking. Evergreen topics can be rescheduled across weeks.
- `topic_conflict: true` means this topic shares `pillar + market + primary_angle` with another topic in the same `topics[]` list. `conflict_group` is a shared integer across conflicting topics. Graeham picks one or splits the angles.
- `user_override` captures Graeham's manual reshuffling. Shape: `{ "original_rank": 3, "final_rank": 1, "reason": "..." }`. Null if no override.
- `previously_shipped_this_week` (top-level array) — list of topics shipped in the preceding week. Populated from `outputs/calendar-data/calendar-{PREVIOUS_WEEK}.json`. The weekly-calendar-builder validates that NO current-week topic slug matches a previously-shipped slug (raises ValueError if duplicate detected). Rendered as an "Already Shipped" collapsible section on the weekly dashboard so Graeham can see what not to repeat.
- `previously_shipped_week_of` (top-level string) — date stamp of the preceding week's calendar, used in the Already Shipped section header.

### 4. `outputs/scored-topics-{ts}.json` (Phase 3 Intent Score output)

```json
{
  "generated_at": "ISO8601",
  "topic_slug": "epa-homicide-free-story",
  "intent_score": {
    "inquiry_type_match": 4,
    "intent_matrix_position": 3,
    "intent_matrix_cell": "CONSIDERATION (MOFU)",
    "source_confirmation": 5,
    "source_platforms": ["Google PAA", "Reddit", "Nextdoor"],
    "emotional_temperature": 4,
    "emotional_band": "moderate",
    "local_relevance": 5,
    "local_band": "hyperlocal",
    "base_total": 21,
    "freshness_adjustment": -1,
    "freshness_detail": "Same market (EPA) used 2x in last 2 weeks: -1. No angle overlap.",
    "final_total": 20,
    "threshold_status": "ships"
  },
  "ctar_recommendation": "Comment EPA for the homicide-free impact report"
}
```

### 5. `outputs/research-{topic-slug}-{ts}.json` (Phase R per-topic research)

See `content-creation-engine/SKILL.md` → Phase R for the full schema. Summary: topic-matched MLS stats, GSC queries, news/permits, social signal, competitor coverage, Reddit signal. **No scoring fields.**

### 6. `references/topic-history.json` (rolling 4-week history)

Consumed by Phase 2 (for exclusion lists) and Phase 3 (for freshness penalty/bonus). Written by content-calendar after each weekly plan ships.

```json
{
  "updated_at": "ISO8601",
  "retention_weeks": 4,
  "topics": [
    {
      "slug": "...",
      "title": "...",
      "published_date": "YYYY-MM-DD",
      "pillar": "...",
      "angle": "...",
      "market": "EPA",
      "neighborhood": "Woodland Park",
      "funnel_tier": "BOFU",
      "ghl_keyword": "COSTS",
      "final_opportunity_score": 22,
      "final_intent_score": 21
    }
  ]
}
```

---

## Data-Flow Diagram (text form)

```
       ┌─────────────────────────────────────┐
       │  Apify Reddit scrape (Job 1)        │
       │  owner: content-ideation-engine     │
       └──────────────┬──────────────────────┘
                      │ writes ideation-topics-{ts}.json
                      ▼
       ┌─────────────────────────────────────┐
       │  Weekly Opportunity Scoring (Job 2) │
       │  owner: content-calendar            │
       │  inputs: GSC + social perf +        │
       │    Reddit signal + competitor +     │
       │    market context                   │
       │  scoring: 25-pt × 5 criteria        │
       └──────────────┬──────────────────────┘
                      │ writes calendar-{YYYY-MM-DD}.json
                      │ writes {YYYY-MM-DD}-production-calendar-v6.html
                      │
          ┌───────────┴──────────┐ user picks a topic
          ▼                      ▼
┌──────────────────┐   ┌──────────────────────┐
│ Per-Topic        │   │ Intent Classification│
│ Research (Job 4) │   │ (Job 3)              │
│ owner: CCE       │   │ owner: CCE Phase 3   │
│ Phase R          │   │ scoring: 25-pt + ±5  │
└────────┬─────────┘   └──────────┬───────────┘
         │                        │
         └────────────┬───────────┘
                      ▼
       ┌─────────────────────────────────────┐
       │  Single-Topic Dashboard             │
       │  owner: CCE                         │
       │  Scoring Architecture Panel shows   │
       │    BOTH scores (Table A + Table B)  │
       │  Research Data Panel shows Job 4    │
       └──────────────┬──────────────────────┘
                      │ HeyGen render
                      ▼
       ┌─────────────────────────────────────┐
       │  heygen-elevenlabs-renderer         │
       │  outputs: MP4, .meta.json           │
       └─────────────────────────────────────┘
```

---

## What this file is NOT

- **Not a tutorial.** For how to use each skill, read the skill's own SKILL.md.
- **Not the scoring rubric text.** The rubrics live inside each skill — this file documents what flows where.
- **Not a design spec.** For single-topic dashboard rendering, read `content-creation-engine/references/single-topic-dashboard-rules.md` (Rules 1-13). For weekly calendar dashboard rendering, read `content-creation-engine/references/weekly-calendar-rules.md` (Rule 14).

---

## Change Log

- **April 22, 2026** — Initial file. Created during the architectural streamline that consolidated four scoring systems into two (Opportunity + Intent), killed Phase R's 10-pt rubric, renamed Phase 2's "4-axis scoring" to "4-axis filtering," and made the Scoring Architecture Panel mandatory on every single-topic dashboard.
- **April 23, 2026** — Architecture v2: added `time_decay_band`, `priority_axes`, `topic_conflict`, `user_override`, and `weighted_total` fields to calendar schema. Added Rule 14 (weekly-calendar-rules.md) for calendar dashboard transparency. Content-calendar SKILL.md Steps 8-14 rewritten to cover re-weighting, priority-axes computation, time-decay classification, conflict detection, override capture, and handoff to content-creation-engine.
- **April 23, 2026** (later) — Added cross-week deduplication: `previously_shipped_this_week` and `previously_shipped_week_of` fields in calendar schema. weekly-calendar-builder.py validates no current topic matches a previously-shipped slug (raises ValueError if duplicate). Renders Already Shipped collapsible section on dashboard. topic-history.json is now actively populated by each weekly plan (both weeks April 20 and April 27 tracked).
