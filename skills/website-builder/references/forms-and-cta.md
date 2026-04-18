# Forms and CTAs

Conversion surfaces. Most AI-generated forms look like Google Forms. Fix the three things below and they stop looking generic.

## Input fields

```css
.input { width: 100%; padding: 12px 14px;
  background: var(--surface); color: var(--ink);
  border: 1px solid var(--border); border-radius: var(--radius-md);
  font-family: var(--font-body); font-size: var(--fs-base);
  transition: border-color var(--dur-fast), box-shadow var(--dur-fast);
}
.input::placeholder { color: var(--ink-faded); }
.input:focus { outline: none; border-color: var(--brand-primary); box-shadow: 0 0 0 3px var(--brand-primary-light); }
.input:disabled { background: var(--border); color: var(--ink-faded); cursor: not-allowed; }
.input.error { border-color: var(--status-danger); }
.input.error:focus { box-shadow: 0 0 0 3px var(--status-danger-light); }
```

Two things that flip inputs from "AI-generic" to "designed":
- Soft focus ring (`box-shadow: 0 0 0 3px var(--brand-primary-light)`) instead of the default blue browser outline.
- `--surface` background even on a `--surface` page — gives a subtle edge. Avoid making the input the same color as the container.

## Labels

```css
.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: var(--fs-sm); font-weight: 500; color: var(--ink); }
.field .hint { font-size: var(--fs-xs); color: var(--ink-muted); }
.field .error-msg { font-size: var(--fs-xs); color: var(--status-danger); display: none; }
.field.error .error-msg { display: block; }
```

Label above the input, not inside (floating labels are trendy but hurt readability for repeat users). Error message appears below the input, never tooltip.

## Multi-step forms

Break long forms into steps. A single 12-field form converts worse than three 4-field steps.

```html
<div class="steps">
  <div class="step done"><span class="num">1</span> Basics</div>
  <div class="step current"><span class="num">2</span> Details</div>
  <div class="step"><span class="num">3</span> Confirm</div>
</div>
```

```css
.steps { display: flex; gap: 20px; margin-bottom: 32px; }
.step { display: flex; align-items: center; gap: 10px; color: var(--ink-muted); font-weight: 500; font-size: var(--fs-sm); }
.step .num { width: 28px; height: 28px; border-radius: 50%; background: var(--border); color: var(--ink-muted); display: grid; place-items: center; font-size: var(--fs-xs); }
.step.current { color: var(--brand-primary); }
.step.current .num { background: var(--brand-primary); color: #fff; }
.step.done .num { background: var(--status-success); color: #fff; }
```

## Inline validation

Validate as the user types or on blur. Never wait until submit — that's what breaks conversion.

```js
document.querySelectorAll('[data-validate]').forEach(input => {
  input.addEventListener('blur', () => {
    const type = input.dataset.validate;
    const val = input.value.trim();
    let ok = true;
    if (type === 'email') ok = /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(val);
    if (type === 'phone') ok = /^\+?[\d\s\-\(\)]{10,}$/.test(val);
    if (type === 'required') ok = val.length > 0;
    input.closest('.field').classList.toggle('error', !ok);
  });
});
```

## CTA cards

Heavy-impact section before the footer. Not a button alone — a card with headline, supporting line, button. See `assets/snippets/cta-card.html`.

```css
.cta-card { padding: 48px; border-radius: var(--radius-lg);
  background: linear-gradient(135deg, var(--brand-primary) 0%, var(--brand-accent) 100%);
  color: #fff; text-align: center;
  position: relative; overflow: hidden;
}
.cta-card::before { content: ""; position: absolute; inset: -50%;
  background: radial-gradient(circle at 30% 30%, rgba(255,255,255,.15), transparent 60%);
  pointer-events: none;
}
.cta-card h2 { font-family: var(--font-display); font-size: clamp(1.8rem, 3vw, 3rem); line-height: 1.1; margin: 0 0 12px; }
.cta-card p { font-size: var(--fs-md); opacity: 0.85; max-width: 48ch; margin: 0 auto 28px; }
.cta-card .btn { background: #fff; color: var(--brand-primary); }
.cta-card .btn:hover { background: var(--brand-primary-light); }
```

## Subscription bar

Single horizontal bar for email capture. Most common newsletter signup pattern.

```html
<form class="subscribe">
  <input class="input" type="email" placeholder="you@domain.com" required>
  <button class="btn btn-primary">Subscribe</button>
</form>
```

```css
.subscribe { display: flex; gap: 8px; max-width: 440px; margin: 0 auto; }
.subscribe .input { flex: 1; }
@media (max-width: 600px) { .subscribe { flex-direction: column; } .subscribe .btn { width: 100%; } }
```

## Pricing cards

Three-tier layout, middle card emphasized.

```css
.pricing { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.plan { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 32px; position: relative; }
.plan.featured { border: 2px solid var(--brand-primary); transform: scale(1.03); box-shadow: var(--shadow-md); }
.plan.featured .badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); }
.plan .price { font-family: var(--font-display); font-size: var(--fs-3xl); line-height: 1; margin: 16px 0 8px; }
.plan .price .per { font-size: var(--fs-sm); color: var(--ink-muted); font-family: var(--font-body); font-weight: 400; }
.plan ul { list-style: none; padding: 0; margin: 20px 0 28px; display: flex; flex-direction: column; gap: 10px; }
.plan ul li::before { content: "✓"; color: var(--status-success); font-weight: 700; margin-right: 8px; }
```

## Copy that converts

Replace AI-default copy. These templates almost always appear on generated sites — rewrite them.

| AI default | Better |
|---|---|
| "Welcome to our platform" | Specific value prop: "Turn MLS data into buyer matches in 90 seconds" |
| "Built for modern teams" | "Built for Peninsula buyers' agents who hate spreadsheet hell" |
| "Get started today" | "Start your free 14-day trial" |
| "Learn more" | Active verb: "See how it works" or "Watch a 2-min demo" |
| "Sign up" | "Create your free account" |

Specificity beats aspiration. "90 seconds", "free 14-day trial", "2-min demo" convert better than their vague equivalents.

## CTA placement

Every long page needs 3+ CTAs: hero, mid-page, before footer. Not more than 5 — readers stop trusting them.

Primary CTA in hero should match the primary CTA in the footer-adjacent band. Same text. Same destination. Consistency builds trust.
