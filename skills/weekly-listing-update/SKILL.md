---
name: weekly-listing-update
description: "Generate the Monday weekly seller status report for any active Graeham Watts listing. Use this skill ANY time the user mentions: weekly listing update, Monday update, weekly seller report, listing status report, weekly seller email, weekly update for [property/address], Monday seller email, weekly status report for a listing, generate the weekly for [listing], run the Monday report. Also trigger when John or Graeham drops a ShowingTime/Supra showing export + Glide disclosure export and references a property address. The skill produces a designed HTML weekly status report (matching the seller-POV format pioneered with 1908 Cooley Ave), pushes it to GitHub Pages for a permanent hosted URL, and creates a Gmail draft addressed to the seller for Graeham's review before sending. Builds a week-over-week trajectory (showings, disclosure pulls, and feedback per week, with real deltas), surfaces any offer prominently at the top, and auto-runs the humanizer skill on all prose so reports never go out with em dashes or AI tells."
---

# Weekly Listing Update

Generate the Monday weekly seller status report for an active listing — synthesizes showing activity, disclosure pulls, market context, and recommended next moves into a designed HTML email that Graeham reviews and forwards to the seller.

## When To Use

- After a showing/disclosure data export is dropped into the session
- User says: "run the weekly for [address]", "Monday update for [address]", "weekly seller report"
- Any time a fresh batch of showing/disclosure data needs to become a seller-ready report

**Do NOT use for:** ad-hoc seller questions, one-off market updates, listing presentations (use cma-generator), disclosure analysis (use disclosure-analyzer).

## The Larger Workflow (Mondays)

This skill is the **execution stage** of a two-stage Monday workflow:

| Stage | When | Who | What happens |
|---|---|---|---|
| 1 — Reminder | Monday 12:30 PM | Scheduled task (`monday-weekly-seller-updates`) | Sends a reminder email to Graeham + John listing the active properties and asking John to upload fresh ShowingTime + Glide exports |
| 2 — Generation | After data is uploaded | This skill | Parses data, drives Chrome to scrape live Zillow/Redfin/Homes.com, builds the report, creates seller Gmail draft for Graeham's review |

**This skill never auto-runs.** It only fires when someone uploads data and asks for a weekly update. The Monday 12:30 PM email just creates the prompt for that human action.

---

## Output: What This Skill Produces

1. **A designed HTML report** saved locally (workspace/outputs) AND pushed to `Graehamwatts/online-content/emails/` for a permanent hosted URL
2. **A Gmail draft** addressed to the seller, with the HTML embedded, marked NOT SENT — Graeham reviews and sends manually
3. **A summary message** in chat with: the hosted URL, the GitHub file URL, the Gmail draft confirmation, and a list of what changed since last week if a prior report exists

**Hosted URL format:**
```
https://graehamwatts.github.io/online-content/emails/[YYYY-MM-DD]-[address-slug]-weekly-status.html
```

---

## Required Inputs (Ask If Missing)

| Input | Source | Required |
|---|---|---|
| Property address | User or showing file name | YES |
| Seller name (greeting) | Stored in skill or asked | YES |
| Seller email | For Gmail draft | YES |
| List price + sqft | For PPSF math (or pull from MLS via web search) | YES |
| Showing data file | ShowingTime / Supra / Aligned Showings export | YES |
| Disclosure data file | Glide disclosure-pull export | Optional but recommended |
| Reporting period dates | Default to "last Monday → today" | Auto-fill |

If any required input is missing, ask once before proceeding. Do NOT proceed with placeholders.

---

## Step 1: Gather and Validate Inputs

Pull property metadata via web search (`WebSearch`) if not provided:
- Search: `"[address] [city] for sale Zillow"`
- Extract: list price, beds, baths, sqft, MLS number, days on market

Pull EPA / city market context:
- Search: `"[city] [zip] average days on market [month] [year] housing trends"`
- Extract: median list price, median PPSF, average DOM
- Calculate: subject DOM gap, subject PPSF premium

### Step 1b: Drive Claude in Chrome to scrape live portal data

WebSearch returns metadata but NOT the live engagement metrics (views, saves, hot-listing badges). For those, use the Claude in Chrome MCP. This is critical — it's what makes the report uniquely valuable each week.

