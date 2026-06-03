# B-Roll Gates, Count, and Asset Router (June 2026)

Source of truth for how this engine plans and emits b-roll. Encodes the production standards agreed with Peter (June 1, 2026). Every production package and every Production Prompt copy MUST follow this.

## 1. B-roll count scales with runtime — with hard floors

Do NOT emit a fixed number of clips. Plan ~1 cutaway per 3-5 seconds of non-talking-head time, then enforce the floors:
- Short-form (Reels / Shorts / TikTok): floor 8-14 cutaways.
- Long-form (YouTube): floor 40+ cutaways.
Compute count = ceil(non_talking_head_seconds / 4) and never drop below the floor. State the math in the shot-list header.

## 2. Asset router — decide and TAG the source per shot

Most shots are NOT AI-generated. Route each shot to the cheapest reliable source and TAG it in the shot list with one of [AI] / [STOCK] / [MAP] / [FILM]:
- [MAP] a map -> Mapbox Static Images API at the real lat/long. NEVER generate a map (generated maps show a generic or wrong place).
- [STOCK] a known real place (a street, San Mateo County aerial, a neighborhood) -> tagged stock library first; if missing, [FILM] it (videographer request).
- [FILM] real footage we shoot or already own -> predictable real-world action, and any real location with no stock.
- (overlay) on-screen text / price card / stat / title -> Remotion motion-graphic overlay (watts-motion-graphics), composited in CapCut. Generative video cannot render text reliably; that is where artifacts come from. Not a b-roll clip.
- [AI] genuinely novel or impossible shots (cinematic hook, surreal, time-lapse) -> generate (Seedance / Kling / Higgsfield). Only when nothing else can produce it.

Every shot in the emitted list carries its tag so Peter knows the source at a glance.

## 3. Generation rules (when a shot is [AI])

- FIRST-FRAME QC (hard gate): generate and APPROVE the still image BEFORE animating. If the still is off, regenerate the cheap still; NEVER animate a bad frame.
- Image-to-video from the approved locked start frame (not text-to-video).
- Short clips, 2-4 seconds (less drift = fewer "door opens wrong" failures).
- Negative prompts for known failure modes (warped hands, doors, signage, text artifacts). One subject action per clip.

## 4. Location specificity (hard rule)

Talking about a specific place -> the visual must BE that place. [MAP] via Mapbox at exact coordinates; real-area look via [STOCK] tagged to that city/county or [FILM]. Never a generic AI city or stand-in. If no stock exists for a needed real location, emit a Videographer Shot Request line (auto-creatable as a GHL/calendar task), e.g. "Videographer is at the Thursday listing shoot; ask for 10 minutes of San Mateo County drone aerials on the way."

## 5. B-roll QC gate (per clip)

Before a clip is accepted: (1) matches the shot intent (right place, right action); (2) continuity and physics are clean; (3) any in-frame text is correct, or there is none (text belongs on Remotion overlays); (4) for [AI], the still was approved first. Fail any -> re-roll THAT clip only, never the whole sequence.

## 6. Avatar

Render the talking-head on HeyGen Avatar V (best motion) by default. Do not render on Avatar IV and then redo on V.

## 7. What rides along in the copy

Every Production Prompt copy and the daily Peter email MUST prepend the "Workflow Quality Rules" block from SKILL.md so whoever pastes into Claude gets these rules inline.
