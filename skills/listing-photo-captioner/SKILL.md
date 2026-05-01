---
name: listing-photo-captioner
description: "Writes MLS-ready photo descriptions from uploaded property images using image recognition. Identifies the room or space shown, names visible features (materials, finishes, fixtures, layout), and produces a numbered, paste-ready caption list for the MLS photo upload workflow. Use this skill ANY time the user uploads listing photos and asks for: photo captions, MLS photo descriptions, photo descriptions for a listing, captions for these photos, write captions for my listing photos, label these property images, MLS-ready photo descriptions. Trigger when the user uploads property images and mentions captions, descriptions, MLS, or labeling. Pairs naturally with listing-remarks-writer (different jobs — captioner does per-photo blurbs, remarks-writer does the main description) but runs independently. Localized for Graeham's Bay Area markets when location-relevant features appear in outdoor shots."
---

# Listing Photo Captioner

Write MLS-ready photo descriptions from uploaded property images. Identifies each room or space, names visible features only, and produces a polished, paste-ready caption list. Stays inside Fair Housing / RESPA / truth-in-advertising guardrails by design.

This skill is the photo equivalent of `listing-remarks-writer` — same compliance posture, same Bay Area context, but per-photo blurbs instead of a full property description. They run independently. The agent can use one without the other.

---

## Before You Start — Read These

1. **`../shared-references/identity.json`** — Graeham's brand identity. NEVER hardcode contact details, DRE, or brokerage from memory.
2. **`../listing-remarks-writer/SKILL.md`** (optional) — if running on the same listing as the remarks writer, read this for shared voice and feature framing. Captions should feel consistent with the main description.

---

## Fair Housing + RESPA Guardrails (Non-Negotiable)

NEVER write captions that:
- Describe people in the photos. If a person is visible (staging photos, dog, neighbor walking by), describe the space only. Most MLS rules also require avoiding identifiable people anyway.
- Reference race, religion, national origin, family status, disability, or sex
- Use coded language: "family-friendly," "great for entertaining" (borderline — only if the space is genuinely a host/entertainment layout, never as a demographic proxy), "kid-friendly," "perfect for empty nesters"
- **Mention school quality, ratings, or rankings.** If a school is visible from a window or shows up in an exterior shot, factually name it at most ("View toward Costaño Elementary"). Never assess quality.
- Promote vendors (no "professionally landscaped by [company]," no lender/inspector references)
- Imply preference for or steering toward specific buyers

When describing exteriors or neighborhood views: stick to property types, transit visibility, parks/trails, architectural styles. Don't characterize the surrounding area.

---

## Truth-in-Advertising Rules (Non-Negotiable)

**Only describe what is clearly visible in the photo.** This is the most important rule.

- If you can see quartz on the counters, say quartz. If you're guessing at granite vs quartz vs solid surface, say "stone countertops" or just "countertops."
- If you see hardwood, say hardwood. If you can't tell hardwood from luxury vinyl plank in the photo, say "wood-tone flooring."
- Don't name appliance brands unless the brand is legible in the image.
- Don't claim a feature exists outside the frame ("kitchen leads to a butler's pantry" is only OK if the pantry is partially visible or you've been told).
- Don't estimate room dimensions from photos.
- Don't claim a window has a "view of [X]" unless [X] is visible in the photo.

If a photo is unclear, ambiguous, or low-quality, write a generic caption and note the uncertainty: "Living area with neutral flooring and large windows. Confirm finishes with listing agent."

**ADU / accessory structures:** If a structure is visible that *might* be an ADU, do NOT call it an ADU. Call it what's visibly true: "detached structure," "studio outbuilding," "garage with potential conversion area." Whether it qualifies as a permitted ADU is a zoning + permit question, not a caption call. (Same rule as listing-remarks-writer.)

---

## Caption Style

- **Lead with the room or space name.** ("Kitchen — ...") This is the most searchable token; AI search engines and MLS users both scan room names first.
- **Follow with 1–2 specific features visible in the image.** Name materials, finishes, fixtures, layout characteristics.
- **Use noun-dense, descriptive language** consistent with the listing-remarks-writer "nouns over pronouns" approach.
- **Keep each caption to 1–2 sentences.** MLS photo captions are meant to be brief and scannable.
- **Sentence case, not Title Case.**
- **No emojis. No hashtags. No promotional language.** No "stunning," "gorgeous," "amazing," "must-see."

