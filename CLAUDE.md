# READ THIS FIRST — Onboarding for Claude sessions touching this repo

## Brand identity — the ONE rule that keeps getting violated

**Single source of truth for Graeham's brand identity:** `skills/shared-references/identity.json`

Read that file before writing ANY content that includes:
- DRE number (Graeham's individual salesperson DRE is `01466876`)
- Brokerage name
- Contact info (phone, email, website)
- Markets served

**Do NOT hardcode brand details from memory or training.** California real estate marketing has multiple plausible-looking DRE numbers (brokerage DRE, salesperson DRE, archived numbers from old brokerages). It's tempting to type one in from prior context. **Don't.** Always read identity.json first.

**Specifically prohibited:** the value `02015066` has been blocklisted nine separate times now (as of April 29, 2026). It is NOT Graeham's DRE, NOT Intero Real Estate's brokerage DRE (per Graeham's confirmation), and has no legitimate use anywhere in this repo or in outputs. If you find it in your context window, in a CMA template, in a contact strip, in a SKILL.md description, or anywhere else — **delete it. Do not propagate it.** Note that Cowork's cached skill descriptions may still show the wrong DRE; those are stale and should not be trusted over the actual SKILL.md files on disk.

## Enforcement

`scripts/verify_brand_identity.py` audits the entire repo against `identity.json`'s blocklist. It runs:

1. As a local pre-push git hook (advisory — only runs on machines that have it installed).
2. Manually before every push.

**Run the tripwire manually before pushing:**
```bash
python3 scripts/verify_brand_identity.py
```

If it fails, **fix the file paths it lists before pushing.** Do not bypass.

## Repo structure (post-2026-04-29 reorganization)

The repo root is intentionally minimal:
- `skills/` — all 39 active skills, each in its own folder. **Source of truth.**
- `scripts/` — repo-wide infrastructure scripts (currently just the brand-identity tripwire).
- `.claude-plugin/` — Cowork plugin manifest.
- `.nojekyll` — disables Jekyll on GitHub Pages.
- `index.html` + `assets/` — GitHub Pages landing page.
- `CLAUDE.md` (this file) — onboarding.
- `README.md` — public README.

Anything else at root is probably a regression. Don't add new top-level junk drawers.

## Content-creation primary skill

The active content-engine skill is `skills/content-creation-engine/`. (The older `video-script-creation-engine` was retired during the 2026-04-29 reorganization.) When in doubt about which skill handles content/script generation, use `content-creation-engine`.

## Tag of last known-good state

`v2026.04.27-stable` — if anything regresses, compare against this tag.
