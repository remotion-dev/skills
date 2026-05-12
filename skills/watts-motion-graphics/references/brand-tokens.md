# Brand Tokens — Watts Motion Graphics

These are the locked tokens for the Watts brand on overlay graphics. Do not change without approval. The corresponding TypeScript file is at `assets/brand.ts` (copy into project's `src/lib/brand.ts`).

## Colors

| Token | Hex | Use |
|---|---|---|
| Watts Navy | `#0A1F44` | Reserved (not used in overlays — used elsewhere in brand system) |
| **Watts Gold** | **`#B8945A`** | **HERO BEAT ONLY** — the single most important moment of the video |
| General Accent | `#C4A265` | All other gold accents — top borders, separators, arrows, option labels, scene titles |
| Watts White | `#FFFFFF` | Primary numbers and main labels |
| Panel Fill | `#000000` | All graphic boxes (solid black) |
| Body Text | `rgba(255,255,255,0.85)` | Soft white for body copy on black panels |
| Background | `#00FF00` | Pure chroma green — the entire canvas |

## The HERO ONLY rule

`#B8945A` is reserved for the climax moment of each video. **One HERO per video.** This is the color the viewer associates with the punch line — protect it.

Examples of valid HERO uses:
- The word "TAX-FREE" floating massive in Section 5 of the layoff video
- A final dollar amount that resolves the entire framework
- A single phrase that delivers the contrarian payoff

Examples of WRONG uses (use General Accent `#C4A265` instead):
- Top border on a stat card
- Right-column option labels in a decision framework
- Scene title text
- Lower third top stroke
- Arrow separators

If unsure: use General Accent. HERO is sacred.

## Typography

| Role | Font | Weight | Size | Notes |
|---|---|---|---|---|
| HERO reveal | **Syne** | Bold (700) | 220–280pt | Free-floating, no panel |
| Scene titles | **Syne** | Bold (700) | 48–64pt | Uppercase |
| Option labels (HELOC, STRATEGIC SALE) | **Syne** | Bold (700) | 36–44pt | Uppercase, General Accent color |
| Eyebrow labels (e.g., "GLOBAL LAYOFFS · META · APRIL 23") | **Inter** or **SF Pro Display** | Bold (700) | 10–12pt | Uppercase, letter-spacing 2px, General Accent or 60% white |
| Big numbers ($100K, +19%) | **Syne** or **Inter Bold** | 800–900 | 60–80pt | White for primary, gold for emphasis |
| Body copy | **Inter** or **SF Pro Display** | 400–500 | 22–28pt | White at 85% opacity, sentence case |

### Font fallbacks
If Syne is unavailable in the render environment:
1. First fallback: **Space Grotesk** (similar geometric editorial weight)
2. Second fallback: **Inter Bold** (loses some character but legible)
3. **Never substitute Helvetica or Arial** — they kill the editorial feel

If Inter is unavailable:
1. First fallback: **SF Pro Display**
2. Second fallback: **System sans-serif**

In Remotion, load fonts via `@remotion/google-fonts` or self-host woff2 files in `public/fonts/`.

## Spacing system

| Element | Padding |
|---|---|
| Inside small panels (stat callout) | 28px top/bottom, 36px left/right |
| Inside large panels (decision framework) | 28px between rows, 40px left/right |
| Between paired panels (compare card) | 36px gap on each side of `vs` |
| Border strokes | 2px (top accent, left accent, separators) |
| Corner radius | **0px** — sharp editorial corners only, NEVER rounded |

## Critical visual rules

- ✅ Sharp corners (0px radius) on all panels
- ✅ Thin 2px gold accent strokes on panel borders
- ✅ Generous padding inside panels — never cramped
- ✅ Letter-spacing 2px on eyebrow labels (tracked-out feel)
- ✅ All eyebrow labels UPPERCASE
- ✅ HERO text in Watts Gold #B8945A, all other gold in General Accent #C4A265
- ❌ NO drop shadows, NO glow, NO motion blur
- ❌ NO rounded corners — corners are square
- ❌ NO gradients on panels — solid black only
- ❌ NO bouncy spring animations — opacity fade only
- ❌ NO swoosh sound effects — clean editorial only