**Good:** "Kitchen with white quartz countertops, stainless steel appliances, and a subway tile backsplash. Center island seats four."

**Weak:** "Beautiful kitchen with amazing finishes!"

---

## What To Describe vs. What To Skip

**Describe (when clearly visible):**
- Room type and layout
- Materials: hardwood, tile, quartz, granite, marble, carpet — only if you can tell
- Fixtures: lighting type, faucet style, built-in shelving
- Architectural details: vaulted ceilings, crown molding, exposed beams, wainscoting, coffered ceilings, built-ins
- Outdoor features: fencing type, landscaping (without quality judgment), patio material, view (only if view subject is in frame)
- Appliances if visible and notable: gas range, double oven, wine fridge, built-in microwave
- Smart home: visible thermostats (Nest), doorbells (Ring), EV chargers — only if currently installed and visible

**Skip:**
- Personal belongings, family photos, identifiable people, pets
- Anything you're guessing at — only describe what is clearly visible
- Decorative staging items unless they highlight the space's function (a staged dining table is fine; "elegant staged decor" is not)
- Quality judgments — don't say "high-end" unless the materials clearly indicate it (and even then, prefer naming the material specifically)
- Subjective light descriptors like "warm and inviting" — describe the actual light source instead ("south-facing windows," "skylight," "recessed lighting")

---

## Bay Area Context (Where Photos Show Outdoor / Location)

If outdoor or exterior photos show identifiable Bay Area landmarks, you may name them factually:
- Bay Trail or Cooley Landing visible in the distance — "view toward the Bay Trail"
- Stanford foothills visible — "western view toward the foothills"
- A Caltrain platform visible from a window — "Caltrain platform visible from the window"
- A specific park (factual name, no quality assessment) — "across from MLK Park"

Do NOT speculate about views that aren't in frame. Do NOT name a neighborhood by quality ("desirable Crescent Park view"). Do NOT assess school quality even if a school is visible.

---

## Process

1. Accept up to 10 photos at a time. If the user has more, process in batches.
2. For each photo, identify:
   - What room or space is shown
   - Key visible features
   - Anything that stands out as a selling point (only if visible)
3. Write one caption per photo — concise, descriptive, searchable.
4. Present all captions in the order the photos were uploaded, numbered to match.
5. After completing a batch, ask: "Do you have more photos for this listing, or is this the full set?"

---

## Intake (Ask If Not Provided)

Before captioning, confirm:
1. **Property address** (helps with context — Bay Area landmarks, MLS framing)
2. **Property condition tier** (fixer / mid / move-in / renovated / new construction) — affects whether captions emphasize finishes or potential
3. **Specific features the agent wants called out** that might not be obvious from photos (recent upgrades, hidden features, specific brands the agent has confirmed)
4. **MLS rules** — most MLS systems cap photo captions at 100–250 characters. MLSListings allows up to 250. If the user is using a different MLS, confirm the limit.

If only photos are provided with no context, write generic factual captions and ask the user to confirm any feature claims that aren't obvious from the image.

---

## Output Format

```
1. Kitchen — White quartz countertops, stainless steel gas range, tiled backsplash, and a center island with seating for four.
2. Living room — Hardwood flooring throughout, large south-facing windows, and a stone-faced fireplace.
3. Primary suite — Vaulted ceiling, walk-in closet, and direct access to the primary bath.
4. Primary bath — Tiled walk-in shower, double vanity with quartz countertop, and a private water closet.
5. Backyard — Covered patio, mature fruit trees, and turf landscaping. Two-car attached garage visible at left.
...
```

Deliver as a clean numbered list the user can paste directly into MLS, one caption per photo position. No headers, no commentary inline.

After the captions, optionally provide:
- **Compliance check** — confirm no school quality language, no people described, no unverified feature claims, no demographic proxies
- **Photos with low confidence** — list any photo numbers where the caption is generic because the image was unclear, with a note on what the agent should verify

---

## Used By

- **Standalone** — agent uploads photos for a new listing and needs captions for the MLS photo upload workflow.
- **Pairs with `listing-remarks-writer`** — when both run on the same listing, captions inform the walkthrough sequence in the main description (kitchen features named in captions appear consistently in the description's kitchen section). Run order doesn't matter — they're independent.
- **`content-creation-engine`** — when a listing-spotlight content package includes photo carousel posts, the engine pulls these captions as the source-of-truth photo blurbs for the carousel slides.
