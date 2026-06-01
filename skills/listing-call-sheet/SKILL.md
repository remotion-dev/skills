---
name: listing-call-sheet
description: "Hybrid Production call-sheet builder for Graeham Watts. When a new listing gets a videographer trip, this turns the single shoot into a full content package: the listing's content plan PLUS a role-split Call Sheet (videographer / agent / editor) so each person gets exactly the instructions they need — including demand-backed extra shots to bank for OTHER videos already queued this month. Use ANY time Graeham says: call sheet, listing call sheet, shoot sheet, shot list for a listing, videographer brief, video brief for my new listing, Wesley is coming out, videographer is coming, plan the shoot, what do we shoot, build the shoot package, content plan for this listing, listing video plan, bank extra shots, forward shots, role-split brief, editor edit sheet, clip IDs, call sheet dashboard, email the videographer the shot list, send the crew the call sheet, email Wesley the brief, or anything about planning and briefing a real estate listing video shoot across videographer, agent, and editor. Also trigger when Graeham gives listing details plus a shoot date and asks what to film, or pastes the month's queued content and wants extra shots attached to an upcoming trip. Output is a visual HTML dashboard, distributed as a Gmail draft to each crew member for Graeham's review. The human still cuts the final video — this skill ONLY plans, briefs, and organizes. It does not auto-edit, does not remember prior runs (that is PropertyIQ's job), and does not build the avatar. One listing per run."
---

# Listing Call Sheet — Hybrid Production

When a new listing comes in, a videographer is already coming out. This skill turns that one trip into a **full content package** so the trip pays for far more than one video.

It produces two things:

1. **A listing content plan** — the listing video (long + short) plus drafted briefs for the PropReach-bound derivatives.
2. **A Call Sheet split into three packets** — one each for the **videographer**, the **agent (Graeham)**, and the **editor** — each written for what that person actually needs, plus **demand-backed forward shots** to bank for other queued videos while the videographer is already on location.

The document this skill produces is called the **Call Sheet**. The mode name is **Hybrid Production** — part content strategy, part field production brief.

## What this skill is and is NOT

This skill **plans, briefs, and organizes**. A human still cuts the final video in CapCut. Hold these boundaries — they are the whole point of the design:

- **No auto-editing.** The output is instructions and an organized asset map. Never assemble or "render" the final cut.
- **Stateless. One listing per run.** Do not remember prior runs, do not track shot-vs-pending across weeks, do not reschedule a calendar. That cross-week memory is the **PropertyIQ** module's job, not this skill's. Each run starts clean.
- **No avatar creation.** This skill *specs the capture* of avatar-source footage. Building the HeyGen avatar from that footage is a separate downstream step.
- **Demand-backed forward shots only, and capped.** Only attach extra shots that a real, queued video actually needs AND that fit where the videographer already is. Cap at **5 extra scenes** per shoot so the trip doesn't bloat and footage doesn't pile up unused.

If Graeham asks this skill to remember last week's shoot or auto-edit, say plainly that's out of scope and point him to PropertyIQ (memory) or CapCut (the human cut).

## STEP 0 — Two required asks (standing rules, never skip)

Before generating anything, ask these two questions. They are Graeham's standing rules, not optional. Ask both in one turn:

1. **"Portrait, landscape, or both?"** — This applies to *every asset in the package*. Portrait = 9:16 (Reels/Shorts/TikTok). Landscape = 16:9 (YouTube long-form). "Both" means every shot gets framed so it can be cropped to either, and the shot list flags which is primary per asset.
2. **"Which HeyGen avatar look carries the talking-head?"** — **Never default.** Offer the known looks (`digital_twin`, `casual_chic`, `freshly_ironed`, `fashion_flip`, `bespectacled`, `suburban_serenity`) or accept a raw look ID. **Voice defaults to Graeham's ElevenLabs clone** unless he says otherwise — only confirm voice if he raises it.

Do not generate the plan or the Call Sheet until both are answered. If Graeham hasn't given the listing details or the month's queued content yet, collect those too (see Inputs).

## Inputs to collect

**Listing details:** address, price, beds/baths, square footage, 3–5 standout features, neighborhood, go-live date, scheduled shoot date.

