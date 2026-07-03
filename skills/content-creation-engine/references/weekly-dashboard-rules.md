# Weekly Calendar Dashboard Rules (9, 10, 11)

Referenced from SKILL.md. Load this file only when actually building or editing a **weekly calendar** HTML dashboard (`online-content/dashboards/weekly-calendars/`). Not needed for single-topic dashboards (see `references/single-topic-dashboard-rules.md` for those) or for ideation/scoring/research phases.

## Rule 9: No Orphan Internal Links (Non-Negotiable)

Every `href=""` attribute in a generated dashboard HTML file MUST point to one of:
1. An in-page anchor (`href="#section-id"`) where the target id exists in the same file, OR
2. A JavaScript no-op (`href="#"` paired with `onclick`) for setView/setFilter buttons, OR
3. A fully-qualified external URL on a domain that's actually reachable (citation links, social posts, etc.), OR
4. A relative URL to another file that is ALSO pushed to GitHub in the same commit

**Forbidden:** any `href=` to a sibling HTML file that doesn't exist on GitHub Pages. This was the root cause of the "blog tab 404s" failure on 2026-05-15 — the `-all-humanizer.html` linked to `2026-05-11-blogs.html`, `-videos.html`, `-research.html`, and `-all.html` (the four older variant files) but only the humanizer variants were ever pushed. Every audience tab 404'd silently on the live URL.

**Pre-push audit (mandatory):**

```bash
# Extract all hrefs from the dashboard HTML
grep -oE 'href="[^"]*"' dashboard.html | sort -u > /tmp/hrefs.txt

# For each href that points to a relative .html file:
# 1. Check it exists in /tmp/online-content-clone/dashboards/weekly-calendars/
# 2. If missing on the remote and not being added in this commit, FAIL the push

# For each href that's a fully-qualified external URL:
# 3. (optional) HEAD request to confirm 2xx, flag any 404
```

The pre-push audit must run as part of every weekly calendar build. If any `href=` points to a missing local file, STOP and either fix the link or include the target file in the same commit.

**Failure mode this prevents:** Zombie file references. Files that exist locally in Documents\Claude but never made it to GitHub get cross-linked from pushed files, creating tabs/buttons that 404 on the live URL while looking fine in local preview.

## Rule 10: Visual Dashboard Sections Required (Non-Negotiable)

Every weekly calendar MUST include the following visual dashboard sections, in this order, at the TOP of the file (before the Calendar grid and per-topic sections):

1. **Hero + audience-tab nav** — header bar, week date range, 5-button filter row (Research / Diagram / Calendar / Video / Blog) wired to `setView()` and `data-audience=""` attributes
2. **Run-note banner** — any blockers (e.g., "Apify blocked at firewall, pivoted to WebSearch") so the production team knows what was fresh vs derived
> **AUTOMATED GATES (added 2026-06-09):** three former prose-only rules are now scripts in `scripts/` — run them, don't re-derive them. (1) `weekly_overlap_check.py` BEFORE pushing any weekly calendar (exit 1 = overlap, review required). (2) `verify_output_brand.py <files>` BEFORE publishing any output (exit 2 = blocked brand value, never ship). (3) `update_topic_history.py` AFTER a calendar ships, so the Phase 3 freshness penalty has data. Routing between sibling skills: read `../shared-references/routing-decision-tree.md`.

3. **Research — Live Data Layer** — source cards showing which 8 data sources ran live, blocked, or partial. Color-coded: green = live, red = blocked
4. **Performance Signal — What's Actually Working** — **ApexCharts brushable time-series ONLY** (Chart.js is forbidden for these charts — it lacks brush interaction):
   - Instagram Activity Over Time — area chart, last 26 weeks (100 posts via Windsor MCP `instagram` connector — Composio Meta Graph API is retired, do not use), dual axis (likes + posts), brush slider below for drag-to-zoom
   - YouTube Activity Over Time — area chart, last 14 weeks (50 videos via YouTube Data API v3), dual axis (views + videos), brush slider below
   - Engagement Rate Per Post Per Week — line chart, avg per-piece for IG + YT, strips out posting-frequency effect, brush slider below
   - Each chart is a PAIR: a main chart (`#xxxChartMain`, height 300) + a brush slider (`#xxxChartBrush`, height 100, marginTop -6) wired via `brush: { target: 'xxxMain', enabled: true }, selection: { enabled: true, ... }`
   - Library: `<script src="https://cdn.jsdelivr.net/npm/apexcharts@4.5.0"></script>` (or later compatible version)
   - The brush pattern lets users drag a window on the bottom slider to zoom the main chart to any time range. This is the canonical "slide it across time" interaction Graeham expects.
   - **Top 5 lists** (YouTube Top 5 last 99 videos, IG Top 5 last 20 posts) — render as data tables, not charts. Sortable by views / likes / engagement.
