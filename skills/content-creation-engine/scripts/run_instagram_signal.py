#!/usr/bin/env python3
"""
run_instagram_signal.py
------------------------
Thin wrapper for content-creation-engine Phase IG (Instagram signal).

Reads standard hashtag + handle targets from the standalone
instagram-competitor-scraper skill, calls its scrape.py, optionally pipes
results to the Obsidian vault via video-to-obsidian, and writes a JSON
output file that the engine's downstream scoring step consumes.

Usage:
    python3 run_instagram_signal.py --days 7 --top 30 --pipe-to-obsidian
    python3 run_instagram_signal.py --dry-run
    python3 run_instagram_signal.py --hashtags x,y --handles a,b  # override targets

Requires:
    pip install python-dotenv apify-client --break-system-packages
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Skills root: scripts/ -> content-creation-engine/ -> skills/ -> Skills/
SKILLS_ROOT = Path(__file__).resolve().parents[3]
SCRAPER_SCRIPT = SKILLS_ROOT / "skills" / "instagram-competitor-scraper" / "scripts" / "scrape.py"
TARGETS_FILE = SKILLS_ROOT / "skills" / "instagram-competitor-scraper" / "references" / "standard-targets.md"
OUTPUTS_DIR = Path(__file__).resolve().parent.parent / "outputs"


def parse_standard_targets():
    if not TARGETS_FILE.exists():
        print(f"ERROR: standard-targets.md not found at {TARGETS_FILE}", file=sys.stderr)
        sys.exit(1)

    text = TARGETS_FILE.read_text(encoding="utf-8")
    hashtags = []
    handles = []
    section = None

    for line in text.splitlines():
        l = line.strip()
        if l.startswith("## "):
            heading = l[3:].lower()
            if "hashtag" in heading:
                section = "hashtag"
            elif "handle" in heading or "competitor" in heading:
                section = "handle"
            else:
                section = None
            continue

        m = re.match(r"^-\s+`([^`]+)`", l)
        if not m:
            continue
        value = m.group(1).strip().lstrip("#").lstrip("@")
        if "PLACEHOLDER" in value.upper():
            continue
        if section == "hashtag":
            hashtags.append(value)
        elif section == "handle":
            handles.append(value)

    return hashtags, handles


def main():
    parser = argparse.ArgumentParser(description="content-creation-engine Phase IG: Instagram signal")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--top", type=int, default=30)
    parser.add_argument("--limit-per-target", type=int, default=30)
    parser.add_argument("--hashtags", default="")
    parser.add_argument("--handles", default="")
    parser.add_argument("--pipe-to-obsidian", action="store_true")
    parser.add_argument("--output", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not SCRAPER_SCRIPT.exists():
        print(f"ERROR: scraper script missing at {SCRAPER_SCRIPT}", file=sys.stderr)
        sys.exit(1)

    if args.hashtags or args.handles:
        hashtags = [h.strip() for h in args.hashtags.split(",") if h.strip()]
        handles = [h.strip() for h in args.handles.split(",") if h.strip()]
    else:
        hashtags, handles = parse_standard_targets()

    if not hashtags and not handles:
        print("ERROR: no targets — standard-targets.md has only placeholders", file=sys.stderr)
        print(f"Edit {TARGETS_FILE} with real handles before running.", file=sys.stderr)
        sys.exit(1)

    print(f"[ig-signal] Hashtags: {hashtags}", file=sys.stderr)
    print(f"[ig-signal] Handles:  {handles}", file=sys.stderr)
    print(f"[ig-signal] Window:   last {args.days} days, top {args.top}", file=sys.stderr)

    cmd = [
        sys.executable, str(SCRAPER_SCRIPT),
        "--top", str(args.top),
        "--days", str(args.days),
        "--limit-per-target", str(args.limit_per_target),
        "--json",
    ]
    if hashtags:
        cmd.extend(["--hashtags", ",".join(hashtags)])
    if handles:
        cmd.extend(["--handles", ",".join(handles)])
    if args.pipe_to_obsidian:
        cmd.append("--pipe-to-obsidian")

    if args.dry_run:
        print("[dry-run] Would run:")
        print("  " + " ".join(f'\"{c}\"' if " " in c else c for c in cmd))
        return

    print("[ig-signal] Calling scraper...", file=sys.stderr)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)

    if result.returncode != 0:
        print(f"[ig-signal] Scraper FAILED (exit {result.returncode})", file=sys.stderr)
        print(result.stderr[-1000:], file=sys.stderr)
        sys.exit(2)

    try:
        posts = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"[ig-signal] Scraper returned non-JSON output: {e}", file=sys.stderr)
        sys.exit(3)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out_path = Path(args.output) if args.output else OUTPUTS_DIR / f"instagram-signal-{ts}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    output_payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "window_days": args.days,
        "hashtags": hashtags,
        "handles": handles,
        "post_count": len(posts),
        "posts": posts,
    }
    out_path.write_text(json.dumps(output_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[ig-signal] Wrote {len(posts)} posts -> {out_path}", file=sys.stderr)
    print(str(out_path))


if __name__ == "__main__":
    main()
