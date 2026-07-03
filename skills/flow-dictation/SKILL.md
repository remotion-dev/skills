---
name: flow-dictation
description: Local Wispr-Flow-style push-to-talk dictation for Graeham — hold Ctrl+Alt anywhere in Windows, speak, release, and the text is pasted into the focused app. Runs 100% locally on the RTX 5090 with faster-whisper large-v3 kept warm in VRAM (~0.9s transcription latency). Use ANY time the user mentions flow dictation, dictation app, push to talk, whisper flow, wispr flow, voice typing, talk to type, dictate into any app, the Ctrl+Alt mic, my dictation hotkey, or wants to change the dictation hotkey/vocabulary/settings, debug why dictation isn't working, or rebuild the desktop shortcut.
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
  red dot + "Listening 0:03" timer, then blue "Transcribing…", then gone.
  Marked WS_EX_NOACTIVATE so it never steals focus from the target app.
- **History window:** every dictation is saved to `outputs/history.jsonl`
  (timestamp, text, seconds, and which window it was pasted into — last 500
  kept). Searchable list, click for full text, Copy button / double-click to
  copy, Clear history. 100% local.
- **Audio cues:** high beep = recording started, two-tone = text pasted,
  low beep = error, short mid beep = pressed while model still loading.

## Architecture (all in `scripts/flow_dictation.py`)

1. Global hotkey hook (`keyboard` lib) — hold-to-talk. Combos ("ctrl+shift")
   use a raw unsuppressed hook with third-key cancel; single keys use
   suppressed on_press/on_release.
2. Mic capture with `sounddevice` at 16 kHz mono into a numpy buffer.
3. faster-whisper **large-v3 / CUDA / float16**, loaded once and kept warm
   (warm-up inference at startup so the first dictation is fast).
   Uses the standard RTX 5090 DLL fix: nvidia pip-wheel `bin/` dirs added via
   `add_dll_directory` AND prepended to PATH **before** importing faster_whisper.
   Falls back to CPU int8 if CUDA fails.
4. `vad_filter=True` + `initial_prompt` built from `vocab.txt` (names/brands
   spelled right: PropertyIQ, Intero, East Palo Alto, GHL...).
5. Paste via clipboard: save clipboard → copy transcript → Ctrl+V → restore
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
- **Verified 2026-07-01:** model loads in ~5s, warm transcription of a 13s
  sentence ≈ 0.9s, TTS self-test transcribed word-perfect including vocab terms.
- **Known limits:** paste can't reach elevated (admin) windows unless the app
  itself runs elevated; terminals that need Ctrl+Alt+V won't auto-paste
  (use tray > Copy last transcript). Requires the mic Windows defaults to.

## Roadmap (not built yet)

- Phase 3: voice commands ("new line", "scratch that"), toggle/lock mode for
  long dictation, optional AI-polish pass before pasting.
