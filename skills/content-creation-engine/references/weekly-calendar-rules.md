# Weekly Calendar Dashboard Rules

> **Rule 14 of the content system** (pairs with Rules 1-13 in `single-topic-dashboard-rules.md`, which govern per-topic dashboards). These rules govern the weekly calendar HTML at `online-content/dashboards/weekly-calendars/{YYYY-MM-DD}-production-calendar-v6.html`. April 2026 — added to close the presentation-layer gap that Rule 13 didn't cover.

---

## Rule 14: Weekly Calendar Dashboard Must Be Fully Transparent

The weekly calendar HTML dashboard is the ARTIFACT Graeham reviews to decide what content ships. It MUST expose every decision the system made, every topic that was cut, and every conflict detected — so Graeham can override with full information.

### Required Sections (in this order)

1. **Hero** — Week-of date, Goal Clarifier answer, funnel mix, total topics selected / total candidates scored.

2. **Top Recommendations (ranked, expanded)** — 4-7 topic cards, sorted by `opportunity_score.weighted_total` descending. Each card shows:
   - Rank (#1, #2, ...) AND `user_override` annotation if applicable ("moved from #3 → #1, reason: ...")
   - Title + slug
   - Scheduled day + `time_decay_band` badge (`breaking_48hr` in red, `weekly_window` in amber, `seasonal_4wk` in blue, `evergreen` in gray)
   - Funnel tier (TOFU/MOFU/BOFU)
   - Primary format
   - **Opportunity Score breakdown** — 5 criteria rows (Performance Signal, Search Demand, Audience Intent, Competitive Gap, Timeliness), each with score /5 and one-line source note. Show base total AND weighted total if re-weighting was applied.
   - **Priority axes readout** — small horizontal bar for business_priority, brand_priority, engagement_priority (each 0-5).
   - **Justification notes** — one paragraph explaining why this topic beat others.
   - **Time-decay note** — "Ship by [date] or lose [window]."
   - **Topic conflict flag** (if `topic_conflict: true`) — red banner: "Shares pillar+market+angle with Topic #N. Pick one or split angles."
   - Link to the single-topic dashboard (Rule 13 compliant) once generated.

3. **Goal Mix Check** — Visual confirmation that the selected topics hit the Goal Clarifier's funnel-mix target. E.g., target 20/30/50 TOFU/MOFU/BOFU, actual 17/33/50. Call out if any drift > 10%.

4. **Cut Topics (collapsed but present)** — All topics that were scored but did NOT make the top 4-7. For each: slug, title, weighted total, threshold status, one-line cut reason. Graeham can scan this to see what was considered and rejected. Use a `<details><summary>` collapsible block — the list is visible but doesn't dominate the view.

5. **Cross-Topic Conflicts Panel** (if any `topic_conflict: true` exist) — Dedicated section at the bottom listing every conflict group, both conflicting topics, and a "Resolve by: (a) pick one, (b) split angles, (c) move one to next week" prompt.

6. **Override Capture Panel** — A section labeled "Graeham's Edits" showing every `user_override` with original rank, final rank, and reason. If no overrides yet, show an empty placeholder: "No overrides yet — tell Claude which topics to swap, drop, or add."

7. **Footer** — Week of, Goal Clarifier answer, generation timestamp, data freshness (how old is each of the 5 data sources), "V6 + Rule 14 compliant" stamp.

### Rendering Requirements

- No hidden scores. Every topic's per-criterion scoring is visible by default (collapsed is OK for cut topics only).
- Weighted total displayed beside base total if re-weighting was applied, with weighting factor called out (e.g., "24.4 weighted (×1.3 lead_gen boost on Performance Signal + Audience Intent)").
- `time_decay_band` is ALWAYS visible as a colored badge. Breaking-news topics (`breaking_48hr`) render with a red border around the whole card so they're impossible to miss.
- Conflict flags render with a red banner; user_override annotations render with a gold banner.
- All cut topics listed (no silent drops).
- Links to single-topic dashboards resolve if those dashboards exist; show "Not yet generated" placeholder if not.

### Interaction Model

The HTML is a read-only artifact — it does NOT have interactive "swap" or "approve" buttons. Graeham reviews it in-browser, then tells Claude (in chat) what to change. Claude writes the changes into the JSON, regenerates the HTML, and the updated dashboard is ready on the next refresh.

Overrides are captured as:
```
"user_override": { "original_rank": 3, "final_rank": 1, "reason": "faster to ship" }
```

These persist in the JSON and propagate to the HTML on next generation.

### Why This Rule Exists

Prior weekly calendar HTMLs showed the selected topics but NOT the cut ones, NOT the conflict detection, NOT the priority axes readouts, and NOT override history. Graeham could see WHAT was recommended but not WHY one topic beat another OR what was considered and rejected. Rule 14 makes the full decision process visible so Graeham can override with context, and so next week's planner can learn from the override history captured in the JSON.
