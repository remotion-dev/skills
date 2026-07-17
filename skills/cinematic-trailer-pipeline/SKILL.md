---
name: cinematic-trailer-pipeline
description: End-to-end cinematic trailer production pipeline for Graeham Watts — from concept to finished MP4. Use ANY time the user mentions cinematic trailer, movie trailer ad, epic trailer, 60-second trailer, brand trailer, narrative video with VO, Drive-style video, Sicario-style trailer, multi-scene story video, "make me a trailer," "build a trailer," "trailer for my brand," "movie ad," "epic ad," or any request for a polished cinematic short-form video with narration, music, and a story arc. Also trigger when user wants to combine AI video generation (PAI / UTOPAI), ElevenLabs voiceover, and music into one finished piece. Encodes the full pipeline we built and the painful lessons learned — PAI content filter pitfalls, character drift workarounds, the editorial pass with color grade + music duck + VO mix, proper trailer pacing. Over-trigger — if the request smells like "epic cinematic video with a story," use this.
---

# Cinematic Trailer Pipeline

> The complete brand-trailer production system for Graeham Watts. Codifies the full workflow from concept to finished MP4. Built from the lessons of building "The Last 47 Days" — what worked, what failed twice, and the editorial craft that saved it.

---

## When to use this skill

Use this any time the user wants a **cinematic short-form video with narrative structure** — typically a 30–90 second piece with:

- A story arc (setup → tension → climax → resolution)
- Multiple distinct scenes / shots
- Voiceover narration
- Music bed and sound design
- A title card / brand drop

Examples:
- "Make me a cinematic movie trailer ad. I want to be the star."
- "I want a Drive-style brand trailer for my real estate business."
- "Build me an epic 60-second video about [topic]."
- "Make a narrative video about [client situation] with my voice."

If the user wants a single talking-head video, route to `heygen-video` instead. If they want b-roll only, route to `higgsfield-video`. This skill is specifically for **multi-scene narrative trailers**.

---

## The full pipeline (5 phases)

```
Phase 1: Concept Lock           → Tagline, dominant tone, 60s beat sheet
Phase 2: Character Refs         → Higgsfield Nano Banana Pro keepers
Phase 3: AI Video Generation    → PAI 2.0 (or fallback)
Phase 4: Voiceover              → ElevenLabs (narrator + Graeham clone)
Phase 5: Editorial Pass         → ffmpeg cut + color grade + music + mix
```

Each phase has its own section below. Don't skip phases — they build on each other.

---

## Phase 1: Concept Lock

Before any generation, pin down four things. Use `references/brief-template.md` as the skeleton.

1. **Dominant tone.** Suspense-led usually wins for real estate. Action gets saturated fast (every realtor with AI tools made a Bond reel in 2025). Romance differentiates but underdelivers the "epic" feeling. The brief template defaults to suspense.

2. **The anchor line.** One memorable sentence that the whole trailer earns. For "The Last 47 Days" this was: *"The story doesn't end the way it starts. It ends the way it's directed."* The narrator delivers this at the resolution moment (usually 0:45–0:55).

3. **The end card line.** What the viewer takes away. For the 47 Days piece: *"Selling your home is the highest-stakes story you'll ever live. I make sure it ends the way you wanted."*

4. **The 8-scene beat sheet.** Write this out at minute-level granularity. Default structure for a 60-second trailer:

| Time | Beat | Tone |
|------|------|------|
| 0:00–0:05 | Cold open (setup, tension) | Suspense |
| 0:05–0:15 | Arrival of protagonist | Suspense + action |
| 0:15–0:20 | Strategy / preparation | Action |
| 0:20–0:25 | Hustle montage | Action |
| 0:25–0:35 | Romance / emotional beat | Romance |
| 0:35–0:45 | Crisis / climax | Suspense climax |
| 0:45–0:55 | Resolution / emotional payoff | Resolution |
| 0:55–1:00 | Title card + CTA | Brand |

Adjust durations for shorter trailers (30s = compress each beat by half, drop one beat). For longer (90s+), expand the action and crisis sections.

