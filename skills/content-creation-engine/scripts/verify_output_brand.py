#!/usr/bin/env python3
"""Pre-publish brand validation for generated content outputs.

Scans output files (HTML, md, txt) for:
  1. Blocked values from shared-references/identity.json (e.g. the banned DRE) — FAIL.
  2. Client-facing HTML missing the correct DRE entirely — WARN (contact block may be absent).
  3. Stale prior-year references in titles/headers (e.g. "2025 Market Update" written in 2026) — WARN.
  4. Empty / suspiciously tiny files — FAIL (truncated-output guard; corrupted snapshots
     have shipped to clients before).

Usage:
    python verify_output_brand.py <file-or-dir> [more paths...]

Exit codes: 0 = pass, 1 = warnings only, 2 = hard failures. Never prints secrets.
"""
import json, os, re, sys
from datetime import datetime

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDENTITY = os.path.join(SKILL_DIR, "..", "shared-references", "identity.json")
SCAN_EXT = {".html", ".htm", ".md", ".txt", ".json"}
MIN_BYTES = 200


def load_identity():
    with open(IDENTITY, encoding="utf-8") as f:
        ident = json.load(f)
    blocked = []
    def harvest(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if "block" in k.lower():
                    harvest(v)
                elif isinstance(v, (dict, list)):
                    harvest(v)
        elif isinstance(node, list):
            for v in node:
                harvest(v)
        elif isinstance(node, str) and re.fullmatch(r"\d{8}", node):
            blocked.append(node)
    harvest(ident)
    correct_dre = None
    text = json.dumps(ident)
    m = re.search(r"01466876", text)
    if m:
        correct_dre = "01466876"
    return sorted(set(blocked)), correct_dre


def files_under(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
        else:
            for root, _, names in os.walk(p):
                for n in names:
                    if os.path.splitext(n)[1].lower() in SCAN_EXT:
                        yield os.path.join(root, n)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    blocked, correct_dre = load_identity()
    year = datetime.now().year
    stale_years = [str(y) for y in range(year - 2, year)]
    fails, warns, scanned = [], [], 0

    for fp in files_under(sys.argv[1:]):
        scanned += 1
        try:
            raw = open(fp, "rb").read()
        except OSError as e:
            fails.append(f"{fp}: unreadable ({e})")
            continue
        if len(raw) < MIN_BYTES:
            fails.append(f"{fp}: only {len(raw)} bytes — empty or truncated output")
            continue
        text = raw.decode("utf-8", errors="replace")
        for b in blocked:
            if b in text:
                fails.append(f"{fp}: contains BLOCKED value {b}")
        if fp.lower().endswith((".html", ".htm")) and correct_dre and correct_dre not in text:
            warns.append(f"{fp}: client-facing HTML has no DRE {correct_dre} — contact block missing?")
        # stale year in headline-ish content (title tags / h1 / first markdown heading)
        head_zone = text[:4000]
        for sy in stale_years:
            if re.search(rf"<title>[^<]*\b{sy}\b|<h1[^>]*>[^<]*\b{sy}\b|^#\s.*\b{sy}\b", head_zone, re.M | re.I):
                warns.append(f"{fp}: headline references {sy} — confirm intentional (current year {year})")

    print(f"Scanned {scanned} file(s). Failures: {len(fails)} · Warnings: {len(warns)}")
    for f_ in fails:
        print(f"FAIL: {f_}")
    for w in warns:
        print(f"WARN: {w}")
    if fails:
        sys.exit(2)
    sys.exit(1 if warns else 0)


if __name__ == "__main__":
    main()
