# Avatar-Led Production Mode (agent NOT on set)

When Graeham is **not** at the shoot, every on-camera moment is a **HeyGen avatar** composited by Peter onto Wesley's footage. Wesley shoots pure property + neighborhood + B-roll "plates"; Graeham never appears live. This mode maximizes content because the talking-head side is unlimited (render any number of avatar pieces from the trained looks) and Wesley's whole window goes to coverage.

Trigger: Graeham says he won't be at the shoot, "use my avatars," "avatar-led," "I'm not going to be there," or "all digital twin." Step 0 asks it (on set vs avatar-led).

## The 6 compositing patterns (this is what Peter needs)

Every video/ad asset gets one of these as its **Assembly recipe** (pattern # + avatar look + which Wesley clips + VO/SSML + graphics + aspect):

1. **Avatar Intro → B-roll body → Avatar Outro.** Full-frame avatar opens (hook), cut to property B-roll under voiceover, full-frame avatar returns for the CTA. → listing video, market update, YouTube tour.
2. **PIP Walk-and-Talk.** Avatar composited small in a bottom corner (~25-30% of frame) over full-frame property/neighborhood B-roll, as if narrating a tour. Use a standing/talking look for a static PIP, or a **walking** avatar over a street/neighborhood plate for the "walking down the street" feel. → reels, neighborhood walkthrough, POV-style.
3. **VO-only over B-roll.** No avatar on screen. Clone voice narrates over property B-roll + text overlays. → hero reveal, lifestyle, fast-cut reels.
4. **Avatar End-Card only.** Property/B-roll carries the whole clip; the avatar appears only at the end for the CTA + brand. → short reels, ad creative.
5. **Green-Screen Stage.** Avatar keyed onto a backdrop, a clean room "plate," a listing photo, or a stat graphic, so Graeham "stands in" the scene. → disclosure drop, value explainer, anything that should feel placed in the home.
6. **Avatar + Motion-Graphics.** Avatar (PIP or full-frame) alongside `watts-motion-graphics` stat / compare cards. → value explainer, market update.

## What Wesley shoots in this mode (plates for compositing)

No Graeham, no talking-head plates. Everything is the property, the community, the neighborhood, details, PLUS deliberate **compositing plates**:

- **PIP plates** — clean shots framed with **deliberate negative space in a bottom corner** so the avatar drops in without covering anything important. Flag these in the shot list ("leave bottom-left clear for avatar PIP").
- **Avatar-stage plates** — clean, locked or slow wide shots of a nice spot (living room, balcony, the gate, a street) held **10-15 seconds** so a green-screen avatar can be composited standing there.
- **Walking plates** — long, smooth gimbal walks (POV down the street, through the home) that run under VO or behind a PIP.
- **Coverage for variety** — multiple angles per room/space; the more clean cuts, the more reels and statics Peter can build.

## Avatar look selection (per placement)

`digital_twin` for the authentic full-frame intro/outro and any face-critical PIP · `freshly_ironed` for polished value/seller pieces · `fashion_flip` for high-energy hook reels · `suburban_serenity` for landscape / YouTube 16:9 · the broader ~70-variation library (incl. walking shots) for walk-and-talk PIP. Voice = the ElevenLabs clone. Full inventory + IDs: `heygen-avatars.md`. Render via `heygen-video` / `heygen-elevenlabs-renderer` straight from the SSML in the Script Library.

## How it changes the packets

- **Videographer packet:** drop the agent block; all shots are property/neighborhood/plates. Add the PIP-negative-space and avatar-stage plate notes.
- **Editor packet:** every video asset carries its **Assembly recipe** (pattern + look + clips + VO). This is the heart of the avatar-led editor packet.
- **Script Library:** every talking-head/VO segment is avatar-rendered (SSML for all; no "filmed live").
- **Content yield goes up:** one shoot's B-roll feeds a large library of avatar-led videos + ads + statics, because the on-camera side is render-on-demand.
