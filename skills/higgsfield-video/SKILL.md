---
name: higgsfield-video
description: Generate AI b-roll video clips on higgsfield.ai by driving Claude in Chrome to execute a two-stage pipeline — Nano Banana Pro OR GPT Image 2 generates a start frame, then Seedance 2.0 or Kling 3.0 animates it into an image-to-video clip. Use ANY time Graeham mentions higgsfield, b-roll, AI b-roll, "make me b-roll", cinematic b-roll, drone shot, aerial shot, cutaway, transition clip, Nano Banana, GPT Image 2, gpt-image-2, ChatGPT Images 2, listing card overlay, "For Sale" sign, address number on image, signage shot, text-in-image, Seedance, Kling, image-to-video, or any request to produce a short AI video clip for inserts, transitions, or visual establishment in his real estate video content. Also trigger on follow-ups like "continue the higgsfield skill", "do another b-roll", "try a different motion", "regenerate with changes", or when iterating on a previously generated clip.
---

# Higgsfield B-Roll Video — Graeham Watts

Two-stage b-roll pipeline on higgsfield.ai, driven via Claude in Chrome browser automation.
**Nano Banana Pro** (default, photoreal) **or GPT Image 2** (when readable text inside the frame matters) generates a 4K start frame → **Seedance 2.0** (or Kling 3.0) animates it into a 5–15 second clip.

Built across multiple sessions with Graeham. Every rule here comes from a verified working outcome or a verified failure mode we encountered live. **GPT Image 2 path added 2026-05-03 — provisional pending first-session verification of URL, credit cost, and prompt response patterns.**

---

## Why this is browser-driven, not API-driven

Higgsfield's API host (`platform.higgsfield.ai`) is not on the Claude.ai sandbox allow-list, and the N8N MCP path is also blocked at the allow-list layer. The only viable path to generate b-roll from a Claude chat session is to **drive the Higgsfield web UI directly via Claude in Chrome**. Graeham stays logged into Higgsfield in Chrome; this skill does the clicking.

---

## Prerequisites before running

1. **Claude in Chrome is connected.** If not, call `switch_browser` and ask Graeham to click Connect in the right Chrome window.
2. **Graeham is signed into higgsfield.ai in that Chrome.** Verify by navigating to `https://higgsfield.ai/image/nano-banana-pro` and confirming his green avatar is visible top-right.
3. **Verify auth state early.** If nav to `/image/nano-banana-pro` redirects to `/ai-image` with **Login / Sign-up buttons visible top-right**, Graeham has been logged out — session cookies expired mid-workflow. Claude cannot handle the auth flow. Ask Graeham to click Login in that specific Chrome window, complete his normal auth (Google SSO typically), and confirm avatar reappears before continuing. Retrying the navigate will not fix it — only re-authentication does.
4. **Credit balance is sufficient.** Minimum ~140 credits for one complete image + Seedance 15s cycle, ~130 credits for image + Seedance 10s cycle, ~36 credits for image + Kling cycle. Check the bottom-right "Credits are running low" banner or the user profile dropdown (shows "XX% credits left").

---

## MANDATORY questions before driving the browser

Use `ask_user_input_v0` with tappable options. Ask in a single turn, not sequentially:

1. **Orientation** — Landscape (16:9) or Portrait (9:16)?
2. **Duration** — 5s, 10s, or 15s?
3. **Video model** — Seedance 2.0 or Kling 3.0?
4. **The subject / scene description** for the start frame (if not already given)
5. **The motion / camera move** for the video (if not already given)

Image model is selected by the **Image Model Routing Rule below** — Claude decides based on whether readable text inside the frame is required for the brief. Do not ask Graeham which image model unless the routing rule is genuinely ambiguous.

---

## 🔀 Image Model Routing Rule (Nano Banana Pro vs GPT Image 2)

Higgsfield hosts both models. They have different strengths — pick the right one for the shot before navigating to Stage 1.

### Decision rule

