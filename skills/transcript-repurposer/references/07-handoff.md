# Phase 7 — Production Handoff

The content package from Phase 6 is the script. This phase formats production-ready handoff blocks so Graeham can move directly from script to render in HeyGen and Higgsfield with no manual translation work.

Produce three handoff blocks in this order. Append them to the content package.

## A. HeyGen-Ready Script Block

HeyGen takes plain script text + an avatar look + a voice. The skill `heygen-video` handles the render — this block prepares everything that skill needs.

**Important:** The HeyGen skill is built around Graeham confirming the avatar look on every video. Do NOT pick silently. Recommend 2-3 looks with rationale; let Graeham choose.

### Avatar Look Recommendation Logic

Match the topic and tone of the script to the appropriate look. Reference `heygen-video/references/avatars.md` if accessible. Default recommendation matrix:

| Topic / Tone | Recommended look | Aspect |
|---|---|---|
| Listing intro, personalized client message | `digital_twin` | 9:16 |
| Approachable everyday content, buyer onboarding | `casual_chic` | 9:16 |
| Polished seller content, CMA presentation | `freshly_ironed` | 9:16 |
| Higher-energy content, variety | `fashion_flip` | 9:16 |
| Market data, buyer education, **Vaibhav-style** | `warm_desk_navy` | 16:9 |
| Neighborhood features, horizontal content | `suburban_serenity` | 16:9 |
| Podcast / longform conversation tone | `podcast_studio` | 16:9 |
| Aspirational / luxury angle | `loft_window` | 16:9 |
| Corporate / professional formal | `corporate_office` | 16:9 |
| Clean studio look | `modern_studio` | 16:9 |

### Block Format

```
## HeyGen-Ready Script

Recommended look (primary): <look_name>
Rationale: <one line — why this look fits the topic/tone>
Aspect: <9:16 portrait | 16:9 landscape>

Recommended look (backup): <look_name>
Rationale: <one line>
Aspect: <9:16 | 16:9>

Voice: Voice Clone (default — locked at 717249201f7745988219b9aeb9041b42)

Script (paste-ready, shot tags removed):
"<the script as paste-able plain text>"

Note for Graeham: HeyGen will ask which look to use. Paste the avatar look ID from the primary recommendation, or name a look from the known set. Voice defaults to your clone automatically.
```

The script text in this block is the SAME script from Phase 6 but with all `[TALKING HEAD]`, `[B-ROLL]`, `[TEXT OVERLAY]`, `[CAPTION OVERLAY]` tags stripped — because HeyGen reads the script directly as spoken text. The tags belong in the editing notes for Jason, not in the HeyGen mouth.

## B. Higgsfield B-Roll Prompt Pack

For every `[B-ROLL: ...]`, `[DRONE: ...]`, or scene-change indicator in the YouTube Long script, generate a paired image + motion prompt.

### Why two prompts per clip

Higgsfield uses a two-stage pipeline:
1. **Nano Banana Pro** generates a 4K still frame from the image prompt.
2. **Seedance 2.0 or Kling 3.0** animates that still into a video clip using the motion prompt.

We need both. The image prompt controls composition, lighting, mood. The motion prompt controls camera move and animation.

### Nano Banana Pro — Realism Anchor Stack

Reference `higgsfield-video/SKILL.md` Realism Rescue Protocol. Graeham's default anchor stack for real estate:

```
Style anchor: Gray Malin + Douglas Friedman + Kodak Portra 400
```

That gives warm, cinematic, aspirational aesthetic without the obvious-AI-render look. Use it as the baseline for any luxury / lifestyle / real estate b-roll.

For place-specific shots (recognizable Peninsula geography), follow the anonymization strategy in the Higgsfield skill — don't try to render specific real buildings, render the *vibe* of the location.

### Seedance / Kling Motion Vocabulary

Cinematic motion descriptors that work well:
- `slow dolly forward`
- `slow dolly back`
- `aerial drone shot, slow pan left`
- `static, golden hour lighting shift`
- `handheld walk-through`
- `slow orbit around subject`
- `tracking shot following [subject]`
- `time-lapse [duration]`
- `rack focus from foreground to background`

Avoid: anything involving fast camera moves, complex character action, fingers/hands close to camera, text in the scene. Those break the model.

### Block Format

```
## Higgsfield B-Roll Prompt Pack

For each [B-ROLL] / [DRONE] tag in the YouTube Long script:

---
B-ROLL #1 — Use at [00:08-00:13]
Image prompt (Nano Banana Pro):
"Cinematic shot of <subject>, <composition details>, <lighting>, in the style of Gray Malin meets Douglas Friedman, Kodak Portra 400 film aesthetic, warm color grading, shallow depth of field, 4K"

Motion prompt (Seedance 2.0):
"<camera move>, <duration>, <lighting consistency note>"

Duration: <5s | 10s | 15s>
Aspect: <9:16 | 16:9>
Use in edit: <where this clip goes — timestamp range, what it cuts to/from>

---
B-ROLL #2 — Use at [00:23-00:28]
...
```

Generate one B-Roll block per shot direction tag in the script. If the script has 4 `[B-ROLL]` tags and 1 `[DRONE]` tag, generate 5 blocks.

### Tip — Don't over-generate

If the YouTube Long has 25 shot tags, that's 25 Higgsfield generations at ~140 credits each = 3500 credits = expensive. Cap the B-roll prompts at ~6-8 per long-form video. For the highest-leverage shots:
- Hook shot (first 2-3 seconds)
- Big stat callout backdrop
- Section transitions
- CTA backdrop

The rest can be edited from existing footage Jason already has.

## C. ElevenLabs SSML Block

For Phase 6 we already produced an SSML block for YouTube Long. This handoff block is the same one, copy-pasteable, with one addition: voice settings recommendations.

```
## ElevenLabs Voice Settings

Voice: <Graeham's ElevenLabs voice ID — Graeham will fill in if not stored>
Stability: 35-45% (lower = more emotion variance, higher = more consistent)
Similarity Boost: 75-85% (higher = sounds more like reference, lower = more dynamic)
Style: 20-30% (higher = more expressive)
Speaker Boost: ON

Notes:
- Stability lower (35%) for short-form energy
- Stability higher (45%) for long-form clarity
- Adjust per derivative

---

SSML (paste into ElevenLabs):

<speak>
... full SSML block from Phase 6 ...
</speak>
```

## Combined Output

The handoff block appended to the content package should look like:

```
## Production Handoff

### A. HeyGen-Ready
<HeyGen block>

### B. Higgsfield B-Roll Pack
<6-8 B-roll prompts>

### C. ElevenLabs SSML
<settings + SSML>
```

Hand the full content package (Phase 6 + Phase 7) to Phase 8 — humanizer pass.

## Quick Reference — Handoff Skill Map

| Output | Goes into | Skill |
|---|---|---|
| HeyGen-Ready Script | HeyGen render | `heygen-video` |
| Higgsfield image + motion prompts | Higgsfield two-stage gen | `higgsfield-video` |
| ElevenLabs SSML | ElevenLabs voice | (manual paste — no skill yet) |
| Vaibhav-template aesthetic | Vaibhav-style render | `vaibhav-template` (then `heygen-video`) |

If Graeham wants the Vaibhav aesthetic, chain to `vaibhav-template` AFTER this skill — that skill takes the script + look and applies the visual system on top.
