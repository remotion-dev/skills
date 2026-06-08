---
name: past-client-follow-up-system
description: "Past Client Follow-up System (PCFS) — central hub for Graeham Watts' past-client operations. Use ANY time Graeham mentions: PCFS, past client follow up, new deal closed, just closed, COE today, onboard new client, add new past client, new buyer closed, new seller closed, just funded, sync new deal, push new deal to GHL, edit past client, update address, fix client info, pause PCFS, unsubscribe from PCFS, stop follow up, mark deceased, snooze contact, audit PCFS, check PCFS health, missing COE dates, anniversary date wrong, cadence not firing, daily call rotation, anniversary batch, CMA digest, Sharon notes, Adrian briefing, birthday touch, By_Date events, propagate contact to GHL, or anything touching Master_Past_Clients Google Sheet, the Excel master, or GoHighLevel COE_date custom field. Also trigger on: add this person to my system, set up follow-up, put in the rotation, enroll in PCFS, fix a client record, or pasting a closing summary."
---

# Past Client Follow-up System (PCFS)

You are the central agent for Graeham Watts' Past Client Follow-up System. The PCFS is the operational backbone for staying in touch with every past client through their lifetime. This skill is the single entry point for every operation that touches it — onboarding new deals, editing existing contacts, pausing/unsubscribing, auditing data quality, and answering questions about how the cadences fire.

**Why this skill exists**: The PCFS has 7 active cadence workflows, 2 systems of record (Google Sheet + Excel master), and 1 CRM (GoHighLevel) with custom fields that drive everything. Mutations need to propagate across all three systems in lockstep or the cadences misfire. This skill encodes the right propagation pattern for every common operation so nothing drifts out of sync.

---

## What This Skill Handles

| Operation | When it fires | Section below |
|---|---|---|
| **New-deal onboarding** | A deal closes, contact needs to enter the system | "New-Deal Onboarding" |
| **Contact edit** | Address change, phone/email correction, family member add | "Contact Edits" |
| **Pause / unsubscribe / mark deceased** | Contact opts out, dies, or asks to be paused | "Pause / Unsubscribe / Deceased" |
| **Audit / health check** | Is data clean? Are cadences firing? Anyone missing? | "Audit Mode" |
| **Cadence question** | "When does X hit anniversary?", "Why didn't Y get the email?" | "Cadence Lookups" |
| **Bulk operations** | Apply Skyslope research, mass COE update, restructure | Defer to ad-hoc N8N work — flag and escalate |

Pick the right section based on what Graeham asked. If unclear, ask once with AskUserQuestion before doing anything.

---

## System Map (read this first, every session)

| System | What's stored | How updated |
|---|---|---|
| **Google Sheet** `Master_Past_Clients` (29 cols) | Operational source of truth — every cadence reads this | N8N workflow `3BsV1POSI3pdKNmY` (Targeted Sheet batch update) or direct Sheets API |
| **Google Sheet** `By_Date` | Anniversary + CMA event rows that drive Daily Call, Anniversary Batch, CMA Digest | Append rows directly |
| **GoHighLevel** | Live CRM, has `COE_date` custom field (`MYBybCgfZiUZTl9aSvSd`), `Selling Property Address` (`aMXm4T9X30OrJmCbFz4l`), `Buying Property Address` (verify ID), tags | N8N workflows: `rwgvg3NFd53pqbdm` (new-deal upsert), `1EiwS1ttwyHXAR0V` (update contact), `Mz9p77tNAdW6Jrne` (push COE only) |
| **Excel master** `Past_Client_Master_FINAL_v*.xlsx` | Graeham's downloadable backup, 26 cols | xlsx skill, regenerate after meaningful edits |

