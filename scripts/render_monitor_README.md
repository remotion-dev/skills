# Render Monitor — Setup Guide

One-time Windows setup for the `render_monitor.py` script that polls HeyGen,
downloads completed-video metadata, and publishes `render_status.json` so the
dashboards can show ▶ Watch Video buttons automatically.

## Why this exists
When you click **Copy Render Command** on a dashboard, paste into PowerShell,
and hit Enter, the video queues at HeyGen. The monitor script is what closes
the loop — it checks HeyGen every few minutes, grabs the finished MP4 URL +
thumbnail when ready, and pushes that state to GitHub so the dashboards light
up with an embedded player. No refresh by hand required beyond reloading the
page.

## Prereqs (already in place)
- `HEYGEN_API_KEY` env var set on Windows (user-scope)
- Local clone of `Graehamwatts/skills` somewhere on disk (default: `C:\Users\<user>\skills`)
- `git` on PATH
- Python 3.10+

## First run
```powershell
cd C:\Users\<user>\skills
git pull
python scripts\render_monitor.py
```

Expected output:
```
[HH:MM:SS] Checked 1 in-flight videos. 0 newly completed.
[HH:MM:SS] Wrote C:\Users\<user>\heygen_renders\render_status.json
[HH:MM:SS] Pushed render_status.json to GitHub.
```

Then open any dashboard (e.g. the EPA Two Years one). The panel for your
submitted format now shows a yellow "Rendering..." card. Once HeyGen finishes
(2–15 min), re-run the monitor and the card flips green with a playable
preview.

## Auto-poll every 2 minutes (recommended)
Create a Windows scheduled task so you never need to run this manually.

1. Open **Task Scheduler** → Create Task…
2. **General tab:**
   - Name: `HeyGen Render Monitor`
   - Run whether user is logged on or not: unchecked (leave checked for
     simpler setup — just lets it run when you're at the machine)
3. **Triggers tab:** New…
   - Begin the task: On a schedule
   - Daily, recur every 1 day
   - **Advanced:** repeat task every 2 minutes, for a duration of 1 day
4. **Actions tab:** New…
   - Action: Start a program
   - Program/script: `python`
   - Arguments: `C:\Users\<user>\skills\scripts\render_monitor.py`
   - Start in: `C:\Users\<user>\skills`
5. **Conditions tab:** uncheck "Start the task only if the computer is on AC
   power" if you work from a laptop.
6. Save.

Alternative (simpler): just run `python scripts\render_monitor.py --watch 120`
in a PowerShell window any time you're waiting for a render. It'll poll every
2 minutes and exit once everything reaches a terminal state.

## What the dashboards show
Each video format panel (YT Long Pt 1, YT Short, IG Reel 1, IG Reel 2, TikTok)
gets a status card auto-injected at the top when its render is tracked:

- 🟡 **Rendering** — HeyGen still working. Refresh the page in a few minutes.
- ✅ **Video Ready** — MP4 embedded with player + Download button + link to
  HeyGen dashboard.
- 🔴 **Render Failed** — error message + video_id. Tell Graeham.

## Peter's usage
Peter does not run this script. He just opens the dashboard and waits for the
green card to appear before posting a video format. The "For Peter" block at
the top of each dashboard covers his full workflow.

## Troubleshooting

| Problem | Fix |
|---|---|
| `HEYGEN_API_KEY env var is not set` | Set it: `[Environment]::SetEnvironmentVariable("HEYGEN_API_KEY", "sk_V2_...", "User")` then restart PowerShell |
| `Repo path not found` | Clone Graehamwatts/skills to `C:\Users\<user>\skills` OR set `SKILLS_REPO_PATH` env var OR pass `--repo-path` |
| `git push failed` | Check your GitHub credential helper is configured for the repo |
| Dashboard card never appears | Hard-refresh the dashboard (Ctrl+Shift+R). The JS cache-busts every minute, so any polling from the last 60s is stale. |
| Status card appears but video doesn't play | Check the MP4 URL in DevTools Network tab. HeyGen URLs can expire; re-run the monitor to refresh the URL. |
