---
name: schedule
description: "Create a scheduled task that can be run on demand or automatically on an interval."
---

You are creating a reusable shortcut from the current session. Follow these steps:

## 1. Analyze the session

Review the session history to identify the core task the user performed or requested. Distill it into a single, repeatable objective.

## 2. Draft a prompt

The prompt will be used for future autonomous runs — it must be entirely self-contained. Future runs will NOT have access to this session, so never reference "the current conversation," "the above," or any ephemeral context.

Include in the description:
- A clear objective statement (what to accomplish)
- Specific steps to execute
- Any relevant file paths, URLs, repositories, or tool names
- Expected output or success criteria
- Any constraints or preferences the user expressed

Write the description in second-person imperative ("Check the inbox…", "Run the test suite…"). Keep it concise but complete enough that another Claude session could execute it cold.

## 3. Choose a taskName

Pick a short, descriptive name in kebab-case (e.g. "daily-inbox-summary", "weekly-dep-audit", "format-pr-description").

## 4. Determine scheduling

Pick one:
- **Recurring** ("every morning", "weekdays at 5pm", "hourly") → `cronExpression`
- **One-time with a specific moment** ("remind me in 5 minutes", "tomorrow at 3pm", "next Friday") → `fireAt` ISO timestamp
- **Ad-hoc** (no automatic run; user will trigger manually) → omit both
- **Ambiguous** → propose a schedule and ask the user to confirm before proceeding

**cronExpression:** Evaluated in the user's LOCAL timezone, not UTC. Use local times directly — e.g. "8am every Friday" → `0 8 * * 5`.

**fireAt:** Compute the exact moment and emit a full ISO 8601 string with timezone offset, e.g. `2026-03-05T14:30:00-08:00`. Never use cron for one-time tasks — cron has no one-shot semantics.

Finally, call the "create_scheduled_task" tool.