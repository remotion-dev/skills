# PropIQ / PropertyOS — Placeholder Tokens

**These are placeholders.** Graeham has NOT locked a brand for PropIQ or PropertyOS yet. The tokens below are what the current UI mockups use. Treat them as "consistent across the current build" — not as "the brand".

When Graeham chooses a final PropIQ brand, update this file and run `scripts/brand-swap.py` to cascade the change across all PropIQ screens.

## Current placeholder palette (Deep Slate)

```css
:root {
  /* Primary — Deep Slate (placeholder) */
  --p: #1a2744;         /* primary */
  --pl: #e8ecf5;        /* primary light, bg tint */
  --pm: #111d33;        /* primary dark, hover */
  --pa: #2d4278;        /* primary accent, secondary buttons, links */

  /* Status colors (stable — keep across brand changes) */
  --am: #BA7517;  --aml: #FAEEDA;  /* amber */
  --re: #C0392B;  --rel: #FDF0F0;  /* red */
  --b:  #185FA5;  --bl:  #E6F1FB;  /* blue */
  --pu: #534AB7;  --pul: #EEEDFE;  /* purple */

  /* ARES / secondary experience accent */
  --ar: #1E3A5F;  --aa: #2563EB;  --arl: #E8F0FA;

  /* Neutrals */
  --ink: #111827;
  --mu: #6B7280;
  --fa: #9CA3AF;
  --bg: #F8F7F4;
  --sf: #FFFFFF;
  --bo: #E5E3DE;
  --b2: #D1CFC9;
}
```

If you're also loading the baseline `design-tokens.md` block, these map across:

```css
--brand-primary: #1a2744;
--brand-primary-hover: #111d33;
--brand-primary-light: #e8ecf5;
--brand-accent: #2d4278;
```

## Typography (placeholder)

- Display / headers: **Playfair Display** (400, 600, 700)
- Body: **Epilogue** (400, 500, 600, 700)

Earlier mockups used Instrument Serif + Inter. Don't use those — the current canonical stack is Playfair + Epilogue.

Load block:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Epilogue:wght@400;500;600;700&display=swap" rel="stylesheet">
```

## PropIQ components you'll see repeatedly

**"Today card"** — large gradient tile at top of dashboard with greeting + current KPI headline.

```css
.today {
  border-radius: 16px; padding: 24px 28px; color: #fff;
  background: linear-gradient(135deg, var(--p) 0%, var(--pa) 100%);
  box-shadow: 0 8px 24px rgba(26, 39, 68, 0.25);
}
```

**Sidebar nav** — fixed-left dark vertical nav for dashboard views.

```css
.sidebar { width: 240px; background: var(--p); color: rgba(255,255,255,.8);
  padding: 20px 0; position: fixed; left: 0; top: 0; bottom: 0; overflow-y: auto;
}
.sidebar .nav-item { padding: 10px 20px; display: flex; align-items: center; gap: 12px;
  font-size: 14px; font-weight: 500; border-left: 3px solid transparent;
}
.sidebar .nav-item:hover { background: var(--pm); color: #fff; }
.sidebar .nav-item.active { background: var(--pm); color: #fff; border-left-color: var(--am); }
```

**Top tab bar** — secondary nav inside the main pane.

```css
.tabs { display: flex; gap: 24px; border-bottom: 1px solid var(--bo); padding: 0 24px; }
.tab { padding: 14px 0; font-size: 14px; font-weight: 500; color: var(--mu); border-bottom: 2px solid transparent; }
.tab:hover { color: var(--ink); }
.tab.active { color: var(--p); border-bottom-color: var(--p); }
```

**Comparison table** — see `component-patterns.md`. Row hover uses `var(--pl)`.

## Brand-swap mechanism

When Graeham chooses the final brand:

1. Update this file's `:root` block.
2. Run `scripts/brand-swap.py path/to/propiq-ui-repo` — finds all HTML files, replaces placeholder hex codes with the new palette.
3. Visually verify via screenshot loop across dashboard, settings, landing page.
4. Commit and deploy.

Everything downstream (buttons, tables, navs, cards) already uses CSS variables, so the swap is one pass — no hunt-and-replace across components.

## Color alternatives under consideration

Not shipped — listed so Graeham knows the options when brand-selection happens.

| Direction | Primary | Notes |
|---|---|---|
| Current — Deep Slate | #1a2744 | Safe, serious, financial-product feel |
| Emerald Pro | #0F5F49 | Warmer, "advisor/wealth" vibe |
| Ink + Coral accent | #0B1019 + #F24E3D | More startup/energy, bolder |
| Heritage Burgundy | #6B1F2B | Luxury / Bay Area real-estate adjacency |

Each would need a full accent-and-neutrals system built out. Don't pick without running comps through the screenshot loop.

## Important reminder

Nothing in this file is Graeham-approved branding. When anyone sees a PropIQ screen and asks "is this the PropIQ brand?" the correct answer is:

> "No — these are placeholder colors from the current mockups. The real brand is still being chosen."
