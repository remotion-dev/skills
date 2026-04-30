#!/usr/bin/env python3
"""
verify_brand_identity.py — Brand identity tripwire.

Reads skills/shared-references/identity.json (the single source of truth)
and audits the entire repo. Fails (exit 1) if any blocked value appears
anywhere outside the identity file itself.

Run before every push:
    python3 scripts/verify_brand_identity.py

Or wire into a git pre-push hook for automatic enforcement:
    cp scripts/verify_brand_identity.py .git/hooks/pre-push
    chmod +x .git/hooks/pre-push

Why this exists:
    Prior to April 24 2026, brand identity (DRE number especially) was
    duplicated across 70+ files. Each "scrub" had to find and fix every
    instance — miss one and the wrong DRE leaked into outputs. Five
    consecutive scrubs failed to fully eliminate the wrong DRE because
    there was no enforcement layer.

    This script IS the enforcement layer. It runs in seconds and grep-fails
    the entire repo against the blocklist. Future regressions get caught
    at push time instead of at user-discovery time.
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    identity_path = repo_root / "skills" / "shared-references" / "identity.json"

    if not identity_path.exists():
        print(f"FAIL: identity source-of-truth not found at {identity_path}")
        return 2

    with open(identity_path) as f:
        identity = json.load(f)

    blocked = identity.get("_blocked_values", {})
    blocklist = blocked.get("dre_blocklist", [])
    correct_dre = identity["identity"]["dre"]

    print(f"Brand identity tripwire — checking {len(blocklist)} blocked values")
    print(f"  Source of truth: {identity_path.relative_to(repo_root)}")
    print(f"  Correct DRE: {correct_dre}")
    print(f"  Blocklist: {blocklist}")
    print()

    failures = []

    for blocked_value in blocklist:
        result = subprocess.run(
            ["grep", "-rln", blocked_value, "--exclude-dir=.git", "."],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        # Allow blocked values to appear in documentation files that
        # legitimately need to reference them (e.g. CLAUDE.md warns about
        # the blocked DRE so future sessions know not to add it).
        exempt = set(blocked.get("_documentation_exempt", ["skills/shared-references/identity.json"]))
        hits = []
        for line in result.stdout.strip().splitlines():
            if not line:
                continue
            # Strip leading ./ from grep output and check against exemption set
            normalized = line.lstrip("./")
            if normalized in exempt:
                continue
            if line.endswith("identity.json"):  # legacy fallback
                continue
            hits.append(line)
        if hits:
            failures.append((blocked_value, hits))

    if not failures:
        print("PASS: zero blocked values found in repo.")
        print(f"      Repo is clean against the {len(blocklist)}-item blocklist.")
        return 0

    print("FAIL: blocked values found:")
    for blocked_value, hits in failures:
        print(f"\n  {blocked_value!r} appears in {len(hits)} file(s):")
        for hit in hits:
            print(f"    - {hit}")

    print()
    print("Fix: replace each instance with the correct DRE from identity.json,")
    print("     or update identity.json's blocklist if a value is no longer blocked.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
