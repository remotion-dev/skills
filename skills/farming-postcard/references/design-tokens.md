# Design Tokens — LOCKED Brand System

These tokens are NEVER negotiable per card. Continuity is the brand.

## Colors

| Token | Hex | CMYK (approx) | Use |
|---|---|---|---|
| Gold (primary) | `#C2A14E` | C:25 M:35 Y:75 K:5 | Border, headline highlights, CTA color, logo roof accent |
| Gold (deep) | `#A88638` | C:30 M:42 Y:85 K:15 | Gradient bottom of gold-box words |
| Gold (light) | `#EAD9A8` | C:8 M:15 Y:40 K:0 | Gradient top of gold-box words, light fills |
| Dark ink | `#1A1D2E` | C:80 M:75 Y:50 K:60 | Headlines, body text, logo |
| Cream | `#FBF7EC` | C:2 M:3 Y:10 K:0 | Back panel background |
| Pattern color | `#E6DABC` (~35% opacity) | n/a | Chevron house pattern overlay |
| White | `#FFFFFF` | 0,0,0,0 | Postcard background |

## Typography

| Use | Font | Weight | Size | Source |
|---|---|---|---|---|
| Front headline | Anton | Regular | 38pt | Google Fonts |
| Back headline | Anton | Regular | 26pt | Google Fonts |
| CTA line | Anton | Regular | 14pt | Google Fonts |
| Body | Inter | 400 (italic) | 10pt | Google Fonts |
| Sub / flip prompt | Inter | 600-800 | 14pt | Google Fonts |
| Contact info | Inter | 400/800 | 8-11pt | Google Fonts |
| Disclaimer | Inter | 400 | 6.5pt | Google Fonts |

**Headline rule:** Anton ONLY. Never substitute. Oswald is acceptable backup if Anton fails to load.

## Layout grid (6" × 4" postcard)

- **Gold left border:** 14px wide, full height, color `#C2A14E`, z-index 6
- **Chevron pattern:** SVG repeat, 80x40px tile, 0.35 stroke opacity, 0.55 layer opacity
- **Bleed:** 0.125" each side (total canvas 6.25" × 4.25")
- **Safe zone:** Keep type 0.25" from all edges minimum

## LOCKED Bottom Contact Block (NEVER edit)

This block appears identically on every card. Continuity is the brand signature.

```
[INTERO LOGO]
A Berkshire Hathaway Affiliate
[gold roof icon]
GRAEHAM WATTS

REALTOR®          650-308-4727
The Martin Team   graehamwatts@gmail.com
DRE #01466876     www.graehamwatts.com
```

**HTML structure (drop-in):**

```html
<div class="gw-logo">
  <div class="intero">INTERO</div>
  <div class="intero-sub">A Berkshire Hathaway Affiliate</div>
  <div class="roof"></div>
  <div class="name">GRAEHAM<br>WATTS</div>
</div>
<div class="contact">
  <div class="role">REALTOR®</div>
  <div>The Martin Team</div>
  <div>DRE #01466876</div>
  <div class="phone">650-308-4727</div>
  <div>graehamwatts@gmail.com</div>
  <div>www.graehamwatts.com</div>
</div>
```

## LOCKED Disclaimer (legal — never remove)

> "If your home is listed with another broker, please disregard this postcard. Homes not necessarily sold by this broker."

- Placement: Vertical text on right edge of BACK
- Size: 6.5pt Inter
- Color: `#555`
- Rotated -90°

## Gold-highlight treatments

Two variants only. Choose per word/phrase:

**Variant A — Solid gold box** (for short emphasized phrases on light background):
```css
background: linear-gradient(180deg, #EAD9A8 0%, #C2A14E 60%, #A88638 100%);
color: #fff;
padding: 0 6px;
text-shadow: 1px 1px 0 rgba(0,0,0,0.15);
```

**Variant B — Gold text fill** (for emphasized words inline with regular headline):
```css
background: linear-gradient(180deg, #EAD9A8, #C2A14E, #A88638);
-webkit-background-clip: text;
background-clip: text;
-webkit-text-fill-color: transparent;
```

**Variant C — Gold underline** (for action verbs):
```css
border-bottom: 4px solid #C2A14E;
padding-bottom: 2px;
```

## What's NEGOTIABLE per card

- Headline text + which words get gold highlight (1-3 max)
- Subline / flip prompt copy
- Back headline + body copy
- CTA line text
- QR target URL
- Headshot pose (pointing for front, smiling for back is the default but can flex)

## What's NEVER negotiable

- Color tokens above
- Font choices
- Bottom contact block
- Disclaimer text + placement
- Gold left border
- Chevron pattern background
- Aspect ratio (6×4 default — can scale to 6×9 for Corefact jumbo but proportions lock)
