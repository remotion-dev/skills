# Design Tokens

Every site this skill builds uses CSS custom properties (`:root` variables). Editing one variable should cascade across the whole page. No raw hex codes scattered in component styles.

## Baseline `:root` block

Paste this at the top of any new page, then edit the brand section only.

```css
:root {
  /* Brand — edit these per project */
  --brand-primary: #1a2744;      /* dominant color */
  --brand-primary-hover: #111d33;
  --brand-primary-light: #e8ecf5; /* tint for bg fills */
  --brand-accent: #2d4278;        /* secondary actions, links */

  /* Status colors — keep these stable */
  --status-success: #1f8a5c;
  --status-success-light: #e8f5ee;
  --status-warn: #ba7517;
  --status-warn-light: #faeeda;
  --status-danger: #c0392b;
  --status-danger-light: #fdf0f0;
  --status-info: #185fa5;
  --status-info-light: #e6f1fb;

  /* Neutral scale */
  --ink: #111827;        /* primary text */
  --ink-muted: #6b7280;  /* secondary text */
  --ink-faded: #9ca3af;  /* hints, placeholders */
  --bg: #f8f7f4;         /* page background (warm white) */
  --surface: #ffffff;    /* cards, inputs */
  --border: #e5e3de;     /* hairlines */
  --border-strong: #d1cfc9;

  /* Spatial */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-pill: 999px;

  /* Shadows — keep subtle */
  --shadow-sm: 0 1px 2px rgba(17,24,39,.06);
  --shadow-md: 0 4px 12px rgba(17,24,39,.08);
  --shadow-lg: 0 12px 40px rgba(17,24,39,.12);

  /* Typography — override per project */
  --font-display: "Playfair Display", Georgia, serif;
  --font-body: "Epilogue", system-ui, sans-serif;

  /* Motion */
  --ease-out: cubic-bezier(.2,.8,.2,1);
  --ease-spring: cubic-bezier(.34,1.56,.64,1);
  --dur-fast: 150ms;
  --dur-med: 280ms;
  --dur-slow: 500ms;
}
```

## Why these tokens and not others

`--bg: #f8f7f4` — warm white instead of pure `#fff`. Pure white pages read as "AI default". A 2% warm tint reads as intentional.

Four status colors not three. Amber (`#ba7517`) is frequently needed for "needs attention, not broken" states in real-estate dashboards (pending docs, expiring contingencies) — separate from red/danger.

Spacing is handled via utility classes or flex/grid gaps, not tokens. Locking spacing to a scale variable creates more friction than benefit on HTML-first builds.

Radius has four values, not a long scale. `sm` for inputs, `md` for cards, `lg` for hero panels, `pill` for chips/buttons. More than four values and consistency slips.

## Brand swap flow

To apply a different brand, touch only the `/* Brand */` block plus `--font-display` and `--font-body`. Everything else stays the same. The `scripts/brand-swap.py` helper does this automatically when you feed it a brand config (see `scripts/brand-swap.py`).

## Dark mode

If the user wants dark mode, wrap an overriding block under `@media (prefers-color-scheme: dark)` or a `[data-theme="dark"]` selector, and redefine only `--bg`, `--surface`, `--ink`, `--ink-muted`, `--border`. The brand and status colors stay the same — they just need to have enough contrast for both themes.

```css
[data-theme="dark"] {
  --bg: #0b0f1a;
  --surface: #141a2b;
  --ink: #eef1f7;
  --ink-muted: #98a0b3;
  --ink-faded: #6b7285;
  --border: #232a3c;
  --border-strong: #2f3650;
}
```

## Never do this

Inline hex values inside components. If you find `color: #1a2744` anywhere outside `:root`, refactor to `color: var(--brand-primary)`.

Ship without testing contrast. Body text on `--bg` needs at least 7:1 (AAA) for readability.

Use the brand color for body text. Brand color goes on headers, links, accent UI only. Body text is `--ink`.
