# Data Verification & Nuanced Language

**Read this every time a script contains a mortgage rate, a price, a median, a percentage change, days-on-market, or any other number that can change week to week.** This is the source of truth for how Graeham talks about data. The goal: stay specific enough to be credible, hedged enough to stay true next week, and sourced enough to defend.

This file exists because perishable numbers go stale fast. A rate that's "6.4%" on a Tuesday can be 6.5% by Friday. A median printed as a hard figure looks wrong the moment a new month closes. The fix isn't to drop the numbers. It's to frame them as a current reading from a named source on a named date, and to use range language so the script stays accurate as the number drifts.

---

## Rule 1: Verify before you write (MANDATORY)

Before writing any script that cites market data, verify each perishable figure against a live primary source. Do not write the number from memory or from a prior script.

**Verification sources, in order of preference:**

| Figure | Primary source | How to pull |
|---|---|---|
| 30-yr / 15-yr fixed mortgage rate | Freddie Mac PMMS (weekly) | `WebSearch` "Freddie Mac PMMS this week" then `web_fetch` the freddiemac.com PMMS page. Mortgage News Daily for the daily read. |
| Median sale price, $/sqft, days-on-market | Redfin Data Center for the specific city; MLS if available | `web_fetch` the Redfin city market page. Cross-check a second source (Movoto, Zillow) and note if they disagree. |
| Active listing count / inventory | FRED (county-level) or MLS | `web_fetch` FRED series for San Mateo County. Do not claim an inventory trend the data doesn't show. |
| Layoff counts | Layoffs.fyi or the company's own filing | `WebSearch`, then cite the source by name. |
| Search demand / keyword interest | Google Search Console connector (`gsc_*` tools) | Pull the actual query data; don't guess what people search. |

Record every figure you use with its source and date. Those go in the script's "Verify before recording" block (see Rule 4) and the description's source list.

If you cannot verify a figure from a live source, do one of two things: leave it as a clearly marked `[VERIFY: figure]` placeholder for Graeham to fill from his MLS, or cut it. Never publish an unverified number as if it were confirmed. This matches Graeham's standing rule: don't invent numbers.

---

## Rule 2: Use range language for anything that moves

A single hard number reads as a claim. A range reads as a current reading. For perishable figures, prefer the range.

**Mortgage rates:**

- YES: "Rates are in the mid-6s right now, hovering around 6.3 to 6.4 percent as of the week of May 14."
- YES: "Call it the mid-six range. It moves week to week, so confirm the live number with your lender before you decide anything."
- NO: "The rate is 6.4 percent." (stale by Friday, and reads as a promise)
- NO: "Rates hit mid-6%." as a past-tense headline event. Say "rates are in the mid-six range right now" instead.

**Prices and medians:**

- YES: "The East Palo Alto median is around 1.1 million as of this spring, per Redfin."
- YES: "Roughly 2.8 to 3 million in Menlo Park, depending on the source and the month."
- NO: "The median is $1,130,000." (false precision on a number that updates monthly)

**Percentage changes and speed:**

- YES: "Up roughly four percent year over year."
- YES: "Selling in about a month, give or take, versus closer to two months a year ago."
- NO: "Up exactly 4.1%, 32 days versus 66." (read it aloud; the false precision sounds like a spreadsheet, not Graeham)

The pattern: lead with the range or the "around" figure for the spoken line, and keep the exact sourced number in the "Verify before recording" block and the description for anyone who wants to check it.

---

## Rule 3: Always date-stamp and source on camera at least once

Every script that leans on data needs at least one spoken line that tells the viewer when the number is from and where it came from. This is the E-E-A-T / trust move and it protects Graeham when the number drifts.

Templates:

- "As of mid-May 2026, per Freddie Mac, the 30-year fixed is averaging in the mid-6s."
- "I check these before every video. This is the Redfin read for East Palo Alto as of this spring."
- "Rates move week to week, so confirm the current number with your lender before you decide anything."

---

## Rule 4: Every data script ships with a "Verify before recording" block

At the top of every script that contains perishable data, include a short block Graeham re-checks the week he shoots. The Spring 2026 Market Update script is the model. Include:

- Each figure used, with its exact sourced value, source name, and date.
- The worked math behind any "buying power" or "savings" claim, so it can be re-run.
- An honest caution on anything you could not fully confirm. (Example from the market-update script: "I could not confirm 'fewer homes than 2024.' Don't say it on camera unless your MLS proves it for EPA specifically.") Keep doing exactly this.

---

## Rule 5: Avoid false-peak and false-event framing

Don't label a date a "peak" or "high" unless the data shows it was one. Late October 2024 was not a 30-year-fixed peak; rates were around 6.7% then, while spring 2024 ran above 7%. Calling October 2024 "the peak" is checkable and wrong, and a sharp viewer will catch it.

- YES: "Compared to where rates sat last fall, around six and three-quarters..."
- NO: "Compared to the October 2024 peak..."

When comparing to a prior point, name the actual point and its actual value, and make sure the direction and size of the change hold up.

---

## Rule 6: Cut the fluff (anti-filler self-edit)

After drafting, do one editing pass that removes filler that adds words but no information. Read every line aloud. If a sentence sounds like a blog intro or a press release, cut or rewrite it.

Common filler to cut:
- Throat-clearing transitions: "Let's dive in," "Quick context, because the why matters," "Here's the thing," "Hear me out," "And that's where it gets interesting."
- Empty hype: "game-changer," "huge," "crazy," "the one thing you need to know" when it's actually five things.
- Restating the obvious: "As I mentioned," "Like I said."
- Rule-of-three padding: three adjectives where one does the job.

Keep: specific numbers, concrete local detail (street names, developments, named sources), and the one-sentence "why it matters to you" after each data point. Tighten everything else. A 950-word market update should be 950 words of signal, not 700 of signal and 250 of warm-up.

---

## Rule 7: Market-update structure (when the topic is a market update)

Market updates compare. Build them on this spine:

1. **Hook** built on a tension or contradiction in the data ("Rates dropped, so why is it harder to buy?").
2. **The rate read** with range language, date, and source, plus the one-line "what it does to your wallet."
3. **The comparison** across two or three specific areas, with sourced, hedged figures (median, $/sqft, days-on-market). Name the source when the numbers come from different places, and flag when sources disagree.
4. **The honest counter-read** ("if you're waiting for a crash, the data isn't pointing that way" / the inventory caution). This is what makes it trustworthy instead of cheerleading.
5. **One clear recommendation** framed around value and data, never around who lives somewhere (see Fair Housing note below).
6. **CTA** with the lead-capture keyword.

---

## Fair Housing guardrail on area comparisons

When recommending or comparing neighborhoods, keep it strictly about price, data, commute, and amenities. Never about who lives there or the "character" of a community. Avoid coded steering language entirely: no "up-and-coming," "changing neighborhood," "pioneering," "transitional," "good schools," "safe," "family-friendly," or "desirable." Comparing East Palo Alto's median to Palo Alto's on price and commute is fine. Implying anything about the people, safety, or trajectory of a community in demographic terms is not. When in doubt, anchor every claim to a number and a source.
