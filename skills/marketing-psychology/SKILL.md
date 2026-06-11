---
name: marketing-psychology
description: Reference skill for sales and marketing persuasion psychology. Use this skill whenever the task involves persuasion, selling, marketing, copywriting, sales pages, ad copy, email subject lines, headlines, hooks, CTAs, objection handling, sales scripts, listing presentations, webinars, landing pages, pre-framing, or any communication intended to move someone from where they are to where you want them to be. Also trigger when the user references the "Gap framing," "the panel," "psychological levers," "Cialdini," "Schwartz awareness levels," "market sophistication," "StoryBrand," "tactical empathy," "Monroe's motivated sequence," or any named persuasion framework. This is a reference-only skill — it does NOT produce deliverables. Other skills (copywriter, content-creation-engine, newsletter-generator, farming-postcard, listing-remarks-writer, price-reduction-angle-generator, cma-generator, past-client-follow-up-system, etc.) load this skill for craft foundations and apply audience-specific context themselves. Audience-agnostic by design.
---

# Marketing Psychology

Reference library for sales and marketing persuasion. Loaded by other skills that produce persuasive copy. Does not produce deliverables itself.

**Audience-agnostic.** The universal craft of persuasion lives here. Audience-specific context (who the reader is, what they fear, what they want) lives in the deliverable skill itself (e.g., `copywriter` intake, `content-creation-engine` pillars, `farming-postcard` archetypes).

This skill enforces a five-step process. Loading skills should run all five steps in order. Each step has its own section below.

---

## Local Adaptations (Graeham's toolkit)

Source: Jason Pantana's AI Marketing Academy "Marketing-Psychology Claude Skill" (super skill, June 2026), installed 2026-06-11 and adapted for this repo.

- **Primary loaders:** `copywriter` (deliverable engine — this skill is its diagnosis/panel/audit layer), `content-creation-engine`, `newsletter-generator`, `farming-postcard`, `listing-remarks-writer`, `price-reduction-angle-generator`, `cma-generator` (email/cover copy), `past-client-follow-up-system`.
- **Brand identity:** any deliverable produced under this skill's guidance pulls brand details (DRE, brokerage, contact info) from `skills/shared-references/identity.json` — never typed from memory or prior context.
- **Final pass:** persuasive prose still runs through the `humanizer` skill before delivery, per the `copywriter` convention. This skill's Step 5 failure audit happens BEFORE humanizing; humanizer is the last touch.
- **Division of labor vs. `copywriter`:** `copywriter` owns formats, character counts, 3-variation output, and tone calibration. This skill owns reader diagnosis (Schwartz awareness/sophistication), framework selection, lever-to-blocking-force matching, the 11-mind panel check, and the failure audit. When both load, run this skill's Steps 1–3 before drafting, `copywriter` Steps 2–4 to draft, then this skill's Steps 4–5 to pressure-test.

---

## Scope of This Skill

The five-step process is the spine. How fully you apply it depends on the work:

**Substantive copy** (ads, emails, landing pages, sales pages, scripts, talks, posts, presentations) → run all five steps in order.

**Micro-copy** (subject lines, button labels, single headlines) → Steps 1, 3, and 5 still apply. Step 2 (framework) is overkill for one sentence. Step 4 (panel) reduces to consulting one mind whose territory is the relevant craft (e.g., Ogilvy for headlines).

**Internal communications, retention, or activation copy** → Step 1 (diagnosis) still applies. Step 2 usually doesn't — these aren't sales motions, they're information design with persuasive elements. Apply Steps 3-5 selectively.

**Live persuasion** (stage talks, sales calls, listing presentations) → Steps 1, 3, and 5 transfer cleanly. Steps 2 and 4 are weaker — the panel skews written, and frameworks need adapting for live delivery. Supplement with live-delivery sources where available.

**Two non-negotiables, regardless of scope:**

