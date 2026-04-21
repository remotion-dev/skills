#!/usr/bin/env python3
"""
unify_final.py — single consolidated patch.

Replaces the 4 layered stylesheets (RENDER_STATUS_CSS_V1, REDESIGN_V5_CSS,
UNIFY_V6, UNIFY_V6_TEXT_FIX) with ONE consolidated source-of-truth
stylesheet, and propagates the v5/v6 HTML transformations across all 5
dashboards.

Idempotent — sentinel UNIFIED_FINAL_V1.

Run after the existing chain (patch_dashboards_render_status, fix_copy_render_js,
redesign_v5, unify_v6, fix_advanced_text_color). This is the consolidation
step that collapses the cascade into one clean overlay.
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

SENTINEL = "UNIFIED_FINAL_V1"

# ---------------------------------------------------------------------------
# THE consolidated stylesheet — single source of truth for every overlay rule.
# Combines and replaces RENDER_STATUS_CSS_V1, REDESIGN_V5_CSS, UNIFY_V6,
# UNIFY_V6_TEXT_FIX. Original baseline <style> in each dashboard stays as-is;
# this is the one canonical OVERLAY, applied last in <head> so it wins.
# ---------------------------------------------------------------------------

CONSOLIDATED_CSS = """
<style>
/* ==========================================================================
 * UNIFIED_FINAL_V1 — single source of truth for dashboard overlay styles.
 * Every rule that previously lived in 4 separate injected stylesheets now
 * lives here. Edit ONLY this block to change visuals.
 * ==========================================================================
 */

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

/* === PAGE === */
body { background: var(--u-bg) !important; font-family: var(--u-font-body) !important; }
.page { max-width: 1120px !important; background: transparent !important; padding: 24px 20px !important; box-shadow: none !important; }

/* === SECTION HEADINGS === */
h1, h2, h3, h4, .sh { font-family: var(--u-font-display) !important; color: var(--u-navy) !important; letter-spacing: -0.3px !important; }
h2.sh { font-size: 18px !important; font-weight: 800 !important; margin: 36px 0 4px 0 !important; padding-bottom: 8px !important; border-bottom: 1px solid var(--u-border) !important; }

/* === UNIFIED CARD === */
.isp-card, .ct-card, .gsc-card, .score-c, .data-card,
.cal-day, .flow-card, .prompt-card, .deriv-panel,
.data-section, .news-card {
  background: var(--u-card) !important;
  border: 1px solid var(--u-border) !important;
  border-radius: var(--u-radius) !important;
  box-shadow: var(--u-shadow) !important;
  padding: 16px 18px !important;
}
.ct-data, .ct-disc, .ct-list, .isp-card h4, .gsc-card h4, .data-card { border-left: none !important; }
.isp-card, .ct-card, .gsc-card { border-left: 3px solid var(--u-gold) !important; }

/* === HELP / INFO BOXES — collapsed to one pattern === */
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
.insight-box { border-left-color: var(--u-green) !important; }
.comp { border-left-color: var(--u-green) !important; }

/* === HERO === */
.hero { border-radius: var(--u-radius) !important; padding: 32px 36px !important; margin-bottom: 20px !important; box-shadow: var(--u-shadow-lg) !important; }
.v5-hero { position: relative; padding-bottom: 6px; }
.v5-recommended-label {
  display: inline-block; background: var(--u-gold); color: var(--u-navy);
  font-size: 11px; font-weight: 800; letter-spacing: 2px; text-transform: uppercase;
  padding: 5px 12px; border-radius: 20px; margin-bottom: 12px;
}
.v5-hero-sub { font-size: 13px; color: rgba(255,255,255,0.72); margin: 6px 0 16px 0; line-height: 1.45; }

