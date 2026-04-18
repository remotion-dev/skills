# Motion and Animation

Motion makes UI feel alive. Overdone motion makes UI feel like a banner ad. These patterns hit the sweet spot.

## Hover elevation

The one animation every interactive element should have.

```css
.hover-lift { transition: transform var(--dur-med) var(--ease-out), box-shadow var(--dur-med) var(--ease-out); }
.hover-lift:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
```

Apply to cards, buttons, list items. Keep `translateY` at `-1px` to `-3px` — anything larger looks like a fever dream.

## Fade-in on scroll (IntersectionObserver)

Lightweight vanilla JS. No library needed.

```html
<div class="reveal">...</div>
```

```css
.reveal { opacity: 0; transform: translateY(20px); transition: opacity var(--dur-slow) var(--ease-out), transform var(--dur-slow) var(--ease-out); }
.reveal.visible { opacity: 1; transform: translateY(0); }
```

```js
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => e.isIntersecting && e.target.classList.add('visible'));
}, { threshold: 0.15, rootMargin: '0px 0px -80px 0px' });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));
```

## Staggered reveal

When a row of features fades in, stagger by 80–120ms per item — feels intentional, not mechanical.

```css
.reveal:nth-child(1) { transition-delay: 0ms; }
.reveal:nth-child(2) { transition-delay: 80ms; }
.reveal:nth-child(3) { transition-delay: 160ms; }
.reveal:nth-child(4) { transition-delay: 240ms; }
```

Or set via JS:
```js
document.querySelectorAll('.feature-grid .reveal').forEach((el, i) => {
  el.style.transitionDelay = `${i * 80}ms`;
});
```

## Text reveal (word by word)

For hero headlines when you want emphasis.

```html
<h1 class="words">Build faster. Ship sharper. Close more.</h1>
```

```css
.words { display: inline; }
.words .w { display: inline-block; opacity: 0; transform: translateY(12px); transition: opacity 600ms var(--ease-out), transform 600ms var(--ease-out); }
.words .w.in { opacity: 1; transform: none; }
```

```js
document.querySelectorAll('.words').forEach(el => {
  el.innerHTML = el.textContent.split(' ').map(w => `<span class="w">${w}</span>`).join(' ');
  el.querySelectorAll('.w').forEach((w, i) => {
    setTimeout(() => w.classList.add('in'), i * 90);
  });
});
```

## Number count-up

For stat sections. Makes big numbers feel earned.

```js
function countUp(el, to, ms = 1400) {
  const start = performance.now();
  (function step(t) {
    const p = Math.min(1, (t - start) / ms);
    const eased = 1 - Math.pow(1 - p, 3);
    el.textContent = Math.floor(eased * to).toLocaleString();
    if (p < 1) requestAnimationFrame(step);
  })(start);
}
// Trigger on viewport intersection:
new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    const n = +e.target.dataset.to;
    countUp(e.target, n);
    io.unobserve(e.target);
  });
}, { threshold: 0.5 }).observe(document.querySelector('[data-to]'));
```

## Scroll-linked parallax (restrained)

```css
.parallax { will-change: transform; transform: translateY(0); transition: transform 50ms linear; }
```

```js
let scrolling = false;
window.addEventListener('scroll', () => {
  if (scrolling) return;
  requestAnimationFrame(() => {
    document.querySelectorAll('.parallax').forEach(el => {
      const speed = +el.dataset.speed || 0.3;
      el.style.transform = `translateY(${window.scrollY * speed * -1}px)`;
    });
    scrolling = false;
  });
  scrolling = true;
});
```

`data-speed="0.3"` means element moves 30% of scroll distance. Speeds above 0.5 create motion sickness. Reserve parallax for one or two hero-level elements.

## Loading states

Never show a spinner if content can be shown within 300ms. Use skeleton screens instead for slower loads.

```css
.skeleton { background: linear-gradient(90deg, var(--border) 0%, var(--border-strong) 50%, var(--border) 100%); background-size: 200% 100%; animation: shimmer 1.4s linear infinite; border-radius: var(--radius-md); }
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
```

## Transitions between states

When a button becomes active/disabled, animate the transition. Instant state-swaps feel broken.

```css
.btn { transition: background var(--dur-fast), color var(--dur-fast), transform var(--dur-fast), opacity var(--dur-fast); }
.btn:disabled { opacity: 0.5; pointer-events: none; }
```

## Respect `prefers-reduced-motion`

Required for accessibility. One block disables animations for anyone who needs it.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

## What not to do

Looping attention-seekers (pulsing CTAs, wiggling buttons) read as spam.

Page-load entrance animations on every element cascade into visual chaos. Only animate above-the-fold and revealed-on-scroll content.

Bouncy easings (`cubic-bezier(.68,-0.55,.27,1.55)`) on non-playful UI. Bounce works for kids' apps, not dashboards.

Parallax on mobile. Detect and disable:
```css
@media (max-width: 768px) { .parallax { transform: none !important; } }
```
