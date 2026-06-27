# Capture Standard — the videographer technical spec + ingest QC

**Why this exists (Fugu deep-dive, 2026-06-27):** the biggest "amateur tell" is the *source footage*, not the script. Plates shot to this spec composite cleanly with Graeham's avatar and grade to a pro look; out-of-spec plates get rejected at ingest. This is the single highest-ROI, lowest-effort quality lever in the whole system. **Paste this into every videographer packet** (it sits with the shot glossary at the top).

## Camera settings (lock these)

- **Frame rate: 24fps** (23.976) for everything. Shoot **60fps** only for clips you *know* are slow-mo b-roll.
- **Shutter: 180° rule → 1/48s** at 24fps (1/50 is fine). Locked, not auto.
- **Picture profile: LOG / flat.** Use the camera's log profile (S-Log, C-Log, etc.) or the flattest neutral profile available — this preserves grading latitude. Never a baked-in "vivid"/contrasty profile.
- **White balance: MANUAL + LOCKED.** Set a Kelvin to the scene (~5600K daylight, ~3200K tungsten) and keep it identical across the shoot. **Never auto-WB** — it shifts shot to shot and can't be matched later.
- **Exposure: PROTECT THE HIGHLIGHTS.** Windows must not blow out — this is the #1 real-estate interior failure. Use zebras at 95–100 / the histogram; expose so window detail holds, even if the room sits slightly dark (we lift it in grade). A clipped window is unrecoverable.
- **ISO:** native ISO where possible; keep noise low.
- **Resolution: 4K minimum** — gives crop, stabilization, and vertical-reframe headroom.

## Stability & framing (the instant-pro signals)

- **Hard stabilization** — tripod or gimbal. No handheld jitter unless a move is intentional and planned.
- **LEVEL VERTICALS.** Door frames, walls, and corners must be vertical; horizon level. Use the camera's level/grid. Crooked verticals are the fastest amateur tell in real estate.
- **Slow, deliberate moves.** Let establishing shots **breathe** — hold ~2 seconds longer than feels necessary (the editor needs the handles).

## Avatar-plate rules (any shot Graeham's avatar composites onto)

Cross-reference the **avatar-match spec card** for the per-shot eyeline/framing. On capture:
- **Locked-off TRIPOD — zero movement** on any plate the avatar lands on (motion can't be match-moved reliably; don't try).
- **Leave clean negative space** in the avatar's placement zone (no busy clutter behind where he'll stand).
- **Even, soft light** on the placement zone, and **note the light direction** (window-left, lamp-right) so the avatar's lighting matches.
- **Avoid:** mirrors / reflective surfaces showing the crew, heavy occlusions in front of the placement zone, strong moving shadows.
- **Hold duration** = the VO length for that beat + 3–5s handles each end.

## Sound capture (cheap, high-impact)

- Record **30 seconds of clean room tone per location** (silence, camera rolling). The post sound layer uses it to match reverb so the avatar VO sounds *inside* the room, not in a booth.

## Ingest QC checklist — REJECT + reshoot/flag any plate that fails

- [ ] 24fps, 180° shutter (1/48–1/50)
- [ ] Log/flat profile
- [ ] White balance locked + consistent across shots
- [ ] Highlights protected — **no blown windows**
- [ ] Verticals level, horizon level
- [ ] Stable (tripod/gimbal, no jitter)
- [ ] 4K+
- [ ] Avatar plates: locked-off, clean placement zone, light direction noted, enough hold
- [ ] Room tone recorded per location

A plate that fails ingest QC is worth more reshot than "fixed in post." Garbage-in dominates everything downstream.
