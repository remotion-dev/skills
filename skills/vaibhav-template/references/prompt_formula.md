# Prompt Formula — Generating New Warm-Desk Looks

This reference captures the exact prompt structure that produces identity-matched Graeham looks via Higgsfield's Nano Banana Pro model. Use this when adding a 6th+ look to the rotation, or regenerating any of the existing 5.

## The four non-negotiables

Every warm-desk look prompt must include these four blocks, in this order:

### Block 1 — Identity lock (opens the prompt)

```
Photorealistic portrait matching the reference image face exactly. Same man 
from the reference image — identical face shape, identical chin with smooth 
rounded contour and absolutely no vertical cleft dimple or crease in the 
chin, identical jaw contour, identical nose shape, identical eyes, identical 
hairline and hair, identical complexion and skin tone. Match every facial 
feature from the reference photo precisely including the smooth uncleft chin.
```

**Why this exact wording:** Nano Banana Pro has a documented bias toward adding chin clefts to white/Caucasian male subjects regardless of reference. Direct negation ("no vertical cleft dimple or crease") reduces but does not eliminate the drift. The redundant closing clause ("including the smooth uncleft chin") reinforces it. Expect ~30-40% improvement over prompts without this block; full elimination is not achievable with prompt engineering alone.

### Block 2 — Camera + desk orientation

```
Camera positioned directly in front of the desk at eye level, square-on to 
the subject. Desk runs horizontally across the bottom edge of the frame, 
perpendicular to the camera, extending left-to-right, not diagonally. He is 
centered in frame, shoulders square to camera, facing camera head-on.
```

**Why this exact wording:** Without explicit camera placement, Nano Banana defaults to 45° angled compositions where the desk extends diagonally away from camera. The "perpendicular" + "horizontally across the bottom" + "not diagonally" triplet is the minimum needed to force Vaibhav's head-on composition. Repetition is necessary — single-mention of "perpendicular" alone fails ~50% of the time.

### Block 3 — Outfit (varies per look)

Describe the full outfit in a single sentence. Be specific about material, fit, and layering. Add glasses as a separate sentence if applicable.

**Known-good outfit descriptors:**
- `"navy blue quarter-zip pullover over a white crewneck tee"` → warm_desk_navy
- `"black crewneck sweater"` → podcast_studio
- `"heather grey long-sleeve henley shirt with the top two buttons undone at the collar"` → loft_window
- `"tailored charcoal grey wool suit jacket over a crisp light blue dress shirt with a navy blue silk necktie knotted neatly at the collar"` → corporate_office
- `"crisp white oxford button-down shirt with the sleeves rolled neatly up to just below the elbows, no tie, no jacket, top button undone"` → modern_studio

**Glasses spec (when used):** `"modern clear round wire-frame glasses"`. Use the **same frame style across all looks that include glasses** — consistency makes them a recognizable signifier rather than visual noise.

### Block 4 — Environment + lighting + props

Describe background as heavily-blurred context, never competing with the face. Include:
- Wall/surface treatment (wood paneling, concrete, acoustic foam, seamless backdrop)
- A practical light source (lamp, window glow)
- 1-2 desk props max (laptop, notebook, coffee cup, fountain pen)
- Explicit instruction: `"His face is the brightest and sharpest element in frame."`

## Words to AVOID (identity-drift risks)

These words pull Nano Banana toward stock-photo "handsome-man" features (chin clefts, exaggerated jawlines, dramatic styling) and away from the reference:

- `angular` — triggers chin cleft + sharp jaw exaggeration
- `confident` / `bold` / `strong` — triggers chin cleft + "stock photo" face
- `chiseled` / `sculpted` — obvious
- Photographer style references: `Douglas Friedman`, `Peter Lindbergh`, `Richard Avedon` — these bleed the photographer's signature face style

**Safe style references:**
- `Kodak Portra 400` (film stock — no face bias)
- `cinematic warm color grading` (tonal, not structural)
- `editorial magazine quality` (generic enough to not overfit)

## Generation settings (Higgsfield UI)

- Model: **Nano Banana Pro**
- Aspect: **16:9** (landscape — all 5 looks are landscape-native)
- Quality: **4K** (5504×3072)
- Variants: **4/4** per batch
- Reference image: drag-and-drop the anchor selfie (`IMG_0520.JPG` or equivalent clean front-facing headshot). **The `file_upload` browser tool fails** — only drag-drop from File Explorer works.
- Cost: 16 credits per 4-variant batch

## QC checklist before downloading a hero

Verify each of these on the candidate before saving:

- [ ] Camera is directly in front of the desk (not angled)
- [ ] Desk runs horizontally across the bottom, perpendicular to camera
- [ ] Shoulders are square to camera, subject is centered
- [ ] Outfit matches the spec exactly (color, garment type, layering, glasses if applicable)
- [ ] Lamp/practical light is positioned as prompted (foreground ≠ background)
- [ ] Face is the brightest and sharpest element in frame
- [ ] Chin looks as smooth as possible (know the AI bias — pick the variant with the least cleft)
- [ ] Hair, stubble, eyes, nose, complexion all match reference
- [ ] Background is heavily blurred and doesn't compete with face

If a batch fails on more than two points, rewrite the prompt rather than rolling another 16-credit batch blindly.

## The technical Higgsfield UI gotcha

When typing a new prompt after clearing the old one, Chrome's `ctrl+a` on Higgsfield's contenteditable div does NOT select all — it inserts a literal `a` character. This caused a silent prefix bug (`aClose-up...`) on early generations this session.

**Fix:** clear the prompt programmatically via JavaScript before typing:

```javascript
const el = document.querySelector('[contenteditable="true"]');
el.focus();
const range = document.createRange();
range.selectNodeContents(el);
const sel = window.getSelection();
sel.removeAllRanges();
sel.addRange(range);
document.execCommand('delete', false, null);
```

Then always screenshot-verify the prompt starts with the correct first word ("Photorealistic...") before clicking Generate. Do this every single time — the bug is subtle and wastes credits when missed.

## Session evidence

This formula was iteratively refined across ~112 Higgsfield credits (7 × 16-credit batches) during the April 23, 2026 build session. The final 5 approved looks — warm_desk_navy, podcast_studio, loft_window, corporate_office, modern_studio — all used this structure. The modern_studio generation (look #5) produced the cleanest chin result, likely because the clean editorial backdrop gave the model more "headroom" to render the reference face faithfully.
