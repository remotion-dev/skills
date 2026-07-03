---
name: flow-dictation
description: Local Wispr-Flow-style push-to-talk dictation for Graeham — hold Ctrl+Alt anywhere in Windows, speak, release, and the text is pasted into the focused app (tap Shift while talking for AI-polish via the Claude API). Runs locally on the RTX 5090 with faster-whisper large-v3-turbo kept warm in VRAM (~0.3s transcription latency), with a live waveform overlay, dictation history + stats window, and personal vocabulary. Use ANY time the user mentions flow dictation, dictation app, push to talk, whisper flow, wispr flow, voice typing, talk to type, dictate into any app, the Ctrl+Alt mic, my dictation hotkey, polish mode, or wants to change the dictation hotkey/vocabulary/settings, debug why dictation isn't working, or rebuild the desktop shortcut.
---

# Flow Dictation — local push-to-talk dictation

A system-tray app that replicates Wispr Flow entirely locally. Hold
**Ctrl+Alt** anywhere in Windows, speak, release — the transcript is pasted
into whatever app has focus. No cloud, no subscription, no audio leaves the
machine.

Combo-hotkey safety: recording arms when both keys are held, but pressing any
THIRD key (Ctrl+Alt+T, Ctrl+Alt+Del...) cancels instantly and silently — so
normal shortcuts never trigger a paste, and the start-beep is delayed 180ms so
quick shortcuts make no sound. Single-key hotkeys (e.g. "f9") still work via
config and are suppressed from the target app.

Hotkey history: F9 → Ctrl+Shift (rejected 2026-07-02: holding Shift 8s fires
the Windows Filter Keys accessibility warning and the OS beeps) → **Ctrl+Alt**
(current; no Windows accessibility feature attaches to holding it). Combos must
be modifier-only — typing keys like Tab/Q can't be suppressed on the combo path
and would leak into the focused app.

## How it runs

- **Launch:** the **"Flow Dictation"** shortcut on the Desktop (gold mic icon),
  which runs `pythonw.exe scripts/flow_dictation.py` — no console window.
- **Tray icon states:** gray = model loading (~5s), **gold = ready**,
  red = recording, blue = transcribing, dark = paused.
- **Tray menu:** History (also opens on LEFT-click of the tray icon) · Pause ·
  Copy last transcript · Edit vocabulary · Start with Windows (toggle, creates/
  removes a shortcut in `shell:startup`) · Quit.
- **Overlay pill:** a small dark capsule appears bottom-center while dictating —
  pink dot + a **flowing violet→magenta voice wave** (continuous oscillating
  gradient line + fainter echo line, amplitude follows the speech envelope)
  + "Listening 0:03" timer, then blue-violet "Transcribing…" (purple
  "Polishing with Claude…" in polish mode), then gone. Marked WS_EX_NOACTIVATE
  so it never steals focus from the target app.
- **Sounds:** soft plucked-sine chimes in `assets/sounds/` (rising pair =
  listening, falling pair = done, low thud = error), generated int16 WAVs
  played via `winsound.PlaySound` async. Regenerate/re-tune them with a
  variant of the make_sounds.py script (documented in the wav header comment
  of scripts history); raw `winsound.Beep` tones remain as fallback only.
- **Color scheme:** soft violet accent `#a78bfa` everywhere (tray icon,
  history window, stats) — the original gold was retired 2026-07-02.
- **AI-polish mode:** tap **Shift** once while holding Ctrl+Alt and talking —
  that dictation is cleaned into tidy prose by Claude before pasting (filler
  removed, grammar fixed, tone kept). Requires an API key (see Architecture
  below); without one it error-beeps and pastes the raw transcript.
- **History window:** every dictation is saved to `outputs/history.jsonl`
  (timestamp, text, seconds, polished flag, and which window it was pasted
  into — last 500 kept). Searchable list (✨ marks polished entries), click
  for full text, Copy button / double-click to copy, Clear history, and a
  **stats strip**: words today / all time, spoken wpm, minutes saved vs
  typing at 40 wpm. 100% local.
