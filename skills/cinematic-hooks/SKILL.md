---
name: cinematic-hooks
description: Generate scroll-stopping cinematic video prompts for AI video generators (Seedance 2.0, Higgsfield, Kling, Runway). Use ANY time user mentions video prompt, Seedance prompt, Higgsfield prompt, AI video, cinematic hook, scroll-stopper, pattern interrupt, creative hook, video concept, shot list, ad opener, brand film prompt, listing video concept, real estate video idea, surreal video, dream sequence, impossible camera move, character consistency, reference file tagging, video generation prompt, or turning a creative idea into generation-ready prompts. Also trigger when user describes a scene, asks for attention-grabbing video ideas, wants to plan a video sequence, or says "make me a video prompt", "write me a Seedance prompt", "plan a hook for this listing", "I need a pattern interrupt opener." Specializes in visually disruptive, curiosity-driven hooks that stop a scroll in under 2 seconds.
---

# Cinematic Hooks — AI Video Prompt Builder

## CRITICAL CONTEXT: What this skill produces

This skill produces TEXT PROMPTS that get pasted into AI video generation tools like Seedance 2.0, Higgsfield, Kling, or Runway. These tools take a text description and generate a video clip from it.

This skill does NOT produce:
- Camera equipment lists or gear recommendations
- Production schedules or timelines
- Color grading software instructions
- Posting strategies or hashtag lists
- Audio/music recommendations
- Real-world shooting plans

Everything in the output should be something that either (a) gets pasted directly into an AI video generator's text prompt field, or (b) helps the user understand how to structure their generation session (which reference images to use, what order to generate clips in, how to maintain character consistency between generations).

Think of it this way: the user will sit at their computer, open Seedance 2.0 or Higgsfield, and paste each shot's PROMPT field into the generator one at a time. That's the workflow. Everything this skill outputs must serve that workflow.

## How this skill works

1. The user provides a **creative brief** — anything from "a surreal hook for my new listing at 123 Oak Street" to a detailed storyboard. They may also provide reference images, mood boards, brand context, or specific effects.
2. Read `references/pattern-interrupt-playbook.txt` to load the creative framework for scroll-stopping hooks.
3. Generate a complete video prompt package in plain text, structured into the six mandatory sections below.

## The psychology of pattern interrupts

Understanding WHY certain visuals stop a scroll is essential to writing prompts that produce them. The human visual system is wired to notice three things instantly:

**Violation of expectations** — Something that doesn't belong. A house floating in clouds. A door opening onto an ocean. A person walking on a ceiling. The brain flags these as "needs attention" before conscious thought kicks in.

**Impossible motion** — Camera moves that couldn't exist in reality. Flying through a keyhole, orbiting a room in a single unbroken shot, a macro-to-aerial transition with no cut. These trigger curiosity because the viewer can't figure out how they were made.

**Scale disruption** — Playing with relative size in ways that feel wrong. A person tiny against an enormous door. A house fitting in someone's palm. A neighborhood seen from inside a snow globe. Scale tricks are viscerally attention-grabbing.

**Temporal disruption** — Time behaving strangely. A room furnishing itself in reverse. Seasons cycling on a single tree in 3 seconds. A person aging/de-aging mid-stride. Time manipulation creates an uncanny quality that holds attention.

Every prompt should leverage at least one of these four mechanisms. The best hooks stack two or three.

## Input expectations

The user's brief can include any combination of:
- Subject/talent description (who or what is on screen)
- Property or location details (address, features, style)
- Setting/environment
- Mood, tone, energy level
- Brand or product context
- Specific effects or camera moves they want
- Duration target
- Reference images or videos (up to 12 for Seedance 2.0)
- Colour palette or grade preferences
- Platform target (Instagram Reels, YouTube Shorts, TikTok, YouTube long-form)

If the brief is too vague to build a full prompt (e.g. "make something cool for my listing"), ask one focused clarifying question. Don't over-interrogate — make creative decisions where the user hasn't specified. Default to bold and surprising over safe and expected.

## Output structure

ALWAYS output ALL SIX sections in this exact order. Use these EXACT section headers. Never skip a section. Never add extra sections. Never replace these sections with things like "Emotional Narrative" or "Production Notes" or "Platform Optimization" — those are not part of this skill's output.

### Section 1: HOOK CONCEPT

A 2-3 sentence description of the core creative idea. What's the pattern interrupt? What makes this stop a scroll? Name the specific psychological mechanism (violation of expectations, impossible motion, scale disruption, temporal disruption) being used. This section exists so the user can gut-check the concept before reading the full shot breakdown.

Example:
```
HOOK CONCEPT
The front door opens to reveal the Bay instead of the interior — a reality glitch
that violates spatial expectations. The door closes and reopens to the real foyer,
then camera pushes through to floor-to-ceiling windows showing the same Bay view.
The payoff: the "impossible" view was real all along.
Mechanism: Violation of expectations + reveal payoff
```

