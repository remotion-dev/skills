#!/usr/bin/env python3
"""
flow_dictation.py — local Wispr-Flow-style push-to-talk dictation for Graeham.

Hold the hotkey (default F9) anywhere in Windows, speak, release.
The speech is transcribed on the RTX 5090 with faster-whisper large-v3
(model stays warm in VRAM) and pasted into whatever app has focus.

Runs as a system-tray app:
  gray  = model loading      gold = ready
  red   = recording          blue = transcribing

Tray menu: Pause/Resume, Copy last transcript, Edit vocabulary,
Start with Windows (toggle), Quit.

Launch via the "Flow Dictation" desktop shortcut (pythonw, no console),
or directly:  python flow_dictation.py
Self-test (no mic needed):  python flow_dictation.py --selftest path/to/clip.wav
"""
import json
import os
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = SKILL_DIR / "config.json"
VOCAB_FILE = SKILL_DIR / "vocab.txt"
LOG_FILE = SKILL_DIR / "outputs" / "flow-dictation.log"

DEFAULTS = {
    "hotkey": "f9",
    "model": "large-v3",
    "device": "cuda",
    "compute_type": "float16",
    "language": "en",
    "sample_rate": 16000,
    "min_seconds": 0.3,
    "beeps": True,
}


def log(msg):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def load_config():
    cfg = dict(DEFAULTS)
    try:
        cfg.update(json.loads(CONFIG_FILE.read_text(encoding="utf-8")))
    except Exception:
        pass
    return cfg


def load_vocab_prompt():
    """vocab.txt lines become Whisper's initial_prompt so names spell right."""
    try:
        words = [
            w.strip()
            for w in VOCAB_FILE.read_text(encoding="utf-8").splitlines()
            if w.strip() and not w.strip().startswith("#")
        ]
        if words:
            return "Vocabulary: " + ", ".join(words) + "."
    except Exception:
        pass
    return None


def setup_cuda_dlls():
    """RTX 5090 / faster-whisper: the CUDA 12 cuBLAS + cuDNN runtime DLLs ship in
    the nvidia-*-cu12 pip wheels under <pkg>/bin (Windows). add_dll_directory
    alone does NOT propagate to ctranslate2's loader — the bin dirs must also be
    on PATH, set BEFORE faster_whisper is imported."""
    import importlib.util

    dirs = []
    for pkg in ("nvidia.cublas", "nvidia.cudnn", "nvidia.cuda_runtime", "nvidia.cuda_nvrtc"):
        try:
            spec = importlib.util.find_spec(pkg)
            if not (spec and spec.submodule_search_locations):
                continue
            base = list(spec.submodule_search_locations)[0]
            for sub in ("bin", "lib"):
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


def beep(kind, enabled=True):
    """Short non-blocking audio cues: rec start, done, error, ignored."""
    if not enabled:
        return

    def _b():
        try:
            import winsound

            tones = {
                "start": [(880, 70)],
                "done": [(1175, 55), (1568, 70)],
                "error": [(220, 180)],
                "busy": [(440, 60)],
            }
            for freq, dur in tones.get(kind, []):
                winsound.Beep(freq, dur)
        except Exception:
            pass

    threading.Thread(target=_b, daemon=True).start()


def make_icon_image(state):
    """Tray icon: mic glyph on a dark disc, ring color = state."""
    from PIL import Image, ImageDraw

    colors = {
        "loading": (128, 128, 128),
        "ready": (212, 175, 55),      # brand gold
        "recording": (220, 60, 50),
        "transcribing": (70, 130, 220),
        "paused": (80, 80, 80),
    }
    ring = colors.get(state, (128, 128, 128))
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([2, 2, 62, 62], fill=(20, 20, 20, 255), outline=ring, width=5)
    gold = (212, 175, 55, 255) if state != "paused" else (110, 110, 110, 255)
    d.rounded_rectangle([26, 14, 38, 36], radius=6, fill=gold)   # capsule
    d.arc([20, 26, 44, 46], start=0, end=180, fill=gold, width=3)  # cradle
    d.line([32, 46, 32, 52], fill=gold, width=3)                 # stem
    d.line([25, 52, 39, 52], fill=gold, width=3)                 # base
    return img


