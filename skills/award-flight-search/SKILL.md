---
name: award-flight-search
description: "Finds and books NEW premium-cabin award flights for Graeham Watts using Amex Membership Rewards and Bilt points. Maps his balances against transfer partners, catches the surcharge and season-cliff traps that destroy otherwise-good redemptions, cross-references destination seasonality, and drives point.me and airline sites through the browser. Use ANY time the user mentions: book a flight with points, award flight, award ticket, where can I go with my points, use my Amex points, use my Bilt points, Membership Rewards, MR points, transfer my points, transferable points, miles for a flight, business class with points, first class with points, premium cabin award, award availability, award space, point.me, seats.aero, award chart, sweet spot, cents per point on a flight, fuel surcharge, carrier imposed surcharge, ANA First, JAL First, Qantas First, Polaris, Atmos Rewards, Aeroplan, Flying Blue, Avianca LifeMiles, Virgin Atlantic miles, Avios, best time to fly to, when should I go to. Personal-use skill, not client-facing. For upgrading a ticket he ALREADY holds, use flight-upgrade instead."

---

# AWARD FLIGHT SEARCH

Graeham's award-booking desk. Takes his points balances and finds a **new** premium-cabin ticket worth booking.

Not the same skill as `flight-upgrade`. That one upgrades a ticket he already holds, which is a different inventory pool entirely. If he already has a booking, stop and use that skill instead.

---

## 0. HARD RULES

1. **Never transfer points.** Transfers are one-way and irreversible. Find and verify the award space first, present the exact numbers, then he transfers. A transfer made before space is confirmed can strand six figures of points in a program he will never use.
2. **Never enter payment details, never book.** Line it up, show the total, stop.
3. **Never ask for or accept a password.** He logs into point.me and airline sites himself.
4. **Never commit the wallet.** See section 1. This repo is public.
5. **Always quote the surcharge next to the miles.** A redemption is miles PLUS cash. Quoting miles alone is how people book an $800 "free" flight. See section 3, which is the most valuable part of this skill.
6. **Re-verify every chart figure at run time.** Award charts and surcharges change constantly. ANA's surcharge went up 19% between October and November 2026. Treat `references/` as a starting frame, not an authority.

---

## 1. THE WALLET

Balances, loyalty numbers and card details live in:

```
skills/award-flight-search/outputs/wallet.md
```

`outputs/` is gitignored repo-wide. This repo is public, so that placement is deliberate and must not be "tidied" into the skill folder. Copy `references/wallet-template.md` on first run.

**point.me's "My Points" dashboard tracks balances across every program.** If he is logged in, read it from there rather than asking. Faster and more accurate than memory.

---

## 2. HIS CURRENCIES

Two transferable currencies, and **which one he uses is often forced by the destination.**

| | Amex Membership Rewards | Bilt Rewards |
|---|---|---|
| Airline partners | 16 | 19, all 1:1, 2,000 min |
| **Only Amex reaches** | **ANA**, Delta, Singapore, Qantas, Aeromexico | — |
| **Only Bilt reaches** | — | **Atmos (Alaska/Hawaiian)**, **JAL**, United, Turkish, TAP, Etihad, Southwest |
| Both reach | Virgin Atlantic, Aeroplan, Flying Blue, LifeMiles, BA, Iberia, Qatar, Aer Lingus, Cathay, Emirates, JetBlue | same 11 |

### Routing rules that cost real money

- **Cathay, Emirates and JetBlue: send from Bilt, never Amex.** Amex transfers those at 5:4, losing 20%, and adds an excise fee on JetBlue.
- **Aeromexico is the only partner paying above 1:1** from Amex, at 5:8.
- **Hilton: Amex at 1:2 beats Bilt at 1:1** decisively.
- **ANA is Amex-only. Atmos and JAL are Bilt-only.** These two facts decide most Japan redemptions.
- Four of the overlap programs (BA, Iberia, Aer Lingus, Qatar) share one combinable **Avios** pool, so the effective pooled balance is larger than any single line shows.

Check live transfer bonuses every run. They are frequently account-targeted, so read his actual Amex offers page rather than a public tracker.

---

## 3. THE SURCHARGE TRAP — read this before quoting any redemption

**The single most valuable thing in this skill.** Two programs can book the identical seat on the identical aircraft for wildly different real cost, because some pass through carrier-imposed fuel surcharges and some do not.

Worked example, SFO to Tokyo, same ANA/JAL metal:

| Path | Miles | Cash | Real cost |
|---|---|---|---|
| ANA Mileage Club (Amex) | 85,000 one-way | **+ ~$419 surcharge per flight** | ~$800+ round trip in cash on top |
| Atmos Rewards (Bilt) | ~110,000 one-way | **+ $20 booking fee** | essentially nothing |

Atmos costs 25,000 more miles and saves roughly $400 each way. Whether that trade is good depends on his miles valuation, but **it must be shown as a trade.** Quoting ANA's 85,000 without the $419 is the error this section exists to prevent.

**No surcharge on partner awards:** Atmos Rewards (except BA, Hainan, Icelandair), Air Canada Aeroplan, Avianca LifeMiles, United.

**Heavy surcharges:** ANA, JAL, British Airways, Turkish (~$200-250 each way), Qantas (moved Business and First to Classic Plus-level carrier charges).

