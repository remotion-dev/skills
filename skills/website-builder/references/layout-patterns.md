# Layout Patterns

Page-level structure. Nav, hero, section rhythms, footer. Pulled from what actually ships on Graeham's PropIQ pages plus common marketing-site patterns.

## Page shell

```css
body { background: var(--bg); color: var(--ink); font-family: var(--font-body);
  margin: 0; min-height: 100vh; -webkit-font-smoothing: antialiased;
}
.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
.container-narrow { max-width: 800px; }
.container-wide { max-width: 1400px; }
section { padding: 96px 0; }
section.compact { padding: 64px 0; }
section.tall { padding: 140px 0; }
```

96px vertical section padding on desktop is the minimum that reads as "breathing room". AI-generated pages default to 48px or 64px and feel cramped.

## Nav variations

Pick one — don't mix.

**Sticky glass nav** (default for most sites). See `assets/snippets/nav-glassmorphism.html`.

**Floating pill nav** — rounded-pill container centered in the viewport, floats over content. Great for editorial / luxury sites.

```css
.nav-pill { position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
  z-index: 50; background: rgba(255,255,255,.7); backdrop-filter: blur(16px);
  border: 1px solid rgba(0,0,0,.06); border-radius: var(--radius-pill);
  padding: 10px 20px; display: flex; align-items: center; gap: 24px;
  box-shadow: var(--shadow-md);
}
```

**Edge-to-edge static nav** — spans viewport, bottom border, no backdrop. Feels more "app" than marketing. Good for dashboards.

## Hero variations

**Editorial hero** — centered or left-aligned display headline, one-sentence subhead, two buttons. Large type. Minimal visual content beside the type. See `assets/snippets/hero-editorial.html`.

**Split hero** — headline + copy on left column, product screenshot or illustration on right. Most common marketing-SaaS pattern.

```css
.hero-split { display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center; padding: 120px 0 80px; }
@media (max-width: 960px) { .hero-split { grid-template-columns: 1fr; gap: 40px; padding: 80px 0 60px; } }
.hero-split .copy h1 { font-size: clamp(2.5rem, 5vw, 4rem); line-height: 1.05; letter-spacing: -0.02em; margin-bottom: 20px; }
.hero-split .copy p.lead { font-size: var(--fs-md); color: var(--ink-muted); max-width: 52ch; margin-bottom: 32px; }
.hero-split .visual { aspect-ratio: 4/3; border-radius: var(--radius-lg); background: linear-gradient(135deg, var(--brand-primary-light), var(--brand-primary) 240%); overflow: hidden; }
```

**Full-bleed hero** — background image or gradient covers the entire viewport, text layered on top. Reserve for landing pages with a strong hero image (property listing site, event page).

## Feature grid

Three columns is the default but four is better for dashboards. Avoid six — reads as "feature dump".

```css
.feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; }
@media (max-width: 900px) { .feature-grid { grid-template-columns: 1fr; } }
.feature { display: flex; flex-direction: column; gap: 12px; }
.feature-icon { width: 48px; height: 48px; display: grid; place-items: center;
  background: var(--brand-primary-light); color: var(--brand-primary);
  border-radius: var(--radius-md); margin-bottom: 4px;
}
.feature h3 { font-size: var(--fs-lg); line-height: 1.2; margin: 0; }
.feature p { font-size: var(--fs-base); color: var(--ink-muted); line-height: 1.5; margin: 0; }
```

Icons must be inline SVG or a real icon font (Lucide, Heroicons) — never emoji. See `component-patterns.md`.

## Bento grid

Variable-size grid. Non-uniform tiles. More visual interest than a flat 3x3.

```css
.bento { display: grid; grid-template-columns: repeat(4, 1fr); grid-auto-rows: 200px; gap: 16px; }
.bento > .cell { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 20px; }
.bento .cell-wide { grid-column: span 2; }
.bento .cell-tall { grid-row: span 2; }
.bento .cell-big { grid-column: span 2; grid-row: span 2; }
```

Use bento when you want to mix heavy and light content — one large product visual, three supporting text cells, two stat tiles. Works well on product homepages.

## Section rhythm

Alternate backgrounds to signal section breaks:

```css
section.alt { background: var(--surface); }
section.dark { background: var(--ink); color: #fff; }
section.dark h1, section.dark h2, section.dark h3 { color: #fff; }
```

Rhythm: `hero (bg) → features (surface) → stats (dark) → testimonials (bg) → CTA (surface) → footer`. Avoids a single flat scroll.

## Footer

Default footer: two or three columns of links, one column with logo + small description. Never stuff an email signup into the footer alongside nav links — give it its own full-width strip above the footer.

```html
<footer class="footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <h3>Graeham Watts</h3>
      <p>REALTOR · DRE# 01466876 · Intero Real Estate</p>
      <p class="muted">Built for the Peninsula.</p>
    </div>
    <div><h4>Work with me</h4><ul>...</ul></div>
    <div><h4>Market</h4><ul>...</ul></div>
    <div><h4>About</h4><ul>...</ul></div>
  </div>
  <div class="footer-legal container">
    <span>© 2026 Graeham Watts. All rights reserved.</span>
    <span>Equal Housing Opportunity.</span>
  </div>
</footer>
```

## Social proof strip

A row of muted logos between hero and features is the highest-ROI marketing element. Grayscale at 60% opacity.

```css
.logo-row { display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 40px; filter: grayscale(1); opacity: 0.6; padding: 32px 0; }
.logo-row img { height: 28px; width: auto; }
```

## Anti-patterns

Full-page centered column with everything stacked vertically. It's the AI default and instantly recognizable. Break the rhythm: one left-aligned section, one right-aligned pull quote, one full-bleed.

Three identical cards in a row with no variation. If you use the feature grid, vary icon color or add one highlighted card.

Stacked heroes across 3+ scroll heights. One hero, then move to content.