**The month's queued content** that still needs real footage or B-roll — so the skill can attach demand-backed forward shots to this trip. If Graeham doesn't have it handy, ask for it; without it, the forward-shot section is skipped (don't invent demand).

**People:** videographer name/email, editor name/email (may be the same person).

## The build sequence

Work in this order. Read the reference file named at each step before doing that step.

1. **Write the listing video script** by orchestrating `video-script-creation-engine` (don't reinvent script-writing — that skill owns voice, hook, AEO, GHL keyword CTA, Fair Housing). Produce a long-form script and a matching short-form cut.
2. **Decompose the script into shots** using `references/shot-decomposition-rubric.md`. This is the hard part and the source of all value — see the warning below.
3. **Assign clip IDs** to every shot up front using `references/clip-id-convention.md`. The videographer applies these IDs; he never invents filenames.
4. **Add demand-backed forward shots** (max 5) from the queued content, each tied to a named queued video.
5. **Spec the avatar-source shots** using `references/avatar-source-specs.md` — these have a stricter capture bar than B-roll because HeyGen Avatar IV locks to the source angle.
6. **Build the content plan + three packets** using `references/packet-templates.md`. Paste `references/shot-glossary.md` at the top of the videographer packet. Fill every field with real content — never emit a skeleton.
7. **Run the locked-rules pass** using `references/locked-production-rules.md` before you finish. This is a hard gate.
8. **Render the visual HTML dashboard** from `assets/call-sheet-template.html` — this is the primary deliverable (a clean, color-coded, scannable page, not a wall of text). Produce the MASTER (all packets) plus a videographer copy and an editor copy. Fill every token; keep the "How to read this" box.
9. **Distribute** per `references/distribution.md`: create a Gmail **draft** for each recipient (videographer → their copy; editor → their copy; Graeham → master), with the HTML inline. Drafts only — never blind-send. Present the master to Graeham, then report which drafts you created.

## ⚠️ The hard part — shot decomposition (read this twice)

All the value lives here. The job is to break each script line into *what kind of footage fills it*:

> this line is **avatar**, this line needs a **real exterior at golden hour**, **B-roll** drops here, a **motion graphic** sits on the stat, **VO** runs under the drone shot.

If the decomposition is vague, the videographer shoots the wrong thing and the trip is wasted. So every script line gets a **footage tag** and a **clip ID (or graphic/VO ID)** — no line is left untyped. The full tagging system, the 7 tags, and worked examples are in `references/shot-decomposition-rubric.md`. **Read it before decomposing.** Don't hand-wave "film the kitchen" — say which angle, what scale, golden hour or not, hold duration, and the clip ID it lands under.

Lean on Graeham's existing skills for the craft instead of reinventing it:

- **Script** → `video-script-creation-engine`
- **AI B-roll prompts** (for gaps real footage can't fill) → `cinematic-hooks` to write the prompt, `higgsfield-video` to generate it
- **Avatar specs** → `heygen-video` / `heygen-elevenlabs-renderer` (look IDs, render config)
- **Motion-graphic callouts** → `watts-motion-graphics` (the 5 templates: Stat Callout, Compare Card, Decision Framework, HERO Reveal, End Card)

Your job is to **orchestrate** these, not duplicate them. Reference the right skill at the right line.

## Emit full working documents — never skeletons

The single most important quality rule: **the Call Sheet you produce is a finished, working document, not a fill-in-the-blank form.** Write every line out in full — real composition detail, real word-for-word script, real assembly order. The only legitimate blanks are clip IDs you assign, IDs/URLs the user must supply (GHL number, QR target → mark `[…TBD]`), and genuinely unknowable post-sale data in the case-study shell. If a packet reads like a template with placeholder phrases, it has failed. Someone should be able to pick it up and act with no further questions.

Write all directions in **plain English first** (abbreviation in parentheses only as shorthand). Never "MS gimbal push" — write "Medium shot, waist-up, camera walks slowly toward him on a gimbal (push-in)." The shot glossary (`references/shot-glossary.md`) goes at the top of the videographer packet so any reader is covered.

## Output: the Call Sheet, in three packets

Full templates and worked examples live in `references/packet-templates.md`. The shape:

**Videographer packet** — opens with the plain-English shot glossary, then a numbered shot list. Every field-capture shot carries seven things: clip ID, what's in frame, **composition** (how much of the house/subject is in frame, camera height, sky-vs-ground ratio, exactly where to stand), camera move (plain English), shot size (plain English), location & light, and hold duration. Three categories:
- **(a) Listing shots** for this property's video — each fully composed (the videographer asked for this: roof not clipped, how much sky, where to stand, what light).
- **(b) Extra footage to bank for upcoming videos** ("demand-backed B-roll") — lead with the plain-English explainer: while the videographer is already on location, grab a few extra clips for OTHER videos Graeham already has planned; "demand-backed" = only footage a real planned video actually needs (never random spares); cap 5 scenes; each names the upcoming video it feeds.
- **(c) Avatar-source shots** 