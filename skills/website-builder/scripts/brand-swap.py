#!/usr/bin/env python3
"""
Brand swap — replace placeholder CSS variables across all HTML/CSS files
in a project folder with the values from a brand config.

Usage:
    python3 brand-swap.py <project-dir> --brand <brand-name>
    python3 brand-swap.py ./propiq-ui --brand realtor

Brands are defined in BRANDS below. Add more as new brands are locked.

What it does:
- Walks <project-dir> for .html/.css files.
- For each file, replaces the :root {...} block's brand section with the
  selected brand's colors (and fonts, if specified).
- Leaves status colors, neutrals, and radii alone — those don't change per brand.

What it does NOT do:
- Replace inline `color: #ABC123` values. You're supposed to be using var(--brand-primary).
  If the swap doesn't fully take effect, that means someone hardcoded colors —
  run with --audit to surface those files.
"""

from __future__ import annotations
import argparse, re, sys
from pathlib import Path

BRANDS = {
    "realtor": {
        "--brand-primary":        "#C5A55A",
        "--brand-primary-hover":  "#A88B3D",
        "--brand-primary-light":  "#F5EFDC",
        "--brand-accent":         "#1A1A1A",
        "--font-display":         '"Eagle CG Bold", "Anton", serif',
        "--font-body":            '"SF Pro Display", -apple-system, BlinkMacSystemFont, sans-serif',
    },
    "propiq-placeholder": {
        "--brand-primary":        "#1a2744",
        "--brand-primary-hover":  "#111d33",
        "--brand-primary-light":  "#e8ecf5",
        "--brand-accent":         "#2d4278",
        "--font-display":         '"Playfair Display", Georgia, serif',
        "--font-body":            '"Epilogue", system-ui, sans-serif',
    },
    # Add more brands here once Graeham locks them.
}

# Hex-color pattern for the --audit mode
HEX_RE = re.compile(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")
# Matches CSS var declarations like:   --brand-primary: #C5A55A;
DECL_RE = re.compile(r"(--[\w-]+)\s*:\s*([^;]+);")


def swap_file(path: Path, brand: dict[str, str]) -> tuple[int, list[str]]:
    """Returns (replacements_made, list_of_keys_touched)."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return 0, []

    touched: list[str] = []
    def replace(m):
        key = m.group(1).strip()
        if key in brand:
            touched.append(key)
            return f"{key}: {brand[key]};"
        return m.group(0)

    new_text = DECL_RE.sub(replace, text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return len(touched), touched


def audit_file(path: Path) -> list[str]:
    """Return a list of 'line N: <snippet>' for every hardcoded hex color
    that's not inside a --var declaration. These are refactor candidates."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    findings = []
    for i, line in enumerate(text.splitlines(), 1):
        # Skip lines that are declaring CSS variables
        if re.search(r"--[\w-]+\s*:", line):
            continue
        if HEX_RE.search(line):
            findings.append(f"  line {i}: {line.strip()[:120]}")
    return findings


def main():
    ap = argparse.ArgumentParser(description="Swap brand tokens across a project.")
    ap.add_argument("project_dir", help="Path to project root (will be walked)")
    ap.add_argument("--brand", choices=list(BRANDS.keys()), help="Brand name to apply")
    ap.add_argument("--audit", action="store_true",
                    help="Don't swap — list files with hardcoded hex colors")
    ap.add_argument("--dry-run", action="store_true",
                    help="Report changes but don't write files")
    args = ap.parse_args()

    root = Path(args.project_dir).resolve()
    if not root.exists():
        sys.exit(f"Project dir not found: {root}")

    files = [p for p in root.rglob("*") if p.suffix in (".html", ".css", ".scss")]
    if not files:
        print("No HTML/CSS files found.")
        return

    if args.audit:
        total = 0
        for f in files:
            findings = audit_file(f)
            if findings:
                total += len(findings)
                print(f"\n{f.relative_to(root)}")
                for line in findings[:20]:
                    print(line)
                if len(findings) > 20:
                    print(f"  ... and {len(findings) - 20} more")
        print(f"\n{total} hardcoded hex color(s) found across {len(files)} files.")
        print("Refactor these to use var(--brand-primary) etc. for clean swaps.")
        return

    if not args.brand:
        sys.exit("--brand required unless --audit is set")

    brand = BRANDS[args.brand]
    changed = 0
    for f in files:
        if args.dry_run:
            text = f.read_text(encoding="utf-8", errors="ignore")
            matches = DECL_RE.findall(text)
            hits = [k for k, _ in matches if k in brand]
            if hits:
                changed += 1
                print(f"[dry-run] would update {f.relative_to(root)}  ({len(hits)} vars)")
        else:
            n, touched = swap_file(f, brand)
            if n:
                changed += 1
                print(f"updated {f.relative_to(root)}  ({n} vars: {', '.join(sorted(set(touched)))})")

    print(f"\nDone. {changed}/{len(files)} files {'would be' if args.dry_run else ''} modified. Brand: {args.brand}")


if __name__ == "__main__":
    main()