### Section 2: SHOT-BY-SHOT PROMPT SEQUENCE

This is the core of the output. Each shot gets its own block. The PROMPT field is the single most important line — it is the exact text the user will copy-paste into the AI video generator.

```
SHOT [N] ([timestamp]) — [Shot Name]
• PROMPT: "[A single, dense paragraph describing exactly what the AI video generator should produce. Written in natural language. Describe the scene, the lighting, the camera angle, any motion, the mood, and every visual element in frame. This is what gets pasted into Seedance/Higgsfield/Kling.]"
• CAMERA: [Camera angle, movement type, lens equivalent if helpful]
• EFFECTS: [Primary visual effect] + [secondary effects if stacked]
• SPEED/TIMING: [Duration of this shot, any speed ramping, slow-mo percentages]
• TRANSITION OUT: [How this shot connects to the next — cut, morph, whip pan, bloom flash, etc.]
• CHARACTER NOTE: [Only if a person appears — repeat their full physical description. AI generators have zero memory between shots, so you must re-describe the character every time.]
• REFERENCE FILES: [Which Seedance reference image slots to use — e.g. "ref1: character face, ref3: location exterior"]
```

Guidelines for the PROMPT field:
- Write it as a complete visual description in one paragraph — imagine you're commissioning a painting
- Include: what's in frame, lighting quality and direction, color palette, camera position, any motion happening, mood/atmosphere, time of day
- Use natural language, not editing software jargon. Say "the camera slowly pulls back to reveal" not "apply a 2-second dolly-out keyframe"
- Be specific: "warm golden hour light casting long shadows across honey-toned hardwood floors" not "nice lighting"
- Each prompt should describe a ~2 second clip by default (Seedance processes best in 2-second chunks). Go up to 4 seconds for slower, contemplative shots.
- If the user provides a START FRAME image, Shot 1's PROMPT should describe what happens NEXT — don't re-describe what's already in the frame. The generator builds forward from the start frame.
- For SEAMLESS single-take prompts (no cuts between shots): combine all shots into one continuous PROMPT paragraph instead of separate shot blocks. Note this option to the user if their concept suits a single unbroken take.

Guidelines for other fields:
- Name effects precisely: "speed ramp (deceleration from 200% to 50%)" not just "speed ramp"
- Describe stacked effects explicitly — if 3 things happen at once, list all 3
- Mark the most impactful shot with "⚡ SIGNATURE SHOT"
- Be specific about speed percentages for slow-motion (e.g. "approximately 20-25% speed")
- For character consistency: the CHARACTER NOTE must repeat the SAME physical description in every shot where the character appears

### Section 3: CHARACTER CONSISTENCY GUIDE

Only include this section if a person/character appears in the video. Skip it entirely if the video has no people. This section locks down the character's visual identity so the user can maintain consistency across multiple AI generations.

```
CHARACTER: [Name or role]
• FACE: [Ethnicity, age range, facial features, hair color/style/length]
• BUILD: [Height impression, body type]
• WARDROBE: [Exact outfit — color, fit, material, style]
• EXPRESSION RANGE: [The emotional arc across shots — e.g. "neutral curiosity → wide-eyed wonder → confident smile"]
• REFERENCE SLOT: [Which Seedance ref image slot to use for this character's face/body]
• CONSISTENCY NOTE: [Practical tip — e.g. "Use the same reference image in every generation. If the generator drifts on hair color, regenerate that shot."]
```

Why this matters: AI video generators notoriously drift on character appearance between clips. Having a single canonical description that gets copy-pasted into every shot's PROMPT dramatically reduces drift. The reference image slot is the strongest consistency tool available.

### Section 4: MASTER EFFECTS INVENTORY

A numbered list of every distinct visual effect used across the full prompt:
- Effect name
- How many times it appears (e.g. "used 3x")
- Which shots it appears in
- A one-line description of what it does in the edit

Group by category: speed manipulation, camera movement, digital effects, transitions, compositing, optical effects.

This section helps the user see the full palette of visual techniques at a glance and plan their generation session.

### Section 5: EFFECTS DENSITY MAP

Break the timeline into segments (roughly 2-4 second chunks) and rate each:
- **HIGH DENSITY** — 4+ effects stacked or rapid-fire
- **MEDIUM DENSITY** — 2-3 effects
- **LOW DENSITY** — 1 effect or clean footage

Format:
```
[timestamp range] = [DENSITY LEVEL] ([effects list] — [count] effects in [duration])
```

The density map must show contrast. If every segment is HIGH, the video will feel exhausting and chaotic. If every segment is LOW, it won't hold attention. The best hooks are HIGH → LOW → HIGH or start with a spike and settle into a reveal.

