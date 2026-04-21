#!/usr/bin/env python3
"""
Dashboard v6 unified visual language — full restyle.

Strategy:
  Instead of rewriting HTML (fragile), inject a UNIFY_V6 stylesheet AT THE END
  of <head> that overrides every existing pattern to a single card shape,
  typography, spacing, and 4-color palette (navy / gold / green / red).

HTML changes (minimal, targeted):
  - Wrap Shot List, Alternate Hooks, and Power-User ElevenLabs sections in
    <details class="u-advanced"> — collapsed by default so Peter isn't staring
    at crew/dev tooling.
  - Copy Bank stays visible (Peter's fast-lane workflow depends on it).
  - Every other change is pure CSS override.

Idempotent via sentinel UNIFY_V6.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path("/var/tmp/stage3/skills")
DASH_DIR = REPO / "content-calendars"
TARGET = "2026-04-18-epa-two-years-homicide-free-production.html"
SENTINEL = "UNIFY_V6"

# ---------------------------------------------------------------------------
# THE unified stylesheet
# ---------------------------------------------------------------------------

UNIFY_CSS = """
<style>
/* UNIFY_V6 — one visual language for the entire dashboard */

:root {
  --u-navy: #1B2A4A;
  --u-gold: #C5A258;
  --u-green: #2e7d32;
  --u-red: #c62828;
  --u-bg: #F7F5EF;
  --u-card: #FFFFFF;
  --u-border: rgba(27, 42, 74, 0.10);
  --u-text: #1B2A4A;
  --u-muted: #5a6478;
  --u-radius: 12px;
  --u-shadow: 0 2px 10px rgba(27, 42, 74, 0.06);
  --u-shadow-lg: 0 6px 20px rgba(27, 42, 74, 0.10);
  --u-font-display: 'Plus Jakarta Sans', 'DM Sans', system-ui, sans-serif;
  --u-font-body: 'DM Sans', system-ui, sans-serif;
}

/* ==============  PAGE  ============== */
body { background: var(--u-bg) !important; font-family: var(--u-font-body) !important; }
.page {
  max-width: 1120px !important;
  background: transparent !important;
  padding: 24px 20px !important;
  box-shadow: none !important;
}

/* ==============  SECTION HEADINGS  ============== */
h1, h2, h3, h4, .sh {
  font-family: var(--u-font-display) !important;
  color: var(--u-navy) !important;
  letter-spacing: -0.3px !important;
}
h2.sh {
  font-size: 18px !important;
  font-weight: 800 !important;
  margin: 36px 0 4px 0 !important;
  padding-bottom: 8px !important;
  border-bottom: 1px solid var(--u-border) !important;
}

/* ==============  UNIFIED CARD  ============== */
/* Every card-like block collapses into one shape. */
.isp-card, .ct-card, .gsc-card, .score-c, .data-card,
.cal-day, .flow-card, .prompt-card, .deriv-panel,
.data-section, .news-card {
  background: var(--u-card) !important;
  border: 1px solid var(--u-border) !important;
  border-radius: var(--u-radius) !important;
  box-shadow: var(--u-shadow) !important;
  padding: 16px 18px !important;
}

/* Kill per-type color accents — everything is one style */
.ct-data, .ct-disc, .ct-list,
.isp-card h4, .gsc-card h4, .data-card {
  border-left: none !important;
}

/* Small gold accent on the left of each card (optional consistency) */
.isp-card, .ct-card, .gsc-card {
  border-left: 3px solid var(--u-gold) !important;
}

/* ==============  INFO / HELP BOXES  ==============
   Previously section-help (blue), insight-box (green), btn-help (gray),
   cal-integrate (teal), comp (green), ds-note (gray), use-in (blue).
   All collapse to one style with gold left border. */
.section-help, .btn-help, .ds-note, .use-in, .cal-integrate,
.insight-box, .comp, .v5-cal-clarifier, .v5-inline-help {
  background: var(--u-card) !important;
  border: 1px solid var(--u-border) !important;
  border-left: 3px solid var(--u-gold) !important;
  border-radius: 0 8px 8px 0 !important;
  padding: 12px 16px !important;
  margin: 10px 0 !important;
  font-size: 13px !important;
  color: var(--u-text) !important;
  line-height: 1.55 !important;
  box-shadow: none !important;
}
/* Only semantic statuses keep their color */
.insight-box { border-left-color: var(--u-green) !important; }
.comp { border-left-color: var(--u-green) !important; }

