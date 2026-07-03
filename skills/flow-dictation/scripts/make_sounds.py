"""Generate soft chime WAVs for flow-dictation (replaces harsh winsound.Beep).
Plucked-sine notes: quick attack, exponential decay, quiet octave harmonic."""
import wave
from pathlib import Path

import numpy as np

SR = 44100
OUT = Path(r"C:\Users\Graeham Watts\Documents\Claude\Skills\skills\flow-dictation\assets\sounds")
OUT.mkdir(parents=True, exist_ok=True)


def pluck(freq, dur=0.16, vol=0.22, decay=16.0):
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    env = np.minimum(t / 0.006, 1.0) * np.exp(-t * decay)
    tone = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * freq * 2 * t)
    return vol * env * tone


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


# start: gentle rising pair (E5 -> A5) — "I'm listening"
save("start", mix([(0.00, pluck(659.26)), (0.07, pluck(880.00))]))
# done: falling pair (A5 -> E5) — "text delivered"
save("done", mix([(0.00, pluck(880.00)), (0.07, pluck(659.26))]))
# error: low soft double thud
save("error", mix([(0.00, pluck(196.00, dur=0.18, vol=0.28, decay=12)),
                   (0.12, pluck(174.61, dur=0.20, vol=0.24, decay=12))]))
# busy: single muted mid note
save("busy", mix([(0.00, pluck(440.00, dur=0.10, vol=0.15))]))
