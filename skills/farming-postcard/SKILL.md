---
name: farming-postcard
description: Generate print-ready 6x4 farming postcards for Graeham Watts in his locked brand system (gold + black, chevron pattern, Intero + Graeham Watts lockup). Three workflows — interactive create on demand, scheduled preview that emails 3-5 hook options 7 days before the 1st and 15th of each month, and recall of previously-emailed options for selection. Use ANY time the user mentions farming postcard, direct mail postcard, EPA postcard, neighborhood postcard, mailer, mail piece, Wise Pelican, Universal Mail Works, Corefact, ProspectsPLUS, monthly postcard, 1st of the month postcard, 15th of the month postcard, equity postcard, buyer-tagged postcard, anti-Zillow postcard, neighbor envy postcard, AI search postcard, new postcard for next month, the next farming card, run the postcard skill, design a postcard, "pull up the postcard options you emailed", "what did you send me for the next postcard", "show me the postcard previews", "pick one of the postcard hooks". Also trigger when user uploads past postcards as reference and asks for the next one in the series, or says things like "what's the hook for next month" or "we need a postcard for the first" or "let's do the 15th card." Encodes Graeham's 6 historical headline archetypes (equity, buyer-tagged, anti-Zillow buyer pool, AI search, anti-Zestimate, neighbor envy), the locked contact block continuity rule, CTA→landing page router, Universal Mail Works print specs, and an option-cache for scheduled previews.
---

# Farming Postcard Skill

## Purpose

Generate Graeham Watts farming postcards that match the locked brand system used across past mailings, with one-shot per-card customization. Every card ships with the same visual continuity (gold border, chevron pattern, identical bottom contact lockup) so the audience recognizes the sender instantly. Only the **hook + back copy + QR target** changes per card.

**Why the lockdown matters:** Direct mail works on repetition. Recognition before reading is the entire point. The bottom contact block, logo lockup, color palette, and disclaimer placement are NEVER negotiable — they are the brand signature.

## Three workflows

| Workflow | Trigger | Output |
|---|---|---|
| **A — Interactive create** | User says "make a postcard for [date]" | HTML preview + print-ready PDF in Downloads |
| **B — Scheduled preview** | Cron: 8th + 24th of month at 8am | Email to graehamwatts@gmail.com with 3-5 hook options + cache to option-cache.md |
| **C — Recall emailed options** | User says "pull up what you emailed me" | Read cached options, present in chat, user picks one → run Workflow A on the choice |

---

## Workflow A — Interactive create (user requests a postcard now)

### Step 1 — Gather inputs

Ask the following IN ORDER, using `AskUserQuestion` where multiple-choice makes sense.

**Q1: Mail date?** (e.g., "06/01/26"). Drives filename `Farming_Postcard_EPA_[MM_DD_YY].pdf` and auto-suggests an archetype.

**Q2: Audience?** Farm only / Past clients only / Both (generic — most common).

**Q3: Hook angle?** Offer the 10 archetypes from `references/headline-library.md`:
1. **Equity** (pride/curiosity)
2. **Buyer-tagged** (scarcity)
3. **Anti-Zillow buyer pool** (scarcity + anti-portal)
4. **AI search invisibility** (FOMO + tech)
5. **Anti-Zestimate** (anti-algorithm)
6. **Neighbor envy** (curiosity + social proof)
7. **Low-inventory timing** (supply-side scarcity)
8. **Quiet sale / no-hassle** (privacy + ease)
9. **Prop 19 tax transfer** (education + unlock)
10. **Local proof / just sold** (social proof + recency)
11. **Custom** (user-provided)

**MANDATORY before offering or accepting any archetype:** run the **4-axis differentiation check** from headline-library.md "Differentiation rules" against the Repetition tracker table — archetype cooldown (3 cards), CTA-destination cooldown (2 cards), villain cooldown (2 cards Zillow-free after any Zillow-bashing card), core-claim cooldown (4 cards). If the user explicitly asks for an archetype that fails, warn them which axis it fails and why, then follow their call. Graeham flagged repetitive output on 2026-06-11 — this check exists because rotating archetype NAMES alone is not differentiation.

