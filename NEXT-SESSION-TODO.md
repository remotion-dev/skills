# Next Session — Pickup Plan

**Written:** May 12, 2026 (late night session)
**Author:** Last night's Claude — for tomorrow's Claude (or Graeham reading this)
**Context to re-load:** `Skills/skills/shared-references/skill-deprecation-protocol.md` + this file.

---

## ⚡ START HERE — One command, then everything else unblocks

```powershell
cd "C:\Users\Graeham Watts\Documents\Claude\Skills"
.\cleanup-and-commit.ps1
```

The script:
- Fixes the broken git state in both repos (`Skills/.git/index.lock`, `Online Content/.git/index` corrupt)
- Deletes the 3 confirmed-stale items (`graeham-watts-skills/` folder, `graeham-watts-skills.plugin`, `devini-claude-watch-transcript.md`)
- Pulls both repos
- Stages all of last night's SKILL.md edits
- Shows you the diff, asks `YES` before pushing
- Pushes if you confirm

**Until this runs, nothing else can push to GitHub.** Repo state stays inconsistent without it.

---

## ✅ What was finished last night

| Item | Where |
|---|---|
| Anti-zombie protocol doc (6 rules, deletion checklist, zombie detector, 4 case studies) | `skills/shared-references/skill-deprecation-protocol.md` |
| `ghl-crm-audit/SKILL.md` rewritten — PIT direct primary, Windsor parallel/backup, n8n removed | `skills/ghl-crm-audit/SKILL.md` |
| `integrations.md` GHL section rewritten + "Last Updated" stamp | `skills/shared-references/integrations.md` |
| Zombie refs to deleted `video-script-creation-engine` fixed in 2 skills | `vaibhav-template`, `watts-motion-graphics` |
| Absorption notes added to both `content-calendar` (receiver) and `social-media-analyzer` (sender) | both SKILL.md tops |
| Cleanup + commit + push script written | `Skills/cleanup-and-commit.ps1` |
| Attribution brief SKILL.md files updated to PIT-direct path (n8n removed) | `Scheduled/daily-attribution-brief/`, `Scheduled/friday-attribution-review/` |

---

## 🎯 Tomorrow's priorities (in order)

### 1. Run the cleanup script (blocks everything else)

See ⚡ section above. ~60 seconds.

### 2. THE BIG ONE — Absorb `social-media-analyzer` into `content-calendar`

This is the focused work for tomorrow. **Follow `skill-deprecation-protocol.md` top-to-bottom** — that's the whole point of writing the protocol.

**Source:** `skills/social-media-analyzer/SKILL.md` (644 lines, V12 dashboard architecture, 7 tabs, multi-source data validation, competitor research, LLM-vs-SEO video recs, weekly JSON storage pattern)

**Target:** `skills/content-calendar/SKILL.md` (currently 718+ lines, weekly planning + topic scoring)

**Both skills already have absorption notes locked in at the top** — those guide the merge.