1. Get a tab via `mcp__Claude_in_Chrome__tabs_context_mcp` (createIfEmpty: true)
2. Navigate to each portal: Zillow, Redfin, Homes.com, Realtor.com
3. For each, wait 3-4 seconds for load, then take a screenshot or use `mcp__Claude_in_Chrome__find` to extract metrics
4. Extract: views, saves, days on Zillow, "Hot Home" badges where available
5. Close tabs when done

**If Chrome navigation is denied:** fall back gracefully — note in the report's Online Visibility section that live portal metrics will be added once portal access is set up. Use the disclosure-pull volume as the engagement proxy.

**Always close the tabs.** Leaving 4 portal tabs open in the user's Chrome each Monday gets annoying fast.

---

## Step 2: Process Showing + Disclosure Data

Use `openpyxl` to parse the Excel file(s). Two sheets typically:
- **Sheet 1 — Supra/Showing activity** — Agent name, Date & Time, Feedback, follow-up flags, Notes
- **Sheet 2 — Glide disclosure activity** — Agent name, Date & Time, Feedback, Notes
- **Sheet 3 — Open House Feedback** — often empty for tenant-occupied listings; skip if so

For each agent row:
- Format name as `First L.` (e.g., "Yang Li" → "Yang L.", "Jun Chen (Cathy)" → "Jun C.")
- Strip date prefixes from feedback (`4/13/26-` etc.)
- Flag rows with offer-relevant keywords: `accepted offer`, `interested`, `negotiate`, `discuss with my clients`, `month to month`
- Skip "Invited by" rows (sub-buyer entries)

The `scripts/generate_report.py` helper handles this parsing.

### Week-over-week is built from the cumulative export

The uploaded ShowingTime/Glide export is **cumulative**: it holds every showing and disclosure pull since the listing went live, each stamped with a date. That single file IS the running history, so the report rebuilds the full week-by-week curve from it each run. Previously published reports in `online-content` serve only as a backup cross-check. There is no separate database to maintain.

`generate_report.py` now emits (as JSON to stdout):
- `weeks` / `detailed_weeks` / `earlier_rollup` — per-calendar-week showings, disclosure pulls, new feedback, and that week's top feedback theme. Weeks older than `--recent-weeks` (default 6) roll into one "Earlier" line.
- `this_week` + `this_week_deltas` — the most recent week's numbers and the change versus the prior week. Use these for the KPI deltas (no more hand-typed guesses).
- `momentum` — `accelerating` / `steady` / `cooling`, from the slope of the recent weeks.
- `cumulative` — totals since launch, for the appendix.
- `offers` (from the optional `--offers` JSON) and `offer_signals` (conservative keyword detection) — drive the offer banner in Step 4.
- `themes_overall` — ranked feedback themes for the "What Buyers Are Telling Us" summary.

If the export has no parseable dates, the script says so on stderr and the report falls back to a single "this period" view. Check the export for Date/Time columns if that happens.

---

## Step 3: Determine Status Indicator

Based on this week's activity:

| Condition | Status | Color |
|---|---|---|
| 2+ showings this week, fresh disclosure pulls, active warm leads | Active | Green |
| 1 showing or fresh follow-ups, but cooling trend | Attention Needed | Amber |
| 0 showings + no fresh follow-ups + DOM > local avg | Stalled | Red |
| Offer in hand, in escrow | Under Contract | Green |

Default to amber when uncertain. Be honest — green should mean genuinely active.

---

## Step 4: Build the HTML Report

Use the template at `templates/weekly-status-report.html` as the base. It contains the full design system established with 1908 Cooley Ave (May 3, 2026 issue).

