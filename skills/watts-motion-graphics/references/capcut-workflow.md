# CapCut Workflow — Chroma Key Assembly

The overlay video is rendered on `#00FF00` chroma green. CapCut removes the green and the black panels survive intact. Here's the exact assembly process.

## Layer order (bottom to top)

| Track | Content | Notes |
|---|---|---|
| 1 (bottom) | HeyGen avatar MP4 | The talking head + audio. Base layer. |
| 2 | Higgsfield b-roll clips | Cuts at b-roll timing windows from production package |
| 3 (top) | Watts overlay `-greenbg.mp4` | This skill's output — chroma key applied |
| Audio bed | Music + SFX | Below voice in the mix, ducked under voice |

## Step-by-step in CapCut

### 1. Set project specs
- 1920 × 1080 for long-form (or 1080 × 1920 for short-form)
- 30 fps
- Match the orientation to the overlay file

### 2. Drop the avatar layer
- Drag the HeyGen MP4(s) onto Track 1
- This is the audio source. Don't separate audio unless you need to slice scenes.

### 3. Drop the b-roll layer
- Drag b-roll clips onto Track 2 at their respective time windows
- Use the b-roll prompt sheet's timing windows from the production package
- Trim aggressively — short cuts feel cinematic, long cuts feel slow

### 4. Drop the overlay
- Drag the `-greenbg.mp4` onto Track 3 (TOP track)
- It plays as solid green with black panels on top of it

### 5. Apply the chroma key
- Select the overlay clip
- Click **Cutout** (or **Adjust → Background Removal** depending on CapCut version)
- Click **Chroma key**
- Click the eyedropper, then click anywhere on the green
- Adjust sliders:
  - **Strength**: 100 (kills all the green)
  - **Shadow**: 30 (removes any green spill / fringe)
  - **Border feathering**: 0–2 (keeps text edges crisp)

After this step: the black panels are visible, the green is gone, the avatar/b-roll show through.

### 6. Test the chroma key
Scrub the timeline. Look specifically for:
- ✅ Green is fully removed everywhere
- ✅ Black panels are fully opaque (you can't see the avatar through them)
- ✅ Text edges are crisp (no green fringe)
- ❌ If you see green halo around text → increase Shadow slider
- ❌ If text edges are jaggy → reduce Border feathering
- ❌ If anything black bleeds through that shouldn't → strength may be too high; back off to 95

### 7. HERO music drop
- Find the HERO Reveal frame (the giant gold text moment)
- On the music track: cut the music exactly 6 frames BEFORE the HERO in-point
- Mute the cut segment (~1.5–2 seconds total)
- Cut again 6 frames before the HERO out-point
- Fade music back in over 0.5s

This silence is what makes the HERO land. Don't skip it.

### 8. Master export
- Resolution: 1920 × 1080 (or 1080 × 1920)
- Framerate: 30fps
- Quality: High or Higher
- Codec: H.264
- Format: MP4

## Common chroma key issues

| Problem | Cause | Fix |
|---|---|---|
| Green halo around text | Shadow slider too low | Increase Shadow to 30–50 |
| Text edges jaggy | Border feathering too high | Reduce to 0–2 |
| Some black showing where green should be | Strength too aggressive on dark green pixels | Reduce Strength to 90–95 |
| Overlay completely transparent including black panels | You picked a black pixel as the key | Re-pick green pixel |
| Green fringe only on certain frames | Compression artifacts at scene cuts | Render the overlay at higher bitrate (15Mbps+) |

## What to deliver to Jason / VAs

If handing off to Jason or a VA for assembly:

1. The `-greenbg.mp4` overlay file
2. A timing notes file: which graphic appears at which timestamp (or which spoken phrase)
3. The HERO music drop instructions
4. Reminder: chroma key, not Screen blend

Jason has built EPA-style overlays before — he knows the workflow. New VAs need the full guide above.