1. **Never silently invent a diagnosis.** If Step 1's information is missing, ask the user or flag the assumptions explicitly in the output. The whole skill collapses if Step 1 is wrong.

2. **Brand voice overrides lever selection.** When the loading context's brand voice conflicts with what the diagnosis suggests, defer to brand voice. A brand that doesn't use fear shouldn't use fear, even if the diagnosis says fear would convert harder.

---

## Foundations

Three rules that govern everything else.

### A lever is a mechanism, not a tactic

A **lever** is a psychological mechanism that, when activated, makes someone more likely to act. Tactics are specific words and formats. Levers are the underlying force the words activate.

> *"Limited time offer — 24 hours only"* is a tactic. *Scarcity* is the lever.

The same lever can be expressed through hundreds of tactics. Tactics decay through overuse. Levers don't — they're rooted in cognition. A great copywriter has a small library of levers and a large library of tactics. A bad one has a large library of clichés.

This connects to Schwartz's foundational principle: *"Copy cannot create desire. It can only channel the desires of the masses."* You're not making someone want something they don't already want — you're showing them that what they already want is available, here, now, in this form. The whole craft is finding the existing desire and naming it more precisely than they've named it themselves.

### Levers stack but don't substitute

Two levers in one piece can compound. Three or more in short copy weakens the work — the reader senses the pile-on and recoils.

- **Short copy** (ad, headline, subject line): 1 dominant, optionally 1 supporting
- **Medium copy** (email, post, landing page section): 1-2 dominant, 1-2 supporting
- **Long copy** (sales page, webinar, presentation): layered across sections, but each section still leads with one

Stacking levers from incompatible categories (fear + permission, scarcity + abundance) creates dissonance. The reader can't track what they're supposed to feel. Pick one emotional spine per piece.

### Persuasion vs. manipulation

**Persuasion** activates a real desire or pain the reader already has and offers a real solution.
**Manipulation** fabricates urgency, fear, or desire that doesn't exist, or promises an outcome the offer can't deliver.

The litmus test: *if the reader saw exactly how the lever was being used, would they still feel honest?* Yes → persuasion. No → manipulation.

This skill never crosses that line and pushes back when asked to. Honest persuasion compounds; manipulation works once.

---

## Step 1 — Diagnose

Five questions, in order. Answer all five before moving to Step 2.

### Q1: Awareness stage (Schwartz)

Where the reader sits dictates everything else.

| Stage | What they know | What works |
|---|---|---|
| Unaware | Don't know they have a problem | Storytelling, intrigue, indirect approach |
| Problem-aware | Know the problem, don't know solutions exist | Name and dimensionalize the problem |
| Solution-aware | Know solutions exist, don't know yours | Differentiate. Why this, not the others |
| Product-aware | Know about your product, haven't bought | Disarm objections. Specifics, proof, risk reversal |
| Most-aware | Ready to buy, just need a nudge | Direct offer, real urgency, friction removal |

Most common failure: writing problem-aware copy to a most-aware audience (boring them) or writing most-aware copy to an unaware audience (confusing them).

### Q2: Market sophistication stage (Schwartz)

How exposed the market is to claims like yours.

| Stage | The market | What works |
|---|---|---|
| 1: First | Nobody has made this claim before | Plain, direct claim |
| 2: Repeated | Others have made the claim | Bigger or more specific claim |
| 3: Skeptical | Basic claim is tired | New mechanism |
| 4: Numb | Mechanism claims are tired | Bigger mechanism, or new identity |
| 5: Exhausted | Heard everything | Identification — sell tribe membership, not outcome |

Most established markets are at stage 4 or 5. Most copy still operates at stage 1 or 2 — which is why it bounces.

### Q3: Emotional state right now

What is the reader actually feeling at the moment they encounter this piece?

