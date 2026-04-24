---
name: room-redesign
description: AI Room Redesign & Virtual Staging for Graeham Watts. Use ANY time the user mentions room redesign, virtual staging, stage a listing, redesign this room, redesign my room, photorealistic redesign, interior design preview, pre-renovation preview, what would this room look like, make this room look, stage this house, staging photos, listing staging, empty room staging, furniture swap, change the decor, change the paint, change the sofa, redesign the kitchen, redesign the bedroom, redesign the office, Japandi, mid-century, minimalist, Scandinavian, boutique hotel vibe, or anything related to generating photorealistic redesigns of real rooms from a user-supplied photo. Also trigger when the user uploads a photo of a room and asks how to make it look different, better, or sold-ready. This skill calls Google's Gemini image API directly — no third-party wrapper — and is built specifically for real estate listing staging and homeowner redesign previews.
allowed-tools: Bash, Read, Write
---

# Room Redesign (Direct Gemini API)

Generates photorealistic room redesigns and virtual staging using Google's Gemini 2.5 Flash Image model, called directly over HTTPS. No third-party CLI, no Node dependencies, no wrapper libraries — just a single Python script under `scripts/redesign.py` that Graeham controls end to end.

## When to Use This Skill

Fire on any of these:

- **Virtual staging for a listing** — empty or dated room → buyer-ready photos
- **Homeowner redesign previews** — "what if my living room looked like…"
- **Pre-renovation previews** — "paint the cabinets, add a backsplash"
- **Test-before-you-buy furniture** — render a specific product in the actual room
- **Whole-home cohesive design** — multiple rooms tied together
- **Listing agent mood boards** — show sellers what staging will look like

Trigger words: redesign, stage, staging, virtual staging, redo, make this look, what would this look like, before and after, empty room, furniture placement, paint color preview, renovation preview.

## Prerequisites (one-time setup)

1. **Get a Google AI Studio API key** (free tier is enough to try this out):
   - Go to `https://aistudio.google.com/`
   - Sign in with any Google account
   - Click "API Keys" in the left sidebar → "Create API Key"
   - Copy the key (starts with `AIza...`)

2. **Store the key as an environment variable** so nothing ever writes it to disk:
   - **macOS/Linux**: add this to `~/.zshrc` or `~/.bashrc`:
     ```bash
     export GEMINI_API_KEY="AIzaSy...your-key..."
     ```
   - **Windows (PowerShell)**: run once in an admin PowerShell:
     ```powershell
     [Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "AIzaSy...your-key...", "User")
     ```
   - Then restart your terminal / Claude desktop app so it picks up the new env var.

3. **Check the Python dependency is installed**:
   ```bash
   python3 -c "import requests" || pip3 install requests --break-system-packages
   ```

That's it. No CLI install, no extension install, no npm, no Node.

## How to Invoke

Once the user uploads a room photo and describes what they want, run:

```bash
python3 "{{SKILL_DIR}}/scripts/redesign.py" \
  --image "/path/to/room.jpg" \
  --prompt "Redesign this living room in warm Japandi style..." \
  --output-dir "/path/to/outputs/"
```

The script will:
1. Read the local photo
2. POST it along with the prompt to Gemini's `generateContent` endpoint
3. Pull the image bytes out of the response
4. Save the redesigned image(s) to the output directory with a timestamped filename
5. Print the final path(s) so you can present them to the user

## Prompt Patterns That Work (Real Estate Focus)

These are pre-tuned for Graeham's workflow. Mix and match based on the actual photo.

### Empty listing staging (seller client)
> "Stage this empty living room for a real estate listing. Neutral, broadly appealing palette. Add a light linen sectional, a natural wood coffee table, a soft area rug, one large piece of abstract art, and two small plants. Keep all existing flooring, windows, and wall color. Warm afternoon light. Photorealistic, MLS-ready."

