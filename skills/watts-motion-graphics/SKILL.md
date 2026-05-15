---
name: watts-motion-graphics
description: "Watts-brand motion-graphics generator for Graeham's videos: Remotion projects composited onto HeyGen avatar + Higgsfield b-roll in CapCut. Use when the user mentions motion graphics, overlay graphics, stat callout, compare card, decision framework graphic, HERO reveal, lower third, title card, end card, 3D title card, 3D gold text, gold chrome title, animated title card, chroma key graphics, green screen graphics, Remotion overlay, animated text reveal, or recreating the visual style of a past Watts video. Also fires on 'motion graphic for that scene', 'animate that stat', '3D title'. TWO OUTPUT PATHS: the 5 green-screen overlay templates render on pure green #00FF00 for chroma key (Syne + Inter type); the 3D Title Card mode renders true 3D extruded gold-chrome text as an alpha-channel .mov (Archivo + Sacramento type). 6 modes total: Stat Callout, Compare Card, Decision Framework, HERO Reveal, End Card, 3D Title Card."
---

# Watts Motion Graphics — Remotion for HeyGen + B-roll Videos

This skill has **two output paths**:

1. **Green-screen overlay templates (5)** — Stat Callout, Compare Card,
   Decision Framework, HERO Reveal, End Card. Functional data overlays
   rendered on pure chroma green `#00FF00`, keyed out in CapCut. Syne + Inter
   type. This is the original core of the skill — everything below the
   "3D Title Card" section is about these.
2. **3D Title Card (1)** — true 3D extruded gold-chrome text, rendered as an
   **alpha-channel `.mov`** (no chroma key needed). A branded title element,
   not a data overlay. Archivo + Sacramento type. See
   `references/3d-title-card.md` and the section just below.

Pick the path by what's being asked for: a stat/compare/framework graphic →
green-screen template; a name card / channel intro / 3D gold title → 3D Title
Card.

## When this skill fires

- "Make me motion graphics for my new video"
- "Add a stat callout that says X when I say Y"
- "Build the overlay package for [video name]"
- "I need a HERO reveal on the word 'tax-free'"
- "Do another motion graphic in the same style as my last video"
- "Build the compare card for $100K vs $55-65K"
- "Add a decision framework graphic to scene 5"
- Any time the user references a previous Watts video and wants the same visual language

If the user has the script and audio rendered but no graphics yet, this is the right skill. Pair with `heygen-video` (avatar layer), `higgsfield-video` (b-roll layer), and `content-creation-engine` (if no script yet — that skill absorbed `video-script-creation-engine` in April 2026).

---

## CRITICAL: Why green background, NOT black + Screen blend

This is the single most important architectural decision in this skill. **Do not change it.**

| Approach | Result |
|---|---|
| ❌ Black background + Screen blend in CapCut | Text becomes translucent. Dark elements vanish. Hard to read. |
| ✅ Pure chroma green (`#00FF00`) + Chroma key removal in CapCut | Black panels stay fully opaque. Text crisp. Contrast preserved. |

The first attempt at the Tech Layoff video used black + Screen blend and the text was unreadable. The fix was to switch to chroma green and key it out in CapCut. **Every Watts overlay from that point forward uses green.**

Filename convention: always end with `-greenbg.mp4` so editors / VAs / future-Graeham immediately know it's chroma-key-ready, not Screen-blend-ready.

**Exception — the 3D Title Card does NOT use green.** It renders an alpha
channel directly (ProRes 4444). See the next section. The green rule above
applies to the 5 overlay templates only.

---

## 3D Title Card (Mode 6) — alpha .mov, NOT green-screen

A separate mode from the 5 green-screen templates. Renders **true 3D extruded
gold-chrome text** with a real alpha channel — composites in CapCut with **no
chroma key step**. It is a branded title element (name card, channel intro,
listing-intro title), not a functional data overlay.

**Full documentation: `references/3d-title-card.md`. Read it before using
this mode.** Quick orientation:

- **Project location:** `assets/3d-title-project/` — a complete Remotion +
  Three.js project. Copy it out, `npm install`, render.
- **Output:** alpha-channel ProRes 4444 `.mov`, landscape + portrait.
- **3 lines:** cursive accent (Sacramento) / 3D gold hero (Archivo Black,
  `rich-gold` chrome material) / flat bold line (Archivo 800). Content is set
  in `src/Root.tsx`.
- **Animation:** pop-in entry, 2-second stagger between lines, fade-out exit.
- **Type system:** this mode runs its OWN type system (Archivo + Sacramento).
  It does NOT use the Syne/Inter system in `brand-tokens.md` — that's for the
  green-screen templates. The skill intentionally carries both.
- **Render:** `cd assets/3d-title-project && npm install && npm run render:landscape`
  (and `render:portrait`). The render scripts auto-detect the headless browser
  — never hardcode the versioned `/opt/pw-browsers/...` path.
- **CapCut:** drop the `.mov` on a track above the b-roll. Transparency is
  native — no chroma key.

**Honest trade-off:** ProRes 4444 alpha files are large (~100MB+ for 8s).
That's why the 5 functional overlay templates were NOT migrated to alpha —
green-screen MP4s stay small for the VA-driven workflow. Different tools,
different jobs.

---

## Standard workflow

> The workflow below is for the **5 green-screen overlay templates**. For the
> 3D Title Card, follow `references/3d-title-card.md` instead.

### Step 1 — Confirm the inputs
Before writing any code, verify:

1. **Script signed off** — full text, scene-by-scene, with HERO word identified
2. **Audio rendered** OR **scene timing estimates** — audio is the master clock per Graeham's standing rules
3. **Orientation** — Long-form (1920×1080) or Short-form (1080×1920)? Ask if not specified.
4. **HERO word and scene** — the single climax moment that gets the Watts Gold treatment (one per video)
5. **Brand variant** — default is Watts (Graeham). If PropOS or Wattson, ask for a tokens override.

### Step 2 — Read the references
Load these in order:

- `references/brand-tokens.md` — exact hex codes, font specs, the HERO-ONLY rule
- `references/graphic-templates.md` — specs for the 5 templates (Stat Callout, Compare Card, Decision Framework, HERO Reveal, End Card)
- `references/capcut-workflow.md` — assembly order, chroma key settings, music drop on HERO
- `references/standing-rules.md` — Graeham's locked rules (no DRE in graphics, etc.)

### Step 3 — Plan the graphic list
For each graphic, capture:
- Template type (one of the 5)
- Anchor phrase (the spoken word/phrase the graphic appears under) — NEVER timestamp anchors
- Hold duration (default 3–5s, HERO is 5–7s)
- Content (label text + numbers + colors)
- Exit (cut out, fade out, or replaced by next graphic)

Organize into a single table the user signs off on **before** scaffolding the Remotion project.

### Step 4 — Scaffold the Remotion project

```
project-name/
├── package.json
├── tsconfig.json
├── remotion.config.ts
├── CLAUDE.md
└── src/
    ├── index.ts
    ├── Root.tsx
    ├── compositions/
    │   └── Overlay.tsx
    ├── components/
    │   ├── StatCallout.tsx       (copy from assets/components/)
    │   ├── CompareCard.tsx
    │   ├── DecisionFramework.tsx
    │   ├── HeroReveal.tsx
    │   └── EndCard.tsx
    └── lib/
        ├── brand.ts              (copy from assets/brand.ts)
        └── timings.ts            (copy from assets/timings-template.ts)
```

Copy the pre-built assets from `assets/`:
- `assets/brand.ts` → `src/lib/brand.ts` (locked tokens, do not edit)
- `assets/components/*.tsx` → `src/components/`
- `assets/timings-template.ts` → `src/lib/timings.ts` (then populate with real frames)