- **Pain** — relief-seeking. Lead with naming the pain.
- **Curiosity** — interested but not committed. Lead with the curiosity gap.
- **Aspiration** — wants more, not in pain. Lead with vision.
- **Skepticism** — burned before. Lead with disarmament.
- **Fatigue** — tired of this category. Lead with anti-pattern.
- **Apathy** — doesn't care yet. Lead with stakes.

### Q4: Blocking force

What is stopping the reader from acting *right now*?

Time. Money. Trust. Inertia. Confusion. Past disappointment. Fear of judgment. Decision fatigue. Wrong moment.

The lever choice in Step 3 must address the specific blocking force. If the block is trust, scarcity won't move them. Match the lever to the lock.

### Q5: Audience temperature

- **Cold** — never heard of you. Filter and earn attention.
- **Warm** — knows you, hasn't bought. Lower friction, sharper offer.
- **Hot** — actively considering. Direct, specific, friction removal.

### Diagnostic shorthand

Before moving to Step 2, fill in this sentence:

> *"This reader is at [awareness stage] in a [sophistication stage] market, currently feeling [emotional state], blocked by [force], and the audience temperature is [cold/warm/hot]."*

If you can't fill it in, you don't have enough information. Either ask the user or flag assumptions.

---

## Step 2 — Structure

Pick the framework that fits the diagnosis and the format. Then decide where pre-framing and objection handling sit inside that framework.

### Framework decision tree

```
Is this short copy with one job (ad, post, micro-CTA)?
  YES → Hook-Story-Offer (Brunson)
  NO ↓

Is this long-form, moving someone from cold to committed in one piece (sales page, webinar, talk)?
  YES → Monroe's Motivated Sequence
  NO ↓

Does the customer have a problem the offer solves?
  YES → StoryBrand (Miller)
  NO ↓

Is this troubleshooting/support content?
  YES → PAS (Problem-Agitate-Solve)
  NO → No framework needed; structure with information design + selective levers
```

**Hook-Story-Offer** — Hook stops the scroll. Story creates the curiosity gap or names the pain. Offer collapses friction.

**Monroe's Motivated Sequence** — Attention → Need → Satisfaction → Visualization → Action. The visualization step is what most writers skip; it's the step that converts.

**StoryBrand** — Customer is the hero with a problem. Brand is the guide with empathy + authority. Plan, call to action, stakes named.

**PAS** — Problem, Agitate, Solve. Compressed StoryBrand for short troubleshooting copy.

(AIDA is acknowledged as predecessor to Monroe but largely superseded.)

For deep reference on each framework, see `references/frameworks.md`.

### Pre-framing — the opening move of any framework

What happens *before* the main message lands often matters more than the message itself. Pre-framing opens the right mental door before walking through it. This is Cialdini's pre-suasion territory.

Pre-framing lives in the **opening** of whatever framework you chose:
- Hook-Story-Offer → pre-frame is inside the hook
- Monroe → pre-frame is the Attention step
- StoryBrand → pre-frame sets the customer's problem in scene before naming it
- PAS → pre-frame primes the problem before stating it

Pre-framing moves: question first, concept priming, temporal framing, identity priming, permission priming.

Test: *Does the opening prime the reader to be receptive to what comes next, or does it just announce what's coming?* Announcing kills the move. Priming makes the work land.

For full treatment with examples, see `references/named-tasks.md`.

### Objection handling — the second-half move

The reader has objections before they finish reading. Naming and disarming them before they fully form is the persuasive move. Pretending the objections don't exist is the failure.

Objection handling lives in the **second half** of whatever framework you chose:
- Hook-Story-Offer → after the offer, before the CTA
- Monroe → inside Visualization and just before Action
- StoryBrand → between the plan and the call to action
- PAS → inside Solve, after presenting the path

**Mini-framework: Acknowledge → Reframe → Evidence**

