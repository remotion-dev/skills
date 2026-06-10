# Graeham's 5 Warm-Desk Looks — Rotation System

All 5 looks share the same composition foundation: subject facing camera head-on, desk running horizontally across the bottom of frame, 16:9 landscape native, warm-cool color grade, shallow depth of field with face as brightest element.

Outfit + environment varies to give the content rotation variety without breaking identity consistency.

---

## Look 1 — `warm_desk_navy`

- **Outfit:** Navy blue quarter-zip pullover over white crewneck tee
- **Environment:** Warm-lit home office, dark wooden bookshelf on right, large window with blurred dusk city bokeh on left, warm tungsten desk lamp left edge
- **Props:** Laptop, leather notepad, coffee cup
- **Grade:** Warm gold + cool blue, warm dominant
- **Best use:** Everyday default. Market updates, buyer education, general content. If in doubt, this is the pick.
- **HeyGen look ID:** `67f9bcd8131140d793b9343851aeb25b`
- **Source file:** `C:\Users\Admin\Downloads\warm_desk_navy.png`

---

## Look 2 — `podcast_studio`

- **Outfit:** Black crewneck sweater
- **Environment:** Professional podcast studio with acoustic foam panels (dark charcoal + navy tones), Shure SM7B broadcast microphone on boom arm visible in left foreground
- **Props:** Mic + boom arm dominant, minimal desk clutter
- **Grade:** Dramatic low-key, blue/teal accent lighting, warm key light on face
- **Best use:** Hot takes, opinion content, long-form explainer, commentary on news/market events, "the truth about X" content. The moody grade signals gravity — save it for content where that tone is earned.
- **HeyGen look ID:** `e975c51279f3449991673293d47b99e2`
- **Source file:** `C:\Users\Admin\Downloads\podcast_studio.png`

---

## Look 3 — `loft_window`

- **Outfit:** Heather grey long-sleeve henley, top two buttons undone at collar
- **Environment:** Modern minimalist loft with floor-to-ceiling windows behind showing dramatic blurred dusk city bokeh with amber + teal pinpoint lights, exposed concrete accents
- **Props:** Sleek laptop left, ceramic coffee mug right, minimal desk
- **Grade:** Cool blue dusk background + warm amber key light from left
- **Best use:** Lifestyle content, neighborhood spotlights, "I love this city" storytelling, relocation content, community features. The cool dusk vibe communicates "end of workday reflection."
- **HeyGen look ID:** `798d3d001a4b44c9a0285621991aad1a`
- **Source file:** `C:\Users\Admin\Downloads\loft_window.png`

---

## Look 4 — `corporate_office`

- **Outfit:** Tailored charcoal grey wool suit jacket over crisp light blue dress shirt with navy blue silk necktie knotted at collar + clear round wire-frame glasses
- **Environment:** Executive office with dark wood-paneled walls, leather-bound books on shelf, large window with soft daylight one side, brass desk lamp casting warm light
- **Props:** Closed leather portfolio, fountain pen, white porcelain coffee cup
- **Grade:** Warm professional, magazine editorial polish
- **Best use:** Seller-facing content, listing introductions, CMA walkthroughs, "I just sold this for $X," high-stakes content, anything that needs executive gravitas. The tie + jacket signals "I'm handling something important."
- **HeyGen look ID:** `92ff2b057ef54b65863e627a30815e31`
- **Source file:** `C:\Users\Admin\Downloads\corporate_office.png`

---

## Look 5 — `modern_studio`

- **Outfit:** Crisp white oxford button-down with sleeves rolled to just below elbows, no tie, no jacket, top button undone + clear round wire-frame glasses (same frames as corporate_office for consistency)
- **Environment:** Clean modern minimalist studio with off-white/warm-grey seamless backdrop, tall brass arm lamp left edge, simple blonde-wood desk
- **Props:** Open notebook, black fountain pen, minimal
- **Grade:** Clean neutral with warm skin tones, bright even soft studio light
- **Best use:** Educational content, contract walkthroughs, "here's how this works" explainers, analyst-mode market breakdowns, PropertyIQ product education. The clean backdrop and glasses signal "I'm about to explain something technical."
- **HeyGen look ID:** `3d52c06f1ab94c09881daef7cfe0743a`
- **Source file:** `C:\Users\Admin\Downloads\modern_studio.png`

---

## Rotation logic

Map content intent to look — don't randomize.

| Content intent | Look |
|---|---|
| Market data / stat / price / metric | `warm_desk_navy` |
| Bold take / hot opinion / "here's what nobody's saying" | `podcast_studio` |
| Neighborhood / lifestyle / "I love it here" | `loft_window` |
| Seller-facing / listing intro / "just sold" | `corporate_office` |
| Educational / contract / process explainer | `modern_studio` |
| Unclear / casual / general | `warm_desk_navy` (default) |

**Never mix looks inside a single video.** One look = one video. Continuity matters more than visual variety at the clip level.

**Glasses consistency:** Two looks (corporate_office + modern_studio) use glasses. Use the same frames. When viewers see Graeham in glasses they should think "ah, he's about to explain something" — that signal only works if the frames match.

---

## HeyGen upload status

✅ **All 5 looks uploaded and registered in HeyGen** (avatar group `2160746aa659445e9cbfa4c02e5cf39c`).

All 5 look IDs are filled in above. The `heygen-video` skill has been extended to recognize these 5 new looks via `--look <name>` — see `/mnt/skills/user/heygen-video/references/avatars.md` and the `LOOKS` dict in `/mnt/skills/user/heygen-video/scripts/create.py`.

**To render a video in any of the 5 looks:**

```bash
python3 /mnt/skills/user/heygen-video/scripts/create.py \
  --script "Your script text" \
  --look warm_desk_navy \
  --aspect 16:9
```

Swap `warm_desk_navy` for any of: `podcast_studio`, `loft_window`, `corporate_office`, `modern_studio`.

**All 5 are landscape-native** (16:9). Always pass `--aspect 16:9`; edit to portrait (9:16) in post.

## If you add a 6th+ look later

1. Generate it in Higgsfield Nano Banana Pro using the prompt formula in `references/prompt_formula.md`
2. Save the PNG to `C:\Users\Admin\Downloads\<look_name>.png`
3. Upload to HeyGen web UI (the `upload.heygen.com` host is blocked from Claude's sandbox)
4. Name it exactly to match the filename
5. Tell Claude the look is uploaded — it will refetch via API and wire it in

---

## Why these 5 (and not olive polo / pub_den)

The original plan included `pub_den` (dark olive polo in warm wood-paneled den) but it was swapped mid-session for `corporate_office` (suit + tie + glasses) and `modern_studio` (white oxford + glasses). Reasons:

- Olive polo was redundant with grey henley — both are casual daywear, no visual differentiation at playback size
- Glasses add a second-axis signifier (analyst mode vs. casual) that the outfit-only variation was missing
- Corporate + tie covers the seller-facing gravitas content that the prior 4 looks couldn't carry

The final 5 cover: everyday (navy), bold-take (black), lifestyle (grey), executive (suit+glasses), educational (oxford+glasses). Each has a distinct content purpose and distinct visual signature.
