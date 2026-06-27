#!/usr/bin/env python3
"""
transcribe_humor.py - build the Humor "backup brain" in the Obsidian vault.

Downloads audio for each comedian clip via yt-dlp, transcribes with
faster-whisper large-v3 on the GPU (RTX 5090), and writes one Obsidian
markdown note per video into  <vault>/Humor/transcripts/ .

- One model load, reused for all clips (fast).
- Per-clip try/except: a dead/hallucinated URL is logged, never faked.
- Writes _transcription-status.json so a later session can finalize the
  README index and flag any URL that failed.

Run:  python transcribe_humor.py
Std-lib + yt_dlp + faster_whisper (all already installed on this machine).
"""
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

# utf-8 console so check/cross glyphs never crash on Windows cp1252
for s in (sys.stdout, sys.stderr):
    try:
        s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

VAULT_HUMOR = Path(r"C:\Users\Graeham Watts\Documents\Obsidian\Humor")
TRANSCRIPTS = VAULT_HUMOR / "transcripts"
STATUS_FILE = VAULT_HUMOR / "_transcription-status.json"

# (comedian, title, video_id) — sourced from Graeham's Gemini pull, 2026-06-27
ENTRIES = [
    ("Mitch Hedberg", "I Wish They Made Fajita Cologne (Conan)", "Z_XbtYfrNYI"),
    ("Mitch Hedberg", "Best of Mitch Hedberg", "saoZjwf7Mfo"),
    ("Ryan Reynolds", "Aviation Gin Homeschool Edition", "O_KEwLfGjIc"),
    ("Ryan Reynolds", "Aviation Gin Misdirect", "d01CzCdjFnE"),
    ("Steven Wright", "Hysteria stand up", "eJCMjJwIGxY"),
    ("Steven Wright", "Classic Steven Wright (Carson Tonight Show)", "nfbIPOi7AF4"),
    ("Anthony Jeselnik", "Parents Found Drugs In His Room (Netflix Is A Joke)", "TYrKZuFxHRE"),
    ("Anthony Jeselnik", "Roasts Pete", "DkZY3oifV68"),
    ("Dan Mintz", "Treadmill Desks, Hippie Dolphins (Fallon)", "WCA0tWmFmyA"),
    ("Dan Mintz", "Stand-Up Performance", "CCaFg6iy3wE"),
    ("Jimmy Carr", "Best One-Liners From Every Stand-Up Show Vol 1", "UYwQ7s-aXiU"),
    ("Jimmy Carr", "His Most Offensive Joke Ever", "N7UVYwQz5_g"),
    ("Bo Burnham", "Bo Burnham Brings The Funny (Conan TBS)", "m135NsKsf34"),
    ("Bo Burnham", "Problem Solving Song (Netflix Is A Joke)", "J-zC46Tiygk"),
    ("Tig Notaro", "Impression Of A Person Doing Impressions (Conan TBS)", "9kxO2Xes31A"),
    ("Tig Notaro", "Loves Marriage and Cat Talking", "lajDlymQlyU"),
    ("John Mulaney", "Stand-Up Monologue (SNL)", "idCBER2J31w"),
    ("John Mulaney", "New in Town - Ice-T on SVU", "F1sd4CRcaE0"),
    ("Milton Jones", "Masterclass of One-Liners (Live at the Apollo)", "zfHM3IKJGgc"),
    ("Milton Jones", "Milton Impossible", "FAJiojVOYAU"),
    ("Morgan Murphy", "Being Single Isn't Something to Wooo About", "kmo45xwXY1A"),
    ("Morgan Murphy", "How to Lose a Guy in 10 Days", "5Rx1yAaK63M"),
    ("Mark Normand", "Mark Normand Performs Stand-Up", "_gOqO75ZOdw"),
    ("Mark Normand", "Pete Davidson & Kim Kardashian (Stand-Up On The Spot)", "ls-WfaXLsR4"),
]


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def ts(seconds):
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"