**Cadence default suggestions:**
- 1st of month → education/pride angles (Equity, Prop 19, Neighbor envy)
- 15th of month → scarcity/timing angles (Buyer-tagged, Low-inventory, Quiet sale, Local proof)

**Q4: CTA type?** Drives QR target via `references/cta-router.md`:
- Home valuation / Testimonials / Free report (market) / Free report (AI score) / Thinking of selling / Off-market buyers / Call-text Graeham / Custom URL

If the CTA type's URL is `[NOT SET]` in `cta-router.md`, ask user once, then CACHE it by editing the file. Never ask twice.

**Q5: Live data to bake in?** Optional. If user provides a number, FLAG: "Verify before print — never fabricate."

### Step 2 — Generate headline

Use chosen archetype from `references/headline-library.md`. Don't copy past headlines verbatim — pull the **lever** and rebuild fresh language using the remix patterns there.

**Gold-highlight rules:** 1-3 words max per headline. Solid gold fill for short emphasized phrases; gold underline for action verbs.

### Step 3 — Build back copy

Structure (always):
1. **Headline** (Anton ~26pt) — gold-box-wrapped key word
2. **Italic body** (Inter 10pt, max 3 sentences) — proof + differentiation
3. **CTA line** (Anton, gold) — what they get
4. **QR + scan label** — "Scan to see your [thing] today"

### Step 4 — Render

Substitute slots in `templates/postcard-template.html`:
- `{{MAIL_DATE}}`, `{{ARCHETYPE}}`, `{{FRONT_HEADLINE_HTML}}`, `{{FRONT_SUBLINE_HTML}}`, `{{BACK_HEADLINE_HTML}}`, `{{BACK_BODY_HTML}}`, `{{BACK_CTA_LINE}}`, `{{QR_SCAN_LABEL}}`, `{{QR_IMAGE_SRC}}`, `{{FRONT_PHOTO_SRC}}`, `{{BACK_PHOTO_SRC}}`

**LOCKED — never substitute** (see `references/design-tokens.md`): All design tokens, the bottom contact lockup, gold border, chevron pattern, vertical disclaimer.

Save HTML preview to: `C:\Users\Admin\Downloads\Farming_Postcard_[MM_DD_YY]_PREVIEW.html`

### Step 5 — Generate print-ready PDF

