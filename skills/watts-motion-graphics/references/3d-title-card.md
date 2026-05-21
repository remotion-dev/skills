# 3D Title Card — Reference

The **3D Title Card** is the 6th mode of this skill. Unlike the 5 green-screen
overlay templates (Stat Callout, Compare Card, etc.), this mode renders **true
3D extruded gold-chrome text** with an **alpha channel** — it drops straight
onto a CapCut track with no chroma key step.

It is a **branded title element**, not a functional data overlay. Use it for
name cards, channel intros, listing-intro title cards, sign-offs.

---

## What it produces

A 3-line title card, rendered as an **alpha-channel ProRes 4444 `.mov`**:

| Line | Role | Font | Notes |
|---|---|---|---|
| 1 | Cursive accent | **Sacramento** | flat white script, e.g. "Bay Area Expert" |
| 2 | 3D gold hero | **Archivo Black** | true extruded 3D, gold-chrome material |
| 3 | Flat bold line | **Archivo 800** | flat white, e.g. a phone number |

Both orientations: **landscape 1920×1080** and **portrait 1080×1920**.

### Why alpha `.mov`, not green-screen

The 5 overlay templates render on chroma green because that's right for
functional panels. The 3D title is different: ProRes 4444 carries a real
alpha channel, so it composites in CapCut **with no chroma key** — no green
spill, no eaten letter edges. Confirmed working in Graeham's CapCut desktop.

**Trade-off, be honest about it:** ProRes 4444 files are large (~100MB+ for
an 8-second card). That's expected and fine for a title card. The green-screen
MP4 templates stay smaller — which is part of why they were NOT replaced.

---

## The type system (locked)

This mode runs its **own** type system — it does NOT use the Syne/Inter system
from `brand-tokens.md` (that's for the green-screen templates). Locked decisions:

- **3D hero:** Archivo Black (a separate purpose-built typeface file)
- **Cursive accent:** Sacramento (the one script exception)
- **Flat text** (line 3, and any other flat role): the **Archivo** family,
  full weight + italic range. Weight 800 for the bold third line.

3D fonts can't use a normal font file — Three.js needs a converted
`typeface.json`. `convert-font.js` in the project does that conversion
(woff → typeface JSON). Pre-converted fonts live in `public/`:
`archivo-black` (the locked 3D hero), plus `anton`, `poppins-bold`,
`helvetiker_bold` available as alternates.

**3D italic is NOT automatic** — Archivo's italic would need its own
conversion. The 3D hero is upright Archivo Black. Flat italic is fine
(Archivo ships true italics).

---

## The gold-chrome material (locked: `rich-gold`)

Defined in `src/layout.ts` → `GOLD_VARIANTS`. The locked default is
**`rich-gold`** — warm, saturated, high-contrast (bright top faces, deep
amber sides). Matched to a reference screenshot Graeham approved.

Other variants are kept in the file for re-picking: `polished-brand`,
`bright-chrome`, `hot-gold`, `deep-luxe`. The "chrome" look comes from the
material + lighting (low roughness, bright contrasty rig, warm emissive on
the shadow faces), NOT just the base color.

To compare variants, render the `GoldVariant-<name>` stills (see below).

---

## The animation (locked)

- **Entry: "pop-in"** — each line scales up from 0 with a slight overshoot
  (a scale spring) plus a fast opacity ramp.
- **Stagger: 2-second intervals** — line 1 at 0s, line 2 at 2s, line 3 at 4s.
- **Exit: "fade-out"** — all three lines fade together over the last ~0.8s.
- **Total length: 8 seconds** (240 frames @ 30fps). Lines land by ~5s, hold,
  then fade by 8s.

Controlled in:
- `src/Root.tsx` — `DURATION_FRAMES` (total length)
- `src/compositions/Title.tsx` — `popIn()` delays (the 0 / 60 / 120 frame
  stagger) and the `fadeOut` window

If a different hold length or stagger is wanted, change those values. To trim
in CapCut instead, just cut the tail.

---

## How to change the content

The three text lines are at the top of `src/Root.tsx`:

```ts
const CURSIVE_LINE = "Bay Area Expert";
const GOLD_LINE    = "GRAEHAM WATTS";
const THIRD_LINE   = "650-308-4727";
```

The 3D hero **auto-fits** to frame width — a short word ("SOLD") and a long
one ("GRAEHAM WATTS") both fit, capped so short words don't get huge. No
manual sizing needed when the text changes.

---

## Render workflow

```bash
cd assets/3d-title-project
npm install                      # first time only - rebuilds node_modules
npm run render:landscape         # -> out/watts-3d-title-landscape.mov
npm run render:portrait          # -> out/watts-3d-title-portrait.mov
```

Each full render is ~2 minutes. Output is ProRes 4444 with alpha
(`pix_fmt=yuva444p`). Verify alpha with:
`ffprobe -show_entries stream=pix_fmt out/watts-3d-title-landscape.mov`

### Fast iteration with stills

A still renders in ~30s vs ~2min for video — use stills for design decisions
(font/gold/spacing), video only for the final deliverable.

```bash
bash still.sh GoldVariant-rich-gold out/check.png 0
```

### CRITICAL: the browser path

Remotion needs a headless Chromium shell. It lives at a path with a **version
number** that changes between sessions (e.g. `chromium_headless_shell-1194`).
**Never hardcode it.** `render.sh` and `still.sh` auto-detect it with
`find /opt/pw-browsers -name headless_shell`. If you write a new render
command, use that same detection — a hardcoded version path will break in
the next session.

---

## CapCut handoff

1. Drop the `.mov` on a track **above** the HeyGen avatar + b-roll layers.
2. That's it — no chroma key. ProRes 4444 alpha is transparent natively.
3. The cursive, 3D gold, and bold line all carry their own soft shadow for
   legibility over busy b-roll.

---

## Files

```
assets/3d-title-project/
├── render.sh              auto-detecting video render (landscape|portrait)
├── still.sh               auto-detecting single-still render
├── convert-font.js        woff -> typeface.json converter (for new 3D fonts)
├── package.json
├── remotion.config.ts     Config.setVideoImageFormat("png") = alpha. KEEP.
├── public/                pre-converted typeface JSON fonts
└── src/
    ├── Root.tsx           content lines, duration, composition registry
    ├── layout.ts          GOLD_VARIANTS, GOLD_FONTS, camera math
    ├── fonts.ts           cursive + Archivo font loading
    ├── measureText.ts     deterministic 3D-text width measurement
    └── compositions/
        ├── Title.tsx      stacks the 3 lines, runs pop-in + fade-out
        ├── GoldText3D.tsx the Three.js extruded-gold layer
        └── FontSample.tsx flat font sample (reference only)
```
