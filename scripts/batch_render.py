#!/usr/bin/env python3
"""
batch_render.py — Render all 5 video formats for a topic with one command.

Instead of clicking 5 separate Copy Render buttons and running PowerShell
5 times, this queues all 5 HeyGen renders in sequence.

Usage:
    python scripts/batch_render.py --topic epa-two-years-homicide-free

Options:
    --formats <list>     Comma-separated format keys to render.
                         Default: yt-long-pt1,yt-short,ig-reel-1,ig-reel-2,tiktok
    --delay <seconds>    Pause between HeyGen API calls (default: 5).
                         Avoids rate-limit pileups.
    --dry-run            Show what would be submitted without hitting the API.

Topics (same list as heygen_render.py):
    epa-two-years-homicide-free
    peninsula-bidding-wars-back
    epa-market-update
    ca-smoke-detector-compliance
    woodland-park-772-units

Per-format avatar looks (hard-coded to match the dashboard defaults):
    yt-long-pt1  -> digital_twin   (authentic video-trained, best for long-form)
    yt-short     -> fashion_flip   (higher energy for hooks)
    ig-reel-1    -> casual_chic    (approachable)
    ig-reel-2    -> freshly_ironed (polished)
    tiktok       -> fashion_flip   (energetic)

Success looks like:
    [1/5] yt-long-pt1 ... queued video_id=abc123
    [2/5] yt-short    ... queued video_id=def456
    ...
    All 5 submitted. Run scripts/render_monitor.py in a few minutes to pick up
    completion status.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path


# Default format -> avatar mapping (matches the HEYGEN_RENDER config in each
# dashboard's builder). Override per-format if needed by editing this map.
DEFAULT_FORMATS = [
    ("yt-long-pt1", "digital_twin"),
    ("yt-short",    "fashion_flip"),
    ("ig-reel-1",   "casual_chic"),
    ("ig-reel-2",   "freshly_ironed"),
    ("tiktok",      "fashion_flip"),
]

KNOWN_TOPICS = {
    "epa-two-years-homicide-free",
    "peninsula-bidding-wars-back",
    "epa-market-update",
    "ca-smoke-detector-compliance",
    "woodland-park-772-units",
}

REPO_ROOT = Path(__file__).resolve().parent.parent
RENDER_SCRIPT = REPO_ROOT / "scripts" / "heygen_render.py"


def die(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def parse_formats(arg: str | None) -> list[tuple[str, str]]:
    """Accept a comma-separated format list. Each format uses its default look
    from DEFAULT_FORMATS; unknown formats raise."""
    if not arg:
        return DEFAULT_FORMATS
    wanted = [x.strip() for x in arg.split(",") if x.strip()]
    default_map = dict(DEFAULT_FORMATS)
    out = []
    for fk in wanted:
        if fk not in default_map:
            die(f"Unknown format '{fk}'. Valid: {', '.join(default_map.keys())}")
        out.append((fk, default_map[fk]))
    return out


def run_one(topic: str, format_key: str, look: str, dry_run: bool) -> tuple[bool, str]:
    """Invoke heygen_render.py as a subprocess. Returns (ok, message)."""
    cmd = [
        sys.executable,
        str(RENDER_SCRIPT),
        "--topic", topic,
        "--format", format_key,
        "--look", look,
    ]
    if dry_run:
        cmd.append("--dry-run")

    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return False, "timeout (>120s)"

    if r.returncode != 0:
        stderr = r.stderr.strip().splitlines()
        last = stderr[-1] if stderr else "unknown error"
        return False, last[:200]

    # heygen_render.py prints the video_id as part of its output. Extract it.
    out_lines = r.stdout.splitlines()
    video_id = None
    for line in out_lines:
        if "video_id:" in line:
            video_id = line.split("video_id:")[-1].strip()
            break

    if dry_run:
        return True, "dry-run OK"
    return True, f"queued video_id={video_id or '?'}"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Queue all 5 HeyGen video formats for a topic in one command.",
    )
    ap.add_argument("--topic", required=True, choices=sorted(KNOWN_TOPICS),
                    help="Topic slug to render. Same slugs the dashboards use.")
    ap.add_argument("--formats", default=None,
                    help="Comma-separated format keys (default: all 5 video formats).")
    ap.add_argument("--delay", type=int, default=5,
                    help="Seconds to pause between API calls (default: 5).")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print what would be submitted without calling HeyGen.")
    args = ap.parse_args()

    if not RENDER_SCRIPT.exists():
        die(f"heygen_render.py not found at {RENDER_SCRIPT}")

    if not args.dry_run and not os.environ.get("HEYGEN_API_KEY"):
        die("HEYGEN_API_KEY env var is not set. Use --dry-run to preview without API.")

    formats = parse_formats(args.formats)

    print(f"Batch render plan:")
    print(f"  Topic:   {args.topic}")
    print(f"  Formats: {len(formats)}")
    print(f"  Delay:   {args.delay}s between calls")
    print(f"  Mode:    {'DRY-RUN' if args.dry_run else 'LIVE'}")
    print()

    results = []
    total = len(formats)
    for i, (fk, look) in enumerate(formats, start=1):
        prefix = f"[{i}/{total}] {fk:<13} "
        print(f"{prefix}submitting ({look})...", flush=True)
        ok, msg = run_one(args.topic, fk, look, args.dry_run)
        status = "OK  " if ok else "FAIL"
        print(f"{prefix}{status}  {msg}")
        results.append((fk, ok, msg))

        # Throttle between calls (except after the last one)
        if i < total and not args.dry_run:
            time.sleep(args.delay)

    # Summary
    ok_count = sum(1 for _, ok, _ in results if ok)
    print()
    print(f"Done: {ok_count}/{total} submitted successfully.")
    if ok_count == total:
        if not args.dry_run:
            print()
            print("Next step: run scripts/render_monitor.py in ~3 minutes to poll")
            print("HeyGen for completion status. The dashboards will then show")
            print("green Watch Video cards as each render finishes.")
        return 0
    else:
        print()
        print("Some renders failed. Failures:")
        for fk, ok, msg in results:
            if not ok:
                print(f"  {fk}: {msg}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
