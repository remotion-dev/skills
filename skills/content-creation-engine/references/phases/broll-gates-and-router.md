# B-Roll Gates, Count, and Asset Router (June 2026)

Source of truth for how this engine plans and emits b-roll. Goal: stop the "doors open wrong / only 5 clips / b-roll takes the longest" failures. Every production package and every Production Prompt copy MUST follow this.

## 1. B-roll count scales with runtime (no fixed number)

Do NOT emit a fixed 5 clips. Compute it:

    count = ceil(spoken_duration_seconds / cadence)   # cadence = 4s default (3-5s range)

- 30s short -> ~6-10 inserts
- 60s short -> ~12-20 inserts
- 4-min long-form -> ~50-70 inserts (mix of generated + stock + overlays)

Emit a count appropriate to the script length. State the math in the shot list header.

## 2. Asset router — decide the SOURCE per shot (most shots are NOT generated)

For each shot in the list, route to the cheapest reliable source:

| If the shot is... | Source | Why |
|---|---|---|
| A map | **Mapbox Static Images API** at the real lat/long | Never generate a map. Generated maps show the wrong/generic place. |
| A known real place (a street, San Mateo County aerial, a specific neighborhood) | **Stock library first** (tagged by city/county); else flag for the videographer | Real place = real or stock footage, not a hallucination |
| On-screen text / price card / stat / title | **Remotion overlay** (watts-motion-graphics), composited in CapCut | Generative video cannot render text reliably — this is where artifacts come from |
| Genuinely novel / impossible (cinematic hook, surreal, time-lapse) | **Generate** (Seedance / Kling / Higgsfield) | Only reach for generation when nothing else can produce it |

## 3. Generation rules (when a shot IS generated)

- **Image-to-video with a LOCKED start frame** by default (Nano Banana / GPT Image 2 -> Seedance/Kling). Not text-to-video.
- **Short clips, 2-4 seconds.** Less time for physics/continuity to drift (the "door opens wrong" failure).
- Add negative prompts for the known failure modes (extra limbs, warped doors, text artifacts).
- One subject action per clip. Don't ask one clip to do two things.

## 4. Location specificity (hard rule)

- Talking about a specific place -> the visual must BE that place. Map -> Mapbox at the exact coordinates. Area look -> stock tagged to that city/county. Never a generic stand-in.
- If no stock exists for a needed real location, DON'T fake it. Emit a **Videographer Shot Request** line in the production package (and it can be auto-created as a GHL/calendar task): e.g., "Videographer is at the Thursday listing shoot — ask for 10 min of San Mateo County drone aerials on the way."

## 5. B-roll QC gate

Before a clip is accepted into the cut:
1. Does it match the shot intent (right place, right action)?
2. Continuity/physics clean (no warped doors, hands, signage)?
3. Any text in-frame is correct (or there is none — text belongs on Remotion overlays)?
Fail any -> re-roll THAT clip only (short clip + locked frame), never the whole sequence.

## 6. What rides along in the copy

Every Production Prompt copy (the purple "Copy Production Prompt" button) and the daily Peter email MUST prepend the "Workflow Quality Rules" block from SKILL.md so whoever pastes into Claude gets these rules inline.
