# Skill Deprecation Protocol

> **Authority:** This document is binding. Any session that merges, absorbs, deprecates, or replaces a skill MUST follow this protocol. Skill-creator's tripwire enforces it.

> **Why this exists:** Past sessions have repeatedly consolidated skills (e.g., `video-script-creation-engine` absorbed into `content-creation-engine` April 2026, `social-media-analyzer` absorbed into `content-calendar` May 2026) but failed to **delete the source folders, scrub cross-references, or update the canonical integration docs**. The result: zombie skills lingering with trigger-word overlap that pollute Claude's skill-matching and cause contradictory instructions to fire. This protocol makes the cleanup non-optional.

---

## The Six Rules

### Rule 1 — One concept = one skill

If two skills have trigger-word overlap >30%, they must merge. No exceptions for "but they're slightly different." Slightly different always rots into "completely contradictory" within 90 days.

### Rule 2 — Deletion is part of the merge, same commit

When skill A is absorbed into skill B:

- `git rm -r skills/A/` lives in the **same commit** as the B changes.
- Not a follow-up commit. Not a TODO. Same commit, or the merge is rejected.

A merge commit message must be of the form: `consolidate: absorb A into B (deletes skills/A/)`.

### Rule 3 — Cross-reference scan before commit

Before the commit lands, run:

```bash
grep -rln "skills/A\b\|name: A\b\|use \`A\`\|run A\|invoke A" skills/ 2>/dev/null
```

Result MUST be empty (zero hits) or only inside B's own SKILL.md (as part of the "what was absorbed" note). If grep returns hits elsewhere, those must be updated to point to B before the commit lands.

### Rule 4 — Absorption note at the top of the receiver

B's SKILL.md must include, near the top:

```markdown
> **Absorbed on YYYY-MM-DD:** `A` was merged into this skill. All capabilities of `A` (list: …) now live here. The folder `skills/A/` was deleted in the same commit. If you find any reference to `skills/A/` anywhere in this repo, that reference is a bug — it should point here.
```

This is the audit trail. Future sessions reading B's SKILL.md will see the history.

### Rule 5 — Canonical integration doc gets updated

If A had its own integrations / data sources / cron schedules, `shared-references/integrations.md` and any other shared-references docs that mentioned A must be updated to point to B in the same commit. Per-skill integration map at the bottom of `integrations.md` must reflect the new ownership.

### Rule 6 — Quarterly audit task (and on-demand)

A scheduled task `skills-audit` (Quarterly or on-demand) runs the **Zombie Detector** checklist below. Anything it finds gets fixed before the next skill-related commit.

---

## The Deletion Checklist (used during every merge)

Run through this checklist top-to-bottom for every consolidation. None of these steps are optional.

1. [ ] Confirm the merge target B exists and covers 100% of A's capabilities (no gaps).
2. [ ] Add the absorption note to the top of B's SKILL.md (Rule 4).
3. [ ] Run cross-reference scan (Rule 3). Update every hit to point to B.
4. [ ] Update `shared-references/integrations.md` "Per-Skill Integration Map" — replace A with B.
5. [ ] Update `shared-references/integrations.md` any narrative section mentioning A.
6. [ ] Update `shared-references/data-contracts.md` if A had its own data contracts.
7. [ ] Update `shared-references/branding.md` if A had its own visual references.
8. [ ] Update `CLAUDE.md` at the workspace root if A appeared in the folder layout.
9. [ ] `git rm -r skills/A/` (force delete the folder; do not leave a "deprecated" stub).
10. [ ] `grep -rln "skills/A\b\|name: A\b" .` returns no results outside B's absorption note.
11. [ ] Commit with message `consolidate: absorb A into B (deletes skills/A/)`.
12. [ ] Push immediately. Do not let the change sit local-only — that's how the duplicate `graeham-watts-skills/` folder happened.

---

## The Zombie Detector (the quarterly audit)

Run this checklist quarterly OR immediately after any consolidation OR before any "I think we have replacements for X" question comes up.

### Detection 1 — Duplicate folder trees

```bash
# A skill folder that exists in two locations is a zombie.
find C:\Users\Graeham\ Watts\Documents\Claude\Skills -maxdepth 3 -type d -name "skills"
# Should return exactly one path. If more, the extras are zombies.
```

### Detection 2 — Orphaned references

```bash
# For every skill folder that exists, check that something else in the repo references it.
# If a skill has zero inbound references AND zero scheduled-task references, it's possibly orphaned.
for skill in skills/*/; do
  name=$(basename "$skill")
  count=$(grep -rln --include="SKILL.md" --include="*.md" "$name" . | grep -v "$skill" | wc -l)
  if [ "$count" -eq 0 ]; then echo "ORPHAN: $name (zero inbound refs)"; fi
done
```

