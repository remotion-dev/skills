# Typography & Caption Spec — Editor Handoff

When Graeham's editor (or CapCut operator) burns captions into a Vaibhav-template video, they need to match this spec exactly. Copy-paste this file into the editor's handoff note.

## Fonts to install

Both are Google Fonts — free, no licensing issues.

| Font family | Download | Used for |
|---|---|---|
| **Playfair Display** | fonts.google.com/specimen/Playfair+Display | All primary subject and emphasis text |
| **DM Sans** | fonts.google.com/specimen/DM+Sans | Secondary text, section titles, list numbers |
| **Inter** | fonts.google.com/specimen/Inter | Burned-in dialogue captions (smaller, dense text) |

## Font weight + style reference

| Text type | Family | Weight | Style | Size @ 1080×1920 | Color |
|---|---|---|---|---|---|
| Primary subject | Playfair Display | 400 (Regular) | *Italic* | 80–96pt | `#FFFFFF` white |
| Emphasis word | Playfair Display | 400 | *Italic* | 80–96pt | `#FFFFFF` on highlight box |
| Secondary clause | DM Sans | 400 (Regular) | Normal | 40–48pt | `#FFFFFF` white |
| List number | DM Sans | 700 (Bold) | Normal | 72–88pt | `#BFFF00` acid green |
| Section title | DM Sans | 500 (Medium) | Normal, **letter-spacing +8%** | 44–52pt | `#FFFFFF` on faded background |
| Dialogue caption | Inter | 600 (Semi-bold) | Normal | 36–44pt | `#FFFFFF` on translucent dark pill |

**Pill spec for dialogue captions:** rounded rectangle, corner radius 12–16px, fill `#000000` at 60% opacity, 12px horizontal padding, 6px vertical padding, centered horizontally, bottom-third vertical anchor.

## Color palette

| Role | Hex | Notes |
|---|---|---|
| Primary text | `#FFFFFF` | All white; never tinted |
| Acid green highlight (numbers + emphasis) | `#BFFF00` | Saturated fluorescent green — this is the signature |
| Warm yellow highlight (occasional emphasis) | `#FFD700` | Use for 1 emphasis word per every 5–10 captions — sparse |
| Dark pill background | `#000000` @ 60% opacity | Never pure black at 100% — always translucent |
| Section wash red | `#FF3030` @ 30% opacity | Hard cut transition only |
| Section wash gold | `#D4A84B` @ 20% opacity | Gentle fade transition only |

**Acid green is the anchor.** Every list number uses it. 1–2 emphasis keywords per 10-second block get it as a highlight-box fill. Don't dilute the signal by using it elsewhere.

## Highlight box spec (for emphasis keywords)

When a keyword gets a color highlight:
- Box extends 4px beyond the text on all sides
- Corner radius 2px (almost sharp — not pill-shaped)
- Box fill: acid green `#BFFF00` @ 100% opacity (solid, not translucent)
- Text on top: **still white** (`#FFFFFF`) — high contrast against green
- Rule: only highlight nouns and verbs that carry meaning. Never articles, connectors, prepositions, or filler. If the keyword doesn't survive the "would this still mean something standalone?" test, it doesn't get a highlight.

## Caption placement zones

Divide the 1080×1920 portrait frame (or 16:9 landscape if unusual) into:

- **Top third (0–640px vertical):** primary subject captions (Mode 1 hook, Mode 5 section headers)
- **Middle third (640–1280px):** full-bleed talking-head emphasis (Mode 2)
- **Bottom third (1280–1920px):** dialogue captions, supporting clauses, Mode 4 card descriptors

**Never center a caption in the middle third if Graeham's face is there.** Captions avoid the face zone.

## Animation timing

- **Caption in:** fade + slight 10% scale-up, 150ms duration
- **Caption out:** fade, 100ms duration, overlaps with next caption's fade-in
- **Crossfades:** do NOT hold captions static more than 2 seconds — refresh them in sync with Graeham's speech beats
- **Emphasis highlight box:** appears 50ms AFTER the text word does (tiny delay reads as intentional)

## Caption writing rules

- Keep captions to 3–7 words per on-screen moment
- Break long sentences into 2–3 sequential captions, not one long overlay
- Match the spoken word EXACTLY — never paraphrase
- Capitalize proper nouns; sentence-case everything else
- NO emoji inside captions (emoji is a separate layer, see below)

## Emoji pop-ins (separate layer)

Vaibhav uses emoji as small animated accents, not inside captions. They appear:
- Off to one side of the primary caption
- Scale in with a bounce (keyframed: 0% → 120% → 100%, ~250ms)
- Stay on screen 800ms–1.2s
- Scale out with a smaller bounce back to 0%

**Common picks by content type:**
- Money / closing: 💰 🏠 ✅
- Market / data: 📈 📊 📉
- Neighborhood: 📍 🌉 (Bay)
- Analysis / explanation: 🤔 💡 👉
- Hot take: 🔥 💀 (use sparingly)

One emoji per on-screen caption moment. More than that = noise.

## Example caption sheet (deliverable format)

This is what the `vaibhav-template` skill outputs for the editor. Drop it into the shot plan table and the editor burns captions accordingly.

```
Time (s)    Caption text                        Font + style                           Highlight       Placement        Emoji
0.0–1.2     Sam Altman                          Playfair Display Italic 88pt white     —               top third        —
1.2–2.5     just killed the entire              DM Sans Regular 44pt white             —               top third        —
2.5–3.8     Image Gen                           Playfair Display Italic 88pt white     on "Image Gen"  center frame     🔥 (left side, 2.8–3.5s)
                                                                                        BFFF00 box
3.8–5.0     Industry with one big launch        DM Sans Regular 44pt white             —               center frame     —
5.0–6.5     01. PRECISE TEXT                    DM Sans Bold 80pt acid green (#BFFF00) —               top third        —
                                                 + Medium letter-spaced 8%
6.5–8.0     [dialogue caption]                  Inter Semi-bold 40pt white on dark pill —              bottom third     —
```

This format maps 1:1 to CapCut's text layer timeline — the editor just copies the row values into the layer properties.

## What this spec does NOT cover

- Music selection / audio design — separate pass
- Transitions between Modes 1–5 — Graeham has editor freedom on cut style (hard cut, whip pan, zoom blur) as long as rhythm pacing is respected
- Color grading LUT — the "warm face + cool background" is lit at capture time (the Higgsfield generation handles it) — post-grade only adjusts contrast and saturation

## Source of truth

If this file and SKILL.md disagree on any spec, **SKILL.md wins** — it's the higher-level document. This file is the editor-handoff translation of the SKILL.md rules, not a separate authority.
