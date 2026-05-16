# Phase 2 — Analyze the Source

Goal of this phase: produce a one-page `source_brief` that tells the writer in Phase 6 exactly what was in the original video, so the rewrite is informed rather than guesswork.

You're not editing or improving yet. You're diagnosing.

## The 7-Field Source Brief

Fill in each field. Be specific. Vague analysis here cascades into vague output later.

### 1. Core Claim

One sentence. What is the original video actually arguing or telling the viewer?

**Good:** "Mortgage rates in 2026 are going to stay above 6.5% because the Fed has signaled no cuts before Q4."

**Bad:** "It's about mortgage rates and the economy." (Too vague — doesn't capture the position.)

If the source has multiple claims, identify the **primary** one (the one the hook + payoff are built around). Note the secondary claims separately for reference.

### 2. Hook Strategy

Identify which of the 8 hook patterns the original creator used. See `hook-frameworks.md`. Common ones in social video:

- **Bold contrarian claim** ("Everyone says X. They're wrong.")
- **Personal stake** ("I just lost $50K because of this mistake.")
- **Pattern interrupt question** ("Why is your landlord suddenly being nice to you?")
- **Specific number shock** ("87% of buyers do this wrong.")
- **Story tease** ("Last week, a client almost lost her deposit because...")
- **Direct address** ("If you're renting in California, watch this.")
- **Curiosity gap** ("There's one thing nobody tells you about closing costs.")
- **Reveal frame** ("I'll tell you what every agent secretly knows.")

If the hook strategy was weak (e.g., the creator opened with "Hey guys, welcome back to the channel"), note that — it's an upgrade opportunity for Phase 5.

### 3. Evidence Quality

For each factual or numeric claim in the source, tag it:

- **Cite-able** — Specific number, date, source — could be defended in writing.
- **Anecdotal** — "I had a client who..." — personal experience, not generalizable.
- **Vague** — "Most people..." / "Studies show..." with no source — needs verification or removal.
- **Opinion** — Framed as opinion, no evidence needed.

Flag anything that needs fact-checking in Phase 4. Don't carry forward unverified vague claims — they'll get cut and replaced with real data.

### 4. Structure

Identify the macro structure:

- **Hook → Setup → Payoff → CTA** (most common 30-90 sec video)
- **List format** ("3 things every buyer does wrong: number one...")
- **Story format** ("Last week I met a client who...")
- **Comparison** ("Here's what changed from 2024 to 2026.")
- **Problem → Solution** ("If you're stuck on this... here's the move.")
- **Q&A / Reaction** (creator responds to a viewer question or another video)

The chosen repurpose angle in Phase 3 may keep this structure or deliberately change it.

### 5. Target Audience Signal

Who was the original creator talking to? Listen for second-person address, jargon level, problems referenced, life-stage clues:

- **First-time buyers** — references to "your first home", down payment, FHA loans
- **Move-up buyers** — references to "selling and buying at the same time", contingencies
- **Investors** — references to cap rates, rentals, cash flow, 1031
- **Renters** — references to leases, rent increases, security deposits
- **Sellers** — references to listing, staging, days on market, agent commission
- **General real estate curious** — broad consumer audience, no jargon
- **Other industry pros** — agent-to-agent talk, MLS, escrow speak

This matters because Graeham's CTA + GHL keyword will be chosen to match the audience. A first-time-buyer video uses `BUY` or `READY`; an investor video uses `INVEST` or `NUMBERS`.

### 6. Length and Pace

- **Word count** of the source
- **Estimated spoken duration** (assume ~150 wpm for conversational pace; ~180 wpm for fast social-media pace)
- **Ideas per 30 seconds** — count the number of distinct claims or transitions. High density (5+) = fast-paced reel. Low density (1-2) = long-form video.

This calibrates Phase 6 — Graeham's rewrite should match the energy of the platform he's posting to, not slavishly copy the source's pacing.

### 7. Localization Need

Critical for Phase 4. Tag the topic on this 3-bucket scale:

- **Strongly local** — Topic is Bay Area / Peninsula / California specific by nature (AB 1482, Prop 19, EPA rent control, SF luxury market, Peninsula commute). Phase 4 pulls heavy local data.
- **Real estate universal** — Topic applies to real estate broadly (mortgage rates, closing costs, buyer-seller psychology) but Graeham CAN frame it locally to deepen authority. Phase 4 adds Bay Area lens where it lands naturally; doesn't force it.
- **Universal non-real-estate** — Topic is general life / business / lifestyle (productivity, mindset, finance basics). Phase 4 does universal research; localization is optional and only if it strengthens the angle.

When in doubt, default to the middle bucket — real estate universal — because Graeham's authority advantage shows up when he adds the Bay Area lens to something the original creator left generic.

## Output Format

Produce a `source_brief` block in markdown like:

```
## Source Brief

1. Core Claim: <one sentence>
2. Hook Strategy Used: <pattern> — <strength assessment: strong / mediocre / weak>
3. Evidence Quality:
   - Claim A: <claim text> → <cite-able / anecdotal / vague / opinion>
   - Claim B: ...
4. Structure: <structure type>
5. Target Audience: <audience>
6. Length and Pace: <word count> words / ~<duration>s / <density rating>
7. Localization Need: <strongly local / real estate universal / universal non-real-estate>

Anomalies / Fair Housing flags: <anything that needs special handling>
```

Hand this brief directly to Phase 3.
