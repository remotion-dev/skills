---
name: comedy-craft
description: Reference skill for comedic craft and humor writing — the twin of marketing-psychology, but for being funny instead of persuasive. Use whenever a task needs to land, be witty, or carry personality — video scripts, captions, hooks, ad copy, social posts, listing remarks, newsletters — or when the user asks to make something "funnier," "less generic," "punchier," "more me," or to "use your imagination." This is a reference-only skill — it does NOT produce deliverables. Other skills (content-creation-engine / script-writer, listing-launch-engine, copywriter, newsletter-generator, listing-remarks-writer, and humanizer for the anti-patterns) load it for the technique toolkit, the punch-up pass, the screenshot-test rubric, and Graeham's calibrated humor taste (his comedian roster + edge level). Encodes the core truth that LLM humor needs concrete examples + a generate-many-then-cut process + a human pick — not just instructions. Audience-agnostic for technique; Graeham-calibrated for taste. Pulls brand details from shared-references/identity.json; final prose still runs through humanizer.
---

# Comedy Craft

Reference library for writing things that are actually funny. Loaded by other skills that produce content with personality. Does not produce deliverables itself.

This is the twin of `marketing-psychology`: that skill makes copy *persuasive*, this one makes it *land*. They stack — persuasion gets attention, humor earns the share and the memory. Audience-specific context lives in the deliverable skill; the universal craft of being funny lives here.

---

## The honest ceiling (read once, believe it)

An LLM is a strong *divergent* engine and a weak *taste* engine. It generates 10 attempts fast, never falls for its first one, chases a weird angle without ego. It cannot reliably feel which line is funny to a specific human. So the target is NOT "the model is a great comedian." It is:

> **Consistently not-cringe, occasionally genuinely funny, and Graeham always gets 3-5 options to pick the live one from.**

The human pick is doing real work. Never auto-finalize the funny. Generate → punch up → cut hard → present options → he picks.

---

## Why output goes generic ("drift"), and the two fixes

1. **Regression to the mean.** With no concrete examples in front of it, the model writes the *average* of all content, which is beige. **Fix: anchor on `references/humor-reference.md` right before writing** — read the examples and the taste profile, THEN write. Examples beat instructions.
2. **Dilution.** Asking for 16 deliverables in one pass spreads the creative core thin. **Fix: nail ONE funny core (hook + 2-3 key lines), get it right, THEN derive the platform variants from it.** Don't try to be funny 16 times in parallel.

(Note: "character drift" in AI *video* — a face changing across frames — is a different problem and lives in `cinematic-trailer-pipeline`, not here.)

---

## Graeham's calibrated taste (the most important section — this is the signal)

Graeham's comedian roster: **Mitch Hedberg, Ryan Reynolds, Steven Wright, Anthony Jeselnik, Dan Mintz, Jimmy Carr, Bo Burnham, Tig Notaro, John Mulaney, Milton Jones, Morgan Murphy, Mark Normand** (Normand added 2026-06-27; rest 2026-06-26).

This list is strikingly coherent. The through-line:

- **Deadpan, dry delivery.** Hedberg, Wright, Mintz, Tig, Murphy, Carr. Flat affect. Never sells the joke. The line is funny; the face isn't doing the work.
- **One-liner economy.** Hedberg, Wright, Mintz, Carr, Jones, Murphy. Dense, short, no wind-up. Setup and punch in one breath.
- **Misdirection / the twist.** Jeselnik (the master), Carr, Jones. The setup leads you one way; the punchline snaps the other.
- **Surreal / absurd logic.** Hedberg, Wright, Jones. Unexpected internal logic stated matter-of-factly.
- **Dark-but-clever.** Jeselnik, Carr, Murphy. The *content* is too edgy to use — but the *construction* (surgical economy, the turn) is exactly what to study.
- **Meta / self-aware.** Bo Burnham, Ryan Reynolds. Aware they're performing/selling; break the fourth wall and win points for it.
- **The marketing north star: Ryan Reynolds.** Not a standup — his Maximum Effort ad voice (Aviation, Mint Mobile, Deadpool). Dry, self-aware, fast, brand-safe-but-sharp. He is the single most on-brand reference on this list, because he proves "funny that still sells."
- **The one storyteller: John Mulaney** (with Tig as minimalist story). Tight, callback-driven, a button at the end.
- **The joke-density craftsman: Mark Normand** (added 2026-06-27). Relentless setup-punchline, very high joke-per-minute, quick crowd-work wit. His "velocity" is really **compression** — tags stacked tight, not loudness (a Fugu-QA correction: he's not high-energy, he's *dense*). He widens the range Fugu flagged as narrow: same economy and craft, more tag-density. Mine him for compression (every line a setup or a punch, no fat) and fast stacked hits in a caption. His real engine, like Hedberg's, is the **language audit** — notice a word's hidden rule, then prove it with an absurd counterexample ("you never say 'this ice cream's riddled with sprinkles'").

