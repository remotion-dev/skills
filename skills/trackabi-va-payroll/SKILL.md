---
name: trackabi-va-payroll
description: Semi-monthly VA payroll run for Graeham Watts ("TrackBee VA assistance") — pulls each virtual assistant's Trackabi timesheet PDF, stages Wise payments one at a time for Graeham to personally approve, files the Wise receipt emails as PDFs, updates Peter's loan tracker, and sends per-person bookkeeping emails with both PDFs attached. Use ANY time Graeham says run the VA payroll, pay my VAs, pay my assistants, TrackBee, Trackabi, trackabi timesheets, pull the timesheets, VA timesheets, pay period, 1st to the 15th, 16th to the end of the month, Wise payments, pay Adrian/Eleanor/John/Jason/Giselle, timesheet PDFs, assistant payroll, bi-monthly payroll, or anything about paying or documenting his virtual assistants' hours. Also trigger on partial asks (just the timesheets, just the receipts, just the bookkeeping emails) — each step runs independently.
---

# Trackabi VA Payroll ("TrackBee VA assistance")

The complete semi-monthly payroll run for Graeham's virtual assistants. Pay periods are the **1st–15th** and **16th–end of month**; the run happens the day after a period closes (the 16th and the 1st). First full run: 2026-07-01 for Jun 16–30, 2026 — everything below is verified against that live run.

## The one non-negotiable rule

**Never click "Send now" in Wise. Ever.** Claude stages each transfer to the review screen and stops; Graeham clicks the send button himself, one transfer at a time. Everything else in this skill is fair game to automate.

## The roster

| Person | Trackabi member | Wise recipient | Notes |
|---|---|---|---|
| Adrian | Aboniawan, Joseph Adrian | "Joseph Adrian Dela Cruz Aboniawan" (Wisetag @josephadrianaboniawanj) | Instant delivery |
| Eleanor | Alabanza, Elenor | "Elenor Espiritu" — BPI ··1457 | Different surname is correct (Espiritu); she is Peter Jason's wife. Instant delivery |
| John | Dimapilis, John Angelo | "John Angelo Bordeos Dimapilis" — Wise PHP account | Delivery can take days |
| Peter Jason | Alabanza, Jason | "Peter Jason Alabanza" — BPI ··5373 (his OWN account) | Goes by both Peter and Jason. Has an active loan — see Step 3. BPI = ~3 working days (ACH funding) |
| Giselle | Bernal, Giselle | **NOT paid via Wise** | Virtudesk handles her pay. Pull her Trackabi PDF for records only. The "Giselle Andrade" recipient in Wise is unconfirmed — never use it without asking |

Payment amount = the **wage total from that person's Trackabi report, exactly**. Do not compute from hours × rate; Trackabi already did.

## Step 1 — Trackabi timesheet PDFs

Via Claude in Chrome (Graeham logged in) at `graeham-watts.trackabi.com`:

1. Sidebar **Company → Reports → Generate new report** (lands on /timesheet).
2. Date filter → **Range** tab. The two calendars are independent: **left calendar sets the START date, right calendar sets the END date** — clicking a date always sets that calendar's endpoint. Navigate each with its own Prev/Next.
3. **Member** filter → one person → **Save as report** (keep the default options, including "Exclude entries with zero billable time") → **Save report**.
4. Preview opens → **PDF** → **Portrait** (all existing files are Letter portrait).
5. PDF lands in Downloads named like the report. **Downloads stay locked by Chrome — use Copy-Item, not Move-Item**, into the destination; delete the Downloads leftovers at the end of the session (they unlock after a while).

Repeat for all five people (including Giselle).

### Filing destinations + exact naming (match each folder's existing pattern)

Base: `C:\Users\Graeham Watts\Documents\Assistants`. Examples from Jun 16–30 2026 — swap dates:

- Adrian → `Adrian Aboniawan\Adrain Aboniawian 06 16 26 to 06 30 26 Trackabi.pdf` — keep the existing "Adrain Aboniawian" misspelling
- Eleanor → `Elenor Alabanza\06 16 2026 06 30 2026 Alabanza, Elenor Trackabi.pdf`
- Peter Jason → `Peter Jason Alabanza\Peter Jason Alabanza 2026\06 16 2026 to 06 30 2026 Jason Alabanza Trackabi.pdf` (year subfolder)
- Giselle → `Giselle Bernal\Giselle Bernal 2026\06 16 26 - 06 30 2026 Giselle Bernal Trackabi.pdf` (year subfolder)
- John → `John Angelo Dimapilis\john Angelo Dimapilis 2026\06 16 2026 to 06 30 2026 John Angelo Dimapilis Trackabi.pdf` (year subfolder; lowercase "john" in folder name)

Wise receipts use the same pattern with `Wise` instead of `Trackabi`.

## Step 2 — Stage Wise payments (Graeham approves each)

At wise.com (Graeham logged in), for Adrian, Eleanor, John, and Jason — one at a time, since Wise stages one transfer per flow:

