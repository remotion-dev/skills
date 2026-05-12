---
name: pipeline-dashboard
description: "Live lead lifecycle dashboard for Graeham's GoHighLevel CRM. Visualizes the entire lead attribution system as a cyclic Sankey diagram (Sources → Active Pipelines → Outcomes → back to Past Client → Referrals/Repeat). Tracks all 7 GHL pipelines, 36 stages, opportunity dollar value, lead source attribution, and Adrian's coordinator activity. Hosted on graehamwatts.github.io/online-content/dashboards/pipeline/. Refreshes via dashboard button + Mon/Fri auto-cron. Use ANY time the user mentions: pipeline dashboard, lead dashboard, GHL dashboard, pipeline visualization, lead attribution, Sankey, lead flow, pipeline health, weekly pipeline report, Monday pipeline email, Friday pipeline email, refresh dashboard, run pipeline report, Adrian activity, coordinator activity, past client engine, referral tracking, repeat business tracking, or anything related to viewing/refreshing/reporting on the lead lifecycle in GHL."
---

# Pipeline Dashboard — Lead Lifecycle Visualizer

A live dashboard that visualizes Graeham's complete lead lifecycle from GoHighLevel as a cyclic Sankey flow, with macro/micro zoom, individual lead drill-down, Adrian's coordinator activity, and past-client engine metrics. Hosted on GitHub Pages, refreshes via button or Mon/Fri cron.

---

## What This Skill Does

Pulls live GHL data via the LeadConnector API (PIT auth), aggregates it into a structured JSON, pushes the JSON + dashboard HTML to `Graehamwatts/online-content/dashboards/pipeline/`, and sends Monday + Friday email digests.

The dashboard itself is a static HTML page hosted at `https://graehamwatts.github.io/online-content/dashboards/pipeline/` that reads the JSON file and renders:

1. **Top scorecards**: Today / 3-day / Week / Month / YTD / Lifetime — counts + pipeline $ value
2. **Zoomable timeline**: 5Y → 1Y → 6M → 3M → custom range (ECharts dataZoom)
3. **Cyclic Sankey diagram**: Sources → Active Pipelines → Outcomes, with closed deals visually feeding the Past Client Pool which loops back as Referral / Repeat Business sources
4. **Past Client Engine panel**: Total past clients, referrals YTD/lifetime, repeat business, avg years between transactions, re-activation signals
5. **Lead Source Attribution**: Volume × conversion % × $ value per source
6. **Adrian Activity Panel**: Calls, contacts attempted, conversations, appointments set, notes logged, tasks completed — benchmarked against daily targets, color-coded vs target
7. **Aging Leads Alert**: Leads stuck in a stage past threshold, sorted by oldest first
8. **Heat Map**: Day-of-week × hour activity (when leads convert best, when Adrian is most active)
9. **Drill-down lead table**: Searchable, filterable, every contact with their full lifecycle path

---

## Architecture

```
┌─ skills/pipeline-dashboard/ (THIS skill, in skills repo) ─┐
│   • SKILL.md — instructions                                │
│   • scripts/refresh.py — pull GHL → aggregate → push JSON  │
│   • scripts/send_monday_email.py                           │
│   • scripts/send_friday_email.py                           │
│   • scripts/deploy.py — pushes index.html to online-content│
│   • templates/index.html — the dashboard                   │
│   • templates/email-monday.html                            │
│   • templates/email-friday.html                            │
│   • references/data-contract.md — JSON schema              │
│   • references/visual-spec.md — design system              │
│   • outputs/ (gitignored — local cache + last run logs)    │
└──────────────────────────────────────────────────────────────┘
                       │
                       │ Python pushes via direct GitHub API (no Composio)
                       │ using ghp_ token from C:\Users\Graeham Watts\Documents\GitHub Credentials\pat-skills-and-pages.txt
                       ▼
┌─ Graehamwatts/online-content/dashboards/pipeline/ ────────┐
│   • index.html — the dashboard                            │
│   • data.json — refreshed each run                        │
│   • Live URL:                                             │
│     https://graehamwatts.github.io/online-content/        │
│         dashboards/pipeline/                              │
└────────────────────────────────────────────────────────────┘
                       │
                       │ Triggers (3 paths into the same refresh logic):
                       ▼
┌─ Trigger sources ─────────────────────────────────────────┐
│ 1. GitHub Action cron — Mon 7am PT, Fri 5pm PT            │
│    (.github/workflows/pipeline-dashboard.yml in           │
│     online-content repo)                                  │
│ 2. workflow_dispatch — fired by dashboard "Refresh" button│
│    via fine-grained PAT scoped only to this workflow      │
│ 3. Manual — `python scripts/refresh.py` from skill folder │
└────────────────────────────────────────────────────────────┘
```

