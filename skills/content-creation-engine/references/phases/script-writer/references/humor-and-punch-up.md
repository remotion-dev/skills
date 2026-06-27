# Humor & Punch-Up Pass

This is the missing layer. `voice-and-style.md` makes a script credible, accurate, and on-brand. It does NOT make it land, and several of its rules (data-first, no hype, "cut anything that sounds like a blog intro") actively flatten humor. This file is where the script earns a laugh, a screenshot, or a share — without breaking a single voice or compliance rule.

Read this on any TOFU or MOFU piece, any short-form hook, and any time Graeham asks for "personality," "make it funny," "less generic," or "use your imagination." For straight BOFU/legal/data pieces, apply lightly — one warm line at the open, then play it straight.

---

## The honest ceiling (read once, believe it)

An LLM is a strong *divergent* engine and a weak *taste* engine. It can generate 10 attempts fast, never falls in love with the first one, and will chase a weird angle without ego. It cannot reliably feel which line is actually funny to a specific human. So the target is NOT "the model is a great comedian." The target is:

> **Consistently not-cringe, occasionally genuinely funny, and Graeham always gets 3-5 options to pick the live one from.**

The human pick at the end is doing real work. Never auto-finalize the funny. Generate, punch up, cut hard, present options.

---

## Why output goes generic ("drift")

Two failure modes, two fixes:

1. **Regression to the mean.** With no concrete examples in front of it, the model writes the *average* of all real-estate content, which is beige. **Fix: anchor on real examples right before writing** — skim `swipe-file.md`, lock 1-2 techniques from this file, THEN write. Examples beat instructions.
2. **Dilution.** Asking for 16 deliverables in one pass spreads the creative core thin; the funny idea never gets nailed once. **Fix: nail ONE funny core (hook + 2-3 key lines), get it right, THEN derive the platform variants from it.** Don't try to be funny 16 times in parallel.

(Note: "character drift" in AI *video* — a face changing across frames — is a different problem and lives in `cinematic-trailer-pipeline`, not here.)

---

## The technique toolkit (real-estate / Bay Area examples)

Pick 1-2 per piece. Do not stack all of them — 1-3 real moments beats 10 puns.

**1. Specificity over category.** The funniest detail is the true, weirdly specific one.
- Flat: *"Bay Area homes are expensive and need work."*
- Better: *"$1.4M gets you a 1956 Redwood City ranch with the original avocado bathroom tile, and the sellers will still get five offers by Sunday."*

**2. The unexpected-but-true observation.** Name the thing everyone notices and nobody says.
- *"Every Palo Alto open house has the same bowl of lemons nobody is allowed to touch."*
- *"We all agree 'cozy' in the listing means charming, and not 'you will hit your head.'"*

**3. Heightening.** Start true, push one notch past reasonable, then one more.
- *"First you check the price. Then the square footage. Then you realize the square footage includes the garage, the garage includes a tenant, and the tenant has been there since 1998."*

**4. Misdirection (the turn).** Set an expectation, snap it.
- *"This home has everything a growing family needs. A roof. That's the list. But it's a new roof."*

**5. Rule of three, twist on the third.** Two straight, third breaks the pattern.
- *"Buyers want natural light, good bones, and to win an offer without selling a kidney."*

**6. Deadpan act-out.** Play the character, don't describe them. The Zestimate as a confident idiot:
- *"Zillow looked at this house for half a second and said, with its whole chest, $1.1 million. It sold for $1.6."*

**7. Self-deprecation / insider honesty.** Punch at yourself or the industry, never the client.
- *"Yes, I'm a realtor telling you the market is complicated. Groundbreaking."*

**8. Local in-jokes.** Specifics that prove you actually live here — the 101 at 5pm, the price cliff across the freeway, La Bamba, the Dutch Goose, the perpetual "is EPA the next ___" discourse. One real local reference signals more authority than three stats.

**9. The tag.** After the laugh, a small quiet button — a 3-word add-on that lands a second hit.

---

## The punch-up pass (the process)

Run AFTER the straight script exists (Step 6 of the pipeline). Order matters:

- **A — Anchor.** Skim `swipe-file.md`. Lock 1-2 techniques above that fit this topic + funnel stage.
- **B — Find the flat lines.** Read the draft and mark the 2-3 flattest, most "real-estate-blog" lines. Those are your punch-up targets. Don't touch the lines that already carry a number or a real local detail.
- **C — Rewrite, don't decorate.** Rewrite each flagged line with a technique so the joke *makes the point better*, not just sits next to it. If a line is purely informational and load-bearing (a price, a legal fact), leave it straight.
- **D — Cut against the rubric.** Run every candidate joke through the screenshot test below. Cut anything that fails. Ruthless. A cut joke costs nothing; a bad joke costs the whole piece.
- **E — Present options.** Give Graeham 3-5 versions of the hook (and key lines) to choose from, labeled by which technique each uses. He picks. Never silently ship one.

---

## The screenshot test (the rubric)

A line earns its place only if **at least one** is true:
- Would someone screenshot it or send it to a friend?
- Is it specific and true enough that a local nods?
- Does it make the point *better*, not just decorate it?
- Could only Graeham — someone who actually knows this market — have written it?

If none are true: **cut it. It's filler pretending to be personality.**

---

## Guardrails (humor never overrides these)

Everything in `voice-and-style.md` and the engine's compliance rules still binds. Specifically:
- **Fair Housing.** Never joke about *who lives somewhere*. Property, process, price, and market only. No demographic proxies, ever. (See the Fair Housing block in the engine CLAUDE.md.)
- **No fear-selling, no false precision.** Still speak figures as ranges ("about a month," "up roughly four percent").
- **Brokerage + license rule.** Intero Real Estate; DRE# 01466876 where required. Never the blocklisted DRE.
- **Direction of the punch.** Aim at yourself, the industry, Zillow, the process, the absurdity of the market. Never at the client, a neighborhood's people, or any protected group.

---

## Anti-patterns — the "AI trying to be funny" tells (cut on sight)

These read as ChatGPT-doing-a-bit and instantly cheapen the piece:
- Pun stacking and groaner wordplay ("soul/sole," "a-door-able," "key to your future").
- Dead trend phrases: "Let's be honest," "plot twist," "I said what I said," "the math isn't mathing," "it's giving ___."
- Exclamation-point spam.
- Explaining the joke after telling it.
- Forced pop-culture references that don't fit the market or the audience.
- Random-for-random's-sake quirk ("anyway, here's a llama").
- The em-dash-heavy "witty aside" cadence. Match Graeham's no-em-dash prose; run `humanizer` on the final copy.

Final gut check (extends the one in `voice-and-style.md`): read the punched-up hook aloud. If it sounds like a confident local who is genuinely a little funny, keep it. If it sounds like a brand "doing comedy," cut back to straight and add one honest observation instead.
