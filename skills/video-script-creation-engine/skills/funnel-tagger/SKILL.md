---
name: funnel-tagger
description: Lightweight funnel-stage tagger for real estate content. Use this skill when you need to quickly classify a video topic, script idea, or content piece as TOFU (Top of Funnel — awareness), MOFU (Middle of Funnel — consideration), or BOFU (Bottom of Funnel — conversion). Trigger when the video-script-generator orchestrator is uncertain about a topic's funnel stage, when the user asks "is this TOFU, MOFU, or BOFU?" or "what funnel stage is this," or when tagging a batch of content ideas for a weekly content calendar. Also trigger when reviewing inherited content to assign funnel tags retroactively.
---

# Funnel Tagger

This is a lightweight sub-skill of the `video-script-generator` orchestrator. Its only job is to classify a content topic or idea into TOFU, MOFU, or BOFU and explain why. Use it when you're uncertain about a topic's funnel stage, or when bulk-tagging content for a weekly calendar.

## The Decision Tree

When tagging any topic, walk through this decision tree in order:

### Step 1: Who is the audience?

Ask: *"Who would watch this content?"*

- **People scrolling, not actively looking for real estate** → lean TOFU
- **People aware of the market and thinking about it, but not ready to transact in the next 6 months** → lean MOFU
- **People who are 0–6 months from a transaction** → lean BOFU

### Step 2: What's the intent?

Ask: *"Why would they watch this?"*

- **Entertainment, culture, lifestyle curiosity** → TOFU
- **Education, research, understanding the market** → MOFU
- **Solving a specific problem tied to their transaction** → BOFU

### Step 3: What's the CTA ceiling?

Ask: *"What's the highest-commitment action this content could plausibly drive?"*

- **Follow / like / share** → TOFU
- **Subscribe / save / comment for more info** → MOFU
- **Comment a specific keyword to trigger a lead capture workflow** → BOFU

### Step 4: Where does this content fit on the search intent spectrum?

Ask: *"Would someone search for this when they're actively trying to transact?"*

- **No, they'd only stumble on it while scrolling** → TOFU
- **Maybe — they might search for it while researching but not immediately before buying/selling** → MOFU
- **Yes, this is exactly the kind of thing someone searches when they're about to transact** → BOFU

## Quick Reference — Topic → Funnel Stage

| Topic | Funnel Stage | Why |
|---|---|---|
| "5 best tacos in East Palo Alto" | 🔵 TOFU | Lifestyle, no transaction intent |
| "Twin Peaks restaurant tour" | 🔵 TOFU | Lifestyle, city vibes |
| "Market update for Palo Alto — November" | 🟡 MOFU | Research-oriented, building awareness |
| "What $2M buys in Redwood City vs. Menlo Park" | 🟡 MOFU | Comparison / awareness building |
| "New Menlo Park development plans" | 🟡 MOFU | Local news, awareness building |
| "A day in the life of a Bay Area Realtor" | 🟡 MOFU | Brand building |
| "Is AB 1482 still in effect in 2026?" | 🔴 BOFU | Legal question, landlord is researching a decision |
| "How to sell a house in EPA as a first-time seller" | 🔴 BOFU | Process question, seller is actively considering listing |
| "Just got laid off from Meta — what are my options as a homeowner?" | 🔴 BOFU | Trigger event, urgent decision window |
| "EPA duplex investment analysis" | 🔴 BOFU | Specific investor intent |
| "Should I sell my house now or wait?" | 🔴 BOFU | Decision-stage question |
| "How to prep your Bay Area home for sale" | 🔴 BOFU | Actionable, pre-listing stage |
| "Rent vs. buy in Palo Alto — the real numbers" | 🔴 BOFU | Decision-stage, specific |
| "Behind the scenes of closing a $2.1M Palo Alto deal" | 🟡 MOFU | Brand/trust building, not specific conversion ask |
| "Client testimonial: Kevin & Rebecca bought their EPA home" | 🟡 MOFU (leaning BOFU) | Social proof, could flip to BOFU with strong CTA |

## Edge Cases and Tiebreakers

**"It feels like both TOFU and MOFU..."**
→ Default to TOFU if the content is entertainment-first and the CTA is lightweight. Default to MOFU if there's any educational content or saveable value.

**"It feels like both MOFU and BOFU..."**
→ The CTA decides it. If the CTA is "subscribe" or "comment for more info," it's MOFU. If the CTA is "comment [KEYWORD] to get [SPECIFIC DELIVERABLE]," it's BOFU.

**"It's a lifestyle hook but the content is really a seller pitch..."**
→ That's still BOFU. The funnel stage is determined by the payoff and the CTA, not the hook. Lifestyle hooks are often used as Trojan horses for BOFU content — that's fine, just tag it correctly.

**"It's educational but also has a lead capture CTA..."**
→ If it has a lead capture keyword CTA, it's BOFU. The CTA is the ultimate arbiter.

## Output Format

When you tag a topic, output:

```
Topic: [The topic being tagged]
Funnel stage: 🔵 TOFU | 🟡 MOFU | 🔴 BOFU
Reasoning: [1-2 sentences explaining why, referencing the decision tree]
Suggested CTA type: [follow/save/subscribe OR lead capture keyword]
Suggested lead capture keyword (if BOFU): [KEYWORD from lead-capture-keywords.md]
Suggested content pillar: [1-9 from content-pillars.md]
```

When tagging a batch, output as a clean table.