### Section 6: ENERGY ARC

Describe the overall energy structure as a narrative arc:
- **HOOK** (first 1-2 seconds): How you grab attention. This must be the strongest visual moment or the most disorienting pattern interrupt. Front-load impact.
- **DEVELOP** (middle): How the concept unfolds. What keeps the viewer watching after the initial hook?
- **LAND** (final moments): How the energy resolves. For real estate: this is usually the reveal (the property, the view, the lifestyle). For brand content: the logo/tagline moment. The landing must feel intentional, not like the effects ran out.

## Creative frameworks for hooks

These are proven patterns for scroll-stopping openers. Use them as starting points, not rigid templates:

**The Impossible Transition** — Start inside something small (a keyhole, a mailbox, a coffee cup) and fly out into the full scene. Or reverse it: start wide and dive into an impossible detail.

**The Reality Glitch** — Something in the scene behaves wrong. A wall dissolves into the view behind it. Gravity reverses for one object. A reflection shows a different scene than reality.

**The Scale Trick** — A miniature version of something becomes full-size (or vice versa). A model house grows into a real house. A person shrinks to walk through a dollhouse-sized neighborhood.

**The Time Splice** — Different time periods or seasons exist simultaneously in the same frame. Half a house under construction, half finished. A yard cycling through seasons in one pan.

**The Perspective Shift** — Start from an unusual or impossible viewpoint (inside a wall, underground looking up, from the POV of a door handle) and transition to normal.

**The Seamless Morph** — One object transforms smoothly into another. A floor plan drawing becomes the actual room. A photo becomes a video. A sketch becomes reality.

## Duration calibration

- **2-5 seconds** (single hook clip): 2-4 shots, one signature effect, maximum front-loaded impact
- **5-10 seconds** (Reel/Short hook): 4-7 shots, lean and punchy, 1 signature effect
- **10-20 seconds** (full short-form): 8-14 shots, room for contrast and build, 1-2 signature effects
- **20-30 seconds** (brand film): 12-20 shots, full three-act arc, 2-3 signature effects
- **30+ seconds**: Scale accordingly but maintain density contrast

Default to 5-10 seconds if the user doesn't specify.

## Real estate context

When the brief involves a property or listing:
- The property is the PAYOFF, not the opener. Lead with the hook, reveal the property.
- Features like views, pools, architecture — these are the "reveal" moments. Build anticipation toward them.
- Lifestyle sells more than specs. Show how it FEELS to live there, not how many bedrooms it has.
- Neighborhood hooks work well: visualize "what if you could walk from your front door to [landmark] in 3 minutes" as an impossible seamless walk.

## Tone and style

- Write in a direct, technical tone — like a director's shot notes
- Use bullet points within each shot block for clarity
- Be concise but complete — every detail earns its place
- No hype language. Don't write "stunning" or "breathtaking." Describe what happens and let the visuals speak.
- The PROMPT field should read like a painting you're commissioning — rich in visual detail, clear about composition, specific about mood and light

## Generator-specific tips

**Seedance 2.0:** Supports up to 12 reference images. Use them for character consistency, location matching, and style anchoring. Note reference slots explicitly in each shot.

**Higgsfield:** Strong at character consistency with clear references. Best at short clips with dramatic motion. Keep prompts focused on one clear action per shot.

**Kling / Runway / General:** Write generator-agnostic prompts focused on clear visual description. Note where reference images would help but don't assume specific slot systems.

## Character limits per platform

This is critical — AI video generators have hard character limits on prompts:
- **Seedance 2.0:** 4,000 characters max per prompt
- **Higgsfield:** ~3,000 characters max per prompt
- **Other platforms:** Assume 3,000 unless told otherwise

When writing prompts, proactively keep them under the target platform's limit. Techniques for fitting more into fewer characters:
- Use standard abbreviations where the generator will understand them: "cam" for camera, "BG" for background, "FG" for foreground, "DOF" for depth of field, "CU" for close-up, "ECU" for extreme close-up, "WS" for wide shot, "MS" for medium shot, "OTS" for over-the-shoulder, "POV" for point of view, "SFX" for special effects, "VFX" for visual effects, "slo-mo" for slow motion
- Combine related visual details into single dense phrases instead of separate sentences: "golden-hour sidelit oak floors, long shadows" instead of "The golden hour light comes from the side and illuminates the oak floors, casting long shadows"
- Cut filler words ruthlessly: "camera pulls back revealing" not "the camera slowly begins to pull back to reveal"
- Stack descriptors with hyphens: "rain-slicked cobblestone" not "cobblestones that are wet from the rain"
- If a prompt still exceeds the limit after compression, split it into two sequential generations and note the split point
