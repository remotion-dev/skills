# ElevenLabs Audio Tag Reference

ElevenLabs does NOT support full W3C SSML. Use bracket-syntax audio tags for emotive delivery.

## Supported bracket tags (eleven_multilingual_v2)

| Tag | Effect |
|---|---|
| `[laughs]` | Short laugh insertion |
| `[chuckles]` | Softer laugh |
| `[sighs]` | Audible sigh |
| `[whispers]` | Switch to whispered delivery for following phrase |
| `[excited]` | Lift energy |
| `[sarcastic]` | Flatten tone |
| `[pause]` | ~0.4s silence |

## SSML subset that IS supported

| Tag | Effect |
|---|---|
| `<speak>...</speak>` | Root wrapper (optional, enables SSML mode) |
| `<break time="0.5s"/>` | Exact silence duration (0.1s–3s) |

## Not supported (silently stripped)

- `<prosody rate="slow">` — tag accepted, text still read, but no rate change
- `<emphasis>`, `<say-as>`, `<phoneme>`, `<sub>`, `<voice>`

## V6 script compatibility

V6 scripts use `<prosody>` and `<break>` for readability. Only `<break>` delivers real audio changes. For true rate/pitch control, pre-split the script and synthesize each chunk with different `voice_settings.stability` values, then concatenate with ffmpeg.
