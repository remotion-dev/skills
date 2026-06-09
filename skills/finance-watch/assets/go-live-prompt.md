# Go-Live Prompt — paste this the moment your Mac Studio n8n is back up

> Copy everything in the box below into a new message to Claude.

---

n8n is back online. Run the finance pipeline go-live using the **finance-watch** skill:

1. Run an n8n health check and confirm it's connected (not 530). If it's still down, stop and tell me — don't read stale data as if it's live.
2. Once connected, list my n8n workflows and look for a Plaid / bank / transactions workflow.
   - If it exists, trigger it.
   - If it does NOT exist, deploy the rebuilt one from the finance-watch skill's `assets/plaid-transactions-to-sheets.json`, then tell me exactly which of the 3 inputs (Plaid env vars, Google Sheet ID, Google Sheets credential) still need filling before it can run.
3. After the pull runs, read the finance sheet, reconcile against SparkReceipt, and give me: how many new transactions landed, anything left untagged (❌ VERIFY), and any tax-relevant items (especially CA FTB / franchise tax payments).
4. Confirm the date range you actually pulled so I know it's live, not the May snapshot.

---

## If you just want the latest numbers and don't care about n8n yet
Paste this instead:

> Read my latest finance data: pull `Documents/Claude/chase_transactions.csv` and tell me the newest transaction date in it, then summarize by account and flag anything tax-relevant. Label it clearly as "as of <newest date>", since this is the last snapshot, not a live pull.
