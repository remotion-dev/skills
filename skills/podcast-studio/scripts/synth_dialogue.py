"""Render a two-host dialogue script to a podcast MP3 via ElevenLabs, deliver to iTunes.

Script format (UTF-8 text), one item per line:
    A: line spoken by host A (Brian)
    B: line spoken by host B (Matilda)
    PAUSE            <- inserts a 0.95s section beat
    # comment        <- ignored (headers, notes)
SSML <break time="0.6s"/> tags inside a line are honored by ElevenLabs.

Usage:
    python synth_dialogue.py <script.txt> "<Album Name>" <track#> "<Title>" [total_tracks]

Delivers to  C:\\Users\\Graeham Watts\\Music\\<Album Name>\\NN - <Title>.mp3
and copies into the iTunes "Automatically Add to iTunes" folder. Per-turn renders are cached in a
scratch dir keyed by album+track so re-runs only re-synthesize changed turns.
"""
import json, os, re, subprocess, sys, time, urllib.request, urllib.error, shutil
from concurrent.futures import ThreadPoolExecutor

SCRIPT_PATH = sys.argv[1]
ALBUM       = sys.argv[2]
TRACK       = int(sys.argv[3])
TITLE       = sys.argv[4]
TOTAL       = sys.argv[5] if len(sys.argv) > 5 else ""

MUSIC_ROOT = r"C:\Users\Graeham Watts\Music"
ALBUM_DIR  = os.path.join(MUSIC_ROOT, ALBUM)
AUTO_ADD   = os.path.join(MUSIC_ROOT, r"iTunes\iTunes Media\Automatically Add to iTunes")
KEY = open(r"C:\Users\Graeham Watts\Documents\Skills LLMS\Claude\.heygen-credentials\elevenlabs-key.txt").read().strip()

# ffmpeg/ffprobe are not on this machine's PATH; resolve to a known install (fallback to PATH).
FFMPEG  = shutil.which("ffmpeg")  or r"C:\Program Files\iTubeGo\ffmpeg.exe"
FFPROBE = shutil.which("ffprobe") or r"C:\Program Files\iTubeGo\ffprobe.exe"

SAFE_ALBUM = re.sub(r'[<>:"/\\|?*]', "", ALBUM)
SCRATCH = os.path.join(os.environ.get("TEMP", "."), "podcast-studio", SAFE_ALBUM, f"track{TRACK:02d}")
os.makedirs(SCRATCH, exist_ok=True)
os.makedirs(ALBUM_DIR, exist_ok=True)

VOICES = {
    "A": ("nPczCjzI2devNBz1zQrb", {"stability": 0.50, "similarity_boost": 0.75, "style": 0.2, "use_speaker_boost": True, "speed": 0.94}),  # Brian
    "B": ("XrExE9yKIg1WjnnlVkGX", {"stability": 0.50, "similarity_boost": 0.75, "style": 0.2, "use_speaker_boost": True, "speed": 0.96}),  # Matilda
}
MODEL = "eleven_multilingual_v2"

turns = []
for ln in open(SCRIPT_PATH, encoding="utf-8").read().splitlines():
    ln = ln.strip()
    if not ln or ln.startswith("#"):
        continue
    if ln == "PAUSE":
        turns.append(("PAUSE", None))
    elif ln[:2] in ("A:", "B:"):
        turns.append((ln[0], ln[2:].strip()))
    else:
        turns.append((turns[-1][0] if turns and turns[-1][0] != "PAUSE" else "A", ln))
total_chars = sum(len(t[1]) for t in turns if t[1])
print(f"{len(turns)} turns, {total_chars} chars", flush=True)

def synth(idx_turn):
    idx, (spk, text) = idx_turn
    fn = os.path.join(SCRATCH, f"t{idx:04d}.mp3")
    if os.path.exists(fn) and os.path.getsize(fn) > 1000:
        return fn
    vid, settings = VOICES[spk]
    payload = {"text": text, "model_id": MODEL, "voice_settings": settings, "apply_text_normalization": "auto"}
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128",
        data=json.dumps(payload).encode(),
        headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                open(fn, "wb").write(resp.read())
            return fn
        except urllib.error.HTTPError as e:
            print(f"  t{idx} HTTP {e.code}: {e.read().decode(errors='replace')[:200]}", flush=True)
            time.sleep(20 if e.code == 429 else 5)
        except Exception as ex:
            print(f"  t{idx}: {ex}", flush=True)
            time.sleep(5)
    raise RuntimeError(f"turn {idx} failed")

sil_short = os.path.join(SCRATCH, "sil_short.mp3")
sil_long  = os.path.join(SCRATCH, "sil_long.mp3")
for path, dur in ((sil_short, "0.30"), (sil_long, "0.95")):
    if not os.path.exists(path):
        subprocess.run([FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", dur,
                        "-c:a", "libmp3lame", "-b:a", "128k", path], capture_output=True, check=True)

speech = [(i, t) for i, t in enumerate(turns) if t[0] != "PAUSE"]
with ThreadPoolExecutor(max_workers=4) as ex:
    results = dict(zip([i for i, _ in speech], ex.map(synth, speech)))

lines = []
for i, (spk, text) in enumerate(turns):
    if spk == "PAUSE":
        lines.append(f"file '{sil_long}'")
    else:
        lines.append(f"file '{results[i]}'")
        lines.append(f"file '{sil_short}'")
listfile = os.path.join(SCRATCH, "concat.txt")
open(listfile, "w").write("\n".join(lines))

safe_title = re.sub(r'[<>:"/\\|?*]', "", TITLE)
final = os.path.join(ALBUM_DIR, f"{TRACK:02d} - {safe_title}.mp3")
track_tag = f"{TRACK}/{TOTAL}" if TOTAL else str(TRACK)
r = subprocess.run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", listfile,
                    "-c:a", "libmp3lame", "-b:a", "128k", "-ar", "44100",
                    "-metadata", f"title={TITLE}",
                    "-metadata", "artist=Graeham Watts",
                    "-metadata", f"album={ALBUM}",
                    "-metadata", "album_artist=Graeham Watts",
                    "-metadata", f"track={track_tag}",
                    "-metadata", "genre=Podcast",
                    "-metadata", "date=2026",
                    final], capture_output=True, text=True)
if r.returncode != 0:
    print(r.stderr[-1500:]); sys.exit(1)
dur = float(subprocess.run([FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
                            "-of", "csv=p=0", final], capture_output=True, text=True).stdout.strip())
# NOTE: intentionally does NOT copy to the iTunes "Automatically Add" folder.
# Auto-add creates a DUPLICATE library entry whenever the track already exists in the
# library at Music\<Album>\ (i.e. on every RE-RENDER), because iTunes imports the auto-add
# copy into iTunes Media\Music as a second entry. iTunes delivery is a deliberate step:
#   - NEW album  -> File > Add Folder to Library once (points the library at Music\<Album>\).
#   - RE-RENDER  -> overwriting the file in place (done above) updates the existing entry's
#                   audio automatically; no auto-add, no duplicate.
print(f"DONE track {TRACK}: {os.path.basename(final)}  {dur/60:.1f} min  (in {ALBUM})", flush=True)
