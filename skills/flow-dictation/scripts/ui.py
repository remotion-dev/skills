"""ui.py — tkinter UI layer for Flow Dictation.

Two pieces, both dark-themed with the gold brand accent:
  1. Overlay pill: a small frameless always-on-top capsule at the bottom-center
     of the screen that appears while recording ("Listening 0:03") and
     transcribing, then vanishes. Marked WS_EX_NOACTIVATE so it can never steal
     focus from the app the user is dictating into.
  2. History window: searchable record of every dictation (persisted to
     outputs/history.jsonl), newest first, click an entry to see the full text,
     Copy button / double-click to copy.

Threading: all tk calls happen on the main thread inside run(); other threads
talk to the UI only through the queue (add_entry / set_state / show_history).
"""
import json
import math
import queue
import time
import tkinter as tk
from datetime import datetime
from pathlib import Path

BG = "#141414"
CARD = "#1e1e1e"
FG = "#eaeaea"
DIM = "#9a9a9a"
ACCENT = "#a78bfa"   # soft violet — the app accent (gold retired 2026-07-02)
RED = "#e05548"
BLUE = "#5b8dd9"
PURPLE = "#aa6edc"
PINK = "#ec4899"

# waveform gradient endpoints (violet -> magenta), per state
WAVE_COLORS = {
    "recording": ((139, 92, 246), (236, 72, 153)),
    "transcribing": ((91, 141, 217), (139, 92, 246)),
    "polishing": ((170, 110, 220), (217, 70, 239)),
}


def _grad(a, b, t):
    return "#%02x%02x%02x" % tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

MAX_HISTORY = 500
TYPING_WPM = 40  # baseline for the "time saved" stat