---

## Phase 2: Character Refs (Higgsfield Nano Banana Pro)

Why this matters: **PAI 2.0's character module is only as good as the reference image you give it.** A great selfie produces about a 25% face-match hit rate. Bootstrapping from a "keeper" first reference gets that to 75%+.

Workflow:
1. Start with a clean, front-facing, well-lit anchor photo of the user.
2. In Higgsfield, open Nano Banana Pro, upload anchor, generate 4 variants of the user in **Look 1** (the dominant wardrobe — usually formal/overcoat for real estate trailers).
3. The user picks the keeper that "looks like them" (the user's eye is better than ours — proven twice this session).
4. Download the keeper as a JPG.
5. **Bootstrap technique:** Re-upload the keeper as the NEW seed photo. Generate 4 more variants at a TIGHTER framing (chest-up close-up). NBP locks much better when the seed is already in the target style.
6. Take the strongest 2 chest-up close-ups as the final ref material for PAI.

**Reusable Higgsfield prompt template (Look 1 — formal arrival):**

> Cinematic photograph of the man from the reference image. Late 30s, neat short dark brown hair, light olive skin, clean-shaven. Wearing a [WARDROBE]. Standing in front of a [SETTING] at golden hour. Medium shot, three-quarter angle. Warm key light from camera left, soft fill, subtle anamorphic lens flare. Calm, watchful, deliberate expression. Cinematography reference: Drive (2011), warm shadows, slightly muted teal midtones. Shallow depth of field. Photorealistic, 35mm film look, subtle grain.

For Look 2 (different mood/wardrobe), keep the camera direction same, change wardrobe + setting + lighting style.

**Output:** 3 reference images (anchor selfie + Look 1 keeper + Look 1 close-up) in `Downloads/<project>/refs/`.

---

## Phase 3: AI Video Generation (PAI 2.0)

PAI is the strongest narrative continuity tool, but it has pitfalls we hit hard tonight. See `references/pai-gotchas.md` for the full list. Top 3 you MUST know:

1. **Content filter blocks emotional adjectives.** Words like "tense," "suspenseful," "intense," "dread," "fear" trip a content policy filter that kills the render. Describe the *visual* mood instead: "low-key lit, quiet pacing, soft afternoon light, contemplative expression." Don't name the emotion.

2. **PAI auto-overrides aspect ratio.** When you mention "35mm anamorphic" in a prompt, PAI auto-switches to 16:9 even if the project is set to 9:16. Fix on the canvas node settings BEFORE running, or you waste 440 credits on the wrong aspect.

3. **"Run" requires a manual click on the canvas node.** PAI's chat will compose and ask for confirmation, then say "click Run on the canvas node." The Run button is the small up-arrow at the bottom-right of the composition panel. Auto-launch toggle is in the bottom bar of the chat — but enabling it requires accepting their IP rights modal, which is a per-action authorization the user must give.

**Standard project setup:**
- Aspect: 9:16 vertical for social trailers (most common)
- Quality: Pro 1080p (44 credits/sec → ~440 credits per 10s scene)
- Mode: Enhance (multi-shot decomposition) for narrative scenes; Raw for title cards
- Character module: upload all 3 ref images

**Per-scene prompt structure:**
- Lead with: "Scene: [setting]. [time of day]. [lighting]."
- Add: "Character [name] from the reference images, [wardrobe], [action]."
- Visual style: "Cinematic 35mm look, [color direction], Drive (2011) cinematography reference."
- Character lock: "CRITICAL: keep [name]'s facial features identical to the reference images."
- End with: "Generate a video clip, use Enhance mode." (or Raw for title cards)

**Cost estimate:** ~3,000 credits per 60s trailer assuming each scene runs first-try. Budget 50% more for retries. The Scene 1 / cold open is most likely to trip content filters — write it visually-focused first time.

**Extraction:** After all 8 scenes render, extract URLs via Chrome console JS:
```javascript
[...new Set([...document.querySelectorAll('video')].map(v => v.src || v.currentSrc).filter(Boolean))]
```
Then bash download. See `scripts/extract_and_download.py` for the helper.

---

## Phase 4: Voiceover (ElevenLabs)

**Two voices, one rule:** narrator voice for the cinematic frame, the user's clone for character dialogue. Don't try to use the clone for the entire narration — it sounds robotic because cloned voices are tuned for natural conversation, not trailer narration.

**Standard voice selections:**
- **Narrator:** Brian (`nPczCjzI2devNBz1zQrb`) — ElevenLabs stock, deep, measured, the closest thing to a film-trailer voice in the library. Alternatives: George (more British/gravelly), Adam (deeper/weightier). Let the user choose if they have a preference.
- **Graeham's voice clone:** `Pa3vOYQHHpLJn1Tf7hnP` — use for the character's actual spoken dialogue inside the story (e.g., the Scene 6 phone call line).

**Voice settings — these are the ones that work:**
- Narrator (calm/measured trailer voice): `stability=0.40, similarity_boost=0.80, style=0.55, use_speaker_boost=true`
- Graeham clone (natural dialogue): `stability=0.35, similarity_boost=0.85, style=0.50, use_speaker_boost=true`
- **Do NOT** use stability > 0.60 — that's what made the v1 clone sound robotic. Lower stability = more variation = more natural.

**Use `<break time="0.X" />` tags for cinematic pacing.** ElevenLabs honors these on `eleven_multilingual_v2`. They give you deterministic pause control. Don't use `<prosody>` — silent pass-through.

**Generation script:** `scripts/synthesize_vos.py` — pass a JSON config with 5 lines, voice IDs, settings, output paths. Reads the API key from `~/Documents/Skills LLMS/Claude/Skills/.heygen-credentials/elevenlabs-key.txt`.

---

## Phase 5: Editorial Pass (the part that makes it land)

**This is where the trailer goes from "AI footage with VO" to actually epic.** The PAI clips alone are too long, the colors don't match between scenes, and there's no music. The editorial pass fixes all three.

### What an editor actually does here

1. **Re-time every shot.** PAI gives you 5–10s shots. A trailer needs 2–4s shots. Trim to the meaningful moment in each, drop the setup tail.
2. **Apply a unifying color grade.** PAI's scene-by-scene color is inconsistent. One LUT across everything (warm shadows, slight teal midtones, light vignette) pulls the trailer into one visual world.
3. **Music bed at ~30% volume.** Music carries the emotion. Dial it under the VO so the words still cut through, but the score does the heavy lifting between lines.
4. **VO mix at 1.4–1.7x.** Narrator at 1.4x, character dialogue at 1.6–1.7x for punch.
5. **Brick-wall limiter on master** to catch any peak.

### Standard cut sheet (60s source → ~40s trailer)

| Scene | Source duration | Trim in | Trim out | New duration | Notes |
|-------|----------------|---------|----------|--------------|-------|
| 1 | 5s | 0.5 | 4.5 | 4s | Hold on the cold open beat |
| 2 | 10s | 2 | 6 | 4s | Just the meaningful action |
| 3 | 5s | 1 | 4 | 3s | Quick insert |
| 4 | 5s | 0 | 3 | 3s | Quick insert |
| 5 | 10s | 5 | 10 | 5s | Skip the weakest first half |
| 6 | 10s | 1 | 9 | 8s | Hold for dialogue + reaction |
| 7 | 10s | 2 | 10 | 8s | Hold for emotional payoff |
| 8 | 5s | 0 | 5 | 5s | Full title |
| **Total** | **60s** | | | **40s** | Tighter = punchier |

Adjust per project. The 40s target is good for social. For longer-form web video, keep more breathing room (50s).

### Color grade presets (ffmpeg)

Three grades defined in `references/ffmpeg-grades.md`:
- **Standard warm** (Scenes 1–5, 7): `colorbalance=rs=.06:bs=-.08,eq=contrast=1.10:saturation=0.92:gamma=0.96,vignette=angle=PI/5`
- **Cool crisis** (Scene 6): `colorbalance=rs=.04:bs=.02,eq=contrast=1.15:saturation=0.85:gamma=0.92,vignette=angle=PI/5`
- **Hero soft** (Scene 7, alternative): `colorbalance=rs=.05:bs=-.05,eq=contrast=1.08:saturation=0.95:gamma=0.97,vignette=angle=PI/5`
- **Title card**: no grade (PAI nails text cards as-is)

### Music sourcing

**For a finished public deliverable, use these in order of preference:**

1. **CapCut library** — if the user is doing the final edit in CapCut, search their cinematic music section. Strong titles: "Cinematic Trailer (Full Version)" by makesound, "Epic Drama Cinematic Trailer" by RomanSenykM, "An intense cinematic..." by Ryuichiro Yamamoto. License is bundled with CapCut export.
2. **Pixabay Music** — free, no attribution required, can download MP3 directly. Search "cinematic trailer" or "cinematic suspense." Best for when we're rendering the final externally (ffmpeg/Resolve).
3. **Artlist or Musicbed** — paid (~$30/track) but highest quality and intended for commercial cinematic use.

For ffmpeg-rendered trailers, default to Pixabay. The script in `scripts/download_music.py` has 3 known-good Pixabay cinematic trailer URLs as defaults.

### The full editorial render

Use `scripts/editorial_pass.sh`. It takes:
- 8 scene MP4s (named scene1.mp4 through scene8.mp4)
- 5 VO MP3s (vo-01 through vo-05)
- 1 music track MP3
- A target output path

It produces a graded, cut, mixed, limited final MP4. The script is broken into two halves to beat sandbox timeout limits — render Part 1 (scenes 1-4) and Part 2 (scenes 5-8) separately, then concat + mix audio.

---

## Honest reality checks (tell the user these upfront)

1. **Character drift across scenes is unavoidable.** Even with bootstrapped refs, you'll get 2–3 versions of the user's face across 8 scenes. **The fix is editorial:** fast cuts (under 4s each), lean on silhouettes and close-ups where the face is less recognizable, use a unifying color grade to mask differences.

2. **Scene 5 (buyer / romance beat) is most likely to miss the brief.** PAI tends to over-emphasize architectural shots (hardwood floors, marble counters) and underdeliver on the human moment. Plan to either regenerate Scene 5 with more aggressive human-focused prompting, or accept it and use editorial trimming to hide the worst part.

3. **PAI's content filter will kill at least one scene per trailer.** Budget for 1–2 retries on the alternate model. The cold open (Scene 1) is most vulnerable because it sets tension.

4. **Music + VO + tight pacing = ~70% of the "epic" feeling.** AI video alone, no matter how good, will not feel epic without these three elements. Do not deliver the trailer with just clips assembled — always do the editorial pass.

5. **Total cost estimate:**
   - PAI credits: ~$30–50 per trailer
   - ElevenLabs: pennies (we're well under the monthly char limit)
   - Music: $0 (Pixabay) or $30 (Artlist)
   - Time: 1.5–2 hours end-to-end if everything runs first-try; 3–4 hours with retries

---

## Files in this skill

- `SKILL.md` — this file (you are here)
- `scripts/synthesize_vos.py` — ElevenLabs VO generation for the 5 standard trailer lines
- `scripts/editorial_pass.sh` — the ffmpeg cut + grade + mix pipeline
- `scripts/download_music.py` — known-good Pixabay cinematic trailer URLs + downloader
- `scripts/extract_and_download.py` — PAI clip URL extraction + download helper
- `references/brief-template.md` — the 8-scene trailer brief structure with prompts
- `references/pai-gotchas.md` — full list of PAI 2.0 pitfalls and fixes
- `references/ffmpeg-grades.md` — color grade presets + when to use each

---

## Hand-off contract

**Upstream:** user request mentions "cinematic trailer," "epic trailer," "narrative video," or similar.

**Downstream:** finished MP4 in `Downloads/<project-slug>/TRAILER-DIRECTORS-CUT.mp4` plus a folder of source assets (8 scene clips, 5 VOs, 1 music track, 3 character refs, brief.md).
