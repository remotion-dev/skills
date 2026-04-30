# Email / HTML Output Branding Reference — Graeham Watts

This is the brand specification for any HTML output the offer-analyzer skill generates. The HTML output is designed to be opened as a hosted GitHub Pages link — NOT pasted into Gmail as a 600px-wide email body. It must match the visual system used in CMA reports so sellers see consistent branding across all listing assets.

## Color Palette (use these exact hex values)

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Primary Black | Near-black | `#1A1A1A` | Cover header bg, section bars, footer, recommendation box, net sheet header rows |
| Primary Gold | Warm gold | `#C5A55A` | Accents, borders, headline text on dark bg, top badges, rule lines |
| White | White | `#FFFFFF` | Content backgrounds, card bg |
| Light Gold / Cream | Cream | `#F5EFDC` | Secondary badge bg, intro callout bg, recommendation paragraph text |
| Dark Gold | Deep gold | `#A88B3D` | Est-Net-to-Seller emphasis, secondary accent |
| Light Gray (rows) | `#F0F0F0` | Alternating table rows |
| Page bg | `#FAFAFA` | Outer page background outside the white container |
| Amber bg | `#FEF3C7` | "Worth discussing" pill background |
| Amber text | `#92400E` | "Worth discussing" pill text |
| Debit Red | `#B91C1C` | Net sheet debit amounts only |

**DO NOT USE:** `#0d9488` (teal), `#1e293b` (navy), `#1e3a5f` (steel blue), or any generic email-blue. Those are NOT the Graeham Watts brand.

## Typography

- Family: **Inter** (Google Fonts) at weights 400, 500, 600, 700, 800
- Import: `<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">`
- Fallback stack: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- Brand wordmark "GRAEHAM WATTS" → 28px, weight 800, letter-spacing 0.18em, ALL CAPS
- "R E A L T O R" subtitle → 11px, letter-spacing 0.4em
- Section headers → 13px, weight 700, UPPERCASE, letter-spacing 0.2em
- Body → 14-15px, weight 400, line-height 1.55-1.7
- Pills/badges → 10-11px, weight 700, UPPERCASE, letter-spacing 0.05em

## Site Nav Bar (sticky top — matches CMA reports)

Every HTML output starts with a sticky nav bar identical to CMA reports.

```html
<nav class="site-nav">
  <a href="https://www.graehamwatts.com/" target="_blank">
    <img class="logo-img"
         src="https://images.leadconnectorhq.com/image/f_webp/q_80/r_1200/u_https://assets.cdn.filesafe.space/6wuU3haUH7uNeT20E3UZ/media/691256870b647e40e3c2e105.png"
         alt="Graeham Watts">
  </a>
  <div class="nav-links">
    <a href="https://www.graehamwatts.com/">Home</a>
    <a href="https://www.graehamwatts.com/buy">Buy</a>
    <a href="https://www.graehamwatts.com/sell">Sell</a>
    <a href="https://www.graehamwatts.com/buying-in-the-bay">Buying in the Bay</a>
    <a href="https://www.graehamwatts.com/the-bay-market">The Bay Market</a>
    <a href="https://www.graehamwatts.com/blogs">Blog</a>
    <a href="https://www.graehamwatts.com/about">About</a>
    <a href="https://www.graehamwatts.com/contact">Contact</a>
  </div>
</nav>
```

CSS:
```css
.site-nav {
  background: #343955;
  height: 72px;
  display: flex;
  align-items: center;
  padding: 0 32px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}
.site-nav .logo-img { height: 44px; width: auto; }
.site-nav .nav-links { margin-left: auto; display: flex; gap: 22px; align-items: center; }
.site-nav .nav-links a {
  color: #ffffff;
  font-size: 13px;
  font-weight: 500;
  text-decoration: none;
  letter-spacing: 0.02em;
  transition: opacity 0.2s;
}
.site-nav .nav-links a:hover { opacity: 0.7; }
@media (max-width: 880px) { .site-nav .nav-links { display: none; } }
```

## Cover Header (CMA-style)

```css
.cover {
  background: #1A1A1A;
  color: #FFFFFF;
  padding: 56px 48px 48px;
  text-align: center;
  border-bottom: 4px solid #C5A55A;
}
```

Content order inside `.cover`:
1. "GRAEHAM WATTS" wordmark (gold, 28px, weight 800, letter-spacing 0.18em)
2. "R E A L T O R" (gold, 11px, letter-spacing 0.4em)
3. Gold horizontal rule (80px × 2px, gold)
4. Report type tag — for offer comparisons this is "OFFER COMPARISON" (14px, gold, letter-spacing 0.25em, weight 600)
5. Property address as h1 (38px, weight 700, white)
6. City, State, Zip subhead (18px, light gray `#cccccc`)
7. Meta line: "X OFFERS RECEIVED · PREPARED [DATE] · LISTED AT $X,XXX,XXX" (13px, gray, with gold "X OFFERS RECEIVED" emphasis)
8. Bottom contact strip separated by gold-tinted top border: "INTERO REAL ESTATE SERVICES | DRE #01466876 | 650-308-4727" (11px gold, letter-spacing 0.08em)

## Layout Width

**Full-width — NOT 600px or 720px email-style centering.**

```css
.page { background: #FAFAFA; padding: 0; }
.container {
  max-width: 1320px;
  margin: 0 auto;
  padding: 48px 48px;
  background: #FFFFFF;
}
@media (max-width: 768px) { .container { padding: 32px 20px; } }
```

The cover and footer span the full browser width. The white inner container is 1320px max with the gray page background visible on either side at very wide viewports.

## Section Header Bars

