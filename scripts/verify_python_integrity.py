#!/usr/bin/env python3
"""
verify_python_integrity.py -- compile-check every Python file in the skills repo.

Catches truncated / corrupted .py files. This is the recurring failure mode:
a bulk text-rewrite during a skill consolidation chops a file mid-string, it gets
committed broken, and it ships silently until someone runs the skill weeks later
(e.g. weekly-calendar-builder.py truncated in the May 2026 social-media-analyzer
consolidation; prompts-library-builder.py truncated and committed broken).

Run with NO args to scan the whole skills/ tree (used by the auto-push hook).
Pass explicit file paths to check only those (used by the pre-push hook for the
files in the push range).

Exit codes:
  0  all scanned files compile
  1  one or more files failed to compile (truncation / syntax error)
"""
from __future__ import annotations

import py_compile
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCAN_ROOT = REPO_ROOT / "skills"


def iter_targets(argv):
    """Yield .py paths to check: explicit args if given, else the whole tree."""
    if argv:
        for a in argv:
            p = Path(a)
            if p.suffix == ".py" and p.exists():
                yield p
        return
    for p in SCAN_ROOT.rglob("*.py"):
        if "__pycache__" in p.parts:
            continue
        yield p


def main():
    targets = list(iter_targets(sys.argv[1:]))
    broken = []
    for p in targets:
        try:
            py_compile.compile(str(p), doraise=True)
        except py_compile.PyCompileError as e:
            broken.append((p, str(e).strip().splitlines()[-1]))
        except SyntaxError as e:
            broken.append((p, f"{type(e).__name__}: {e}"))

    print(f"Python integrity check -- {len(targets)} file(s) scanned under {SCAN_ROOT}")
    if not broken:
        print("PASS: every scanned Python file compiles.")
        return 0
    print(f"FAIL: {len(broken)} file(s) do NOT compile (truncated or corrupted):")
    for p, msg in broken:
        try:
            rel = p.relative_to(REPO_ROOT)
        except ValueError:
            rel = p
        print(f"  BROKEN  {rel}")
        print(f"          -> {msg}")
    print("")
    print("A non-compiling .py must never be committed/pushed -- fix or remove it.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
