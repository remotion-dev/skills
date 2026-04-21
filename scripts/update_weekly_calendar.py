#!/usr/bin/env python3
"""
update_weekly_calendar.py — shift the weekly calendar dashboard forward one
week (Apr 20-26 → Apr 27-May 3) and apply the UNIFIED_FINAL_V2 overlay so
the weekly view matches the single-topic dashboards visually.

Keeps historical date references (Apr 17 milestone, Apr 5/6/10/14/18 data
points) unchanged. Leaves the filename as-is so existing links don't break.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path("/var/tmp/stage3/skills")
TARGET = REPO / "content-calendars" / "2026-04-20-production-calendar-v6.html"


# Forward-shifts for next-week references. Order matters — do the longer/
# more-specific strings first so we don't accidentally half-replace.
DATE_SWAPS = [
    # Week-range header
    ("Week of April 20&ndash;26, 2026", "Week of April 27&ndash;May 3, 2026"),
    ("Week of April 20-26, 2026", "Week of April 27-May 3, 2026"),
    ("April 20&ndash;26", "April 27&ndash;May 3"),
    ("April 20-26", "April 27-May 3"),
    # Full dates
    ("April 20, 2026", "April 27, 2026"),
    ("April 21, 2026", "April 28, 2026"),
    ("April 22, 2026", "April 29, 2026"),
    ("April 23, 2026", "April 30, 2026"),
    ("April 24, 2026", "May 1, 2026"),
    ("April 25, 2026", "May 2, 2026"),
    ("April 26, 2026", "May 3, 2026"),
    # Short forms (regex-safe — only when word-bounded)
]

# Short-form swaps need word-boundary matching so "Apr 10" and "Apr 200"
# don't match when we only want "Apr 20".
SHORT_DAY_SWAPS = [
    (r'\bApr 20\b', 'Apr 27'),
    (r'\bApr 21\b', 'Apr 28'),
    (r'\bApr 22\b', 'Apr 29'),
    (r'\bApr 23\b', 'Apr 30'),
    (r'\bApr 24\b', 'May 1'),
    (r'\bApr 25\b', 'May 2'),
    (r'\bApr 26\b', 'May 3'),
]


def main() -> int:
    if not TARGET.exists():
        print(f"MISSING: {TARGET}")
        return 1

    html = TARGET.read_text(encoding="utf-8")
    original = html

    # 1. Apply literal date swaps (forward by 7 days)
    for old, new in DATE_SWAPS:
        html = html.replace(old, new)

    # 2. Short-form Apr X → new date (word-bounded so historical data stays)
    for pattern, new in SHORT_DAY_SWAPS:
        html = re.sub(pattern, new, html)

    if html != original:
        TARGET.write_text(html, encoding="utf-8")
        print(f"Dates shifted forward 7 days")
    else:
        print(f"No date changes needed")

    # 3. Apply the UNIFIED_FINAL_V2 overlay via subprocess so we share the
    #    canonical transformation logic instead of duplicating it.
    r = subprocess.run(
        [sys.executable,
         str(REPO / "scripts" / "unify_final.py"),
         "--target", str(TARGET),
         "--day", "Week",
         "--date", "April 27 \u2013 May 3, 2026"],
        capture_output=True, text=True,
    )
    if r.returncode == 0:
        print(f"Unified: {r.stdout.strip()}")
        return 0
    else:
        print(f"WARN: unify failed (rc={r.returncode}): {r.stderr.strip()[:200]}")
        return r.returncode


if __name__ == "__main__":
    sys.exit(main())
