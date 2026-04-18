---
name: website-builder
description: "Professional website builder with Standard and Premium build modes. Use ANY time the user mentions: website, landing page, web page, HTML site, build a site, property page, farm page, single-page site, multi-page site, marketing site, brand site, portfolio site, PropIQ site, investor page, listing page, coming soon page, squeeze page, lead capture page, or anything related to creating, editing, or improving a website or web page. Also trigger when the user says 'build me a site', 'make a landing page', 'website for my listing', 'update my site', 'redesign this page', or describes a web presence they want created. Supports reference site cloning, design token systems, scroll-triggered animations, AI asset generation, and glass morphism effects."
---

# Website Builder

Build professional, brand-consistent websites with two build modes: **Standard** (clean, fast, professional) and **Premium** (high-end with animations, cloned layouts, and custom assets). Every build uses a design token system for brand consistency, and pages are constructed section-by-section for quality control.

---

## Step 0: Choose Build Mode

When this skill is triggered, **immediately present the two build modes** before writing any code:

> **Which build mode do you want?**
>
> **Standard Build** — Clean, professional, brand-consistent. Design tokens + section-by-section construction + auto-generated design system doc. Great for property pages, farm landing pages, business sites.
>
> **Premium Build** — Everything in Standard PLUS scroll-triggered animations, reference site cloning, AI-generated custom assets, glass morphism effects, and micro-interactions. For luxury listings, brand sites, PropIQ marketing, investor pitch pages — anything where first impression matters.
>
> Just say "standard" or "premium" (or "high-end" / "wow factor" for premium).

If the user doesn't specify, default to **Standard**. If they say "premium", "high-end", "wow factor", or "make it impressive", use **Premium**.

---

## Standard Build (Default)

Every Standard build includes these three pillars. They are **not optional** — they are the foundation of every site this skill produces.

### Pillar 1: Design Token System

**Before writing ANY HTML or CSS**, generate a `:root` block of CSS custom properties (variables) that define the brand's entire visual language. Every component references these tokens — **never hardcode colors, fonts, spacing, or shadows**.

```css
:root {
  /* Colors */
  --color-primary: #1a1a1a;
  --color-accent: #C5A55A;
  --color-light: #ffffff;
  --color-bg: #ffffff;
  --color-text: #333333;
  --color-text-muted: #666666;
  --color-border: #e0e0e0;

  /* Typography */
  --font-heading: 'Montserrat', sans-serif;
  --font-body: 'Inter', sans-serif;
  --font-size-base: 1rem;
  --font-size-lg: 1.25rem;
  --font-size-xl: 1.5rem;
  --font-size-2xl: 2rem;
  --font-size-3xl: 2.5rem;
  --font-size-hero: 3.5rem;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  --line-height-tight: 1.2;
  --line-height-normal: 1.6;

  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 2rem;
  --space-xl: 3rem;
  --space-2xl: 5rem;
  --space-section: 6rem;

  /* Layout */
  --max-width: 1200px;
  --max-width-narrow: 800px;
  --border-radius-sm: 4px;
  --border-radius-md: 8px;
  --border-radius-lg: 16px;
  --border-radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.08);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.1);
  --shadow-lg: 0 8px 30px rgba(0,0,0,0.12);
  --shadow-xl: 0 20px 60px rgba(0,0,0,0.15);

  /* Transitions */
  --transition-fast: 0.15s ease;
  --transition-base: 0.3s ease;
  --transition-slow: 0.5s ease;
}
```

The tokens above are **Graeham's branding defaults** (see Branding Defaults section below). For other clients, ask for their brand colors, fonts, and style preferences and generate a custom token set.

**Why this matters:** When every element references tokens instead of hardcoded values, you can rebrand an entire site by changing 10 lines of CSS. It also means every section automatically matches every other section — no drift.

### Pillar 2: Section-by-Section Building

**Never generate a full page in one shot.** Build sequentially, reviewing each section before moving on:

1. **Design tokens** (the `:root` block above)
2. **HTML boilerplate** — `<\!DOCTYPE html>`, meta tags, font imports, viewport tag
3. **Header / Navigation** — logo, nav links, mobile hamburger menu
4. **Hero Section** — headline, subheadline, CTA button, hero image/background
5. **Content Sections** — build each one individually:
   - Features / services grid
   - About / bio section
   - Testimonials
   - Stats / social proof
   - Gallery / portfolio
   - Contact / CTA
6. **Footer** — links, contact info, legal, social icons

For each section:
- Write the HTML structure
- Write the CSS using token references only
- Make it fully responsive (mobile-first)
- Test mentally: does this section look complete on its own?

