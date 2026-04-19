# Single-Topic Production Dashboard — Strict Rules

This document locks in the dashboard pattern produced on April 18, 2026 during the EPA Two Years Homicide-Free build. Every future single-topic dashboard MUST follow these rules. They exist because every rule was violated at least once during that build, producing visible bugs Graeham caught.

Reference implementation: `content-calendars/2026-04-18-epa-two-years-homicide-free-production.html`
Template builder: `skills/content-creation-engine/templates/single-topic-dashboard-builder.py`

---

## Rule 1: Python-Only HTML Generation

NEVER use `cat > file << 'EOF'` bash heredoc for HTML output. Bash silently escapes `!` in HTML comments to `\!`, leaking `<\!-- comment -->` as visible text.

ALWAYS write HTML via Python:
```python
from pathlib import Path
Path("content-calendars/YYYY-MM-DD-slug-production.html").write_text(html, encoding="utf-8")
```

VERIFY after write: `grep -c '<\\!--' file.html` — must return 0.

**Failure captured:** v1 dashboard had 20+ visible `<\!--` strings because it was written via bash heredoc.

---

## Rule 2: Three-Library Architecture

Every dashboard loads THREE JavaScript objects into `window`:

1. `window.PROMPT_LIBRARY` — keys: format IDs, values: full Claude/ChatGPT prompts (with Agent Identity + Fair Housing + DATE/YEAR QC + Timing Self-Check + Voice + Topic + AEO + Key Facts + GHL CTA). Used by `copyPrompt()`.
2. `window.CONTENT_LIBRARY` — keys: format IDs, values: pre-generated production-ready content. Used by `copyContent()`.
3. `PAIRINGS` (Python build-time only) — map of format → companion format for paired buttons (e.g., `yt-long-pt1` → `yt-long-pt2`).

Keys MUST match across all three libraries. Builder asserts this at generation time.

---

## Rule 3: Dual-Button Pattern (Non-Negotiable)

Every format panel has TWO buttons:

1. **Copy Content** (gold solid, primary action) — copies `CONTENT_LIBRARY[key]` (the production-ready deliverable). Paste directly into YouTube description / Instagram caption / Gmail / etc.
2. **Copy Prompt** (gold outline, secondary action) — copies `PROMPT_LIBRARY[key]` (the full context-loaded prompt). Paste into Claude/ChatGPT to regenerate a fresh version.

Specific formats get a THIRD paired button (see Rule 4). No format ever has only one button.

---

## Rule 4: Paired Buttons for Voice ↔ Production Formats

`yt-long-pt1` (script + SSML, voice side) MUST have a paired "Copy Production Content" button that copies `yt-long-pt2` (B-roll prompts, editing notes for Jason, AI video prompts for Seedance, YouTube SEO, 3 alt hooks).

Purpose: user grabs script + production package from the same panel without clicking over to another tab.

The paired button uses `--purple` background (not gold) so it reads as an Also Grab action, not the primary action.

Future pairings to consider as the system matures:
- `ig-reel-1` → `ig-carousel` (same story, different format)
- `blog` → `email` (long-form + newsletter distribution)

---

## Rule 5: Show Full Research Data Expandable Panel

Every single-topic dashboard MUST include a "Show Full Research Data" toggle button that expands a panel with ALL 8+ research sources:

1. Google Search Console — top queries table with clicks/impressions/CTR/position
2. Instagram Performance — post-level table (last 30 days, top 12 by reach)
3. Facebook Performance — summary cards (impressions, posts, best/worst)
4. YouTube Performance — video-level table
5. MLS Market Data — stat cards for primary markets
6. Local News & Events — bulleted list with clickable source links
7. Trigger Events (tech layoffs etc.) — bulleted list with dates
8. Topic History — table showing prior + planned topics
9. Data Pull Metadata — timestamp, sources hit, windows, gaps

Panel is CLOSED by default. Button is navy (not gold — research data is UI chrome, not brand).

---

## Rule 6: Gold is Brand — Use Sparingly

