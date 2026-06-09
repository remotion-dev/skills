# Trailer Brief Template

The skeleton for any cinematic trailer brief. Customize section by section. Don't skip the concept-lock section — every later phase depends on it.

---

## 1. Concept Lock

**Logline (one sentence):**  
*[Protagonist] has [stake] to [achieve goal]. [Force opposing them] is rising. They must [action] before [time runs out].*

**Dominant tone:** Suspense / Action / Romance / Other

**Anchor line** (the narrator delivers this at the resolution, 0:45–0:55):  
*"[The line the whole trailer earns.]"*

**End card line** (final text on screen):  
*"[The brand promise the viewer takes away.]"*

**Visual reference movies** (for PAI's grade reference):
- *Drive* (2011) — color and pacing
- *Sicario* — night/crisis grade
- *Ford v Ferrari* — gravitas/character

---

## 2. 8-Scene Beat Sheet (60s default)

| Time | Scene | Beat | Tone | Notes |
|------|-------|------|------|-------|
| 0:00–0:05 | 1 | Cold open / setup | Suspense | A face. A clock. Tension established. |
| 0:05–0:15 | 2 | Arrival | Suspense + action | Protagonist enters. |
| 0:15–0:20 | 3 | Strategy / preparation | Action | What they're going to do. |
| 0:20–0:25 | 4 | Hustle montage | Action | Quick cuts of effort. |
| 0:25–0:35 | 5 | Romance / emotional beat | Romance | The heart of the trailer. |
| 0:35–0:45 | 6 | Crisis | Suspense climax | Highest stakes. Often the dialogue moment. |
| 0:45–0:55 | 7 | Resolution | Emotional payoff | The anchor line lands here. |
| 0:55–1:00 | 8 | Title card | Brand | Tagline + CTA. |

---

## 3. Scene Prompts (for PAI)

For each scene, build a prompt that PAI 2.0 will accept. Structure:

```
Scene: [SETTING]. [TIME OF DAY]. [LIGHTING NOTES].

[CHARACTER NAME] from the reference images, [WARDROBE], [ACTION].

[VISUAL DETAILS — color, depth, lens flare, etc.]

Visual style: cinematic 35mm look, [COLOR DIRECTION], Drive (2011) cinematography reference. Photorealistic, [MOOD WORD - VISUAL not emotional].

CRITICAL: keep [CHARACTER]'s facial features identical to the reference images.

Generate a video clip, use Enhance mode.
```

**Key prompt rules:**

1. **Lead with the human action, not the setting.** PAI tends to interpret detailed settings as architectural shots.

2. **Avoid emotional adjectives.** "Tense," "suspenseful," "anxious," "intense" trip the content filter. Use visual mood words: "low-key lit," "soft afternoon light," "shallow depth," "contemplative expression."

3. **Always end with the character lock instruction.** PAI needs this every time, even with the character module loaded.

4. **Use "Enhance mode" for narrative scenes** (multi-shot decomposition). Use "Raw mode" for static title cards.

5. **Don't say "35mm anamorphic"** — it makes PAI auto-flip to 16:9 even on a 9:16 project. Say "35mm look" instead.

---

## 4. Voiceover Script

5 standard lines (4 narrator + 1 character dialogue). All wrapped in `<speak>` SSML tags with `<break>` tags for cinematic pacing.

```json
{
  "lines": [
    {
      "filename": "vo-01-cold-open.mp3",
      "text": "<speak>[Hook line at 0:00, short]. <break time=\"0.8s\"/></speak>",
      "voice": "narrator"
    },
    {
      "filename": "vo-02-arrival.mp3",
      "text": "<speak>[Stakes line at 0:05, longer, with <break time=\"0.5s\"/> dramatic <break time=\"0.4s\"/> pauses].</speak>",
      "voice": "narrator"
    },
    {
      "filename": "vo-03-buyer-found.mp3",
      "text": "<speak>[Romance beat narration at 0:25, quieter].</speak>",
      "voice": "narrator"
    },
    {
      "filename": "vo-04-dialogue.mp3",
      "text": "<speak>[Character spoken line at 0:35, the dialogue beat].</speak>",
      "voice": "graeham"
    },
    {
      "filename": "vo-05-resolution.mp3",
      "text": "<speak>[The anchor line at 0:45, the takeaway. <break time=\"0.6s\"/> Two-clause structure].</speak>",
      "voice": "narrator"
    }
  ]
}
```

---

## 5. Music Direction

**Genre:** Cinematic suspense, slow build, low strings, percussive hits.  
**Reference:** Cliff Martinez *Drive* main theme + Hans Zimmer *Interstellar* warmth.  
**Length:** Minimum 1:00, prefer 2:00+ for cutting flexibility.

**Cue map (60s trailer):**

| Time | Function |
|------|----------|
| 0:00–0:05 | Diegetic clock tick + single low piano note |
| 0:05–0:15 | Slow pulse, low strings, sub-bass |
| 0:15–0:25 | Adds percussion on cut hits |
| 0:25–0:35 | Softens to warm pad, birdsong |
| 0:35–0:45 | Returns harder, percussion, rain |
| 0:45–0:55 | Full swell, then silence |
| 0:55–1:00 | Final low piano note out |

For the ffmpeg editorial pass, the music gets ducked to 32% volume so the VOs cut through cleanly.

---

## 6. Color Grade Plan

- Scenes 1, 2, 3, 4, 5: `GRADE_WARM` (warm shadows, slight desaturation)
- Scene 6: `GRADE_COOL` (cooler shadows, more contrast, "night/crisis")
- Scene 7: `GRADE_HERO` (softer, preserves skin tones)
- Scene 8: no grade (title card pristine)

See `references/ffmpeg-grades.md` for the exact filter strings.

---

## 7. Character Reference Plan

For each named character that appears in 2+ scenes:

1. **Anchor photo** — clean front-facing reference.
2. **Look 1 keeper** — generate 4 variants in Higgsfield Nano Banana Pro, pick the strongest "looks like the user" choice.
3. **Look 1 close-up** — bootstrap from the keeper, generate 4 chest-up close-ups, pick the strongest.

Upload all 3 to PAI's character module before generating any scene.

---

## 8. Honest Reality Checks (tell the user before starting)

- **Character drift across scenes is unavoidable.** Editorial pacing (3-4s cuts) hides it.
- **Scene 5 is the most likely to miss the brief.** Plan to either regenerate or trim hard.
- **PAI's content filter will kill at least one scene.** Budget for 1–2 retries.
- **Music + VO + tight pacing = ~70% of the "epic" feeling.** Don't deliver raw clips.
- **Total cost: ~$30–50 in PAI credits + ~1.5–2 hours of orchestration time.**
