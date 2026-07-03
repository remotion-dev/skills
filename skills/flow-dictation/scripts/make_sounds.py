"""Generate soft chime WAVs for flow-dictation (replaces harsh winsound.Beep).
v2 (2026-07-02): softer & warmer per Graeham — lower volume, C5/G5 pair,
slow airy decay with a detuned shimmer partial. Run: python make_sounds.py"""
import wave
from pathlib import Path

import numpy as np

SR = 44100
OUT = Path(__file__).resolve().parent.parent / "assets" / "sounds"
OUT.mkdir(parents=True, exist_ok=True)


def pluck(freq, dur=0.38, vol=0.12, decay=8.0):
    """Soft airy chime: slow 15ms attack, long gentle decay, a quiet octave
    plus a barely-detuned partner tone for shimmer."""
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    env = np.minimum(t / 0.015, 1.0) * np.exp(-t * decay)
    tone = (
        np.sin(2 * np.pi * freq * t)
        + 0.5 * np.sin(2 * np.pi * freq * 1.003 * t)
        + 0.2 * np.sin(2 * np.pi * freq * 2 * t)
    )
    return vol * env * tone / 1.7


def mix(notes):
    """notes = [(start_sec, samples)] -> single float array"""
    total = max(int(s * SR) + len(x) for s, x in notes)
    out = np.zeros(total)
    for s, x in notes:
        i = int(s * SR)
        out[i:i + len(x)] += x
    return out


def save(name, sig):
    sig = np.clip(sig, -1, 1)
    data = (sig * 32767).astype(np.int16)
    with wave.open(str(OUT / f"{name}.wav"), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(data.tobytes())
    print(f"{name}.wav  {len(data)/SR*1000:.0f}ms")


# start: warm rising pair (C5 -> G5) — "I'm listening"
save("start", mix([(0.00, pluck(523.25)), (0.09, pluck(783.99))]))
# done: warm falling pair (G5 -> C5) — "text delivered"
save("done", mix([(0.00, pluck(783.99)), (0.09, pluck(523.25))]))
# error: low soft double thud
save("error", mix([(0.00, pluck(174.61, dur=0.30, vol=0.20, decay=9)),
                   (0.14, pluck(155.56, dur=0.32, vol=0.17, decay=9))]))
# busy: single muted mid note
save("busy", mix([(0.00, pluck(392.00, dur=0.18, vol=0.08))]))
