# Shot Decomposition Rubric

This is the heart of the skill. A script is a wall of words; a shoot needs frames. Decomposition is the act of walking the script line by line and deciding **what kind of footage fills each line** — and pinning each decision to a clip ID so it can be shot, labeled, and reassembled weeks later by different people.

If you skip the discipline here, the videographer shoots the wrong thing and the trip is wasted. So the rule is simple and absolute: **every line of every script gets exactly one footage tag and one ID.** No line is left untyped.

## The 7 footage tags

Tag each script beat with one of these. The tag tells the videographer/editor what asset the line resolves to.

| Tag | Means | Who captures it | Gets a clip ID? |
|---|---|---|---|
| `AVATAR` | Graeham's face delivers this line on camera (real talking-head OR HeyGen avatar source). | Videographer (avatar-source) OR HeyGen render | Yes — `A` category, or marked HEYGEN if synthetic |
| `REAL-EXT` | Real exterior footage of this property/street/neighborhood. | Videographer | Yes — `L` (listing) or `B` (bank) |
| `REAL-INT` | Real interior footage inside the property. | Videographer | Yes — `L` |
| `BROLL` | A cutaway/establishing clip, real footage, no dialogue under it. | Videographer | Yes — `L` or `B` |
| `AI-BROLL` | A shot real footage can't get (impossible move, aerial we won't fly, a frame that needs text). Fill with an AI clip. | `cinematic-hooks` writes prompt → `higgsfield-video` generates | Yes — `AI` category; prompt lives in editor packet |
| `MOTION-GFX` | A stat, comparison, framework, or HERO word gets an on-screen graphic overlay. | `watts-motion-graphics` (chroma-green overlay, keyed in CapCut) | Graphic ID — `G` category |
| `VO` | Voiceover runs under footage with no face on screen (ElevenLabs clone). | ElevenLabs render; pairs with a B-roll/EXT clip underneath | VO segment ID — `V` category |

Notes that matter:
- A single beat can resolve to **a stack** — e.g. a drone `REAL-EXT` clip with a `VO` line over it and a `MOTION-GFX` price callout on top. When that happens, tag the primary footage and list the stacked layers explicitly (the editor packet keys them together by ID).
- `AVATAR` lines that will be delivered by the **HeyGen avatar** (synthetic) still need **avatar-source footage captured on this trip** if the chosen look isn't already trained — that's why avatar-source shots exist. If the look is already trained, mark the line `AVATAR (HEYGEN — existing look)` and no field capture is needed.
- `AI-BROLL` is a *gap-filler*, not a default. Use real footage wherever the videographer can physically get it. Reach for AI only when the shot is impossible, too expensive, or needs legible in-frame text.

## Per-shot capture spec

When a tag requires field capture (`AVATAR`, `REAL-EXT`, `REAL-INT`, `BROLL`), it is not "done" until you can answer all **seven**. These become the fields in the videographer packet. Write them in **plain English** (lead with plain words, abbreviation in parentheses) — the videographer should not need to decode jargon. See `shot-glossary.md`, which goes at the top of the packet.

1. **Clip ID** — assigned up front (see `clip-id-convention.md`).
2. **What's in frame** — what is literally visible, specific enough to picture cold. Not "the kitchen" → "the quartz waterfall island, island centered, window light from the left."
3. **Composition** — the detail the field crew specifically asked for: *how much* of the subject is in frame (full house corner-to-corner? just the porch? the right third where the ADU is?), **camera height** (eye-level, chest height, low looking up), **sky-vs-ground ratio** for exteriors (e.g. "~20% sky above the roofline, house through the middle, lawn in the bottom third — don't clip the roof"), and **exactly where to stand** ("end of the front walk, centered on the house"). This is what stops a videographer guessing.
4. **Camera move** — plain English: static/locked, slow push-in (camera eases toward subject), pull-back reveal, pan, tilt-up, gimbal walk (operator walks smoothly with a stabilizer), orbit, drone pull-back.
5. **Shot size** — plain English: wide shot (whole subject), medium shot (waist-up), medium close-up (chest-up), close-up (one feature fills frame).
6. **Location & light** — exact spot ("primary bath, from the doorway") and the light ("golden hour, sun behind camera"; "open shade, no harsh shadows").
7. **Hold duration** — seconds to roll (gives the editor handles): cutaways 4–6s, establishing 6–8s. Avatar-source is different — **2–3 minutes** per look for a Digital Twin (see `avatar-source-specs.md`), not seconds.

For `AI-BROLL`, instead of a field spec you provide the **generation prompt** (hand to `cinematic-hooks`/`higgsfield-video`) and note orientation, duration, and where it drops. For `MOTION-GFX`, provide the template type, the anchor phrase it sits under, and the exact label/number text. For `VO`, provide the line text and the clip ID it rides over.

## How to decompose — the pass

1. Take the long-form script (from `video-script-creation-engine`). It already carries inline tags like `[TALKING HEAD]`, `[B-ROLL: …]`, `[TEXT OVERLAY: …]`, `[DRONE: …]`. Treat those as the *starting point*, not the finished decomposition — they tell you intent; you add the capture spec and IDs.
2. Walk it top to bottom. For each beat, assign one of the 7 tags.
3. For every field-capture tag, fill the six-column spec. For `AI-BROLL`/`MOTION-GFX`/`VO`, fill their lighter spec.
4. Assign the clip/graphic/VO ID.
5. Derive the short-form cut: it reuses listing clip IDs (no new shooting) — note which IDs the short pulls.
6. Sweep for stacks (footage + VO + graphic on the same beat) and key them together.

## Worked example

Script beat (from the long-form listing script):

```
[TALKING HEAD] "This East Palo Alto home just hit the market at $1.15 million."
[B-ROLL: exterior of the house, for-sale sign]
[TEXT OVERLAY: "$1,150,000 — 1247 Weeks St"]
"Three beds, two baths, and a backyard that does the heavy lifting."
[DRONE: pull back over the backyard revealing the neighborhood]
```

Decomposes to:

**WEEKS-A01** — `AVATAR` (only if training/using a new look; skip if the look is already trained)
- Composition: medium shot (waist-up), straight-on, eye-level, tripod-locked, Graeham centered, consistent headroom. Stand on the front walk facing the porch.
- Light: open shade, soft frontal — no backlight, no hard sun.
- Hold: **2–3 minutes** of c