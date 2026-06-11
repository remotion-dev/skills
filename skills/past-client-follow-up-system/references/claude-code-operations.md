# Claude Code Operations Handoff (2026-06-10)

PCFS operation moved from Cowork to Claude Code on 2026-06-10. This file is the
operational layer for Claude Code sessions — newer than parts of SKILL.md.
**Where this file and SKILL.md disagree, this file wins** (SKILL.md predates the
2026-06-07 schedule rebuild and the move off n8n.cloud).

## Known SKILL.md staleness (as of 2026-06-10)

| Topic | SKILL.md says | Current truth |
|---|---|---|
| n8n instance | `graehamwatts.app.n8n.cloud` webhook URLs | `https://n8n.graehamwattsn8n.com` — operate via n8n-mcp tools |
| Sheet tabs | `Master_Past_Clients` / `By_Date` | `Master Past Clients` / `Actions By Date` (live schedule, ~2,897 rows through Dec 31 2027) |
| Sheet writes | workflow `3BsV1POSI3pdKNmY` ("Targeted Sheet batch update") | That ID is now "DIAG COE Batch Update (one-off)". Use the **temp-workflow pattern** below |
| Schedule source | Excel `By_Date` tab | DEPRECATED — live `Actions By Date` tab is the only schedule truth |

## First move, every session

Read `SKILL.md` + this references folder. Brand identity from
`skills/shared-references/identity.json` — Graeham's DRE is `01466876`; the
blocklisted DRE value (see identity.json `_blocked_values`) must NEVER be typed.

## The three systems of record — keep them in lockstep

Any change to a contact must propagate to ALL THREE or the cadences drift:

1. **GoHighLevel (GHL)** — live CRM, REST API.
   - Token + location file: `C:\Users\Graeham Watts\Documents\Claude\Skills\ghl-pit.txt`
     (line 1 = PIT bearer token, line 2 = location ID `6wuU3haUH7uNeT20E3UZ`).
   - Base `https://services.leadconnectorhq.com`, headers `Version: 2021-07-28`,
     `Authorization: Bearer <token>`.
   - Use `curl` from bash — python `urllib`/`requests` are 403-blocked in sandboxes.
     Pipe curl output to python only for JSON parsing.
   - Endpoints: `GET/PUT /contacts/{id}`, `GET /contacts/?locationId=<loc>&query=<name>`,
     `POST /contacts/{id}/notes`, `GET /locations/{loc}/customFields`.
   - Custom field IDs: Buying Property Address `F3jzxzh9JBCzF3FQRy7E`,
     Selling Property Address `aMXm4T9X30OrJmCbFz4l`, COE_date `MYBybCgfZiUZTl9aSvSd`.
     (Note: data-spec.md's older placeholder for Buying Property Address is wrong —
     this list is the verified one.)

2. **Google Sheet** (operational layer the n8n cadences READ) —
   ID `1PtfGzUvjJOz5qNmA5173MqmKO9cLCevAhcP12pFeG3s`.
   - Tab **`Master Past Clients`** — contact master (mailing Address/City/State/Zip,
     Buyer?/Seller?, COE Date (verified), Buying/Selling Address, Family Member,
     Notes, MLS Verified?, PCFS Active?, etc.).
   - Tab **`Actions By Date`** — the dated schedule the cadences read
     (Date, Day, Week of (Mon), Action, Client Name, Phone, Email, Who Does It,
     Property Address, EPA?, Type, Contact ID). ~2,897 rows through **Dec 31 2027**.
   - Tab **`ABD Backup 2026-06-07`** — pre-rebuild snapshot for rollback.
   - **No direct Sheets API credential in bash.** Read/write via the temp-workflow
     pattern below.

3. **Local Excel master** — latest dated copy in Downloads, currently
   `Past Clients Master (updated 2026-06-07).xlsx`. Edit with `openpyxl`.
   Excel `Master_Past_Clients` tab has **no Family Member column** (put that in
   Notes); its `By_Date` tab is deprecated as a schedule source.

## n8n — the cadence engine

Instance `https://n8n.graehamwattsn8n.com`, operated with the n8n-mcp tools
(`n8n_get_workflow`, `n8n_create_workflow`, `n8n_update_partial_workflow`,
`n8n_test_workflow`, `n8n_delete_workflow`, `n8n_executions`, `n8n_validate_workflow`).

Shared credentials inside n8n: Google Sheets = `AkBUwX11QA8RRHec`, Gmail = `DtB2QyzcO239Eb5l`.

**7 cadence workflows (do NOT edit unless asked):**

| ID | Workflow | Schedule | Manual webhook (POST) |
|---|---|---|---|
| `whjMmVXawdg1Ingx` | Daily Past-Client Call Email | Mon–Fri 10am PT | `pcfs-daily-call-fire` |
| `7CxqNkCQAuw1noGL` | Sharon Weekly Handwritten Notes | daily 8am PT | `pcfs-sharon-notes-fire` |
| `LHGnZC2X2KKXljB0` | CMA Weekly Digest | daily 9am PT | `pcfs-cma-digest-fire` |
| `oNUrUUXCtdaZXUcr` | Monthly Anniversary Batch | 24th 9am | — |
| `lS3ZMPHQA92AoyJt` | Bimonthly Market Update | 24th odd months 9am | — |
| `nxoRGbUYh5b4SxoK` | Monthly Birthday Touch | 24th 10am | — |
| `zrUVXmEE3Bso72RU` | Adrian Weekly Briefing | Mon 7am | — |