**Use GPT Image 2 when ANY of these are true:**
- Brief specifies readable text inside the frame — "FOR SALE" signs, address numbers, street signs, listing card mockups, "JUST SOLD" overlays, neighborhood watermarks, building signage that needs to spell correctly
- Brief specifies a UI mockup, screenshot, infographic, or document with legible copy
- Brief involves non-Latin script (rare for Graeham's content but flagging — Chinese, Japanese, etc.)
- Brief requires a multi-panel composition (comic strip layout, before/after split, side-by-side comparison) — GPT Image 2's thinking mode handles multi-panel coherence better

**Use Nano Banana Pro (default) when ANY of these are true:**
- Pure photoreal establishing shot — Peninsula suburbia, aerial drone view, neighborhood overview, landscape, interior, exterior architecture without prominent signage
- Faster turnaround needed — Nano Banana Pro is well-understood, fewer first-pass surprises
- **Transparent background output is required** (PNG with alpha channel) — GPT Image 2 does not support transparent output yet; this is a hard limitation
- The shot has been generated before with Nano Banana Pro and you're iterating on a known-working composition

### Why this matters

Nano Banana Pro produces stronger pure-photoreal frames with fewer "AI render" tells when the realism rescue protocol is applied. GPT Image 2 produces dramatically better text rendering (95%+ accuracy including curved surfaces and small sizes) but its photoreal output, while strong, is a newer entrant on Higgsfield with less verified prompt-response data in this skill.

For most of Graeham's b-roll — Bay-visible aerials, stucco-ranch establishing shots, golden-hour Peninsula neighborhoods — Nano Banana Pro stays primary. GPT Image 2 fills the specific gap where text inside the frame must be legible (which previously required CapCut overlay work in post).

### Hard limitation to flag to Graeham

**GPT Image 2 does NOT support transparent backgrounds.** If a shot needs to be composited later as a layer over other footage with a transparent PNG, route to Nano Banana Pro instead and accept that text rendering will be weaker — or use GPT Image 2 with a solid background and key it out in CapCut. This is a real production trade-off Claude should surface before generating, not after.

---

## Stage 1: Generate start frame

**Per the Image Model Routing Rule above, navigate to either Nano Banana Pro or GPT Image 2.**

### Path 1A: Nano Banana Pro (default for photoreal shots)

#### Navigate directly

`https://higgsfield.ai/image/nano-banana-pro` **(direct URL required)**

The top-nav "Image" button routes to Nano Banana 2, which is a different (weaker for this use case) model. Always go to the URL directly.

### Path 1B: GPT Image 2 (when readable text inside the frame matters)

#### Navigate (provisional URL discovery)

The exact in-app generator URL has not yet been verified in a Graeham session. On first use, try in this order:

1. **Try `https://higgsfield.ai/image/gpt-image-2`** (matches the Nano Banana Pro URL pattern)
2. **If 404, navigate to `https://higgsfield.ai/image/nano-banana-pro` and look for an in-page model dropdown/picker** to switch models
3. **If neither works, navigate to `https://higgsfield.ai/gpt-2`** (the marketing landing page) and click the "Try Now" / "Open Editor" / "Start Generating" button to be routed to the live editor

**On first successful navigation, document the working URL and replace this block in the skill with the verified path** — the goal is to lock this in the same way Nano Banana Pro's URL is locked.

#### Verify model identity before generating

Before typing the prompt, confirm via the page title, model badge, or model picker that GPT Image 2 (or "gpt-image-2") is the active model. The Higgsfield UI surfaces several image models in similar layouts; an accidental render on the wrong model wastes credits and creates routing confusion.

#### Thinking mode (Plus/Pro tier — enable when text accuracy is critical)

GPT Image 2 has a "thinking" toggle on Higgsfield. When enabled, the model reasons through composition, text layout, and constraints before rendering — significantly higher text accuracy, slower generation, higher credit cost. **Default to thinking mode ON for any shot where the routing rule selected GPT Image 2** — the whole reason we're on this model is text fidelity.

#### Reference images (up to 16 supported)

GPT Image 2 accepts up to 16 reference images for edit/composition calls. For Graeham's use case this almost never matters — most b-roll uses 0 or 1 reference. Drag-and-drop is still the only working attach path from Claude-in-Chrome (`file_upload` tool blocked — same reason as Nano Banana Pro path).

---

### Common steps for both paths (Nano Banana Pro AND GPT Image 2)

#### Clear prior state

Both the prompt AND attached reference image thumbnails persist across sessions. Before typing the new prompt:

- Hover any attached reference thumbnail. An X appears in the top-right corner. Click the X.
- Click the prompt textbox. `ctrl+a` → `Delete`.

### Optional: drag-and-drop reference image (for matching a specific composition)

When Graeham wants the output to match a specific image he already has — a listing photo, a neighborhood reference he shot himself, a competitor's framing — use drag-and-drop to attach it as a reference:

1. **Graeham saves the file to** `C:\Users\Admin\Downloads\` (or tells you where it is)
2. **He drags the file from File Explorer onto the "Describe the scene you imagine" prompt area.** Drop anywhere in that dark bar; a thumbnail appears next to the "+" icon confirming attachment.
3. **Claude then types the prompt with explicit match language:** e.g. "match the composition, lighting, and architectural style of the reference image exactly" followed by specific element descriptions.

**Why drag-and-drop and not the automation's file_upload tool:** Chrome automation's `file_upload` fails with `{"code":-32000,"message":"Not allowed"}` against Higgsfield's file input — sandbox security blocks the sandbox→local-disk path. Drag-and-drop is the ONLY working attach path from Claude-in-Chrome. Verified in session.

**Effect on variants:** With a reference image attached, the 4 generated variants will converge to 90%+ identical compositions — the reference anchors the model tightly. Pick the hero based on micro-lighting differences (warm vs cool, softer vs sharper shadows, sky haze variation) rather than composition, which will be nearly identical across all four.

### Type the image prompt

This is where realism lives. **See the "Realism Rescue Protocol" section below — this is the most important part of the skill.**

For real estate b-roll, Graeham's default anchor stack is **Gray Malin + Douglas Friedman + Kodak Portra 400** (proven in build session). This gives warm, cinematic, aspirational aesthetic that avoids the AI-render look while staying appropriate for luxury lifestyle / real estate audiences.

**For place-specific shots (aerials, neighborhoods, recognizable geography), see the "Anonymization Strategy" section below** — this overrides the default anchor stack.

#### GPT Image 2-specific prompt notes (when routing selected this model)

When the routing rule sent you to GPT Image 2 because text fidelity matters, the prompt structure shifts:

- **Quote the exact text in double quotes inside the prompt.** Example: `a "FOR SALE" sign with phone number "650-555-0123" and address "1247 Weeks Street"`. Quoted text is what the model is told to render literally.
- **Specify text placement explicitly.** "Text positioned in the upper third, centered, sans-serif typeface, high contrast against the background" — placement instructions reduce reroll rate.
- **Realism anchors still apply.** The Gray Malin / Friedman / Portra 400 stack still works on GPT Image 2 — text accuracy is the additional capability, not a replacement for the realism layer. Stack realism instructions AFTER the text-rendering instructions in the prompt.
- **Anonymization Strategy still applies.** GPT Image 2 is on Higgsfield, which means Higgsfield's same output-side classifiers run on the result. Named geography is still risky regardless of which image model produced the start frame. See the Anonymization section below.

### Set controls

- **Aspect:** 16:9 or 9:16 (per Graeham's answer)
- **Resolution:** 4K (default, keep it)
- **Batch:** 4/4 (gives 4 variants to pick from)

Aspect control is a custom pill-button panel, NOT a native HTML select. Click the pill, click the target option.

### Generate

Cost: **16 credits** for 4 variants at 4K **on Nano Banana Pro** (verified in session). **GPT Image 2 credit cost on Higgsfield has NOT been verified yet** — confirm credit balance and observe the deduction on first GPT Image 2 generation, then update this skill with the actual cost. Per OpenAI's direct API pricing the underlying model is more expensive than Nano Banana Pro at the same quality tier, so expect higher per-image credit consumption.

Takes 20–60 seconds total on Nano Banana Pro. GPT Image 2 with thinking mode enabled is slower — expect 30–90 seconds, possibly longer for multi-panel or text-heavy prompts.

Four "Generating" placeholders appear at top of page, fill in progressively.

### Pick the hero variant

After all 4 render, **narrate briefly what each captures** — composition, whether it matches the brief, lighting quality. Recommend ONE explicitly with reasoning. Don't list pros/cons and leave it to Graeham — per his preferences, give a firm pick.

### Download the hero to local Downloads

**Mandatory step.** Click the hero thumbnail to open detail view → click the **Download** button in the bottom right of the detail panel.

This saves the 4K PNG to Graeham's `C:\Users\Admin\Downloads\` folder.

**Why this is mandatory:** Some Higgsfield models (like Kling 3.0) use native OS file pickers for start frames. Chrome's security sandbox blocks automation tools from reaching Graeham's local filesystem directly. Having the image already in Downloads enables fallback workflows (paperclip upload to chat → re-attach via `file_upload` tool) if the Assets → Animate path ever breaks.

---

## Stage 2: Animate with Seedance 2.0 or Kling 3.0

### Do NOT click the "Animate" button on the image detail view

This is a known broken handoff. It just closes the dialog without navigating. Skip it entirely.

### The correct navigation paths

**⚠️ STANDING RULE — model selection hierarchy:** Seedance 2.0 is **primary, always.** Kling 3.0 is **fallback, only.** Do not switch to Kling upfront to avoid a possible failure — try Seedance first, auto-pivot to Kling on classifier failure per the failure mode table. Credits are auto-refunded on classifier failures, so the cost of testing Seedance first is time (2–5 min per attempt), not credits. This is Graeham's explicit preference — confirmed in session.

**Path A — Seedance 2.0 (primary, per standing rule):**

1. Click the **Video** button in top nav (or navigate to `https://higgsfield.ai/ai/video`)
2. Click the **"Upload media"** slot on the left panel
3. Switch to **"Image Generations"** tab in the modal
4. Find the hero variant. New images may show black thumbnails with "Check eligibility" — click once to trigger the auto-check (takes 1–5 seconds), it should resolve to "Eligible"
5. Click the thumbnail again to select it as the reference
6. **Close the picker with Escape key or the X button — NEVER click-outside the picker area.** Click-outside can auto-commit the Generate action before you've finished setting up the prompt/duration, wasting 110+ credits. Verified in session — the picker has a click-outside-to-submit behavior that's easy to trigger accidentally.

**⚠️ CRITICAL — check for stale attachments.** The Upload media slot can accumulate old images from prior sessions. Before clicking Generate, verify only ONE image is in the slot. If two are visible (two small thumbnails side by side in the slot), hover over the old one to reveal the X and remove it. Multiple references cause Seedance to interpolate between them, creating morphing artifacts.

**Path B — Kling 3.0 (fallback only, after Seedance failure):**

Navigate to the **Assets** page (`https://higgsfield.ai/asset/all`) — it's the green button in top-right nav. Find the hero variant in the grid, click once to open detail view, click **Animate** button. This DOES work on the Assets page (unlike the broken Animate button on Nano Banana Pro's detail view).

