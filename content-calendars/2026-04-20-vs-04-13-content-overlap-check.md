# Content Overlap Check — Week of April 20-26 vs Week of April 13-19

**Purpose**: Prevent content duplication between consecutive weekly calendars so subscribers, YouTube audience, and IG followers don't see the same topic twice in a row.

**Compared**:
- `2026-04-13-production-calendar-v6.html` (last week, shipped)
- `2026-04-20-production-calendar-v6.html` / v7.3 (this week, about to ship)

---

## Side-by-side topic list

| Day | Week of April 13-19 (LAST WEEK) | Week of April 20-26 (THIS WEEK) |
|---|---|---|
| MON | EPA Homes Under **$700K**: Your Entry to Silicon Valley | EPA Homes Under **$1M**: Your Entry to Silicon Valley |
| TUE | Meta Just Laid Off 200+ in the Bay Area. What It Means for Housing. | Bay Area Mortgage Rate Update: **6.37%** and What It Means |
| WED | AB 1482 Explained: California Rent Control That Every Landlord Must Know | East Palo Alto **Q2 2026** Price Breakdown by Neighborhood |
| THU | The Richest City in America That Nobody Talks About (Atherton) | What **$5M Buys**: Atherton vs Palo Alto vs Menlo Park |
| FRI/SAT | SAT — Mortgage Rates at **6.46%**: Should Bay Area Buyers Wait or Act? | FRI — California Smoke & CO Detector Law: Seller Compliance Guide |

---

## Overlap risk assessment

### HIGH RISK — Day 1 (Monday)

**Last week**: "EPA Homes Under **$700K**: Your Entry to Silicon Valley"
**This week**: "EPA Homes Under **$1M**: Your Entry to Silicon Valley"

The title framing is nearly identical. Same neighborhood (East Palo Alto), same buyer archetype (entry-level Silicon Valley), same angle (affordability → geographic access), same BOFU intent. Only difference is the price ceiling expanded from $700K to $1M — which mathematically *includes* every property covered in last week's video.

**Why this is a problem**: Subscribers who watched last week's $700K video will pattern-match this as "same video, wider price filter." YouTube algorithm may also see topical overlap and suppress distribution if last week's video is still being served.

**Recommended fix (pick one)**:
1. **Reframe the angle** — not "homes under $1M" as the hook, but something narrower: "The 3 EPA Neighborhoods Between $750K-$1M Most Buyers Miss" (differentiates from last week's under-$700K framing by targeting the $750K-$1M gap specifically).
2. **Replace the topic entirely** — use a different BOFU/MOFU topic that didn't appear last week. Options from the backlog: "5 Questions to Ask Before Buying in East Palo Alto" (BOFU buyer checklist), "How EPA's Rent Control Ordinance Affects New Buyers" (local policy + BOFU), or "EPA vs Redwood City: Which Sub-$1M Market Wins in 2026" (comparison angle).
3. **Defer to next week** — push this topic to Apr 27 and swap in a fresher Monday topic this week.

My recommendation: **Option 1** — reframe to "$750K-$1M gap in EPA." Minimal production disruption, clear differentiation.

### MODERATE RISK — Day 2 (Tuesday)

**Last week (Saturday)**: "Mortgage Rates at **6.46%**: Should Bay Area Buyers Wait or Act?"
**This week (Tuesday)**: "Bay Area Mortgage Rate Update: **6.37%** and What It Means"

Same core subject: Bay Area mortgage rates. The rate dropped 9 basis points (6.46% → 6.37%). Last week's angle was buyer-decision-framing. This week's angle is currently generic ("what it means").

**Why this is a problem**: Without clear differentiation, this reads as "same mortgage rate video, updated number."

**Recommended fix**:
Re-angle the prompt to lead with the **rate DROP as news hook** and shift focus to **refinance math** (existing homeowners) rather than buy-or-wait (covered last week). That separates the audiences cleanly: last week served buyers deciding whether to enter; this week serves homeowners evaluating refi. Also reinforces the MOFU tier tag already in the library.

Proposed revised title: "Bay Area Mortgage Rates Just Dropped to 6.37% — What This Means for Refinancing in 2026."

### LOW-MODERATE RISK — Day 4 (Thursday)

**Last week**: "The Richest City in America That Nobody Talks About" (Atherton solo profile, likely TOFU lifestyle)
**This week**: "What $5M Buys: Atherton vs Palo Alto vs Menlo Park" (TOFU three-city comparison)

Both feature Atherton. Comparison angle is fresh but AI video generation may pull the same Atherton stats/B-roll as last week.

**Recommended fix**:
When generating Day 4 Part 2 (production package), explicitly brief the prompt: "This video is a comparison across 3 cities — DO NOT repeat Atherton stats or framing from April 16 video. Focus on price-per-sq-ft and lot-size differentials, not Atherton lifestyle profile."

### NO OVERLAP ✓

- **Day 3 Wed** (EPA Q2 Price Breakdown) — brand new quarterly data report, no prior version
- **Day 5 Fri** (CA Smoke/CO Compliance) — brand new evergreen seller-education topic
- **Last Tuesday's Meta Layoffs** — no equivalent this week (good)
- **Last Wednesday's AB 1482** — no equivalent this week (good)

---

## Audience-fatigue cross-check

Looking at the IG engagement data for the week of Apr 6-12 (from this week's Performance Analysis tab):
- IG Reach: 2,290 (up 188% WoW)
- Apr 10 single-day reach: 1,301 (6× baseline)

That spike happened on a specific post. Before scheduling Day 1 and Day 2 of this new week, **check which April 10 post caught fire** — if it was the EPA-entry-level or mortgage-rate content, that's further evidence that repeating those topics this week is dangerous (algorithm has just served that audience the same message).

---

## Action items before shipping this week's calendar

1. **Reframe Day 1 (Mon Apr 20)** from "EPA Homes Under $1M" to "The $750K-$1M EPA Gap: Neighborhoods Most Buyers Skip" (or a replacement topic). Update the calendar HTML + PROMPT_LIBRARY `day1` TOPIC field + key_facts.
2. **Re-angle Day 2 (Tue Apr 21)** prompt to lead with the rate-drop news and pivot to refi math. Update TOPIC field + lead_magnet.
3. **Add brief to Day 4 (Thu Apr 23) Part 2** production package prompt to explicitly avoid repeating Atherton framing from April 16.
4. No changes needed for Day 3, Day 5, or the email newsletter.

---

## Systematization

Going forward, this comparison should run **before every new week's calendar ships**. Two ways to bake it in:

- **Option A (manual)**: Run this comparison as a 5-minute check at the end of each Sunday's calendar build.
- **Option B (automated)**: Add a `TOPIC_HISTORY` object to the calendar HTML that tracks the last 4 weeks of topics. Future calendar generation runs a pre-publish check that flags any new topic whose slug, keyword, or title substring overlaps with history and requires explicit override.

Recommend **Option B** for next iteration (v7.4 or v8). Would take ~30 min to implement.

---

*Generated April 13, 2026 — reviewed against calendar commits d190129 (v7.1), 49a8acb (v7.2), e764efd (v7.3).*