### Occupied but cluttered (seller prep)
> "Redesign this lived-in room as if professionally staged for sale. Remove all personal items, family photos, and clutter. Simplify furniture to essentials. Add styled accessories — a vase, two books, one throw blanket. Neutral tones. Keep structure, windows, and flooring identical. Photorealistic."

### Pre-renovation kitchen preview
> "Show this kitchen after a cosmetic renovation. Paint the cabinets deep forest green, change hardware to brass, add a natural stone backsplash, install two matte black pendants over the island. Keep layout, appliances, and flooring unchanged. Photorealistic, editorial photography style."

### Buyer "what would it look like" (buyer client)
> "Redesign this room as a buyer's dream [style]. Show what it could look like with [specific furniture]. Keep the floors and windows the same so the buyer can visualize the actual space."

### Three-style mood board
> "Give me three completely different redesigns of this room: (1) modern minimalist, (2) warm mid-century, (3) moody and dark. Keep floors and windows consistent in every version. For each, describe the vibe in one sentence before the image."

## Pro Moves

These move the needle on output quality:

- **Always tell it what to keep.** "Keep flooring, windows, and ceiling height identical" stops the model from fabricating a different room.
- **Reference real places.** "Like a Soho House lounge" or "feels like a Parisian apartment" beats generic adjectives.
- **Describe the light.** "South-facing, bright afternoon" or "dim evening vibe, lamps on" changes the whole mood.
- **One change at a time on iterations.** After the first render, adjust a single thing per prompt. "Now make the sofa green." "Now add plants."
- **Ask for a shopping list.** After a design Graeham loves, ask the model to "list every piece of furniture and decor used, with approximate price range and where to buy." Graeham gets a seller handout or buyer upsell.

## Output Handling

- The script drops renders into `{{output_dir}}/redesign-YYYYMMDD-HHMMSS-NN.png`.
- Present the most recent image(s) to the user with absolute path links.
- If the user wants variations, re-run with the same prompt — Gemini returns different results each call.
- If the user wants edits, pass the new image as `--image` and the edit instruction as `--prompt`.

## Cost & Quota

- Default model: `gemini-2.5-flash-image` (fast, low cost, stable — not a preview).
- For higher quality: set `GEMINI_IMAGE_MODEL=gemini-3-pro-image-preview` in env.
- Other available models on your account: `nano-banana-pro-preview`, `gemini-3.1-flash-image-preview` (all preview names may rotate without notice — the stable default above will not).
- Free tier allows plenty for testing. Paid tier is usage-based and cheap per image.
- If quota errors: wait or switch models. The script surfaces the exact API error message.

## Troubleshooting

| Problem | Fix |
|---|---|
| `GEMINI_API_KEY not set` | Set env var (see Prerequisites step 2) and restart terminal |
| `403` or `permission denied` | Key is wrong or revoked. Generate a new one in AI Studio |
| `429 quota exceeded` | Wait 60s or switch to a different model tier |
| No image in response | Prompt may have hit a safety filter. Simplify or soften language |
| Blurry / wrong room | Tell the model explicitly what to keep and be specific about the style |

## Why This Is Better Than the Third-Party Wrapper

- **Zero dependencies on strangers' code.** The only thing running on Graeham's machine is this Python script he can read top to bottom.
- **API key never leaves his environment.** It's only used in the one HTTPS call to `generativelanguage.googleapis.com`.
- **Works offline from GitHub.** Even if the `cc-nano-banana` repo disappeared tomorrow, this skill keeps working.
- **Tuned for real estate.** Prompts, trigger words, and pro moves are all built around listing staging and buyer visualization.

## What This Skill Does NOT Do

Be honest with the user if they ask for:
- **Video.** This is images only. For video, use `heygen-video`, `video-creator`, or `higgsfield-video`.
- **Real product rendering with exact SKUs.** Gemini approximates styles — it's not a CAD tool.
- **Legally-disclosable staging.** Virtually staged photos must be disclosed in MLS per most regional rules. Remind the user.