1. **Send** → pick the recipient from Recents/All accounts (verify full name and account ending against the roster above).
2. Amount = Trackabi wage total in **USD** (Jason: minus the loan deduction — Step 3).
3. Funding source should default to **PLAT BUS CHECKING ··3974** — verify it.
4. Reference: `MM DD to MM DD YY` (e.g. `06 16 to 06 30 26`). **No punctuation** — Wise rejects periods/special characters. Jason's reference appends ` minus 106` when the loan is deducted.
5. Continue to the **review screen and STOP.** Report the details (recipient, account ending, USD, PHP, reference) and let Graeham click **Send now**.
6. After he confirms, verify the transaction (screenshot shows "Transfer complete" or, for BPI, "Waiting for your money" — that's the normal ACH funding stage), then stage the next person.

## Step 3 — Peter's loan tracker

File: `Documents\Assistants\Peter Jason Alabanza\peter loan tracker.xlsx` (sheets: Summary, Ledger, Loan Schedule).

- Loan: $1,030 financed at 7%, 10 payments of **$106.33**. Ledger drives the Summary via formulas — fill only the input cells (wage, deduction, transfer #, date, status, notes) with openpyxl (`data_only=False` so formulas survive).
- **Before deducting, check the deduction is actually due** — history shows skipped periods (May 16–31 and Jun 1–15 2026 went out full-wage). Cross-check the Ledger against actual Wise payment history; when the tracker and reality disagree, Wise history wins. Correct the Ledger to match.
- When deducting: Jason's net = wage − 106.33. Log the row (payment N of 10), update the Summary "THIS PERIOD" block and "Last updated" date.
- Status as of Jul 1 2026: payment 5 of 10 done, remaining balance $522.49.
- Email Jason the updated tracker: **graehamwattsvideo@gmail.com**. The Gmail connector's create_draft DOES accept base64 attachments (ignore its description saying otherwise). Create a draft for Graeham to review/send, summarizing wage, deduction, net, and remaining balance.

## Step 4 — Wise receipt emails → PDFs

Wise's confirmation emails arrive at graehamwatts@gmail.com within minutes of each send. Instant transfers get "Transfer sent (#...)"; BPI transfers get "Transfer set up (#...)" first and "Transfer sent" days later when the money delivers — file what exists on run day, offer to swap in the final one later.

1. Gmail connector: `search_threads` query `from:wise.com newer_than:1d`, match transfer numbers to people.
2. `get_thread` each → extract `htmlBody`. If the result persists to a tool-results file, parse the JSON from there; if it comes inline, the body can be recovered byte-exact from the session transcript jsonl under `~/.claude/projects/<project>/` — don't retype it and don't reconstruct/fabricate email content.
3. Save each htmlBody as `.html`, then convert with headless Chrome (matches Graeham's existing receipts, which are Chrome print-to-PDFs):
   ```
   chrome.exe --headless --disable-gpu --user-data-dir=<scratch-profile> --no-pdf-header-footer --print-to-pdf="<dest>.pdf" "file:///<src>.html"
   ```
   Use a scratchpad `--user-data-dir` so it doesn't fight the open Chrome profile.
4. File per person with the Step 1 naming, `Wise` suffix. Giselle gets none.
5. **After conversion, delete the Wise emails from Gmail** — the PDFs are the permanent record. The Gmail connector cannot trash (label_thread with TRASH fails); use the Gmail tab in Chrome: search `from:wise.com newer_than:1d`, verify the result count matches the emails just converted, select all, click the trash icon, confirm the "moved to Trash" toast. Trash is recoverable for 30 days — never empty it.
6. **BPI follow-up (~3-5 working days later):** when a BPI recipient's final "Transfer sent (#...)" email arrives (Jason, and any future BPI transfers), convert it the same way, REPLACE the "Transfer set up" PDF in the folder, and trash that email too. Track this as an open item in the wrap-up report.

## Step 5 — Bookkeeping emails

One email **per person** (Adrian, Eleanor, John, Jason) to **graehamwattsbookeeping@gmail.com** (that spelling — "bookeeping"), SENT (not drafted) via `skills/switchy-engine/scripts/send_email.py` which supports repeatable `--attach`:

- Subject: `<Name> - Pay Period <MM DD YYYY> to <MM DD YYYY> - Trackabi + Wise`
- Body: HTML summary table — assistant, pay period, hours, wage, deduction, net paid, Wise transfer #, status — plus a note that Giselle (with her hours) is paid via Virtudesk, records-only.
- Attachments: that person's Trackabi PDF + Wise PDF.

## Wrap-up checklist

- All Trackabi PDFs filed (5 people) and Wise PDFs filed (4 people)
- All 4 transfers show Sent / funding-in-progress in Wise
- Loan tracker row complete with receipt # (when a deduction ran); draft to Jason created
- 4 bookkeeping emails sent
- Wise emails trashed after conversion (Gmail UI, not connector)
- Downloads leftovers deleted (retry later if still locked)
- Report a per-person summary table to Graeham: hours, wage, deduction, net, transfer #, delivery status — flag any pending BPI "Transfer sent" swap as an open item

## Known quirks

- Trackabi's SPA sometimes paints a stale recipient list after navigation — scroll up and re-read the page; the URL hash tells you the real step.
- Wise's send flow occasionally renders shifted/blank in screenshots — `get_page_text` is more reliable than screenshots for verifying the review screen.
- The memory file `trackabi-timesheet-run.md` in Claude's memory directory mirrors this workflow; if this SKILL.md and live reality diverge, trust reality, then update both.
- Full automation is intentionally out of scope until agents can hold their own logins — and even then, the Send click stays with Graeham.
