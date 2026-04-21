#!/usr/bin/env python3
"""
Quick fix — the Power-User ElevenLabs section has inline
color:rgba(255,255,255,...) styles that were readable when it sat inside a
dark navy block. After my v6 wrap put it in a white <details> accordion,
the white text is invisible/garbled on white.

Fix: append CSS that forces all text inside .u-advanced .u-body to navy,
overriding any inline white-color declarations via !important.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path("/var/tmp/stage3/skills")
DASH_DIR = REPO / "content-calendars"
TARGET = "2026-04-18-epa-two-years-homicide-free-production.html"
SENTINEL = "UNIFY_V6_TEXT_FIX"

CSS_FIX = """
<style>
/* UNIFY_V6_TEXT_FIX — force readable text color inside accordion bodies */
details.u-advanced .u-body,
details.u-advanced .u-body p,
details.u-advanced .u-body li,
details.u-advanced .u-body ol,
details.u-advanced .u-body ul,
details.u-advanced .u-body span,
details.u-advanced .u-body strong,
details.u-advanced .u-body em,
details.u-advanced .u-body code,
details.u-advanced .u-body div,
details.u-advanced .u-body h3,
details.u-advanced .u-body h4 {
  color: #1B2A4A !important;
}
details.u-advanced .u-body code {
  background: rgba(27, 42, 74, 0.06) !important;
  color: #1B2A4A !important;
  padding: 2px 6px !important;
  border-radius: 4px !important;
  font-family: ui-monospace, Consolas, monospace !important;
  font-size: 12px !important;
}
/* Make any block-level code block readable */
details.u-advanced .u-body > code,
details.u-advanced .u-body p + code {
  display: block !important;
  white-space: pre-wrap !important;
  line-height: 1.6 !important;
  padding: 12px 14px !important;
  margin: 10px 0 !important;
  border: 1px solid rgba(27, 42, 74, 0.12) !important;
  overflow-x: auto !important;
}
/* cta-row (voice/avatar/ghl references at bottom of ElevenLabs section) */
details.u-advanced .u-body .cta-row {
  display: flex !important;
  flex-wrap: wrap !important;
  gap: 14px !important;
  padding: 12px 16px !important;
  background: #FAFAFA !important;
  border: 1px solid rgba(27, 42, 74, 0.1) !important;
  border-radius: 8px !important;
  margin-top: 14px !important;
  font-size: 12px !important;
  color: #1B2A4A !important;
}
details.u-advanced .u-body .cta-row > div {
  color: #1B2A4A !important;
}
</style>
"""


def main() -> int:
    path = DASH_DIR / TARGET
    html = path.read_text(encoding="utf-8")
    if SENTINEL in html:
        print("already fixed")
        return 0
    # Inject right before </head>
    html = html.replace("</head>", CSS_FIX + "\n</head>", 1)
    path.write_text(html, encoding="utf-8")
    print("fixed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
