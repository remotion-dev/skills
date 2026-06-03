# PAI 2.0 Gotchas (Reference)

The full list of pitfalls hit during the "Last 47 Days" build. Every one of these cost time or credits or both. Read before driving PAI for the first time on any new project.

---

## 1. Content filter blocks emotional adjectives

**The trap:** Words like "tense," "suspenseful," "intense," "dread," "menace," "fear" trip a content policy filter on PAI's main video model. The render fails with `failed due to content policy filter`. Even softer language like "anxious" or "ominous" can trigger it.

**The fix:** Describe the **visual** mood instead of naming the emotion.

Bad:  
> "A tense, suspenseful 5-second clip of a woman who looks anxious..."

Good:  
> "A quiet, contemplative 5-second clip of a woman standing at a window in soft afternoon light, her face partially lit..."

**If you've already been blocked:** PAI offers "Retry as-is on the alternate video model" — this often works because the alt model has different content rules. Use that before rewriting the prompt.

---

## 2. PAI auto-overrides aspect ratio

**The trap:** When the prompt mentions "35mm anamorphic" or "cinematic widescreen," PAI auto-changes the clip's aspect to 16:9 — even if the project default is 9:16. You discover this when reviewing the Composed clip card and the aspect shows 16:9.

**The fix:** Before running, click on the clip node → change the Ratio dropdown from 16:9 back to 9:16. This must happen BEFORE clicking Run. There's no way to fix it after generation without re-rendering at full credit cost.

**Better fix:** Drop "35mm anamorphic" from prompts. PAI's cinematography reference ("Drive (2011)") already implies the look. Reference the grade and depth-of-field, not the lens format.

---

## 3. "Run" is a manual click on a small canvas node button

**The trap:** PAI's chat agent will compose a clip and tell you to "click Run on the canvas node." There is no Run button on the actual canvas node itself — it's at the **bottom-right of the composition detail panel** that appears when you click on the node. It's a small upward arrow icon, easy to miss.

**The location:** Open the failed/composed clip node on canvas → composition panel slides up from the bottom → look for the **up-arrow icon** at the bottom-right next to the credit count (e.g., "+220 ↑"). That's Run.

**Alternative:** Toggle "Auto-launch" in the bottom bar of the right-side chat panel. This makes PAI auto-spend and auto-render. BUT enabling it requires accepting an IP rights modal — that's a legal acknowledgment the user must explicitly approve. Don't click through it autonomously.

---

## 4. Don't ask again — the per-project credit confirmation

**The trap:** First credit spend in a project pops a "Spend credits?" modal with a "Don't ask again for this project" checkbox.

**The fix:** Check the box on the first spend. This eliminates the modal for every subsequent generation, saving 3+ clicks per scene.

---

## 5. Multi-shot prompts can fail decomposition

**The trap:** Prompts with explicit cuts ("CUT A: phone call. CUT B: hands on table. CUT C: silhouette at dusk.") sometimes result in PAI only rendering ONE of the three cuts — usually the first. The full montage doesn't appear.

**The fix:** Two paths:
- **Accept one shot.** Use the single shot PAI gave you as a represented montage beat — editorial pacing in the trailer will sell it.
- **Generate each cut as a separate scene.** Don't decompose in the prompt; instead, run 3 separate 1.5s generations for the three cuts. Stitch in editing.

---

## 6. Karen / female character lock is weaker than male

**The trap:** Even with a strong character lock for the protagonist (Graeham), supporting characters without reference images drift heavily. Karen looked like three different women across Scene 1 and Scene 7.

**The fix:** Either (a) generate a quick reference image for any character that appears in 2+ scenes — PAI's Scene 5 seed-image flow shows this works — or (b) accept the drift and use editorial tricks (close-ups, profile shots, silhouettes) to hide the inconsistency.

---

## 7. Karen at the hardwood floor — PAI literalism on romance beats

**The trap:** Romance / emotional beats describing the setting in detail get interpreted as architectural shots. The Scene 5 buyer-couple prompt described a "sunlit Bay Area kitchen with white oak floors and a marble island" — PAI delivered a 10-second shot of bare feet walking on hardwood floor. The human moment between Maya and Dev was gone.

**The fix:** Lead emotional beats with the human action and emotional state. Save the setting description for the last 20% of the prompt, not the first 60%.

Bad:  
> "A young couple in their early 30s walking slowly through a sunlit Bay Area kitchen with white oak floors and a marble island..."

Good:  
> "A long, restrained romantic beat between MAYA and DEV. She squeezes his hand. He nods, almost imperceptibly. The look between them says 'this is the one.' Setting: sunlit Bay Area kitchen, white oak floors, marble island in background. Two-shot, medium framing, shallow depth of field."

Put the EMOTIONAL action first. Setting last.

---

## 8. Scene 1 cold open is the most likely scene to fail

**The trap:** Cold opens tend to be moody, slow, contemplative — which means the prompts use mood words ("contemplative," "still," "watchful") that brush the content filter. Across two builds, Scene 1 failed first twice.

**The fix:** Write Scene 1's prompt with extra visual focus. Describe the **light**, the **camera move**, and the **physical action** in detail. Leave mood for the cinematography reference at the end.

---

## 9. URL extraction from canvas requires clicking each node

**The trap:** PAI's canvas view doesn't expose video URLs in the DOM until you click the node. JavaScript scraping returns empty arrays.

**The fix:** Click each rendered node to load its video into the detail player, then run:
```javascript
[...new Set([...document.querySelectorAll('video')].map(v => v.src || v.currentSrc).filter(Boolean))]
```

Or, in the Video / Timeline tab, click each thumbnail in the strip — each click loads a new URL into the main player. Capture each one.

See `scripts/extract_and_download.py` for the helper that automates this loop.

---

## 10. PAI's "Don't ask again" doesn't extend to retries on the alternate model

**The trap:** Even after enabling "Don't ask," a content-filtered scene that gets retried on the alternate model spawns a fresh "Continue Anyway?" modal that needs explicit confirmation.

**The fix:** Just click through it when it appears. The acknowledgment is per-flag, not per-project.

---

## Summary: a clean PAI run takes ~3 spent-credit clicks per scene

For each scene:
1. Click Spend X credits on the chat confirm card
2. (If content filter trips) Click Retry as-is on alternate model
3. (If alternate model) Click Run on the canvas node

Plus 1 cross-checking click when the final scene renders, to confirm it's actually done.

Average ~3,000–3,500 PAI credits per 60s trailer with one or two retries baked in.