- **Audio cues:** high beep = recording started, two-tone = text pasted,
  low beep = error, short mid beep = pressed while model still loading.

## Architecture (all in `scripts/flow_dictation.py`)

1. Global hotkey hook (`keyboard` lib) — hold-to-talk. Combos ("ctrl+alt")
   use a raw unsuppressed hook with third-key cancel; single keys use
   suppressed on_press/on_release. Exception: tapping the `polish_key`
   (Shift) while recording does NOT cancel — it arms AI-polish for that
   dictation (pill shows "✨ polish", tray/pill go purple while polishing).
2. Mic capture with `sounddevice` at 16 kHz mono into a numpy buffer; per-chunk
   RMS feeds the live waveform in the overlay pill.
3. faster-whisper **large-v3-turbo / CUDA / float16 / beam_size 1**, loaded
   once and kept warm (~2.7s load, ~0.33s warm transcription of a 13s clip —
   verified 2026-07-02). Uses the standard RTX 5090 DLL fix: nvidia pip-wheel
   `bin/` dirs added via `add_dll_directory` AND prepended to PATH **before**
   importing faster_whisper. Falls back to CPU int8 if CUDA fails.
4. `vad_filter=True` + `initial_prompt` built from `vocab.txt` (names/brands
   spelled right: PropertyIQ, Intero, East Palo Alto, GHL...).
5. Optional polish pass (only when Shift was tapped): raw transcript →
   Claude API (`polish_model` in config, default `claude-opus-4-8`, official
   `anthropic` SDK) with a cleanup system prompt (no em dashes, keep tone,
   return only cleaned text). Key resolution: `ANTHROPIC_API_KEY` env var,
   else the gitignored `<repo-root>/anthropic-token.txt`. No key or API error
   → error beep + raw transcript pasted; everything else stays 100% local.
6. Paste via clipboard: save clipboard → copy transcript → Ctrl+V → restore
   old clipboard after 1s. Works in virtually every app, instant.

## Files

| File | Purpose |
|---|---|
| `scripts/flow_dictation.py` | core app: hotkey, mic, whisper, paste, tray |
| `scripts/ui.py` | tkinter layer: overlay pill + history window |
| `config.json` | hotkey, model, device, language, beeps |
| `vocab.txt` | one term per line → Whisper priming prompt (editable live) |
| `assets/flow.ico` | app icon (regenerate: `make_icon_image('ready').save(...)`) |
| `outputs/flow-dictation.log` | runtime log (gitignored output) |
| `outputs/history.jsonl` | dictation history, one JSON per line (gitignored) |

Threading: tkinter owns the main thread (`ui.run()`); pystray runs via
`run_detached()`; keyboard hooks + transcription run on worker threads. All UI
calls from workers go through `UI.q` (a queue polled with `root.after`).

## Ops

- **Change hotkey:** edit `config.json` (`"hotkey": "ctrl+shift"` — any
  `keyboard`-lib key name or a modifier combo joined with `+`), then Quit +
  relaunch from the desktop shortcut.
- **Self-test without a mic:**
  `python scripts/flow_dictation.py --selftest path/to/clip.wav`
- **Verified 2026-07-01 (large-v3):** ~5s load, ~0.9s warm transcription.
  **2026-07-02 (large-v3-turbo, beam 1):** ~2.7s load, ~0.33s warm
  transcription of the same 13s clip, word-perfect including vocab terms.
- **Enable polish mode:** put a Claude API key in `ANTHROPIC_API_KEY` or in
  `Documents\Claude\Skills\anthropic-token.txt` (gitignored via `*token*.txt`).
- **Known limits:** paste can't reach elevated (admin) windows unless the app
  itself runs elevated; terminals that need Ctrl+Alt+V won't auto-paste
  (use tray > Copy last transcript). Requires the mic Windows defaults to.

## Roadmap (not built yet)

- Phase 3: voice commands ("new line", "scratch that"), toggle/lock mode for
  long dictation, optional AI-polish pass before pasting.
