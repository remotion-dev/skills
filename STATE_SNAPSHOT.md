# Stable State Snapshot — Week of April 27, 2026

**Tag:** `v2026.04.27-stable`
**Commit:** `05a75b6` (architecture fixes) on top of `e12f0fd` (identity tripwire)
**Verified:** April 24, 2026
**Verified by:** Triple-pass section-by-section audit (8 sections)

This document is the source of truth for what "working" looks like. If anything drifts from this state, refer back here to identify regressions.

## Section 1 — Identity tripwire (root-cause fix for DRE creep)

| Check | Result |
|---|---|
| `skills/shared-references/identity.json` exists | OK (1207 bytes) |
| `scripts/verify_brand_identity.py` exists and executable | OK |
| `.git/hooks/pre-push` installed and runs the tripwire | OK |
| Manual tripwire run | PASS — 0 blocked values |
| `branding.md` points to `identity.json` as source of truth | OK |

**What it does:** every push runs the tripwire. If any blocklisted value (the old/incorrect DRE listed in `identity.json` or any future blocklisted value) appears anywhere outside `identity.json`, the push fails with file paths printed. No more silent regressions.

## Section 2 — index.html (main dashboard)

| Check | Result |
|---|---|
| Headline | "This Week's Content Plan" |
| Week marker | "Week of April 27 – May 3, 2026" |
| Day-tile links | 5/5 present and resolve |
| Calendar link | resolves |
| DRE shown | `01466876` (correct) |

## Section 3 — 5 day views

Per file: 15 format cards, 15 master prompt templates, 15 master + 15 SSML + 15 Production buttons (45 buttons), 1 copyPromptMode JS function, 1 status-flip CSS, 0 broken research links, 5 unique research stub links, 0 old single-button regressions.

| Day | File | Size |
|---|---|---|
| Mon | day-2026-04-27-mon-peninsula-rent-vs-own.html | 69,746 |
| Tue | day-2026-04-28-tue-peninsula-bidding-wars.html | 62,189 |
| Wed | day-2026-04-29-wed-hidden-equity-refi-vs-sell.html | 62,442 |
| Thu | day-2026-04-30-thu-woodland-park-772-units.html | 62,809 |
| Fri | day-2026-05-01-fri-ab1482-rental-exemption.html | 63,914 |

## Section 4 — v7 weekly calendar

| Check | Result |
|---|---|
| File exists | OK (21,757 bytes) |
| 5 topic cards | OK with correct titles |
| All 5 dashboard links resolve | OK |
| DRE shown | `01466876` |
| Old EPA Under $1M references | 1 — intentional (swap audit note) |

## Section 5 — calendar JSON

| Check | Result |
|---|---|
| Topics | 5/5 with correct slugs and dashboard links |
| Funnel mix actual | 0/20/80 (T/M/B) vs target 20/30/50 |
| Funnel field populated on every topic | OK |
| previously_shipped_this_week | empty (intentional — first week of new system) |

Topic-by-topic:
- BOFU `peninsula-rent-vs-own-math-2026` → BUY → Mon
- BOFU `peninsula-bidding-wars-are-back` → OFFERS → Tue
- BOFU `peninsula-homeowner-equity-refi-vs-sell-2026` → EQUITY → Wed
- MOFU `woodland-park-development-epa` → EPA → Thu
- BOFU `ab1482-2026-amendment-landlords` → 1482 → Fri

## Section 6 — topic-history.json (v2.0 schema)

| Check | Result |
|---|---|
| Schema version | 2.0 |
| Registers documented | history, in_production |
| history weeks | 1 (week_of 2026-04-27, 5 topics) |
| in_production register | 1 entry: `epa-homes-around-1m-shot-2026-04` |
| in_production has `exclusion_radius` field | OK |

## Section 7 — research stubs

25/25 files present. 5 sources × 5 days. 0 orphans, 0 broken references.

## Section 8 — skills directory

38 skills present. Legacy `video-script-creation-engine` deleted. Critical files all present:

- `skills/shared-references/identity.json` (source of truth)
- `skills/shared-references/branding.md` (points at identity.json)
- `skills/content-creation-engine/SKILL.md` (Rules 1-15 documented including new Rule 15: Two-Register Freshness)
- `skills/content-creation-engine/templates/prompts-library-builder.py` (now writes 3-button block — regression fixed at the source)
- `scripts/verify_brand_identity.py` (the tripwire)
- `.git/hooks/pre-push` (the enforcement)

## Architecture changes that prevent regressions

1. **Single source of truth for identity** — `identity.json` instead of 71 hardcoded copies
2. **Pre-push tripwire** — push fails if blocked values reappear
3. **Two-register topic history** — gatekeepers see shot-but-unposted content
4. **Builder scripts updated** — `prompts-library-builder.py` writes 3 buttons by default, so any future regeneration preserves them

## How to verify this state in the future

```bash
cd /path/to/skills
python3 scripts/verify_brand_identity.py    # tripwire
python3 - <<'PY'                             # full audit
import re, json
from pathlib import Path
issues = []
for d in sorted(Path('.').glob('day-2026-*.html')):
    h = d.read_text()
    if h.count('class="format-card"') != 15: issues.append(f"{d.name}: not 15 cards")
    if 'function copyPromptMode' not in h: issues.append(f"{d.name}: JS missing")
    if 'fc-status.copied' not in h: issues.append(f"{d.name}: status flip CSS missing")
    for href in re.findall(r'href="(?!http|#)([^"]+)"', h):
        clean = href.split('#')[0].split('?')[0]
        if clean and not Path(clean).exists(): issues.append(f"{d.name} broken: {href}")
print(f"{'CLEAN' if not issues else f'{len(issues)} ISSUES'}: {issues}")
PY
```

Both must report PASS / CLEAN. If 