### Pillar 3: Auto-Generated Design System Doc

After building the site, automatically create a `design-system.md` file documenting:

- All design tokens and their values
- Component patterns used (card style, button variants, section layouts)
- Brand rules (logo usage, color combinations, typography hierarchy)
- Responsive breakpoints used
- Any animations or interactions included

This means **future edits or new pages automatically stay on-brand** — hand someone the design system doc and they can extend the site without guessing.

---

## Premium Build

Everything in Standard Build, PLUS the following four enhancements. Use Premium when the user says "premium", "high-end", "wow factor", "make it impressive", or when the project is a luxury listing, brand marketing site, investor pitch, or anything where first impression is critical.

### Enhancement 1: Reference Site Cloning

**Optional Step 0** — before building, ask:

> "Do you have a reference site you want to match? Drop a URL and I'll extract its design patterns as a foundation."

If the user provides a URL:
1. Use Chrome browser tools to navigate to the reference URL
2. Use `get_page_text` or `read_page` to grab the page structure
3. Extract design patterns:
   - Font families and sizes
   - Color palette
   - Spacing rhythm
   - Layout structure (grid vs. flexbox, section ordering)
   - Animation patterns
   - Navigation style
4. Generate a custom token set based on the reference
5. Use the extracted patterns as the structural foundation, then customize for the user's brand

**Why this produces better results:** Describing "I want it to look like Apple's site" is vague. Actually extracting the CSS patterns from Apple's site gives exact values to work from.

### Enhancement 2: Advanced Animations

Scroll-triggered animations using the **4-event framework**:

#### Event 1: On Scroll-In (element enters viewport)
```css
.fade-up {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity var(--transition-slow), transform var(--transition-slow);
}
.fade-up.visible {
  opacity: 1;
  transform: translateY(0);
}
```

#### Event 2: On Scroll-Out (element leaves viewport)
```css
.fade-out-on-leave.hidden {
  opacity: 0;
  transform: translateY(-20px);
}
```

#### Event 3: While Scrolling (parallax)
```css
.parallax-bg {
  background-attachment: fixed;
  background-position: center;
  background-size: cover;
}
```
For more control, use JS to adjust `transform: translateY()` based on scroll position.

#### Event 4: On Page Load
```css
@keyframes stagger-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.hero-text > * {
  animation: stagger-in 0.6s ease forwards;
  opacity: 0;
}
.hero-text > *:nth-child(1) { animation-delay: 0.1s; }
.hero-text > *:nth-child(2) { animation-delay: 0.25s; }
.hero-text > *:nth-child(3) { animation-delay: 0.4s; }
```

