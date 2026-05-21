# Skills Audit Report
**Generated:** 2026-05-14
**Audited folder:** C:\Users\Graeham Watts\Documents\Claude\Skills\

## Note on terminology
The original prompt used "DRV"; this audit treats it as **DRE** (California Department of Real Estate license number), matching the canonical field defined in `skills/shared-references/identity.json`.

## Canonical values (from identity.json)
- **DRE:** `01466876` (correct, current)
- **Blocklisted:** `02015066` (the recurring zombie - must never appear except in documentation-exempt files)
- **Doc-exempt files** (legitimately reference the blocklisted value to enforce policy): `CLAUDE.md`, `skills/shared-references/identity.json`, `scripts/verify_brand_identity.py`

## Skill folder inventory
- Total skill folders under `skills/`: 45
- All have valid `SKILL.md`: yes
- Deprecated skills (per CLAUDE.md policy) present: NONE - `video-script-creation-engine`, `social-media-analyzer`, `video-prompt-builder`, `html-email`, `github-skill-sync` all already removed
- `_backup` / `_archive` / `old` / `deprecated` folders inside Skills/: none found

## DRE occurrences scan
| File | Status |
|---|---|
| `Skills/CLAUDE.md` lines 15, 73 | DOC-EXEMPT (policy warning) |
| `Skills/skills/shared-references/identity.json` lines 27, 30, 37 | DOC-EXEMPT (blocklist + audit history) |
| All other content files | CLEAN (0 occurrences) |

## Stray `.skill` bundles outside Skills/
| File | Disposition |
|---|---|
| `Documents/Claude/weekly-listing-update.skill` | ZOMBIE - canonical version is at `Skills/skills/weekly-listing-update/`. Targeted for removal. |

## Recommended canonical version per skill type
All 45 skills under `skills/` are unique; no duplicates. Each folder's own `SKILL.md` is the canonical version.

## Cleanup actions taken in this session
- Patched DRE 02015066 -> 01466876 in:
  - `skills/content-calendar/templates/main-dashboard-builder.py`
  - `skills/shared-references/publishing-via-composio.md`
  - `skills/watts-motion-graphics/references/standing-rules.md`
  - `skills/contract-estimate-builder/SKILL.md`
  - `Online Content/dashboards/attribution/2026-05-12-daily.html`
- Pushed cleaned state to `Graehamwatts/skills` main (commit `384b595`)