1. Acknowledge — say the objection out loud (Voss's labeling: *"It seems like…"*)
2. Reframe — offer the new lens, not denial
3. Evidence — specific proof for the reframe

Test: *Did I name the objection more clearly than the reader had named it themselves?* If they could state it sharper than the copy did, the disarm misses.

For full treatment with examples, see `references/named-tasks.md`.

---

## Step 3 — Lever

Pick 1 dominant lever, optionally 1 supporting. The diagnosis from Step 1 determines which fits.

### Lever library at-a-glance

**Fear-based** (use when reader is in pain or complacent)
Loss aversion · The Gap · Time bankruptcy · Status threat · Cost of inaction

**Desire-based** (use when reader is curious or aspirational)
Gain framing · Unfair advantage · Compounding system · Identity reinforcement · The vision

**Social** (Cialdini's 7 principles)
Reciprocity · Commitment/consistency · Social proof · Authority · Liking · Scarcity · Unity

**Cognitive** (use to break thinking patterns)
Curiosity gap · Pattern interrupt · Specificity · Anchoring · Reframing

**Action** (use to remove the last barrier)
Real urgency · Friction removal · Risk reversal · Named-objection disarmament

**Identity** (use when self-concept is the door in)
"You're already that person" reframe · Peer signal · Tribe markers

**Stickiness** (use only when shareability is part of the goal)
STEPPS (Berger) · SUCCESs (Heath brothers)

For full descriptions of each lever — when each fires, what each pairs with, what each fails at — see `references/levers.md`.

### Selection — the blocking-force matrix

Match the lever to the lock. The blocking force from Step 1 Q4 dictates which levers move them and which don't.

| Blocking force | Strongest levers |
|---|---|
| Time | Specificity, compounding system, friction removal |
| Money | Risk reversal, anchoring, cost of inaction, gain framing with ROI |
| Trust | Authority, named-objection disarm, real testimonials, risk reversal |
| Inertia | Loss aversion, the Gap, real urgency, friction removal |
| Confusion | Specificity, clarity, plan |
| Past disappointment | Named-objection disarm, mechanism difference, evidence |
| Fear of judgment | Identity reinforcement, peer signal, unity |
| Decision fatigue | Pattern interrupt, anti-pattern voice, specificity |
| Wrong moment | Real urgency, friction removal, low-commitment first step |

### Selection — the sophistication-stage shortcut

Default lever orientation by Schwartz market sophistication (Step 1 Q2):

- Stage 1-2 → Direct claim + Specificity
- Stage 3 → New mechanism + Authority
- Stage 4 → Bigger mechanism + Identity
- Stage 5 → Identity + Unity + Anti-pattern

### Stack rules

When stacking two levers, **one carries the emotional weight, the other supports**. They must come from compatible emotional categories — the reader has to know what they're being asked to feel.

**Compatible stacks** (the second amplifies the first without conflict):
- Specificity + Identity — works at any stage
- Loss aversion + Real urgency — works for inertia blocks
- Social proof + Authority — works for trust blocks
- Curiosity gap + Specificity — works for cold audiences
- Identity + Unity — works at sophistication stage 5

**Incompatible stacks** (cause dissonance, the reader can't track the emotional ask):
- Fear + Permission (which feeling is the reader supposed to have?)
- Scarcity + Abundance (logical conflict)
- Authority + Liking, taken to extreme (the brand is either the expert or the friend; choose)
- Multiple fear levers (Loss + Status threat + Cost of inaction = panic copy, not persuasion)

For deeper treatment of why each stack works or fails, see `references/levers.md`.

---

## Step 4 — Panel Check

Eleven minds. Don't load all 11 every time — load the ones whose territory matches the work being done.

### Panel cheat sheet

| Stage of work | Consult |
|---|---|
| Headlines, hooks | Ogilvy, Kennedy, Bernbach |
| Structure (long form) | Miller, Brunson |
| Voice / tone | Godin, Bernbach |
| Transitions | Phil M. Jones |
| Lever selection sanity check | Cialdini, Schwartz |
| Sales conversation, objection handling | Voss, Phil M. Jones |
| Positioning, category | Ries |

Note on Cialdini and Schwartz: their primary work is in Step 1 (Schwartz's awareness and sophistication frameworks) and Step 3 (lever selection grounded in Cialdini's principles). At Step 4, consult them only as a sanity check — *did the lever I chose actually match the principle I think it's invoking, and the awareness stage I diagnosed?*

### The eleven minds

- **Ogilvy** — Headlines, specificity, respect for the reader
- **Miller** — Customer-as-hero structure, clarity
- **Brunson** — Direct response, hook-story-offer, real offers
- **Godin** — Voice, remarkability, no filler
- **Phil M. Jones** — Bridge phrases, transitions, sales conversation patterns
- **Kennedy** — Filtering, calling the reader by name, real urgency
- **Bernbach** — Wit, anti-advertising honesty, "sound least like an ad"
- **Cialdini** — The 7 principles, behavioral grounding
- **Schwartz** — Awareness stages, market sophistication, channeling existing desire
- **Voss** — Tactical empathy, mirroring, labeling, objection handling
- **Ries** — Positioning, category strategy, market laws

For each mind's deeper lens, anchor moves, and the specific test they apply — see `references/panel.md`.

If a draft fails any consulted panel member's test, rewrite that piece before moving on.

---

## Step 5 — Failure Audit

Eleven failure modes. Run the audit before shipping. Each comes with a fix.

| Failure | Symptom | Fix |
|---|---|---|
| **Hype** | Reads like every other ad in the category | Replace abstract claims with specific ones |
| **Manipulation** | Lever doesn't honestly match the offer | Apply the litmus test; if no, replace |
| **Formula** | Framework is showing through | Vary sentence length, break the pattern in each section |
| **Wrong-stage writing** | Over- or under-explaining for the audience | Re-do the diagnostic |
| **Lever pile-on** | 3+ levers in short copy | Pick one dominant; cut to supporting at most |
| **Hero-of-own-marketing** | "We do this. Our team. Our process." | Rewrite with customer as hero, brand as guide |
| **Unfiltered hook** | Works for everyone, magnetic to no one | Add a filter; name the audience |
| **Faux-clever** | Brand trying to sound clever | Cut the cleverness; find the obvious true thing |
| **No real offer** | Reader doesn't know what they get | Name the specific outcome; free + specific + now |
| **Pre-frame mismatch** | Opening primes ≠ body delivery | Rewrite the hook or the body so they match |
| **Objections unaddressed** | Obvious doubts ignored | Name the top 3; Acknowledge → Reframe → Evidence each |

For symptom + cause + fix detail on each failure mode, see `references/failure-modes.md`.

---

## Reference Files and When to Load Them

The five steps above are the working spine. Most persuasive tasks can be completed using only this SKILL.md. Load reference files only when the depth is needed.

| Reference file | Load when |
|---|---|
| `references/frameworks.md` | Picking between StoryBrand, Monroe, or Hook-Story-Offer needs deeper guidance, or when applying a framework feels mechanical |
| `references/levers.md` | Lever selection requires understanding *why* a lever fires, what it pairs with, or what its specific failure mode is |
| `references/panel.md` | A panel member's territory is central to the work and surface-level cheat-sheet guidance isn't enough |
| `references/named-tasks.md` | Pre-framing or objection handling is in scope and you need worked examples of how each move plays out |
| `references/failure-modes.md` | A specific failure has been spotted and needs deeper diagnosis to fix |
| `references/examples.md` | Calibration on what good output looks like — includes a poor-draft-then-rewrite, a pre-framing demonstration, and an objection-handling demonstration |

If you skip Step 1, Steps 2-5 are guesswork. If you skip Step 4, the failure modes hide. If you skip Step 5, hype slips through. The process produces better copy when applied in order.
