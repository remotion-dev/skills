# Single-Topic Production Dashboard — Strict Rules

This document locks in the dashboard pattern produced on April 18, 2026 during the EPA Two Years Homicide-Free build. Every future single-topic dashboard MUST follow these rules. They exist because every rule was violated at least once during that build, producing visible bugs Graeham caught.

Reference implementation: `online-content/dashboards/single-topic/2026-04-18-epa-two-years-homicide-free-production.html`
Template builder: `skills/content-creation-engine/templates/single-topic-dashboard-builder.py`

---

## Rule 1: Python-Only HTML Generation

NEVER use `cat > file << 'EOF'` bash heredoc for HTML output. Bash silently escapes `!` in HTML comments to `\!`, leaking `<\!-- comment -->` as visible text.

ALWAYS write HTML via Python:
```python
from pathlib import Path
Path("online-content/dashboards/single-topic/YYYY-MM-DD-slug-production.html").write_text(html, encoding="utf-8")
```

VERIFY after write: `grep -c '<\\!--' file.html` — must return 0.

**Failure captured:** v1 dashboard had 20+ visible `<\!--` strings because it was written via bash heredoc.

---

## Rule 2: Three-Library Architecture (Updated April 2026 for Audience-Targeted Buttons)

Every dashboard loads THREE JavaScript objects into `window`:

1. `window.PROMPT_LIBRARY` — keys: format IDs (with audience suffix), values: full Claude/ChatGPT prompts (Agent Identity + Fair Housing + DATE/YEAR QC + Timing Self-Check + Voice + Topic + AEO + Key Facts + GHL CTA + deliverable spec).

   **Key naming scheme:**
   - Non-video formats: `<format>` (e.g., `blog`, `email`, `gmb`, `facebook`, `ig-carousel`)
   - Video formats: TWO keys per format — `<format>-script` and `<format>-production`
     - `yt-short-script`, `yt-short-production`
     - `ig-reel-1-script`, `ig-reel-1-production`
     - `ig-reel-2-script`, `ig-reel-2-production`
     - `tiktok-script`, `tiktok-production`
   - YouTube Long uses pt1/pt2 split: `yt-long-pt1` (script + SSML), `yt-long-pt2` (production package). Both keys exist in PROMPT_LIBRARY (regeneration prompts for each).

   Used by `copyPrompt(key)` and `copyScriptPrompt(format)` / `copyProductionPrompt(format)` JS helpers.

2. `window.CONTENT_LIBRARY` — keys: format IDs (no audience suffix), values: pre-generated production-ready content for the blog producer. Used by `copyContent(key)`.

   Keys: `blog`, `email`, `gmb`, `facebook`, `ig-carousel`, `yt-long-pt1`, `yt-long-pt2`, `yt-short`, `ig-reel-1`, `ig-reel-2`, `tiktok`. (Video formats have ONE content key per format — The blog producer posts the same content regardless of how Peter produces it.)

3. `PAIRINGS` (Python build-time only) — map of format → companion format for cross-references (e.g., `yt-long-pt1` ↔ `yt-long-pt2`, `ig-reel-1` ↔ `ig-carousel`).

Keys MUST match across PROMPT_LIBRARY and CONTENT_LIBRARY for non-script/non-production keys. Builder asserts this at generation time. The script/production sub-keys exist only in PROMPT_LIBRARY (no corresponding content key — they regenerate the script or production package on demand).

---

## Rule 3: Audience-Targeted Button Pattern (Non-Negotiable)

Each format panel has buttons targeted at one of two audiences: **Blog Track** (posts / publishes the content) or **Peter** (produces the video). The button set is determined by format type.

### For non-video formats (Blog, Email, GMB, Facebook, IG Carousel)

Two buttons. Blog Track is the only audience.

1. **Copy Content** (gold solid, primary) — copies `CONTENT_LIBRARY[key]` (post-ready deliverable). Blog Track pastes into the publishing platform.
2. **Copy Prompt** (gold outline, secondary) — copies `PROMPT_LIBRARY[key]` (regeneration prompt). Blog Track pastes into Claude/ChatGPT to regenerate if the first version misses.

### For video formats (YT Long, YT Short, IG Reel #1, IG Reel #2, TikTok)

Three buttons. Blog Track posts the content; Peter produces the video.