Render HTML to PDF at 6.25" × 4.25" (includes 0.125" bleed each side) at 300 DPI using Playwright (see `references/print-specs.md` for the script). Output to `C:\Users\Admin\Downloads\Farming_Postcard_[MM_DD_YY]_PRINT.pdf`.

### Step 6 — Present + log

1. `mcp__cowork__present_files` to surface HTML + PDF
2. Append new card row to "Cards shipped" table in `headline-library.md`
3. Offer GitHub sync if skill itself was edited

### Step 7 — Auto-publish to online archive (MANDATORY)

Every new card must be added to the public-facing archive at `Graehamwatts/online-content/farming-postcards/` so Graeham (and Claude in future sessions) can see the running history.

**Steps:**
1. Clone `Graehamwatts/online-content` to /tmp
2. Copy the PDF to `farming-postcards/pdfs/[YYYY-MM-DD]-[archetype-slug].pdf`
3. Generate a thumbnail (page 1, 100 DPI JPG via `pdftoppm`) to `farming-postcards/thumbnails/`
4. If the card is preview-only (no PDF yet), copy the HTML preview to `farming-postcards/[YYYY-MM-DD]-[archetype-slug]-preview.html`
5. Append the new card entry to `farming-postcards/archive.json` under `cards[]`
6. Regenerate `farming-postcards/index.html` from `archive.json` — add a new card to the grid at the top
7. Commit: `Add [YYYY-MM-DD] [archetype] postcard to archive` and push to main

**Live dashboard URL:** https://graehamwatts.github.io/online-content/farming-postcards/

**Archive entry format (matches existing archive.json schema):**
```json
{
  "id": "YYYY-MM-DD-archetype-slug",
  "mail_date": "YYYY-MM-DD",
  "archetype": "[Equity / Buyer-tagged / etc.]",
  "lever": "[psychological lever]",
  "front_headline": "[plain text]",
  "back_headline": "[plain text]",
  "cta_type": "[CTA type from cta-router]",
  "cta_line": "[gold CTA tagline]",
  "audience": "[Farm / Past clients / Both]",
  "pdf": "pdfs/YYYY-MM-DD-archetype-slug.pdf",
  "thumbnail": "thumbnails/YYYY-MM-DD-archetype-slug-1.jpg",
  "notes": "[one-line note about the card]"
}
```

---

## Workflow B — Scheduled preview (cron-triggered, no user in the loop)

**Trigger:** Scheduled task fires on the 8th of each month (7 days before the 15th drop) and on the 24th (7 days before the 1st of next month) at 8am.

### Step B1 — Calculate target mail date

- If today is the 8th → target date is the 15th of this month
- If today is the 24th → target date is the 1st of NEXT month

### Step B2 — Pick 3-5 archetype options

1. Read `references/headline-library.md` — BOTH the "Cards shipped" table AND the "Repetition tracker" table
2. Run the **4-axis differentiation check** (see "Differentiation rules" in headline-library.md) on every candidate:
   - Archetype not used in last 3 cards
   - CTA destination differs from the previous 2 cards
   - If recent cards named Zillow/algorithms as villain, candidate must be villain-free (2-card cooldown)
   - Core claim not repeated within 4 cards (e.g., "I have buyers waiting" is the SAME claim whether the archetype is Buyer-tagged or Anti-Zillow)
3. Pick 3-5 candidates that pass ALL FOUR axes, honoring cadence:
   - Target = 1st → bias toward education/pride angles (Equity, Prop 19, Neighbor envy)
   - Target = 15th → bias toward scarcity/timing angles (Buyer-tagged, Low-inventory, Quiet sale, Local proof)
4. The library has 10 archetypes (#7-10 added 2026-06-11 after Graeham flagged repetition) — never offer an option that fails the check just to fill a slot.

### Step B3 — Generate hook options

For EACH archetype picked, generate:
- A fresh headline (using the remix patterns, not copy/paste)
- One-line "why this works" rationale
- Suggested back-headline + CTA line
- Suggested CTA type (drives QR target)

Format as a clean comparison table.

### Step B4 — Send email to Graeham + Peter (REAL SEND via SMTP)

**Recipients (LOCKED — always both):**
- graehamwatts@gmail.com (Graeham)
- graehamwattsvideo@gmail.com (Peter, also goes by Jason)

**Method:** Use the SMTP send script (NOT Gmail MCP draft — the MCP only supports drafts which Graeham won't see). The script reads his Gmail App Password from `C:\Users\Graeham Watts\Documents\Claude\Skills\gmail-app-password.txt`.

```bash
python "C:\Users\Graeham Watts\Documents\Claude\Skills\skills\farming-postcard\scripts\send_options_email.py" \
    "<path_to_rendered_html>" \
    "Postcard options for [TARGET_MAIL_DATE] — pick one by [PICK_DEADLINE]" \
    "<path_to_plaintext_fallback>"
```

**HTML body:** Build by substituting slots in `templates/options-email-template.html` and `templates/option-card.html`. Both templates use the locked brand system (white postcard look, gold left border, cream option panels, Anton headlines, INTERO + Graeham Watts lockup at bottom). DO NOT use the dark dashboard style — that's not on-brand.

**Subject format:** `Postcard options for [Date] — pick one by [Deadline]`
Example: `Postcard options for June 15 — pick one by June 12`

**Plaintext fallback:** Always include a plaintext version for clients that don't render HTML. Short bullet list of options.

**Error handling:** If `gmail-app-password.txt` is missing or returns 401 (invalid/expired password), abort the send, log to schedule-log.md as `email_status=failed_no_credential`, and create a fallback Gmail draft as a safety net so the options aren't lost.

### Step B5 — Cache options

Append to `references/option-cache.md`:

```markdown
## [TARGET_DATE] (emailed [SENT_DATE])
Status: pending pick

### Option 1 — [Archetype]
Front headline: [text with markup]
Back headline: [text]
CTA: [type] → [URL]
Why: [rationale]

### Option 2 — [Archetype]
...

[etc.]
```

### Step B6 — Confirm to logs

Write a one-line entry to `references/schedule-log.md`: `[timestamp] Emailed [N] options for [target date], cached at option-cache.md`

---

## Workflow C — Recall emailed options (user is back in Cowork)

**Trigger:** User says "pull up what you emailed me", "show me the postcard previews", "what did you send for the next card", "pick one of the postcard hooks", etc.

### Step C1 — Read cache

Read `references/option-cache.md`. Find the most recent entry with `Status: pending pick`.

### Step C2 — Present in Cowork

Show the user a clean side-by-side comparison of the cached options (table or cards). Use the existing markup from the email so it feels like the same brief.

### Step C3 — User picks

User picks an option ("use option 2", "let's go with the neighbor envy one"). If user wants to modify the picked option, accept tweaks now.

### Step C4 — Run Workflow A on the pick

Hand the chosen option's parameters into Workflow A starting at Step 4 (skip the question flow — answers are already in the cache).

### Step C5 — Update cache

Mark that option in `option-cache.md`: `Status: PICKED on [date]`. Mark others: `Status: not picked`. Move the whole entry under a "Resolved" section.

---

## Critical principles (apply to all workflows)

- **Bottom contact block continuity is sacred.** Never edit it per card.
- **Never fabricate stats.** Verify before any number lands on print.
- **One hook per card.** 3-second glance time. One hook, one CTA, one flip.
- **Two headshots, two moods.** Front = pointing pose; Back = smiling pose.
- **Disclaimer is legally required.** Vertical right edge of back. Never remove.
- **Repetition rule is 4-dimensional.** Archetype (3-card cooldown), CTA destination (2-card cooldown), villain (2 Zillow-free cards after any Zillow-bashing card — check the BACK copy too, that's where it sneaks in), and core claim (4-card cooldown). Run the check against the "Repetition tracker" in headline-library.md in EVERY workflow, and append a row to that tracker every time a card ships. Rotating archetype names alone is NOT variety — that failure mode shipped 3 Zillow-bashing cards in a row and offered Graeham the same recycled hooks by email (caught 2026-06-11).
- **Headlines must be structurally fresh, not just lever-fresh.** Before finalizing any headline, compare it word-by-word against every front AND back headline in the Repetition tracker. If it shares its sentence skeleton or signature phrase with a prior card ("I have...", "Your ___ is wrong", "the real number"), rewrite it.

## Files in this skill

```
farming-postcard/
├── SKILL.md                          (this file)
├── references/
│   ├── headline-library.md           (6 archetypes + remix + memory)
│   ├── design-tokens.md              (locked brand system)
│   ├── cta-router.md                 (CTA type → URL cache)
│   ├── print-specs.md                (UMW + bleed math + Playwright script)
│   ├── option-cache.md               (emailed preview options awaiting pick)
│   └── schedule-log.md               (cron run history)
└── templates/
    └── postcard-template.html        (parameterized master template)
```

## Setup (one-time, already done as of build)

- **GitHub backup:** PAT at `C:\Users\Graeham Watts\Documents\Claude\Skills\github-token.txt`
- **Gmail SMTP:** App Password at `C:\Users\Graeham Watts\Documents\Claude\Skills\gmail-app-password.txt`
- **Scheduled tasks:**
  - `farming-postcard-15th-preview` — fires 8th of each month at 8am → SMTP sends options for the 15th
  - `farming-postcard-1st-preview` — fires 24th of each month at 8am → SMTP sends options for the 1st of next month
- **Email recipients (LOCKED):**
  - graehamwatts@gmail.com (Graeham)
  - graehamwattsvideo@gmail.com (Peter, aka Jason)
- **Send method:** SMTP via `scripts/send_options_email.py` (NOT Gmail MCP draft)

## After a card ships

1. Append the shipped card to BOTH the "Cards shipped" table AND the "Repetition tracker" table (core claim / villain / CTA destination) in `headline-library.md`
2. Move the picked option in `option-cache.md` to "Resolved"
3. Run Step 7 (auto-publish to online archive at `Graehamwatts/online-content/farming-postcards/`)
4. Push skill update to GitHub via `github-skill-sync` if any reference files changed

## Live archive

All historical and current postcards are tracked at:
- **Dashboard URL:** https://graehamwatts.github.io/online-content/farming-postcards/
- **Repo path:** `Graehamwatts/online-content/farming-postcards/`
- **Source of truth:** `archive.json` in that folder — regenerate `index.html` from it whenever cards are added
