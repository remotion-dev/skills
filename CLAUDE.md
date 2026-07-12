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

The `02015066` blocklist entry above exists because of a real incident on 2026-04-29 (a wrong-DRE leak into a published client offer report). **Read `skills/shared-references/dre-leak-incident-log.md`** for the full root-cause writeup and the still-open audit gap (the tripwire doesn't yet cover the `online-content` repo). The enforcement rule itself is already stated above and doesn't require reloading this history every session.

## graphify (optional, on-demand only)

This project has a knowledge graph at `graphify-out/` covering the `scripts/` and `.py`/`.js`-style code in this repo (most of this repo is SKILL.md/reference markdown, which the graph doesn't meaningfully help with — don't reach for it there).

Use it ONLY when doing genuine code-relationship archaeology across script files — e.g. "how do these scripts call each other," "what depends on this function." It is NOT a required first step for normal file reads or greps; there are no automatic hooks enforcing it, by design, so it doesn't tax routine skill/doc reads.

- `graphify query "<question>"`, `graphify path "<A>" "<B>"`, `graphify explain "<concept>"` — scoped subgraph queries, cheaper than a broad grep when the question really is about code structure.
- After modifying `scripts/` code, run `graphify update .` to keep the graph current (AST-only, no API cost).

**Staleness check (mandatory before trusting any graphify query result — applies to every graphed folder, not just this repo):** before answering from a graph query, check whether `graphify-out/needs_update` exists in that folder. This check is free (just a file existence check). If the flag is present, the graph may be stale — do NOT answer from it silently. Either (a) read the specific file in question directly instead of trusting the graph, or (b) tell the user the graph is stale for this folder and ask whether to run a full refresh (paid) before answering. Never present a graph-derived answer as current without this check.
