---
name: concept-forge
description: The writers' room — a divergent ideation engine that generates novel, avatar-realizable, truth-anchored video/content CONCEPTS with strong scored hooks, then returns the top 5 as concept cards for Graeham to greenlight. Use whenever the task is to come up with original video or content IDEAS, concepts, angles, hooks, or "what should this video be" — for a listing, a geographic farming push, a market/education piece, or a direct-response ad. This is an EXECUTABLE engine (it generates, scores, and selects), not a passive reference. It is CALLED BY content-creation-engine (generic/geographic content) and listing-launch-engine (listing content); it does not orchestrate them. It loads comedy-craft for the hook/VO voice and marketing-psychology for the CTA. It hands the chosen concept to cinematic-video-engine for execution. Trigger phrases: concept ideas, video concepts, give me concepts, unique angles, strong hooks, creative ideas for this listing, farming video ideas, make it not generic, pitch me concepts, what's the hook. Every concept is anchored to a real real-estate truth, realizable with an existing avatar + videographer plates, and brand-safe (clean with a little bite). Fugu Ultra is the standing QA gate.
---

# Concept Forge — the writers' room

Divergent ideation. Generate ~25 concepts, score them, return the **top 5 concept cards**. This is the half of the system that solves "the ideas come out generic." It is high-temperature and wide; the *execution* (convergent, structured) lives in `cinematic-video-engine`. Do not do both in one pass — they are opposite cognitive jobs.