#### Intersection Observer (required for scroll-triggered animations)
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    } else {
      entry.target.classList.remove('visible');
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.fade-up, .slide-in-left, .slide-in-right, .scale-up').forEach(el => {
  observer.observe(el);
});
```

**Staggered delays for multi-element sections** — cards, features, team members should appear one-by-one, not all at once:
```css
.stagger > *:nth-child(1) { transition-delay: 0s; }
.stagger > *:nth-child(2) { transition-delay: 0.1s; }
.stagger > *:nth-child(3) { transition-delay: 0.2s; }
.stagger > *:nth-child(4) { transition-delay: 0.3s; }
```

### Enhancement 3: AI-Generated Custom Assets

Instead of relying on stock photos (which look generic), offer to generate custom assets:

- **Custom icons** — illustrated or isometric style via Recraft.ai (not generic line icons)
- **Illustrated hero images** — isometric or illustrated style stands out more than photorealistic stock
- **Background textures** — subtle gradients, grain overlays, geometric patterns
- **Brand illustrations** — custom scenes matching the brand's visual language

**How to offer this:**
> "I can generate AI image prompts for custom icons and illustrations instead of using stock photos. Want me to create prompts you can run through an image generator? This gives you unique assets that match your brand perfectly."

Generate the prompts, and the user can create the assets externally and provide them back for integration.

### Enhancement 4: Interactive Elements

Use these **only where they add value** — not on every element:

#### Glass Morphism
```css
.glass-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--border-radius-lg);
}
```

#### Hover State Transitions
```css
.card-hover {
  transition: transform var(--transition-base), box-shadow var(--transition-base);
}
.card-hover:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}
```

#### Button Micro-Animations
```css
.btn-primary {
  transition: transform var(--transition-fast), box-shadow var(--transition-fast);
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
.btn-primary:active {
  transform: translateY(0);
}
```

#### Cursor-Following Effect (hero sections only)
```javascript
document.querySelector('.hero').addEventListener('mousemove', (e) => {
  const x = (e.clientX / window.innerWidth - 0.5) * 20;
  const y = (e.clientY / window.innerHeight - 0.5) * 20;
  document.querySelector('.hero-bg').style.transform =
    `translate(${x}px, ${y}px) scale(1.05)`;
});
```

---

## Contextual Options

At any point during a build, if the user asks "what can you do?" or "what are my options?", present enhancements relevant to the **current section being built**:

| Currently Building | Available Enhancements |
|---|---|
| **Hero section** | Parallax scrolling, staggered text animation, subtle video background, cursor-following effect, glass morphism overlay |
| **Cards / Features grid** | Hover lift effects, staggered scroll-in animations, glass morphism styling, bento grid layout |
| **Testimonials** | Auto-rotating carousel, fade transitions, quote mark decorations |
| **Navigation** | Sticky header with blur background, smooth scroll anchors, mobile slide-out menu |
| **Any section** | "I can clone the layout from a reference site if you have a URL" |
| **Whole page** | Custom AI icons instead of stock, scroll-triggered animations throughout, design system doc for future consistency |

Don't dump all options at once — only show what's relevant to the current context.

---

## Design Pattern Vocabulary

Reference for terms used in this skill. Use these correctly in all builds:

| Term | What It Means | CSS/JS |
|---|---|---|
| **Bento grid** | Asymmetric card layout with varying sizes (like Apple's product pages) | `grid-template-columns` with `span` variations |
| **Glass morphism** | Frosted glass effect — semi-transparent background with blur | `backdrop-filter: blur()` + `rgba()` background |
| **Parallax** | Background moves slower than foreground on scroll | `background-attachment: fixed` or JS scroll transform |
| **Staggered animation** | Elements animate in sequence with increasing delays | `transition-delay` or `animation-delay` increments |
| **Scroll-triggered** | Animations fire when element enters viewport | Intersection Observer API |
| **Micro-interaction** | Small hover/click feedback | `transform: scale()`, `translateY()`, `box-shadow` transitions |
| **Design tokens** | CSS custom properties that define the brand's visual language | `:root { --color-primary: ... }` |
| **Section rhythm** | Consistent vertical spacing between page sections | `padding: var(--space-section) 0` |
| **Mobile-first** | Write CSS for mobile, then add `@media` for larger screens | `@media (min-width: 768px) { }` |

---

## Graeham's Branding Defaults

When building for Graeham (which is the default unless a different client is specified), use these tokens:

```css
:root {
  --color-primary: #1a1a1a;    /* Black */
  --color-accent: #C5A55A;     /* Gold */
  --color-light: #ffffff;       /* White */
  --color-bg: #ffffff;          /* White background */
  --font-heading: 'Montserrat', sans-serif;
  --font-body: 'Inter', sans-serif;
}
```

**Agent info for footers/headers:**
- Name: Graeham Watts
- Brokerage: Intero Real Estate
- DRE #: 01466876

Import fonts via Google Fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

---

## Responsive Breakpoints

Use these consistently across all builds:

```css
/* Mobile-first base styles (< 768px) */

@media (min-width: 768px) {
  /* Tablet */
}

@media (min-width: 1024px) {
  /* Desktop */
}

@media (min-width: 1280px) {
  /* Large desktop */
}
```

---

## Build Checklist

Before delivering any site, verify:

- [ ] All colors/fonts/spacing use token references, never hardcoded values
- [ ] Fully responsive — tested mentally at mobile, tablet, desktop widths
- [ ] All images have `alt` text
- [ ] Semantic HTML (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`)
- [ ] Smooth scroll enabled for anchor links
- [ ] Mobile navigation works (hamburger menu or equivalent)
- [ ] Page loads fast — no unnecessary libraries, optimized assets
- [ ] Meta tags present (title, description, viewport, Open Graph)
- [ ] Design system doc generated (Standard+) or offered (all builds)
- [ ] If Premium: animations are smooth, not janky; glass morphism has fallbacks
- [ ] Favicon linked
- [ ] No horizontal scroll on any viewport width

---

## File Output

Save the completed site as a single `.html` file in the outputs folder. For Premium builds with significant JavaScript, keep it in the same file using `<script>` tags at the bottom of `<body>`.

If a design system doc is generated, save it as `design-system.md` alongside the HTML file.

If the site has multiple pages, create a folder structure:
```
site-name/
├── index.html
├── about.html
├── contact.html
├── design-system.md
└── assets/
    └── (any generated images or icons)
```
