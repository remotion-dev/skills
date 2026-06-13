---
name: cowork-task-shutoff
description: >
  Disable the Cowork-side copies of Graeham's recurring scheduled tasks so they don't double-fire
  alongside the live copies now running in Claude Code (migrated 2026-06-09). Use ANY time Graeham
  says: turn off the Cowork tasks, disable the duplicate scheduled tasks, stop the double emails,
  Cowork is firing tasks twice, shut off Cowork automations, kill the Cowork-side schedules, or
  "make sure the Cowork tasks are off and the Claude Code ones are on." RUN THIS INSIDE COWORK —
  it disables Cowork's own scheduled tasks and verifies the result. Report-only safe: it never
  deletes a task, only toggles it off, and it lists exactly what it changed.
---

# Cowork Scheduled-Task Shut-Off

**Purpose:** Graeham's 18 recurring tasks were migrated into **Claude Code's** scheduler on 2026-06-09
and are the live, authoritative copies. Cowork still holds duplicate copies of the same tasks. If both
are enabled, every task **fires twice** — double emails to John/Peter/Maria/Adrian, double postcard
previews, double newsletter sends, double git pushes. This skill disables the Cowork copies and confirms
the Claude Code copies stay on.

> **Run this skill inside Cowork.** Claude Code cannot read or toggle Cowork's task state from disk
> (Cowork stores schedules server-side). Only a Cowork session can enumerate and disable them.

---

## The kill list — disable these 18 in Cowork

These are the tasks that now live in Claude Code. Find each one in Cowork's task/automation list and
**toggle it OFF** (disable — do NOT delete). Match on name/intent; schedules are listed to help you
identify the right one.

| # | Task | Cowork schedule to match |
|---|------|--------------------------|
| 1 | property-os-daily-backup | Daily ~11:09 PM — Obsidian vault → property-os repo |
| 2 | coaching-transcript-phase2 | Daily 6 AM — coaching transcripts → Obsidian |
| 3 | monday-crm-intelligence-report | Mondays 7 AM — GHL CRM report to Graeham + Maria |
| 4 | weekly-blog-topics-eric-peter | Mondays 7 AM — 21 topics + 3 dashboards + email |
| 5 | switchy-monday-dashboard | Mondays 8 AM — Switchy clicks dashboard |
| 6 | weekly-social-media-report | Mondays 9 AM — V8 social dashboard + email |
| 7 | weekly-content-email-monday | Mondays 11 AM — v5.4 content calendar + email |
| 8 | monday-weekly-seller-updates | Mondays 12:30 PM — seller-update upload reminder |
| 9 | pcfs-cma-autobuild-weekly | Mondays 10 AM — past-client CMA value updates |
| 10 | weekly-peter-newsletter-content-reminder | Wednesdays 8 AM — EPA Report video content reminder |
| 11 | monthly-newsletter-monday | 1st Monday 7 AM — monthly Bay Area Real Estate Brief |
| 12 | quarterly-skills-audit | Quarterly (1st Feb/May/Aug/Nov) 9 AM — zombie-skill audit |
| 13 | friday-attribution-review | Fridays 4 PM — GHL attribution dashboard + email |
| 14 | farming-postcard-1st-preview | 24th of month 8 AM — 1st-of-month postcard hooks |
| 15 | farming-postcard-15th-preview | 8th of month 8 AM — 15th-of-month postcard hooks |
| 16 | weekly-signal-sweep | Mondays 6 AM — pre-collect IG/news/MLS signal |
| 17 | bilt-cash-mortgage-redeem | 1st of month 9 AM — Bilt Cash → PNC mortgage reminder |
| 18 | weekly-content-email-monday twin / any other recurring Cowork task that matches a Claude Code task name above |

> If you find a recurring Cowork task whose name/intent matches one of the 18 above, it's a duplicate —
> disable it. If you find a recurring Cowork task that is **not** on this list, **do not touch it** —
> flag it to Graeham instead (it may be something he set up separately).

## DO NOT touch these

- **daily-attribution-brief** — deliberately NOT migrated to Claude Code. It self-runs as a GitHub
  Actions cron on the online-content repo. Leave it exactly as-is in every system.
- **n8n workflows** (finance/bank pulls, content webhooks, PCFS temp workflows) — these are not Cowork
  scheduled tasks; they live in n8n. Out of scope. Do not disable.

---

## Procedure (run in Cowork)

1. **Enumerate** Cowork's scheduled/recurring tasks (open the Cowork tasks/automations panel, or use
   whatever task-list capability this Cowork session exposes). Capture each task's name and on/off state.
2. **For each of the 18 kill-list tasks found enabled:** toggle it **OFF** (disable). Never delete.
3. **Record the outcome per task** in one of four buckets:
   - `disabled` — was on, now off (this is the win)
   - `already-off` — was already disabled, no action
   - `not-found` — no Cowork copy exists (fine — means it was never duplicated)
   - `left-on (NOT on kill list)` — a recurring task you found that isn't a known duplicate → flag, don't disable
4. **Cross-check the Claude Code side stays ON.** The live copies must remain enabled or the task stops
   running entirely. As of **2026-06-12**, a Claude Code session verified all 18 were `enabled: true`.
   In Claude Code, the truth source is `list_scheduled_tasks` (all 18 should read `enabled: true`).
   You cannot toggle Claude Code's scheduler from Cowork — only confirm via the Claude Code app sidebar.

## Final report (always print this)

Print a table: **Task | Cowork result | Claude Code (expected ON)**. Then a one-line summary:

> "Disabled N Cowork duplicates, M were already off, K had no Cowork copy. Claude Code copies remain the
> live schedulers (expected all 18 ON — verify in the Claude Code sidebar). No tasks were deleted."

If you disabled anything, remind Graeham: it may take a moment for Cowork's server to reflect the change;
re-open the panel to confirm each toggle stuck.

## Safety rules

- **Disable, never delete.** A toggle is reversible; a delete loses the task definition.
- **One scheduler per task.** The goal state is: Cowork = OFF, Claude Code = ON, for all 18.
- **Never disable a Claude Code task** to "fix" a double-fire — that would stop the task completely.
  The duplicate to kill is always the Cowork one.
- If unsure whether a Cowork task is a duplicate, **leave it on and ask Graeham**.
