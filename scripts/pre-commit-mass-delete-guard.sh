#!/bin/sh
# Mass-deletion guard — pre-commit hook for the skills repo.
#
# Why: on 2026-06-09 an automated "Auto-sync: session-end" commit deleted 64
# files (10 entire skills + shared-references/identity.json) because the
# Documents working copy was stale relative to a sandbox-clone push. This hook
# blocks any commit that stages a suspicious number of deletions so that an
# auto-sync against a stale tree fails loudly instead of silently wiping work.
#
# Install (already done on Graeham's machine, repeat after a fresh clone):
#   cp scripts/pre-commit-mass-delete-guard.sh .git/hooks/pre-commit
#
# To intentionally delete many files in one commit, run with the override:
#   ALLOW_MASS_DELETE=1 git commit -m "..."

LIMIT=5

if [ "$ALLOW_MASS_DELETE" = "1" ]; then
    exit 0
fi

deletions=$(git diff --cached --diff-filter=D --name-only | wc -l | tr -d ' ')

if [ "$deletions" -gt "$LIMIT" ]; then
    echo "BLOCKED: this commit deletes $deletions files (limit $LIMIT)." >&2
    echo "If the working copy is stale (sandbox push not pulled yet), run:" >&2
    echo "    git pull origin main" >&2
    echo "and re-check. To force a genuine mass deletion:" >&2
    echo "    ALLOW_MASS_DELETE=1 git commit ..." >&2
    git diff --cached --diff-filter=D --name-only | head -10 >&2
    exit 1
fi

# Never allow deleting the brand source of truth, even under the limit.
if git diff --cached --diff-filter=D --name-only | grep -q "shared-references/identity.json"; then
    echo "BLOCKED: commit deletes skills/shared-references/identity.json (brand source of truth)." >&2
    echo "Use ALLOW_MASS_DELETE=1 only if this is truly intentional." >&2
    exit 1
fi

exit 0
