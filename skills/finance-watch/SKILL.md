---
name: finance-watch
description: >
  Graeham's personal finance pipeline brain — Plaid bank transactions + SparkReceipt receipts → the
  Finance Google Sheet → entity tax tabs. Use ANY time Graeham mentions: watch my finances, my finances,
  Plaid, Chase, bank transactions, pull my transactions, refresh finances, finance sheet, bookkeeping,
  SparkReceipt, receipt workflow, tax totals, chase_transactions, FTB / franchise tax payments, "is the
  finance pipeline up", "pull my bank data", "reconcile receipts", or anything about reading or refreshing
  his bank/expense data. ALSO trigger when n8n has just been fixed/restarted and he wants the bank pull run
  ("n8n is back", "go live", "run the finance pull now"). This skill knows the architecture, the failure
  modes, the exact go-live sequence, and where every credential lives.
---

# finance-watch — Graeham's finance pipeline operator

## STATUS as of 2026-06-09 (verified live; consolidation completed this date)
- n8n is UP at `n8n.graehamwattsn8n.com` (healthz ok).
- **THE MASTER SHEET (single source of truth): "Finances 2026 — MASTER (Auto)"**, Google Sheet id
  `1zerRMfH7C7-hgbIVSPVgeHBNpiDJkOGsVQkWMP_9unw` (formerly "PropIQ Finance Lab — Working Copy 2026").
  22 tabs: 9 automation tabs (Dashboard, Receipt Check, Detail Ledger (Auto), Transactions, Tagging Rules,
  Receipts, PropIQ (Auto), Realtor Faraday Expenses (Auto), Enterprise Holdings (Auto)) + 13 manual entity
  tabs merged in from Sharon's "Finances 2026 .xlsx" on 2026-06-09 (GW Personal, Realtor Faraday Expenses,
  GW Property Expenses, Enterprise holdings, PROP IQ, 2842 Cornelius Drive, All Income & expenses, Loans info,
  Income estimate, 2048 Huran SJ, Monthly Costs, Explanation of Expense Item #s, Endavour Enterprise).
- The Plaid workflow EXISTS and is ACTIVE: **"Plaid Multi-Sync (Chase + AMEX + BILT)"** (n8n id `GXP6VSXuqJcnFpbs`, 11 nodes), daily 6am cron + webhook `plaid-sync-trigger`, writes to the
  MASTER's `Transactions` tab. Verified pulling all 3 institutions (840 txns on 2026-06-09; data current
  through 2026-06-08). Do NOT redeploy `assets/plaid-transactions-to-sheets.json` unless this workflow is gone.
- **"Spark Receipt → Google Sheets"** is ACTIVE (id `723IrFCLz0SDaQ61`), webhook `spark-receipt`, writes to the
  MASTER's `Receipts` tab (includes receipt image_url).
- **"Reconciliation — Missing Receipts"** is ACTIVE (id `uB4TUGuFieMSu8n7`, fixed + activated 2026-06-09): daily
  6:30am cron + webhook `reconcile-missing`. Rebuilds the MASTER's `Missing Receipts` tab — last-30-days outgoing
  charges with no receipt matching within $0.01 / 5 days (skips transfers, card payments, loans, payroll).
- **"Plaid Balances Sync (Chase + AMEX + BILT)"** is ACTIVE (id `n0V85d2I2dA2N0Ym`, built 2026-06-09): daily
  6:15am cron + webhook `plaid-balances-sync`. Writes one row per account (12 accounts) to the MASTER's
  `Balances` tab — institution, name, mask, type, available/current/limit, as_of. NOTE: the Plaid account does
  NOT have the standalone `balance` product — balances come from the `accounts` block of `/transactions/get`
  (a 1-day window with count:1); do not "fix" it back to `/accounts/balance/get` (INVALID_PRODUCT).
  Institution tokens are duplicated from the Multi-Sync workflow's `Set All Institution Tokens` node — if tokens
  rotate, update BOTH workflows.
