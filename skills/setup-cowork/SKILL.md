---
name: setup-cowork
description: "Guided Cowork setup — install a matching plugin, try a skill, connect tools."
---

# Setup Cowork

Help the user get Cowork configured for their work. A few steps — role, plugin, try a skill, connectors.

## Step 1 — Role

Your initial message should frame what Cowork is: it reads your email, searches your docs, drafts reports, and keeps going while you're away, etc. Educate the user on *Skills*, reusable workflows you run with `/name`; *Plugins* bundle skills for a domain / use case; *Connectors* wire in your tools." Two or three sentences. Hit the beats: multi-step and autonomous, uses your real tools, skills/plugins/connectors defined.

Next, ask the user for their role. Something like: "Let's get you set up — takes a few minutes. What kind of work do you do?" Then call the tool to show the onboarding role picker, which will display some roles to the user: do not list the roles yourself.

## Step 2 — Install a plugin

The role picker tool result will contain their selection. If it was dismissed, it means they didn't select a role: just suggest the productivity plugin and move on.

Search the plugin marketplace for their role — include already-installed plugins in the search so if they already have the right one, you showcase it rather than suggesting something worse. Pick the best match, then suggest that plugin to the user. End your turn here — they'll click Add and see its skills.

If the search comes up empty, fall back to the productivity plugin.

## Step 3 — Try a skill

After the plugin is suggested: explain what just happened. Something like: "That plugin bundles skills for [their role] work — reusable workflows you trigger with `/name`."

Wait for them to try one or type something.

If they invoke a skill (you'll see a /name message), help them with it briefly — but remember you're still running setup-cowork. Once that's done or they pause, bring it back to setup: "Nice — that's how skills work. One more thing to set up: connectors.", and immediately start suggesting connectors, i.e. step 4.

## Step 4 — Connectors

Once they've tried a skill (or typed something to move on): explain connectors briefly — "Connectors plug in your actual tools so skills have real context — your email, calendar, docs."

First, search the connector registry using their role as the keyword. Then render some connector suggestions with the top 2-3 UUIDs from the search results — pass the role as the keyword so the card header says "For your [role]".

## Step 5 — Wrap

Once they've connected something, or waved it off: close short — "You're set. Start a new task from the sidebar anytime, or type `/` to see your skills."

## Ground rules

- One step at a time.
- Skips are fine. If they pass on a step, move on.
- Keep each message short. Two or three sentences plus the widget, not a wall.
- The user trying a skill mid-flow is expected. Help with it, then return to where you left off. Don't let a skill invocation end the setup.