Substitute these variables: `{{ISSUE_NUMBER}}`, `{{REPORT_DATE}}`, `{{GHL_CALENDAR_URL}}` (Graeham's GoHighLevel scheduling link — used in the Decision Required CTA), `{{PROPERTY_ADDRESS}}`, `{{CITY_STATE}}`, `{{BEDS_BATHS_SQFT}}`, `{{LIST_PRICE}}`, `{{MLS}}`, `{{REPORTING_PERIOD}}`, `{{STATUS_LEVEL}}`, `{{STATUS_HEADLINE}}`, `{{STATUS_MESSAGE}}`, `{{KPI_*_NUM}}`, `{{KPI_*_DELTA}}`, `{{SELLER_FIRST_NAME}}`, `{{EXEC_NARRATIVE}}`, `{{DECISION_TITLE}}`, `{{DECISION_BODY}}`, `{{DOM_DELTA}}`, `{{PPSF_DELTA}}`, `{{SUBJECT_DOM}}`, `{{MARKET_DOM}}`, `{{SUBJECT_PPSF}}`, `{{MARKET_PPSF}}`, `{{SHOWING_COUNT}}`, `{{DISCLOSURE_COUNT}}`, `{{TOTAL_INTERACTIONS}}`, `{{UNIQUE_AGENT_COUNT}}`, `{{SHOWING_TABLE_ROWS}}`, `{{DISCLOSURE_TABLE_ROWS}}`, `{{CONCERN_*}}`, `{{ACTIONS_THIS_WEEK}}`, `{{LISTED_DATE}}`, `{{LIST_PRICE_FULL}}`, `{{PROPERTY_DETAILS}}`.

New data blocks (2026-06-22), all filled from the `generate_report.py` JSON: the offer banner (`offers` / `offers_count`), the week-over-week bars + trend table (`weeks` / `earlier_rollup` / `cumulative`), the momentum chip (`momentum`), and the "What Buyers Are Telling Us" bullets (`themes_overall` plus the standout quotes you pick).

Key visual elements that MUST be preserved:
- Top bar with "Weekly Status Report · No. [N] · [Date]"
- Property header with address, beds/baths/sqft, list price, MLS, reporting period
- Status strip (color-coded)
- **Offer banner (NEW)** — right after the status strip, but ONLY when offers >= 1. One offer is the headline; make it loud (agent, offer price, percent of list, status badge, terms). Omit the block entirely when there are no offers.
- 4 KPI cards for THIS WEEK with deltas — fill deltas from the script's `this_week_deltas`, not by eye
- **Trajectory / week-over-week (NEW)** — the climbing bars + trend table (each week's showings, disclosure pulls, new feedback; an "Earlier" rollup; a Total row; the most-recent week highlighted) plus a momentum chip. Fill from `weeks` / `detailed_weeks` / `earlier_rollup` / `cumulative` / `momentum`.
- "The Read" — short executive paragraph
- Decision Required block (dark navy) — only include if a real decision is needed. **Primary CTA: Graeham's GHL calendar link** (substitute `{{GHL_CALENDAR_URL}}`). **Secondary CTA: tap-to-call `tel:6503084727`** ((650) 308-4727). If the GHL URL isn't known, leave the placeholder `[PASTE-GHL-CALENDAR-URL-HERE]` and tell the user to paste it.
- Market Context cards with big delta numbers (+X days, +Y%)
- Online Visibility section with syndication chips
- **What Buyers Are Telling Us summary (NEW)** — bullet summary ABOVE the detailed tables: the dominant theme(s) from `themes_overall`, two or three standout quotes, and a "shift this week" line. The full agent tables stay below it.
- Hero stat: showing count
- Showing Activity table (agent + feedback, two-column)
- Hero stat: disclosure count
- Disclosure Activity table
- Hero stat: total interactions
- Three ranked concern cards (#01 critical navy, #02 urgent amber, #03 standard)
- "What I'm Doing This Week" action list
- Appendix with cumulative numbers
- Signature block + footer

---

## Step 4b: Humanize the Prose — MANDATORY before publishing

Every line of **authored prose** in the report must pass the `humanizer` skill before it is published or drafted. This is a hard gate, not optional. It is what removes the em dashes (—) and the other AI tells.

How to run it:
1. Collect the narrative you wrote: status message, The Read, Decision block, the trajectory blurb, hero subtitles, the "What Buyers Are Telling Us" bullets, concern cards, "What I'm Doing This Week", and the signature paragraph.
2. Run that text through the `humanizer` skill (invoke the Skill). Replace em dashes with periods, commas, or parentheses; cut rule-of-three cadence, filler, and stiff AI vocabulary; keep Graeham's plain, warm voice.
3. Place the humanized prose into the template.

**Do NOT humanize:** verbatim agent feedback in the tables (it is quoted), MLS figures, addresses, or any number.

**Fallback if the `humanizer` skill is not installed here:** apply its checklist by hand — remove every em dash (use period / comma / parentheses); no "not only X but Y"; no three-item lists used purely for rhythm; cut "It's worth noting", "Importantly", "In today's market". Prefer short declarative sentences.

**Final safety scan:** before publishing, search the assembled HTML for the em dash character. The only allowed occurrences are inside quoted agent-feedback rows and the sign-off ("— Graeham"). Fix anything else.

---

## Step 5: Push to GitHub Pages with git (direct, NOT Composio)

Composio is retired in this workspace. Publish by pushing directly to the `online-content` repo with git, using the token in that clone's `github-token.txt`.

- owner: `Graehamwatts` · repo: `online-content` · branch: `main`
- path: `emails/[YYYY-MM-DD]-[address-slug]-weekly-status.html`
- Robust method on the Windows mount: clone `online-content` fresh into a temp dir, copy the generated HTML in, commit, and push, which avoids leftover `.git/*.lock` cruft. Pattern:
  - `PAT=$(cat github-token.txt | tr -d '[:space:]')`
  - `git push "https://${PAT}@github.com/Graehamwatts/online-content.git" HEAD:main`
- **Before pushing, run the brand tripwire** (`python scripts/verify_brand_identity.py` in the skills repo) and confirm only DRE `01466876` appears (the tripwire blocks the known-bad one). Keep `.github/workflows/` out of the commit (the token is `repo` scope, not `workflow`).

Filename: `YYYY-MM-DD-[address-slug-lowercase-hyphens]-weekly-status.html`
Example: `2026-05-04-1908-cooley-ave-weekly-status.html`

---

## Step 6: Create Gmail Draft (DO NOT SEND)

Use `mcp__69816e67-52bb-4259-b487-681f474d6ef0__create_draft`:
- to: [seller email]
- subject: `Weekly update — [property address] — [date range]`
- htmlBody: the full HTML report (or short intro pointing to hosted URL)
- The draft sits in Graeham's Gmail awaiting review. He can edit, then send.

**Never send seller emails directly — always create draft only.**

---

## Step 7: Return the Result

Output to chat:

```
Weekly status report generated.

Property: [Address]
Reporting period: [Range]
Status: [emoji] [Status Headline]

Hosted URL: https://graehamwatts.github.io/online-content/emails/[filename].html
Local copy: [workspace path]
Gmail draft created: [link to draft]

Top of mind for this week:
- [bullet 1]
- [bullet 2]
- [bullet 3]

Awaiting Graeham's review before sending to [seller name].
```

---

## Multiple Listings Workflow

When the schedule fires Monday afternoon and there are multiple active listings:

1. Look up active listings list (Graeham maintains in his contacts/notes)
2. For each listing, check if showing data has been dropped in the session
3. If yes, run Steps 1–7 for that listing
4. If no, flag it: "No data for [property] — John still needs to drop the export"
5. After all are done, send Graeham a single summary

---

## Important Rules

- **Humanize every line of prose (mandatory).** Run the `humanizer` skill before publishing. No em dashes in authored copy. See Step 4b.
- **One offer is the headline.** When offers >= 1, show the offer banner near the top. Never let an offer sit buried as "1 offer received" in the appendix.
- **Show the climb.** Always include the week-over-week trajectory (bars + trend table) and compute KPI deltas from the data, not by eye.
- **Always wait for Graeham's review** before any seller email is sent. Never use `send_message`, only `create_draft`.
- **Be honest about status.** Default to amber when uncertain. Green means genuinely active.
- **Always publish via direct git push** to `online-content`. Local-only files get lost; the hosted URL is the deliverable. Composio is retired.
- **Run the brand tripwire before every push.** The only valid DRE is `01466876`; the tripwire rejects the known-bad DRE listed in `identity.json`.
- **Never reuse a filename.** If a similar report exists, suffix `-v2`, `-followup`, etc.
- **Filter "Invited by" rows** out of agent counts.
- **Strip date prefixes** from feedback strings before display.
- **Format names as First L.** consistently.
- **Use real market data** when available. The +X days and +Y% PPSF cards are the strongest decision drivers.

---

## SOP Integration (For John)

This skill is designed to be runnable by John on Monday afternoons. The full SOP for John lives at:
`https://graehamwatts.github.io/online-content/emails/2026-05-03-john-weekly-update-sop.html`

John's role: pull data → run skill → review output → forward Gmail link to Graeham for approval.

---

*Part of the PropertyIQ skill library — Graeham Watts Real Estate*
