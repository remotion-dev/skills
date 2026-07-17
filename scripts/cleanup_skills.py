#!/usr/bin/env python3
"""cleanup_skills.py - Remove zombie skill files and patch wrong DRE values.

CANONICAL_DRE is the correct value. Edit this constant if it ever changes
(should also be reflected in skills/shared-references/identity.json).

Safe by default:
- Creates a timestamped backup of every file BEFORE deletion or modification
- Prompts for YES confirmation before any destructive operation
- Skips documentation-exempt files (CLAUDE.md, identity.json, this script's
  own definition list) so the policy warnings don't get neutered
"""
import argparse
import datetime
import re
import shutil
import sys
from pathlib import Path

# ---- Canonical values (mirror of identity.json) -----------------------------
CANONICAL_DRE = "01466876"   # The correct current DRE
BLOCKED_DRES = ["02015066"]  # Values to scrub out

# ---- Paths ------------------------------------------------------------------
SKILLS_ROOT = Path(r"C:\Users\Graeham Watts\Documents\Skills LLMS\Claude\Skills")
BACKUP_ROOT = SKILLS_ROOT / "_backup"

# Files that may legitimately reference blocked values (policy/enforcement)
DOC_EXEMPT = {
    "CLAUDE.md",
    "identity.json",
    "verify_brand_identity.py",
    "cleanup_skills.py",  # this script itself
}

# Zombie bundles to remove (outside the canonical Skills/ folder)
EXTERNAL_ZOMBIES = [
    Path(r"C:\Users\Graeham Watts\Documents\Skills LLMS\Claude\weekly-listing-update.skill"),
]


def find_dre_violations(root: Path):
    """Return list of (path, line_no, line) where a blocked DRE appears
    in a file that is NOT in the doc-exempt allowlist."""
    hits = []
    exts = {".md", ".txt", ".json", ".py", ".html", ".yml", ".yaml"}
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in exts:
            continue
        if any(seg in (".git", "_backup") for seg in p.parts):
            continue
        if p.name in DOC_EXEMPT:
            continue
        try:
            for i, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
                for bad in BLOCKED_DRES:
                    if bad in line:
                        hits.append((p, i, line.rstrip(), bad))
        except Exception as e:
            print(f"  WARN: could not read {p}: {e}", file=sys.stderr)
    return hits


def find_zombie_duplicates(root: Path):
    """Detect duplicate skill folders.

    A skill is identified by its folder name under skills/. A 'zombie'
    is a folder that matches a deprecation list OR another folder of the
    same canonical name.
    """
    skills_dir = root / "skills"
    if not skills_dir.exists():
        return []
    deprecated_names = {
        "video-script-creation-engine",
        "social-media-analyzer",
        "video-prompt-builder",
        "html-email",
        "github-skill-sync",
    }
    zombies = []
    for sub in skills_dir.iterdir():
        if sub.is_dir() and sub.name in deprecated_names:
            zombies.append(sub)
    return zombies


def backup_file(p: Path, ts: str):
    rel = p.relative_to(SKILLS_ROOT) if str(p).startswith(str(SKILLS_ROOT)) else Path(p.name)
    dest = BACKUP_ROOT / ts / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if p.is_dir():
        shutil.copytree(p, dest, dirs_exist_ok=True)
    else:
        shutil.copy2(p, dest)


def patch_dre(p: Path) -> int:
    """Replace any blocked DRE with the canonical one. Returns count of replacements."""
    txt = p.read_text(encoding="utf-8", errors="ignore")
    n = 0
    for bad in BLOCKED_DRES:
        if bad in txt:
            n += txt.count(bad)
            txt = txt.replace(bad, CANONICAL_DRE)
    if n:
        p.write_text(txt, encoding="utf-8")
    return n


def main():
    parser = argparse.ArgumentParser(description="Clean up zombie skills and patch DRE.")
    parser.add_argument("--yes", action="store_true",
                        help="Skip the YES prompt (only for automation)")
    args = parser.parse_args()

    print("=" * 70)
    print(f"SKILLS CLEANUP - {datetime.datetime.now().isoformat(timespec='seconds')}")
    print(f"Canonical DRE: {CANONICAL_DRE}")
    print(f"Blocked DRE(s): {', '.join(BLOCKED_DRES)}")
    print("=" * 70)

    if not SKILLS_ROOT.exists():
        print(f"ERROR: {SKILLS_ROOT} does not exist.", file=sys.stderr)
        sys.exit(1)

    # Stage 1: find DRE violations
    print("\n[1/3] Scanning for blocked DRE values in content files...")
    violations = find_dre_violations(SKILLS_ROOT)
    if violations:
        for p, ln, line, bad in violations:
            print(f"   {p.relative_to(SKILLS_ROOT)}:{ln}  ({bad})")
    else:
        print("   No violations.")

    # Stage 2: find zombie skill folders
    print("\n[2/3] Scanning for deprecated/duplicate skill folders...")
    zombies = find_zombie_duplicates(SKILLS_ROOT)
    if zombies:
        for z in zombies:
            print(f"   ZOMBIE: {z}")
    else:
        print("   None.")

    # Stage 3: external stray bundles
    print("\n[3/3] Checking for stray .skill bundles outside Skills/...")
    strays = [p for p in EXTERNAL_ZOMBIES if p.exists()]
    if strays:
        for s in strays:
            print(f"   STRAY: {s}")
    else:
        print("   None.")

    files_to_patch = sorted({v[0] for v in violations})
    if not files_to_patch and not zombies and not strays:
        print("\nNothing to do. Exiting clean.")
        return

    print("\n" + "=" * 70)
    print("PLANNED ACTIONS:")
    print(f"  - Patch DRE in {len(files_to_patch)} file(s)")
    print(f"  - Delete {len(zombies)} zombie skill folder(s)")
    print(f"  - Delete {len(strays)} stray .skill bundle(s)")
    print(f"  - Backup destination: {BACKUP_ROOT}")
    print("=" * 70)

    if not args.yes:
        ans = input("Type YES to proceed (anything else aborts): ").strip()
        if ans != "YES":
            print("Aborted.")
            return

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)

    # Backup + patch DRE files
    for p in files_to_patch:
        backup_file(p, ts)
        n = patch_dre(p)
        print(f"  patched ({n}x): {p.relative_to(SKILLS_ROOT)}")

    # Backup + remove zombies
    for z in zombies:
        backup_file(z, ts)
        shutil.rmtree(z)
        print(f"  removed: {z}")

    for s in strays:
        backup_file(s, ts)
        s.unlink()
        print(f"  removed: {s}")

    # Final manifest
    print("\n" + "=" * 70)
    print("SURVIVING SKILL MANIFEST")
    print("=" * 70)
    skills_dir = SKILLS_ROOT / "skills"
    for sub in sorted(skills_dir.iterdir()):
        if not sub.is_dir():
            continue
        sm = sub / "SKILL.md"
        if sm.exists():
            mtime = datetime.datetime.fromtimestamp(sm.stat().st_mtime).isoformat(timespec="seconds")
            print(f"  {sub.name:35s}  {mtime}  {sm}")
    print(f"\nBackup saved to: {BACKUP_ROOT / ts}")


if __name__ == "__main__":
    main()
