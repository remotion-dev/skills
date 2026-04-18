# Typography

Typography is the single biggest tell for AI-generated UI. If the page opens in Inter or Roboto, a designer will spot it instantly.

## Default pairings (pick one per project)

| Aesthetic | Display (headers) | Body |
|---|---|---|
| Editorial / luxury | Playfair Display, Fraunces | Epilogue, Inter Tight |
| Tech / SaaS | Instrument Serif, Space Grotesk | Inter Tight, Manrope |
| Warm / earthy | Fraunces, Young Serif | Outfit, Plus Jakarta |
| Modern brutalist | Space Grotesk, Monument (paid) | Inter Tight, IBM Plex |
| Realtor — Graeham locked | Eagle CG Bold | SF Pro Display |

Default for PropIQ screens and most client projects is Playfair Display + Epilogue — that's what the current placeholder mockups use.

`Inter`, `Roboto`, `Arial`, `system-ui` are banned for headers. Body text in `Inter Tight` or `Manrope` is fine — they're the geometric-sans peers, not the defaults.

## Loading from Google Fonts

Always preconnect. Saves ~200ms on first paint.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Epilogue:wght@400;500;600;700&display=swap" rel="stylesheet">
```

Only load the weights you'll actually use — every extra weight is a network request. 400, 600, 700 cover 90% of real use.

## Size scale

Use a modular scale, not arbitrary px values.

```css
:root {
  --fs-xs: 12px;
  --fs-sm: 14px;
  --fs-base: 16px;
  --fs-md: 18px;
  --fs-lg: 22px;
  --fs-xl: 28px;
  --fs-2xl: 36px;
  --fs-3xl: 48px;
  --fs-4xl: 64px; /* hero */
  --fs-5xl: 88px; /* huge editorial hero */
}
```

For marketing heroes lean larger than feels comfortable — 64px min, 88px preferred on desktop. Timid hero sizes are the #1 tell of AI-generated marketing copy.

## Line height and tracking

Display text uses tight tracking and tight line-height. Body uses generous line-height.

```css
h1, h2, .display { font-family: var(--font-display); line-height: 1.05; letter-spacing: -0.02em; }
h3, h4 { font-family: var(--font-display); line-height: 1.15; letter-spacing: -0.01em; }
body, p { font-family: var(--font-body); line-height: 1.55; letter-spacing: 0; }
small, .caption { font-size: var(--fs-sm); line-height: 1.45; color: var(--ink-muted); }
```

## Weight hierarchy

Don't use more than 3 weights per page. A common clean pattern:

- Display headers: 600 or 700
- Body: 400
- UI labels / small caps: 500 with `letter-spacing: 0.08em` and `text-transform: uppercase`

Bold body text is lazy emphasis. Use color contrast (`--brand-primary`) or italic instead.

## Fluid sizing for heroes

Hero headlines should scale with viewport:

```css
.hero h1 {
  font-size: clamp(2.25rem, 5vw + 1rem, 5.5rem);
  line-height: 1.02;
  letter-spacing: -0.03em;
}
```

`clamp()` removes the need for breakpoints on headline sizing and prevents giant text overflowing on mobile.

## Measure (line length)

Body paragraphs should cap at 65 characters per line. Easy enforcement:

```css
.prose p { max-width: 62ch; }
```

Without this, body text stretches across full desktop width and becomes unreadable.

## Editorial touches that elevate cheap-looking pages

Drop cap on the first paragraph of a long-form section:

```css
.prose p:first-of-type::first-letter {
  font-family: var(--font-display);
  font-size: 4em; float: left; line-height: 0.9;
  margin: 0.1em 0.1em 0 0; color: var(--brand-primary);
}
```

Italic emphasis instead of bold in body copy. Reads as more literary and less like a sales page.

Numbered section headers in small caps (`01 · Research` / `02 · Build`) across a services or process page.

## Realtor brand override

When `references/realtor-brand-kit.md` is active, Eagle CG Bold replaces the display font and SF Pro Display replaces the body font. Eagle CG Bold is a paid font — if unavailable in the target environment, use `"Libre Caslon Display"` or `"Anton"` as a free fallback with similar visual weight.
