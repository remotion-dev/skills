# Title / Hero Card Typography & Spacing (LOCKED)

> Graeham locked this spec on 2026-06-03 after the "Last 47 Days" build. Use it as the default for any title card, hero card, or end card going forward unless he explicitly asks for something different.

---

## The reference (what we shipped)

The Scene 8 title card on "The Last 47 Days." Two-stanza fade-in structure on deep matte black:

> **Stanza 1 (the hook):**
> *Selling your home is*  
> *the highest-stakes story*  
> *you'll ever live.*
>
> **Stanza 2 (the promise):**
> *I make sure it ends*  
> *the way you wanted.*

---

## Locked specs

### Background
- **Color:** deep matte black (not pure #000 — slightly textured, around #0a0a0a with subtle film grain)
- **Texture:** subtle film grain overlay across the full frame
- **No gradients, no shapes, no logo on the title card itself** (logo goes on a separate brand card after)

### Typography
- **Font family:** elegant classic serif (Playfair Display, Cormorant, EB Garamond, or similar weight/style)
- **Weight:** Regular or Medium (NOT Bold — Bold reads cheap on a hero card)
- **Color:** white (#FFFFFF) for stanza 1, slightly softer (~#E8E8E8 or 90% opacity) for stanza 2 — gives a subtle hierarchy without making stanza 2 feel less important
- **Letter spacing:** slightly loose (+10 to +20 thousandths of an em)
- **Line height:** comfortable — around 1.3–1.4× the type size

### Layout
- **Vertical position:** centered vertically with a slight upward bias (text occupies roughly the 35–65% vertical range, not dead-center)
- **Horizontal:** centered, with generous left and right margin — text spans roughly the **center 60–70%** of the frame width, never edge-to-edge
- **9:16 vertical aspect:** stanza 1 sits around 38% from top, stanza 2 sits around 55% from top (a comfortable gap of ~1 full line height between stanzas)
- **16:9 horizontal aspect (if used):** stanzas centered vertically with the same horizontal margin treatment

### Line breaks
- Break **at meaningful phrasing pauses**, not at a fixed character count
- Each stanza wants 2–3 lines, never more than 3
- The break should *feel* like a breath, not a wrap

### Stanza spacing
- Gap between stanza 1 and stanza 2 ≈ 1 full line height
- Visual rhythm should let the reader finish stanza 1 before stanza 2 enters

### Animation (for video)
1. **Fade in stanza 1** (~0.5s ease-in), hold 2s
2. **Fade in stanza 2 below stanza 1** (~0.5s ease-in), hold 1s
3. **Cross-dissolve to brand card** (final logo + name + license + URL) — separate card, simpler treatment

---

## Brand card (separate card after the title card)

If the title card flows into a brand identification card (e.g., "GRAEHAM WATTS / Intero Real Estate / DRE# 01466876 / graehamwatts.com"):

- Same deep matte black background, same grain
- "GRAEHAM WATTS" in elegant sans-serif (NOT serif — visual differentiation from the title card)
- Larger weight than the title card serif (Medium/Semi-bold acceptable here)
- Below that, smaller text for the license + URL — light gray (#9A9A9A), thin weight
- Hold for 1 second, then fade to black

---

## What NOT to do (anti-pattern checklist)

- ❌ Bold the serif → looks cheap, breaks the elegance
- ❌ Pure black background (#000) → flat and digital, missing the texture
- ❌ All-caps the tagline → too aggressive for a contemplative trailer
- ❌ Center the text dead-center vertically → makes it feel static
- ❌ Edge-to-edge horizontal text → cramped, no breathing room
- ❌ Hard-break lines at arbitrary widths → makes the cadence wrong
- ❌ Equal weight on both stanzas → no hierarchy, reads as one block

---

## Implementation notes

**If PAI generates the title card:** PAI's title card output (from Raw mode prompt) already lands close to these specs. Don't apply color grade to it. Hand-tune in post if PAI's wrap is wrong — break the stanza into stanzas with manual hard breaks in the prompt.

**If hand-crafting in DaVinci/CapCut/After Effects:** match the specs above. The font is the most important variable — Playfair Display or Cormorant are the safest defaults.

**PAI prompt template that produces this layout:**

```
Pure cinematic title card on a deep matte black background with subtle film grain. Fade in white elegant serif text, centered vertically, comfortable left and right margin: '[STANZA 1 LINE 1] / [STANZA 1 LINE 2] / [STANZA 1 LINE 3].' Hold for 2 seconds. Fade in a second line below in slightly softer white serif text with same margin: '[STANZA 2 LINE 1] / [STANZA 2 LINE 2].' Hold for 1 second. Cross-dissolve to a final brand card on deep matte black: '[BRAND NAME]' in elegant sans-serif at top, then below in smaller lighter-weight text '[LICENSE]' then '[URL].' Hold for 1 second then fade to black. Visual style: cinematic, restrained, premium. No moving elements except text fades. Generate a video clip, use Raw mode for literal interpretation.
```

Use this template verbatim for any future title card unless Graeham explicitly changes the brief.
