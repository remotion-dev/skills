# YouTube Script Template (Principles-First)

> Use this template whenever writing a YouTube long-form script (4-8 min BOFU, 8-15 min edutainment). The four principles below are **parallel rules that ALL apply throughout the whole script** — not a rule per segment. You check every segment against every principle.

## The four principles (equally weighted, always applied)

### 1. Consequence-first
Every segment asks: what does the viewer LOSE if they don't know this? Safe content gets ignored — risk creates attention. Applies in the hook (strongest), reinforced in data reveal, personalized in application, made explicit in CTA. Every segment should have some stakes visible.

### 2. Story over explanation
Don't list features — write scenes. Put the viewer in a specific moment. Applies to every segment: the hook has a story, the data reveal has a scenario that makes the number tangible, the application has a personal case, the CTA has a "here's what happens next."

### 3. Escalating stakes
Each segment must feel HIGHER-stakes than the previous. If stakes flatten, viewers leave. This is a cross-cutting principle — you compare segment N against segment N-1 and ask "does this feel bigger?" If no, restructure.

### 4. Retention cliffs at segment boundaries
The last 2-3 sentences of every segment must make the next segment feel irresistible. This is where viewers decide to stay or leave. Applies to every segment boundary, including the entry to the CTA.

**Critical:** you don't apply these in sequence. You apply all four to every segment, and the script is done when every segment passes every check.

---

## Structure (what goes where)

### Hook (0:00–0:20)
- Paradox or charged statement
- The update (what's changed)
- The promise (what they'll learn in X minutes)

**Principle check:** consequence-first (strongest here), story (specific moment), stakes (curiosity/money at risk), cliff (leads to segment 1).

### Segment 1 — Story setup (0:20–1:15)
- Archival scene or personal story
- What the listener probably believes going in
- A crack in that belief

**Principle check:** consequence (what they lose by holding this belief), story (specific scene), stakes (≥ hook), cliff (leads to data).

### Segment 2 — Data reveal (1:15–2:30)
- Specific numbers with sources
- Comparison that makes the number matter
- Visual/motion-graphic cue

**Principle check:** consequence (money at stake), story (put them in the data moment), stakes (≥ segment 1), cliff (leads to application).

### Segment 3 — Personal application (2:30–3:45)
- Address 2 audience types (buyers + sellers, etc.)
- What each should DO with this information
- A second personal scenario

**Principle check:** consequence (their specific house, their specific move), story (case study), stakes (≥ segment 2), cliff (leads to CTA).

### CTA (3:45–4:30)
- Refer back to the charged statement from the hook
- State the reward for engaging (comment keyword → report)
- Lead capture mapped to GoHighLevel
- Personal sign-off

**Principle check:** consequence (what happens if they DON'T act), story (imagine doing X), stakes (highest — the viewer is about to decide), cliff (action, not another video).

### End card (4:30–4:34)
Graeham branding, 3-4 second hold.

---

## Required elements check (before shipping)

- [ ] Every segment passes consequence-first (viewer feels loss if they don't know this)
- [ ] Every segment uses story over explanation (scene, not list)
- [ ] Every segment stakes > previous segment (no flattening)
- [ ] Every segment boundary has a retention cliff
- [ ] 2 personal stories or scenarios (minimum, more welcome)
- [ ] 3 key learnings identified + recapped in CTA
- [ ] 1 signature analogy that makes the complex thing simple
- [ ] Numbers sourced (MLS / GSC / news URL)
- [ ] Fair Housing compliant (no demographic framing, no school rankings)
- [ ] Single CTA with clear reward
- [ ] ElevenLabs-ready SSML tags (`<prosody>`, `<break>`)

## SSML annotation standards

Use v2 break tags inline: `<break time="400ms"/>`
Use prosody for emphasis sparingly: `<prosody rate="slow">[critical number]</prosody>`
Never over-annotate — ElevenLabs reads clean text better than over-tagged text.

## B-roll annotation

In the script, mark:
- `[TALKING HEAD]` — Graeham on camera
- `[TH CUTBACK]` — cut back to TH from B-roll
- `[CUT TO: <description>]` — B-roll insert
- `[TEXT OVERLAY: "<text>"]` — on-screen title card
- `[MOTION GRAPHIC: <description>]` — animated data viz

These annotations hand off to the Production Brief (for Jason, the editor).

## Timing math

Always calculate duration as:
```
word_count ÷ 150 WPM × 1.15 (pause/B-roll buffer) = target_minutes
```

Print this math in the final script so Peter (publisher) can verify.