def load_model():
    # CUDA is available via system PATH on this machine; the pip nvidia libs
    # are optional. Try to add their dll dirs if present, else proceed.
    # RTX 5090 / faster-whisper: the CUDA 12 cuBLAS + cuDNN runtime DLLs ship in
    # the nvidia-*-cu12 pip wheels under <pkg>/bin (Windows). add_dll_directory
    # alone does NOT propagate to ctranslate2's loader — the bin dirs must also be
    # on PATH, set BEFORE faster_whisper is imported.
    import importlib.util
    dirs = []
    for pkg in ("nvidia.cublas", "nvidia.cudnn", "nvidia.cuda_runtime", "nvidia.cuda_nvrtc"):
        try:
            spec = importlib.util.find_spec(pkg)
            if not (spec and spec.submodule_search_locations):
                continue
            base = list(spec.submodule_search_locations)[0]
            for sub in ("bin", "lib"):  # Windows DLLs in bin/, Linux in lib/
                d = os.path.join(base, sub)
                if os.path.isdir(d):
                    dirs.append(d)
        except Exception:
            pass
    for d in dirs:
        try:
            os.add_dll_directory(d)
        except Exception:
            pass
    if dirs:
        os.environ["PATH"] = os.pathsep.join(dirs) + os.pathsep + os.environ.get("PATH", "")
    from faster_whisper import WhisperModel
    print("[*] loading faster-whisper large-v3 on cuda ...", flush=True)
    return WhisperModel("large-v3", device="cuda", compute_type="float16")


def download_audio(video_id, tmpdir):
    import yt_dlp
    url = f"https://www.youtube.com/watch?v={video_id}"
    opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(tmpdir, "a.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
    files = list(Path(tmpdir).glob("a.*"))
    if not files:
        raise RuntimeError("no audio file after download")
    return str(files[0]), info.get("title", ""), info.get("duration", 0)


def transcribe(model, audio_path):
    segments, info = model.transcribe(audio_path, vad_filter=True)
    rows = [(s.start, s.text.strip()) for s in segments]
    return rows, info.language


def write_note(comedian, title, video_id, rows, lang, real_title, duration):
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    url = f"https://www.youtube.com/watch?v={video_id}"
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    timestamped = "\n".join(f"[{ts(t)}] {txt}" for t, txt in rows if txt)
    full = " ".join(txt for _, txt in rows if txt)
    body = f"""---
comedian: {comedian}
title: {title}
youtube_title: {real_title}
url: {url}
video_id: {video_id}
duration_sec: {duration}
language: {lang}
method: faster-whisper large-v3 (GPU)
transcribed: {today}
tags: [humor, transcript, comedian/{slug(comedian)}]
---

# {comedian} — {title}

[Watch on YouTube]({url})

> Private study reference. Do not republish.

## Timestamped

{timestamped}

## Full text

{full}
"""
    out = TRANSCRIPTS / f"{slug(comedian)}--{video_id}.md"
    out.write_text(body, encoding="utf-8")
    return out, len(full)


def main():
    VAULT_HUMOR.mkdir(parents=True, exist_ok=True)
    model = load_model()
    status = {"started": datetime.now(timezone.utc).isoformat(), "results": []}
    ok = 0
    for i, (comedian, title, vid) in enumerate(ENTRIES, 1):
        tag = f"[{i:02d}/{len(ENTRIES)}] {comedian} - {title}"
        print(f"\n=== {tag} ===", flush=True)
        rec = {"comedian": comedian, "title": title, "video_id": vid, "ok": False}
        note_path = TRANSCRIPTS / f"{slug(comedian)}--{vid}.md"
        if note_path.exists():
            print(f"  [skip] already transcribed -> {note_path.name}", flush=True)
            rec.update(ok=True, skipped=True, file=note_path.name)
            status["results"].append(rec)
            STATUS_FILE.write_text(json.dumps(status, indent=2), encoding="utf-8")
            ok += 1
            continue
        try:
            with tempfile.TemporaryDirectory() as tmp:
                print("  downloading audio ...", flush=True)
                audio, real_title, dur = download_audio(vid, tmp)
                print(f"  transcribing ({dur}s) ...", flush=True)
                rows, lang = transcribe(model, audio)
                out, nchars = write_note(comedian, title, vid, rows, lang, real_title, dur)
            print(f"  [ok] {nchars} chars -> {out.name}", flush=True)
            rec.update(ok=True, chars=nchars, file=out.name)
            ok += 1
        except Exception as e:
            print(f"  [FAIL] {type(e).__name__}: {e}", flush=True)
            rec["error"] = f"{type(e).__name__}: {e}"
        status["results"].append(rec)
        STATUS_FILE.write_text(json.dumps(status, indent=2), encoding="utf-8")

    status["finished"] = datetime.now(timezone.utc).isoformat()
    status["ok"] = ok
    status["total"] = len(ENTRIES)
    STATUS_FILE.write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(f"\n=== DONE: {ok}/{len(ENTRIES)} transcribed ===", flush=True)
    fails = [r for r in status["results"] if not r["ok"]]
    if fails:
        print("Failed (likely bad/unavailable URLs):", flush=True)
        for r in fails:
            print(f"  - {r['comedian']} | {r['title']} | {r['video_id']}", flush=True)


if __name__ == "__main__":
    main()
