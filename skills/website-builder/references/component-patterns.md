# Component Patterns

Canonical reusable components. Pulled and normalized from Graeham's PropIQ screens. Copy into a page, wire to tokens from `design-tokens.md`, done.

## Buttons

Six variants. Three is enough for marketing sites; all six are needed for product UI.

```css
.btn { display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 18px; border-radius: var(--radius-md);
  font-family: var(--font-body); font-weight: 600; font-size: var(--fs-base);
  border: 1px solid transparent; cursor: pointer; transition: all var(--dur-fast) var(--ease-out);
  text-decoration: none; line-height: 1; white-space: nowrap;
}
.btn-primary { background: var(--brand-primary); color: #fff; }
.btn-primary:hover { background: var(--brand-primary-hover); transform: translateY(-1px); box-shadow: var(--shadow-md); }

.btn-outline { background: transparent; color: var(--brand-primary); border-color: var(--brand-primary); }
.btn-outline:hover { background: var(--brand-primary-light); }

.btn-ghost { background: transparent; color: var(--ink); }
.btn-ghost:hover { background: var(--brand-primary-light); }

.btn-danger { background: var(--status-danger); color: #fff; }
.btn-danger:hover { filter: brightness(0.92); }

.btn-amber { background: var(--status-warn); color: #fff; }
.btn-amber:hover { filter: brightness(0.92); }

.btn-muted { background: var(--border); color: var(--ink-muted); }
.btn-muted:hover { background: var(--border-strong); color: var(--ink); }

.btn-lg { padding: 14px 26px; font-size: var(--fs-md); }
.btn-sm { padding: 6px 12px; font-size: var(--fs-sm); }
```

Never use `border-radius: 50px` on rectangular buttons — use `var(--radius-md)` (10px). Pill buttons read as consumer-brand; sharp-corner buttons read as tech/product. Match the aesthetic.

## Badges / chips

```css
.badge { display: inline-flex; align-items: center; gap: 6px;
  padding: 3px 10px; border-radius: var(--radius-pill);
  font-size: var(--fs-xs); font-weight: 600;
  letter-spacing: 0.04em; text-transform: uppercase;
}
.badge-neutral { background: var(--border); color: var(--ink); }
.badge-success { background: var(--status-success-light); color: var(--status-success); }
.badge-warn { background: var(--status-warn-light); color: var(--status-warn); }
.badge-danger { background: var(--status-danger-light); color: var(--status-danger); }
.badge-info { background: var(--status-info-light); color: var(--status-info); }
.badge-brand { background: var(--brand-primary-light); color: var(--brand-primary); }
```

A dot before the label reads cleaner than an icon. `<span class="badge badge-success">● Active</span>`.

## Card

```css
.card { background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px;
  transition: transform var(--dur-med) var(--ease-out), box-shadow var(--dur-med) var(--ease-out);
}
.card-interactive:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); border-color: var(--border-strong); }
.card-feature { border: none; background: linear-gradient(135deg, var(--surface), var(--brand-primary-light) 140%); }
.card-hero { padding: 32px; border-radius: 24px; box-shadow: var(--shadow-lg); }
```

Avoid `box-shadow` on every card by default — it creates "floating cards everywhere" which looks generic. Reserve shadow for interactive hover state or hero emphasis.

## KPI / metric card

```css
.kpi { display: flex; flex-direction: column; gap: 4px; padding: 18px;
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-md);
}
.kpi-label { font-size: var(--fs-xs); font-weight: 600; letter-spacing: 0.08em;
  text-transform: uppercase; color: var(--ink-muted);
}
.kpi-value { font-family: var(--font-display); font-size: var(--fs-2xl); line-height: 1; color: var(--ink); }
.kpi-delta { display: inline-flex; align-items: center; gap: 4px; font-size: var(--fs-sm); font-weight: 600; }
.kpi-delta.up { color: var(--status-success); }
.kpi-delta.down { color: var(--status-danger); }
```

Value in display font. Label in small caps. Delta with a triangle, not an arrow — triangles read more "financial dashboard" than emoji arrows.

## Comparison table

```css
.table { width: 100%; border-collapse: separate; border-spacing: 0;
  font-size: var(--fs-sm); font-family: var(--font-body);
}
.table thead th { text-align: left; padding: 10px 14px;
  font-size: var(--fs-xs); font-weight: 600; letter-spacing: 0.06em;
  text-transform: uppercase; color: var(--ink-muted);
  border-bottom: 1px solid var(--border);
}
.table tbody td { padding: 14px; border-bottom: 1px solid var(--border); vertical-align: middle; }
.table tbody tr:hover { background: var(--brand-primary-light); }
.table tbody tr:last-child td { border-bottom: none; }
.table .num { text-align: right; font-variant-numeric: tabular-nums; }
```

Always `tabular-nums` on numeric columns. It prevents digit columns from shifting horizontally as values change.

## Progress bar

```css
.progress { height: 8px; background: var(--border); border-radius: var(--radius-pill); overflow: hidden; }
.progress > .bar { height: 100%; background: var(--brand-primary); border-radius: inherit;
  transition: width var(--dur-slow) var(--ease-out);
}
```

Gradient fills on progress bars read as consumer-app. Flat brand color reads as business-product.

## Accordions

Use `<details>` and `<summary>` native elements, not a JS widget.

```css
details { border-bottom: 1px solid var(--border); padding: 16px 0; }
summary { list-style: none; cursor: pointer; font-weight: 600; display: flex; justify-content: space-between; align-items: center; }
summary::-webkit-details-marker { display: none; }
summary::after { content: "+"; font-size: 24px; color: var(--ink-muted); transition: transform var(--dur-fast); }
details[open] summary::after { transform: rotate(45deg); }
details > *:not(summary) { margin-top: 12px; color: var(--ink-muted); }
```

## Tooltip

Use the native `title` attribute for simple hover labels. Build a custom tooltip only when you need rich content (multiple lines, formatting).

## Empty state

Dashboards need empty-state patterns. Skip the usual "Nothing here yet 🤷" text.

```html
<div class="empty">
  <div class="empty-icon"><!-- inline SVG --></div>
  <h3 class="empty-title">No comps yet</h3>
  <p class="empty-body">Drop a listing address above to pull three comparable sales.</p>
  <button class="btn btn-outline">Import from MLS</button>
</div>
```

Empty state should always suggest the next action. Never be a dead-end.
