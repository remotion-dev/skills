# Data Contracts — Content System

> **Shared reference across `content-creation-engine`, `content-calendar`, `content-ideation-engine`, and `heygen-elevenlabs-renderer`.** This file is the single source of truth for folder names, file naming, JSON schemas, and the two-score model. Updated April 2026 during the scoring-architecture streamline.

---

## The Four-Job Model

The content system has four distinct jobs. Each one has a specific owner skill and a specific output. Jobs are NOT interchangeable, and their outputs must NOT be merged.

| # | Job | Owner | Output file |
|---|---|---|---|
| 1 | Ingest raw audience signal from Reddit | `content-creation-engine/references/phases/content-ideation-engine/` (Phase 2) | `outputs/ideation-raw-{ts}.json`, `outputs/ideation-topics-{ts}.json` |
| 2 | Score topics for WEEKLY coverage (Opportunity Score, 25 pts) | `content-calendar` | `content-calendar-data/calendar-{YYYY-MM-DD}.json` + `content-calendars/{YYYY-MM-DD}-production-calendar-v6.html` |
| 3 | Classify BOFU intent of ONE topic (Intent Score, 25 pts + freshness ±5) | `content-creation-engine/references/phases/bofu-scorer/` (Phase 3) | `outputs/scored-topics-{ts}.json` |
| 4 | Pull per-topic research citations (no scoring) | `content-creation-engine` Phase R | `outputs/research-{topic-slug}-{ts}.json` |

**Rule of thumb for routing:** "Which topic should I cover?" → Job 2. "What's the intent of this one topic?" → Job 3. "What stats/quotes back this specific topic?" → Job 4. "What are people talking about on Reddit?" → Job 1.

---

## Folder Naming (IMPORTANT — they look similar, they are NOT the same)

Both folders live at the top of the `Graehamwatts/skills` repo. The singular/plural difference is intentional.

| Folder | Purpose | Files inside |
|---|---|---|
| `content-calendars/` (plural) | Hosted HTML dashboards — one per week OR one per topic | `{YYYY-MM-DD}-production-calendar-v6.html` (weekly), `{YYYY-MM-DD}-{slug}-production.html` (per-topic) |
| `content-calendar-data/` (singular-data suffix) | Machine-readable JSON — weekly planning data | `calendar-{YYYY-MM-DD}.json` |

**If you are writing HTML for a human to view in browser → `content-calendars/`.**
**If you are writing JSON for a future run to read → `content-calendar-data/`.**

The single-topic dashboard reads `content-calendar-data/calendar-{YYYY-MM-DD}.json` to pull the matching Opportunity Score for Rule 13's Scoring Architecture Panel. Without this file, Table A renders as "—" with an "ad-hoc topic" note.

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

### 3. `content-calendar-data/calendar-{YYYY-MM-DD}.json` (weekly plan)

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
      "opportunity_score": {
        "performance_signal": 4,
        "search_demand": 5,
        "audience_intent": 4,
        "competitive_gap": 5,
        "timeliness": 5,
        "total": 23,
        "threshold_status": "must_create"
      },
      "source_badges": ["src-news", "src-gsc", "src-perf"],
      "justification_notes": "..."
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
- **Not a design spec.** For dashboard rendering, read `content-creation-engine/references/single-topic-dashboard-rules.md`.

---

## Change Log

- **April 22, 2026** — Initial file. Created during the architectural streamline that consolidated four scoring systems into two (Opportunity + Intent), killed Phase R's 10-pt rubric, renamed Phase 2's "4-axis scoring" to "4-axis filtering," and made the Scoring Architecture Panel mandatory on every single-topic dashboard.