### Detection 3 — Trigger-word collisions

```bash
# For every skill's description, count which other skills have any of its trigger phrases.
# Overlap >30% = candidate for merge.
# (script in scripts/trigger-collision-check.py — to be added)
```

### Detection 4 — Local-vs-GitHub diff

```bash
# Local folder list vs GitHub remote folder list. Any local-only folder is unpushed; any
# GitHub-only folder is a deletion that didn't get applied locally.
diff <(ls -1 skills/) <(curl -s -H "Authorization: Bearer $PAT" \
  https://api.github.com/repos/Graehamwatts/skills/contents/skills \
  | python3 -c "import json,sys;[print(d['name']) for d in json.load(sys.stdin) if d.get('type')=='dir']" \
  | sort)
```

### Detection 5 — Backup / .old / draft files

```bash
find skills/ -type f \( -name "*.bak" -o -name "*.old" -o -name "*-old.md" -o -name "*-draft.md" \) 2>/dev/null
```

### Detection 6 — Stale "see X instead" / "deprecated" / "moved to" notes

```bash
grep -rln --include="SKILL.md" -i "deprecated\|superseded\|see .* instead\|moved to\|legacy skill\|do not use" skills/
```

Any hits should EITHER (a) be the absorption note from Rule 4 referencing an already-deleted folder, OR (b) be removed because the referenced skill no longer exists.

---

## Examples — Correct vs Wrong

### CORRECT merge (the way `video-script-creation-engine` SHOULD have been done)

```
Commit: consolidate: absorb video-script-creation-engine into content-creation-engine (deletes skills/video-script-creation-engine/)

Changes:
  + skills/content-creation-engine/SKILL.md — added absorption note + integrated capabilities
  - skills/video-script-creation-engine/  ← DELETED ENTIRELY
  ~ skills/heygen-video/SKILL.md — updated reference
  ~ skills/heygen-elevenlabs-renderer/SKILL.md — updated reference
  ~ skills/content-calendar/SKILL.md — updated reference
  ~ skills/github-skill-sync/SKILL.md — updated reference
  ~ shared-references/integrations.md — updated per-skill map
```

### WRONG merge (the way it actually got done — the bug this protocol fixes)

```
Commit: content-creation-engine: absorb video-script logic

Changes:
  ~ skills/content-creation-engine/SKILL.md
  (note: skills/video-script-creation-engine/ still exists, will clean up later)
```

"Clean up later" never happens. The folder lingers, gets matched by Claude's skill triggers, and we end up here.

---

## Specific Cases That Caused This Document to Exist

### Case 1 — `video-script-creation-engine` (April 2026)

Absorbed into `content-creation-engine` but the folder was never deleted. Lingered as a zombie. Required this protocol to resolve. (Resolution: tonight's audit.)

### Case 2 — `social-media-analyzer` (completed May 12, 2026)

Absorbed into `content-calendar`. Protocol followed in full. The folder `skills/social-media-analyzer/` was deleted in the same commit as the calendar update. All cross-references updated. Absorption note added to content-calendar's SKILL.md per Rule 4.

### Case 3 — `graeham-watts-skills/` duplicate folder (May 2026)

Not a skill consolidation but a duplicate-tree zombie. Created when an old skill-package staging folder wasn't cleaned up. Triggered identical confusion. Solution: same — delete the duplicate, document the decision, never let it come back.

### Case 4 — Today's contradictory commits (May 12, 2026)

Earlier-in-day commits promoted `n8n + HighLevel credential` as primary path for GHL. Later-in-day decision: PIT direct is primary, Windsor parallel, n8n removed entirely. The earlier commits became zombie instructions. Solution: this protocol's overwrite-and-delete pattern, not "leave both around."

---

## skill-creator Integration

The `skill-creator` skill (which Claude uses when asked to merge or consolidate skills) MUST read this document before any merge operation. Specifically:

- Add a step to skill-creator's SKILL.md: "If the user asks to merge / absorb / consolidate / replace skill A with skill B: read `shared-references/skill-deprecation-protocol.md` first and follow the Deletion Checklist top-to-bottom."
- skill-creator must refuse to write the merge if it can't execute Rule 2 (same-commit deletion) — instead, surface the obstacle to the user.

---

## Last Updated

May 12, 2026 — initial creation following the n8n/PIT direction-reversal incident and the discovery of the `graeham-watts-skills/` duplicate tree.
