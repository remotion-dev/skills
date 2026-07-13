REPLY IN THREAD: "combining everything: token optimizations + full restructure onto Claude Team plan"
To: sami@lfglabs.ai

Hi Samii,

Updating yesterday's email — since I sent it I pulled the real numbers from my Anthropic Console and ran an independent audit of all the repos, so now we're working with facts instead of feelings. Some of it is worse than I thought, some of it is genuinely better. Read this before our call.

**1. The real burn numbers.**

- July 1-13: $7,300 spent. That's about $600/day, pace of ~$18K/month.
- June was $4,150 for the ENTIRE month. So the daily rate quadrupled starting July 1-2 — which is exactly when we cancelled Fugu and that verification workload moved onto Fable 5 via the API. Nobody re-costed that migration, including me. So this isn't me saying you dropped the ball across the board — the explosion has a specific cause and a specific date.
- 91% of all token volume is running on Fable 5, the most expensive model that exists. Haiku is at 0.06%. That's the fixable part.
- Credit where due: your caching is working great — 97.8% cache hit ratio. Without it this would be 10x worse.

I have to be straight with you: I can't sustain $18K/month, period. If we can't get this fixed the project as currently structured has to stop. But the fix looks very doable, which brings me to:

**2. The gears.** Fable 5 needs to become the TOP gear, not the only gear:

- Gear 1 (routine/mechanical — file ops, extraction, formatting, status checks): Haiku, or DeepSeek for the absolute cheapest tier (caveat: DeepSeek's hosted API is China-based servers, so nothing client or proprietary goes there unless self-hosted).
- Gear 2 (standard well-specified coding, tests, routine refactors): Sonnet, and add ChatGPT/OpenAI models here too — I want us multi-model so we're not single-vendor priced.
- Gear 3 (architecture, hard debugging, verification, anything a lower gear failed at): Fable 5 only. Escalate up, never default up.

Benchmark to design against: Viktor (viktor.com) sells a full AI employee at $50/month. That's the cost class the Wattson assistants have to hit — not because I'm cheap, but because if we ever sell Wattson assistants to other agents at the $349-399/month price point, the AI cost per assistant has to sit way under that or there's no margin. This cost discipline IS our unit economics, not just my savings.

**3. The audit — good news and a real problem you both need to fix this week.**

I had an independent audit run across all five repos today. The good news, and I mean this: the July spend bought real work. 162 commits, ~37,000 lines on the Watson PropCast fork in nine days — lead intake, attribution pipeline, publishing center, engagement queue — with 50 test files, CI, and proper PR gates. Quality was rated above average, not agent thrash. That would have cost more from human devs. The fleet works.

The problem: **Watson's fork and QuestLab's main PropCast repo are building overlapping features separately and diverging.** The fork itself is by design — I want human review before anything hits main, that stays. But the review/merge pipeline has stalled, so ~37K lines of good work is sitting unmerged while QuestLab independently builds overlapping approval/publishing features upstream. I'm paying twice for some of the same functionality.

Two things I need done on this, starting today:

1. **QuestLab needs a detailed writeup — today if we can** — of exactly what the Watson system has built and where it overlaps with what they're building, so they stop duplicating and correct the overlap ASAP. I want this on our call.
2. **The Watson agents need an updated snapshot of QuestLab's current build in their context before every build cycle** — so Watson builds FROM the end of what QuestLab has done, forward. Not duplicating what already exists. Make that a standing part of the fleet's workflow, not a one-time sync. And use this as the template for how the system develops going forward: sync first, then build.

Also from the audit: PropSearch is ~70% built and real, but has almost no test coverage (4 test files across 76K lines) — QuestLab needs to fix that. And a regular merge cadence (weekly at minimum) so reviewed fork work actually lands in main.

**4. Quick confirms for the call:**

- Our OpenClaw is the public open-source project (openclaw.ai) with your modifications, correct? And Watson runs on a proper API key — nothing token-extraction-based (that's the pattern Anthropic blocked in January and I don't want us anywhere near it).
- The Wattson Discord agent is still unresponsive (I sent the screenshot on WhatsApp + the error email Saturday) — status?

Everything from yesterday's email stands: the seat restructure, the internal-jobs migration plan, the inventory of every Wattson API job tagged internal vs customer-facing with spend split, BYO-subscription for resale. The targets now have numbers attached: I want the plan to get us to low four figures this month, with a path under $1K/month as the gears and migration land. If the architecture fundamentally can't run at that level, I need to hear that on the call, not discover it in August.

Talk Monday.

Graeham Watts
650-308-4727
graehamwatts.com
