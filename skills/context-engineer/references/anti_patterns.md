# The Seven Context Anti-Patterns

Each anti-pattern has a diagnostic signature (how to spot it), a cost profile (why it hurts), and a fix.

## Table of contents
1. The Kitchen Sink
2. The Repeat Offender
3. The Stale Tool Result
4. The Silent Re-Read
5. The Verbose Example
6. The Unused Lookup Table
7. The Restatement of Defaults

---

## 1. The Kitchen Sink

**Signature:** one SKILL.md file that handles every domain, variant, and edge case. Often 800–2000 lines.

**Cost:** every invocation pays the full body tax, even for the 80% of runs that only need 20% of the content.

**Fix:** Split by variant/domain/phase into reference files (see `patterns.md`). Keep the shared workflow in SKILL.md. The body should shrink to the decision logic + the common path.

**Example:** a video-creator SKILL.md that inlines ffmpeg slideshow instructions AND Remotion project scaffolding AND HeyGen API docs. Split into three references.

---

## 2. The Repeat Offender

**Signature:** the same instruction written in multiple places. "Use TypeScript" appears in Step 2, Step 5, and the "important notes" section. Or the output format is spec'd three times for three different cases that could share one spec.

**Cost:** more tokens, and (worse) ambiguity — if the three statements drift apart over edits, the model has to guess which to follow.

**Fix:** pick one canonical spot. Link or reference from other spots.

**Example:** a SKILL.md that says "ALWAYS save output to /outputs" in four places. Pick the first, delete the rest.

---

## 3. The Stale Tool Result

**Signature:** a large tool result sitting in conversation history from 10 turns ago, no longer relevant. Common culprits: directory listings, grep results, web fetches, subagent reports.

**Cost:** persistent token cost that grows with every tool call. Especially painful in long sessions.

**Fix:** summarize the result after you've extracted what you need. In new turns, reference the summary instead of scrolling back to find the raw output.

**Example:** a `find /` that returned 40,000 characters of paths, of which the user only needed 3. Summarize as: "Found the following relevant files: [path1, path2, path3]. Full listing archived in prior turn if needed."

---

## 4. The Silent Re-Read

**Signature:** the same file Read multiple times across a session because Claude didn't track that it was already in context.

**Cost:** N copies of the file in history instead of 1. For large files, this is brutal.

**Fix:** Read once. For subsequent references, cite the file by path/line numbers rather than re-reading. If the file has been edited mid-session, re-read is appropriate; if not, it's waste.

**Example:** a 2,000-line source file Read 5 times in one debugging session. Fix: Read once up front, note the important functions and line numbers, reference those in subsequent turns.

---

## 5. The Verbose Example

**Signature:** a single example in SKILL.md that runs 100+ lines. Often 3–5 of them stacked.

**Cost:** examples are valuable (better than abstract instructions), but each example is paid for on every invocation, not just when relevant.

**Fix:** keep 1 canonical example inline. Move the rest to `references/examples.md` with a short index. The SKILL.md body says "For more examples covering X, Y, Z, read references/examples.md."

**Example:** a copywriting skill with full before/after rewrites for 6 formats inline. Keep one format's example inline; move the other 5 to references.

---

## 6. The Unused Lookup Table

**Signature:** a long reference table (prices, codes, flags, character limits) that the skill rarely consults, but it's sitting at the top of SKILL.md.

**Cost:** the table is paid for every invocation; the value is returned only on invocations where the skill actually needs to look something up.

**Fix:** move the table to a reference file. The SKILL.md body says "For the full character limit table across all ad formats, read references/format_specs.md."

**Example:** a 40-line table of Google Ads character limits. If it's checked 1 run in 5, move it.

---

## 7. The Restatement of Defaults

**Signature:** the skill (or the user) restates things Claude already does by default. "Always be helpful." "Respond in Markdown." "Use clear language." "Ask clarifying questions when unsure."

**Cost:** tokens that convey zero new information.

**Fix:** delete. Trust the defaults. Only write down the things that deviate from default behavior or specify the domain-specific move.

**Example:** a SKILL.md that opens with 15 lines of "You are a helpful AI assistant. You should be clear and concise..." Delete it all. The model already knows.

---

## Diagnostic workflow

When auditing a context / skill for anti-patterns:

1. **Scan for repeated phrases.** If "ALWAYS" appears more than 3 times, there's probably a Repeat Offender.
2. **Count lines per conceptual block.** Anything over 200 lines on a single concept is Kitchen Sink territory.
3. **Grep for example blocks.** If there's more example text than instruction text, you probably have Verbose Examples.
4. **Look for tables.** Tables over 20 rows used less than every run = Unused Lookup Tables.
5. **Look at the top 10 lines.** Is any of it restatement of default AI behavior? That's Restatement of Defaults.
6. **For live sessions:** check the last 10 tool results. Any of them over 5KB? Candidate for Stale Tool Result once they've been consumed.
7. **For live sessions:** grep the Read calls. Same path twice? Silent Re-Read.

---

## What's actually worth optimizing

Not every anti-pattern is worth fixing. Optimize where the cost is significant:

- **A 5KB unused table in a skill used 10x/day** → fix it. 50KB/day of waste.
- **A 500-byte repeated instruction in a skill used once a month** → leave it. The juice isn't worth the squeeze.
- **A 40KB stale tool result in a 200k context** → summarize. Big, idle, easy.
- **A 2KB example repeated in a skill used 1000x/day** → cut one copy. Measurable impact.

Context engineering has diminishing returns. Fix the big offenders first, and don't spend an hour saving 200 tokens on something rarely used.
