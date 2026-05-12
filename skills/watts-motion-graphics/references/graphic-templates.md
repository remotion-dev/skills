# Graphic Templates — Watts Motion Graphics

The 5 reusable graphic templates. Pre-built React components for each are in `assets/components/`. This file documents the specs and when to use each.

## Template 1 — Stat Callout (single)

**Purpose:** A single big number with a tiny label above it.

**When to use:**
- One key data point standing alone (e.g., "GLOBAL LAYOFFS · META · APRIL 23 / 8,000")
- A locked rate, a YoY %, a price point
- Any moment where the viewer needs to absorb one number cleanly

**Specs:**
- Solid black box, ~440 × 160px
- Top accent: thin General Accent line (`#C4A265`, 2px, 80% width centered on top edge)
- Eyebrow label: General Accent, uppercase, letter-spacing 2px, 11pt
- Big number: white (or gold if hero-emphasis within the scene), Syne Bold or Inter Bold, 64pt
- Padding: 28px top/bottom, 36px left/right
- Corner radius: 0px

**Animation:**
- Opacity fade-in 8 frames
- Optional: subtle scale 95→100% over same window
- Hold 3–5s
- Opacity fade-out 8 frames

**Component:** `assets/components/StatCallout.tsx`

---

## Template 2 — Compare Card (side-by-side)

**Purpose:** Two stat callouts juxtaposed — A vs B.

**When to use:**
- Pull out $100K vs Take home $55–65K (the 401(k) penalty math)
- DOM 11–13 vs SF YoY +19% (market context compare)
- Single $250K vs Married $500K (Section 121 thresholds)
- Any moment where two numbers tell a story together

**Specs:**
- Two stat callouts on the same horizontal line
- Separator: `vs` token in soft white at 36pt centered between them
- 36px gap between each box and the `vs`
- When one side is the "win," its big number renders in **General Accent gold**, the other in white
- Both boxes same size

**Animation:**
- Both boxes fade in together (don't stagger)
- `vs` fades in 4 frames after the boxes
- Hold 4–5s (slightly longer than single because viewer needs to compare)

**Component:** `assets/components/CompareCard.tsx`

---

## Template 3 — Decision Framework (3-row stacked)

**Purpose:** Multi-condition framework on one card — condition → recommendation.

**When to use:**
- Runway → Option (the closing framework in financial videos)
- Symptom → Action (any "if X then Y" framework)
- Stage → Strategy (educational frameworks)

**Specs:**
- One large solid black box, ~830 × 290px, 3 horizontal rows
- Left column (~50%): condition in white body text — Inter, sentence case, 22–24pt
- Center column (~10%): General Accent arrow `→`, 24pt
- Right column (~40%): option label in General Accent uppercase Syne Bold, 36pt
- Rows separated by thin General Accent horizontal rule (1px, 90% opacity)
- Left edge of card: thin General Accent vertical stroke (2–3px, full height)
- Padding: 28px between rows, 40px left/right

**Animation:**
- Card fades in 12 frames
- Rows can stagger: row 1 at frame N, row 2 at N+8, row 3 at N+16 (optional, looks great)
- Hold 5–7s (longest hold of any non-HERO graphic — viewer needs to read all 3 rows)

**Component:** `assets/components/DecisionFramework.tsx`

---

## Template 4 — HERO Reveal (no panel)

**Purpose:** The single climax word/phrase of the video. **One per video.** Reserved.

**When to use:**
- The contrarian payoff word ("TAX-FREE")
- A final number that resolves the entire setup ("$500,000")
- A two-word phrase that delivers the punch ("ZERO TAX")

**Specs:**
- **NO panel, NO box, NO background** — just text floating directly on the green
- Font: **Syne Bold**, ALL CAPS
- Size: **220–280pt** (massive scale — must dominate frame)
- Color: **Watts Gold `#B8945A`** (the protected color, ONLY used here)
- Position: bottom-third or right-third (per Vaibhav-style framing rules — never centered)
- The avatar should occupy the remaining negative space

**Animation:**
- Scale-in 95% to 100% over 24 frames (0.8s) with opacity fade
- Hold **5–7 seconds** — never cut early
- Scale-out 100% to 105% with opacity fade-out 12 frames

**CapCut audio rule:**
- Music drops to **silence** at the in-point
- Hold silence for the full duration of the reveal
- Music fades back in over 0.5s after the exit

**Component:** `assets/components/HeroReveal.tsx`

---

## Template 5 — End Card / Lower Third

**Purpose:** Brand intro lower third (early in video) or end card (final scene).

**When to use:**
- Lower third introducing Graeham early in scene 1
- End card with name + role + CTA contact at video close
- Any "who is talking" or "how to reach me" moment

**Specs:**
- Solid black box, full-width or 2/3 width, anchored bottom of frame
- Layout: name/title on left, role/contact on right
- Top edge: thin General Accent stroke (2px)
- Name: Syne Bold 36pt white
- Role line: Inter 18pt at 70% white
- Padding: 24px top/bottom, 48px left/right

**Critical rule: NEVER include DRE number in the graphic.** Per Graeham's standing rule, DRE goes in the video description / dashboard, not on screen.

**Animation:**
- Slide up from bottom + opacity fade over 12 frames
- Hold 4–6s
- Slide down + fade out 8 frames

**Component:** `assets/components/EndCard.tsx`

---

## Choosing the right template

| Need | Template |
|---|---|
| One big number to absorb | Stat Callout |
| Two numbers that tell a story together | Compare Card |
| Condition → action framework with 3 rows | Decision Framework |
| The single climax of the video | HERO Reveal |
| "Who is talking" or contact closer | End Card |

If a need doesn't fit cleanly, the safest default is Stat Callout. Add multiple sequenced Stat Callouts rather than inventing new templates — consistency across videos is part of the brand.

## What to do when none of these fit

If the user requests something genuinely new (e.g., a chart, a map, a checklist), **flag this explicitly** rather than improvising. Options:

1. Build it as a one-off component and warn that it's not in the standard library
2. Suggest restructuring the moment to use one of the 5 standard templates
3. Recommend Jason adds it manually in CapCut as a graphic asset

Resist the urge to invent new templates without the user's explicit blessing. The system works because it's tight.
