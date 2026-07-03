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
import queue
import time
import tkinter as tk
from datetime import datetime
from pathlib import Path

BG = "#141414"
CARD = "#1e1e1e"
FG = "#eaeaea"
DIM = "#9a9a9a"
GOLD = "#d4af37"
RED = "#e05548"
BLUE = "#5b8dd9"

MAX_HISTORY = 500


class UI:
    def __init__(self, history_file):
        self.history_file = Path(history_file)
        self.q = queue.Queue()
        self.history = self._load()
        self.state = "loading"
        self.rec_t0 = None
        self.root = None
        self.overlay = None
        self.overlay_dot = None
        self.overlay_label = None
        self.win = None
        self.listbox = None
        self.detail = None
        self.search_var = None
        self.filtered = []

    # ---------- called from any thread ----------

    def add_entry(self, text, app="", seconds=0.0):
        e = {
            "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "text": text,
            "app": app,
            "seconds": round(seconds, 1),
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
        self.overlay_label = tk.Label(inner, text="Listening", bg=BG, fg=FG, font=("Segoe UI", 11))
        self.overlay_label.pack(side="left")
        self.overlay = o

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
            self.overlay_dot.config(fg=RED)
            self.overlay_label.config(text=f"Listening  {secs // 60}:{secs % 60:02d}")
            self._place_overlay()
            self.overlay.deiconify()
            self._no_activate(self.overlay)
        elif self.state == "transcribing":
            self.rec_t0 = None
            self.overlay_dot.config(fg=BLUE)
            self.overlay_label.config(text="Transcribing…")
            self._place_overlay()
            self.overlay.deiconify()
            self._no_activate(self.overlay)
        else:
            self.rec_t0 = None
            self.overlay.withdraw()

    # ---------- history window ----------

    def _build_history_window(self):
        w = tk.Toplevel(self.root)
        w.title("Flow Dictation — History")
        w.configure(bg=BG)
        w.geometry("420x520")
        w.attributes("-topmost", True)
        try:
            w.iconbitmap(str(Path(__file__).resolve().parent.parent / "assets" / "flow.ico"))
        except Exception:
            pass

        top = tk.Frame(w, bg=BG, padx=10, pady=8)
        top.pack(fill="x")
        tk.Label(top, text="Search", bg=BG, fg=DIM, font=("Segoe UI", 9)).pack(side="left", padx=(0, 6))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self._refresh_list())
        entry = tk.Entry(
            top, textvariable=self.search_var, bg=CARD, fg=FG, insertbackground=GOLD,
            relief="flat", font=("Segoe UI", 10),
        )
        entry.pack(side="left", fill="x", expand=True, ipady=4)

        mid = tk.Frame(w, bg=BG, padx=10)
        mid.pack(fill="both", expand=True)
        sb = tk.Scrollbar(mid)
        sb.pack(side="right", fill="y")
        self.listbox = tk.Listbox(
            mid, bg=CARD, fg=FG, selectbackground=GOLD, selectforeground="#141414",
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
                btns, text=label, command=cmd, bg=CARD, fg=GOLD, relief="flat",
                font=("Segoe UI", 10), padx=14, pady=4, activebackground=GOLD,
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
            preview = e["text"][:52] + ("…" if len(e["text"]) > 52 else "")
            self.listbox.insert("end", f" {day} {t}   {preview}")
        self.count_label.config(text=f"{len(self.filtered)} of {len(self.history)}")

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
                elif cmd == "refresh":
                    self._refresh_list()
                elif cmd == "show_history":
                    self._show_history_window()
        except queue.Empty:
            pass
        self._update_overlay()
        self.root.after(120, self._poll)

    def run(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self._build_overlay()
        self._poll()
        self.root.mainloop()
