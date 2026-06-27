---
name: content-multiplier
description: The content-multiplication / atomization layer — turns ONE listing's greenlit concepts into the full cross-platform asset matrix (every video, Short, Reel, carousel, static, GBP post, X post, and paid ad variant), reverse-derives the single shot list that captures it all in one trip, and wires in lead capture + cross-format A/B tests. Use whenever Graeham says: multiply this listing, all the content for this listing, every post and ad for this property, the content matrix, atomize this, how many pieces can we make, turn this listing into content, the full launch content, repurpose this concept across platforms, or gives a listing + greenlit concepts and wants the whole content factory output. It sits BETWEEN concept-forge (which makes the concepts) and listing-launch-engine (which owns launch phases, the calendar, crew packets, and approval). It is a CULLING engine, not a volume machine: generate many candidate assets, score, kill the weak, keep the native-fit ones. content-creation-engine writes the actual copy/scripts for each row; meta-ads/google deploy paid; switchy-engine mints tracked links; GHL owns the comment keywords. Fugu Ultra is the standing QA gate.
---

# Content Multiplier — the atomization layer

The layer that was missing. `concept-forge` makes the *ideas*; this turns each greenlit concept into the **asset matrix** — every native platform/format rendition worth making, organic and paid — then reverse-derives the one shot list that feeds them all.

**The first principle (Fugu's, non-negotiable): multiplication ≠ volume.** This is a *scored options market*: it generates many candidate assets, kills the weak ones, and hands production a complete, deduped shot list. The promise is NOT "one listing → 300 posts." It's: **one listing + one shoot → complete capture coverage → native assets → phase-aware distribution → organic + paid → cross-format testing → attributed leads → learning for the next listing.**

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

**Key AssetMatrixRow fields:** launch_phase · objective (awareness/engagement/education/lead_capture/retargeting/open_house/showing/seller_proof) · audience_segment · native_format_family · creative_job (show_spatial_flow / prove_feature / handle_objection / create_urgency / drive_open_house / capture_floorplan_lead / build_trust / retarget) · status (candidate→approved→needs_shoot→ready_to_render→published→killed) · rank_score · why_this_format · creative_spec (hook, beats, avatar mode+screen position+negative space, on-screen text, caption brief, CTA) · shoot_spec (required shot/plate atoms, orientation, movement, fallback_if_missing) · crop_spec (master ratio + allowed ratios + must-keep-visible + UI-avoidance zones) · lead_capture · experiment · compliance.

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

Each ShotAtom carries: room/feature, **assets served**, required orientation, movement, min duration, safe crop targets, avatar negative-space zone, must-keep-visible, priority, and **fallback if missed** (still / floorplan / alt room / rewrite / drop). After the shoot, real clips map back; a missing shot's dependents are rewritten or killed, **never faked.**

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
concept-forge → makes concepts/hooks/scores
content-multiplier (this skill) → chooses which concepts earn which formats, builds the AssetMatrixRows,
   renditions, distribution variants, ShotAtoms, experiments, lead-capture offers
listing-launch-engine → owns launch phases, calendar, crew packets, approval; embeds the matrix as
   LaunchContentPlan.asset_matrix (LLE's old "derivative render list" becomes a VIEW of the matrix, not the source)
content-creation-engine → consumes the rows; writes scripts, captions, blogs, ad copy (fed mode)
meta-ads / google ads → deploy paid DistributionVariants   ·   switchy-engine → tracked link per variant
GHL → workflows, comment keywords, contact routing
```

---

## Guardrails — the hard gates (this is a culling engine)
- **Multiplication ≠ volume.** If the engine ever celebrates raw count, it's broken. Generate many, approve fewer, kill freely.
- Hard controls: minimum native-fit score · minimum visual-proof score · **max assets per phase** · **max direct CTAs per week** · max repeated room/plate usage · visual-variance rule · audience-fatigue penalty · paid auto-pause · **listing-status suppression** (kill/park everything if the listing goes pending/sold) · **human approval for hero assets**.
- Compliance flows from the row: Fair Housing + MLS rules + housing ad category + price-off-spoken (copy-surface) + no-financing-terms — checked per row before render, on real listing data.
- **Fugu Ultra** QA on the matrix before a listing goes to the crew (per `comedy-craft`/`concept-forge` convention).