### Step 5 — Populate timings
**If audio is already rendered:**
1. Run Whisper on the MP3 for word-level timestamps
2. For each graphic, find the timestamp of its anchor phrase
3. Convert to frame: `frame = Math.round(seconds * 30)`
4. Update `src/lib/timings.ts`

**If audio is not yet rendered:**
1. Use placeholder frame numbers based on speech pace (~150 wpm = ~2.5 wps)
2. Comment each line `// PLACEHOLDER — update after audio render`
3. Tell the user: "These are placeholders. Re-render the overlay AFTER you have the MP3, with real timings from Whisper."

### Step 6 — Build the composition
`src/compositions/Overlay.tsx` orchestrates all graphics on a single `<AbsoluteFill backgroundColor="#00FF00">` canvas. Each graphic uses Remotion's `<Sequence from={frame} durationInFrames={hold * 30}>` to control entry/exit.

### Step 7 — Render
```bash
cd project-name
npm install
npm run render
# Output: out/overlay-greenbg.mp4
```

### Step 8 — Hand off to CapCut
Tell the user:
1. Drop the `-greenbg.mp4` on the TOP track in CapCut
2. Cutout → Chroma key → pick the green pixel → strength 100, shadow 30
3. The black panels and text survive; green pixels become transparent
4. HeyGen avatar + b-roll show through underneath
5. At HERO trigger, drop music to silence for 1.5s then fade back in

---

## Output file naming

| Format | Filename |
|---|---|
| Long-form 16:9 | `<topic>-overlay-greenbg.mp4` |
| Short-form 9:16 | `<topic>-shortform-overlay-greenbg.mp4` |

Example: `tech-layoff-overlay-greenbg.mp4`, `tech-layoff-shortform-overlay-greenbg.mp4`

The `-greenbg` suffix is mandatory. It tells everyone downstream "this is chroma-key, not Screen blend."

---

## Pacing rules (locked)

- Graphics appear **only on beats**, not constantly on screen
- Default hold: **3–5 seconds**
- HERO hold: **5–7 seconds** — never cut early, music drops to silence
- Between graphics: pure green = pure transparency in CapCut (avatar shows through cleanly)
- Animations: opacity fade-in over 8–12 frames, optional 95→100% scale. NO bouncy springs, NO swooshes
- Never stack 2+ graphics simultaneously unless intentional (compare card counts as 1)

---

## What this skill does NOT handle

- ❌ HeyGen avatar generation → use `heygen-video`
- ❌ B-roll generation → use `higgsfield-video`
- ❌ Video script writing → use `content-creation-engine`
- ❌ Generic Remotion projects (non-Watts brand) → use `remotion-video`
- ❌ Final CapCut assembly (the user does this manually with the chroma key step)
- ❌ Audio rendering → ElevenLabs, run by the user

This skill is purely the OVERLAY layer. It pairs with the others.

---

## After running this skill

After scaffolding/rendering, if the user has confirmed it works, proactively trigger `github-skill-sync` to back up any tweaks made to the skill itself (not the project — just the skill folder if it was modified).

---

## References

- `references/brand-tokens.md` — Colors, fonts, the HERO ONLY rule (green-screen templates)
- `references/graphic-templates.md` — Specs for all 5 green-screen templates with measurements
- `references/capcut-workflow.md` — Chroma key assembly guide for CapCut
- `references/standing-rules.md` — Graeham's locked production rules
- `references/3d-title-card.md` — **3D Title Card mode** — type system, gold-chrome material, animation, render workflow

## Assets (ready to copy into projects)

- `assets/brand.ts` — TypeScript brand tokens (paste into `src/lib/brand.ts`)
- `assets/timings-template.ts` — Frame timings template (paste into `src/lib/timings.ts`)
- `assets/components/*.tsx` — Pre-built React components for the 5 green-screen templates
- `assets/3d-title-project/` — **Complete Remotion + Three.js project for the 3D Title Card.** Copy out, `npm install`, render. Includes pre-converted typeface JSON fonts in `public/` and auto-detecting render scripts.
