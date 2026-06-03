# B-Roll Gates, Count, and Asset Router (June 2026)

Source of truth for how this engine plans and emits b-roll. Goal: stop the "doors open wrong / only 5 clips / b-roll takes the longest" failures. Every production package and every Production Prompt copy MUST follow this.

## 1. B-roll count scales with runtime (no fixed number)

Do NOT emit a fixed 5 clips. Compute it: count = ceil(spoken_duration_seconds / cadence), cadence ~4s (3-5s range). 30s short -> ~6-10; 60s -> ~12-20; 4-min long-form -> ~50-70 (mix of generated + stock + overlays). State the math in the shot list header.

## 2. Asset router — decide the SOURCE per shot (most shots are NOT generated)

- A MAP -> Mapbox Static Images API at the real lat/long. Never generate a map (generated maps show the wrong/generic place).
- A known real place (a street, San Mateo County aerial, a neighborhood) -> stock library first (tagged by city/county); else flag for the videographer.
- On-screen text / price card / stat / title -> Remotion overlay (watts-motion-graphics), composited in CapCut. Generative video cannot render text reliably; that is where artifacts come from.
- Genuinely novel / impossible (cinematic hook, surreal, time-lapse) -> generate (Seedance / Kling / Higgsfield). Only when nothing else can produce it.

## 3. Generation rules (when a shot IS generated)

Image-to-video with a LOCKED start frame by default (not text-to-video). Short clips, 2-4 seconds (less drift = fewer "door opens wrong"). Negative prompts for known failure modes. One subject action per clip.

## 4. Location specificity (hard rule)

Talking about a specific place -> the visual must BE that place (Mapbox at exact coordinates, or stock tagged to that city/county). Never a generic stand-in. If no stock exists, emit a Videographer Shot Request line (auto-creatable as a GHL/calendar task), e.g. "Videographer is at the Thursday listing shoot; ask for 10 min of San Mateo County drone aerials on the way."

## 5. B-roll QC gate

Before a clip is accepted: (1) matches the shot intent (right place, right action); (2) continuity/physics clean; (3) any in-frame text correct (or none; text belongs on Remotion overlays). Fail any -> re-roll THAT clip only, never the whole sequence.

## 6. What rides along in the copy

Every Production Prompt copy and the daily Peter email MUST prepend the "Workflow Quality Rules" block from SKILL.md so whoever pastes into Claude gets these rules inline.
