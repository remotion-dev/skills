---
name: content-multiplier
description: The content-multiplication / atomization layer — turns ONE listing's greenlit concepts into the full cross-platform asset matrix (every video, Short, Reel, carousel, static, GBP post, X post, and paid ad variant), reverse-derives the single shot list that captures it all in one trip, and wires in lead capture + cross-format A/B tests. Use whenever Graeham says: multiply this listing, all the content for this listing, every post and ad for this property, the content matrix, atomize this, how many pieces can we make, turn this listing into content, the full launch content, repurpose this concept across platforms, or gives a listing + greenlit concepts and wants the whole content factory output. It sits BETWEEN concept-forge (which makes the concepts) and listing-launch-engine (which owns launch phases, the calendar, crew packets, and approval). It is a CULLING engine, not a volume machine: generate many candidate assets, score, kill the weak, keep the native-fit ones. content-creation-engine writes the actual copy/scripts for each row; meta-ads/google deploy paid; switchy-engine mints tracked links; GHL owns the comment keywords. Fugu Ultra is the standing QA gate.
---

# Content Multiplier — the atomization layer

The layer that was missing. `concept-forge` (via the **showrunner gauntlet**) presents 3–5 **built survivor mini-treatments** — each with a filled Formal Comedy Map and a `concept_type` (STANDARD / CINEMATIC). This layer consumes ONLY those survivors (never raw loglines or loose ideas), multiplies **only STANDARD** ones into the **asset matrix** (CINEMATIC stays parked until `cinematic-video-engine` exists), and reverse-derives the one shot list that feeds them all. It carries **beat-level *intent*** — never finished copy, jokes, camera specs, clip IDs, links, keywords, SSML, or paid deployments (those belong to the owners in the boundaries below).

