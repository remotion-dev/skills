#!/usr/bin/env python3
"""
Surgical fix — repairs the broken copyRender() function that has literal newlines
inside single-quoted JS strings, killing the entire inline <script> block and
causing raw JS source to dump at the bottom of every dashboard.

Applies to all 5 single-topic dashboards. Idempotent (detects if already fixed).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path("/var/tmp/stage3/skills")
DASH_DIR = REPO / "content-calendars"
DASHBOARDS = [
    "2026-04-18-epa-two-years-homicide-free-production.html",
    "2026-04-19-peninsula-bidding-wars-back-production.html",
    "2026-04-19-epa-market-update-production.html",
    "2026-04-19-ca-smoke-detector-compliance-production.html",
    "2026-04-19-woodland-park-772-units-production.html",
]

# Clean replacement using a template literal (backticks) which supports newlines.
CLEAN_FUNCTION = """function copyRender(btn, key) {
  var cfg = window.HEYGEN_RENDER[key];
  var content = window.CONTENT_LIBRARY[key];
  if (!cfg || !content) { btn.textContent = 'No render config'; return; }
  var instruction =
    'Render this video via HeyGen MCP.\\n\\n' +
    'Format: ' + cfg.label + '\\n' +
    'Avatar: ' + cfg.avatar + ' (' + cfg.avatar_id + ') \\u2014 ' + cfg.reason + '\\n' +
    'Voice: Graeham Watts Voice Clone (' + cfg.voice_id + ')\\n' +
    'Aspect: ' + cfg.aspect + ' | Resolution: 1080p\\n\\n' +
    'Script to speak:\\n' +
    content + '\\n\\n' +
    'Call the HeyGen MCP generate_avatar_video tool. Confirm the avatar choice with me before submitting. Return the video_id and HeyGen dashboard URL so I can check status later.';
  navigator.clipboard.writeText(instruction).then(function(){
    var o = btn.textContent;
    btn.textContent = 'Copied! Paste into Claude with HeyGen MCP';
    btn.classList.add('copied');
    setTimeout(function(){ btn.textContent = o; btn.classList.remove('copied'); }, 3000);
  });
}"""

# Regex to match the BROKEN function. We anchor on the function header and
# terminate at the closing brace that follows the setTimeout call.
BROKEN_RE = re.compile(
    r"function copyRender\(btn, key\) \{"
    r".*?"
    r"navigator\.clipboard\.writeText\(instruction\)\.then\(function\(\)\{"
    r".*?"
    r"\}\);\s*\}",
    re.DOTALL,
)

SENTINEL = "COPY_RENDER_FIX_V1"


def patch_file(path: Path) -> str:
    html = path.read_text(encoding="utf-8")

    if SENTINEL in html:
        return "skip (already fixed)"

    m = BROKEN_RE.search(html)
    if not m:
        return "no match (unexpected — may already be clean)"

    # Verify the matched block has literal newlines inside a single-quoted string
    # (the bug we're fixing). If it doesn't, bail — we don't want to overwrite a
    # version that's already been repaired differently.
    span = m.group(0)
    suspicious = bool(re.search(r"'[^'\n]*\n\s*'", span))
    if not suspicious:
        return "match found but not broken — skipping"

    new_html = (
        html[:m.start()]
        + f"/* {SENTINEL} */ "
        + CLEAN_FUNCTION
        + html[m.end():]
    )
    path.write_text(new_html, encoding="utf-8")
    return "fixed"


def main() -> int:
    print(f"Repairing copyRender() in {len(DASHBOARDS)} dashboards")
    for name in DASHBOARDS:
        path = DASH_DIR / name
        if not path.exists():
            print(f"  MISSING: {name}")
            continue
        result = patch_file(path)
        print(f"  {name}  ->  {result}")
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