Watchdog (catches missed/failed runs): `SMQMpqyKWQVBkiZs`.

Webhooks require **POST** (GET returns 404 "not registered for GET"). Fire a
manual run with `n8n_test_workflow` (triggerType webhook, httpMethod POST).

## The temp-workflow pattern (how to read/write the live Sheet)

Bash can't hit the Sheets API directly, so do sheet reads/writes through a
throwaway n8n workflow:

1. `n8n_create_workflow`: Webhook (POST) → Google Sheets node (read or update,
   credential `AkBUwX11QA8RRHec`, doc ID above, tab name) → optional Code node
   to filter/verify.
2. For an **update**, output a row object that includes `row_number` and use
   Google Sheets `update` with `matchingColumns: ["row_number"]`,
   `mappingMode: autoMapInputData`.
3. `n8n_update_partial_workflow` to `activateWorkflow`, then `n8n_test_workflow`
   to fire it, then **read back** to confirm the write landed.
4. **Always `n8n_delete_workflow` the temp workflow when done.** Name temps
   `PCFS TEMP — ... (delete me)`.

## Non-negotiable rules

- **Three-way sync:** GHL + Google Sheet + Excel must all reflect every contact
  change. After editing, re-deliver the updated Excel to Downloads and present it.
- **Zero-Guard / trust-no-zero:** a PCFS email reporting "0" is guilty until
  proven innocent. The Sharon/Call/CMA workflows carry a 🛡️ self-check footer
  (rows read, schedule rows, next item, horizon) and a red "⚠️ ZERO FAILED
  SELF-CHECK" banner for suspicious zeros. Preserve that logic (variables
  prefixed `__`) in any Build-Email edit; test on a temp staging workflow first.
- **Sheet-edit safety:** never blind-edit cells by position. Match by
  `row_number` (or value-targeted Find & Replace). Blind edits caused duplicate
  rows here before.
- **CMA output:** built by `cma-generator` in Past-Client mode. Warm open,
  referral CTA close, months-of-inventory included, NO data-source/MLS caveats
  (only allowed disclaimer: "Professional opinion of value, not a formal
  appraisal"). For a past **seller** who moved: "your former home / neighborhood,"
  never "your home"; never mail to a sold address.
- **Email = draft, don't send.** Create Gmail drafts; Graeham reviews/sends.
  Only send on an explicit per-email "yes."
- **Verification discipline:** credential `updatedAt` timestamps are NOT proof.
  Ground truth = the workflow executed AND the data/email actually landed.
  Read it back.

## Credential file locations (paths only — open at runtime, never hardcode)

- GHL token + location: `C:\Users\Graeham Watts\Documents\Claude\Skills\ghl-pit.txt`
- GitHub PAT: `C:\Users\Graeham Watts\Documents\Claude\Skills\Git Hub PAT Token for claude\github-token.txt`
  (root-level copy sometimes disappears; this subfolder copy is reliable).
- Gmail app password: `C:\Users\Graeham Watts\Documents\Claude\Skills\gmail-app-password.txt`
- Gmail also available as MCP connector (search_threads / get_thread /
  create_draft — connector cannot SEND or trash drafts).

## Common tasks → where to act

- **New deal closed / onboard** → SKILL.md "New-Deal Onboarding" (GHL + Sheet
  Master + Actions By Date + Excel).
- **Fix a contact** → GHL (curl), live Sheet (temp workflow, match row_number),
  Excel (openpyxl), then re-deliver Excel.
- **"Why didn't X get an email"** → check that workflow's recent
  `n8n_executions`, and confirm the row exists in `Actions By Date` with the
  right Date/Week.
- **Find a current mailing address** → check Glide (app.glide.com) and SkySlope
  first; if blank, draft an email to title rep **Daniel Dietrich,
  danield@octitle.com** (Orange Coast Title) for a property/title-plant search,
  cc TC **Giselle, graehamwattstc@gmail.com**. Do NOT skip-trace via
  people-search sites. The tax-billing address on the MLS Realist tax view is a
  reliable mailing-address source.
- **Push a skill change** → edit under `...\Skills\skills\...`, run
  `python3 scripts/verify_brand_identity.py` before pushing.

## Current state (as of 2026-06-10)

- Schedule rebuilt and live through **Dec 31 2027**; OAuth app published to
  Production (stops the 7-day token death); watchdog active.
- Zero-Guard self-checks live in Sharon/Call/CMA workflows.
- Reference example completed end-to-end: contact **Zhen Wang**
  (`J5DJPVv96CpBawxasDtF`) + co-seller **Qing Gan** — past sellers of 2617
  Fordham St EPA (MLS ML81727278, Graeham listing agent, sold $938K, COE
  12/10/2018), mailing address set to **228 Montevideo Cir, Fremont, CA
  94539-5352** across all three systems.

When unsure, re-read SKILL.md and confirm any side-effectful step with Graeham
before firing it.