1. **Copy Content** (gold solid, primary — Blog Track) — copies `CONTENT_LIBRARY[key]` (post-ready caption/description with hashtags + GHL keyword CTA). Blog Track pastes into the publishing platform.
2. **Copy Script Prompt** (gold outline, secondary — Peter) — copies `PROMPT_LIBRARY[key + "-script"]` (full prompt to regenerate the script + SSML/ElevenLabs XML). Peter pastes into his AI tool to get a fresh, production-ready script.
3. **Copy Production Prompt** (purple solid — Peter) — copies `PROMPT_LIBRARY[key + "-production"]` (full prompt to regenerate the production package: B-roll list, editing notes for Jason, AI video prompts for Seedance/Kling, shot list, transitions, music direction, thumbnail concept). Peter pastes into his AI tool to get the production-side companion to the script.

The two-prompt split for video formats is intentional — Peter regenerates script and production package as separate AI invocations because output length per response can otherwise truncate. Same pattern as the existing YT Long pt1/pt2 split, but applied per format rather than per part.

### Button colors and meaning

- **Gold solid** = Blog Track's primary action (post-ready content)
- **Gold outline** = secondary regeneration / script-side prompt
- **Purple solid** = Peter's production-side prompt
- **Navy** = UI chrome (toggles, expanders, navigation)

Never use gold for non-Blog Track actions. Never use purple for non-Peter actions. The color tells the user whose action it is at a glance.

---

## Rule 4: YouTube Long Pt1 / Pt2 Output Split (Token-Limit Workaround)

YouTube Long is the one format where the production prompt's output is too large for a single AI response (40K-60K characters across 6 deliverables). The Pt1/Pt2 split is the workaround.

`yt-long-pt1` panel (Script + Voice side):
- **Copy Content** (gold) — finished script + SSML for ElevenLabs paste
- **Copy Script Prompt** (gold outline) — regenerates pt1 (script + SSML, ~20-25K chars output)
- **Copy Production Prompt** (purple) — copies the pt2 prompt (production package: editing notes + AI video prompts + YouTube SEO + 3 alt hooks, ~20-25K chars output)

`yt-long-pt2` panel (Production-Package side):
- **Copy Content** (gold) — finished production package
- **Copy Script Prompt** (gold outline) — copies the pt1 prompt (so Peter can regenerate the script if needed)
- **Copy Production Prompt** (purple) — regenerates pt2

In other words: the two panels mirror each other. Both panels show all three buttons. The "primary" button (gold solid Copy Content) gives the panel's deliverable; the other two prompt buttons give Peter access to the companion prompt.

For all other video formats (YT Short, IG Reel, TikTok), the script and production prompts each fit in single AI responses, so no Pt1/Pt2 split is needed — just three buttons on one panel.

### Future pairings to consider as the system matures

