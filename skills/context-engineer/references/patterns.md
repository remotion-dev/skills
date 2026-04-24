# Tiered Context Patterns

Three organizing principles for splitting a monolithic SKILL.md into a tiered structure. Pick the one that matches how the skill's variation falls.

## Pattern 1 — Domain-organized

Use when the skill supports multiple domains or verticals and each has its own deep playbook.

**Example — a real-estate content skill that serves multiple markets:**

```
real-estate-content/
├── SKILL.md            (workflow + market selection)
└── references/
    ├── bay_area.md     (local nuance for SF, Peninsula, EPA)
    ├── austin.md       (local nuance for Austin TX)
    └── nyc.md          (local nuance for NYC)
```

**Pattern:** SKILL.md asks the user which market (or infers it from inputs), then reads only the matching reference. The other market files never enter context.

**When this pattern fits:** the shared workflow is 60%+ of the job and the rest is market/vertical nuance. Each domain file is self-contained.

---

## Pattern 2 — Variant-organized

Use when the skill produces different output formats / variants of the same core thing.

**Example — a video creation skill:**

```
video-creator/
├── SKILL.md                (format selection + shared principles)
└── references/
    ├── mp4_slideshow.md    (ffmpeg-based slideshows)
    ├── remotion.md         (React component-based video)
    ├── heygen.md           (avatar-based video)
    └── stock_broll.md      (higgsfield b-roll generation)
```

**Pattern:** SKILL.md contains a decision tree ("Is this a talking-head video? → HeyGen. Is this a slideshow? → MP4. Is this component-based? → Remotion."). Only the matching reference loads.

**When this pattern fits:** the variants are fundamentally different technologies / output shapes, even if the user-facing request ("make me a video") looks the same.

---

## Pattern 3 — Phase-organized

Use when the skill has a long multi-phase workflow where each phase is expensive to describe.

**Example — a CMA (comparable market analysis) skill:**

```
cma-generator/
├── SKILL.md              (overall workflow + phase selector)
└── references/
    ├── intake.md         (gathering subject property + comp data)
    ├── selection.md      (which comps to include, how to filter)
    ├── adjustments.md    (time, size, condition adjustments)
    ├── pricing.md        (three-strategy pricing framework)
    └── presentation.md   (how to format the final report)
```

**Pattern:** SKILL.md is the conductor. Each phase of the workflow tells Claude which reference to load next. A full run will touch several references; a quick spot-check might only touch one.

**When this pattern fits:** workflows where each phase is self-contained with its own rules, and where different invocations may only need a subset of phases.

---

## Anti-patterns

### The false split
Splitting a SKILL.md into references when the references are so tightly coupled they all get loaded on every run anyway. You just added Read overhead for zero benefit.

Signal: the SKILL.md says "first read references/a.md, then references/b.md, then references/c.md" at the start of every invocation. Not a split — just a slower monolith. Put it all back together.

### The too-fine split
Breaking a 300-line SKILL.md into 8 reference files. Each file is 30 lines and the overhead of loading them outweighs the savings.

Rule of thumb: don't create a reference file under ~100 lines unless it's genuinely independent and only rarely needed. The minimum viable reference is usually ~200 lines.

### The mis-organized split
Using domain organization when variant organization fits better (or vice versa). Signal: the SKILL.md selection logic is awkward — "if the user's industry is X and the format is Y..." when the split was done on industry. Usually means the split should have been on format.

---

## Designing the SKILL.md "dispatcher"

The SKILL.md body in a tiered system has one main job: route to the right reference.

Good dispatcher patterns:

**Explicit routing table:**
```markdown
## Which reference to read

| User says | Read |
|---|---|
| "make me a slideshow" | references/mp4_slideshow.md |
| "React video" or "Remotion" | references/remotion.md |
| "avatar video" or "HeyGen" | references/heygen.md |
```

**Decision tree in prose:**
```markdown
## Pick the format

Ask yourself:
1. Is this a talking-head format with a real face? → HeyGen. Read references/heygen.md.
2. Is this a programmatic composition with React? → Remotion. Read references/remotion.md.
3. Is this a photo-based slideshow with voiceover? → MP4 slideshow. Read references/mp4_slideshow.md.
```

Both work. Pick whichever flows more naturally with the skill's style.

---

## Mixing patterns

Large skills sometimes benefit from two levels of organization:

```
real-estate-content/
├── SKILL.md
└── references/
    ├── markets/
    │   ├── bay_area.md
    │   └── austin.md
    └── formats/
        ├── listing_video.md
        └── market_update.md
```

The dispatcher reads one from `markets/` and one from `formats/`. More complexity, but scales if you have >5 in each axis.

Don't do this for skills with <3 entries in an axis. It's overkill.