- **Old finance files are deprecated** — renamed "OLD — … DO NOT USE" where API access allowed. Sharon's old
  "Finances 2026 .xlsx" (`1ibvrsfnWNJOlRL0GDXQEu7ZZp_brEKGa`) is the pre-merge backup; manual entry now happens
  in the MASTER's entity tabs. A converted backup of the merged tabs lives at "MERGE SOURCE — Finances 2026
  converted (backup)" (`1gbP-kfu0vnlKS6_V4fDzUY9NjWSfWaR-KQlL3HO2U3w`).
- **KNOWN ISSUE:** both n8n Google **Drive** OAuth credentials ("Google Drive account", "Google Drive account 2")
  have expired/revoked refresh tokens (EAUTH). The Google **Sheets** credential (`AkBUwX11QA8RRHec`) works and
  has `spreadsheets` + `drive.file` scope — full Sheets API on any spreadsheet, Drive API only on app-created
  files. Until a Drive credential is reconnected in the n8n UI, old xlsx files can't be renamed/moved via API.
- **"FIN — Live Dashboard (web app)"** is ACTIVE (id `22Yn7HY5zuSMCURD`, built 2026-06-09): a GET webhook at
  `/webhook/finance-dashboard?key=<secret>` that renders a phone-friendly HTML dashboard LIVE from the MASTER on
  every load — cash on hand, credit cards owed, monthly spend trend, per-card and per-category spend, entity
  totals (from Detail Ledger routing; unrouted shows as "no rule"), open Closings vs cash check (60-day
  horizon), and the Missing Receipts list. The secret key lives ONLY in the workflow's `Build HTML` Code node
  (never commit it to this public repo). Deliberately NOT published to GitHub Pages — finance data stays private
  behind n8n. Goes down when the Mac Studio tunnel is down (same as everything else here).
- **"Closings" tab** added to the MASTER (Property, Client, Side, Close Date, Cash Needed $, Cash Incoming $,
  Status, Notes). Graeham/Sharon enter escrows there; the dashboard computes cash-needed-vs-available.
- One-off consolidation workflows (deactivated, kept for reference): `FIN — Consolidate Master v2` (xlsx upload
  → convert → copyTo merge), `FIN — Rename Old Sheets`, `FIN — Add Closings Tab`, `FIN — Drive Cred Test`.
- The go-live sequence below is the FALLBACK for when the pipeline is down or lost; check the live state first.

## What this system actually is (read this first)
Graeham does **not** have, and cannot have, a "log into Plaid and see Chase live" button. Plaid is plumbing
that sits *behind* an app — there is no consumer Plaid dashboard of transactions. The thing that pulls his
bank data **is an n8n workflow that acts as the Plaid client.** Claude never queries Chase directly; Claude
reads the **output** of this pipeline (the Google Sheet / a CSV export).

```
Chase accounts ──Plaid API──> n8n workflow ──> Finance Google Sheet ──> entity tax tabs
SparkReceipt (receipts) ──────────────────────> same sheet (Receipt Match ID)
```

- **Plaid** → bank transactions (txn_id, date, account, merchant, category, amount).
- **SparkReceipt** → receipt images, tagged by Entity + Category (see `Receipt-Workflow-SOP.md`). Cloud SaaS,
  independent of n8n.
- **n8n** (self-hosted on the Mac Studio, tunneled at `n8n.graehamwattsn8n.com`) → the glue that runs the
  Plaid pull and writes rows. **This is the fragile part.**
- **Destination schema** (canonical row, from `Claude_2026_Finances_Skeleton.xlsx` → tab `GW Personal`):
  `Date | Vendor / Description | Payment Method | Amount | Category | Health Insurance | Notes | Receipt Match ID | Auto-Tag Source | txn_id (from Plaid)`
- **Routing**: the `Tagging Rules` tab (Match Type, Vendor Pattern, Entity, Property, Category, IRS Line,
  Confidence) maps each transaction to an entity (GW Personal, Realtor Faraday, GW Property, Enterprise
  Holdings, Endeavour Enterprises, PROP IQ) and an IRS line.

