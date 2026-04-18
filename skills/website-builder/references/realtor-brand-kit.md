# Graeham Watts Realtor Brand Kit

Locked brand system for everything shipped under the Graeham Watts / REALTOR identity — listings, CMAs, buyer guides, market reports, property landing pages, disclosure analyses.

This brand is CONFIRMED. Do not vary. Do not apply "creative aesthetic exploration" here — the brand is the asset. Variation breaks recognition.

Reference sheet: `assets/brand-kit/graeham-watts-realtor-brand-sheet.png`.

## Color palette

```css
:root {
  --gw-gold: #C5A55A;         /* primary brand — warm champagne gold */
  --gw-gold-dark: #A88B3D;    /* hover, underlines, secondary accents */
  --gw-black: #1A1A1A;        /* text, dark sections, footers */
  --gw-cream: #F5EFDC;        /* background tint, page wash */
  --gw-white: #FFFFFF;        /* surface */
}
```

When using the shared `:root` from `design-tokens.md`, map:

```css
--brand-primary: #C5A55A;
--brand-primary-hover: #A88B3D;
--brand-primary-light: #F5EFDC;
--brand-accent: #1A1A1A;
--ink: #1A1A1A;
--bg: #F5EFDC;      /* cream wash for editorial feel */
--surface: #FFFFFF;
```

For heavy-text pages (disclosure reports, long buyer guides), switch `--bg` to `#FFFFFF` and use cream only for section accent bars. Pure cream behind long text reduces readability.

## Typography

Header font: **Eagle CG Bold**. Paid font — license lives in Graeham's Intero account.

Body font: **SF Pro Display**. Free on Apple platforms. Web fallback stack:

```css
font-family: "SF Pro Display", -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif;
```

If Eagle CG Bold can't load (PDF generation, non-licensed context), fall back to:

```css
font-family: "Anton", "Libre Caslon Display", "Playfair Display", Georgia, serif;
```

Anton is free on Google Fonts and has similar geometric weight. Always set `letter-spacing: 0.04em` on Anton for realtor headers — Eagle CG has tighter natural spacing.

All realtor headers use UPPERCASE, always. Lowercase headers are off-brand.

```css
h1, h2, h3 { font-family: "Eagle CG Bold", "Anton", serif;
  text-transform: uppercase; letter-spacing: 0.02em;
  color: var(--gw-black);
}
```

## Logo treatment

Primary logo: "GRAEHAM WATTS" stacked with small house-and-heart icon. Tagline "R E A L T O R" (letter-spaced, 0.3em) sits below the name on the secondary lockup.

Three variations exist:
1. **Black-on-cream** — default for most surfaces (print, light backgrounds).
2. **Gold-on-black** — for dark section headers, hero bars.
3. **White-on-gold** — for accent panels, business-card reverse.

Never stretch. Never colorize with off-palette colors. Never rotate. Never place on low-contrast backgrounds (gold-on-cream is ILLEGAL — fails AAA contrast).

Clear space around the logo: minimum 1x the logo height on every side. More is better.

## Slogan / tagline

"YOUR HOME, OUR PASSION & COMMITMENT — THE EXPERIENCE YOU DESERVE"

Usage rules:
- Full slogan appears once per piece, usually in hero or footer.
- Short form "THE EXPERIENCE YOU DESERVE" can be used as a recurring accent on section headers or CTA buttons.
- Never paraphrase. It's the registered tagline.

## Contact footer (required on every realtor deliverable)

```html
<footer class="gw-footer">
  <div class="gw-logo-lockup">GRAEHAM WATTS<br><span>R E A L T O R</span></div>
  <div class="gw-contact">
    <div>graeham.watts@intero.com</div>
    <div>650-306-6727</div>
    <div>Intero Real Estate · DRE# 02015066</div>
  </div>
</footer>
```

```css
.gw-footer { background: var(--gw-black); color: var(--gw-white);
  padding: 32px 40px; display: flex; justify-content: space-between; align-items: center;
  font-family: "SF Pro Display", sans-serif; font-size: 13px;
}
.gw-logo-lockup { font-family: "Eagle CG Bold", "Anton", serif;
  font-size: 20px; letter-spacing: 0.04em; color: var(--gw-gold);
}
.gw-logo-lockup span { font-size: 10px; letter-spacing: 0.4em; color: var(--gw-cream); display: block; margin-top: 4px; }
```

DRE license number (02015066) must appear on every outbound marketing piece — legal requirement in California.

## Section rhythm / visual language

**Section headers:** Eagle CG Bold on cream or white, gold underline below.

```css
.gw-section-title { font-size: 32px; letter-spacing: 0.04em; color: var(--gw-black); margin-bottom: 4px; }
.gw-section-rule { width: 60px; height: 3px; background: var(--gw-gold); margin-bottom: 32px; }
```

**Gold bars** for navigation or emphasis:

```css
.gw-bar { height: 4px; background: var(--gw-gold); margin: 24px 0; }
```

**Price callouts:**

```css
.gw-price { font-family: "Eagle CG Bold", "Anton", serif;
  font-size: 48px; color: var(--gw-gold-dark); letter-spacing: 0.02em;
}
```

## PDF outputs (via ReportLab)

Realtor deliverables often render to PDF through `cma-generator`, `offer-analyzer`, and `disclosure-analyzer`. Those skills use ReportLab which can't load arbitrary fonts — the fallback stack there is:

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Eagle CG Bold bundled in the skill's fonts/ folder if available, else Anton
try:
    pdfmetrics.registerFont(TTFont('EagleCG', 'fonts/EagleCG-Bold.ttf'))
    HEADER_FONT = 'EagleCG'
except Exception:
    pdfmetrics.registerFont(TTFont('Anton', 'fonts/Anton-Regular.ttf'))
    HEADER_FONT = 'Anton'

BODY_FONT = 'Helvetica'  # SF Pro equivalent in ReportLab's default set
```

Colors as `HexColor('#C5A55A')` — don't use named colors.

## Voice

Concise, confident, data-first. Graeham writes like a pro who respects the client's time.

- "The best 3-bed in Redwood City under $1.6M right now." (Not: "Check out this lovely home!")
- "Inspection flagged three items. Two matter. I've drafted a credit request for $8,400." (Not: "Thought you'd want to know about the inspection findings.")
- Signs off with "— Graeham" (one em-dash, no "Best,", no "Cheers,").

## Do not

- Pair gold with cream text. Contrast fails.
- Use rounded logo or modify proportions.
- Use sparkles or emoji on realtor content. Off-brand.
- Use gradients on the gold. Flat only.
- Apply the brand to non-realtor work (PropertyOS, PropIQ). Those projects have their own identity.