```css
.section-header {
  background: #1A1A1A;
  color: #C5A55A;
  padding: 14px 24px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  margin: 40px 0 28px;
  border-left: 4px solid #C5A55A;
}
```

## Pills / Badges

| Class | Background | Text | Use case |
|-------|-----------|------|----------|
| `pill-gold` / `badge-gold` | `#C5A55A` | `#1A1A1A` | Top positives — "Waived", "Highest Net", "All Cash" |
| `pill-cream` / `badge-cream` | `#F5EFDC` (1px gold border) | `#A88B3D` or `#1A1A1A` | Secondary positives — "Fastest Close", short contingency, "None" |
| `pill-amber` / `badge-amber` | `#FEF3C7` | `#92400E` | Worth discussing — long contingencies, low down %, "Active Loan Cont." |
| `pill-gray` / `badge-gray` | `#F0F0F0` | `#555555` | Neutral — standard timelines |

Common pill style: `border-radius: 9999px; padding: 4px 11px; font-size: 10.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;`

## Offer Cards

- White bg, 1px `#E5E5E5` border, border-radius 8px, padding 28px 24px
- Hover: `translateY(-2px)` + soft shadow
- Rank badge: 36px circle, black bg with gold text (#1 inverts to gold/black with a "RECOMMENDED" pinned tag)
- The #1 card gets `border: 2px solid #C5A55A` and `box-shadow: 0 4px 16px rgba(197,165,90,0.18)`
- Price: 32px, weight 800, black, letter-spacing -0.02em
- "Est. Net to Seller: $X" underneath: 13px, color `#A88B3D`, weight 600

## Net Sheet Table (Side-by-Side, NOT Tabbed)

For multi-offer analyses, build a SINGLE side-by-side comparison table — line items as rows, offers as columns. **No tabs.** Sellers want to compare at a glance.

```html
<div class="net-sheet-wrapper">
  <table class="net-sheet-table">
    <thead>
      <tr>
        <th>Line Item</th>
        <th class="recommended">
          <span class="buyer-name">Krishnan</span>
          <span class="price-tag">$1,125,000 · #1</span>
        </th>
        <th><span class="buyer-name">Ortega</span><span class="price-tag">$1,100,000 · #2</span></th>
        <th><span class="buyer-name">Oakwood</span><span class="price-tag">$926,000 · #3</span></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Sale Price</strong></td>
        <td class="recommended-col"><strong>$1,125,000</strong></td>
        <td><strong>$1,100,000</strong></td>
        <td><strong>$926,000</strong></td>
      </tr>
      <tr class="section"><td colspan="4">Debits</td></tr>
      <!-- one row per debit line item; debit amounts get class="debit" -->
      <tr><td>Listing Commission (2.5%)</td>
          <td class="debit recommended-col">($28,125)</td>
          <td class="debit">($27,500)</td>
          <td class="debit">($23,150)</td></tr>
      <!-- ... etc ... -->
    </tbody>
    <tfoot>
      <tr>
        <td>Estimated Net to Seller</td>
        <td class="recommended-col">$1,049,025</td>
        <td>$1,025,695</td>
        <td>$886,468</td>
      </tr>
    </tfoot>
  </table>
</div>
```

Key CSS rules:
- `.net-sheet-wrapper` → `overflow-x: auto` so the table scrolls horizontally on mobile
- Header row: black bg + gold text; the recommended column header inverts to gold bg + black text
- `.recommended-col` cells get a subtle cream tint (`#FFFBEF`) background so the #1 column visually stands out
- `.section` row (Debits divider): cream bg (`#F0EBD8`), black uppercase text, 2px gold top + 1px gold bottom border
- `.debit` cells: red text (`#B91C1C`) with parentheses
- `.zero` cells: gray text (`#999999`)
- Footer row: black bg + gold text by default; recommended column gets solid gold bg + black text
- Body row striping: alternating `#FAFAFA` for visual separation

For single-offer analyses, use a simple vertical table instead — item label on left, amount on right, no comparison column needed.

## Recommendation Box

```css
.rec-box {
  background: #1A1A1A;
  color: #FFFFFF;
  padding: 32px 36px;
  border-radius: 8px;
  border-left: 6px solid #C5A55A;
}
.rec-box .rec-label { color: #C5A55A; text-transform: uppercase; letter-spacing: 0.2em; font-weight: 800; }
.rec-box p { color: #F5EFDC; line-height: 1.7; }
.rec-box strong { color: #C5A55A; }
```

## Footer

- Background `#1A1A1A`, padding 36px 48px, text-align center
- Wordmark "GRAEHAM WATTS" in gold, 14px, weight 700, letter-spacing 0.15em
- Contact line: "Intero Real Estate Services | DRE #01466876 | 650-308-4727 | graehamwatts@gmail.com" in light gray
- Disclaimer block (max-width 720px, centered, 10.5px, color `#666666`, separated by 1px `#333333` top border)

## Mobile Behavior

- Site nav hides nav links below 880px (logo stays)
- Offer cards stack vertically below 880px
- Cover padding reduces to 40px 24px below 600px
- h1 reduces to 26px below 600px
- Container padding reduces to 32px 20px below 768px

## Quality Check Before Publishing

Before pushing to GitHub Pages, verify:
1. Cover header uses gold/black, NOT teal/navy
2. There is a sticky site nav at the very top
3. Layout goes full browser width (no 600/720px email-style centering)
4. Inter font is loaded
5. The #1 ranked card has the gold border and "RECOMMENDED" tag
6. Net sheet "ESTIMATED NET TO SELLER" row is black bg with gold text
7. Footer matches CMA brand