**The non-negotiable order (Fugu's rule): Funnel goal + audience → real-estate TRUTH → idea engine → (hook) → score → gate.** Never start from the visual or the gag. A concept with no true tension underneath is just weirdness.

---

## Inputs (the brief)

Gather before generating. Ask only for what's missing; don't block on optional fields.
- **What** — a listing (with its facts) OR a generic topic (geographic farm, market update, education, ad).
- **Channel + funnel slot** — listing video / farming / market-ed / direct-response; TOFU/MOFU/BOFU.
- **Audience** — who, and what they currently feel.
- **Avatar inventory** — which of Graeham's existing avatars/looks are available (pull from the avatar registry; if absent, ask). Concepts must use a look that EXISTS.
- **Platform** — Reel / Short / YouTube / ad.
- **Forbidden** — clichés to avoid, brand/compliance limits.

---

## The 7 idea engines (spread across them — chaos is ONE of seven)

Each is a *generative mechanism* for finding a novel concept. A good run uses at least 4 different engines so nothing collapses into one format.

1. **Unfazed Expert in Chaos** — escalating visual catastrophe; the avatar delivers calm property specs and never acknowledges it. (The flagship, not the whole toolbox.)
2. **Literalized Anxiety** — a real buyer/seller fear made physically literal (the inspection report as a creature; "missing the top" as melting clocks).
3. **Absurd World Law** — define one impossible rule of this world, then behave normally inside it ("in this town, houses choose their buyers").
4. **Prestige Documentary over the Mundane** — Ken Burns / nature-doc treatment (reverent, slow, awed) pointed at a subject with **built-in absurdity or friction** (a bidding war as a predator sequence; an open-house ritual). The funny is the *mismatch*, so the subject must carry it. **Never aim the reverence at something earnest** (equity, "a porch," a lockbox) — that produces nothing (learned from Graeham's 2026-06-27 review: the lockbox/lemons subjects were dead, the bidding-war was the keeper).
5. **Open House as Ritual/Bureaucracy** — treat a normal step as solemn ceremony or absurd red tape ("buyers must prove themselves worthy of the mudroom").
6. **Luxury Feature as Survival Infrastructure** — frame a plain feature as tactical/elite ("technically a pantry, strategically a bunker with shelving").
7. **Wrong-Genre Transfer** — shoot a real-estate moment in a borrowed genre (heist, hostage negotiation, courtroom, disaster briefing).

**Visual modes** (the *look*, chosen later by `cinematic-video-engine`; concept-forge only notes a candidate): Absurdist Juxtaposition · Hyper-Stylized Luxury (A24/Wes Anderson) · High-Octane Action · Documentary Realism.

---

## The real-estate truth anchor

Every concept bolts to a TRUE tension. Keep a running truth bank; seed examples:
- Sellers overvalue; buyers want charm until charm needs plumbing.
- Everyone thinks they missed the window.
- The Zestimate has never been inside the house.
- Equity-rich longtime owners don't know their number.
- Location beats finishes; mortgage math feels fake.
- Open houses are social theater; disclosures turn optimism into paperwork.

If a concept can't name its truth in one sentence, cut it.

---

## The hook lab (runs on every surviving concept)

Per concept, write **2-3 candidate spoken hooks** for the 0:00-0:03:
- **Under 20 words.** AI over-writes intros; enforce it.
- Score each hook 1-10 on five vectors (thumbstop): **Curiosity · Specificity · Pattern-Interrupt · Emotion · Stakes.**
- **Gate: average ≥ 8 AND no single vector < 7.** Rewrite up to 3 rounds; if it still fails, the concept is weak, not the hook.
- Keep the hooks in *different* styles — don't converge them into one "optimized" line.
- Note the opening visual and whether its tone **contrasts or matches** the line (contrast is a technique, not a law — luxury/trust pieces often want congruence).

The score is a **heuristic, not truth.** Graeham's pick and real performance are the validators. Load `comedy-craft` so the hooks land dry, not cheesy.

---

## The avatar-aware "shootable" gate (coarse pass)

Because Graeham isn't on site, a concept is only viable if (5 checks):
1. **Truth supportable by plates** — real B-roll can carry the claim; no premise the location can't sell.
2. **Plate capturable** — clean space for avatar placement; usable framing/duration/vertical crop; avoid mirrors, heavy reflections, occlusions, chaotic handheld unless planned.
3. **Existing avatar fits** — a current look matches wardrobe/posture/angle; no walking/pointing/holding/door-opening unless that render mode supports it.
4. **Composite plausible** — eyeline, scale, lighting direction, camera height, lens all matchable.
5. **No new-avatar on the critical path** — if it needs a look that doesn't exist yet, it goes to the avatar backlog, not this deliverable.

concept-forge runs this **coarse** (possible?). `cinematic-video-engine` does the detailed avatar-match spec later.

---

## Scoring & selection

Generate ~25 → score each on **Truth · Novelty · Shootability · Brand-fit · Funnel-fit** (1-5) → return the **top 5**. Spread the 5 across idea engines and, where relevant, funnel slots. Truth and shootability are **gates** (fail = cut); hook strength and novelty are the **ranking** on top.

---

## Output — the concept card

For each of the top 5:

```
### [Title] | Engine: [1 of 7] | Visual mode (candidate): [..] | Slot: [listing/farm/market-ed/ad · TOFU/MOFU/BOFU]
- Best format: [talking-head video / carousel / static graphic / multi — NOT everything is a video; "opportunity math" concepts often land better as a carousel or static]
- Truth: [the one true tension, one sentence]
- The concept: [the collision, 1-2 sentences]
- 3-beat escalation: [beat 1] → [beat 2] → [beat 3 → lands on the RE point]
- Hook(s): "[<20 words]"  (Cur _/Spec _/PI _/Emo _/Stakes _ → avg _)
- Opening visual: [the 0:00-0:03 image; contrast or congruent]
- Avatar/plate: [which existing avatar; what plate the videographer grabs; composite plausible?]
- Shootable gate: [pass + any flag]
- Risk: [too cheesy / weird / unshootable / salesy — or none]
- Why it works: [one line]
```

**Judge in context, never from a logline (learned 2026-06-27).** A concept can't be evaluated from one decontextualized sentence — a bare line "does nothing" until you can see the scene. Each card must carry enough of the *treatment* (the opening visual, the VO register, how the beat actually plays) that Graeham reacts to a mini-scene, not a sentence. If a concept "only works with the right text and cinematography," then put that text and that cinematography on the card — don't make him imagine it. **Build the actual visual beats to a concrete, shootable level** — name what's on screen, what's absurd, what the avatar does and says, and the button. The bar is Graeham's own 2026-06-27 "X-ray" expansion (a giant X-ray machine wheeled to the house, the zap, the funny interior reveals). If Graeham has to invent the beats himself, the card failed.

These go to Graeham for **Greenlight 1** (concept + avatar availability). The pick(s) hand off to `cinematic-video-engine`. Use **creative beat IDs** in any shot reference (`BEAT_03_KITCHEN_REVEAL`) — never final clip IDs; `listing-launch-engine` / the production-packager owns those.

---

## Scope, compliance & selection (Fugu-validated boundaries)
- **Video-only lead hooks.** concept-forge owns the **video** lead hook. Blog / ad / caption headlines stay with `content-creation-engine`'s script-writer. Don't generate non-video copy hooks here.
- **Ingest the brief + seeds; never invent off-listing.** When called by `listing-launch-engine`, ingest its brief (lane + buyer-need + data-angle + listing facts + copy-surface rules). Cite the **Hook Database** seed corpus (`Documents\Obsidian\Content Listing Engine\Hook Database\`, incl. the *cinematic seed treatments*) and any `content-creation-engine` demand signal, so concepts stay on-listing and on-demand.
- **Compliance gate (mandatory).** The old static Hook DB was implicitly pre-vetted; generated hooks are not. The caller runs Fair Housing + listing-claims + copy-surface rules on the returned hooks BEFORE anything is built. Flag, don't ship, anything borderline.
- **Selection authority.** concept-forge returns a *set*; the human (Graeham) picks (Greenlight 1). Rank the set by combining the **hook/novelty score (here)** with the **demand/intent score** (`content-calendar` / `content-creation-engine`) when available — concept-forge does NOT replace demand validation.
- **Determinism / fallback.** Generation isn't instant or repeatable like the old static pick. Cache the returned packages per listing/run so a re-run is stable and a compliance reviewer sees the same set.

## Cinematic gate — graceful degradation while CVE is unbuilt (production, Fugu-validated 2026-06-27)

`cinematic-video-engine` (CVE) renders CINEMATIC concepts; until it exists, NEVER hand editors a half-built cinematic packet. The gate:
- **Tag every concept `concept_type: STANDARD | CINEMATIC`.** STANDARD = realizable with the current listing-launch-engine pipeline (talking-head + B-roll + avatar overlay + standard shot decomposition). CINEMATIC = needs CVE's AV matrix / continuity ledger. **In presentation, label each concept by its Title + the plain word (Standard) or (Cinematic) — NEVER codes like S1/C1 (Graeham wants to read the type, not decode it).**
- **Capability flag `CVE_AVAILABLE = false` for now** — flip it when CVE ships.
- **Only a STANDARD concept can be the ACTIVE / lead concept** the editor packet is built from. The packet is ALWAYS populated from a STANDARD concept while CVE is off.
- **Guarantee ≥1 STANDARD per run.** If the top-scored hook rides a CINEMATIC concept, re-attach that hook to the best STANDARD treatment rather than dropping it. If a run somehow returns all-cinematic, fall back to a default standard treatment (talking-head + B-roll on the lead truth).
- **Park CINEMATIC concepts in a "🎬 Future / Needs CVE" section** — title + hook + rationale ONLY. Never emit a partial AV matrix or continuity ledger. Fail-closed, informational.
- **Compliance gate covers BOTH the hooks AND the final word-for-word scripts** (Fair Housing + listing-claims + copy-surface) — verified against REAL listing data, not toy data.
- **Human checkpoint:** Graeham approves concept + hook + final script BEFORE the crew shoots or anything publishes (he's on-site anyway).

## Guardrails
- **Truth & shootability first**, cleverness second. A brilliant unshootable concept is a failure.
- **Fair Housing**: never about who lives somewhere; property/process/price/market only. Comparing prices/markets is fine; comparing people is not.
- **Brand**: clean with a little bite, never at a client's expense. DRE/brokerage from `shared-references/identity.json`.
- **For an ACTIVE listing you're selling, the humor NEVER targets the property itself.** "This house is a mess / the good news is the bad news" jokes are funny but they undercut the sale. Aim the wit at the market, Zillow, the price gap, the process, or the agent — never the home you're trying to move. (Graeham 2026-06-27: S2 was funny-but-wrong for exactly this.)
- **Never narrate or explain the bit.** The VO stays 100% on property specs; the VISUAL carries the absurdity and the avatar never acknowledges it. A line like "watch the house fix itself while I stay calm" *explains* the joke and kills it. Deadpan = he reads specs, dead serious, while chaos happens behind him.
- **Avatar-real**: only looks that exist; flag wishlist looks separately.
- **Fugu Ultra** is the standing QA gate on the final 5 (per `comedy-craft` convention).

## Pipeline position
Called by `content-creation-engine` (generic/geographic) or `listing-launch-engine` (listing) → concept-forge returns 5 cards → Graeham greenlights → `cinematic-video-engine` executes → `heygen-video` + `heygen-elevenlabs-renderer` render → `humanizer` polishes captions. Loads `comedy-craft` (voice) and `marketing-psychology` (CTA).
