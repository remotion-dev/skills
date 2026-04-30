# READ THIS FIRST — Onboarding for Claude sessions touching this repo

## Brand identity — the ONE rule that keeps getting violated

**Single source of truth for Graeham's brand identity:** `skills/shared-references/identity.json`

Read that file before writing ANY content that includes:
- DRE number (Graeham's individual salesperson DRE is `01466876`)
- Brokerage name
- Contact info (phone, email, website)
- Markets served

**Do NOT hardcode brand details from memory or training.** California real estate marketing has multiple plausible-looking DRE numbers (brokerage DRE, salesperson DRE, archived numbers from old brokerages). It's tempting to type one in from prior context. **Don't.** Always read identity.json first.

**Specifically prohibited:** the value `02015066` has been blocklisted seven separate times. It is NOT Graeham's DRE, NOT Intero Real Estate's brokerage DRE (per Graeham's confirmation), and has no legitimate use anywhere in this repo or in outputs. If you find it in your context window, in a CMA template, in a contact strip, or anywhere else — **delete it. Do not propagate it.**

## Enforcement

`scripts/verify_brand_identity.py` audits the entire repo against `identity.json`'s blocklist. It runs:

1. As a local pre-push git hook (advisory — only runs on machines that have it installed).
2. As a GitHub Actions workflow on every push to main (server-side enforcement — see `.github/workflows/verify_brand_identity.yml` if it exists).

**Run the tripwire manually before pushing:**
```bash
python3 scripts/verify_brand_identity.py
```

If it fails, **fix the file paths it lists before pushing.** Do not bypass.

## Other state-keeping rules

- `skills/content-creation-engine/references/topic-history.json` has TWO registers: `history` (posted topics) and `in_production` (shot-but-unposted). Read BOTH for freshness checks. See Rule 15 in `skills/content-creation-engine/SKILL.md`.
- Day views at root of repo (`day-2026-MM-DD-*.html`) follow the schema documented in `STATE_SNAPSHOT.md`. Don't break it.
- The current weekly calendar is `content-calendars/2026-04-27-production-calendar-v7.html`. Index.html links to all 5 day views.

## Tag of last known-good state

`v2026.04.27-stable` — if anything regresses, compare against this tag.
