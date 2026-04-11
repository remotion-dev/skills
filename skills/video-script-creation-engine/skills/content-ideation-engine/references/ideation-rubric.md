# Ideation Scoring Rubric

How to turn a raw Reddit dataset into a ranked list of content opportunities.

---

## The core question

For each post (and optionally its top comments), ask: **"Would this make a good piece of content for Graeham's real estate brand?"**

A "good piece of content" meets at least three of these criteria:
- It's about a topic his audience (Bay Area buyers, sellers, or investors) cares about
- It's specific to a local market Graeham works (EPA, Peninsula, or Bay Area broadly)
- It represents a moment where someone is making or considering a real estate decision
- It has an angle Graeham can uniquely answer with his expertise or data
- It fits one of the 9 content pillars from the main orchestrator

---

## The 4-axis scoring system

Score each post on these 4 axes. Each axis is 0-3. Total possible score: 12.

### Axis 1: Funnel relevance (0-3)

| Score | Meaning | Examples |
|---|---|---|
| 0 | Pure noise, not real estate related | "Best burrito in Redwood City?" |
| 1 | TOFU — lifestyle/awareness, no transaction intent | "Moving to Bay Area next year, any tips?" |
| 2 | MOFU — research mode, actively gathering info | "AB 1482 — does it apply to owner-occupied duplexes?" |
| 3 | BOFU — near-decision moment, ready to transact | "Meta laid me off, need to sell my Menlo Park house fast" |

**Bias toward BOFU posts.** They convert 10x better than TOFU. One score-3 post beats five score-1 posts.

### Axis 2: Local specificity (0-3)

| Score | Meaning |
|---|---|
| 0 | Not geographic |
| 1 | National or generic (e.g., "First-time buyer tips") |
| 2 | Bay Area mentioned but not a specific city |
| 3 | Specific Peninsula city named (EPA, RWC, PA, MP, SMC, etc.) |

**Peninsula cities score 3. EPA posts get a special boost (+1 bonus if applicable) because that's Graeham's primary market and content there has less competition.**

### Axis 3: Engagement velocity (0-3)

Engagement alone doesn't matter — velocity does. A 500-upvote post from 6 days ago is dead. A 50-upvote post from 6 hours ago is climbing.

| Score | Criteria |
|---|---|
| 0 | Dead thread — last comment >3 days ago, <10 upvotes |
| 1 | Low activity — posted in last week, <30 upvotes, few comments |
| 2 | Moderate — posted in last 72 hours, 30-100 upvotes, 10+ comments |
| 3 | Hot — posted in last 48 hours, >100 upvotes OR >50 comments, still getting replies |

**Calculation shortcut:** `velocity = (upvotes + comments * 2) / hours_since_posted`. Normalize across the dataset and assign 0-3 based on percentile (bottom 25% = 0, top 10% = 3).

### Axis 4: Content gap fit (0-3)

Does this post match a pillar Graeham hasn't recently covered?

| Score | Criteria |
|---|---|
| 0 | Topic Graeham covered in the last 2 weeks — saturated |
| 1 | Related to recent content but with a new angle |
| 2 | Matches a pillar Graeham hasn't touched in 4+ weeks |
| 3 | Matches a pillar Graeham has never covered OR addresses a brand-new trigger event (e.g., fresh layoff wave, new legislation, major comp closing nearby) |

**If you can't check recent content history, default to score 2 for any pillar match.**

---

## Final ranking

Total score = Axis1 + Axis2 + Axis3 + Axis4 (plus EPA bonus if applicable, max 13).

- **Score 10-13:** TOP OPPORTUNITY — surface immediately, recommend packaging
- **Score 7-9:** GOOD OPPORTUNITY — surface if top 5 not full yet
- **Score 4-6:** WORTH NOTING — mention in passing, don't lead with
- **Score 0-3:** FILTER OUT — don't surface

---

## Noise filters (apply BEFORE scoring)

Auto-filter out posts that match any of these:

- **Pure memes:** post has `[meme]` tag, or body is only an image link with no context
- **Self-promotion spam:** post is from a real estate agent self-promoting a listing
- **Off-topic:** post has no real estate keywords (buy, sell, rent, lease, house, home, condo, landlord, tenant, mortgage, price, sale, market, comp, listing, property, 1482, etc.)
- **Foreign languages:** post is not in English (check first 50 chars)
- **Deleted/removed:** body is "[removed]" or "[deleted]"
- **Too old:** posted more than 10 days ago (we said time=week but safety net)
- **Off-geography:** mentions a city that isn't Bay Area, Peninsula, or a market Graeham works (e.g., Sacramento, Los Angeles, Texas)

---

## Special signal boosters

Give +2 to the final score (capped at 13) if a post matches any of these HIGH-VALUE triggers:

1. **Layoff trigger:** mentions Meta, Google, Apple, Tesla, Nvidia, Stripe, etc. + "laid off" / "layoff" / "severance" / "exit package"
2. **Life event trigger:** "divorce", "inherited", "downsizing", "empty nest", "baby on the way", "job transfer"
3. **Legislation trigger:** AB 1482, Prop 13, rent control, ADU law, SB 9, recent ballot measure
4. **Market timing trigger:** "should I buy now", "is it a good time to sell", "prices going down", "interest rates"
5. **Competitive intelligence trigger:** mentions a specific listing, agent, or transaction nearby

These triggers map directly to Pillar 8 (Trigger Event Content), Graeham's HIGHEST-CONVERTING pillar from the main content-pillars reference.

---

## Output format for each ranked opportunity

```markdown
### Opportunity #N — [Short descriptive title]

**Source:** r/[subreddit] → "[post title]" ([URL])
**Posted:** [date/time] by [username]
**Engagement:** [X upvotes, Y comments]
**Score:** [total]/13 (F:[n] L:[n] V:[n] G:[n]) [+bonus if applicable]
**Funnel stage:** BOFU / MOFU / TOFU
**Pillar:** #[N] — [Pillar name]
**Signal summary:** [1-2 sentences describing what's happening and why it matters]
**Recommended format:** [YouTube Long-Form / Reel / Carousel / GBP / Blog / Email]
**Suggested hook:** "[One-line hook]"
**Lead capture keyword:** [SELL / OPTIONS / 1482 / etc.]
**Raw quote (if useful):** "[1-2 quoted sentences from the original post — for authenticity in the final content]"
```

---

## Honesty check

Before surfacing any opportunity, ask yourself:
- **Is this real signal or am I pattern-matching on noise?**
- **Would Graeham actually want to make this content, or is it generic filler?**
- **Does the recommended angle have a unique take only Graeham (with his EPA expertise) can provide?**

If the answer to any of those is "I'm not sure," either downgrade the score or drop the opportunity. **Better to surface 3 great ideas than 10 mediocre ones.** The goal is Graeham's time, not our dataset volume.