5. **Full Weekly Research Data panel** — collapsible accordion containing the 7 mandatory data tables that back the week's topic picks:
   a. Instagram Own-Channel Performance — last 25 posts with caption excerpt, likes, comments, pattern match column (gold-highlighted rows = match week's content patterns)
   b. YouTube Own-Channel Performance — last 15 videos with views, likes, comments, pattern match column
   c. Google Search Console Topic-Targeted Queries — query, impressions (last 7d), clicks, position, trend WoW, day-the-query-maps-to
   d. Reddit Demand Signals — subreddit, thread title, upvotes, comments, topic cluster (star the day-of-week match)
   e. Zillow Q&A — question, page, asked count (last 30d), day-the-question-maps-to
   f. MLS Pull — metric, current month, year-ago, YoY delta (with trend-up/trend-down color coding)
   g. Convergence — Why Each Day Picked — day, topic, sources-converged list, score out of 25 (star the highest-converging day)
   Plus a Macro Rates & Permits bullet list (30Y fixed rate, Fed Funds, county permits, notable ADU permits) and a DataForSEO SERP Queue status note.
6. **Freshness Constraints + Citations** — 4-week topic history check, blocked angles, citation URLs (external)
7. **Diagram — How We Built This (10-Step Data Pipeline)** — clickable nodes showing data flow: 4 INPUT nodes → 3 ANALYSIS nodes → 3 OUTPUT nodes
8. **Calendar — Week of [date range]** — 5 day-cards with funnel-tier color coding (TOFU/MOFU/BOFU), GHL keyword chips, click-to-expand topic details
9. **Video Content — All 5 Topics** — per-topic article cards with Copy SSML + Copy Production Prompt buttons
10. **Blog Content — All 5 Topics** — per-topic article cards with Copy Blog Brief + Copy Production Prompt buttons

**Failure mode this prevents:** Calendars shipped without the visual research dashboard look like prompt dumps and provide no analytical context. The production team can't tell which topics are backed by which data signal, and Graeham can't review the run quality at a glance. Two real production failures led to this rule:

1. On 2026-05-15 the `-all-humanizer.html` shipped without sections 4 (Performance Signal charts) and 7 (Pipeline Diagram), making it look incomplete next to the prior week's production-calendar.html.
2. Later that same night the rebuilt production-calendar shipped with Chart.js line charts (no brush) and only a 6-card Live Data Layer with no underlying data tables. Graeham flagged it: "the graphs you created are different from the graphs in the previous version — should be the ones where you can slide across time" and "missing a lot of the research data." The fix required transplanting the ApexCharts brushable charts + 7 data tables from `2026-05-11-research.html`. **This rule's section 4 now mandates ApexCharts brushable (not Chart.js) and section 5 enumerates the 7 required data tables explicitly so the omission can't repeat.**

## Rule 11: Single Canonical File Pattern (Non-Negotiable)

A weekly calendar is ONE file, not four. The deprecated pattern was:
- `2026-05-11-all.html` — full view
- `2026-05-11-blogs.html` — blog-track filter
- `2026-05-11-videos.html` — video-track filter
- `2026-05-11-research.html` — research-only filter

That pattern is **forbidden** going forward. The four files were not in sync (different sizes, different prompt content), the audience tabs cross-linked between them (creating the Rule 9 violations), and maintaining four parallel files for the same week multiplied the surface area for bugs by 4x.

The canonical pattern is **ONE file per week**:
- `2026-MM-DD-production-calendar.html` (where MM-DD is the Monday the week starts)

Audience filtering happens **via in-page JavaScript** using:
- `data-audience="blog all"` attributes on each section
- A `setView('blog')` function that hides/shows sections matching the selected view
- The "Show everything" link resets to `setView('all')`

This means clicking "Blog Track" doesn't navigate to a sibling file — it just filters the current file. No 404 risk. No drift between variants. One file to maintain, one URL to share, one place to verify before pushing.

**Existing deprecated files** (`2026-05-11-all.html`, `-blogs.html`, `-videos.html`, `-research.html`, and their `-humanizer` siblings) should be removed from `Graehamwatts/online-content` in a cleanup commit. They remain locally for archival but should not be referenced or linked to from any new file.

**Failure mode this prevents:** Variant proliferation. Each variant file is another place where the prompt data can drift, where href targets can break, and where a humanizer update has to be applied 4x instead of 1x.