**The first principle (Fugu's, non-negotiable): multiplication ≠ volume.** This is a *scored options market*: it generates many candidate assets, kills the weak ones, and hands production a complete, deduped shot list. The promise is NOT "one listing → 300 posts." It's: **one listing + one shoot → complete capture coverage → native assets → phase-aware distribution → organic + paid → cross-format testing → attributed leads → learning for the next listing.**

---

## Source-of-truth boundaries (what this layer does NOT own)

The matrix rows are **beat-level intent**, not finished assets. Cite these owners; never restate their content:
- **Concept intake** → `concept-forge/references/showrunner-gauntlet.md` — consume built STANDARD survivors only; reject loglines/loose ideas; park CINEMATIC.
- **Jokes / copy / scoring** → `comedy-craft/references/joke-architecture.md`, written by `content-creation-engine` in **fed mode** (Greg Dean for lines, UCB game for multi-beat carousels/reels; the hard 0–5 joke scoring lives there). This layer carries *briefs/intent* — it never writes or scores hooks, captions, lines, CTAs, or SSML.
- **Camera / capture / ingest / avatar-match** → `listing-launch-engine/references/capture-standard.md` + its avatar-match spec card. Never restate frame rate, shutter, profile, exposure, crop, negative-space, or clip IDs.
- **Clip IDs / call sheets / distribution** → `listing-launch-engine` / packager. **Links** → `switchy-engine`. **Keywords** → GHL. **Paid deployment** → `meta-ads` / Google.

---

## The object model (plain version)

```
Concept (from concept-forge)
  → AssetMatrixRow        ← ONE native creative SKU (the main product of this layer)
      → PlatformRendition ← a native version per platform (IG Reel, TikTok, Short, GBP…)
          → DistributionVariant ← organic post OR paid ad (organic & paid are NOT separate content)
      → ShotAtom / PlateAtom ← the footage this asset depends on
      → LeadCaptureOffer  ← the GHL comment-keyword offer
      → ExperimentGroup   ← the A/B test it belongs to
```

**The one rule that prevents bloat:** a minor platform tweak (crop, caption length, first-frame) is a *PlatformRendition* of the same row. A material change in story, framing, shoot requirement, or persuasion job is a *new AssetMatrixRow*. If it's the same idea cropped differently → rendition. If it's a different argument → new row.

**Key AssetMatrixRow fields (all INTENT, not finished content):** launch_phase · objective (awareness/engagement/education/lead_capture/retargeting/open_house/showing/seller_proof) · audience_segment · native_format_family · creative_job (show_spatial_flow / prove_feature / handle_objection / create_urgency / drive_open_house / capture_floorplan_lead / build_trust / retarget) · status (candidate→approved→needs_shoot→ready_to_render→published→killed) · rank_score · why_this_format · **creative_intent** (hook_intent, beat_intents that *reference* the survivor's Comedy Map beats [never rewrite them], avatar role intent [position/negative-space live in the avatar-match card, not here], on-screen-text intent, caption brief, cta_intent — all *briefs*, zero final copy) · **capture_intent** (the beat-level coverage needed; all camera specs inherited from `capture-standard.md`) · **surface_intent** (which formats/platforms; renditions + clip IDs owned by the packager) · **conversion_intent** (the desired action; final CTA + link + keyword owned by CCE / Switchy / GHL) · experiment_hypothesis · compliance. **The actual copy, jokes, and SSML for every row are written by `content-creation-engine` in fed mode loading `comedy-craft` + `joke-architecture.md` — this layer never writes or scores them.**

---

## Anti-garbage: a concept earns a format only if the format improves the persuasion

Do NOT do `Concept × Platform × Format × Organic/Paid` (that's landfill). Do: `Concept → persuasion job → format families that ENHANCE that job → native renditions → distribution variants.`

**Format-fit rules:**

| Concept type | Strong formats | Avoid |
|---|---|---|
| Spatial flow / walkthrough / reveal | Vertical video, Short, Reel, TikTok, long tour | Static-only (unless the image is exceptional) |
| Objection / disclosure / education | Carousel, YouTube explainer, retargeting ad | Trendy short-form with no depth |
| Single strong claim | Static image-with-text, GBP post, Meta ad | 8-slide carousel |
| Lifestyle / neighborhood | Vertical video, carousel, GBP, YouTube segment | Hard lead ad too early |
| Open house / price / urgency | Static, story, GBP, Meta + Google ad | Long narrative video |
| Social proof / sold | Static, short video, Facebook, GBP, X | Excessive repurposed clips |

**Scoring gate — every candidate row is scored before it exists; below threshold = killed:**
```
asset_value = concept_score × phase_relevance × platform_format_fit × visual_proof_available
              × lead_or_brand_value × paid_amplification_potential
              − production_cost − redundancy_penalty − audience_fatigue_penalty − compliance_risk
```

---

## One shoot captures all — reverse-derive the shot list

The shot list is **not invented; it's reverse-derived from the approved AssetMatrixRows:**
```
approved rows → their required ShotAtoms/PlateAtoms → dedupe by (room, movement, orientation,
crop targets, avatar negative-space) → rank by value of assets served → ONE crew packet → shoot once
→ ingest clips/photos → unlock/rewrite/downgrade/kill each dependent asset
```

**Contrarian capture rule (don't "shoot horizontal and crop later" — that makes mediocre verticals).** Capture in three modes:
1. **Native vertical hero shots** (Reels/TikTok/Shorts/stories/vertical ads).
2. **Horizontal master shots** (YouTube long, website, thumbnails, 16:9).
3. **Clean avatar plates** — locked/slow shots with intentional negative space for Graeham's HeyGen overlay + captions/diagrams/text.

Each capture-intent carries: room/feature, **assets served**, coverage purpose, the visual evidence needed, priority, and **fallback if missed** (still / floorplan / alt room / rewrite / drop). **All actual camera specs — frame rate, shutter, profile, white balance, exposure, resolution, stabilization, orientation, crop targets, avatar negative-space, clip IDs — are inherited from `listing-launch-engine/references/capture-standard.md` and its avatar-match spec card; this layer does not restate them.** The three modes above are coverage-intent labels, not camera specs. After the shoot, real clips map back; a missing shot's dependents are rewritten or killed, **never faked.**

---

## Lead capture without being spammy

CTA intensity: `none` (pure content) / `soft` ("DM me") / `direct` ("Comment FLOORPLAN and I'll send it"). Mix by phase: awareness/lifestyle = none/soft; layout/detail = soft/direct; disclosure/objection = direct if useful; open house/price/retargeting = direct; sold/social proof = soft.

Rules: **one offer per concept** (never 5 CTAs on a post); **one public keyword per offer/listing** (`FLOORPLAN` `PRICE` `OPEN` `TOUR` `DISCLOSURES` `NEIGHBORHOOD`); **direct CTAs on only ~20–35% of visible content** (or the brand reads desperate); **use GHL state** (if a contact already claimed `FLOORPLAN`, route them down-funnel instead of re-sending). The public sees `FLOORPLAN`; GHL internally receives listing_id, concept_id, asset_row_id, distribution_id, platform, phase, offer_id, experiment_id, source_keyword.

---

## Cross-format A/B (same concept as video AND static)

Lives in an `ExperimentGroup` tied to the `concept_id`. **Use the SAME public keyword** when the offer is the same — never `FLOORPLAN_A` / `FLOORPLAN_B`; show `FLOORPLAN` and track the variant internally via platform_post_id / platform_ad_id / Switchy link / UTM content / GHL source tag. Hold invariant: audience, geo, offer, phase, budget, publish window. Paid = real split test; organic = directional unless the sample is large. Decision rule example: "if CPL differs by 30% past the sample threshold, move budget to the winner, pause the loser."

---

## Where it lives (wiring)

```
concept-forge → presents 3–5 built STANDARD gauntlet survivors (mini-treatment + Comedy Map + concept_type)
content-multiplier (this skill) → consumes STANDARD survivors; builds the asset matrix of beat-level INTENT
   rows (creative / capture / surface / conversion intent + experiment hypotheses); parks CINEMATIC survivors
content-creation-engine (FED MODE) → writes the final copy / jokes / SSML for each row, loading comedy-craft +
   joke-architecture.md (Greg Dean lines, UCB game for carousels/reels; the hard 0–5 joke scoring lives here)
listing-launch-engine / packager → owns launch phases, calendar, crew packets, approval, the real shot list,
   clip IDs, capture execution (per capture-standard.md), packaging + distribution; embeds the matrix as
   LaunchContentPlan.asset_matrix (its old "derivative render list" becomes a VIEW of the matrix)
switchy-engine → mints tracked links   ·   GHL → comment keywords + routing   ·   meta-ads / google → paid deployment
```

---

## Guardrails — the hard gates (this is a culling engine)
- **Multiplication ≠ volume.** If the engine ever celebrates raw count, it's broken. Generate many, approve fewer, kill freely.
- Hard controls: minimum native-fit score · minimum visual-proof score · **max assets per phase** · **max direct CTAs per week** · max repeated room/plate usage · visual-variance rule · audience-fatigue penalty · paid auto-pause · **listing-status suppression** (kill/park everything if the listing goes pending/sold) · **human approval for hero assets**.
- Compliance flows from the row: Fair Housing + MLS rules + housing ad category + price-off-spoken (copy-surface) + no-financing-terms — checked per row before render, on real listing data.
- **Fugu Ultra** QA on the matrix before a listing goes to the crew (per `comedy-craft`/`concept-forge` convention).