**Unconfirmed and worth a phone call before transferring:** whether Virgin Atlantic passes ANA's surcharge on an ANA First redemption. That one unknown decides whether Virgin's 72,500 is the best deal available or a trap.

---

## 4. SEASON CLIFFS

Award charts have hard date boundaries where the price jumps overnight. Finding one is often worth more than finding a better program.

**ANA, Japan to North America, as of November 2026:**

| Dates | Season | First one-way |
|---|---|---|
| Nov 2026 through **Dec 18** | Regular | **85,000** |
| **Dec 19 - Dec 31** | High | **150,000** |
| Jan 1 - 3 | High | 150,000 |
| Jan 4 - 5 | Regular | 85,000 |
| **Jan 6 onward** | Low | **75,000** |

Departing 18 December instead of 19 December saves **65,000 miles one-way**. Departing 6 January instead of 3 January saves 75,000.

**Always locate the cliff before proposing dates.** Shifting a trip by one day is the cheapest optimisation available, and it is invisible unless someone looks for it.

---

## 5. WHERE REAL FIRST CLASS ACTUALLY EXISTS

He often asks for "first class" meaning "the good cabin." Clarify early, because on two of his four usual regions real First does not exist at all and promising it wastes the search.

| Region | Real First? | Reality |
|---|---|---|
| **Japan** | **Yes** | ANA First "The Suite", JAL First. The only region where real First is both available and reachable from his points |
| **Australia** | Yes, **but not from SFO** | Qantas First is A380-only. SFO gets the 787-9, no First cabin. Requires positioning to LAX for SYD-LAX, or DFW |
| **Brazil / South America** | **No** | Business is the top cabin. AA's Flagship First on the 777-300ER ended 19 Nov 2026 and was never a West Coast product |
| **Eastern Europe** | **No** | No carrier flies a First cabin to Warsaw, Prague, Budapest or Bucharest |

**The Lufthansa workaround is dead.** Since 1 June 2026 Lufthansa keeps First Class award space for its own Miles & More members, and no credit card program transfers to Miles & More. Lufthansa First is unbookable from Amex or Bilt at any price. Partner business saver space on Lufthansa, Austrian and SWISS was also heavily restricted in July 2026, which damages the Star Alliance path to Eastern Europe generally.

---

## 6. AVAILABILITY REALITY

Award space is not seat availability. A cabin can be half empty with zero award space.

- **ANA releases roughly one First seat per flight** at the 355-day mark. Partner space appears in two windows: at the edge of the 355-day window, and again around 14 to 21 days out. **Inside a few months, everything available comes from cancellations.**
- **Qantas releases long-haul Business and First in batches close to departure**, to higher status tiers first, with no-status members last.
- Two premium seats together on one flight is rare at any time of year. For a solo traveller this constraint largely disappears, which is worth saying out loud when it applies.

Set expectations honestly. For a trip inside three weeks in a premium cabin, the correct framing is "we are hunting cancellation space," not "let me find you a seat."

---

## 7. TOOLS, AND WHAT EACH ACTUALLY DOES

| Tool | What it is | Verdict |
|---|---|---|
| **point.me** | Award search across 150+ programs, live availability, step-by-step transfer instructions, My Points balance dashboard | **The primary tool.** He subscribes. Drive it with the browser |
| **Thrifty Traveler Premium** | Human-curated deal-alert newsletter | **Not a search engine.** He cannot run his own searches. It will never answer "what can I book with my points." Do not plan around it |
| **seats.aero** | Award availability search, ~$99/yr, has a real API | Worth buying if point.me ever lapses. Not currently subscribed |
| **Bilt Points Path** | In-portal widget that replaced Bilt's point.me access on 20 Mar 2026 | One-ways only, airline's own metal only, subset of partners. A downgrade. Use point.me directly |

**Airline sites block automation.** Qantas, Alaska/Atmos and JAL all return bot checks to plain fetches. ANA's own site reads fine. When a site blocks, hand back with the exact next click rather than retrying harder.

---

## 8. METHOD

1. **Read the wallet.** Balances, status, cards. Ask only what is missing.
2. **Settle the cabin question.** "First class" or "the good cabin"? Section 5 decides whether the ask is even possible for that region.
3. **Season first, award second.** Cross-reference destination seasonality before searching. A cheap award into monsoon season is not a deal. His stated preference is the **edge of a season**, not peak and not the dead end of it.
4. **Find the season cliff** in the relevant award chart. Section 4.
5. **Search point.me** for live availability across programs.
6. **Price every candidate as miles PLUS cash.** Section 3. Rank by real cost, not headline miles.
7. **Check which currency can even reach the winning program.** Section 2. This frequently eliminates the best option.
8. **Present, then stop.** He transfers. He books.

---

## 9. OUTPUT

An interactive artifact ranking the realistic options. Per card: destination, dates, cabin, operating airline, booking program, miles, cash, **real total**, which currency feeds it, confirmed-or-hunting, and one line of why.

Pinned at the top: the single best move, and the deadline that kills it if one exists.

Include dead ends with the reason. Knowing Lufthansa First is unbookable stops the same question being asked next trip.

---

## 10. TONE

Lead with the number. Show miles and cash together, always. When an option is a lottery ticket rather than a plan, say so in those words.

He asked for the better deal, not the fancier label. Rank on value and let him choose.
