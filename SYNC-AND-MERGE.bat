@echo off
REM ============================================================
REM SYNC-AND-MERGE.bat v3 — handles corrupt git index
REM Generated 2026-05-13 via bash heredoc
REM
REM Current diagnosed state:
REM   - .git/index is corrupt ("bad signature 0x00000000")
REM   - Stale lock file: .git/index.stash.6.lock
REM   - Local missing 4 skills GitHub has
REM   - Local has 4 zombie folders (s-m-a, v-p-b, bofu-intent-scorer, bofu-query-generator)
REM   - ghl-pit.txt is MISSING — you need to recreate it manually after this runs
REM ============================================================

setlocal EnableDelayedExpansion
set "SKILLS=C:\Users\Graeham Watts\Documents\Claude\Skills"

echo.
echo === Step 1: Clean up all .git lock + corrupt index files ===
cd /d "%SKILLS%"
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\index.stash.6.lock" del /f /q ".git\index.stash.6.lock"
for %%f in (".git\*.lock") do (
    echo Removing stale lock: %%f
    del /f /q "%%f"
)
REM Force rebuild corrupt index
if exist ".git\index" (
    echo Deleting corrupt .git\index to force rebuild
    del /f /q ".git\index"
)
git reset 2>nul

echo.
echo === Step 2: Fetch GitHub HEAD ===
git fetch origin main
if errorlevel 1 (
    echo Fetch failed. Cannot continue without GitHub connection. Aborting.
    pause
    exit /b 1
)

echo.
echo === Step 3: Hard reset to GitHub HEAD (restores missing skills, wipes local-only state) ===
git reset --hard origin/main

echo.
echo === Step 4: Verify 4 missing skills are restored ===
set MISSING=0
for %%s in (pipeline-dashboard property-os-sync video-research-engine watts-motion-graphics) do (
    if exist "%SKILLS%\skills\%%s" (
        echo   RESTORED: %%s
    ) else (
        echo   STILL MISSING: %%s
        set /a MISSING+=1
    )
)
if !MISSING! gtr 0 (
    echo.
    echo %MISSING% skill(s) still missing after pull. Something's wrong with GitHub state.
    pause
    exit /b 1
)

echo.
echo === Step 5: Pause for Claude to redo the absorption work ===
echo.
echo *** STOP HERE — DO NOT CONTINUE PAST THIS POINT ON YOUR OWN ***
echo.
echo Tell Claude: "the sync ran successfully, local is at 47 skills"
echo Claude will then redo the absorption notes, the new phase reference files,
echo the skill-deprecation-protocol.md, and the integrations.md updates
echo IN THIS SESSION via bash heredoc (which persists to disk reliably).
echo.
echo After Claude finishes that prep, Claude will write a SECOND .bat file
echo called FINISH-MERGES.bat which you will run to delete zombies +
echo commit + push.
echo.
echo This two-script approach avoids the prior failure mode where the bat
echo tried to do everything in one shot and the sync wiped Claude's edits.
echo.
pause
