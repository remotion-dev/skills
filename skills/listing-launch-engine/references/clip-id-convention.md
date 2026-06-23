# Clip-ID & Filename Convention

The clip ID is the spine of the whole system. It is assigned **in the Call Sheet, before anyone shoots**. The videographer never invents a filename — he names every export with its pre-assigned ID. The editor maps incoming files back to IDs. Because the ID is decided up front, footage shot today and footage shot three weeks from now reassemble into the right videos without anyone remembering the trip.

## Format

```
<SHOOTCODE>-<CAT><NN>
```

- **SHOOTCODE** — a short uppercase token for the shoot. Use the street name of the listing (e.g. `1247 Weeks St` → `WEEKS`). If two shoots could collide, append the go-live month (`WEEKS-JUN`). If there's no single address (rare), use the shoot date `MMDD`.
- **CAT** — one letter for the shot category:
  - `L` — **Listing** shot (this property's own video)
  - `B` — **Bank** shot (demand-backed B-roll for a *queued* video, not this listing)
  - `A` — **Avatar-source** shot (Graeham on camera for HeyGen training/source)
  - `AI` — **AI B-roll** gap-fill (generated, not filmed)
  - `G` — **Graphic** (motion-graphic overlay, built not filmed)
  - `V` — **Voiceover** segment (ElevenLabs, not filmed)
- **NN** — two-digit sequence within that category, starting `01`.

## Examples

| ID | Meaning |
|---|---|
| `WEEKS-L01` | First listing shot for 1247 Weeks St |
| `WEEKS-L07` | Seventh listing shot |
| `WEEKS-A02` | Second avatar-source clip captured on this trip |
| `WEEKS-B01` | First banked B-roll clip — belongs to a queued video, not this listing |
| `WEEKS-AI01` | First AI-generated gap-fill clip (Higgsfield) |
| `WEEKS-G01` | First motion-graphic overlay |
| `WEEKS-V01` | First voiceover segment |

## Filename rule for the videographer

Export each clip as: `<CLIPID>_<orientation>.<ext>` — e.g. `WEEKS-L01_landscape.mp4`, `WEEKS-A02_portrait.mp4`. If Step 0 answer was "both," shoot framed for both and export the master as `WEEKS-L01_both.mp4`; the editor crops per asset. Nothing else goes in the filename — no dates, no descriptions. The Call Sheet is the lookup table.

## Bank-shot mapping (category B)

Every `B` clip MUST name the queued video it feeds, so it doesn't become orphan footage. Carry a small map in the videographer and editor packets:

| Bank clip ID | Feeds queued video | Why it fits this trip |
|---|---|---|
| `WEEKS-B01` | "AB 1482 rent-cap explainer" | Need real Peninsula street-level B-roll; we're already on the block |
| `WEEKS-B02` | "First-time buyer down-payment myths" | Need a generic EPA front-porch establishing shot |

If a candidate bank shot can't name a real queued video, it doesn't get shot. Cap the `B` category at **5 scenes** total.
