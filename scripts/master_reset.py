#!/usr/bin/env python3
"""master_reset.py - One-command orchestrator.

Runs in sequence:
  1. cleanup_skills.py  (gated by YES confirmation unless --yes passed)
  2. sync_skills.py
  3. claude_with_cache.py prewarm  (writes Skills bundle into Anthropic's
     server-side cache so the first real user request hits cache)

Final report prints zombie removals, sync counts, and estimated token
savings per session.
"""
import argparse
import datetime
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(cmd):
    print(f"\n>>> {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=str(HERE))
    return r.returncode


def estimate_token_savings():
    """Rough estimate of cached tokens. Counts ~chars/4 across all SKILL.md."""
    skills_dir = HERE.parent / "skills"
    total_chars = 0
    n = 0
    if skills_dir.exists():
        for sub in skills_dir.iterdir():
            sm = sub / "SKILL.md"
            if sm.exists():
                try:
                    total_chars += len(sm.read_text(encoding="utf-8"))
                    n += 1
                except Exception:
                    pass
    tokens = total_chars // 4
    return n, tokens


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--yes", action="store_true",
                    help="Skip cleanup confirmation prompt")
    ap.add_argument("--skip-cleanup", action="store_true")
    ap.add_argument("--skip-sync", action="store_true")
    ap.add_argument("--skip-prewarm", action="store_true")
    args = ap.parse_args()

    print("=" * 70)
    print(f"MASTER RESET - {datetime.datetime.now().isoformat(timespec='seconds')}")
    print("=" * 70)

    zombie_removals = 0
    sync_summary = "skipped"

    if not args.skip_cleanup:
        cleanup_cmd = [sys.executable, "cleanup_skills.py"]
        if args.yes:
            cleanup_cmd.append("--yes")
        rc = run(cleanup_cmd)
        if rc != 0:
            print("Cleanup aborted - stopping.")
            sys.exit(rc)
        # Count what got moved into _backup as a proxy for zombie removals
        backup_root = HERE.parent / "_backup"
        if backup_root.exists():
            latest = sorted(backup_root.iterdir())
            if latest:
                zombie_removals = sum(1 for _ in latest[-1].rglob("*") if _.is_file())

    if not args.skip_sync:
        rc = run([sys.executable, "sync_skills.py"])
        sync_summary = "ran (see sync_log.txt)" if rc == 0 else f"errors (rc={rc})"

    if not args.skip_prewarm:
        rc = run([sys.executable, "claude_with_cache.py", "prewarm"])
        if rc != 0:
            print("Pre-warm failed (likely missing ANTHROPIC_API_KEY).")

    n_skills, est_tokens = estimate_token_savings()

    print("\n" + "=" * 70)
    print("MASTER RESET COMPLETE")
    print("=" * 70)
    print(f"  Files moved to _backup (proxy for zombies removed): {zombie_removals}")
    print(f"  Sync step: {sync_summary}")
    print(f"  Skills bundled into cache: {n_skills}")
    print(f"  Estimated cached tokens per session: ~{est_tokens:,}")
    print(f"  Estimated savings: cache reads cost ~10% of base "
          f"input tokens, so each cached session saves roughly "
          f"~{int(est_tokens * 0.9):,} billable input tokens.")
    print("=" * 70)


if __name__ == "__main__":
    main()
