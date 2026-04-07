# Offer Summary Format Reference

This reference shows how Graeham's team currently organizes offer summaries for multiple-offer situations. The skill should produce output that follows this structure but is more polished and includes net sheets.

## Standard Offer Summary Columns

Based on real offer summary spreadsheets, these are the fields tracked for each offer:

### Core Columns (Always Include)
| Column | Description | Example Values |
|--------|-------------|---------------|
| Buyer/s | Full name(s) of the buyer(s) | "Patrick Ayers, Molly Ayers" |
| Agent | Buyer's agent name | May not always be listed |
| Offer Price | The purchase price offered | $1,130,000 / "$1,085,000 — Offer expires Saturday at 5pm" |
| Deposit (EMD) | Earnest money deposit — amount, percentage, and timing | "$33,900 / 3% / within 1 business day" |
| Down Payment | Down payment percentage or "All Cash" | 35%, 20%, "All Cash" |
| COE Timeframe | Close of escrow date or number of days | "March 23, 2026" or "30 days" |
| Loan Contingency | Days or "waived" | "waived", "10 days", "7 days" |
| Appraisal Contingency | Days or "waived" | "5 days", "10 days", "waived" |
| Disclosures/Reports Contingency | Days or "waived" | "waived", "5 Days" |

### Additional Columns (Include When Relevant)
| Column | Description | Example Values |
|--------|-------------|---------------|
| CAR Form Received? | Whether the standard CAR forms were submitted | "Yes" / "No" |
| Counter Offer? | Whether a counter was issued | "--" or details |
| Buyer Agent Compensation | What the buyer's agent is asking the seller to pay | "2.5%" or "--" |
| Other Terms / Notes | Catch-all for special conditions | "3 days Insurance Contingency and 5 days Prelim Contingency / 2.5% Seller to pay buyer agent compensation / Seller to pay Home Warranty not to exceed $650 / Escrow - Buyer prefers Fidelity National Title" |

## Notes on Real-World Data

### Offer Price Can Include Context
Sometimes the offer price cell includes more than just a number — expiration dates, conditions, etc. Extract the number cleanly but preserve the context in notes. Example: "$1,085,000 — Offer expires Saturday at 5pm"

### Deposit Formatting
Teams often show deposit as a combined format: "$33,900 / 3% / within 1 business day" — amount, percentage of offer price, and deposit timing all in one cell. The skill should extract these as separate data points but can present them together.

### Down Payment Can Indicate Financing Type
- 100% or "All Cash" = cash offer, no loan
- 20%+ = conventional loan, strong position
- 10-20% = conventional or jumbo, depends on lender
- 3.5% = likely FHA
- 0% = likely VA

### The "Other Terms" Column Is Critical
This is where the important nuances live — things like:
- Buyer agent compensation requests
- Seller-paid home warranty requests
- Escrow/title company preferences
- Insurance contingencies
- Prelim (preliminary title report) contingencies
- As-is language
- Rent-back requests
- Contingent on sale of buyer's property
- Escalation clauses

The skill needs to parse these notes carefully and present each item clearly rather than dumping them all into one block of text.

## Presentation Order

When ranking offers, the strongest offer should be listed first (leftmost column in a spreadsheet, first card in the HTML view). But always make it clear that the ranking is a suggestion — the seller and their agent make the final call.