**Why no n8n / no Composio:**
- n8n is a third-party orchestrator — replaced by GitHub Actions (one fewer service)
- Composio is a wrapper around GitHub API — replaced by direct GitHub Contents API calls in Python
- Only third parties remaining: GHL itself (data source), GitHub (hosting + Actions). Both unavoidable.

---

## Credentials

Read at runtime from local files (NEVER hardcoded, NEVER committed — gitignored):

- **GHL PIT**: `C:\Users\Graeham Watts\Documents\Claude\Skills\ghl-pit.txt`
  - Line 1: PIT token (starts `pit-`)
  - Line 2: Location ID (`6wuU3haUH7uNeT20E3UZ`)
- **GitHub PAT**: `C:\Users\Graeham Watts\Documents\GitHub Credentials\pat-skills-and-pages.txt`
  - Line 1: PAT (starts `ghp_`)

In the GitHub Action, the same values come from repo Secrets:
- `GHL_PIT`
- `GHL_LOCATION_ID`
- `GH_DASHBOARD_PAT` (a separate fine-grained PAT scoped to: contents:write on online-content + actions:write for workflow_dispatch)

---

## GHL API Endpoints Used

| Endpoint | Purpose |
|---|---|
| `GET /opportunities/pipelines?locationId={id}` | All 7 pipelines + 36 stages |
| `GET /opportunities/search?location_id={id}` | All opportunities (paginated) |
| `POST /contacts/search` | All contacts (paginated) |
| `GET /users/?locationId={id}` | Team members for activity attribution |
| `GET /contacts/{id}/notes` | Notes per contact for activity tracking |
| `GET /contacts/{id}/tasks` | Tasks per contact for activity tracking |
| `GET /conversations/search?locationId={id}` | Conversations (calls/SMS/email metadata) |
| `GET /locations/{id}/customFields` | Custom fields for source attribution |

API base: `https://services.leadconnectorhq.com`
Auth header: `Authorization: Bearer pit-...`
Version header: `Version: 2021-07-28`

---

## Pipeline Structure (as of skill creation, May 2026)

| Pipeline | Role |
|---|---|
| New Leads (6 stages) | Entry funnel |
| Buyer Pipeline (10 stages) | Active buyer track |
| Seller Pipeline (9 stages) | Active seller track |
| Investor/Flipper (1 stage) | Specialty track |
| Past Buyers (4 stages) | Post-close cycle |
| Past Sellers (4 stages) | Post-close cycle |
| Lost deal — already bought/sold (2 stages) | Loss tracking |

The skill must NOT hardcode pipeline IDs. It pulls them fresh each run from `/opportunities/pipelines`.

---

## Adrian's Daily Activity Targets (v1 — recalibrate after week 1)

| Metric | Target |
|---|---|
| Dials | 60 |
| Contacts attempted | 25 |
| Conversations had | 5 |
| Appointments set | 1-2 |
| Notes logged | 15 |
| Tasks completed | 10 |

Activity panel color-codes: green ≥100% target, yellow 70-99%, red <70%.

---

## Brand Identity

**ALWAYS read identity.json at runtime — never hardcode.** Source: `skills/shared-references/identity.json`. The DRE is `01466876`. The blocklist value MUST never appear in any output.