## Known failure mode (this is why it breaks)
The n8n instance was migrated off `graehamwatts.app.n8n.cloud` onto the Mac Studio tunnel. When the Mac is
asleep/off or the Cloudflare tunnel (`cloudflared`) isn't running, the host returns **HTTP 530** and the
whole pipeline stalls. The freshest data Claude can see is then whatever was last exported
(`Documents/Skills LLMS/Claude/chase_transactions.csv`). **A 530 = the box/tunnel is down, not a credential problem.**

## STEP 1 — Always check the host first
Run `mcp__n8n-mcp__n8n_health_check` (mode=status).
- **connected:false / 530** → pipeline is DOWN. Tell Graeham plainly. The fix is on the Mac Studio: wake it,
  confirm n8n is running, confirm `cloudflared` is up. Re-check `https://n8n.graehamwattsn8n.com/healthz`
  (should return `{"status":"ok"}`). Do NOT pretend live data is available — read the CSV snapshot instead
  and label it with its date.
- **connected:true** → proceed to go-live.

## STEP 2 — Go-live sequence (run the moment n8n is back)
1. `n8n_health_check` → confirm connected:true.
2. `n8n_list_workflows` → look for a Plaid / bank / transactions workflow.
3. **If it exists** → trigger it, then read the sheet.
4. **If it does NOT exist** (likely — it was lost in the migration) → deploy the rebuilt one:
   `n8n_create_workflow` using `assets/plaid-transactions-to-sheets.json`. Then fill the 3 inputs below,
   activate, and trigger.
5. Read the resulting rows and reconcile against SparkReceipt (`receipt_match` / Receipt Match ID).
6. Report: new transactions, anything untagged (❌ VERIFY), and any tax-relevant items (e.g. FTB payments).

## STEP 3 — The 3 inputs the workflow needs (Graeham fills once)
1. **Plaid credentials** → set as n8n ENV vars: `PLAID_CLIENT_ID`, `PLAID_SECRET`, `PLAID_ACCESS_TOKEN`
   (the access token for the linked Chase Item), `PLAID_ENV` (`production`). These are NOT stored in any
   file on disk — they live only in n8n (or were issued when the Chase Item was linked). If the access
   token was lost in the migration, the Chase Item must be re-linked via Plaid Link to mint a new one.
3. **Google Sheet ID** → the finance sheet's ID, set on the `Append to Finance Sheet` node, plus the target
   tab name (default `Bank Transactions`).
3. **Google Sheets credential** → select Graeham's Google OAuth credential on that same node.

## If Graeham wants live access WITHOUT n8n
Two honest options — both are builds, not logins:
- **Read the live Google Sheet** via a connected Google Drive/Sheets connector (the SparkReceipt side keeps
  it current even while n8n is down). Fastest path to fresh *expense* data.
- **Dedicated Plaid MCP** added in Settings → Connectors with his Plaid keys → gives Claude direct Plaid
  access independent of n8n. Requires standing up a Plaid MCP server.

## Files this skill relies on (in Graeham's Documents)
- `Claude/Receipt-Workflow-SOP.md` — the SparkReceipt side, plain-English.
- `Claude/Claude_2026_Finances_Skeleton.xlsx` — canonical schema + `Tagging Rules` + `Property Master`.
- `Claude/chase_transactions.csv` — last Plaid export (snapshot; check its newest date before quoting it).
- `Claude/Skills/n8n-workflows/` — where workflow JSON exports live (this rebuild is added here).
- `assets/plaid-transactions-to-sheets.json` — the rebuilt, deploy-ready workflow.
- `assets/go-live-prompt.md` — the one-paste prompt to run when n8n is back.

## Hard rules
- Never claim live Chase access when `n8n_health_check` is not `connected:true`. Read the snapshot and date it.
- Never invent transaction numbers. If reading the CSV, say "as of <newest date in file>."
- Secrets stay in n8n ENV / the credential store, never written into the workflow JSON or into chat.