`--gold` (#C5A258) appears ONLY on:
- `copy-big` buttons (Copy Content primary action)
- `hero-score` pill (Opportunity Score hero badge)
- `.score-c .sv` values (3/3, 2/2 scoring breakdown)
- `.hook-tag` (PICKED tag on alt hook cards)
- `.cta-card h3` (CTA section heading)
- Small hero decorative accent (circle overlay at `::after`)

Gold NEVER appears on: timing card border, intelligence stack card borders, flow card active states, picked hook card border, use-in callouts, table headers, shot number circles, data toggle buttons.

Maximum ~10 instances of `var(--gold)` per dashboard. If more, you violated the rule.

---

## Rule 7: Design Language Consistency

All dashboards use:
- **Palette:** `--navy` #1B2A4A, `--gold` #C5A258, `--teal` #00695c, `--purple` #6a1b9a, `--green` #2e7d32, `--red` #c62828, `--orange` #e65100
- **Fonts:** `DM Sans` (body), `Plus Jakarta Sans` (headings and buttons)
- **Radius:** `--radius: 12px` for cards, 8px for buttons, 6px for small elements
- **Shadow:** `--shadow: 0 2px 8px rgba(0,0,0,0.04)` as the default
- **Border:** `--border: #e2e5ea`

Copy these tokens verbatim from the template. Don't invent new ones per dashboard.

---

## Rule 8: Required Sections (In This Order)

Every single-topic dashboard contains, in order:

1. Hero (gradient navy background, topic title, meta pills, generated-date footer)
2. How-To panel (3-step dashboard usage instructions)
3. Timing Card (verified calculation with math shown — no generic defaults)
4. Fair Housing Compliance banner (green, passed/failed status)
5. Intelligence Stack (6+ source cards)
6. Show Full Research Data toggle + expandable panel
7. Opportunity Score Breakdown (4 score cards showing per-criterion math)
8. Calendar Integration banner (how this slots into existing weekly calendar)
9. Content Derivatives header + flow-map cards (14 formats)
10. Panel container (14 panels, one active by default)
11. Shot List (12-shot table for production crew)
12. 3 Alternate Hooks with PICKED tag
13. Auto-Render Hand-off card (HeyGen command + voice/avatar IDs)
14. Footer (brand + generation metadata + sources)

Missing any section = dashboard is incomplete.

---

## Rule 9: Timing Self-Check Required

Every timing calculation on the dashboard MUST show the math:
```
{word_count} words × 150 WPM × 1.15 pause buffer = {minutes}
```

Never default to generic durations like "8-10 min". The prompt must also instruct the external AI to calculate timing before emitting.

---

## Rule 10: Screenshot Verification Before Push

After every build, VERIFY visually before the final push:

**Preferred:** Screenshot-loop from `skills/website-builder/references/screenshot-loop.md` (if sandbox supports headless Chromium).

**Fallback:** Push to GH Pages first, then use Claude-in-Chrome MCP to navigate to the live URL and screenshot.

**Fallback to fallback:** If browser tools fail (sandbox restrictions), ask the user to visually verify and list specific items to check.

NEVER declare a build done without visual verification. Code review catches structure; screenshots catch the visible bugs.

---

## Rule 11: Commit Message Format

```
Single-Topic Dashboard: {slug} — {one-line summary}
```

Example: `Single-Topic Dashboard: epa-two-years-homicide-free — v4.1 paired production button + full research data`

---

## Rule 12: Self-Check Block Before Declaring Done

Before the final Send-User-Message declaring the dashboard complete, run and include this checklist in the response:

- [ ] PROMPT_LIBRARY, CONTENT_LIBRARY, PAIRINGS all have matching keys (asserted in builder)
- [ ] Every format has Copy Content (gold) + Copy Prompt (gold outline)
- [ ] YT Long Pt 1 has Copy Production Content paired button (purple)
- [ ] Show Full Research Data button present + expandable panel has 8+ sections
- [ ] Gold usage count ≤ 10 instances of `var(--gold)` in the rendered HTML
- [ ] Navy is used for general UI chrome (timing card border, intelligence stack, flow cards, etc.)
- [ ] HTML comment escape bug: `grep -c '<\\!--' file.html` returns 0
- [ ] Timing calculation shows word-count math (no generic "~8-10 min")
- [ ] Fair Housing compliance banner passed
- [ ] Intelligence Stack has 6+ source cards with clear source attribution per finding
- [ ] Shot list has all 12 shots with durations and setup notes
- [ ] 3 alt hooks present with PICKED tag on recommended hook
- [ ] Auto-Render Hand-off card includes voice ID, avatar ID, render command
- [ ] Footer includes DRE number and all data sources
- [ ] Screenshot-loop OR live-URL verification executed before push
- [ ] Commit message follows format

Ship the dashboard only after all 16 items verify.
