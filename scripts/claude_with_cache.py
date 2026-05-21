#!/usr/bin/env python3
"""claude_with_cache.py - Single entry point for Claude API calls with
server-side prompt caching of the Skills bundle.

Behavior:
  - On init, reads every SKILL.md from Skills/skills/<name>/ and joins them
    into system prompt blocks (one block per skill).
  - Marks the LAST block with cache_control: {"type": "ephemeral"} so
    Anthropic caches the whole skills bundle as one entry.
  - Exposes send_message(user_input, model=DEFAULT_MODEL).
  - Logs CACHE WRITE on first call, CACHE HIT on subsequent calls within
    5 minutes (driven by the response's cache_read_input_tokens vs.
    cache_creation_input_tokens fields).

Usage:
    from claude_with_cache import send_message
    text = send_message("Hello, give me a 1-line market summary.")
"""
import datetime
import json
import os
import sys
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("ERROR: pip install anthropic", file=sys.stderr)
    sys.exit(1)

SKILLS_DIR = Path(r"C:\Users\Graeham Watts\Documents\Claude\Skills\skills")
DEFAULT_MODEL = "claude-sonnet-4-6"

_CLIENT = None
_SYSTEM_BLOCKS = None


def _load_skill_blocks():
    """Build a list of system blocks, one per skill, plus a small header
    block. The last block gets cache_control."""
    blocks = []
    header = (
        "You have access to Graeham Watts's skill toolkit. Each block below "
        "is one skill's SKILL.md. The blocks are immutable - they describe "
        "tools available to you. Read identity.json (referenced inside the "
        "skills) for canonical brand details (name, DRE, etc.) - never type "
        "those values from memory."
    )
    blocks.append({"type": "text", "text": header})

    if not SKILLS_DIR.exists():
        return blocks

    for sub in sorted(SKILLS_DIR.iterdir()):
        if not sub.is_dir():
            continue
        sm = sub / "SKILL.md"
        if not sm.exists():
            continue
        try:
            content = sm.read_text(encoding="utf-8")
            blocks.append({"type": "text", "text": f"### Skill: {sub.name}\n\n{content}"})
        except Exception as e:
            print(f"WARN: could not read {sm}: {e}", file=sys.stderr)

    # Mark the LAST block with ephemeral cache_control so the whole prefix
    # is cached as a single cache entry on Anthropic's side.
    if blocks:
        blocks[-1]["cache_control"] = {"type": "ephemeral"}
    return blocks


def _client():
    global _CLIENT
    if _CLIENT is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set")
        _CLIENT = anthropic.Anthropic(api_key=api_key)
    return _CLIENT


def _system():
    global _SYSTEM_BLOCKS
    if _SYSTEM_BLOCKS is None:
        _SYSTEM_BLOCKS = _load_skill_blocks()
    return _SYSTEM_BLOCKS


def _log_cache(usage):
    """Print one of: CACHE WRITE | CACHE HIT | CACHE MISS based on usage."""
    write = getattr(usage, "cache_creation_input_tokens", 0) or 0
    hit = getattr(usage, "cache_read_input_tokens", 0) or 0
    if write and not hit:
        print(f"CACHE WRITE: {write} tokens written to cache")
    elif hit:
        print(f"CACHE HIT: {hit} tokens read from cache (saved)")
    else:
        print("CACHE MISS: no cache_read / cache_creation tokens reported")


def send_message(user_input: str, model: str = DEFAULT_MODEL, max_tokens: int = 1024,
                 stream: bool = False):
    """Send one message with the cached Skills system prompt.

    Returns the assistant text. For more advanced use (tools, multi-turn),
    call _client() directly with _system() as the system parameter.
    """
    client = _client()
    sys_blocks = _system()

    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=sys_blocks,
        messages=[{"role": "user", "content": user_input}],
    )
    _log_cache(resp.usage)

    # Collect text from content blocks
    parts = []
    for blk in resp.content:
        t = getattr(blk, "text", None)
        if t:
            parts.append(t)
    return "".join(parts)


def prewarm():
    """One-shot call to write the Skills bundle into cache. Smallest possible
    real request - max_tokens=1 because Anthropic requires >= 1."""
    print("Pre-warming Skills cache...")
    out = send_message("Reply with the single word: OK", max_tokens=4)
    print(f"  prewarm output: {out.strip()[:40]}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "prewarm":
        prewarm()
    else:
        msg = " ".join(sys.argv[1:]) or "Reply with the single word: OK"
        print(send_message(msg))