- `ig-reel-1` → `ig-carousel` (same story, different format) — content-side pairing, not production-side
- `blog` → `email` (long-form + newsletter distribution) — content-side pairing

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
7. **Scoring Architecture Panel (see Rule 13)** — TWO tables side by side: Opportunity Score (5 rows × 5 pts) and Intent Score (6 rows × 5 pts, including freshness ±5). Both tables fully expanded. No scores hidden.
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
- [ ] Non-video formats (Blog, Email, GMB, Facebook, IG Carousel) have Copy Content (gold) + Copy Prompt (gold outline) — TWO buttons total
- [ ] Video formats (YT Long Pt1+Pt2, YT Short, IG Reel #1, IG Reel #2, TikTok) have Copy Content (gold) + Copy Script Prompt (gold outline, Peter) + Copy Production Prompt (purple, Peter) — THREE buttons total
- [ ] PROMPT_LIBRARY has both `<format>-script` and `<format>-production` keys for every video format
- [ ] Purple buttons appear ONLY on production-side prompts (never on Blog Track-side actions)
- [ ] Show Full Research Data button present + expandable panel has 8+ sections
- [ ] **Scoring Architecture Panel present with BOTH tables (Opportunity + Intent) fully visible, expanded by default, matching Rule 13 spec**
- [ ] Gold usage count ≤ 10 instances of `var(--gold)` in the rendered HTML
- [ ] Navy is used for general UI chrome (timing card border, intelligence stack, flow cards, etc.)
- [ ] HTML comment escape bug: `grep -c '<\\!--' file.html` returns 0
- [ ] Timing calculation shows word-count math (no generic "~8-10 min")
- [ ] Fair Housing compliance banner passed
- [ ] Intelligence Stack has 6+ source cards with clear source attribution per finding
- [ ] Shot list has all 12 shots with durations and setup notes
- [ ] 3 alt hooks present with PICKED tag on recommended hook

---

## Rule 13: Scoring Architecture Panel (Two Scores, Fully Visible)

Every single-topic dashboard MUST render a Scoring Architecture Panel containing BOTH scores side-by-side (desktop) or stacked (mobile). Both tables are expanded by default. **No Show/Hide toggle is allowed** — visibility is mandatory.

### Panel Structure

Section heading: `<h2 class="sh">Scoring Architecture — Why This Topic Ships</h2>`

Section intro (one sentence): `Two scores answer two different questions. Opportunity Score = "should we cover this topic THIS WEEK vs other candidates?" (owned by content-calendar). Intent Score = "what's the BOFU intent of this topic for CTA/funnel decisions?" (owned by bofu-scorer).`

Then two tables in a responsive 2-column grid (`grid-template-columns: 1fr 1fr` on desktop, `1fr` on mobile at ≤800px).

### Table A — Opportunity Score (25 pts)

Owner: `content-calendar`. Source: `outputs/calendar-data/calendar-{YYYY-MM-DD}.json` → `topics[].opportunity_score`.

| Criterion | Score /5 | Source / Notes |
|---|---|---|
| Performance Signal | n/5 | Pulled from content-calendar Performance Analysis Layer + GSC historical |
| Search Demand | n/5 | GSC rising query count matching topic |
| Audience Intent | n/5 | Reddit/Nextdoor confirmation count |
| Competitive Gap | n/5 | Competitor coverage audit |
| Timeliness | n/5 | Current news/permit/event hook |
| **Total** | **n/25** | Threshold status: `must_create` (22-25), `strong` (17-21), `consider` (12-16), `skip` (<12) |

**Fallback rule:** If this topic is ad-hoc (no matching entry in `outputs/calendar-data/calendar-*.json`), render every row as `—` with a single-row note below: "Ad-hoc topic — no weekly Opportunity Score available. Intent Score still applies."

### Table B — Intent Score (25 pts base + freshness ±5)

Owner: `content-creation-engine/references/phases/bofu-intent-scorer.md` (absorbed May 2026). Source: `outputs/scored-topics-{ts}.json` for this topic's slug.

| Criterion | Score /5 | Source / Notes |
|---|---|---|
| Inquiry Type Match | n/5 | Property / Process / Professional-Process |
| Intent Matrix Position | n/5 | DECISION / CONSIDERATION / AWARENESS cell |
| Source Confirmation | n/5 | Count of platforms (GSC, Reddit, Nextdoor, PAA, Zillow Q&A...) |
| Emotional Temperature | n/5 | Conversion potential (high / moderate / low) |
| Local Relevance | n/5 | Hyperlocal / market / state / national |
| Freshness | n/5 | Angle + market + keyword overlap with last 2-4 weeks |
| **Base Total** | **n/25** | Before freshness adjustment |
| **Freshness Adjustment** | **±n** | From rolling topic-history.json |
| **Final Total** | **n/25** | Threshold status: `ships` (≥18), `reconsider` (14-17), `drop` (<14) |

### Rendering Requirements

- Both tables rendered inline as real HTML `<table>` elements (NOT collapsed into accordions).
- Use CSS Grid on the wrapper so tables sit side-by-side on desktop (≥800px viewport) and stack vertically on mobile.
- Total rows get `font-weight: 700` and a top border separator.
- Threshold status text gets color coding: green for `ships`/`must_create`, amber for `strong`/`consider`/`reconsider`, red for `skip`/`drop`.
- If a criterion score is missing (e.g., Freshness when `topic-history.json` doesn't exist), render as `—` with a small italic note, do NOT omit the row.

### Hero Pill Update

The hero score pill (top of dashboard, under the title) MUST show BOTH scores joined by a separator:

```
<div class="hm-pill hero-score">Opportunity 23/25 · Intent 20/25 &starf;</div>
```

If Opportunity Score is unavailable (ad-hoc topic): `<div class="hm-pill hero-score">Ad-hoc · Intent 20/25</div>`.

### Why This Rule Exists

Prior dashboards rendered ONE combined score on a 10-pt scale, conflating "is this worth covering?" with "is this BOFU?" The two-score model (April 2026 architectural streamline) separates weekly-topic-selection from per-topic-intent-classification. Showing both tables on every dashboard keeps the distinction visible and prevents the scores from silently merging b