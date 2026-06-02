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

---

## Rule 15: Main Dashboard Structure (Locked Canonical Layout — Added 2026-05-14)

Added after 5 iterations of dashboard drift on the week of 2026-05-11. This rule mandates the canonical structure for the weekly Main Dashboard so the format is consistent every Monday and Claude cannot regress to a sub-view-only or audience-tab-missing layout.

### Required Structure (in this exact order)

1. **Hero banner** — `<header class="hero">` with H1 "Main Dashboard — Week of {date range}", funnel mix subtitle, meta chips (engine version, generation date, brokerage, lead-gen ratio). NEVER title the page "Production Calendar" or "Weekly Calendar" — this is the MAIN DASHBOARD.

2. **Sticky audience-tabs nav** — exactly 5 tabs in order: Research / Diagram / Content / Video Content / Blog Content. Each with `.aud-btn .aud-{key}` class. Tab keys: `research`, `diagram`, `content`, `video`, `blog`. Default view: `content`. Uses `setView()` JS pattern lifted from `all.html` reference. URL hash routing: `#view-{key}`.

3. **Run-note banner** (always visible) — `<div class="banner">` documenting any data-pull anomalies this run (Apify firewall, etc.).

4. **Research section** (`data-audience="research all"`) — Live Data Layer (green/red cards per source), Performance Signal (YouTube channel snapshot + Instagram top performers table from live Composio pulls), Freshness Constraints box, Source Citations list. NEVER bare; should always show what was pulled this run.

5. **Diagram section** (`data-audience="diagram all"`) — 10-step pipeline rendered as 3 flow rows (4 data nodes / 3 intelligence nodes / 3 output nodes). Each node is a clickable button calling `openStep('s{N}')`. Modal opens with rich content per step.

6. **Content section** (`data-audience="content all"`) — 5 day-cards (Mon-Fri) with score pill, title, hook, funnel chip, pillar, market, GHL keyword chip, score breakdown row, data-trail block.

7. **Video Content section** (`data-audience="video all"`) — 5 cards with video deliverables summary + ElevenLabs settings block.

8. **Blog Content section** (`data-audience="blog all"`) — 5 cards with blog deliverables summary + slug + schema notes.

9. **Footer** — DRE# 01466876 + repo links + generation date.

### Required Modal Depth (per pipeline step)

Every pipeline-step modal MUST include:

- **Actual tool slugs** that ran (e.g., `YOUTUBE_GET_CHANNEL_STATISTICS`, not "YouTube API")
- **Actual Composio account names** (e.g., `youtube_manor-maki`, `instagram_carton-palama`)
- **Actual numbers from this run** (subscribers, post counts, engagement counts, dollar amounts, dates)
- **Actual findings** (specific insights like "lifestyle hooks beat RE-direct ~3x")
- **Source citations** with hyperlinks where applicable
- **Clear next-step / output** indicating where this step's output goes

Modals MUST NOT contain:
- Generic skill-config language ("Markets covered: EPA, RWC, PA, MP, SMC")
- Placeholder copy
- Re-statements of the dashboard structure (we're documenting what RAN, not what the dashboard IS)

### Required Bug Fixes (every build)

These three CSS/JS bugs have bitten the build repeatedly. They must be present in every dashboard:

1. **Modal CSS specificity fix:** `.modal-backdrop[hidden] { display: none !important; }` MUST be in the stylesheet. Without this, `.modal-backdrop { display: flex }` overrides the `[hidden]` attribute and the modal pops up empty on page load.

2. **STEP_DATA as JSON:** Build `STEP_DATA` as a Python dict, serialize with `json.dumps(STEP_DATA, ensure_ascii=True)`. NEVER regex-edit JSON strings. Validate with `json.loads()` before write.

3. **HTML entities only for special characters:** Every em-dash, en-dash, smart-quote, middot, ampersand MUST be an HTML entity (`&mdash;`, `&ndash;`, `&rsquo;`, `&ldquo;`, `&rdquo;`, `&middot;`, `&amp;`, `&copy;`). NEVER use literal special characters in the source. This prevents multi-layer UTF-8 mojibake when files are read/written across Windows/Linux boundaries.

### What Must NOT Be on the Main Dashboard

- Companion cards linking to sibling sub-dashboards (Videos Dashboard / Blogs Dashboard / Research Dashboard / All-in-One). These duplicate the 5 audience tabs and confuse the navigation.
- Sub-dashboard sibling files (`{date}-videos.html`, `{date}-blogs.html`, `{date}-research.html`, `{date}-all.html`). Deleted from the repo. The Main Dashboard is THE dashboard for the week.

### Reference Implementation

Reference commit: `https://github.com/Graehamwatts/online-content/commit/3675a988eee7411e2ab5a8b4921ba0655cc0faca` (2026-05-14 v3 canonical build).

Builder script: `skills/content-calendar/templates/main-dashboard-builder.py` (generates the canonical layout from a calendar JSON + analytics JSON input).

### Why This Rule Exists

The week of 2026-05-11 dashboard required 5 iterations to land on the canonical structure. Failure modes encountered: (1) wrong skill used (cached deprecated `video-script-creation-engine` instead of canonical `content-creation-engine`), (2) gutted prior pipeline diagram, (3) overwrote another session's work, (4) empty modal popup on page load (CSS specificity bug), (5) mojibake from prior file's corrupted bytes, (6) wrong DRE leak, (7) TOC pills instead of audience tabs, (8) generic modal content instead of rich analysis, (9) duplicate companion cards leading to conflicting sibling layouts. Rule 15 enumerates each failure with the explicit fix so future Mondays cannot regress.

