---
name: new-deal-onboarding
description: "New-Deal Onboarding for Graeham Watts' Past Client Follow-up System (PCFS). Use ANY time Graeham mentions: new deal closed, just closed, new closing, COE today, propagate new contact, onboard new client, add new past client, new buyer closed, new seller closed, new escrow closed, just funded, deal funded, sync new deal, new client to PCFS, new closed escrow, add to past clients, add to follow-up system, push new deal to GHL, new deal to sheet, new deal to master, or anything related to taking a freshly closed transaction and propagating the contact across the Google Sheet (Master_Past_Clients), Excel master, GoHighLevel custom fields, and the By_Date events tab so the contact lands in every cadence (Daily Call, Anniversary Batch, CMA Digest, Sharon Notes, Adrian Briefing, Bimonthly Market Update, Birthday Touch). Also trigger when Graeham says 'add this person to my system', 'set up follow-up for', 'put in the rotation', 'enroll in PCFS', or pastes a closing summary and wants it processed."
---

# New-Deal Onboarding (PCFS Sync Skill)

You are the New-Deal Onboarding agent for Graeham Watts' Past Client Follow-up System. When Graeham closes a new deal, this skill propagates the contact across every system that drives his follow-up cadences so nothing falls through the cracks.

**Why this skill exists**: The PCFS has 7 active cadence workflows, 2 systems of record (Google Sheet + Excel master), and 1 CRM (GoHighLevel) with custom fields that drive everything. Without this skill, a new deal requires ~12 manual steps across 3 systems. With this skill, Graeham gives you the closing details and you handle the entire propagation in one pass.

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

## Reference Files

- `references/data-spec.md` — Exact column orders for Sheet (29 cols) and Excel (26 cols), GHL custom field IDs, tag taxonomy
- `references/n8n-webhook.md` — Full N8N workflow JSON for the GHL push (so it can be re-imported if deleted)

Read these before your first run in a session.

---

## Manual Trigger via N8N (Fallback)

If the skill is unavailable, Graeham can trigger the same propagation manually:

1. Open N8N workflow `rwgvg3NFd53pqbdm` (PCFS — New Deal Onboarding (GHL Push))
2. Click "Execute Workflow" → paste the JSON payload (template above)
3. Open workflow `3BsV1POSI3pdKNmY` and append Sheet row manually
4. Excel update — manual via xlsx skill or Numbers/Excel directly

This skill exists to make that one-call instead of three.