**7 active cadence workflows** (don't touch unless asked):
- `whjMmVXawdg1Ingx` — Daily Call Email (Mon-Fri 10am)
- `oNUrUUXCtdaZXUcr` — Monthly Anniversary Batch (24th 9am)
- `LHGnZC2X2KKXljB0` — CMA Weekly Digest (Mon 9am)
- `lS3ZMPHQA92AoyJt` — Bimonthly Market Update (24th of odd months 9am)
- `nxoRGbUYh5b4SxoK` — Monthly Birthday Touch (24th 10am)
- `7CxqNkCQAuw1noGL` — Sharon Weekly Notes (Mon 8am)
- `zrUVXmEE3Bso72RU` — Adrian Weekly Briefing (Mon 7am)

---

## New-Deal Onboarding

This is the most common operation. When Graeham closes a deal, propagate the contact into every system in one pass.

---

## Inputs You Need from Graeham

Before doing anything, collect these. Use AskUserQuestion if any are missing — do NOT guess. If Graeham pastes a closing summary, parse what you can and ask for the rest.

**Required**:
1. **Full name** (First + Last)
2. **Email** (primary)
3. **Phone** (E.164 or 10-digit, you'll normalize to +1XXXXXXXXXX)
4. **Buyer or Seller?** (B / S — the role on THIS deal)
5. **COE date** (YYYY-MM-DD — close of escrow date)
6. **Property address** (full address: street, city, state, zip — this is the property they bought OR sold)

**Optional but valuable**:
7. **EPA?** (Y/N — is the property in East Palo Alto? Drives the EPA-segmented Bimonthly Market Update cadence)
8. **Birthday** (YYYY-MM-DD or just MM-DD — feeds Birthday Touch cadence)
9. **Family member** (spouse/partner name — preserves context like "Brian Zimmerman, wife Danielle")
10. **Notes** (anything Graeham wants to remember — referral source, kid names, dog names, etc.)
11. **Existing GHL Contact ID** (if Graeham already created the contact in GHL during the transaction; if not, the skill creates one)

**Confirm back to Graeham before pushing anything.** Show a one-line summary like:
> About to onboard: Jane Smith (B), jane@email.com, +14155551234, COE 2026-04-29, 123 Main St San Jose CA 95129, EPA: N, BD: 1985-07-12, Family: husband Tom. Confirm?

Only proceed on a clear "yes / go / confirm".

---

## What This Skill Writes (and Why)

| System | What gets written | Why it matters |
|---|---|---|
| **Google Sheet** `Master_Past_Clients` | New row with all 29 columns populated | Source of truth that ALL N8N cadence workflows read from |
| **Google Sheet** `By_Date` | 4-6 calculated event rows | Drives Daily Call rotation, Anniversary Batch, CMA Digest |
| **GoHighLevel** | Contact updated/created with `COE_date` custom field, address, Buying/Selling Property Address custom fields, EPA/Buyer/Seller tags | GHL is what Graeham uses live; cadences cross-reference COE_date for trigger timing |
| **Excel master** | New row appended to local Excel file (latest version) | Graeham's downloadable backup / audit trail |

---

## Phase 1: Validate + Compute Derived Fields

Once Graeham confirms inputs, compute these BEFORE any writes:

1. **Anniversary (next)** = COE date + 1 year if COE < today, else COE date itself. Bump forward by years until > today.
2. **Anniversary Month** = month name of Anniversary (next)
3. **Call Rotation Week (1-13)** = `((day_of_year(Anniversary) - 1) % 91) // 7 + 1` — distributes contacts across 13 weeks for Sharon's call rotation
4. **PCFS Active?** = `Y` (default — only flip to N if Graeham says so)
5. **MLS Verified?** = `Y` (we trust closing data)
6. **Buying Address** vs **Selling Address**:
   - If `Buyer or Seller? == B` → Property goes in **Buying Address**, Selling Address blank
   - If `Buyer or Seller? == S` → Property goes in **Selling Address**, Buying Address blank
7. **Address / City / State / Zip** = the property address parsed (this is the contact's CURRENT residence — for buyers it's the property they just bought; for sellers it's whatever they confirmed as their new residence — ASK if unclear)

**Edge case to flag**: If seller is moving (most common), Graeham needs to tell you their NEW residence. The Selling Address is what they sold; the main Address columns are where they live NOW. If unclear, ask: *"Is [seller name] staying in the area? What's their current residence address now that they've sold [property]?"*

---

## Phase 2: Push to GoHighLevel (FIRST)

Push to GHL first because we need the Contact ID to use as the canonical key in the Sheet/Excel.

**Use N8N workflow `rwgvg3NFd53pqbdm` (PCFS — New Deal Onboarding (GHL Push))** — webhook trigger, accepts JSON body:

```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane@email.com",
  "phone": "+14155551234",
  "address1": "123 Main St",
  "city": "San Jose",
  "state": "CA",
  "postal_code": "95129",
  "coe_date": "2026-04-29",
  "buyer_or_seller": "B",
  "buying_address": "123 Main St San Jose CA 95129",
  "selling_address": "",
  "epa": "N",
  "birthday": "1985-07-12",
  "tags_to_add": ["past-client", "buyer", "2026"]
}
```

Webhook URL: `https://graehamwatts.app.n8n.cloud/webhook/pcfs-new-deal-ghl`

The workflow will:
- Search GHL for existing contact by email
- If found, UPDATE (PUT /contacts/{id})
- If not found, CREATE (POST /contacts/)
- Set custom field `COE_date` (ID: `MYBybCgfZiUZTl9aSvSd`) to COE date
- Set custom field `Buying Property Address` (ID: `bGn4kT9X30OrJmCbFz4l` — confirm before run, see references/data-spec.md) if buyer
- Set custom field `Selling Property Address` (ID: `aMXm4T9X30OrJmCbFz4l`) if seller
- Add tags: `past-client`, `buyer` or `seller`, `[year]`, `epa` if applicable
- Return `contactId` in response

**Capture the returned `contactId`** — that's the canonical key for everything else.

If the workflow returns an error (e.g., HTTP 422 on duplicate phone), surface it cleanly to Graeham and ask how to resolve before retrying.

---

## Phase 3: Append to Google Sheet (Master_Past_Clients)

Use N8N workflow `3BsV1POSI3pdKNmY` (Targeted Sheet batch update) OR call Google Sheets API directly via `mcp__workspace__bash` with the credential we already have configured.

**Tab**: `Master_Past_Clients`
**Spreadsheet ID**: stored in N8N credential `wIsb5mNoRmq7fh1Q`
**Operation**: append a new row

**Column order (29 cols, exact match required)**:

```
Contact ID | Full Name | First | Last | Email | Phone | Address | City | State | Zip | Buyer? | Seller? | EPA? | MLS Verified? | COE Date (verified) | Anniversary (next) | Anniversary Month | Birthday Known? | Birthday | Call Rotation Week (1-13) | Tags (planned for GHL) | Family Member | Notes | Buying Address | Selling Address | PCFS Active? | PCFS Paused Until | Last Call Date | Last CMA Sent
```

**Cell rules**:
- For `Buyer?` and `Seller?` — populate `Y` for the role on this deal, blank otherwise. (A contact who bought AND sold gets Y/Y when their second deal hits.)
- `Birthday Known?` = `Y` if birthday provided, else blank
- `Last Call Date` and `Last CMA Sent` start blank — cadences update them
- `Tags (planned for GHL)` = comma-separated list matching what we sent to GHL
- Use the `__EMPTY__` sentinel for any trailing empty cells to prevent Sheets API trim (lessons learned the hard way)

After append, verify by reading the row back and confirming Contact ID is in column A.

---

## Phase 4: Add Events to By_Date Tab

The `By_Date` tab drives Daily Call email + monthly events. For each new contact, add 2 recurring events:

| Event Type | Date | Notes |
|---|---|---|
| Anniversary | Anniversary (next) | Triggers Anniversary Batch on the 24th of that month |
| CMA Send | Anniversary (next) - 6 months | Triggers CMA Digest 6 months after anniversary |

Append both rows to `By_Date`. Columns (typical structure):
`Date | Contact ID | Full Name | Event Type | Property Address | Notes`

If the Anniversary - 6 months date is in the past, skip the CMA row (the next year's cycle will pick it up).

---

## Phase 5: Update Excel Master

Read the latest `Past_Client_Master_FINAL_v*.xlsx` from `outputs/`. Use the `xlsx` skill (Read its SKILL.md first if you haven't this session).

Append a new row to the `Master_Past_Clients` sheet matching the Excel column order (26 cols — see `references/data-spec.md` for the Excel-vs-Sheet column map). Excel has 4 columns the Sheet doesn't:
- `Multi-Property?` = `N` (default, set Y if they have multiple properties)
- `Confidence` = `High` (we just closed the deal — this is verified)
- `Source` = `New Close` or `MLS-verified`
- `Property History (multi)` = blank for first deal, populated for repeat clients

Save as `Past_Client_Master_FINAL_v[N+1]_[YYYY-MM-DD].xlsx`. Provide a `computer://` link.

---

## Phase 6: Confirm + Summary

Reply to Graeham with a clean summary:

```
Onboarded Jane Smith into PCFS
  Contact ID: AbC123xYz
  GHL: updated (COE 2026-04-29 set, tagged past-client/buyer/2026)
  Sheet: appended at row 281
  By_Date: 2 events added (Anniversary 2027-04-29, CMA 2026-10-29)
  Excel: Past_Client_Master_FINAL_v6_2026-04-29.xlsx

Next contact will hit:
  - Daily Call rotation: Week 17 starting 2027-04-23
  - Anniversary Batch: April 2027
  - CMA Digest: October 2026 (Mon following 10/29)
  - Birthday Touch: July 2026 (if birthday provided)
```

Include the Excel file link.

---

## Error Handling

**If GHL push fails** → Stop. Don't write to Sheet/Excel until GHL is resolved. Surface the exact error to Graeham. Common causes:
- Duplicate phone (HTTP 422) — search by phone, ask Graeham if it's the same person
- Bad email format — re-prompt
- Rate limit (HTTP 429) — wait 60s, retry once, then surface

**If Sheet append fails** → Roll back GHL? No — GHL is canonical, the Sheet should follow. Retry the Sheet append up to 2x, then surface error and tell Graeham the contact IS in GHL but Sheet needs manual fix. Provide the row data so they can paste it in.

**If Excel update fails** → Don't sweat it. The Sheet is the operational source of truth; Excel is the backup. Tell Graeham, regenerate Excel from Sheet on next pass.

---

## Repeat Clients (Second Deal)

If Graeham onboards a contact who already exists (matched by email or phone):
1. Don't create a duplicate — UPDATE the existing row
2. Flip the appropriate Buyer/Seller column to `Y` (so it might end up Y/Y)
3. UPDATE COE Date to the most recent close (this becomes the active anniversary)
4. UPDATE Anniversary (next) and Call Rotation Week
5. APPEND to the Property History (multi) column in Excel: `[old COE] [old address]; [new COE] [new address]`
6. Set `Multi-Property?` = `Y` in Excel
7. Re-run By_Date events for the NEW anniversary (delete old anniversary events first)

Confirm with Graeham before doing this — sometimes it's a different person with a similar name.

---

## Contact Edits

When Graeham wants to fix or update info on an EXISTING past client (address change, phone correction, family member add, notes update, etc.):

**Workflow**:
1. Look up the contact by name → confirm Contact ID with Graeham
2. Determine which fields are changing
3. Build the change set in this order: GHL → Sheet → Excel
   - GHL via N8N workflow `1EiwS1ttwyHXAR0V` (GHL Update Contact) for address1/city/state/postalCode + custom fields
   - Sheet via `3BsV1POSI3pdKNmY` (Targeted Sheet batch update) — patch only the cells that changed
   - Excel — regenerate from Sheet, or hand-edit if a single cell change
4. **Preserve the Notes column.** Always READ the existing notes first, then APPEND new info as a sentence. Never overwrite.
5. If the change is "primary residence vs investment property" (like the Linda Li / Liz Lucas / Brian Zimmerman corrections), update the main Address columns AND the Selling/Buying Address columns separately, AND update the GHL `Selling Property Address` custom field if it's a sold property.

**Confirm before pushing**: show Graeham the diff before any writes happen.

---

## Pause / Unsubscribe / Deceased

When a contact opts out, asks for a pause, or has died:

**For "pause until [date]"**:
- Set `PCFS Active?` = `N` and `PCFS Paused Until` = `YYYY-MM-DD` in Sheet
- No GHL change needed (cadences read PCFS Active flag from Sheet)
- Tell Graeham when the pause expires

**For "unsubscribe permanently"**:
- Set `PCFS Active?` = `N` (no expiry) in Sheet
- Add tag `unsubscribed` in GHL via workflow `1EiwS1ttwyHXAR0V`
- Append "[YYYY-MM-DD] Unsubscribed from PCFS — [reason]" to Notes
- Confirm with Graeham — this is a permanent action

**For "deceased"**:
- Set `PCFS Active?` = `N` permanently
- Add tag `deceased` in GHL
- Append "[YYYY-MM-DD] Deceased — [optional context]" to Notes
- If a spouse/family member is in the system as a separate contact, ASK Graeham whether to flag for special handling (the cadences shouldn't send "happy anniversary on your home" if it triggers grief)
- Be sensitive — this is real for Graeham's relationship with these people

---

## Audit Mode

When Graeham wants a health check on the PCFS:

**Quick checks** (you can run these without permission):
1. Count rows in Sheet `Master_Past_Clients` — flag if changed unexpectedly since last audit
2. Count rows missing COE Date (verified) — should be a known small number
3. Count rows where `PCFS Active?` ≠ `Y` — confirm the pause/unsubscribe list matches Graeham's expectations
4. Spot-check 3 random rows: do anniversary, COE, and Anniversary Month agree?
5. Pull next 30 days of `By_Date` events — confirm cadences will fire as expected

**Deeper audit** (ask Graeham first):
1. Compare Sheet COE dates against GHL `COE_date` custom field — flag mismatches
2. Compare Sheet vs Excel master row counts — flag drift
3. Pull last 7 days of cadence workflow executions from N8N — confirm none failed silently
4. Flag any contact who hasn't been touched (`Last Call Date` and `Last CMA Sent` both blank or stale > 1 year) and isn't on a pause

For suspicious findings, present to Graeham with a clear "fix Y/N?" prompt before changing anything.

---

## Zero-Guard: Trust No Zero (added 2026-06-07)

Hard rule born from the June 2026 failures: a PCFS email that reports **0 items is guilty until proven innocent**. History shows zeros are usually a broken feed (dead OAuth token, schedule horizon expiry, date-format mismatch, filter bug), not a quiet day.

**In the workflows (implemented 2026-06-07):** the Build Email code in Sharon (`7CxqNkCQAuw1noGL`), Daily Call (`whjMmVXawdg1Ingx`), and CMA Digest (`LHGnZC2X2KKXljB0`) self-verifies before every send:

- Every email carries a 🛡️ Self-check footer: total rows read, action-type rows in schedule, this-week count, next upcoming item with date, and schedule horizon date.
- A zero result is cross-checked before sending. A benign zero (weekend, genuine gap) sends with "Zero verified against the full schedule." A suspicious zero (sheet read empty, zero rows of that action type anywhere, items exist but got filtered out, horizon expired) sends a red "⚠️ ZERO FAILED SELF-CHECK" banner and the subject gets prefixed "⚠️ VERIFY —".
- Horizon early-warning: the footer warns when a schedule runs out within 45 days (65 for calls). As of 2026-06-07 the live call schedule ends Fri Aug 7 2026, so the warning shows in every call email until the schedule is regenerated.

**For Claude sessions (you):**

1. NEVER accept a 0-count PCFS email at face value during audits. Cross-reference the live `Actions By Date` tab, not just the local Excel (see fork warning below).
2. If a zero email arrives WITHOUT the 🛡️ Self-check footer, the workflow code regressed. Re-apply the zero-guard.
3. When modifying any Build Email code, preserve the zero-guard block (variables prefixed `__`). Test changes on a temp staging workflow first (webhook → same sheet reads → patched code, NO Gmail node, `simNow` override in the webhook body to simulate other days) before touching production. Delete temp workflows when done.
4. The watchdog catches missed or failed executions; the zero-guard catches successful-but-wrong ones. Both must stay.

**Schedule fork — RESOLVED 2026-06-07 (unified rebuild executed):** the live `Actions By Date` tab is now the single canonical schedule: 2,897 rows covering May 11 2026 → Dec 31 2027 (1,629 Quarterly Calls in repeating 13-week cycles, 430 Handwritten Notes, 425 Anniversary Video