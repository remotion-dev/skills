# YouTube Script Template (Principles-First)

> Use this template whenever writing a YouTube long-form script (4-8 min BOFU, 8-15 min edutainment). All four principles from `philosophy.md` apply — this template operationalizes them.

## Structure

### Hook (0:00–0:20)
**Rule:** consequence-first. Open with what's wrong / what the viewer is missing.

- Sentence 1: the paradox or charged statement (e.g., "They called this the most dangerous city in America.")
- Sentence 2: the update (e.g., "That was 1992. Today they just hit 2 years homicide-free.")
- Sentence 3: the promise (e.g., "And if you've been skipping EPA because of a 90s headline, this is the 4 minutes that'll change your math.")

### Segment 1 — Story setup (0:20–1:15)
**Rule:** story over explanation. Put the viewer in a specific moment.

- Personal story or archival scene
- What the listener probably believes going in
- A crack in that belief — the "but here's what changed"
- **Retention cliff:** last 2 sentences must make Segment 2 feel irresistible

### Segment 2 — Data reveal (1:15–2:30)
**Rule:** escalating stakes — this segment is about money now.

- Specific numbers (with sources — MLS, GSC, official data)
- Comparison that makes the number matter (e.g., "EPA +1.7% YoY vs SMC -7.2% — the widest spread in a decade")
- Visual/motion-graphic cue implied in the script
- **Retention cliff:** "but here's what that MEANS for YOU…"

### Segment 3 — Personal application (2:30–3:45)
**Rule:** higher stakes — it's about their specific situation now.

- Address two audience types: buyers, sellers (or buyers + homeowners + investors depending on topic)
- What each should DO with this information
- A second personal story or brief scenario illustrating the application
- **Retention cliff:** "and if you don't act in the next [window], here's what happens…"

### CTA (3:45–4:30)
**Rule:** one ask, clear reward.

- Refer back to the charged statement from the hook
- State the reward for engaging (comment keyword → get full report)
- Lead capture: comment keyword (EPA, COSTS, SELL, etc.) mapped to GoHighLevel
- Personal sign-off (name, role, market)

### End card (4:30–4:34)
- Graeham branding, 3-4 second hold
- Subscribe / follow prompt if channel growth is a goal

## Required elements check (before shipping)

- [ ] Consequence-first hook (not "today we're going to talk about…")
- [ ] Story over explanation (at least 2 personal stories or scenarios)
- [ ] Escalating stakes (each segment stakes > previous)
- [ ] Retention cliff at each segment boundary
- [ ] 3 key learnings identified and recapped in CTA
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