**What is NOT on the list:** physical/animated (no Maniscalco), hype, high energy, and — the key nuance (Fugu QA) — anything *sentimental*. Note the distinction: the *subjects* can be relatable (anxiety, adulting, the market); what's banned is the *warm, sentimental treatment* of them. Graeham likes **smart, dry, economical, surprising.** Write the relatable thing, but dry-and-sharp, never sweet.

### How to write for Graeham (apply this every time)

1. **Lead with the twist.** Economy over warmth. The turn is the point.
2. **Deadpan it.** State the absurd thing flatly. No "lol," no winking, no exclamation points.
3. **One strong line beats a paragraph of setup.** Cut the runway.
4. **A little surreal is welcome.** Unexpected-but-internally-logical lands for him.
5. **Self-aware/meta is on-brand.** "Yes, a realtor is telling you this" is a feature, not a bug. That's the Reynolds move.
6. **Mine the dark comedians for STRUCTURE, not content.** Jeselnik/Carr/Murphy teach misdirection and surgical economy. Apply that mechanism to *safe* targets — the market, Zillow, the process, himself — never clients, neighborhoods' people, or any protected group.

### Edge calibration (Graeham's exact words, 2026-06-26)

> "A little bit of edge is okay, but nothing that's going to offend people because we still have a business to run. You're okay offending me, but for clients and the kind of stuff we're doing, don't push it too far. I'm okay pushing just a little bit."

Translation: **brand-facing output = clean with a little bite.** Dry, sharp, a touch of edge. Never mean, never crude, never at a client's expense. The dark roster is studied for mechanism; its tone is not copied. When unsure, dial the *content* back and let the *construction* (the twist, the economy) carry the funny.

---

## The technique toolkit

Pick 1-2 per piece, weighted toward the deadpan/twist end for Graeham. Do not stack all of them — 1-3 real moments beats 10 puns.

**1. The twist / misdirection (his favorite — lead here).** Setup points one way, punch snaps the other.
- *"This home has everything a growing family needs. A roof. That's the list. But it's a new roof."*

**2. Specificity over category.** The funniest detail is the true, weirdly specific one.
- *"$1.4M gets you a 1956 Redwood City ranch with the original avocado tile — and five offers by Sunday."*

**3. Deadpan act-out.** Play the character flatly, don't describe them. Zillow as a confident idiot:
- *"Zillow looked at this house for half a second and said, with its whole chest, $1.1 million. It sold for $1.6."*

**4. The unexpected-but-true observation.** Name what everyone notices and nobody says.
- *"Every Palo Alto open house has the same bowl of lemons nobody is allowed to touch."*

**5. One-liner economy.** Setup and punch in one breath. No wind-up.
- *"The Zestimate and the appraisal have never met."*

**6. Surreal logic, stated flat.** Unexpected internal logic, delivered deadpan.
- *"Square footage in the Bay Area is measured in offers, not feet."*

**7. Heightening.** Start true, push one notch past reasonable, then one more.
- *"First you check the price. Then the square footage. Then you learn the square footage includes the garage, the garage includes a tenant, and the tenant has been there since 1998."*

**8. Self-aware / meta (the Reynolds move).** Acknowledge the bit.
- *"Yes, I'm a realtor telling you the market is complicated. Groundbreaking."*

**9. Local in-jokes.** Specifics that prove you live here — the 101 at 5pm, the price cliff across the freeway, La Bamba, the Dutch Goose. One real local reference beats three stats.

**10. The tag.** After the laugh, a small quiet button — a 3-word add-on that lands a second hit.

---