/* ==============  HERO (already redesigned in v5, just refine)  ============== */
.hero {
  border-radius: var(--u-radius) !important;
  padding: 32px 36px !important;
  margin-bottom: 20px !important;
  box-shadow: var(--u-shadow-lg) !important;
}

/* ==============  FORMAT PICKER TABS  ============== */
.flow-map { gap: 8px !important; }
.flow-card {
  padding: 12px 14px !important;
  background: var(--u-card) !important;
  border: 1px solid var(--u-border) !important;
  box-shadow: none !important;
  transition: all 0.12s !important;
}
.flow-card:hover {
  border-color: var(--u-gold) !important;
  transform: translateY(-1px) !important;
  box-shadow: var(--u-shadow) !important;
}
.flow-card.active {
  background: var(--u-navy) !important;
  border-color: var(--u-navy) !important;
  color: #fff !important;
}
.flow-card.active .fc-type, .flow-card.active .fc-title { color: #fff !important; }
.fc-tag {
  background: rgba(197, 162, 88, 0.18) !important;
  color: var(--u-navy) !important;
  border-radius: 12px !important;
  padding: 2px 8px !important;
  font-size: 10px !important;
  font-weight: 700 !important;
}
.flow-card.active .fc-tag {
  background: rgba(197, 162, 88, 0.35) !important;
  color: #fff !important;
}

/* ==============  FORMAT PANELS — simplified ============== */
.deriv-panel { padding: 22px 24px !important; }
.prompt-card { background: transparent !important; border: none !important; box-shadow: none !important; padding: 0 !important; }
.pc-h {
  margin-bottom: 18px !important;
  padding-bottom: 12px !important;
  border-bottom: 1px solid var(--u-border) !important;
}
.pc-label {
  font-family: var(--u-font-display) !important;
  font-weight: 800 !important;
  font-size: 18px !important;
  color: var(--u-navy) !important;
}
.pc-meta { font-size: 12px !important; color: var(--u-muted) !important; }

.content-section {
  background: #FAFAFA !important;
  border: 1px solid var(--u-border) !important;
  border-radius: 8px !important;
  padding: 16px !important;
  margin: 12px 0 !important;
}
.cs-h {
  font-family: var(--u-font-display) !important;
  font-weight: 800 !important;
  font-size: 11px !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
  color: var(--u-gold) !important;
  margin-bottom: 10px !important;
  border: none !important;
  padding: 0 !important;
}
.content-preview {
  background: #fff !important;
  border: 1px solid var(--u-border) !important;
  border-radius: 6px !important;
  font-size: 12px !important;
  max-height: 180px !important;
  overflow: auto !important;
}

/* The main Copy buttons become THE action */
.copy-big {
  background: var(--u-gold) !important;
  color: var(--u-navy) !important;
  border: none !important;
  border-radius: 8px !important;
  padding: 12px 22px !important;
  font-family: var(--u-font-display) !important;
  font-weight: 800 !important;
  font-size: 13px !important;
  letter-spacing: 0.3px !important;
  cursor: pointer !important;
  box-shadow: 0 2px 6px rgba(197, 162, 88, 0.3) !important;
  transition: all 0.12s !important;
}
.copy-big:hover { transform: translateY(-1px) !important; box-shadow: 0 4px 10px rgba(197, 162, 88, 0.4) !important; }
.copy-big.copied { background: var(--u-green) !important; color: #fff !important; }

/* Collapse the regenerate section into a subtle tail link */
.regenerate-section {
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
  margin: 14px 0 0 0 !important;
  text-align: right !important;
}
.regenerate-section .regen-h { display: none !important; }
.regenerate-section .section-help { display: none !important; }
.regenerate-section .btn-help { display: none !important; }
.regenerate-section .char-meta { display: none !important; }
.regenerate-section .button-row { display: inline-block !important; margin: 0 !important; }
.regenerate-section .copy-outline {
  background: transparent !important;
  color: var(--u-muted) !important;
  border: 1px dashed var(--u-muted) !important;
  font-size: 11px !important;
  padding: 5px 12px !important;
  font-weight: 600 !important;
  letter-spacing: 0 !important;
  text-transform: none !important;
  border-radius: 6px !important;
}
.regenerate-section .copy-outline:hover { color: var(--u-navy) !important; border-color: var(--u-navy) !important; }

/* ==============  RENDER STATE CARDS  ============== */
.rs-card { border-radius: var(--u-radius) !important; box-shadow: var(--u-shadow) !important; }

/* ==============  TABLES  ============== */
.perf-tbl, .data-table {
  background: var(--u-card) !important;
  border-radius: var(--u-radius) !important;
  overflow: hidden !important;
  border: 1px solid var(--u-border) !important;
  box-shadow: var(--u-shadow) !important;
}
.perf-tbl th, .data-table th {
  background: #FAFAFA !important;
  color: var(--u-navy) !important;
  font-family: var(--u-font-display) !important;
  font-size: 11px !important;
  letter-spacing: 1px !important;
  text-transform: uppercase !important;
  font-weight: 800 !important;
  border-bottom: 1px solid var(--u-border) !important;
}
.perf-tbl td, .data-table td {
  border-bottom: 1px solid var(--u-border) !important;
  font-size: 13px !important;
}
.chg-up { color: var(--u-green) !important; font-weight: 700 !important; }
.chg-down { color: var(--u-red) !important; font-weight: 700 !important; }

/* ==============  CALENDAR DAYS  ============== */
.cal-day { padding: 14px !important; }
.cal-day-primary { border: 2px solid var(--u-gold) !important; }
.cal-dayname {
  font-family: var(--u-font-display) !important;
  font-weight: 800 !important;
  color: var(--u-navy) !important;
  font-size: 13px !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
}

/* ==============  ADVANCED / CREW SECTIONS (wrapped)  ============== */
details.u-advanced {
  background: var(--u-card);
  border: 1px solid var(--u-border);
  border-radius: var(--u-radius);
  margin: 20px 0;
  box-shadow: var(--u-shadow);
  overflow: hidden;
}
details.u-advanced > summary {
  list-style: none;
  cursor: pointer;
  padding: 18px 22px;
  font-family: var(--u-font-display);
  font-weight: 800;
  font-size: 14px;
  color: var(--u-navy);
  position: relative;
  display: block;
}
details.u-advanced > summary::-webkit-details-marker { display: none; }
details.u-advanced > summary::after {
  content: "+";
  position: absolute;
  right: 24px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 24px;
  color: var(--u-gold);
  font-weight: 800;
  line-height: 1;
}
details.u-advanced[open] > summary::after { content: "−"; }
details.u-advanced .u-tag {
  display: inline-block;
  background: rgba(197, 162, 88, 0.15);
  color: var(--u-navy);
  font-size: 10px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  font-weight: 800;
  padding: 3px 8px;
  border-radius: 10px;
  margin-left: 8px;
  vertical-align: middle;
}
details.u-advanced .u-body {
  padding: 8px 22px 22px 22px;
  border-top: 1px solid var(--u-border);
}

/* Hide the now-wrapped h2 inside advanced details (we show it in summary) */
details.u-advanced > .u-body > h2.sh:first-child { display: none !important; }
details.u-advanced > .u-body > h3:first-child { display: none !important; }

/* ==============  FOOTER  ============== */
.footer { border-top: 1px solid var(--u-border) !important; }

/* ==============  BUTTONS (general)  ============== */
.data-toggle {
  background: var(--u-navy) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 8px !important;
  font-family: var(--u-font-display) !important;
  font-weight: 700 !important;
  padding: 10px 20px !important;
}
.copy-outline {
  border-radius: 8px !important;
  font-family: var(--u-font-display) !important;
  font-weight: 700 !important;
}

/* ==============  FLOW MAP HEADER  ============== */
.flow-map .fc-type {
  font-size: 11px !important;
  letter-spacing: 0.8px !important;
  text-transform: uppercase !important;
  color: var(--u-muted) !important;
  font-weight: 800 !important;
}
.flow-map .fc-title {
  font-family: var(--u-font-display) !important;
  font-weight: 800 !important;
  color: var(--u-navy) !important;
  font-size: 13px !important;
}

/* Hide now-redundant tag pills where we added v5 badges */
.hero-meta .hm-pill { display: none !important; }

/* Score breakdown — cleaner */
.score-grid { gap: 12px !important; }
.score-c { text-align: center !important; }
.sv { font-family: var(--u-font-display) !important; color: var(--u-gold) !important; font-size: 28px !important; font-weight: 800 !important; }

/* Utility: pad body bottom */
.page > *:last-child { margin-bottom: 40px !important; }
</style>
"""

# ---------------------------------------------------------------------------
# Wrap a section in a <details class="u-advanced"> accordion
# ---------------------------------------------------------------------------

def wrap_section(html: str, heading_re: str, label: str, tag: str,
                 sentinel: str, end_heading_re: str) -> str:
    """Wrap HTML from heading_re up to (but not including) end_heading_re in
    a <details class="u-advanced"> block, with a summary bar."""
    if sentinel in html:
        return html

    # Find the start
    m_start = re.search(heading_re, html)
    if not m_start:
        return html

    # Find the end — search from after the heading
    m_end = re.search(end_heading_re, html[m_start.end():])
    if not m_end:
        # If no next heading, look for footer or close of body content
        end_pos = len(html)
    else:
        end_pos = m_start.end() + m_end.start()

    section = html[m_start.start():end_pos]

    wrapper = (
        f'<!-- {sentinel} -->\n'
        '<details class="u-advanced">\n'
        f'  <summary>{label} <span class="u-tag">{tag}</span></summary>\n'
        '  <div class="u-body">\n'
        + section + '\n'
        '  </div>\n'
        '</details>\n'
    )

    return html[:m_start.start()] + wrapper + html[end_pos:]


# ---------------------------------------------------------------------------
# Main patch
# ---------------------------------------------------------------------------

def patch_file(path: Path) -> str:
    html = path.read_text(encoding="utf-8")

    if SENTINEL in html:
        return "skip (already unified)"

    # 1. Inject UNIFY_V6 stylesheet — goes LAST in <head> so it overrides
    #    everything that came before.
    html = html.replace("</head>", UNIFY_CSS + "\n</head>", 1)

    # 2. Wrap Shot List section — ends at next <h2 class="sh"> (Copy Bank)
    html = wrap_section(
        html,
        heading_re=r'<h2 class="sh">[^<]*Shot List[^<]*</h2>',
        label='&#x1F3A5; Shot List &mdash; For crew / manual filming',
        tag='Skip if HeyGen-rendered',
        sentinel='UNIFY_V6_WRAP_SHOTLIST',
        end_heading_re=r'<h2 class="sh">',
    )

    # 3. Wrap Alternate Hooks — ends at next <h3> (Power-User ElevenLabs)
    html = wrap_section(
        html,
        heading_re=r'<h2 class="sh">[^<]*(?:\d+\s+)?Alternate Hooks[^<]*</h2>',
        label='&#x1F504; Alternate Hooks &mdash; A/B test swap-ins',
        tag='Only if primary underperforms',
        sentinel='UNIFY_V6_WRAP_HOOKS',
        end_heading_re=r'<h3[^>]*>|<div class="footer"',
    )

    # 4. Wrap Power-User ElevenLabs — ends at footer
    html = wrap_section(
        html,
        heading_re=r'<h3[^>]*>\s*(?:&[#\w]+;\s*)?Power-?User[^<]*ElevenLabs[^<]*</h3>',
        label='&#x1F680; Power-User &mdash; ElevenLabs voice pipeline',
        tag='Advanced',
        sentinel='UNIFY_V6_WRAP_ELEVEN',
        end_heading_re=r'<div class="footer"',
    )

    # 5. Sentinel — rsplit-safe (target final </body>)
    parts = html.rsplit("</body>", 1)
    if len(parts) == 2:
        html = parts[0] + f"<!-- {SENTINEL} -->\n</body>" + parts[1]

    path.write_text(html, encoding="utf-8")
    return "unified"


def main() -> int:
    path = DASH_DIR / TARGET
    if not path.exists():
        print(f"MISSING: {path}")
        return 1
    result = patch_file(path)
    print(f"{TARGET} -> {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
