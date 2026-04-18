> **Canonical brand reference:** `../../website-builder/references/realtor-brand-kit.md`
>
> The website-builder skill holds the single source of truth for Graeham Watts realtor brand (palette, logo rules, voice, contact footer, tagline).
> This file adds only the **HTML-report-specific deltas** needed for off-market output: Google Fonts fallback stack (Montserrat + Inter), card shadow/border treatments, and the "estimated price around $X" framing language.
> When Graeham's brand changes, update website-builder first — then apply format-specific overrides here.

---

# Graeham Watts Branding — Off-Market Report

## Color Palette (exact hex values — don't improvise)

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Primary Black | Near-black | `#1A1A1A` | Header bar, footer bar, section dividers, body text on white |
| Primary Gold | Warm gold | `#C5A55A` | Headline accent, card borders/accents, price callout, rule lines |
| White | White | `#FFFFFF` | Page background, card background, text on dark areas |
| Light Gold | Cream | `#F5EFDC` | Subtle alternate-row background (rarely used in this report) |
| Dark Gold | Deep gold | `#A88B3D` | Hover / secondary accent |
| Medium Gray | Text gray | `#666666` | Captions, stat row separators, date line |
| Soft Gray | Border / shadow | `#E5E5E5` | Card drop-shadow base, subtle dividers |

## Typography (Google Fonts CDN — always link these)

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

| Use | Font | Weight | Transform |
|-----|------|--------|-----------|
| Main header ("GRAEHAM WATTS") | Montserrat | 800 | UPPERCASE, letter-spacing 0.3em |
| Subhead ("R E A L T O R") | Montserrat | 500 | UPPERCASE, letter-spacing 0.5em |
| Section title ("OFF-MARKET PROPERTIES — CITY") | Montserrat | 700 | UPPERCASE, letter-spacing 0.15em |
| Property address | Montserrat | 700 | Title Case |
| Price callout ("Estimated price around $X") | Montserrat | 700 | — |
| Stat row (beds/baths/sqft/lot/year) | Inter | 500 | — |
| Body paragraphs (intro, notes) | Inter | 400 | — |
| Footer contact line | Inter | 400 | small, medium gray |

## Header Block (top of every report)

Layout: full-width black bar `#1A1A1A`, gold text inside, generous vertical padding (48–64px top and bottom).

```
              GRAEHAM WATTS             ← gold #C5A55A, Montserrat 800, 42px, UPPERCASE, letter-spacing 0.3em
               R E A L T O R             ← gold, Montserrat 500, 14px, letter-spacing 0.5em
        ━━━━━━━━ thin gold rule ━━━━━━━━
    OFF-MARKET PROPERTIES — MENLO PARK    ← white, Montserrat 700, 22px
              April 16, 2026              ← medium gray #CCCCCC, Inter 400, 14px
```

## Intro Paragraph (sits on white, below header)

Always include this text (or a near-variant). Body copy in Inter 400, 16px, line-height 1.7, max-width ~680px, centered:

> "As part of our ongoing market research, we've identified the following properties that are not yet available to the general public. These off-market opportunities are exclusively available through agent networks."

## Property Card

```
┌────────────────────────────────────────┐
│                                        │
│        [ MAIN PROPERTY PHOTO ]         │   ← full-bleed inside card, 16:10 aspect
│                                        │
├────────────────────────────────────────┤
│                                        │
│   123 Main St, Menlo Park, CA 94025    │   ← Montserrat 700, 20px, #1A1A1A
│                                        │
│   3 Beds  •  2 Baths  •  1,850 SqFt    │   ← Inter 500, 14px, #666666
│      •  6,250 SqFt Lot  •  1962        │
│                                        │
│   ━━━━━━ thin gold rule ━━━━━━━━━━━━━━  │
│                                        │
│   Estimated price around $2,150,000    │   ← Montserrat 700, 22px, #C5A55A
│                                        │
│   [ thumb1 ] [ thumb2 ]                 │   ← optional, 80x60 each, rounded 4px
│                                        │
└────────────────────────────────────────┘
```

Card styling:
- Background: white `#FFFFFF`
- Border-radius: 8px
- Box-shadow: `0 4px 16px rgba(0,0,0,0.08)` + a 3px gold top border (`border-top: 3px solid #C5A55A`)
- Padding: 0 on the photo (full-bleed top), 28px inside the body
- Margin between cards: 32px vertical
- On desktop: two-column grid (`grid-template-columns: repeat(2, 1fr)`, gap 32px). On screens narrower than 900px collapse to one column.

## Footer (every visual page)

Full-width black bar `#1A1A1A`, 48px vertical padding, centered content, gold thin rule separating it from the content above.

```
       ━━━━━━━━━ thin gold rule ━━━━━━━━━
  Graeham Watts  |  Intero Real Estate  |  DRE #01466876
  650-308-4727  |  graehamwatts@gmail.com  |  www.graehamwatts.com
```

All pipe-separated. Text color: gold `#C5A55A` for Graeham's name, white `#FFFFFF` for the rest, Inter 400, 13px, letter-spacing 0.05em.

## Design Principles

- **Generous white space.** Never crowd cards. If you only have 3 cards, that's fine — give them room.
- **One hero color.** Gold is the only accent. Don't add blues, greens, reds.
- **Photography first.** The property photo is the most important element on the card. Let it be big.
- **Quiet type.** Use Montserrat only for headers/numbers. Body is Inter, small, relaxed line-height.
- **No MLS visual language.** No MLS logos, MLS numbers, "Courtesy of" language, broker remarks, or anything that screams "this is an MLS printout".