class UI:
    def __init__(self, history_file, levels=None):
        self.history_file = Path(history_file)
        self.levels = levels if levels is not None else []
        self.q = queue.Queue()
        self.history = self._load()
        self.state = "loading"
        self.polish = False
        self.locked = False
        self.rec_t0 = None
        self.root = None
        self.overlay = None
        self.overlay_dot = None
        self.overlay_label = None
        self.wave = None
        self._disp = []      # displayed envelope amplitudes (animated toward targets)
        self._phase = 0.0    # wave phase, advances each frame
        self.win = None
        self.listbox = None
        self.detail = None
        self.search_var = None
        self.stats_label = None
        self.filtered = []

    # ---------- called from any thread ----------

    def add_entry(self, text, app="", seconds=0.0, polished=False):
        e = {
            "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "text": text,
            "app": app,
            "seconds": round(seconds, 1),
            "polished": polished,
        }
        self.history.append(e)
        self.history = self.history[-MAX_HISTORY:]
        try:
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.history_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
        except Exception:
            pass
        self.q.put(("refresh", None))

    def set_state(self, state):
        self.q.put(("state", state))

    def set_polish(self, on):
        self.q.put(("polish", on))

    def set_locked(self, on):
        self.q.put(("locked", on))

    def show_history(self):
        self.q.put(("show_history", None))

    # ---------- internals (main thread only) ----------

    def _load(self):
        items = []
        try:
            for line in self.history_file.read_text(encoding="utf-8").splitlines():
                try:
                    items.append(json.loads(line))
                except Exception:
                    pass
        except FileNotFoundError:
            pass
        return items[-MAX_HISTORY:]

    def _no_activate(self, widget):
        """WS_EX_NOACTIVATE so the overlay never takes focus from the target app."""
        try:
            import ctypes

            widget.update_idletasks()
            hwnd = widget.winfo_id()
            GWL_EXSTYLE = -20
            WS_EX_NOACTIVATE = 0x08000000
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_NOACTIVATE)
        except Exception:
            pass

    def _build_overlay(self):
        o = tk.Toplevel(self.root)
        o.withdraw()
        o.overrideredirect(True)
        o.attributes("-topmost", True)
        o.attributes("-alpha", 0.93)
        o.configure(bg=BG)
        inner = tk.Frame(o, bg=BG, padx=16, pady=8)
        inner.pack()
        self.overlay_dot = tk.Label(inner, text="●", bg=BG, fg=RED, font=("Segoe UI", 12))
        self.overlay_dot.pack(side="left", padx=(0, 8))
        self.wave = tk.Canvas(inner, width=150, height=26, bg=BG, highlightthickness=0)
        self.wave.pack(side="left", padx=(0, 10))
        self.overlay_label = tk.Label(inner, text="Listening", bg=BG, fg=FG, font=("Segoe UI", 11))
        self.overlay_label.pack(side="left")
        self.overlay = o

    def _draw_wave(self, state):
        """Voice wave: a continuous oscillating line whose amplitude follows the
        smoothed speech envelope, drawn in a violet->magenta gradient with a
        fainter phase-shifted echo line underneath (getty-style sound wave).
        Fast-attack/slow-decay animation keeps the motion fluid; the phase
        advances every frame so the line undulates even between words."""
        self.wave.delete("all")
        w, h, env_n, pts_n = 150, 26, 30, 60
        mid = h / 2
        samples = list(self.levels)[-env_n:]
        # pad on the left so new audio enters from the right like a ticker
        targets = [0.0] * (env_n - len(samples)) + [min(1.0, (s * 14) ** 0.5) for s in samples]
        smoothed = [
            (targets[max(0, i - 1)] + 2 * targets[i] + targets[min(env_n - 1, i + 1)]) / 4
            for i in range(env_n)
        ]
        if len(self._disp) != env_n:
            self._disp = [0.0] * env_n
        for i in range(env_n):
            t, d = smoothed[i], self._disp[i]
            self._disp[i] = d + (t - d) * (0.6 if t > d else 0.22)
        self._phase += 0.55

        def envelope(pos):  # linear interp of _disp at fractional index
            f = pos * (env_n - 1)
            i = min(env_n - 2, int(f))
            frac = f - i
            e = self._disp[i] * (1 - frac) + self._disp[i + 1] * frac
            return 0.05 + e * 0.95  # small idle ripple so it never flatlines

        a, b = WAVE_COLORS.get(state, WAVE_COLORS["recording"])
        for layer, (amp_k, freq, ph, width) in enumerate([
            (0.55, 0.62, 1.9, 1),   # echo line: smaller, offset, thin
            (1.00, 0.55, 0.0, 2),   # main line
        ]):
            pts = []
            for j in range(pts_n + 1):
                pos = j / pts_n
                y = mid + envelope(pos) * (mid - 2) * amp_k * math.sin(
                    self._phase * (0.8 if layer == 0 else 1.0) + j * freq + ph
                )
                pts.append((pos * w, y))
            for j in range(pts_n):
                c = _grad(a, b, j / pts_n)
                if layer == 0:  # dim the echo toward the background
                    c = _grad(tuple(int(x * 0.45) for x in a), tuple(int(x * 0.45) for x in b), j / pts_n)
                self.wave.create_line(*pts[j], *pts[j + 1], fill=c, width=width, capstyle="round")

    def _place_overlay(self):
        self.overlay.update_idletasks()
        w = self.overlay.winfo_reqwidth()
        h = self.overlay.winfo_reqheight()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.overlay.geometry(f"{w}x{h}+{(sw - w) // 2}+{sh - h - 80}")

    def _update_overlay(self):
        if self.state == "recording":
            if self.rec_t0 is None:
                self.rec_t0 = time.time()
            secs = int(time.time() - self.rec_t0)
            suffix = "  ✨ polish" if self.polish else ""
            if self.locked:
                suffix += "  🔒 tap Ctrl+Alt to finish"
            self.overlay_dot.config(fg=PURPLE if self.polish else PINK)
            self._draw_wave("polishing" if self.polish else "recording")
            self.overlay_label.config(text=f"Listening  {secs // 60}:{secs % 60:02d}{suffix}")
            self._place_overlay()
            self.overlay.deiconify()
            self._no_activate(self.overlay)
        elif self.state in ("transcribing", "polishing"):
            self.rec_t0 = None
            polishing = self.state == "polishing"
            self.overlay_dot.config(fg=PURPLE if polishing else BLUE)
            self._draw_wave(self.state)
            self.overlay_label.config(text="Polishing with Claude…" if polishing else "Transcribing…")
            self._place_overlay()
            self.overlay.deiconify()
            self._no_activate(self.overlay)
        else:
            self.rec_t0 = None
            self.overlay.withdraw()

    # ---------- history window ----------

    def _build_history_window(self):
        w = tk.Toplevel(self.root)
        w.title("Flow Dictation")
        w.configure(bg=BG)
        w.geometry("500x600")
        w.attributes("-topmost", True)
        try:
            w.iconbitmap(str(Path(__file__).resolve().parent.parent / "assets" / "flow.ico"))
        except Exception:
            pass

        tk.Label(
            w, text="Speak naturally, paste instantly — hold Ctrl+Alt anywhere",
            bg=BG, fg=DIM, font=("Segoe UI", 9), anchor="w", padx=12, pady=8,
        ).pack(fill="x")

        # Blip-style stat cards: value on top, caption below
        cards = tk.Frame(w, bg=BG, padx=10)
        cards.pack(fill="x")
        self.stat_vals = {}
        for key, caption in (
            ("today", "words today"),
            ("month", "words this month"),
            ("wpm", "avg dictation WPM"),
            ("saved", "money saved"),
        ):
            card = tk.Frame(cards, bg=CARD, padx=10, pady=10)
            card.pack(side="left", expand=True, fill="both", padx=3)
            val = tk.Label(card, text="—", bg=CARD, fg=ACCENT, font=("Segoe UI", 15, "bold"))
            val.pack()
            tk.Label(card, text=caption, bg=CARD, fg=DIM, font=("Segoe UI", 8)).pack()
            self.stat_vals[key] = val

        tk.Label(
            w, text="Recent Transcriptions", bg=BG, fg=FG,
            font=("Segoe UI", 11, "bold"), anchor="w", padx=12, pady=8,
        ).pack(fill="x")

        top = tk.Frame(w, bg=BG, padx=10, pady=8)
        top.pack(fill="x")
        tk.Label(top, text="Search", bg=BG, fg=DIM, font=("Segoe UI", 9)).pack(side="left", padx=(0, 6))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self._refresh_list())
        entry = tk.Entry(
            top, textvariable=self.search_var, bg=CARD, fg=FG, insertbackground=ACCENT,
            relief="flat", font=("Segoe UI", 10),
        )
        entry.pack(side="left", fill="x", expand=True, ipady=4)

        mid = tk.Frame(w, bg=BG, padx=10)
        mid.pack(fill="both", expand=True)
        sb = tk.Scrollbar(mid)
        sb.pack(side="right", fill="y")
        self.listbox = tk.Listbox(
            mid, bg=CARD, fg=FG, selectbackground=ACCENT, selectforeground="#141414",
            relief="flat", font=("Segoe UI", 10), activestyle="none", yscrollcommand=sb.set,
        )
        self.listbox.pack(fill="both", expand=True)
        sb.config(command=self.listbox.yview)
        self.listbox.bind("<<ListboxSelect>>", lambda e: self._show_detail())
        self.listbox.bind("<Double-Button-1>", lambda e: self._copy_selected())

        self.detail = tk.Text(
            w, height=5, bg=CARD, fg=FG, relief="flat", wrap="word",
            font=("Segoe UI", 10), padx=8, pady=6, state="disabled",
        )
        self.detail.pack(fill="x", padx=10, pady=(8, 0))

        btns = tk.Frame(w, bg=BG, pady=8)
        btns.pack(fill="x", padx=10)
        for label, cmd in (("Copy", self._copy_selected), ("Clear history", self._clear_history)):
            tk.Button(
                btns, text=label, command=cmd, bg=CARD, fg=ACCENT, relief="flat",
                font=("Segoe UI", 10), padx=14, pady=4, activebackground=ACCENT,
                activeforeground="#141414", cursor="hand2",
            ).pack(side="left", padx=(0, 8))
        self.count_label = tk.Label(btns, text="", bg=BG, fg=DIM, font=("Segoe UI", 9))
        self.count_label.pack(side="right")

        w.protocol("WM_DELETE_WINDOW", w.withdraw)
        self.win = w
        self._refresh_list()

    def _refresh_list(self):
        if not (self.win and self.listbox):
            return
        needle = (self.search_var.get() if self.search_var else "").lower()
        self.filtered = [
            e for e in reversed(self.history)
            if needle in e["text"].lower() or needle in e.get("app", "").lower()
        ]
        self.listbox.delete(0, "end")
        for e in self.filtered:
            t = e["ts"][11:16]
            day = e["ts"][5:10]
            mark = "✨" if e.get("polished") else " "
            preview = e["text"][:50] + ("…" if len(e["text"]) > 50 else "")
            self.listbox.insert("end", f" {day} {t} {mark} {preview}")
        self.count_label.config(text=f"{len(self.filtered)} of {len(self.history)}")
        self._refresh_stats()

    def _refresh_stats(self):
        if not getattr(self, "stat_vals", None):
            return
        now = datetime.now()
        today, month = now.strftime("%Y-%m-%d"), now.strftime("%Y-%m")
        t_words = t_secs = d_words = m_words = 0
        for e in self.history:
            words = len(e["text"].split())
            t_words += words
            t_secs += e.get("seconds", 0) or 0
            if e["ts"][:10] == today:
                d_words += words
            if e["ts"][:7] == month:
                m_words += words
        wpm = (t_words / (t_secs / 60)) if t_secs else 0
        # same framing Blip uses: time saved vs typing, valued at $15/hr
        saved_hours = max(0.0, t_words / TYPING_WPM - t_secs / 60) / 60
        self.stat_vals["today"].config(text=f"{d_words:,}")
        self.stat_vals["month"].config(text=f"{m_words:,}")
        self.stat_vals["wpm"].config(text=f"{wpm:.0f}")
        self.stat_vals["saved"].config(text=f"${saved_hours * 15:,.2f}")

    def _selected_entry(self):
        sel = self.listbox.curselection() if self.listbox else ()
        return self.filtered[sel[0]] if sel else None

    def _show_detail(self):
        e = self._selected_entry()
        if not e:
            return
        self.detail.config(state="normal")
        self.detail.delete("1.0", "end")
        app = f"  →  {e['app']}" if e.get("app") else ""
        self.detail.insert("1.0", f"{e['ts']}{app}\n{e['text']}")
        self.detail.config(state="disabled")

    def _copy_selected(self):
        e = self._selected_entry()
        if not e:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(e["text"])

    def _clear_history(self):
        self.history = []
        try:
            self.history_file.write_text("", encoding="utf-8")
        except Exception:
            pass
        self._refresh_list()

    def _show_history_window(self):
        if self.win is None or not self.win.winfo_exists():
            self._build_history_window()
        self._refresh_list()
        self.win.deiconify()
        self.win.lift()

    # ---------- main loop ----------

    def _poll(self):
        try:
            while True:
                cmd, arg = self.q.get_nowait()
                if cmd == "state":
                    self.state = arg
                elif cmd == "polish":
                    self.polish = arg
                elif cmd == "locked":
                    self.locked = arg
                elif cmd == "refresh":
                    self._refresh_list()
                elif cmd == "show_history":
                    self._show_history_window()
        except queue.Empty:
            pass
        self._update_overlay()
        self.root.after(60, self._poll)

    def run(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self._build_overlay()
        self._poll()
        self.root.mainloop()
