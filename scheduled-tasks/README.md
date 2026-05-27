# Scheduled Tasks

This folder holds the canonical, version-controlled copy of Cowork scheduled-task SKILL.md files. Cowork itself reads them from `~/Documents/Claude/Scheduled/<task-name>/SKILL.md` on each machine, so when one of these files changes here in the repo, the next step is to copy it onto each machine that runs the task.

## Sync onto the Mac Studio

```bash
cd ~/Documents/Claude/Skills
git pull origin main
# Copy any updated scheduled task SKILL.md files into Cowork's scheduled folder
rsync -a scheduled-tasks/ ~/Documents/Claude/Scheduled/
```

That `rsync -a` copies the contents of `scheduled-tasks/<task-name>/SKILL.md` into `~/Documents/Claude/Scheduled/<task-name>/SKILL.md` while preserving the folder structure. Run it any time after pulling.

## Tasks tracked here

| Task | Cadence | What it does |
|---|---|---|
| pcfs-cma-autobuild-weekly | Mon 9:21am PT | Builds past-client CMA value-update reports for clients due in next 7 days; sends review emails to Graeham + Adrian (changed from drafts → sends 2026-05-26) |