This auto-routes to `/ai/video` with the image pre-attached to Kling's Start frame slot. Kling 3.0 auto-derives aspect from the source image (no aspect pill).

### Clear the motion prompt textbox

Previous prompts persist. `ctrl+a` → `Delete` before typing the new motion prompt.

### Type the motion prompt

**See the "NSFW Rules" section below — this is the second-most-important part of the skill.** Motion prompts have hard rules for passing Higgsfield's output-side safety classifier.

### Set video controls

- **Model:** Seedance 2.0 or Kling 3.0 (per Graeham's answer). Click the Model pill to switch if needed.
- **Duration:** 5s/10s/15s. The duration pill opens a range slider — click the pill, use arrow keys to adjust.
- **Aspect:** 16:9 or 9:16. Custom pill-panel, not a select. (Kling 3.0 hides this control — it derives from source image.)
- **Resolution:** 1080p

### Generate

| Model | 10s / 1080p / 16:9 cost | Render time |
|---|---|---|
| Seedance 2.0 | ~120 credits | 2–5 minutes |
| Kling 3.0 | ~20 credits | 1–3 minutes |

### Handle the upsell modal

Higgsfield periodically pops a "Generate Without Interruptions — Enable usage-based billing" modal. **Always click Skip.** Never click Continue — that enables automatic billing top-ups, which is a financial commitment that requires Graeham's explicit permission, not Claude's default.

---

> Read `references/realism-protocol.md` for the Realism Rescue Protocol (image-prompt anchor stacks, default template, what NOT to anchor to, boundary-crossing compositions) and the Anonymization Strategy for place-specific shots (replacement dictionary, proven anonymized aerial prompt).

> Read `references/classifier-rules.md` for the Classifier Rules — motion prompt engineering, the 7 verified rules, aerial duration gating (10s max on Seedance), motion-pattern risk table, and verified-working motion prompt templates.

---

## The Mandatory Revision Loop

**Do not download the video immediately after it completes.** First ask Graeham whether it works. Always.

After a successful render:

1. **Describe what the clip appears to show** — camera move, subject visibility throughout, lighting consistency, obvious artifacts. Be specific about what frames at 0:00, 0:05, 0:10 look like if you can tell from the playback scrubber.

2. **Ask a single explicit question** using `ask_user_input_v0` with these exact tappable options:
   - "Perfect — download it and finalize the skill"
   - "Good but needs one tweak — regenerate with changes"
   - "Start over with different start frame"

3. **Branch based on answer:**
   - **Perfect** → Click download button in video detail view (hover over the rendered video; download icon appears in top-right of the clip panel). Confirm file saved to Downloads. Done.
   - **Needs changes** → Ask specifically what to change (motion, composition, pacing, lighting). Keep the same start frame unless Graeham says otherwise — single-variable iteration makes it clear what caused the change. Confirm credit cost before regenerating.
   - **Start over** → Go back to Stage 1 with a refined image prompt.

4. **Never regenerate without confirming credit cost.** Every new attempt is another 120 credits (Seedance) or 20 credits (Kling). Graeham knows but confirm anyway.

---

> Read `references/failure-modes.md` for the full failure mode table (symptom → diagnosis → action).

---

## What this skill intentionally does NOT do

- ❌ No API-based access (sandbox allow-list blocks it; browser is the only path)
- ❌ No N8N webhook triggering (also blocked at allow-list layer)
- ❌ No Cinema Studio / Soul ID / advanced Higgsfield features (web UI only, too complex for v1)
- ❌ No automatic download — the revision loop requires Graeham's approval first
- ❌ No batch generation of multiple clips in one run — one clip per session, iterate from there
- ❌ No automatic billing opt-in

---

## Quick reference card

```
STAGE 1: IMAGE — ROUTE FIRST, THEN GENERATE

  ROUTING RULE:
    • Text in frame (signs, addresses, listing cards, UI mockups, multi-panel) → GPT Image 2
    • Pure photoreal (aerials, neighborhoods, interiors, exteriors)             → Nano Banana Pro
    • Transparent PNG required (alpha channel)                                  → Nano Banana Pro (GPT Image 2 doesn't support transparency yet)

  PATH 1A — Nano Banana Pro (default):
    URL:        higgsfield.ai/image/nano-banana-pro (DIRECT URL required)
    Cost:       16 credits / 4 variants at 4K (verified)
    Time:       20–60s for all 4 variants

  PATH 1B — GPT Image 2 (text-fidelity shots):
    URL:        Try /image/gpt-image-2 → /image/nano-banana-pro picker → /gpt-2 landing (provisional, lock on first session use)
    Verify:     Confirm "GPT Image 2" badge before generating
    Thinking:   Default ON when text accuracy matters (slower, higher cost)
    Cost:       UNVERIFIED on Higgsfield — expect higher than Nano Banana Pro
    Time:       30–90s, possibly longer with thinking mode
    Prompt:     Quote exact text in "double quotes", specify placement explicitly

  COMMON STEPS (both paths):
    AUTH CHECK: If redirects to /ai-image with Login/Sign-up → Graeham logged out, stop and ask
    Clear:      prior prompt + any attached reference thumbnails
    Prompt:     - Default: Gray Malin + Douglas Friedman + Portra 400 stack
                - Place-specific: unnamed descriptive anchors + anonymized geography
                - GPT Image 2 + text: quoted literals + placement instructions FIRST, then realism stack
    Optional:   drag-and-drop reference image onto prompt bar (4 variants converge)
    Settings:   4K, 4 variants, aspect per Graeham
    After:      Always DOWNLOAD hero to local Downloads folder

STAGE 2A: VIDEO via Seedance 2.0 (PRIMARY — standing rule)
  URL:        higgsfield.ai/ai/video (via top-nav Video)
  Image:      Upload media → Image Generations tab → click to check → click to select
  CHECK:      Only ONE image in Upload media slot (remove stale with X)
  PICKER:     Close with Escape/X — NEVER click-outside (auto-commits!)
  Clear:      prior prompt
  Prompt:     <25 words, camera move only. No color/temp words on warm images.
              No vertical moves on warm images (rule 7).
  Settings:   Seedance 2.0, 10s default, 16:9 pill, 1080p
  DURATION:   For aerial shots: 10s max. 12s+ fails classifier reliably.
              For interior/orbit/lateral: 15s fine.
  Cost:       ~110 credits (10s) / ~165 credits (15s, non-aerial only)
  Time:       2–5 minutes

STAGE 2B: VIDEO via Kling 3.0 (FALLBACK only after Seedance failure)
  URL:        higgsfield.ai/asset/all → click hero → Animate (this one works!)
  Image:      Auto-attached from Assets Animate button
  Clear:      prior prompt
  Prompt:     same rules as Seedance
  Settings:   Kling 3.0, 10s, 1080p. Aspect auto-derived from source.
  Cost:       ~20 credits
  Time:       1–3 minutes
  OVERRIDE:   For street-level walking shots, use Kling FIRST (Seedance
              reliably flags this pattern as protected content)

FAILURE AUTO-PIVOT LADDER (when Seedance flags):
  1. Protected content at 15s → retry at 10s (same image, same prompt)
  2. Still flagged at 10s → pivot to Kling 3.0
  3. NSFW on warm image with vertical move → switch to non-vertical motion,
     or strip all color/temp words, or switch to Kling

AFTER RENDER (MANDATORY):
  ASK:        "Perfect / needs tweak / start over?"
  REVISE:     single-variable changes, confirm credits first
  DOWNLOAD:   only after explicit "Perfect" approval
```

---

> Read `references/session-history.md` for session history notes — rejected approaches, the 2026-05-03 GPT Image 2 routing addition, and the final working stack summary.
