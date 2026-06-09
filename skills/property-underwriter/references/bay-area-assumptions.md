# Bay Area / Peninsula Underwriting Assumptions

These are **starting defaults** to get a first pass fast. Override per deal. The three flagged ⚠️ items move the answer the most and must be **verified from a primary source** before the underwrite is trusted — do not present them as fact.

## ⚠️ Property tax (CA — the big one)
California reassesses to the **purchase price** on sale (Prop 13), so the tax is based on what the investor pays, not the seller's old basis. Model:
- **Effective rate ≈ 1.1%–1.25% of purchase price/yr** as a starting estimate (1% base + local voter-approved bonds/assessments; **Mello-Roos** adds more in some newer districts).
- A **supplemental tax bill** hits in year 1 for the jump from old to new assessed value.
- **VERIFY per parcel** at the county assessor / current tax bill — San Mateo vs Santa Clara vs Alameda differ, and Mello-Roos varies by subdivision. Graeham has `Documents\Transfer Tax Rates List of Counties.pdf` for the transfer side.

## ⚠️ Transfer tax (at purchase and exit)
- **County documentary transfer tax = $1.10 per $1,000** of price ($0.55/$500) — the California baseline.
- **Some cities add a city transfer tax on top** (e.g., the city of San Mateo). Many Peninsula cities charge only the county rate. **VERIFY the specific city** — it changes closing and exit costs. Don't assume.

## ⚠️ Rent control (caps the rent-growth assumption)
- **AB 1482 (statewide):** rent increases capped at **CPI + 5%, max 10%/yr**, plus just-cause eviction, for qualifying properties. **Exempt:** single-family homes/condos *not* owned by a corporation/REIT (with proper notice), and housing built within the **last 15 years** (rolling).
- **Local ordinances can be stricter and override AB 1482.** Known stricter local control on Graeham's turf includes **East Palo Alto** (rent stabilization) and **Mountain View** (CSFRA). **VERIFY the local ordinance per city** before modeling rent growth — Graeham has `Documents\Rent Control In California\` and `East Palo Alto Rent control Questions\`.

## Income & operating defaults
| Line | Default | Note |
|---|---|---|
| Vacancy & credit loss | **5%** | Peninsula is tight; 5% is a conservative baseline |
| Property management | **8% of EGI** | If self-managed, set to 0 but keep a shadow figure |
| Repairs & maintenance | **5–8% of EGI** | Older Peninsula stock trends higher |
| Reserves / CapEx | **~$250–300 / unit / mo** (or 5% EGI) | Roof, systems, turnover |
| Insurance | **Get a real quote** | CA premiums rising; FAIR plan in wildfire zones — don't default-guess |
| Market rent | **Pull it** | PropSearch estimate / RentCast / comps — never guess |

## Transaction & exit
- **Buyer closing costs:** ~1–2% of price (title, escrow, lender) — verify.
- **Selling costs at exit:** model **6%** (commissions + transfer + escrow) — verify.
- **Hold period:** default **5 years**.
- **Appreciation / rent growth:** model conservatively and always show a **0% appreciation** bear row — on the Peninsula the deal often lives or dies on appreciation, so make that explicit rather than buried.

## ADU upside (pairs with PropSearch Zoneomics)
- Only model ADU income **after** zoning confirms it's permitted (Zoneomics flag from PropSearch).
- **ADU build cost** in the Bay Area ranges widely (~$150k–$400k+) — **get a real bid**, don't default. Show incremental NOI ÷ cost = ADU yield, and the post-ADU value lift at market cap.

## Quick sanity screens (before a full build)
- **1% rule** (monthly rent ≥ 1% of price): almost never true on the Peninsula — don't reject a deal on this alone here; appreciation + ADU + rent control exemption status carry more weight.
- **DSCR ≥ 1.20–1.25** is the typical lender floor — if NOI doesn't cover it, the financing assumption is the problem.
- **GRM** (price ÷ annual GPR) — fast relative screen across comps, not a valuation.
