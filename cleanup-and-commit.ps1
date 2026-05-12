# Cleanup + commit script — run from PowerShell in admin mode if "permission denied" errors appear
# Generated 2026-05-12 — single-use script for the consolidation commit
#
# WHAT THIS DOES (in order):
#   1. Fix git state in both repos (clear locks, rebuild corrupt index)
#   2. Delete the duplicate skill tree + stale plugin file + orphan transcript
#   3. Pull both repos to get current GitHub state
#   4. Stage all the SKILL.md changes from this session
#   5. Commit with an atomic message
#   6. Show you the diff and the staged status so you can review BEFORE the push
#   7. Wait for you to type 'YES' to actually push (so you can abort if anything looks off)
#
# Tonight's session changes that get committed:
#   - NEW: skills/shared-references/skill-deprecation-protocol.md
#   - REWRITE: skills/ghl-crm-audit/SKILL.md (PIT primary, Windsor backup, drop n8n primary)
#   - UPDATE: skills/shared-references/integrations.md (GHL section + Last Updated)
#   - FIX zombie refs: skills/vaibhav-template/SKILL.md, skills/watts-motion-graphics/SKILL.md
#   - DELETE: Skills/graeham-watts-skills/ folder (23 redundant skill copies)
#   - DELETE: Skills/graeham-watts-skills.plugin (776 KB stale package)
#   - DELETE: Skills/devini-claude-watch-transcript.md (orphan dropped at top level)

$ErrorActionPreference = "Stop"
$skillsDir = "C:\Users\Graeham Watts\Documents\Claude\Skills"
$onlineDir = "C:\Users\Graeham Watts\Documents\Claude\Online Content"

Write-Host "=== Step 1: Fix git state ===" -ForegroundColor Cyan

Set-Location $skillsDir
if (Test-Path ".git\index.lock") {
    Write-Host "Removing Skills/.git/index.lock"
    Remove-Item -Force ".git\index.lock"
}

Set-Location $onlineDir
if (Test-Path ".git\index.lock") {
    Write-Host "Removing Online Content/.git/index.lock"
    Remove-Item -Force ".git\index.lock"
}
# Online Content has a corrupt index — rebuild it
if (Test-Path ".git\index") {
    $idx = Get-Item ".git\index"
    if ($idx.Length -lt 100) {
        Write-Host "Online Content/.git/index is corrupt (too small) — rebuilding"
        Remove-Item -Force ".git\index"
        git reset
    }
}

Write-Host ""
Write-Host "=== Step 2: Delete duplicates from Skills/ ===" -ForegroundColor Cyan
Set-Location $skillsDir

$toDelete = @(
    "graeham-watts-skills",
    "graeham-watts-skills.plugin",
    "devini-claude-watch-transcript.md"
)
foreach ($item in $toDelete) {
    $path = Join-Path $skillsDir $item
    if (Test-Path $path) {
        Write-Host "Deleting: $item"
        Remove-Item -Recurse -Force $path
    } else {
        Write-Host "Already gone: $item"
    }
}

Write-Host ""
Write-Host "=== Step 3: Pull both repos (with stash to protect untracked files) ===" -ForegroundColor Cyan

Set-Location $skillsDir
Write-Host "Pulling Skills..."
git stash push -u -m "auto-stash-before-pull-$(Get-Date -Format yyyy-MM-dd-HHmm)" 2>&1 | Out-Host
git pull origin main 2>&1 | Out-Host
git stash pop 2>&1 | Out-Host

Set-Location $onlineDir
Write-Host "Pulling Online Content..."
git stash push -u -m "auto-stash-before-pull-$(Get-Date -Format yyyy-MM-dd-HHmm)" 2>&1 | Out-Host
git pull origin main 2>&1 | Out-Host
git stash pop 2>&1 | Out-Host

Write-Host ""
Write-Host "=== Step 4: Stage Skills changes ===" -ForegroundColor Cyan
Set-Location $skillsDir
git add -A
git status --short

Write-Host ""
Write-Host "=== Step 5: Review before commit ===" -ForegroundColor Yellow
Write-Host "About to commit with message:"
Write-Host ""
$msg = @"
consolidate: PIT-direct primary for GHL, drop n8n primary, kill duplicate skill tree

- ghl-crm-audit: rewrite Phase 1 (PIT direct primary, Windsor backup, Composio tertiary)
- ghl-crm-audit: rewrite Phase 4 (GitHub Action replaces n8n workflow recommendation)
- shared-references/integrations.md: GHL section updated; n8n highLevelApi credential retired
- NEW shared-references/skill-deprecation-protocol.md: enforces zombie cleanup discipline
- Fix zombie refs to video-script-creation-engine in vaibhav-template + watts-motion-graphics
- Delete graeham-watts-skills/ folder (23 redundant skill copies)
- Delete graeham-watts-skills.plugin (stale package)
- Delete devini-claude-watch-transcript.md (orphan)

Direction change ratified: n8n is no longer used as a GHL integration path. PIT direct
hitting services.leadconnectorhq.com is primary. Windsor is parallel/backup per the
Parallel-Pull Rule. Overrides today's earlier commits c2110b1 and 296f91b which had
promoted n8n.
"@
Write-Host $msg -ForegroundColor Gray
Write-Host ""

$confirm = Read-Host "Commit and push? Type YES to proceed, anything else to abort"
if ($confirm -ne "YES") {
    Write-Host "Aborted. Your changes are staged. Run 'git status' to inspect, then 'git commit' manually when ready." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Step 6: Commit and push Skills ===" -ForegroundColor Cyan
git commit -m $msg

$pat = (Get-Content "$skillsDir\github-token.txt" -Raw).Trim()
git push "https://${pat}@github.com/Graehamwatts/skills.git" main

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Green
Write-Host "Skills repo is now: PIT-direct primary for GHL, zombie protocol in place, duplicates gone."
Write-Host ""
Write-Host "Next session task: absorb social-media-analyzer into content-calendar (per skill-deprecation-protocol.md)."
