---
name: watts-motion-graphics
description: "Watts-brand motion-graphics overlay generator for Graeham's videos. Produces chroma-key-ready Remotion overlay projects that composite on top of HeyGen avatar + Higgsfield b-roll in CapCut. Use ANY time the user mentions: motion graphics, video graphics, overlay graphics, stat callout, compare card, decision framework graphic, HERO reveal, lower third, title card, end card, chroma key graphics, green screen graphics, Remotion overlay, graphics for CapCut, animated text reveal, big number graphic, side-by-side compare, framework card, or anything related to motion graphics layered on a HeyGen + b-roll video. Also trigger on 'motion graphic for that scene', 'animate that stat', 'do another motion graphic', or recreating visual style from a previous Watts video. CRITICAL: renders on pure green #00FF00, NOT black + Screen blend (Screen blend turns text translucent). Locks brand tokens, Syne Bold + Inter typography, and 5 templates (Stat Callout, Compare Card, Decision Framework, HERO Reveal, End Card)."
---

# Watts Motion Graphics — Chroma-Key Remotion Overlay

Generate motion-graphics overlay videos for Graeham Watts' real estate content. The output is a single MP4 rendered on **pure chroma green (`#00FF00`)** that gets keyed out in CapCut and composited on top of the HeyGen avatar layer + Higgsfield b-roll layer.

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

---

## Standard workflow

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

After scaffolding/rendering, if the user has confirmed it works and asks to back up any tweaks made to the skill itself, push to `Graehamwatts/skills` via the Composio publishing pattern (see `shared-references/publishing-via-composio.md`). Do NOT use `git push`.

---

## References

- `references/brand-tokens.md` — Colors, fonts, the HERO ONLY rule
- `references/graphic-templates.md` — Specs for all 5 templates with measurements
- `references/capcut-workflow.md` — Chroma key assembly guide for CapCut
- `references/standing-rules.md` — Graeham's locked production rules

## Assets (ready to copy into projects)

- `assets/brand.ts` — TypeScript brand tokens (paste into `src/lib/brand.ts`)
- `assets/timings-template.ts` — Frame timings template (paste into `src/lib/timings.ts`)
- `assets/components/*.tsx` — Pre-built React components for the 5 graphic templates