class FlowDictation:
    def __init__(self, cfg):
        self.cfg = cfg
        self.model = None
        self.paused = False
        self.recording = False
        self.frames = []
        self.stream = None
        self.last_text = ""
        self.state = "loading"
        self.tray = None
        self.transcribe_lock = threading.Lock()
        self.rec_lock = threading.Lock()

    # ---------- model ----------

    def load_model(self):
        setup_cuda_dlls()
        from faster_whisper import WhisperModel

        log(f"loading faster-whisper {self.cfg['model']} on {self.cfg['device']} ...")
        t0 = time.time()
        try:
            self.model = WhisperModel(
                self.cfg["model"], device=self.cfg["device"], compute_type=self.cfg["compute_type"]
            )
        except Exception as e:
            log(f"GPU load failed ({type(e).__name__}: {e}); falling back to CPU int8")
            self.model = WhisperModel(self.cfg["model"], device="cpu", compute_type="int8")
        # warm-up pass so the first real dictation isn't slow
        import numpy as np

        self.model.transcribe(np.zeros(self.cfg["sample_rate"], dtype=np.float32), language=self.cfg["language"])
        log(f"model ready in {time.time() - t0:.1f}s")
        self.set_state("ready")

    # ---------- recording ----------

    def on_press(self, _event=None):
        with self.rec_lock:
            if self.paused or self.recording:
                return
            if self.model is None:
                beep("busy", self.cfg["beeps"])
                return
            self.recording = True
        self.frames = []
        try:
            import sounddevice as sd

            self.stream = sd.InputStream(
                samplerate=self.cfg["sample_rate"],
                channels=1,
                dtype="float32",
                callback=lambda indata, *_: self.frames.append(indata.copy()),
            )
            self.stream.start()
            self.set_state("recording")
            beep("start", self.cfg["beeps"])
        except Exception as e:
            with self.rec_lock:
                self.recording = False
            log(f"mic error: {type(e).__name__}: {e}")
            beep("error", self.cfg["beeps"])

    def on_release(self, _event=None):
        with self.rec_lock:
            if not self.recording:
                return
            self.recording = False
        try:
            self.stream.stop()
            self.stream.close()
        except Exception:
            pass
        frames = self.frames
        self.frames = []
        threading.Thread(target=self.process, args=(frames,), daemon=True).start()

    # ---------- transcribe + paste ----------

    def process(self, frames):
        import numpy as np

        if not frames:
            self.set_state("ready")
            return
        audio = np.concatenate(frames).flatten()
        seconds = len(audio) / self.cfg["sample_rate"]
        if seconds < self.cfg["min_seconds"]:
            self.set_state("ready")
            return
        self.set_state("transcribing")
        try:
            with self.transcribe_lock:
                t0 = time.time()
                segments, _info = self.model.transcribe(
                    audio,
                    language=self.cfg["language"],
                    vad_filter=True,
                    initial_prompt=load_vocab_prompt(),
                )
                text = " ".join(s.text.strip() for s in segments).strip()
            if text:
                self.last_text = text
                self.paste(text)
                log(f'{seconds:.1f}s audio -> {time.time() - t0:.2f}s -> "{text[:80]}"')
                beep("done", self.cfg["beeps"])
            else:
                log(f"{seconds:.1f}s audio -> (no speech detected)")
        except Exception as e:
            log(f"transcribe error: {type(e).__name__}: {e}")
            beep("error", self.cfg["beeps"])
        finally:
            self.set_state("recording" if self.recording else "ready")

    def paste(self, text):
        """Clipboard paste beats simulated keystrokes: instant, works everywhere.
        Restore the old clipboard after the target app has had time to read it."""
        import keyboard
        import pyperclip

        old = None
        try:
            old = pyperclip.paste()
        except Exception:
            pass
        pyperclip.copy(text)
        time.sleep(0.05)
        keyboard.send("ctrl+v")
        if old is not None:

            def restore():
                time.sleep(1.0)
                try:
                    pyperclip.copy(old)
                except Exception:
                    pass

            threading.Thread(target=restore, daemon=True).start()

    # ---------- tray ----------

    def set_state(self, state):
        self.state = "paused" if (self.paused and state == "ready") else state
        if self.tray:
            try:
                self.tray.icon = make_icon_image(self.state)
                self.tray.title = f"Flow Dictation — {self.state} (hold {self.cfg['hotkey'].upper()})"
            except Exception:
                pass

    def toggle_pause(self, *_):
        self.paused = not self.paused
        self.set_state("ready")
        log("paused" if self.paused else "resumed")

    def copy_last(self, *_):
        import pyperclip

        if self.last_text:
            pyperclip.copy(self.last_text)

    def open_vocab(self, *_):
        os.startfile(VOCAB_FILE)

    # -- start-with-Windows toggle (shortcut in shell:startup) --

    def startup_lnk(self):
        appdata = os.environ.get("APPDATA", "")
        return Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup" / "Flow Dictation.lnk"

    def autostart_enabled(self, *_):
        return self.startup_lnk().exists()

    def toggle_autostart(self, *_):
        lnk = self.startup_lnk()
        if lnk.exists():
            lnk.unlink()
            log("autostart disabled")
        else:
            pythonw = Path(sys.executable).parent / "pythonw.exe"
            script = Path(__file__).resolve()
            ico = SKILL_DIR / "assets" / "flow.ico"
            import subprocess

            ps = (
                f"$s=(New-Object -ComObject WScript.Shell).CreateShortcut('{lnk}');"
                f"$s.TargetPath='{pythonw}';$s.Arguments='\"{script}\"';"
                f"$s.WorkingDirectory='{script.parent}';$s.IconLocation='{ico}';$s.Save()"
            )
            subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True)
            log("autostart enabled")

    def quit(self, icon, *_):
        log("quit")
        icon.stop()
        os._exit(0)

    # ---------- run ----------

    def run(self):
        import keyboard
        import pystray

        log(f"=== Flow Dictation starting (hold {self.cfg['hotkey'].upper()} to talk) ===")
        threading.Thread(target=self.load_model, daemon=True).start()

        keyboard.on_press_key(self.cfg["hotkey"], self.on_press, suppress=True)
        keyboard.on_release_key(self.cfg["hotkey"], self.on_release, suppress=True)

        menu = pystray.Menu(
            pystray.MenuItem(lambda item: f"Hold {self.cfg['hotkey'].upper()} to dictate", None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Pause", self.toggle_pause, checked=lambda item: self.paused),
            pystray.MenuItem("Copy last transcript", self.copy_last),
            pystray.MenuItem("Edit vocabulary", self.open_vocab),
            pystray.MenuItem("Start with Windows", self.toggle_autostart, checked=self.autostart_enabled),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self.quit),
        )
        self.tray = pystray.Icon("flow-dictation", make_icon_image("loading"), "Flow Dictation — loading model...", menu)
        self.tray.run()


def selftest(wav_path):
    """Transcribe a wav file through the exact same pipeline (no mic/hotkey)."""
    cfg = load_config()
    app = FlowDictation(cfg)
    app.load_model()
    t0 = time.time()
    segments, _ = app.model.transcribe(wav_path, language=cfg["language"], vad_filter=True, initial_prompt=load_vocab_prompt())
    text = " ".join(s.text.strip() for s in segments).strip()
    print(f"SELFTEST ({time.time() - t0:.2f}s): {text}")


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if len(sys.argv) > 2 and sys.argv[1] == "--selftest":
        selftest(sys.argv[2])
    else:
        FlowDictation(load_config()).run()
