# Data Spec — Column Maps + GHL Field IDs

## Google Sheet `Master_Past_Clients` — 29 columns (exact order)

| # | Column | Notes |
|---|---|---|
| 1 | Contact ID | GHL Contact ID — canonical key |
| 2 | Full Name | "First Last" — display only |
| 3 | First | First name |
| 4 | Last | Last name |
| 5 | Email | Primary email |
| 6 | Phone | E.164 (+1XXXXXXXXXX) |
| 7 | Address | Current residence street |
| 8 | City | Current residence city |
| 9 | State | 2-letter (e.g., CA) |
| 10 | Zip | 5-digit |
| 11 | Buyer? | Y if any deal as buyer, blank otherwise |
| 12 | Seller? | Y if any deal as seller, blank otherwise |
| 13 | EPA? | Y if property in East Palo Alto |
| 14 | MLS Verified? | Y for closed deals (always Y for new closes) |
| 15 | COE Date (verified) | YYYY-MM-DD — most recent close |
| 16 | Anniversary (next) | YYYY-MM-DD — computed forward |
| 17 | Anniversary Month | Full month name (e.g., "April") |
| 18 | Birthday Known? | Y/blank |
| 19 | Birthday | YYYY-MM-DD or MM-DD |
| 20 | Call Rotation Week (1-13) | Sharon's call distribution |
| 21 | Tags (planned for GHL) | Comma-separated: past-client,buyer,2026 |
| 22 | Family Member | Spouse/partner name |
| 23 | Notes | Free text, preserve across updates |
| 24 | Buying Address | If they bought via Graeham |
| 25 | Selling Address | If they sold via Graeham |
| 26 | PCFS Active? | Y/N — pause flag |
| 27 | PCFS Paused Until | YYYY-MM-DD or blank |
| 28 | Last Call Date | Updated by Daily Call cadence |
| 29 | Last CMA Sent | Updated by CMA Digest cadence |

## Excel Master — 26 columns

Excel has 4 columns the Sheet doesn't, and skips 7 operational state cols.

| # | Column | Notes |
|---|---|---|
| 1 | Contact ID | Same as Sheet |
| 2 | Full Name | |
| 3 | First | |
| 4 | Last | |
| 5 | Email | |
| 6 | Phone | |
| 7 | Address | |
| 8 | City | |
| 9 | State | |
| 10 | Zip | |
| 11 | Buyer? | |
| 12 | Seller? | |
| 13 | EPA? | |
| 14 | MLS Verified? | |
| 15 | COE Date | |
| 16 | Anniversary (next) | |
| 17 | Anniversary Month | |
| 18 | Birthday Known? | |
| 19 | Birthday | |
| 20 | Family Member | |
| 21 | Notes | |
| 22 | Buying Address | |
| 23 | Selling Address | |
| 24 | Multi-Property? | Y/N — Excel only |
| 25 | Confidence | High/Medium/Low — Excel only |
| 26 | Source | New Close / MLS-verified / Skyslope / Manual — Excel only |

(Property History (multi) lives inside Notes for current Excel version — confirm by Reading the latest file before write)

## GoHighLevel Custom Field IDs

| Field Name | Field ID | Type |
|---|---|---|
| COE_date | `MYBybCgfZiUZTl9aSvSd` | DATE |
| Selling Property Address | `aMXm4T9X30OrJmCbFz4l` | TEXT |
| Buying Property Address | `bGn4kT9X30OrJmCbFz4l` | TEXT (verify before first push — pull /custom-fields if uncertain) |

**To verify field IDs**, call:
```
GET https://services.leadconnectorhq.com/locations/{locationId}/customFields
Authorization: Bearer {token}
Version: 2021-07-28
```

The location ID for Graeham's GHL: `6wuU3haUH7uNeT20E3UZ`

## Tag Taxonomy

Always apply on new-deal onboarding:
- `past-client` — universal flag for all closed clients
- `buyer` OR `seller` (or both for repeat clients)
- `[year]` — the year of COE (e.g., `2026`)
- `epa` — only if EPA? = Y
- `multi-property` — only on second-deal onboarding

Never apply automatically:
- `unsubscribed` — only via explicit user request
- `dnd` — manual only
- pipeline stage tags — managed by GHL workflows separately

## Anniversary Math

```python
# In bash via python3
from datetime import date
coe = date.fromisoformat("2026-04-29")
today = date.today()
anniv = coe.replace(year=coe.year + 1) if coe < today else coe
while anniv <= today:
    anniv = anniv.replace(year=anniv.year + 1)
# anniv is next anniversary
```

## Call Rotation Week (1-13)

13-week rotation distributes contacts roughly evenly. Formula:

```python
day_of_year = anniv.timetuple().tm_yday
week = ((day_of_year - 1) // 7) % 13 + 1
```

This is deterministic — same anniversary always lands on same week, so re-onboarding doesn't shuffle the rotation.
