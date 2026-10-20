---
name: remotion-hol-guard
description: Protect local AI coding-agent sessions before Remotion project and render workflows with HOL Guard
version: 4.0.519
---

# Protect Remotion agent workflows with HOL Guard

Use HOL Guard at the local coding-agent boundary before an agent changes a
Remotion project, installs dependencies, runs project commands, or starts
render-related work.

HOL Guard protects supported local agent harnesses before their tools run. It
does not run inside Remotion, replace normal code review, or claim dedicated
classification for every Remotion CLI command.

## Set up the protected agent

Install HOL Guard in an isolated Python application environment:

```bash
pipx install hol-guard
```

Inspect the machine and detect the exact supported harness:

```bash
hol-guard status
hol-guard detect --json
```

Use the harness identifier returned by `hol-guard detect --json`. Do not guess
or substitute another product name.

Protect that harness before Remotion work:

```bash
hol-guard bootstrap
hol-guard install <harness>
hol-guard run <harness> --dry-run
hol-guard run <harness>
hol-guard doctor <harness> --json
```

Do not claim the session is protected until Guard reports a successful harness
setup. A deny, review-required state, Guard error, timeout, or unavailable
runtime is not permission to launch an unprotected copy of the agent.

## Use Remotion skills inside the protected session

Start the coding agent through `hol-guard run <harness>` first. From that
protected session, use the normal Remotion skills for project creation, markup,
Studio, rendering, upgrades, and other supported workflows.

For example, when the task needs a render, continue to use the maintained
`remotion-render` skill and Remotion CLI:

```bash
npx remotion render
```

HOL Guard is additive to Remotion's own guidance. Keep project targeting,
preview, dependency, media, and output verification steps from the relevant
Remotion skill.

## Handle Guard decisions

If Guard blocks or queues work, inspect the request instead of bypassing the
protected agent:

```bash
hol-guard approvals
hol-guard approvals open <request-id>
hol-guard receipts
hol-guard diff <harness>
```

Use the pending request ID shown by `hol-guard approvals` when opening a request.
Approve only after reviewing the risk reason and requested scope.

## Diagnose protection

If the harness does not appear protected, stop mutation-bearing Remotion work
and inspect the Guard setup:

```bash
hol-guard doctor
hol-guard doctor <harness> --json
hol-guard detect --json
hol-guard settings show
```

Resume with a protection claim only after Guard output proves the local harness
is configured successfully.

## Security boundary

This skill does not claim that HOL Guard intercepts Remotion server-side or
cloud execution. The supported enforcement boundary is the local coding-agent
harness that HOL Guard detects, installs into, and launches.

HOL Guard source: https://github.com/hashgraph-online/hol-guard