/* === HERO BADGES (clickable tooltips) === */
.v5-badge {
  position: relative; display: inline-flex; align-items: center; gap: 6px;
  background: rgba(255,255,255,0.08); color: #fff;
  padding: 7px 14px; border-radius: 20px;
  font-size: 12px; font-weight: 700;
  margin: 4px 6px 4px 0;
  cursor: help; border: 1px solid rgba(255,255,255,0.15);
  transition: background 0.15s;
}
.v5-badge:hover { background: rgba(255,255,255,0.16); }
.v5-badge.score { background: var(--u-gold); color: var(--u-navy); border-color: var(--u-gold); }
.v5-badge.pass { background: rgba(46,125,50,0.2); border-color: rgba(46,125,50,0.6); color: #a5d6a7; }
.v5-badge .b-tooltip {
  display: none; position: absolute; bottom: calc(100% + 8px); left: 0; z-index: 50;
  background: #fff; color: var(--u-navy); padding: 12px 14px; border-radius: 8px;
  font-size: 12px; font-weight: 400; line-height: 1.5; width: 280px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.25); border: 1px solid rgba(27,42,74,0.15);
  text-align: left;
}
.v5-badge .b-tooltip strong { color: var(--u-gold); font-weight: 700; display: block; margin-bottom: 4px; font-size: 11px; letter-spacing: 1px; text-transform: uppercase; }
.v5-badge:hover .b-tooltip, .v5-badge:focus .b-tooltip { display: block; }
.hero-meta .hm-pill { display: none !important; } /* hide old plain pills now badges replace */

/* === TIMING CARD === */
.v5-timing {
  background: #fff; border: 1px solid rgba(27,42,74,0.1); border-left: 4px solid var(--u-gold);
  padding: 16px 20px; border-radius: 0 10px 10px 0;
  margin: 22px 0 16px 0; font-size: 14px; line-height: 1.55; color: #2d3550;
}
.v5-timing .t-big { font-family: var(--u-font-display); font-weight: 800; color: var(--u-navy); font-size: 20px; margin-bottom: 4px; }
.v5-timing .t-math { font-size: 11px; color: var(--u-muted); margin-top: 6px; }
.v5-timing code { background: rgba(27,42,74,0.06); padding: 1px 5px; border-radius: 3px; font-size: 11px; }

