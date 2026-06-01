# Distribution — who gets what, and how

After the Call Sheet is built, each person gets the piece they need, and Graeham + the editor get the full master. This is the last step of every run.

## What gets rendered

Render the visual HTML dashboard (`assets/call-sheet-template.html`) three ways:

| File | Contents | Goes to |
|---|---|---|
| **MASTER** | The full dashboard — all four packets (plan, videographer, agent, editor) | Graeham + the editor |
| **VIDEOGRAPHER copy** | Plan header + packet ② (the shot list, glossary, bank shots) | The videographer |
| **EDITOR copy** | Plan header + the full script (③) + packet ④ (assembly map) | The editor (in addition to the master) |

The agent (Graeham) reads his script straight from the master, so there's no separate "agent-only" file — he gets the master.

Save all three to the outputs folder and present them to Graeham first. Hosting the master on GitHub Pages (the `online-content` repo, per the repo CLAUDE.md) is optional but nice — it gives a clickable link to drop in the emails instead of a giant inline body.

## How the emails go out — DRAFTS, not auto-send (be honest about this)

The Gmail connector available here (`mcp__…__create_draft`) **creates drafts only — it cannot auto-send, and cannot attach files yet.** That is both the real capability limit and the safer pattern (it matches `weekly-listing-update`, which drafts for Graeham's review). So the flow is:

1. Build the HTML for each recipient's piece.
2. Create one Gmail **draft per recipient** with that HTML as the `htmlBody` (inline — no attachments supported). If the master is hosted, include its link near the top of the body.
3. Tell Graeham the drafts are sitting in Gmail for his review, and he hits **Send** on each (or says "send them" and — when a send capability exists — they go). **Never imply the skill blind-sends.**

### Recipient matrix (create one draft each)

| Draft → | Subject | Body (htmlBody) |
|---|---|---|
| **Videographer** (e.g. Wesley) | `Shoot brief — <address> — <shoot date>` | the VIDEOGRAPHER copy + (optional) master link |
| **Editor** | `Edit sheet — <address>` | the EDITOR copy + (optional) master link |
| **Graeham** (master, for his records/approval) | `Call sheet (master) — <address>` | the MASTER |

**Dedupe:** if the videographer and editor are the same person (often true — e.g. Wesley does both), create **one** draft to that person containing the videographer copy + the editor copy + the master link, not three separate emails.

**Addresses:** use the emails Graeham supplied for the videographer/editor; his own is `graehamwatts@gmail.com`. The `create_draft` tool needs plain addresses (`name@example.com`), not "Name <…>" format.

## Order of operations

1. Build + save the master and per-role HTML.
2. Present the master to Graeham (he eyeballs it).
3. Create the Gmail drafts per the matrix above.
4. Report: "Drafts are in your Gmail — [recipient/subject for each]. Review and send when you're happy." List exactly which drafts you created.

If Graeham hasn't given recipient emails, build + present the HTML and ask for the addresses before drafting — don't guess an email.
