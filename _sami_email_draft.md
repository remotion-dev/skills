Subject: URGENT: $7,300 burned in 12 days — we need a cost restructure now, plus the full rollout agenda

Hey Sami,

Two parts to this email. Part 1 is urgent and needs action this week. Part 2 is the rollout agenda we've been building toward — still important, but Part 1 comes first.

---

## PART 1 — The API burn rate is unsustainable and will kill the project if we don't fix it

I pulled the real numbers from my Anthropic Console today:

- **$7,289 spent in the first 12 days of July** — that's ~$607/day, on pace for **~$18,000/month**
- **2.43 billion input tokens** month-to-date, 34M output
- My $250 auto-reload is refilling multiple times per day

I have to be direct: **I cannot sustain this.** If we can't get this under control, I'll have to cancel the project as it's currently running. That's not where I want to end up — the fix is architectural, and I think it's very doable — but it has to happen now, not eventually.

**What the data shows (this is the good news — the problem is specific, not vague):**

| Model | Input tokens (last 7 days) | Share of volume |
|---|---|---|
| Claude Fable 5 (premium tier) | 1.26 BILLION | ~91% |
| Opus 4.8 | 88.5M | ~6% |
| Sonnet 4.6 | 24M | ~2% |
| Haiku 4.5 | 840K | ~0.06% |

Credit where due: **your prompt caching is excellent** — 97.8% cache hit ratio. Without it this bill would be ~10x worse. So that lever is already pulled. The problem is the two things caching can't fix:

1. **~91% of ALL volume runs on Fable 5, the most expensive model that exists** — while Haiku (roughly 1/30th the cost) is essentially unused. The routine 80% of agent work (file reads, mechanical steps, formatting, status checks, simple edits) is running on the premium reasoning tier.
2. **Raw volume: 1.38 billion input tokens in 7 days.** Even at cached rates that's enormous. I need to understand what runs 24/7, what loops exist, and whether anything polls/retries in ways that burn tokens without producing output.

**The fix — "gears," in priority order:**

1. **Model tiering (the big one).** I get that Fable 5 is the primary coding model and we need it for real coding. But it should be the TOP gear, not the only gear:
   - **Gear 1 — routine/mechanical** (file ops, data extraction, formatting, status checks, simple lookups): Haiku, or a cheap non-Anthropic model — pennies per task.
   - **Gear 2 — standard coding work** (implementing well-specified features, tests, routine refactors): Sonnet 4.6 — a genuinely strong coder at a fraction of Fable's price. Also add **ChatGPT/OpenAI models** into this tier — I want us multi-model so we're not single-vendor priced. DeepSeek is worth evaluating for the cheapest tier too, with one caveat: their hosted API sends data to their (China-based) servers, so nothing client-related or proprietary goes there unless we self-host it.
   - **Gear 3 — Fable 5 ONLY for** architecture decisions, hard debugging, multi-system reasoning, and tasks a lower gear failed at. Escalate up, don't default up.
   
   If ~80% of current Fable volume moves down-gear, that alone likely cuts the bill by several thousand dollars a month.

2. **Volume audit.** Please send me a breakdown of what Watson runs continuously vs. on-demand, and per-step model usage for a typical day. I want to find whatever is generating a billion-plus tokens a week and confirm it's all genuinely productive work.

3. **Context diet.** The input:output ratio is 71:1 — huge contexts resent constantly. Where steps don't need the full spec/codebase in context, use retrieval instead of stuffing. (Related: I've got a Graphify knowledge-graph system running on my machine — measured 25-225x token reduction per lookup vs. reading raw files — worth a look for the Watson/PropIQ repos: could you apply it across the PropIQ repo, and the same across Wattson?)

4. **Batch API — 50% off everything schedulable.** Anything on a schedule rather than needed-right-now: CMAs on a weekly cadence (want a "run now vs. queue for the weekly batch" option in the CMA flow), farming postcards (1st/15th), weekly content calendars, monthly newsletter assembly, weekly social reports.

5. **Shift human-supervised work onto subscription seats.** Claude Code usage under a real human's subscription seat is covered by the subscription, not metered API. Anything you or the team actively drive (kicking off and supervising sessions) should run that way. IMPORTANT constraint we have to respect: unattended automation on a subscription login is against Anthropic's ToS — it's the exact pattern they blocked OpenClaw-style token extraction for in January. So: humans on seats, true unattended automation stays on API (but cheap, per the above). Related — quick confirm: our OpenClaw IS the public open-source project (openclaw.ai) with your modifications, right? And is Watson's current setup running on a proper API key (fine) vs. anything token-extraction-based (the blocked pattern)?

**Target:** I want a plan from you this week to get the monthly run-rate from ~$18K to low four figures as step one, with a path to under $1K/month as the system matures. If the architecture fundamentally can't operate at that level, I need to know that now so we can rescope what Watson does.

---

## PART 2 — The rollout agenda (from before, still current)

**A. Wattson agent unresponsive on Discord.** I messaged it and got nothing back — already sent you an image on WhatsApp. Please check.

**B. Team structure & individual assistant agents (from our Monday conversation).** As we build the per-person virtual assistants for me and my team:
   - Same token-efficiency design requirement applies from day one — reasoning depth scaled to task complexity, or spend scales with headcount.
   - I'm cross-referencing my Team Directory role docs against the Wattson Playbook Library to map what's automatable per person — will sync with you once organized.
   - Security: per-person permission scoping from the start — OpenClaw's Gateway has broad file/shell/browser access by design, and that's drawn public security scrutiny. You've probably got this covered; flagging anyway.
   - Naming: continuing the Watson → Hudson pattern — thinking Dawson/Carson/Mason for individual assistant agents.

**C. OpenClaw mobile app + white-labeling.** The new iOS/Android apps are remote-controls into a running Gateway (not standalone agents). Want to explore white-labeling eventually — build with that in mind rather than retrofit.

**D. Claude Team plan.** I'm setting up Team seats for the humans (me and team members who'll actually use it) — that's ~$460-525/mo all-in, separate from and unrelated to the API problem above. Watson does NOT get a seat (ToS, see above).

Let's get a call on the calendar this week for Part 1 — it can't wait for the usual cadence. Happy to walk you through the Console data and everything I've got running here.

Graeham
