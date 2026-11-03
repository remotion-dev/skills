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

## 4A. A CHART PRICE IS NOT AN AVAILABLE SEAT

**Learned the hard way on 2026-11-03.** Four research passes produced a clean table of First class chart prices. A live point.me sweep found that **not one of them was bookable.**

| Route | Date searched | Chart price researched | What live search actually showed |
|---|---|---|---|
| SFO-Tokyo | 5 Dec 2026 | ANA First 85,000 / JAL First 110,000 | No ANA or JAL First at any price. Cheapest 150,000 + $11, Atmos, 28h35m, 1 stop |
| SFO-Tokyo | 10 Jan 2027 | ANA First Low 75,000 | Same 150,000 + $6, but 15h25m. January buys a shorter trip for the same points |
| SFO-Hong Kong | 5 Dec 2026 | Cathay First 70,000 Atmos | No Cathay at all. Cheapest 97,000, United+EVA, part economy, 2 stops, 22h |
| LAX-Sydney | 5 Dec 2026 | Qantas First 130,000 Atmos | No Qantas at all. Cheapest 330,000 Fiji business |
| SFO-Rio | 28 Dec 2026 | Aeroplan business 50-60,000 | Cheapest 207,000 AA, 2 stops, 25h44m |

**But the same sweep found the value had simply moved to business class**, where it was excellent:

| Route | Date | Live price | Note |
|---|---|---|---|
| **SFO-London** | 20 Jan 2027 | **58,000 + $734** | BA business, **nonstop, 10h25m**. Cash price $4,093 |
| **London-SFO** | 28 Jan 2027 | **58,000 + $428** | AA/Atmos 1-stop. BA nonstop same points but $901 |
| **SFO-Buenos Aires** | 28 Dec 2026 | **100,000 + $28** | Copa business, 1 stop via Panama. Flagged GREAT DEAL |
| EZE-SFO | 7 Jan 2027 | 97,000 + $50 | Copa/United, but part economy. Avianca all-business 220,000 |

So the full conclusion is not "nothing is available," it is **"First is gone, business is a bargain."** London round trip came to 116,000 points and about $1,162 against a $12,749 cash fare. Always price the business cabin before telling him a window is dead.

**The rule this produces: never quote a chart price without a live search behind it.** Four to eight weeks out, saver premium inventory is gone and what remains is dynamically priced at two to four times the chart. Research the chart to know what *good* looks like; search live to know what *exists*.

Corollary: when live prices are this far above chart, the honest advice is usually "not this trip, this window" rather than a worse redemption.

---

## 5. WHERE REAL FIRST CLASS ACTUALLY EXISTS

He often asks for "first class" meaning "the good cabin." Clarify early, because on two of his four usual regions real First does not exist at all and promising it wastes the search.

| Region | Real First? | Reality |
|---|---|---|
| **Japan** | **Yes** | ANA First "The Suite", JAL First. The only region where real First is both available and reachable from his points |
| **Australia** | Yes, **but not from SFO** | Qantas First is A380-only. SFO gets the 787-9, no First cabin. Requires positioning to LAX for SYD-LAX, or DFW |
| **Brazil / South America** | **No** | Business is the top cabin. AA's Flagship First on the 777-300ER ended 19 Nov 2026 and was never a West Coast product |
| **Eastern Europe** | **No** | No carrier flies a First cabin to Warsaw, Prague, Budapest or Bucharest |

### The one real First cabin to Europe

**British Airways First, SFO-LHR.** 93,500 Avios off-peak, 110,000 peak, plus roughly £574 in carrier charges. Avios transfers 1:1 from **both** Amex and Bilt, and four programs (BA, Iberia, Aer Lingus, Qatar) pool into one Avios balance, so this is the most *fundable* First cabin in the whole map. Off-peak runs roughly mid-January to mid-March, mid-April to mid-May, and September to mid-November. **December is peak**, so a January trip is both cheaper in Avios and far likelier to have space.

It is not the world's best First product, and the cash component is real. It is, however, the only genuine First cabin to Europe that these two currencies can actually buy.

**Caveat from the 3 Nov 2026 live sweep: no BA First space surfaced on any date checked.** What did surface was BA *business* nonstop at 58,000 Avios, which is the better buy anyway. Treat the 93,500 First figure as the alert target, and quote the 58,000 business as the actual plan.

### European First dead ends, all confirmed closed

- **Lufthansa.** Since 1 June 2026, First award space is kept for Miles & More members only, and no credit card program transfers to Miles & More. Unbookable at any price.
- **SWISS.** Same policy, and explicitly so: partner miles do not get around the elite-Miles & More restriction. The Aeroplan and United booking windows people still cite were brief openings in 2016-2018, and SWISS cancelled some of those bookings afterward. Treat any "book SWISS First with Aeroplan" post as historical.
- **Emirates.** First awards have been restricted to Silver, Gold and Platinum Skywards members since May 2025. SFO-DXB prices around 186,000-188,000 miles plus roughly $850-880 anyway. Status gate first, price second. The workaround people use is booking business and upgrading with miles.
- **Etihad First Apartment.** The A380 appears to be off the New York route for the 2026 network, and Etihad ended SFO service on 29 October. Verify the schedule before building any plan on it.

Partner business saver space on Lufthansa, Austrian and SWISS was also heavily restricted in July 2026, which damages the Star Alliance path to Eastern Europe generally.

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

### Driving point.me — skip the form

He is signed in on **Chrome**, not the Ultrafast Browser. Chrome shares its profile, so a tab opened with `mcp__claude-in-chrome__*` inherits the login even though this session cannot see his own tabs.

**Do not fight the search form.** The airport fields are multi-chip comboboxes that keep their previous value, and the date picker ignores typed dates. Build the URL instead:

```
https://www.point.me/flight/search?departureIata=SFO&arrivalIata=HND&departureDate=2026-12-05&classOfService=first&legType=oneWay&passengers=1
```

`classOfService` takes `business` or `first` (the UI labels both "Business / First"). `legType=oneWay`. Results take 15-20 seconds, so navigate, wait, then `get_page_text` — and chain two full searches in one `browser_batch`, since batched actions run in order.

Useful on the results page: the **My Programs** toggle filters to currencies he actually holds, and an **IN YOUR WALLET / You have enough points!** badge marks redemptions his current balance covers. A result that survives the filter but shows no badge is one he can reach but cannot yet afford.

His **My Points** dashboard gives balances per program, with a sync age. Check that age. A manually-entered balance months old is a guess, not a number.

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