Visual spec (matches existing GHL audit + CMA branding):
- Background: `#1a2744` (deep slate)
- Cards: `#1e2d4d`
- Accent: `#2d4278`
- Critical: `#e74c3c`
- Warning: `#f39c12`
- Healthy: `#27ae60`
- Past Client (special): `#9b59b6` (purple — the asset that compounds)

Typography: clean sans-serif. Numbers large + bold + color-coded. Sankey bands use gradient fills shifting from source color to outcome color.

---

## Phases

When invoked, work through these phases in order:

### Phase 1: Verify Credentials
- Read `ghl-pit.txt` from `C:\Users\Graeham Watts\Documents\Claude\Skills\` (GoHighLevel PIT — not yet centralized)
- Read `pat-skills-and-pages.txt` from `C:\Users\Graeham Watts\Documents\GitHub Credentials\` (GitHub PAT)
- Make a single test call to `/opportunities/pipelines` to verify PIT works
- If either credential file is missing or invalid, stop and tell the user exactly what's missing

### Phase 2: Pull Fresh Data
Run `scripts/refresh.py` which:
1. Reads PIT + Location ID
2. Pulls all opportunities (paginated, 100 per page)
3. Pulls all contacts (paginated, 100 per page)
4. Pulls pipelines, users, custom fields, conversations
5. For each contact: pulls notes + tasks (rate-limited to respect 100 req/10s GHL limit)
6. Aggregates everything into the data.json schema (see references/data-contract.md)

### Phase 3: Generate Outputs
- Write `outputs/data-{timestamp}.json` (local cache)
- Render `templates/index.html` with the JSON embedded as initial state
- Generate Mon or Fri email HTML if appropriate trigger

### Phase 4: Deploy
- Push `index.html` + `data.json` to `Graehamwatts/online-content/dashboards/pipeline/` via GitHub Contents API
- Use the GitHub PAT directly (no Composio)
- Verify push succeeded by reading the file back

### Phase 5: Send Email (Mon/Fri only)
- Compose email with embedded mini-Sankey image, scorecard summary, link to dashboard
- Send via Gmail MCP (skill defers to user's already-connected Gmail)
- Recipients: graehamwatts@gmail.com (default — user can add others)

### Phase 6: Verify
- Open the live dashboard URL, confirm it loads + JSON is valid
- Spot-check a few key numbers against raw GHL counts
- Report back to user with summary + dashboard link

---

## Triggers

This skill responds to:

- "Refresh pipeline dashboard" / "update the dashboard" / "run the pipeline report"
- "What's our pipeline look like" — runs full refresh + summarizes inline
- "Send the Monday pipeline email" / "Send the Friday pipeline email"
- "How many leads came in this week"
- Scheduled fires from GitHub Action cron (Mon 7am PT, Fri 5pm PT)
- Webhook fire from dashboard's Refresh button (via workflow_dispatch)

---

## Safety Rules

- NEVER commit credential files (gitignore enforces this)
- NEVER hardcode brand identity (read identity.json)
- NEVER print PIT or GitHub PAT in chat output (read silently, use silently)
- ALWAYS verify GitHub push succeeded before declaring run complete
- If GHL rate limit hit (100 req / 10s): pause + retry with exponential backoff
- If a Mon/Fri cron run fails: send a failure alert email, do NOT silently skip

---

## Open Items (build-time)

- [ ] Confirm Adrian's daily targets with Graeham after first week of real data
- [ ] Verify CORS for graehamwatts.github.io origin (needed for browser-direct Refresh button); if blocked, the button instead triggers GitHub Action via workflow_dispatch
- [x] Referral attribution custom field — CREATED 2026-05-05. Field ID `aCIXKsxuECYRLPw84FAe`, key `contact.referred_by`, type TEXT. Used by Past Client Engine panel.
- [ ] Decide email cadence after week 2 — 7am Monday + 5pm Friday is the v1 default
- [ ] Build training note for Adrian on how to populate the new "Referred By" field on referred leads (so Past Client Engine attribution works)
