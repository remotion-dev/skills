@echo off
REM ============================================================
REM FINAL-COMMIT.bat — finishes what FINISH-MERGES.bat couldn't
REM Generated 2026-05-13 — fixes git identity + force-deletes zombies
REM
REM Prerequisites:
REM   - git config --global user.email/user.name must be set
REM   - SYNC-AND-MERGE.bat already ran (local at GitHub HEAD)
REM   - FINISH-MERGES.bat ran content preservation but failed on commits
REM ============================================================

setlocal EnableDelayedExpansion
set "SKILLS=C:\Users\Graeham Watts\Documents\Claude\Skills"

echo.
echo === Step 1: Verify git identity is set ===
cd /d "%SKILLS%"
for /f "delims=" %%i in ('git config user.email 2^>nul') do set GIT_EMAIL=%%i
if "!GIT_EMAIL!"=="" (
    echo ERROR: git user.email not set. Run these first:
    echo   git config --global user.email "graehamwatts@gmail.com"
    echo   git config --global user.name "Graeham Watts"
    pause
    exit /b 1
)
echo Git identity: !GIT_EMAIL!

echo.
echo === Step 2: Force-delete zombie folders ===
rmdir /s /q "%SKILLS%\skills\social-media-analyzer" 2>nul
rmdir /s /q "%SKILLS%\skills\video-prompt-builder" 2>nul
rmdir /s /q "%SKILLS%\skills\bofu-intent-scorer" 2>nul
rmdir /s /q "%SKILLS%\skills\bofu-query-generator" 2>nul
rmdir /s /q "%SKILLS%\skills\video-research-engine" 2>nul

REM Verify
for %%z in (social-media-analyzer video-prompt-builder bofu-intent-scorer bofu-query-generator video-research-engine) do (
    if exist "%SKILLS%\skills\%%z" (
        echo WARNING: skills\%%z still exists — may be locked by another process
    ) else (
        echo Deleted: skills\%%z
    )
)

echo.
echo === Step 3: Also clean up the test artifacts ===
del /f /q "%SKILLS%\test-persist.txt" 2>nul

echo.
echo === Step 4: Stage everything ===
git add -A
echo --- git status ---
git status --short

echo.
echo === Step 5: Single atomic commit (combining all 4 merges) ===
git commit -m "consolidate: absorb 4 skills into parents per skill-deprecation-protocol" -m "" -m "Merge 1: cinematic-hooks absorbs video-prompt-builder" -m "Merge 2: content-creation-engine absorbs bofu-intent-scorer + bofu-query-generator (content preserved in references/phases/)" -m "Merge 3: content-creation-engine absorbs video-research-engine (content in references/phases/video-research.md, scripts in scripts/video-research/, references in references/video-research/, templates in templates/video-research/)" -m "Audit: remove social-media-analyzer local zombie, add skill-creator tripwire, update integrations.md per-skill map"

echo.
echo === Step 6: Push ===
for /f "delims=" %%i in (github-token.txt) do set PAT=%%i
git push https://!PAT!@github.com/Graehamwatts/skills.git main

echo.
echo === Step 7: Verify final state ===
echo Local skill count:
dir /b /ad "%SKILLS%\skills" | find /c ""
echo (Expected: 43)

echo.
echo Final cross-reference scan:
git grep -l "skills/video-prompt-builder\|skills/bofu-intent-scorer\|skills/bofu-query-generator\|skills/video-research-engine\|skills/social-media-analyzer" 2>nul
echo (Should only show absorption notes + protocol doc — intentional audit trail)

echo.
echo === DONE ===
pause
