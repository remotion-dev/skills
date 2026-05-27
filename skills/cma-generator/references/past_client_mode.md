# Past-Client Mode — Home Value Update Layer

This layer turns the standard CMA into a warm, personalized **home-value update for an existing owner** who is NOT selling. It sits on top of the normal cma-generator methodology (same data rigor, same brand, same charts) but changes the framing, section set, and voice so it reads like a personal note from their agent — not a listing presentation or a buyer offer analysis.

Use it whenever the CMA is for a past client: PCFS cadence, "home value update," "equity update," anniversary touch, "keep them posted," or any owner who isn't actively listing.

---

## The mindset shift

A listing CMA answers "what should I list this for?" A past-client update answers **"what is my home worth right now, and how's my equity doing?"** The owner asked for nothing — Graeham is proactively keeping them informed because that's what a good agent does between transactions. So nothing in the piece should feel like a pitch.

---

## Section changes vs the standard (listing) report

| Standard listing section | Past-Client Mode |
|---|---|
| Hero: "Listing Presentation" / "Buyer Offer Analysis" | **"Home Value Update"** |
| "Pricing Strategy Analysis" (below / at / above market) | **DELETE.** Replace with "What Your Home Is Worth Today" |
| "Recommended List Price" — Conservative / Competitive / Stretch | **"Your Home's Value Today"** — Likely range / Most-likely value today / Top of range in strong condition |
| "The Market Story" written toward a pricing decision | Same data, written toward *where the owner stands* |
| Subject summary | Keep — but add ownership context (years owned, equity gained) when known |
| Comparable sales + $/sqft chart | Keep as-is |
| Market data & trends | Keep as-is |
| Special considerations | Keep — frame as "things that affect your value," not "things to fix before listing" |
| Closing | Warm, no-agenda sign-off from Graeham |

If a section would only make sense to someone about to sell (staging advice, list-timing strategy, days-on-market targets framed as "to sell fast"), cut or re-frame it.

---

## Voice rules

- Address the client by **first name** in the email and, where natural, the report intro.
- **No sales push.** Never "let's list," "ready to sell?", "call me to get started." The one soft offer allowed at the end: "if you ever want to talk through what a sale would actually net you, I'm here" — once, low-key.
- Lead with **equity and standing**, not price-to-list. If purchase price + date are known: "you bought in [year] for $X; comparable homes are now around $Y — that's roughly $Z in appreciation."
- Warm, plain, human. Run the final copy through the **humanizer** skill. No em-dash overuse, no "nestled," no corporate filler.
- Honesty intact: still flag thin comp data, condition unknowns, and "professional opinion of value, not a formal appraisal."

---

## Value section (replaces Pricing Strategy + Recommended List Price)

Header: **"What Your Home Is Worth Today"**. Three range cards, relabeled:

- **Likely range** (green accent) — the safe floor, accounting for condition/lot.
- **Most-likely value today** (gold accent) — anchored on the closest comps. This is the headline number.
- **Top of range in strong condition** (coral accent) — what it could reach if it shows turnkey.

Frame as current market value / equity, never as a list price. Keep the subject-positioning chart (where the home sits among comps).

---

## Companion email (for PCFS review-and-forward)

The report ships with a forward-ready client email. Build it as a Gmail DRAFT to Graeham + the clientcare inbox (never auto-send). Structure:

1. **Internal note** at top (delete-before-forwarding): what it is, the value range, the live link.
2. Divider.
3. **Client email** — suggested subject with a 🔥 fire emoji, warm first-name greeting, 2-3 short paragraphs (market is good to you / where your home stands / quick equity context), the CMA as a **clickable link/button**, and a no-agenda close.

### Example client email body (adapt per client)

> Subject: 🔥 A quick update on your [City] home
>
> Hi [First name],
>
> Hope you and the family are doing well! I was running some numbers this week and pulled a fresh read on [street], so I wanted to share where things stand.
>
> Short version: the market's been good to you. Homes like yours in [area] have been selling around [range], and based on the recent sales your place is most likely worth somewhere around **[most-likely value]** today[, with room toward [top] if it shows in top shape]. For perspective, that's [equity context vs purchase].
>
> I put together a quick visual breakdown — recent comparable sales, the charts, and where your home lands:
>
> [View your home value update →](LIVE_LINK)
>
> No agenda at all, just thought you'd want to know where you stand. Anytime you want to talk it through, I'm around.
>
> [Graeham sign-off + contact block]

---

## What stays identical to the standard skill

Brand (DRE #01466876 from `shared-references/identity.json`), the graehamwatts.com nav, Chart.js charts, comp-selection rules (1-mile / same-city / sqft range / recency), the mandatory QC verification pass, and GitHub Pages publishing. Past-Client Mode changes the *story and labels*, not the *data discipline*.
