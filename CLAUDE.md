# READ THIS FIRST — Onboarding for Claude sessions touching this repo

## Brand identity — the ONE rule that keeps getting violated

**Single source of truth for Graeham's brand identity:** `skills/shared-references/identity.json`

Read that file before writing ANY content that includes:
- DRE number (Graeham's individual salesperson DRE is `01466876`)
- Brokerage name
- Contact info (phone, email, website)
- Markets served

**Do NOT hardcode brand details from memory or training.** California real estate marketing has multiple plausible-looking DRE numbers (brokerage DRE, salesperson DRE, archived numbers from old brokerages). It's tempting to type one in from prior context. **Don't.** Always read identity.json first.

**Specifically prohibited:** the value `02015066` has been blocklisted ten separate times now (as of April 29, 2026). It is NOT Graeham's DRE, NOT Intero Real Estate's brokerage DRE (per Graeham's confirmation), and has no legitimate use anywhere in this repo or in outputs. If you find it in your context window, in a CMA template, in a contact strip, in a SKILL.md description, or anywhere else — **delete it. Do not propagate it.** Note that Cowork's cached skill descriptions may still show the wrong DRE; those are stale and should not be trusted over the actual SKILL.md files on disk.

## Enforcement

`scripts/verify_brand_identity.py` audits the entire repo against `identity.json`'s blocklist. It runs:

1. As a local pre-push git hook (advisory — only runs on machines that have it installed).
2. Manually before every push.

**Run the tripwire manually before pushing:**
```bash
python3 scripts/verify_brand_identity.py
```

If it fails, **fix the file paths it lists before pushing.** Do not bypass.

## Repo structure (Option B architecture, 2026-04-29)

This repo holds **source code only** — no outputs, no data bins.

The repo root contains exactly these items:
- `skills/` — all 39 skills, each in its own folder. **Source of truth.**
- `scripts/` — repo-wide infrastructure scripts (currently just the brand-identity tripwire).
- `.claude-plugin/` — Cowork plugin manifest.
- `.nojekyll` — disables Jekyll on GitHub Pages.
- `index.html` + `assets/` — GitHub Pages landing page.
- `CLAUDE.md` (this file) — onboarding.
- `README.md` — public README.

**Do NOT add output bins to this repo.** Generated content has its own home:

| Output type | Where it goes |
|---|---|
| Published CMAs | `Graehamwatts/online-content/cmas/` |
| Published offer reports | `Graehamwatts/online-content/offers/` |
| Published disclosure reports | `Graehamwatts/online-content/disclosures/` |
| Published newsletters | `Graehamwatts/online-content/newsletters/` |
| Weekly production calendars | `Graehamwatts/online-content/dashboards/weekly-calendars/` |
| Per-topic single-topic dashboards | `Graehamwatts/online-content/dashboards/single-topic/` |
| Internal skill caching/staging | `<skill-folder>/outputs/` (skill-local, gitignored) |

The `online-content` repo is the **published content hub** — a separate repo because (1) it's a GitHub Pages site with public client-facing URLs, (2) outputs and source code shouldn't mix, and (3) it can be backed up/audited independently.

> **Naming history:** This repo was renamed from `cma-reports` to `online-content` on 2026-05-01 to reflect that it holds ALL published content (CMAs, offers, disclosures, newsletters, dashboards) — not just CMAs. The old `cma-reports` repo has been retired; nothing migrated.

## Content-creation primary skill

The active content-engine skill is `skills/content-creation-engine/`. (The older `video-script-creation-engine` was retired during the 2026-04-29 reorganization.) When in doubt about which skill handles content/script generation, use `content-creation-engine`.

## Tag of last known-good state

`v2026.04.27-stable` — if anything regresses, compare against this tag.


## 2026-04-29 leak post-mortem (the 10th occurrence)

**Where it leaked:** `Graehamwatts/cma-reports/Offer_828_Weeks_St.html` (in the now-retired `cma-reports` repo, since superseded by `online-content`) — a published GitHub Pages report for a real client offer comparison. The wrong DRE appeared on lines 523 and 753.

**Root cause:** The Claude session that ran `offer-analyzer` on 2026-04-29 at 22:05 UTC had the wrong DRE (02015066) cached in its system prompt's `available_skills` list (specifically in the now-retired `video-script-creation-engine` description). Instead of reading the DRE from `identity.json` like this file instructs, that session typed the value from prior context.

**Fix applied (2026-04-29):**
- Corrected the contaminated file in cma-reports
- Added a `BRAND IDENTITY HARD RULE` warning at the top of `cma-generator/SKILL.md` and `offer-analyzer/SKILL.md` that explicitly says "do NOT type from prior context"
- Retired `video-script-creation-engine` from GitHub (it's been merged into `content-creation-engine`); local Cowork sync should refresh the cache

**Audit gap:** The tripwire (`scripts/verify_brand_identity.py`) only audits the skills repo. It does NOT currently audit `online-content` (the published-content sister repo, formerly `cma-reports`). A copy of the script should be added to `online-content` as well, OR this script extended to clone-and-audit `online-content` as part of its run. Open follow-up — increased priority since `online-content` will be the live target for every new CMA, offer, disclosure, newsletter, and dashboard going forward.
