# Backgrounds and Textures

Backgrounds are what separate "looks like a template" from "looks custom". One background treatment per page. Stacking them (gradient + orbs + noise + grid) creates noise, not depth.

## Glassmorphism

Frosted-glass surfaces layered over colorful content. Used in the canonical PropIQ nav. Requires two things: semi-transparent background + `backdrop-filter: blur()`.

```css
.glass {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 8px 32px rgba(17, 24, 39, 0.06);
}
.glass-dark {
  background: rgba(17, 24, 39, 0.6);
  backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
}
```

Glass only works over something colorful. Glass over a flat white bg looks like a grey box. Pair with orbs or a gradient.

## Floating orbs

Large radial-gradient blurs positioned behind content. Softly animated. The canonical "modern hero background".

```html
<div class="orb-layer" aria-hidden="true">
  <div class="orb orb-1"></div>
  <div class="orb orb-2"></div>
  <div class="orb orb-3"></div>
</div>
```

```css
.orb-layer { position: fixed; inset: 0; z-index: -1; overflow: hidden; pointer-events: none; }
.orb { position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.45; animation: float 20s var(--ease-out) infinite; }
.orb-1 { width: 500px; height: 500px; background: var(--brand-primary); top: -150px; left: -100px; }
.orb-2 { width: 400px; height: 400px; background: var(--brand-accent); bottom: -100px; right: 0; animation-delay: -7s; }
.orb-3 { width: 350px; height: 350px; background: var(--status-info); top: 40%; left: 40%; animation-delay: -14s; }

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(40px, -30px) scale(1.05); }
  66% { transform: translate(-30px, 20px) scale(0.95); }
}
```

Use three orbs, not two (reads as flat) and not five (reads as busy). Animation duration 18–24 seconds — shorter feels anxious, longer feels dead.

## Noise overlay

Subtle film-grain texture over the page. Hides banding in gradients and adds tactile quality.

```html
<div class="noise" aria-hidden="true"></div>
```

```css
.noise { position: fixed; inset: 0; z-index: 1000; pointer-events: none; opacity: 0.035; mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' seed='2'/></filter><rect width='100%' height='100%' filter='url(%23n)' opacity='0.8'/></svg>");
}
```

Opacity above 0.05 is too visible and reads as a bad JPEG. 0.03–0.04 is the sweet spot.

## Grid overlay

Line-grid background. Reads as "technical / product" rather than "editorial".

```css
.grid-bg {
  background-image:
    linear-gradient(to right, rgba(17, 24, 39, 0.04) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(17, 24, 39, 0.04) 1px, transparent 1px);
  background-size: 40px 40px;
}
```

Fade the grid at the edges with a radial mask so it doesn't feel like graph paper to the viewport edge:

```css
.grid-bg { mask-image: radial-gradient(ellipse at center, #000 40%, transparent 85%); }
```

## Dot grid

Softer alternative to line grid. Reads more "design system reference" than "engineering spec".

```css
.dot-bg { background-image: radial-gradient(rgba(17, 24, 39, 0.1) 1px, transparent 1px); background-size: 24px 24px; }
```

## Aurora / mesh gradient

Multiple color radial gradients layered. Modern SaaS hero background. More alive than flat gradients, less playful than orbs.

```css
.aurora {
  background:
    radial-gradient(at 20% 10%, hsla(220, 70%, 70%, 0.3) 0, transparent 50%),
    radial-gradient(at 80% 20%, hsla(280, 70%, 75%, 0.25) 0, transparent 50%),
    radial-gradient(at 30% 80%, hsla(180, 70%, 70%, 0.25) 0, transparent 50%),
    radial-gradient(at 90% 80%, hsla(340, 70%, 75%, 0.2) 0, transparent 50%),
    var(--bg);
}
```

## Paper texture (editorial sites)

```css
.paper {
  background: var(--bg);
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100'><filter id='p'><feTurbulence baseFrequency='0.04' numOctaves='5'/><feColorMatrix values='0 0 0 0 0.15 0 0 0 0 0.13 0 0 0 0 0.10 0 0 0 0.015 0'/></filter><rect width='100%' height='100%' filter='url(%23p)'/></svg>");
}
```

Pairs well with serif-heavy layouts. Do not combine with orbs.

## Choosing which background

| Aesthetic goal | Use |
|---|---|
| Modern SaaS hero | Aurora or orbs + glass |
| Editorial long-form | Paper texture, no orbs |
| Product dashboard | Dot grid or flat `--bg` with noise |
| Luxury / realtor | Flat `--bg` with subtle noise only |
| Tech / developer tool | Line grid with faded edges |

## Performance notes

`backdrop-filter: blur()` is expensive. On pages with many glass surfaces, GPU performance drops. If a page has more than 3–4 glass elements visible at once, reduce blur radius or drop to flat translucent backgrounds.

Animated orbs cost very little (GPU compositing). Use freely.

Noise SVGs inlined as data URIs are ~800 bytes. Cheaper than an image request.
