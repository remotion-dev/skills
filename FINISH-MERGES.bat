@echo off
REM ============================================================
REM FINISH-MERGES.bat — Step 2 of 2 (run after SYNC-AND-MERGE.bat completed)
REM Generated 2026-05-13 via bash heredoc
REM
REM Prerequisites (already done by you in this session):
REM   - Local at GitHub HEAD 3fba2b2 (47 skills, all zombies present)
REM   - Absorption notes added to cinematic-hooks, content-creation-engine
REM   - Tripwire added to skill-creator
REM   - integrations.md updated
REM
REM This script:
REM   1. PRESERVES SKILL.md content from soon-to-be-deleted skills into
REM      content-creation-engine/references/phases/
REM   2. PRESERVES video-research-engine scripts into
REM      content-creation-engine/scripts/video-research/
REM   3. Deletes the 4 zombie folders
REM   4. Creates 4 atomic commits per protocol
REM   5. Pushes
REM ============================================================

setlocal EnableDelayedExpansion
set "SKILLS=C:\Users\Graeham Watts\Documents\Claude\Skills"
set "CCE=%SKILLS%\skills\content-creation-engine"
set "PHASES=%CCE%\references\phases"

echo.
echo === Step 1: Ensure phases and scripts directories exist ===
cd /d "%SKILLS%"
if not exist "%PHASES%" mkdir "%PHASES%"
if not exist "%CCE%\scripts\video-research" mkdir "%CCE%\scripts\video-research"

echo.
echo === Step 2: Preserve content before deletion ===

echo -- Copying bofu-intent-scorer SKILL.md to references/phases/
if exist "%SKILLS%\skills\bofu-intent-scorer\SKILL.md" (
    copy /Y "%SKILLS%\skills\bofu-intent-scorer\SKILL.md" "%PHASES%\bofu-intent-scorer.md"
)

echo -- Copying bofu-query-generator SKILL.md to references/phases/
if exist "%SKILLS%\skills\bofu-query-generator\SKILL.md" (
    copy /Y "%SKILLS%\skills\bofu-query-generator\SKILL.md" "%PHASES%\bofu-query-generator.md"
)

echo -- Copying video-research-engine SKILL.md + scripts
if exist "%SKILLS%\skills\video-research-engine\SKILL.md" (
    copy /Y "%SKILLS%\skills\video-research-engine\SKILL.md" "%PHASES%\video-research.md"
)
if exist "%SKILLS%\skills\video-research-engine\scripts" (
    xcopy /E /I /Y "%SKILLS%\skills\video-research-engine\scripts\*" "%CCE%\scripts\video-research\"
)
if exist "%SKILLS%\skills\video-research-engine\references" (
    if not exist "%CCE%\references\video-research" mkdir "%CCE%\references\video-research"
    xcopy /E /I /Y "%SKILLS%\skills\video-research-engine\references\*" "%CCE%\references\video-research\"
)
if exist "%SKILLS%\skills\video-research-engine\templates" (
    if not exist "%CCE%\templates\video-research" mkdir "%CCE%\templates\video-research"
    xcopy /E /I /Y "%SKILLS%\skills\video-research-engine\templates\*" "%CCE%\templates\video-research\"
)

echo.
echo === Step 3: Delete the 4 zombie folders ===
rmdir /s /q "%SKILLS%\skills\social-media-analyzer" 2>nul
rmdir /s /q "%SKILLS%\skills\video-prompt-builder" 2>nul
rmdir /s /q "%SKILLS%\skills\bofu-intent-scorer" 2>nul
rmdir /s /q "%SKILLS%\skills\bofu-query-generator" 2>nul
rmdir /s /q "%SKILLS%\skills\video-research-engine" 2>nul

echo.
echo === Step 4: Atomic commits (protocol Rule 2) ===

git add -A
git commit -m "consolidate: absorb video-prompt-builder into cinematic-hooks (deletes skills/video-prompt-builder/)"

git add -A
git commit -m "consolidate: absorb bofu-intent-scorer and bofu-query-generator into content-creation-engine (deletes both source folders, content preserved in references/phases/)"

git add -A
git commit -m "consolidate: absorb video-research-engine into content-creation-engine (deletes skills/video-research-engine/, scripts/templates/references preserved)"

git add -A
git commit -m "audit: remove social-media-analyzer local zombie + skill-creator tripwire + integrations.md updates"

echo.
echo === Step 5: Push to GitHub ===
for /f "delims=" %%i in (github-token.txt) do set PAT=%%i
git push https://!PAT!@github.com/Graehamwatts/skills.git main

echo.
echo === Step 6: Verification ===
echo Local skill folders:
dir /b /ad "%SKILLS%\skills" 2>nul | find /c ""
echo Expected: 43

echo.
echo Cross-reference scan (should show only absorption notes):
git grep -l "skills/video-prompt-builder" 2>nul
git grep -l "skills/bofu-intent-scorer" 2>nul
git grep -l "skills/bofu-query-generator" 2>nul
git grep -l "skills/video-research-engine" 2>nul
git grep -l "skills/social-media-analyzer" 2>nul

echo.
echo === DONE ===
echo Local + GitHub are now in sync at 43 skills.
echo This script is NOT self-deleting. Delete manually when satisfied.
echo.
pause
