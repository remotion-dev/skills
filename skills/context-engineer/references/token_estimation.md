# Token Estimation — Without Running a Tokenizer

You usually won't have a live tokenizer in the loop, but you can estimate token counts within ±15% using simple heuristics. Good enough for diagnostics.

## The rules of thumb

### Prose (English)
- **1 token ≈ 4 characters** (including spaces and punctuation)
- **1 token ≈ 0.75 words**
- A typical paragraph (80 words) ≈ 100–110 tokens
- A page of prose (~500 words) ≈ 650–700 tokens
- Typical chat message (200 words) ≈ 250–270 tokens

### Code
Code tokenizes differently — more symbols, shorter identifiers, more punctuation.
- **Python / JavaScript / TypeScript:** ~2 characters per token (half of prose)
- A 100-line Python file (~2,500 chars) ≈ 1,200–1,400 tokens
- A 1,000-line codebase file ≈ 12,000–15,000 tokens

### JSON and structured data
Punctuation heavy; lots of repeated keys.
- **~3 characters per token**
- A 10 KB JSON blob ≈ 3,000–3,500 tokens
- A typical MCP tool result (list of records) is surprisingly expensive — a 100-record list with 10 fields each can run 8,000+ tokens

### Markdown
Close to prose, slightly higher due to syntax.
- **~3.5 characters per token**
- A 500-line SKILL.md (assume 50 chars/line average) ≈ 7,000 tokens

### URLs and paths
Very dense.
- **~2 characters per token**
- A long URL with query strings can be 30–50 tokens on its own

### Non-English languages
Much higher token-per-character ratios.
- Japanese / Chinese / Korean: 1 token ≈ 1 character
- Many European languages: slightly higher than English (accented chars, compound words)

## Estimating from disk

For a file on disk, the quick formula:

```
estimated_tokens = file_size_in_bytes / cpb
```

where `cpb` (characters per byte) is:
- Prose: 4
- Code: 2
- JSON/YAML: 3
- Markdown: 3.5

In bash:
```bash
# Quick token estimate for a file
wc -c path/to/file | awk '{print "~"int($1/4)" tokens (prose)"; print "~"int($1/2)" tokens (code)"}'
```

## Estimating a conversation

For a whole conversation including system prompt and history, sum these:

1. **System prompt** — if you can see its length in characters, divide by 4
2. **Each user message** — count roughly 100 tokens per short message, 500 per long one
3. **Each assistant message** — same math, but assistant messages tend to be longer
4. **Tool results** — treat as JSON (÷3) if structured, prose (÷4) if text
5. **Loaded files** — see "from disk" above

Double your estimate if the system prompt looks unusually large (includes many tool definitions, user preferences, skill index). Modern Claude agent system prompts run 5–20k tokens before you add anything.

## What token counts look like in practice

For reference, these are typical sizes for common things:

| Thing | Tokens |
|---|---|
| Short chat message ("what's the weather?") | 10–15 |
| Typical user request (3–4 sentences) | 50–100 |
| Long user message (1 paragraph of context) | 200–400 |
| Claude's typical response (1–2 paragraphs) | 200–500 |
| A SKILL.md frontmatter (name + description) | 100–300 |
| A SKILL.md body (500 lines, markdown) | 6,000–8,000 |
| A reference file (300 lines) | 3,500–5,000 |
| A bash `ls -la ~` output | 500–2,000 |
| A bash `find /` output | can be 50,000+ |
| A web fetch of a standard page | 3,000–15,000 |
| A PDF extracted to text (10 pages) | 3,000–5,000 |
| A 50KB JSON blob | 15,000–18,000 |

## The "should I summarize?" threshold

Rule of thumb: if an item takes more than **5% of your remaining context budget** to keep around, and it's not actively being referenced, summarize it.

Example: 200k window, you're at 150k used, remaining = 50k. 5% of 50k = 2,500 tokens. Anything over ~10KB of content sitting idle should be summarized or dropped.

## Caveats

These are estimates, not ground truth. Actual tokenization varies:
- Anthropic's tokenizer treats some English words as single tokens while splitting others
- Emoji and special characters can each be multiple tokens
- Code with lots of identifiers in one style (camelCase vs snake_case) tokenizes differently

For diagnostics, estimates are plenty. If you need exactness, run the text through a tokenizer (e.g., `tiktoken` for OpenAI models, Anthropic's SDK tokenizer for Claude).
