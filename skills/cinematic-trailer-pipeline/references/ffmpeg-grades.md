# ffmpeg Color Grade Presets

Three locked grades used in the editorial pass. Apply per-scene depending on the scene's role in the narrative arc.

---

## GRADE_WARM (default — Scenes 1, 2, 3, 4, 5, 7)

```
colorbalance=rs=.06:bs=-.08,eq=contrast=1.10:saturation=0.92:gamma=0.96,vignette=angle=PI/5
```

**What it does:**
- `colorbalance=rs=.06`: push warm into shadows (+6% red)
- `colorbalance=bs=-.08`: push cool out of shadows (-8% blue) → warm shadow lift
- `eq=contrast=1.10`: bump contrast 10% for cinematic punch
- `eq=saturation=0.92`: pull saturation down 8% for film-like color
- `eq=gamma=0.96`: slight gamma drop crushes blacks subtly
- `vignette=angle=PI/5`: light circular vignette draws eye to center

**Vibe:** *Drive* (2011) reference — warm amber tones, slightly desaturated, contrasty without being crushed.

---

## GRADE_COOL (Scene 6 — the crisis / night beat)

```
colorbalance=rs=.04:bs=.02,eq=contrast=1.15:saturation=0.85:gamma=0.92,vignette=angle=PI/5
```

**What changes vs. warm:**
- `bs=.02`: push cool INTO shadows (+2% blue, not subtracted) → blue-green night feel
- `contrast=1.15`: more aggressive contrast for tension
- `saturation=0.85`: pull more color out (cool/desaturated like a thriller)
- `gamma=0.92`: deeper crush on blacks for the night office feel

**Vibe:** *Sicario* / *Mindhunter* night-scene look. Cool, desaturated, contrasty.

**When to use:** crisis scenes, night scenes, anything that should feel cold/distant from the rest of the trailer.

---

## GRADE_HERO (Scene 7 — the emotional resolution)

```
colorbalance=rs=.05:bs=-.05,eq=contrast=1.08:saturation=0.95:gamma=0.97,vignette=angle=PI/5
```

**What changes vs. warm:**
- Less aggressive across the board
- `contrast=1.08`: lighter contrast preserves skin tone gradients
- `saturation=0.95`: keeps more natural color in skin
- `gamma=0.97`: lifts blacks slightly so emotional details aren't lost

**Vibe:** Softer, more natural, hero-shot grade. Lets skin tones breathe for the emotional payoff moment.

**When to use:** the trailer's emotional peak — usually the resolution or the hug / smile / handshake moment.

---

## TITLE_CARD (no grade)

PAI's title card output is already perfectly graded — clean white serif on textured matte black, subtle film grain. Applying any color filter to it dirties the typography. Pass it through with no filter.

---

## Quick-reference filter strings (copy-paste-ready)

```bash
# Warm (default)
GRADE_WARM="colorbalance=rs=.06:bs=-.08,eq=contrast=1.10:saturation=0.92:gamma=0.96,vignette=angle=PI/5"

# Cool (crisis/night)
GRADE_COOL="colorbalance=rs=.04:bs=.02,eq=contrast=1.15:saturation=0.85:gamma=0.92,vignette=angle=PI/5"

# Hero (emotional resolution)
GRADE_HERO="colorbalance=rs=.05:bs=-.05,eq=contrast=1.08:saturation=0.95:gamma=0.97,vignette=angle=PI/5"
```

---

## When to push the grade further

The defaults above are **subtle** — they unify look without overwhelming PAI's existing aesthetic. For a stronger cinematic statement:

- Bump `contrast=1.15` → `contrast=1.20` for more punch
- Bump `colorbalance=rs=.06` → `rs=.10` for deeper warm shadows  
- Add `curves=preset=darker` for a more "Sicario night" feel

Don't go past 1.25 on contrast or you'll start losing detail in skin tones and shadows. Always export a test frame and check skin tones before committing.

---

## Audio limiting (always do this)

Final audio always gets `alimiter=limit=0.95` on the master to prevent peak clipping. Without it, the music + VO mix can spike above 0dB and distort on playback.

```
[music][a1][a2][a3][a4][a5]amix=inputs=6:duration=longest:normalize=0,alimiter=limit=0.95[aout]
```

The `normalize=0` is critical — without it, amix averages the inputs and the mix gets quiet. With it disabled, full volume on each stream is preserved.
