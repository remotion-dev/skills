# Phase 4 — Research & Data Injection

This is the phase that fixes the actual problem the user flagged. SurfFast gives us the words. SurfFast does NOT give us the data layer that makes Graeham's Content Engine scripts feel authoritative instead of like a karaoke version of someone else's video.

The output of this phase is a `research_pack` — a small set of cite-ready, date-stamped facts that Phase 6 will weave into the script.

## Branching Logic — Where to Look Based on Localization Need

From Phase 2's source brief, you tagged the topic as one of: strongly local, real estate universal, or universal non-real-estate. Each branch uses a different research playbook.

## Branch A — Strongly Local (Bay Area / Peninsula / California)

The Content Engine already has a rich set of references for Graeham's markets. Reuse them — don't reinvent.

**Step 1:** Read `video-script-creation-engine/references/market-config.md` for:
- Primary market: East Palo Alto
- Secondary markets: Redwood City, Palo Alto, Menlo Park, San Mateo County, Peninsula
- Lead magnets and CTA matrix
- Current jurisdiction-specific process terms

**Step 2:** If the topic involves a specific legal/regulatory item, reach for:
- AB 1482 — California Tenant Protection Act (5% + CPI or 10% cap)
- Prop 19 — Property tax base transfer rules
- TDS / SPQ / AVID disclosure obligations
- East Palo Alto Rent Stabilization Ordinance (more restrictive than AB 1482 for covered units)
- San Mateo County transfer tax structure

**Step 3:** Pull market data with explicit date anchors. NEVER quote a bare statistic. Always frame as "As of <Month Year>, <stat>." If we don't have a fresh stat for the month, web-search for the most recent and date-stamp accurately.

**Step 4:** Check `video-script-creation-engine/references/topic-history.json` — if Graeham has covered this topic before, reference his prior coverage in a "see also" line so the content cross-links. Don't repeat exactly what he said last time.

## Branch B — Real Estate Universal

Topic applies broadly (mortgage rates, closing costs, buyer psychology, market cycles) but Graeham CAN deepen authority by adding the Bay Area lens where it lands naturally.

**Step 1:** Web search for the most current national/state-level data on the topic. Verify any numerical claims from the source transcript — flag if the source was using a stale 2024 or 2025 number.

**Step 2:** Identify ONE specific Bay Area localization that strengthens the point. For example, if the topic is "buying in a high-rate environment," the local angle could be Peninsula-specific monthly payment math at the current rate vs. 18 months ago. One strong local data point beats five generic mentions.

**Step 3:** Pull current source citations — Fed funds rate, CPI print, NAR median sale price, Case-Shiller, whatever is relevant. Date-stamp each.

**Step 4:** Don't force local references where they don't naturally fit. If the topic is genuinely universal, a forced "in the Bay Area..." line will sound tacked-on.

## Branch C — Universal Non-Real-Estate

Topic is general life / business / lifestyle / finance basics. Real estate connection is optional.

**Step 1:** Web search for current data, statistics, expert sources relevant to the topic.

**Step 2:** Verify any numerical claims from the source transcript. Don't carry stale data forward.

**Step 3:** If the topic CAN bridge to real estate naturally (e.g., personal finance topic → connection to homebuying), build one bridge line for the CTA. If not, leave the CTA generic ("DM me if you want to talk Bay Area real estate").

**Step 4:** Don't over-localize. Forced real estate connections from unrelated topics will feel salesy and tank engagement.

## Fact-Verification Rules

For every numeric or factual claim that's going into Graeham's script:

1. **Has a source.** Web URL, document name, or "Graeham's direct experience" (for personal stories).
2. **Has a date.** Either the publication date of the source, or the as-of date for the data point.
3. **Is current to within 6 months** for market data, 12 months for legal/regulatory data, indefinite for historical facts.
4. **Is defensible if challenged in a comment.** If a viewer pushes back on the claim, Graeham should be able to point to where it came from.

If a claim from the source transcript fails any of these tests, replace it or remove it. Don't repeat it just because the source did.

## Output Format

```
## Research Pack — As of <Month Year>

Verified Facts (cite-ready):
1. <Fact 1>. Source: <source>. Date: <date>.
2. <Fact 2>. Source: <source>. Date: <date>.
3. <Fact 3>. Source: <source>. Date: <date>.
...

Source-Transcript Claims Filtered Out:
- "<claim from source>" — Reason: <stale / unverified / wrong / Fair Housing>
- ...

Bay Area Lens Insertion Points (if applicable):
- Phase 6 should land this stat: "<Bay Area data point>" at <position in script>
- ...

Lead Magnet / CTA Recommendation:
- GHL Keyword: <KEYWORD>
- Lead Magnet: <name>
- Rationale: <one line>
```

Hand this directly to Phase 5 (hook generation — strong hooks pull from research data) and Phase 6 (script writing).

## Time Budget

Phase 4 should take real effort but not blow the context. For a typical 30-90 second source transcript, target:

- 3-7 verified facts in the research pack
- 1-2 web searches if needed
- 5 minutes of attention

If you find yourself going down a 30-min research rabbit hole, you're over-budget for a social repurpose. Compress and move on.