## The punch-up process

Run AFTER a straight draft exists. Order matters:

- **A — Anchor.** Read `references/humor-reference.md` (taste profile + examples). Lock 1-2 techniques that fit the topic and Graeham's lean.
- **B — Find the flat lines.** Mark the 2-3 flattest, most "real-estate-blog" lines. Those are the punch-up targets. Leave lines that already carry a number or a real local detail.
- **C — Rewrite, don't decorate.** Rewrite each flagged line with a technique so the joke makes the point *better*, not just sits beside it. Load-bearing facts (a price, a legal point) stay straight.
- **D — Cut against the rubric.** Run every candidate through the screenshot test. Cut anything that fails. A cut joke costs nothing; a bad joke costs the piece.
- **E — Present options.** Give Graeham 3-5 versions of the hook (and key lines), labeled by technique. He picks. Never silently ship one.

---

## The screenshot test (the rubric)

A line earns its place only if **at least one** is true:
- Would someone screenshot it or send it to a friend?
- Is it specific and true enough that a local nods?
- Does it make the point *better*, not just decorate it?
- Could only Graeham — someone who knows this market — have written it?

If none are true: **cut it. It's filler pretending to be personality.**

---

## Verification — Fugu Ultra (standing default)

Distillation passes and any QA of humor output run through **Fugu Ultra** as an independent second opinion (Graeham's standing instruction, 2026-06-27 — he asked for it repeatedly, so treat it as required, not optional). Call it:
`python "C:\Users\Graeham Watts\Documents\Claude\fugu\fugu.py" --model fugu-ultra --stream -` (heredoc the prompt; `--stream` dodges the 300s non-stream timeout). Use it to (a) sanity-check the taste synthesis against real transcript material, (b) ruthlessly cut a candidate line set down to the keepers, and (c) flag brand-safety, clarity, or repetition issues. On 2026-06-27 it corrected the "language audit" framing, the "unsentimental not un-relatable" nuance, Normand-as-compression, and cut the one line that poked at clients — so it earns its place.

## Guardrails (humor never overrides these)

- **Fair Housing.** Never joke about *who lives somewhere*. Property, process, price, market only. No demographic proxies, ever.
- **No fear-selling, no false precision.** Speak figures as ranges ("about a month," "up roughly four percent").
- **Brand + license.** Pull DRE / brokerage / contact from `shared-references/identity.json` — never typed from memory. Never the blocklisted DRE.
- **Direction of the punch.** Aim at yourself, the industry, Zillow, the process, the absurdity of the market. Never the client, a neighborhood's people, or any protected group.
- **Brand voice wins.** If a loading skill's brand voice conflicts with a joke, the brand voice wins (mirrors the marketing-psychology non-negotiable).

---

## Anti-patterns — the "AI trying to be funny" tells (cut on sight)

- Pun stacking and groaner wordplay ("soul/sole," "a-door-able," "key to your future").
- Dead trend phrases: "Let's be honest," "plot twist," "I said what I said," "the math isn't mathing," "it's giving ___."
- Exclamation-point spam. (Especially wrong for Graeham — deadpan never shouts.)
- Explaining the joke after telling it.
- Forced pop-culture references that don't fit the market.
- Random-for-random's-sake quirk ("anyway, here's a llama").
- The em-dash-heavy "witty aside" cadence that reads as ChatGPT. Match Graeham's no-em-dash prose; the final copy still runs through `humanizer`.

---

## Reference file

| Reference file | Load when |
|---|---|
| `references/humor-reference.md` | Before writing ANY creative/short-form piece. Graeham's comedian roster, the taste profile, and his flagged examples. The single highest-leverage anti-generic input — read it to anchor, every time. |
| `references/joke-architecture.md` | The CONSTRUCTION layer (Fugu-authored): Greg Dean's 5-mechanism build for individual lines/punchlines/hooks (1st Story → Target Assumption → Connector → Reinterpretation → 2nd Story), the UCB game/heightening for escalation, CLoT for concepts, worked EPA examples, templates, debugging, and the hard-scoring batch pipeline. **Load it in the punch-up pass to *construct* a line by mechanism instead of guessing** — this is what raises the hit-rate from 1-in-5 to 3-4-in-5. Taste owns the ceiling; this raises the floor. |