/* === RESEARCH ACCORDION (v5) === */
details.v5-research {
  background: linear-gradient(180deg, #F7F5EF 0%, #FEFCF6 100%);
  border-radius: var(--u-radius); margin: 24px 0; padding: 0;
  border: 1px solid rgba(197,162,88,0.35); overflow: hidden;
}
details.v5-research > summary {
  list-style: none; cursor: pointer; padding: 18px 24px;
  font-family: var(--u-font-display); font-weight: 800; font-size: 15px; color: var(--u-navy);
  display: flex; align-items: center; gap: 12px; position: relative;
}
details.v5-research > summary::-webkit-details-marker { display: none; }
details.v5-research > summary::after {
  content: "+"; position: absolute; right: 24px; font-size: 24px;
  color: var(--u-gold); font-weight: 800; line-height: 1;
}
details.v5-research[open] > summary::after { content: "−"; }
details.v5-research > summary .v5r-sub { font-family: var(--u-font-body); font-weight: 500; font-size: 12px; color: var(--u-muted); margin-left: 4px; }
details.v5-research .v5r-body { padding: 8px 24px 24px 24px; border-top: 1px solid rgba(197,162,88,0.25); }

/* === CAL CLARIFIER === */
.v5-cal-clarifier { border-left-color: #3b4f99 !important; }

/* === FORMAT PICKER TABS === */
.flow-map { gap: 8px !important; }
.flow-card { padding: 12px 14px !important; transition: all 0.12s !important; }
.flow-card:hover { border-color: var(--u-gold) !important; transform: translateY(-1px) !important; box-shadow: var(--u-shadow) !important; }
.flow-card.active { background: var(--u-navy) !important; border-color: var(--u-navy) !important; color: #fff !important; }
.flow-card.active .fc-type, .flow-card.active .fc-title { color: #fff !important; }
.fc-tag { background: rgba(197, 162, 88, 0.18) !important; color: var(--u-navy) !important; border-radius: 12px !important; padding: 2px 8px !important; font-size: 10px !important; font-weight: 700 !important; }
.flow-card.active .fc-tag { background: rgba(197, 162, 88, 0.35) !important; color: #fff !important; }
.flow-map .fc-type { font-size: 11px !important; letter-spacing: 0.8px !important; text-transform: uppercase !important; color: var(--u-muted) !important; font-weight: 800 !important; }
.flow-map .fc-title { font-family: var(--u-font-display) !important; font-weight: 800 !important; color: var(--u-navy) !important; font-size: 13px !important; }

/* === FORMAT PANELS === */
.deriv-panel { padding: 22px 24px !important; }
.prompt-card { background: transparent !important; border: none !important; box-shadow: none !important; padding: 0 !important; }
.pc-h { margin-bottom: 18px !important; padding-bottom: 12px !important; border-bottom: 1px solid var(--u-border) !important; }
.pc-label { font-family: var(--u-font-display) !important; font-weight: 800 !important; font-size: 18px !important; color: var(--u-navy) !important; }
.pc-meta { font-size: 12px !important; color: var(--u-muted) !important; }
.content-section { background: #FAFAFA !important; border: 1px solid var(--u-border) !important; border-radius: 8px !important; padding: 16px !important; margin: 12px 0 !important; }
.cs-h { font-family: var(--u-font-display) !important; font-weight: 800 !important; font-size: 11px !important; letter-spacing: 1.5px !important; text-transform: uppercase !important; color: var(--u-gold) !important; margin-bottom: 10px !important; border: none !important; padding: 0 !important; }
.content-preview { background: #fff !important; border: 1px solid var(--u-border) !important; border-radius: 6px !important; font-size: 12px !important; max-height: 180px !important; overflow: auto !important; }

/* === COPY BUTTONS === */
.copy-big {
  background: var(--u-gold) !important; color: var(--u-navy) !important;
  border: none !important; border-radius: 8px !important;
  padding: 12px 22px !important;
  font-family: var(--u-font-display) !important; font-weight: 800 !important;
  font-size: 13px !important; letter-spacing: 0.3px !important;
  cursor: pointer !important;
  box-shadow: 0 2px 6px rgba(197, 162, 88, 0.3) !important;
  transition: all 0.12s !important;
}
.copy-big:hover { transform: translateY(-1px) !important; box-shadow: 0 4px 10px rgba(197, 162, 88, 0.4) !important; }
.copy-big.copied { background: var(--u-green) !important; color: #fff !important; }

/* Regenerate as subtle tail link */
.regenerate-section {
  background: transparent !important; border: none !important;
  padding: 0 !important; margin: 14px 0 0 0 !important; text-align: right !important;
}
.regenerate-section .regen-h, .regenerate-section .section-help, .regenerate-section .btn-help, .regenerate-section .char-meta { display: none !important; }
.regenerate-section .button-row { display: inline-block !important; margin: 0 !important; }
.regenerate-section .copy-outline {
  background: transparent !important; color: var(--u-muted) !important;
  border: 1px dashed var(--u-muted) !important;
  font-size: 11px !important; padding: 5px 12px !important; font-weight: 600 !important;
  letter-spacing: 0 !important; text-transform: none !important; border-radius: 6px !important;
}
.regenerate-section .copy-outline:hover { color: var(--u-navy) !important; border-color: var(--u-navy) !important; }

/* === RENDER STATUS CARDS === */
.rs-card { margin: 12px 0 16px 0; padding: 14px 16px; border-radius: var(--u-radius); font-family: var(--u-font-body); font-size: 13px; line-height: 1.5; border: 1px solid transparent; box-shadow: var(--u-shadow); }
.rs-card.done { background: #E8F5E9; border-color: var(--u-green); color: #1b5e20; }
.rs-card.pending { background: #FFF8E1; border-color: var(--u-gold); color: #6d4c00; }
.rs-card.failed { background: #FFEBEE; border-color: var(--u-red); color: #8b0000; }
.rs-card .rs-h { font-weight: 800; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
.rs-card video { width: 100%; max-width: 480px; border-radius: 8px; margin-top: 8px; display: block; background: #000; }
.rs-card a.rs-dl { display: inline-block; background: var(--u-navy); color: #fff; padding: 8px 14px; border-radius: 6px; font-weight: 700; font-size: 12px; text-decoration: none; margin-top: 10px; margin-right: 8px; }
.rs-card a.rs-dl:hover { background: #0f1a30; }
.rs-card a.rs-open { color: var(--u-navy); font-weight: 700; text-decoration: underline; font-size: 12px; }
.rs-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; vertical-align: middle; }
.rs-dot.done { background: var(--u-green); }
.rs-dot.pending { background: var(--u-gold); animation: rsPulse 1.2s infinite ease-in-out; }
.rs-dot.failed { background: var(--u-red); }
@keyframes rsPulse { 0%,100% { opacity: 1; } 50% { opacity: 0.3; } }

/* === PETER GUIDE === */
details.peter-guide {
  background: linear-gradient(135deg, var(--u-navy) 0%, #2a3d66 100%);
  color: #fff; border-radius: var(--u-radius); margin: 20px auto; padding: 18px 22px;
  max-width: 1100px; border: 2px solid var(--u-gold);
  box-shadow: 0 4px 14px rgba(27,42,74,0.18); font-family: var(--u-font-body);
}
details.peter-guide > summary {
  list-style: none; cursor: pointer; font-size: 16px; font-weight: 800;
  color: #fff; display: flex; align-items: center; gap: 10px;
}
details.peter-guide > summary::-webkit-details-marker { display: none; }
details.peter-guide > summary::after { content: "+"; margin-left: auto; font-size: 22px; color: var(--u-gold); font-weight: 800; }
details.peter-guide[open] > summary::after { content: "−"; }
details.peter-guide .pg-body { margin-top: 16px; font-size: 14px; line-height: 1.65; color: rgba(255,255,255,0.92); }
details.peter-guide .pg-body h3 { color: var(--u-gold); text-transform: uppercase; font-size: 12px; letter-spacing: 1.5px; margin: 18px 0 8px 0; font-weight: 800; }
details.peter-guide .pg-body ol { padding-left: 22px; }
details.peter-guide .pg-body ol li { margin-bottom: 8px; }
details.peter-guide .pg-body code { background: rgba(0,0,0,0.35); color: #a5d6a7; padding: 2px 6px; border-radius: 4px; font-family: ui-monospace, Consolas, monospace; font-size: 12px; }
details.peter-guide .pg-badge { display: inline-block; background: var(--u-gold); color: var(--u-navy); padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; margin-left: 8px; }

/* === ADVANCED ACCORDION === */
details.u-advanced {
  background: var(--u-card); border: 1px solid var(--u-border); border-radius: var(--u-radius);
  margin: 20px 0; box-shadow: var(--u-shadow); overflow: hidden;
}
details.u-advanced > summary {
  list-style: none; cursor: pointer; padding: 18px 22px;
  font-family: var(--u-font-display); font-weight: 800; font-size: 14px; color: var(--u-navy);
  position: relative; display: block;
}
details.u-advanced > summary::-webkit-details-marker { display: none; }
details.u-advanced > summary::after {
  content: "+"; position: absolute; right: 24px; top: 50%; transform: translateY(-50%);
  font-size: 24px; color: var(--u-gold); font-weight: 800; line-height: 1;
}
details.u-advanced[open] > summary::after { content: "−"; }
details.u-advanced .u-tag {
  display: inline-block; background: rgba(197, 162, 88, 0.15); color: var(--u-navy);
  font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; font-weight: 800;
  padding: 3px 8px; border-radius: 10px; margin-left: 8px; vertical-align: middle;
}
details.u-advanced .u-body { padding: 8px 22px 22px 22px; border-top: 1px solid var(--u-border); }
details.u-advanced > .u-body > h2.sh:first-child { display: none !important; }
details.u-advanced > .u-body > h3:first-child { display: none !important; }

/* Force readable text inside advanced accordion (overrides inline white styles
   that came from the original dark-bg ElevenLabs section) */
details.u-advanced .u-body, details.u-advanced .u-body p, details.u-advanced .u-body li,
details.u-advanced .u-body ol, details.u-advanced .u-body ul, details.u-advanced .u-body span,
details.u-advanced .u-body strong, details.u-advanced .u-body em, details.u-advanced .u-body code,
details.u-advanced .u-body div, details.u-advanced .u-body h3, details.u-advanced .u-body h4 {
  color: var(--u-navy) !important;
}
details.u-advanced .u-body code {
  background: rgba(27, 42, 74, 0.06) !important; color: var(--u-navy) !important;
  padding: 2px 6px !important; border-radius: 4px !important;
  font-family: ui-monospace, Consolas, monospace !important; font-size: 12px !important;
}
details.u-advanced .u-body > code, details.u-advanced .u-body p + code {
  display: block !important; white-space: pre-wrap !important; line-height: 1.6 !important;
  padding: 12px 14px !important; margin: 10px 0 !important;
  border: 1px solid rgba(27, 42, 74, 0.12) !important; overflow-x: auto !important;
}
details.u-advanced .u-body .cta-row {
  display: flex !important; flex-wrap: wrap !important; gap: 14px !important;
  padding: 12px 16px !important; background: #FAFAFA !important;
  border: 1px solid rgba(27, 42, 74, 0.1) !important; border-radius: 8px !important;
  margin-top: 14px !important; font-size: 12px !important; color: var(--u-navy) !important;
}
details.u-advanced .u-body .cta-row > div { color: var(--u-navy) !important; }

/* === TABLES === */
.perf-tbl, .data-table {
  background: var(--u-card) !important; border-radius: var(--u-radius) !important;
  overflow: hidden !important; border: 1px solid var(--u-border) !important;
  box-shadow: var(--u-shadow) !important;
}
.perf-tbl th, .data-table th {
  background: #FAFAFA !important; color: var(--u-navy) !important;
  font-family: var(--u-font-display) !important; font-size: 11px !important;
  letter-spacing: 1px !important; text-transform: uppercase !important; font-weight: 800 !important;
  border-bottom: 1px solid var(--u-border) !important;
}
.perf-tbl td, .data-table td { border-bottom: 1px solid var(--u-border) !important; font-size: 13px !important; }
.chg-up { color: var(--u-green) !important; font-weight: 700 !important; }
.chg-down { color: var(--u-red) !important; font-weight: 700 !important; }

/* === CALENDAR === */
.cal-day { padding: 14px !important; }
.cal-day-primary { border: 2px solid var(--u-gold) !important; }
.cal-dayname { font-family: var(--u-font-display) !important; font-weight: 800 !important; color: var(--u-navy) !important; font-size: 13px !important; letter-spacing: 1.5px !important; text-transform: uppercase !important; }

/* === SCORE BREAKDOWN === */
.score-grid { gap: 12px !important; }
.score-c { text-align: center !important; }
.sv { font-family: var(--u-font-display) !important; color: var(--u-gold) !important; font-size: 28px !important; font-weight: 800 !important; }

/* === FOOTER === */
.footer { border-top: 1px solid var(--u-border) !important; }

/* === BUTTONS === */
.data-toggle { background: var(--u-navy) !important; color: #fff !important; border: none !important; border-radius: 8px !important; font-family: var(--u-font-display) !important; font-weight: 700 !important; padding: 10px 20px !important; }
.copy-outline { border-radius: 8px !important; font-family: var(--u-font-display) !important; font-weight: 700 !important; }

.page > *:last-child { margin-bottom: 40px !important; }

/* === MOBILE === */
@media (max-width: 768px) {
  .v5-badge .b-tooltip { width: 240px; left: -100px; }
  .deriv-panel { padding: 16px !important; }
}
</style>
"""

# ---------------------------------------------------------------------------
# HTML transformation helpers
# ---------------------------------------------------------------------------

def wrap_research_accordion(html: str) -> str:
    if "V5_RESEARCH_ACCORDION" in html:
        return html
    start_m = re.search(r'<h2 class="sh">[^<]*Intelligence Stack', html)
    end_m = re.search(r'<h2 class="sh">[^<]*7-Day Posting Calendar', html)
    if not start_m or not end_m:
        return html
    start, end = start_m.start(), end_m.start()
    wrapped = (
        '<!-- V5_RESEARCH_ACCORDION -->\n'
        '<details class="v5-research">\n'
        '  <summary>&#x1F4CA; Why This Topic? &mdash; The Research <span class="v5r-sub">(click to expand &middot; 8 data sources + scoring + calendar context)</span></summary>\n'
        '  <div class="v5r-body">\n'
        + html[start:end] + '\n'
        '  </div>\n'
        '</details>\n'
    )
    return html[:start] + wrapped + html[end:]


def add_calendar_clarifier(html: str) -> str:
    if "V5_CAL_CLARIFIER" in html:
        return html
    clarifier = (
        '<!-- V5_CAL_CLARIFIER -->\n'
        '<div class="v5-cal-clarifier section-help">\n'
        '  <strong>Who does what, when:</strong> These are the times <strong>Peter publishes</strong> each format. He pulls finished content from the Copy Bank below or from each format panel. Times are based on actual IG performance data (top posts land 6&ndash;9am and 5&ndash;8pm). Click any day card to jump to that format.\n'
        '</div>\n'
    )
    pattern = re.compile(
        r'(<h2 class="sh">[^<]*7-Day Posting Calendar[^<]*</h2>\s*<p class="section-help">[^<]*(?:<[^<]+)*?</p>)',
        re.DOTALL,
    )
    m = pattern.search(html)
    if not m:
        return html
    return html[:m.end()] + '\n' + clarifier + html[m.end():]


def add_inline_help(html: str) -> str:
    # Shot List
    if "V5_HELP_SHOTLIST" not in html:
        sh_help = '<div class="v5-inline-help"><!-- V5_HELP_SHOTLIST --><strong>What a Shot List is:</strong> The filming guide for when you or a crew shoots b-roll or a live human-filmed version. It changes per format because IG Reels / TikTok need 9:16 vertical framing, YT Long needs 16:9 landscape, and YT Short needs 9:16 with tighter pacing. If you\'re rendering entirely via HeyGen avatar, you can ignore the shot list &mdash; it\'s for manual production only.</div>'
        html = re.sub(r'(<h2[^>]*>\s*(?:&[#\w]+;\s*)?Shot List[^<]*</h2>)', r'\1\n' + sh_help, html, count=1, flags=re.IGNORECASE)
    # Alternate Hooks
    if "V5_HELP_HOOKS" not in html:
        hk_help = '<div class="v5-inline-help"><!-- V5_HELP_HOOKS --><strong>What Alternate Hooks are:</strong> Three swap-in opening lines for A/B testing. If the primary hook underperforms 48 hours after posting (reach below your 2,125/wk IG average), re-upload with one of these swapped into the first 3 seconds. The hooks change per topic because they\'re written specifically to pair with the topic\'s emotional beat.</div>'
        html = re.sub(r'(<h[23][^>]*>\s*(?:&[#\w]+;\s*)?\d*\s*Alternate Hooks[^<]*</h[23]>)', r'\1\n' + hk_help, html, count=1, flags=re.IGNORECASE)
    # Power-User ElevenLabs
    if "V5_HELP_ELEVEN" not in html:
        el_help = '<div class="v5-inline-help"><!-- V5_HELP_ELEVEN --><strong>When to use this:</strong> HeyGen\'s built-in voice clone is great for 90% of your content, but for high-stakes videos (the YT Long, paid ads, sponsored content) you may want studio-grade voice. Use this path: (1) render the HeyGen avatar <em>without</em> audio, (2) generate the voiceover separately in ElevenLabs using your trained voice and this SSML script, (3) stitch audio + video in your editor. Trade-off: noticeably better voice quality for ~15 extra minutes of editing. Skip this for social-first content &mdash; HeyGen voice is fine there.</div>'
        html = re.sub(r'(<h[23][^>]*>\s*(?:&[#\w]+;\s*)?Power-?User[^<]*ElevenLabs[^<]*</h[23]>)', r'\1\n' + el_help, html, count=1, flags=re.IGNORECASE)
    return html


def wrap_advanced_section(html: str, heading_re: str, label: str, tag: str,
                          sentinel: str, end_re: str) -> str:
    if sentinel in html:
        return html
    m_start = re.search(heading_re, html)
    if not m_start:
        return html
    m_end = re.search(end_re, html[m_start.end():])
    end_pos = (m_start.end() + m_end.start()) if m_end else len(html)
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


def wrap_advanced_sections(html: str) -> str:
    html = wrap_advanced_section(
        html,
        r'<h2 class="sh">[^<]*Shot List[^<]*</h2>',
        '&#x1F3A5; Shot List &mdash; For crew / manual filming',
        'Skip if HeyGen-rendered',
        'UNIFY_V6_WRAP_SHOTLIST',
        r'<h2 class="sh">',
    )
    html = wrap_advanced_section(
        html,
        r'<h2 class="sh">[^<]*(?:\d+\s+)?Alternate Hooks[^<]*</h2>',
        '&#x1F504; Alternate Hooks &mdash; A/B test swap-ins',
        'Only if primary underperforms',
        'UNIFY_V6_WRAP_HOOKS',
        r'<h3[^>]*>|<div class="footer"',
    )
    html = wrap_advanced_section(
        html,
        r'<h3[^>]*>\s*(?:&[#\w]+;\s*)?Power-?User[^<]*ElevenLabs[^<]*</h3>',
        '&#x1F680; Power-User &mdash; ElevenLabs voice pipeline',
        'Advanced',
        'UNIFY_V6_WRAP_ELEVEN',
        r'<div class="footer"',
    )
    return html


def strip_marked_stylesheet(html: str, marker: str) -> str:
    """Remove the <style>...</style> block that contains the given marker.
    Robust to comments, line breaks, and arbitrary CSS in between by finding
    the marker first then walking outward to the enclosing tags.
    """
    idx = html.find(marker)
    if idx < 0:
        return html
    style_start = html.rfind('<style>', 0, idx)
    if style_start < 0:
        return html
    style_end = html.find('</style>', idx)
    if style_end < 0:
        return html
    return html[:style_start] + html[style_end + len('</style>'):]


def clean_stale_text(html: str) -> str:
    """Remove obsolete copy that no longer applies (was added during candidate-topic phase)."""
    # The "Tuesday April 21 candidate topic" calendar-integration block
    html = re.sub(
        r'This is the <strong>Tuesday April 21</strong> candidate topic[^<]*?(?:<a[^>]*>[^<]*</a>)?',
        'This topic is the anchor for <strong>Monday April 20, 2026</strong>.',
        html,
    )
    return html


# ---------------------------------------------------------------------------
# Main patch
# ---------------------------------------------------------------------------

def patch_file(path: Path) -> str:
    html = path.read_text(encoding="utf-8")

    if SENTINEL in html:
        return "skip (already final)"

    # 1. Apply v5 generic transformations (idempotent — skip if sentinel present)
    html = wrap_research_accordion(html)
    html = add_calendar_clarifier(html)
    html = add_inline_help(html)

    # 2. Apply v6 advanced wraps (idempotent)
    html = wrap_advanced_sections(html)

    # 3. Strip the 4 layered injected stylesheets
    for marker in [
        "RENDER_STATUS_CSS_V1",
        "REDESIGN_V5_CSS",
        "UNIFY_V6 — one visual language",
        "UNIFY_V6_TEXT_FIX",
    ]:
        html = strip_marked_stylesheet(html, marker)

    # 4. Inject the consolidated stylesheet (last in <head> so it wins)
    html = html.replace("</head>", CONSOLIDATED_CSS + "\n</head>", 1)

    # 5. Clean stale text
    html = clean_stale_text(html)

    # 6. Sentinel — rsplit-safe (target final </body>)
    parts = html.rsplit("</body>", 1)
    if len(parts) == 2:
        html = parts[0] + f"<!-- {SENTINEL} -->\n</body>" + parts[1]

    path.write_text(html, encoding="utf-8")
    return "unified-final"


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(
        description="Apply UNIFIED_FINAL_V1 overlay to dashboard HTML files. "
                    "Without --target, runs against all 5 known dashboards. "
                    "With --target, runs against a single new file (use this in "
                    "the canonical builder pipeline so freshly-generated "
                    "dashboards inherit the unified design).",
    )
    ap.add_argument("--target", default=None,
                    help="Path to a single dashboard HTML file. "
                         "Default: apply to all 5 production dashboards.")
    args = ap.parse_args()

    if args.target:
        path = Path(args.target).resolve()
        if not path.exists():
            print(f"MISSING: {path}")
            return 1
        result = patch_file(path)
        print(f"{path.name[:60]}  ->  {result}")
        return 0

    print(f"Unifying {len(DASHBOARDS)} dashboards")
    for name in DASHBOARDS:
        path = DASH_DIR / name
        if not path.exists():
            print(f"  MISSING: {name}")
            continue
        result = patch_file(path)
        print(f"  {name[:55]:<55}  ->  {result}")
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
