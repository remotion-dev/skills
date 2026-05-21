# Watts 3D Title — two-line cursive + gold-chrome text

Renders a title card: a flat white cursive line on top, true 3D extruded
gold-chrome text below. Output is alpha-channel `.mov` (ProRes 4444) — drops
straight onto b-roll in CapCut desktop Pro, no green screen, no chroma key.

## What got delivered

| File | What it is |
|---|---|
| `watts-3d-title-landscape.mov` | 1920×1080, 4s, transparent. For 16:9 / YouTube. |
| `watts-3d-title-portrait.mov` | 1080×1920, 4s, transparent. For 9:16 / Reels. |
| `watts-3d-title-PREVIEW.mp4` | Flattened on black, viewable in any player. NOT for the edit — just to preview the motion. |

Current text: cursive "Bay Area Expert" / gold "GRAEHAM WATTS".

## How it works (the important parts)

- **The cursive line** is flat HTML text (Great Vibes font, bundled from npm so
  no network needed at render time). Layered on top of the 3D canvas.
- **The gold line** is real Three.js geometry — extruded letters with bevels,
  a metallic gold material, three-point studio lighting, and a procedural
  studio environment for reflections. It springs in and gently sways.
- **Auto-fit**: the gold text measures its own width from the font's glyph
  metrics, then scales to fit the frame. "SOLD" and "GRAEHAM WATTS" both fit
  correctly without anyone touching a size value. Short words are capped so
  they don't get huge.
- **Transparency**: `remotion.config.ts` sets PNG image format → the render
  carries a real alpha channel → ProRes 4444 preserves it.

## To make a new title

Edit `src/Root.tsx` — change `CURSIVE_LINE` and `GOLD_LINE`. That's the only
thing that changes. Everything else (look, lighting, motion, fit) stays locked.

Then render:
```bash
npm install            # first time only
npm run render:landscape
npm run render:portrait
```

Output lands in `out/`.

## Render environment note

Rendering needs a browser. This project is pinned to use the Chromium that
ships with the render environment via `--browser-executable=`. On the Mac
Studio, Remotion will find Chrome on its own — you can drop that flag, or
keep it if the path matches.

## Known-good versions

Remotion 4.0.461 · three 0.169 · @react-three/fiber 8.17 · @react-three/drei 9.114
· @remotion/three 4.0.461 · @fontsource/great-vibes 5.1