**Concrete steps (mirror the protocol's Deletion Checklist):**

1. [ ] Confirm content-calendar can absorb 100% of analyzer's capabilities (no gaps). Sections to bring over:
    - STEP 0 Connection Health Check
    - Data Collection (Windsor + Apify + GHL multi-source strategy)
    - YouTube Shorts blind spot handling
    - Data Validation rules (Never Fabricate, Cross-Validate, Verify Totals, Check Missing, Caption QA)
    - 7-tab dashboard structure (V12 actions-integrated-with-data design)
    - Trending & comparison requirements (week-over-week JSON storage)
    - Status ratings (🟢🟡🔴⚪)
    - Top performers / CRM intelligence sections
    - Competitor research (3-tier scraping, Apify + Supadata + Chrome fallback)
    - Organic SEO vs LLM Search optimization framework
2. [ ] Add merged sections to content-calendar/SKILL.md as a new "PERFORMANCE ANALYSIS LAYER" mega-section. Place BEFORE the weekly scoring sections (so the scoring uses the analytics as input — matches the actual data flow).
3. [ ] Update content-calendar's frontmatter `description:` to include all of analyzer's trigger phrases (social media analytics, post performance, engagement metrics, etc.) so Claude's skill router catches them after analyzer is gone.
4. [ ] Update content-calendar's Scope Boundary section — it currently says "Rearview Mirror = social-media-analyzer"; rewrite to say "this skill now handles both Rearview Mirror (was social-media-analyzer, absorbed May 2026) AND Weekly Planning (always was this skill)."
5. [ ] Replace the "Upcoming absorption" note at the top of content-calendar/SKILL.md with the actual Rule 4 absorption note: `> **Absorbed YYYY-MM-DD:** social-media-analyzer was merged into this skill. All capabilities (list...) now live here. skills/social-media-analyzer/ was deleted in the same commit.`
6. [ ] Run cross-reference scan: `grep -rln "social-media-analyzer" Skills/skills/` — every hit outside content-calendar's absorption note must be updated to point to content-calendar.
7. [ ] Update `shared-references/integrations.md` Per-Skill Integration Map: replace `social-media-analyzer` row with the absorbed capabilities under `content-calendar`.
8. [ ] Check `Scheduled/weekly-social-media-report/SKILL.md` — likely references social-media-analyzer; update to content-calendar.
9. [ ] Check `Scheduled/social-report-manual-run/SKILL.md` and `Scheduled/run-social-report-now/SKILL.md` — same.
10. [ ] `git rm -r skills/social-media-analyzer/` — same commit as the content-calendar update.
11. [ ] Commit message: `consolidate: absorb social-media-analyzer into content-calendar (deletes skills/social-media-analyzer/)`
12. [ ] Push immediately.

**Estimated time:** 60-90 minutes if focused. Don't bake other work into this commit.

### 3. Build the GitHub Action workflows for attribution briefs

The attribution brief SKILL.md files were updated last night to use the PIT direct via GitHub Action — but no Action workflows exist yet. Need to actually create them.

**To create in `Graehamwatts/online-content`:**

- `.github/workflows/daily-attribution-brief.yml` — cron `15 7 * * 1-5` (7:15am Mon-Fri PT) + `workflow_dispatch`
- `.github/workflows/friday-attribution-review.yml` — cron `0 16 * * 5` (4pm Fri PT) + `workflow_dispatch`

**Python scripts (live in the repo):**

- `scripts/attribution_daily.py` — reads PIT, pulls 24h window from GHL, generates HTML brief, emails
- `scripts/attribution_weekly.py` — reads PIT, pulls 7d window, generates HTML dashboard, emails

**Repo secrets to add (Settings → Secrets and variables → Actions):**

- `GHL_PIT` — from `ghl-pit.txt` line 1
- `GHL_LOCATION_ID` — `6wuU3haUH7uNeT20E3UZ`
- `GH_DASHBOARD_PAT` — fine-grained PAT with `contents:write` + `actions:write`
- Gmail SMTP credentials OR a SendGrid/Mailgun key for email delivery

**Use the `pipeline-dashboard` skill's existing GitHub Action as the template** (per its SKILL.md lines 60-65, that pattern is established).

### 4. Update skill-creator with the deprecation protocol tripwire

`skills/skill-creator/SKILL.md` needs a new section near the top:

```markdown
## Merge / Absorb / Consolidate Operations

If the user asks to merge, absorb, consolidate, deprecate, or replace skill A with skill B:

1. STOP. Read `../shared-references/skill-deprecation-protocol.md` first.
2. Follow the Deletion Checklist top-to-bottom — same-commit deletion of `skills/A/` is non-negotiable.
3. If you cannot execute Rule 2 (same-commit deletion) for any reason (permissions, ongoing work, etc.), surface the obstacle to the user instead of writing a partial merge.
```

### 5. Online Content/ cleanup (low-priority — flag for user)

Empty directories I left alone (need user's call):

- `Online Content/scheduled-tasks-backup/daily-attribution-brief/` (empty)
- `Online Content/scheduled-tasks-backup/friday-attribution-review/` (empty)
- `Online Content/skill-references/weekly-listing-update/` (empty)

Ambiguous:
- `Online Content/emails/` — still has 5 HTML files despite the today's commit `3bb6b1e "Rename emails/ to online-content/"`. Need to determine if the rename was supposed to move these or if emails/ is the canonical name and the commit message was misleading. **Ask Graeham first.**

### 6. Push the 2 unpushed skills

These exist locally but have never been pushed to GitHub:

- `skills/pipeline-dashboard/` — the canonical PIT architecture skill, important to push
- `skills/video-research-engine/` — also needs first-time push
  - **Bug to fix before push:** has a malformed subdir named `C:UsersGraeham WattsDocumentsObsidianProp OS` — that's a Windows path that got created as a literal directory name. Delete that subdir, then push.

The cleanup script will catch these on `git add -A` once git state is clean.

### 7. Schedule the quarterly skills audit task

Per `skill-deprecation-protocol.md` Rule 6, create a Cowork scheduled task `skills-audit` that runs quarterly. Prompt = "Run the Zombie Detector checklist from `skill-deprecation-protocol.md`. Report findings. Don't fix anything — surface them."

Easy way: use the `schedule` skill. First quarterly fire date: ~August 12, 2026.

---

## 📋 Deferred backlog (not for tomorrow, but track them)

- **Audit Online Content/ structure** — emails/ vs dashboards/ vs newsletters/ vs cmas/ vs runbooks/. May have its own zombie problem.
- **Reddit official API** — was applied for in April; check status via Chrome (per integrations.md line 240).
- **County records scrapers** (Santa Clara + San Mateo) — pending wiring, listed in integrations.md.
- **Apify Zillow scraper verification** — listed as "Stale / Needs Verification" in integrations.md.

---

## 🛡 Discipline check — read before any merge

When you (or a session) tries to do another consolidation tomorrow, the rule is:

1. Read `skill-deprecation-protocol.md` first.
2. Same commit = the absorption + the deletion. No follow-ups.
3. Cross-reference scan must return zero hits outside the receiver's absorption note.
4. Push immediately. Don't let local-only changes accumulate (that's how `graeham-watts-skills/` happened).

---

## File index — where last night's work lives

```
Skills/
├── cleanup-and-commit.ps1          ← Run this FIRST tomorrow
├── NEXT-SESSION-TODO.md            ← This file
└── skills/
    ├── shared-references/
    │   ├── skill-deprecation-protocol.md   ← NEW — the prevention layer
    │   └── integrations.md                 ← UPDATED — GHL section + Last Updated
    ├── ghl-crm-audit/
    │   └── SKILL.md                        ← REWRITTEN — PIT primary
    ├── content-calendar/
    │   └── SKILL.md                        ← absorption note added (receiver)
    ├── social-media-analyzer/
    │   └── SKILL.md                        ← absorption note added (sender, slated for deletion)
    ├── vaibhav-template/
    │   └── SKILL.md                        ← zombie refs fixed
    └── watts-motion-graphics/
        └── SKILL.md                        ← zombie refs fixed

Scheduled/
├── daily-attribution-brief/SKILL.md        ← PIT path locked in (needs GH Action built)
└── friday-attribution-review/SKILL.md      ← PIT path locked in (needs GH Action built)
```

---

Sleep well. Pick this up cold tomorrow — the absorption notes and the protocol make it self-guiding.
