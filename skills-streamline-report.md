# Skills Streamline Audit — April 21, 2026

Comprehensive walk through every skill in the `skills/` folder, looking for
the same kind of stylesheet-stacking / layered-patch / scope-overlap issues we
just resolved on the single-topic dashboards.

## TL;DR

The skills folder is mostly clean. The ONE serious cleanup target was the
patch-script proliferation in `scripts/`, which is now resolved (deprecated
patches moved to `scripts/_deprecated/`, single canonical `unify_final.py`
remains). A few minor follow-ups documented below — all low-priority.

## Skills inventory

26 skills total. None have stylesheet stacking inside their SKILL.md. None
have layered patches like the dashboards did.

| Skill | SKILL.md lines | Health |
|---|---|---|
| cinematic-hooks | 220 | clean |
| cma-generator | 277 | clean |
| content-calendar | 483 | minor: stale Apr dates |
| content-creation-engine | 716 | minor: stale Apr dates, broken shared-references link |
| disclosure-analyzer | 295 | clean |
| docx | 590 | clean |
| ghl-crm-audit | 471 | clean |
| github-repo-analyzer | 365 | clean |
| github-skill-sync | 281 | clean |
| heygen-elevenlabs-renderer | 151 | clean |
| heygen-video | 134 | clean |
| html-email | 235 | clean |
| newsletter-generator | 150 | clean (DRE check passed) |
| off-market-property-search | 238 | clean |
| offer-analyzer | 458 | clean |
| pdf | 314 | clean |
| pptx | 231 | clean |
| remotion | 70 | clean |
| remotion-video | 222 | clean |
| schedule | 40 | clean |
| setup-cowork | 47 | clean |
| skill-creator | 485 | clean |
| social-media-analyzer | 645 | minor: stale Apr dates |
| video-creator | 242 | clean |
| website-builder | 99 | clean |
| xlsx | 291 | clean |

## Issues found + dispositions

### A. scripts/ folder had 9 patch scripts → cleaned ✅

**Before:** `scripts/` contained 6 sequential patch scripts that had each been
applied once during the April 18-21 dashboard iterations. Confusing for any
future maintainer ("which do I run?").

**After:** Moved 6 deprecated patches to `scripts/_deprecated/` with a README
explaining the history. Active `scripts/` now contains only:
- `unify_final.py` — single canonical dashboard post-processor (formerly v2)
- `verify.py` — comprehensive QA across dashboards + URLs + JS syntax
- `heygen_render.py` — submit a render to HeyGen API
- `render_monitor.py` — poll HeyGen + push status JSON to GitHub
- `render_monitor_README.md` — Task Scheduler setup notes

### B. content-creation-engine references shared-references/branding.md (doesn't exist) — minor

SKILL.md line ~44 references `../shared-references/branding.md` for branding
consistency, but `skills/shared-references/` doesn't exist. Either:
1. Create the folder + file with the canonical brand colors / fonts
2. Remove the reference and inline the branding rules into content-creation-engine

Recommend #1 — a single canonical branding.md is the same architectural pattern
as the consolidated stylesheet. Future skills can reference it.

### C. Three skills mention "April 18-20, 2026" in SKILL.md text — minor

`content-calendar`, `content-creation-engine`, and `social-media-analyzer` all
have hard-coded April 18-20 references in their SKILL.md. These are mostly in
"failure mode this prevents" examples (historical context), so leaving them is
fine. If they bug you visually, change to "April 2026" without the day.

### D. content-creation-engine SKILL.md Rule 7 instructs running `unify_final.py`

This is now correct since I just made `polish_v2.py`'s code the new
`unify_final.py`. Sentinel `UNIFIED_FINAL_V2` is what gets applied. No edit
needed unless you want to bump the rule text to mention V2 explicitly.

### E. The canonical builder template still doesn't bake in the unified design

`skills/content-creation-engine/templates/single-topic-dashboard-builder.py`
is 85 KB and produces dashboards in the OLD pre-v5 design. It works because
Rule 7 mandates running `unify_final.py --target <new-file>` after the
builder. That's a workaround, not a real fix. Eventually the builder template
should bake in the unified design natively. **Estimated effort: 90 min.**
Acceptable as-is for now since the workaround is documented and idempotent.

## Recommendations going forward

1. **Single source of truth for visuals:** edit `scripts/unify_final.py`'s
   `CONSOLIDATED_CSS_V2` constant. Never add a second injected stylesheet.

2. **Single source of truth for branding:** create
   `skills/shared-references/branding.md` (item B above) with navy/gold
   palette, DM Sans / Plus Jakarta Sans font specs, and accent rules.

3. **Verification gate on every push:** run `python3 scripts/verify.py`
   before any `git push` of dashboard or email changes. It takes ~5 seconds
   and catches structure regressions before they ship.

4. **When updating any single-topic dashboard,** the canonical workflow is
   now:
   ```
   <make changes>
   python3 scripts/unify_final.py            # apply unified treatment to all 5
   python3 scripts/verify.py                  # confirm green
   git add . && git commit && git push
   ```

5. **When generating a new dashboard for next week's topic,** the workflow is:
   ```
   <run the canonical builder>
   python3 scripts/unify_final.py --target content-calendars/<new-file>.html
   python3 scripts/verify.py
   git add . && git commit && git push
   ```

## What was NOT changed in this audit

- Skill descriptions (frontmatter)
- Skill-specific scripts (heygen_render, render_monitor, etc)
- Newsletter-generator (DRE check was a false-positive — it actually warns
  AGAINST using the old DRE)
- Date references in skill bodies (deemed historical context, safe to keep)

---

Generated April 21, 2026 by automated skills audit.
