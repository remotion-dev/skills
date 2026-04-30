#!/usr/bin/env python3
"""
render_monitor.py — Poll HeyGen for render completions and publish a status
file the dashboards read.

What this does (in plain English):
    1. Reads ~/heygen_renders/render_log.jsonl  (every render you've triggered).
    2. For each video_id, asks HeyGen "is it done yet?" via the v1 status API.
    3. When a video is DONE, grabs the MP4 URL + thumbnail + duration.
    4. Writes ~/heygen_renders/render_status.json  (a keyed-by-slug lookup).
    5. Copies that file into the skills repo so GitHub Pages serves it.
    6. Git-commits + pushes the status file so dashboards fetch it live.

Run it manually any time, OR schedule it every 2 minutes via Task Scheduler
on Windows. Once the MP4 lands, the dashboard shows a ▶ Watch Video button
and an embedded preview automatically.

Usage (from PowerShell):
    python render_monitor.py
    python render_monitor.py --push             # also git-commit + push
    python render_monitor.py --once --no-push   # one-shot, local only

Env vars required:
    HEYGEN_API_KEY      (already set for heygen_render.py)

Optional:
    SKILLS_REPO_PATH    Where your local clone of Graehamwatts/skills lives.
                        Defaults to C:\\Users\\<user>\\skills on Windows,
                        ~/skills elsewhere. Override with --repo-path.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

HOME = Path.home()
LOG_DIR = HOME / "heygen_renders"
LOG_FILE = LOG_DIR / "render_log.jsonl"
STATUS_FILE_LOCAL = LOG_DIR / "render_status.json"

DEFAULT_REPO_PATH = HOME / "skills"

STATUS_API = "https://api.heygen.com/v1/video_status.get"

TERMINAL_STATES = {"completed", "failed"}


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def log(msg: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def die(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def require_api_key() -> str:
    key = os.environ.get("HEYGEN_API_KEY")
    if not key:
        die(
            "HEYGEN_API_KEY env var is not set.\n"
            "Run in PowerShell:\n"
            '   [Environment]::SetEnvironmentVariable("HEYGEN_API_KEY", "sk_V2_...", "User")\n'
            "Then restart PowerShell."
        )
    return key


def load_log() -> list[dict]:
    """Read ~/heygen_renders/render_log.jsonl. Returns list of entries."""
    if not LOG_FILE.exists():
        return []
    entries = []
    for line in LOG_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def load_existing_status() -> dict:
    if not STATUS_FILE_LOCAL.exists():
        return {"updated_at": None, "videos": {}}
    try:
        return json.loads(STATUS_FILE_LOCAL.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"updated_at": None, "videos": {}}


# ---------------------------------------------------------------------------
# HeyGen status check
# ---------------------------------------------------------------------------

def check_status(video_id: str, api_key: str) -> dict:
    url = f"{STATUS_API}?video_id={video_id}"
    req = Request(
        url,
        headers={"X-Api-Key": api_key, "Accept": "application/json"},
    )
    try:
        raw = urlopen(req, timeout=20).read().decode("utf-8")
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore") if e.fp else ""
        return {"status": "error", "error": f"HTTP {e.code}: {body[:200]}"}
    except URLError as e:
        return {"status": "error", "error": f"Network: {e}"}
    try:
        return json.loads(raw).get("data") or {"status": "error", "error": raw[:200]}
    except json.JSONDecodeError:
        return {"status": "error", "error": raw[:200]}


# ---------------------------------------------------------------------------
# Core run
# ---------------------------------------------------------------------------

def run_once(api_key: str) -> dict:
    entries = load_log()
    if not entries:
        log("No renders in log yet. Nothing to check.")
        return {"updated_at": datetime.now(timezone.utc).isoformat(), "videos": {}}

    state = load_existing_status()
    videos = state.get("videos", {})

    checked = 0
    newly_done = 0
    for entry in entries:
        video_id = entry.get("video_id")
        if not video_id:
            continue

        # Skip if already in terminal state — HeyGen video_url won't change
        existing = videos.get(video_id) or {}
        if existing.get("status") in TERMINAL_STATES:
            continue

        checked += 1
        data = check_status(video_id, api_key)
        status = data.get("status", "unknown")

        record = {
            "video_id": video_id,
            "topic_slug": entry.get("topic"),
            "format_key": entry.get("format"),
            "look": entry.get("look"),
            "aspect": entry.get("aspect"),
            "status": status,
            "video_url": data.get("video_url"),
            "video_url_caption": data.get("video_url_caption"),
            "thumbnail_url": data.get("thumbnail_url"),
            "gif_url": data.get("gif_url"),
            "duration": data.get("duration"),
            "error": data.get("error"),
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "submitted_dashboard_url": entry.get("dashboard_url"),
        }
        videos[video_id] = record

        label = f"{entry.get('topic', '?')} / {entry.get('format', '?')}"
        if status == "completed":
            newly_done += 1
            log(f"  DONE  {label}  ({data.get('duration', '?')}s)")
        elif status == "failed":
            log(f"  FAIL  {label}  — {data.get('error')}")
        elif status == "error":
            log(f"  ERR   {label}  — {data.get('error')}")
        else:
            log(f"  ...   {label}  [{status}]")

    state = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "videos": videos,
    }

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    STATUS_FILE_LOCAL.write_text(json.dumps(state, indent=2), encoding="utf-8")
    log(f"Checked {checked} in-flight videos. {newly_done} newly completed.")
    log(f"Wrote {STATUS_FILE_LOCAL}")
    return state


# ---------------------------------------------------------------------------
# Push to GitHub (so dashboards served from GitHub Pages can fetch)
# ---------------------------------------------------------------------------

def git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git"] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )


def push_status_to_repo(repo_path: Path, status: dict) -> bool:
    if not repo_path.exists():
        log(f"Repo path not found: {repo_path}  (skipping push)")
        log(f"Set SKILLS_REPO_PATH env var or pass --repo-path.")
        return False
    if not (repo_path / ".git").exists():
        log(f"Not a git repo: {repo_path}  (skipping push)")
        return False

    target = repo_path / "render_status.json"
    target.write_text(json.dumps(status, indent=2), encoding="utf-8")

    add = git(["add", "render_status.json"], repo_path)
    if add.returncode != 0:
        log(f"git add failed: {add.stderr.strip()}")
        return False

    status_check = git(["status", "--porcelain", "render_status.json"], repo_path)
    if not status_check.stdout.strip():
        log("No changes to render_status.json — skipping commit.")
        return True

    commit_msg = f"Update render_status.json ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
    commit = git(["commit", "-m", commit_msg, "--only", "render_status.json"], repo_path)
    if commit.returncode != 0:
        log(f"git commit failed: {commit.stderr.strip() or commit.stdout.strip()}")
        return False

    push = git(["push"], repo_path)
    if push.returncode != 0:
        log(f"git push failed: {push.stderr.strip() or push.stdout.strip()}")
        return False

    log("Pushed render_status.json to GitHub.")
    return True


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Poll HeyGen for render completions and publish a status file.",
    )
    ap.add_argument("--push", action="store_true",
                    help="Commit + push render_status.json to the skills repo (default).")
    ap.add_argument("--no-push", dest="push", action="store_false",
                    help="Skip the git push step (local-only).")
    ap.set_defaults(push=True)
    ap.add_argument("--repo-path", default=None,
                    help=f"Path to local clone of Graehamwatts/skills. "
                         f"Default: {DEFAULT_REPO_PATH}")
    ap.add_argument("--watch", type=int, default=0, metavar="SECONDS",
                    help="Keep polling every N seconds until all videos are "
                         "done (or Ctrl-C). 0 = run once (default).")
    ap.add_argument("--once", action="store_true",
                    help="Run a single pass (same as default).")
    args = ap.parse_args()

    api_key = require_api_key()

    repo_path = Path(args.repo_path) if args.repo_path else Path(
        os.environ.get("SKILLS_REPO_PATH") or DEFAULT_REPO_PATH
    )

    def one_pass():
        state = run_once(api_key)
        if args.push:
            push_status_to_repo(repo_path, state)
        in_flight = sum(
            1 for v in state.get("videos", {}).values()
            if v.get("status") not in TERMINAL_STATES
        )
        return in_flight

    if args.watch and args.watch > 0:
        log(f"Watch mode — polling every {args.watch}s. Ctrl-C to stop.")
        try:
            while True:
                in_flight = one_pass()
                if in_flight == 0:
                    log("All renders reached terminal state. Exiting watch loop.")
                    return
                time.sleep(args.watch)
        except KeyboardInterrupt:
            log("Interrupted.")
            return
    else:
        one_pass()


if __name__ == "__main__":
    main()
