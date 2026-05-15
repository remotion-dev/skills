#!/usr/bin/env python3
"""sync_skills.py - Sync local skills to the Anthropic Console + git push.

Behavior:
  1. Iterate every SKILL.md under Skills/skills/<name>/ on the canonical disk
  2. Upload or update the matching skill via the Anthropic Skills API
  3. git add + commit + push the whole Skills repo
  4. Log every action with a timestamp to sync_log.txt
  5. Print a final summary

Auth:
  - ANTHROPIC_API_KEY must be set in the environment
  - For git push, the PAT lives at Skills/github-token.txt (gitignored)

Note: The Anthropic Skills Console API surface may evolve. This script uses
the /v1/skills HTTP endpoints (PATCH/POST/GET). If your account uses a
different surface, swap the SKILLS_LIST / SKILLS_UPSERT helpers.
"""
import datetime
import os
import subprocess
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: install requests first: pip install requests", file=sys.stderr)
    sys.exit(1)

SKILLS_ROOT = Path(r"C:\Users\Graeham Watts\Documents\Claude\Skills")
SKILLS_DIR = SKILLS_ROOT / "skills"
LOG_PATH = SKILLS_ROOT / "scripts" / "sync_log.txt"
GIT_TOKEN_FILE = SKILLS_ROOT / "github-token.txt"
GIT_REMOTE = "https://github.com/Graehamwatts/skills.git"

ANTHROPIC_BASE = "https://api.anthropic.com"
ANTHROPIC_VERSION = "2023-06-01"


def log(msg: str):
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def api_headers():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        log("FATAL: ANTHROPIC_API_KEY not set")
        sys.exit(2)
    return {
        "x-api-key": key,
        "anthropic-version": ANTHROPIC_VERSION,
        "content-type": "application/json",
    }


def list_console_skills():
    r = requests.get(f"{ANTHROPIC_BASE}/v1/skills", headers=api_headers(), timeout=30)
    if r.status_code == 404:
        log("Skills API returned 404 - Skills surface may not be enabled on this account.")
        return {}
    r.raise_for_status()
    data = r.json()
    by_name = {}
    for s in data.get("data", data.get("skills", [])):
        name = s.get("name") or s.get("display_name")
        if name:
            by_name[name] = s
    return by_name


def upsert_skill(name: str, content: str, existing_id: str | None):
    payload = {"name": name, "display_name": name, "instructions": content}
    if existing_id:
        url = f"{ANTHROPIC_BASE}/v1/skills/{existing_id}"
        r = requests.patch(url, headers=api_headers(), json=payload, timeout=60)
        return "updated", r
    url = f"{ANTHROPIC_BASE}/v1/skills"
    r = requests.post(url, headers=api_headers(), json=payload, timeout=60)
    return "created", r


def read_skill_files():
    out = []
    for sub in sorted(SKILLS_DIR.iterdir()) if SKILLS_DIR.exists() else []:
        if not sub.is_dir():
            continue
        sm = sub / "SKILL.md"
        if sm.exists():
            try:
                out.append((sub.name, sm, sm.read_text(encoding="utf-8")))
            except Exception as e:
                log(f"WARN cannot read {sm}: {e}")
    return out


def git_commit_and_push(changed_names):
    try:
        if not GIT_TOKEN_FILE.exists():
            log("WARN: github-token.txt not found - skipping git push")
            return False
        pat = GIT_TOKEN_FILE.read_text(encoding="utf-8").strip()
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"skill-sync: {ts} {' '.join(changed_names) if changed_names else '(no content changes)'}"

        cwd = str(SKILLS_ROOT)
        subprocess.run(["git", "add", "-A"], cwd=cwd, check=True)
        diff = subprocess.run(["git", "diff", "--cached", "--name-only"],
                              cwd=cwd, capture_output=True, text=True)
        if not diff.stdout.strip():
            log("git: no changes to commit")
            return True
        subprocess.run(["git", "commit", "-m", msg], cwd=cwd, check=True)
        push_url = f"https://{pat}@github.com/Graehamwatts/skills.git"
        subprocess.run(["git", "push", push_url, "HEAD:main"], cwd=cwd, check=True)
        log(f"git: pushed - {msg}")
        return True
    except Exception as e:
        log(f"git error: {e}")
        return False


def main():
    log("==== sync_skills.py start ====")
    local = read_skill_files()
    log(f"local skills found: {len(local)}")

    if not local:
        log("Nothing to sync.")
        return

    try:
        console = list_console_skills()
        log(f"console skills found: {len(console)}")
    except Exception as e:
        log(f"could not list console skills: {e} - aborting console sync")
        console = None

    synced = created = updated = errors = 0
    changed_names = []

    if console is not None:
        for name, path, content in local:
            existing = console.get(name)
            existing_id = existing.get("id") if existing else None
            try:
                action, resp = upsert_skill(name, content, existing_id)
                if resp.status_code >= 400:
                    log(f"  ERROR {name}: {resp.status_code} {resp.text[:200]}")
                    errors += 1
                    continue
                synced += 1
                changed_names.append(name)
                if action == "created":
                    created += 1
                else:
                    updated += 1
                log(f"  {action}: {name}")
            except Exception as e:
                log(f"  EXCEPTION {name}: {e}")
                errors += 1
    else:
        log("Skipping console upload step (API not reachable).")

    git_commit_and_push(changed_names)

    log("==== summary ====")
    log(f"  synced : {synced}")
    log(f"  created: {created}")
    log(f"  updated: {updated}")
    log(f"  errors : {errors}")
    log("==== sync_skills.py end ====")


if __name__ == "__main__":
    main()
