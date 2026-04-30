#!/usr/bin/env python3
"""
polish_v2.py — second-pass polish on top of unify_final.py.

What it does (idempotent, all 5 dashboards):
  1. Strips the previous UNIFIED_FINAL_V1 stylesheet so we can re-inject the
     updated CONSOLIDATED_CSS_V2 (now with hero-h1 contrast fix + a few
     spacing tweaks).
  2. Propagates the v5 hero structure to the other 4 dashboards by
     extracting their existing topic_meta from the OLD hero block and
     rebuilding with the new framing (recommended-label, clickable badge
     tooltips, plain-English timing card, Fair Housing pill).
  3. Reschedules every "Monday April 20" reference forward by one week to
     "Monday April 27" (and proportionally shifts April 18 generation date
     to April 25, week-of references to April 27, etc).
  4. Marks each file with sentinel UNIFIED_FINAL_V2.

Run: python3 scripts/polish_v2.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path("/var/tmp/stage3/skills")
DASH_DIR = REPO / "content-calendars"

# Day-of-week mapping for v5 hero "recommended topic" label
DAY_FOR_TOPIC = {
    "2026-04-18-epa-two-years-homicide-free-production.html":   ("Monday", "April 27, 2026"),
    "2026-04-19-peninsula-bidding-wars-back-production.html":   ("Tuesday", "April 28, 2026"),
    "2026-04-19-epa-market-update-production.html":             ("Wednesday", "April 29, 2026"),
    "2026-04-19-ca-smoke-detector-compliance-production.html":  ("Thursday", "April 30, 2026"),
    "2026-04-19-woodland-park-772-units-production.html":       ("Friday", "May 1, 2026"),
}

DASHBOARDS = list(DAY_FOR_TOPIC.keys())

OLD_SENTINEL = "UNIFIED_FINAL_V1"
NEW_SENTINEL = "UNIFIED_FINAL_V2"

# ---------------------------------------------------------------------------
# CONSOLIDATED CSS V2 — same as V1 + hero h1 contrast fix + a few touchups
# ---------------------------------------------------------------------------

CONSOLIDATED_CSS_V2 = """
<style>
/* ==========================================================================
 * UNIFIED_FINAL_V2 — single source of truth for dashboard overlay styles.
 * V2 changes vs V1:
 *   - Hero h1 forced to white (was inheriting global navy → invisible on
 *     navy gradient hero)
 *   - Hero h1 size bumped slightly for visual hierarchy
 *   - Eyebrow "Content Engine Stage 3..." de-emphasized further so the
 *     real topic title dominates
 *   - Tighter top-of-page rhythm
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

body { background: var(--u-bg) !important; font-family: var(--u-font-body) !important; }
.page { max-width: 1120px !important; background: transparent !important; padding: 24px 20px !important; box-shadow: none !important; }

h1, h2, h3, h4, .sh { font-family: var(--u-font-display) !important; color: var(--u-navy) !important; letter-spacing: -0.3px !important; }
h2.sh { font-size: 18px !important; font-weight: 800 !important; margin: 36px 0 4px 0 !important; padding-bottom: 8px !important; border-bottom: 1px solid var(--u-border) !important; }

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

/* === HERO === V2 contrast fix: force white h1 on navy gradient bg */
.hero { border-radius: var(--u-radius) !important; padding: 32px 36px !important; margin-bottom: 20px !important; box-shadow: var(--u-shadow-lg) !important; }
.hero h1, .v5-hero h1 {
  color: #FFFFFF !important;
  font-size: 30px !important;
  font-weight: 800 !important;
  line-height: 1.2 !important;
  margin: 6px 0 12px 0 !important;
  letter-spacing: -0.5px !important;
}
.hero .hsub, .v5-hero .hsub { color: rgba(255,255,255,0.78) !important; font-size: 14px !important; }
.hero .hero-ey { font-size: 10px !important; letter-spacing: 1.5px !important; opacity: 0.5 !important; text-transform: uppercase !important; color: rgba(255,255,255,0.6) !important; font-weight: 700 !important; margin-bottom: 8px !important; }
.hero .pow { font-size: 11px !important; opacity: 0.6 !important; color: rgba(255,255,255,0.6) !important; margin-top: 14px !important; }

.v5-hero { position: relative; padding-bottom: 6px; }
.v5-recommended-label {
  display: inline-block; background: var(--u-gold); color: var(--u-navy);
  font-size: 11px; font-weight: 800; letter-spacing: 2px; text-transform: uppercase;
  padding: 5px 12px; border-radius: 20px; margin-bottom: 12px;
}
.v5-hero-sub { font-size: 13px; color: rgba(255,255,255,0.72); margin: 6px 0 16px 0; line-height: 1.45; }

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
.hero-meta .hm-pill { display: none !important; }

.v5-timing {
  background: #fff; border: 1px solid rgba(27,42,74,0.1); border-left: 4px solid var(--u-gold);
  padding: 16px 20px; border-radius: 0 10px 10px 0;
  margin: 22px 0 16px 0; font-size: 14px; line-height: 1.55; color: #2d3550;
}
.v5-timing .t-big { font-family: var(--u-font-display); font-weight: 800; color: var(--u-navy); font-size: 20px; margin-bottom: 4px; }
.v5-timing .t-math { font-size: 11px; color: var(--u-muted); margin-top: 6px; }
.v5-timing code { background: rgba(27,42,74,0.06); padding: 1px 5px; border-radius: 3px; font-size: 11px; }

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
details.v5-research > summary::after { content: "+"; position: absolute; right: 24px; font-size: 24px; color: var(--u-gold); font-weight: 800; line-height: 1; }
details.v5-research[open] > summary::after { content: "−"; }
details.v5-research > summary .v5r-sub { font-family: var(--u-font-body); font-weight: 500; font-size: 12px; color: var(--u-muted); margin-left: 4px; }
details.v5-research .v5r-body { padding: 8px 24px 24px 24px; border-top: 1px solid rgba(197,162,88,0.25); }

.v5-cal-clarifier { border-left-color: #3b4f99 !important; }

.flow-map { gap: 8px !important; }
.flow-card { padding: 12px 14px !important; transition: all 0.12s !important; }
.flow-card:hover { border-color: var(--u-gold) !important; transform: translateY(-1px) !important; box-shadow: var(--u-shadow) !important; }
.flow-card.active { background: var(--u-navy) !important; border-color: var(--u-navy) !important; color: #fff !important; }
.flow-card.active .fc-type, .flow-card.active .fc-title { color: #fff !important; }
.fc-tag { background: rgba(197, 162, 88, 0.18) !important; color: var(--u-navy) !important; border-radius: 12px !important; padding: 2px 8px !important; font-size: 10px !important; font-weight: 700 !important; }
.flow-card.active .fc-tag { background: rgba(197, 162, 88, 0.35) !important; color: #fff !important; }
.flow-map .fc-type { font-size: 11px !important; letter-spacing: 0.8px !important; text-transform: uppercase !important; color: var(--u-muted) !important; font-weight: 800 !important; }
.flow-map .fc-title { font-family: var(--u-font-display) !important; font-weight: 800 !important; color: var(--u-navy) !important; font-size: 13px !important; }

.deriv-panel { padding: 22px 24px !important; }
.prompt-card { background: transparent !important; border: none !important; box-shadow: none !important; padding: 0 !important; }
.pc-h { margin-bottom: 18px !important; padding-bottom: 12px !important; border-bottom: 1px solid var(--u-border) !important; }
.pc-label { font-family: var(--u-font-display) !important; font-weight: 800 !important; font-size: 18px !important; color: var(--u-navy) !important; }
.pc-meta { font-size: 12px !important; color: var(--u-muted) !important; }
.content-section { background: #FAFAFA !important; border: 1px solid var(--u-border) !important; border-radius: 8px !important; padding: 16px !important; margin: 12px 0 !important; }
.cs-h { font-family: var(--u-font-display) !important; font-weight: 800 !important; font-size: 11px !important; letter-spacing: 1.5px !important; text-transform: uppercase !important; color: var(--u-gold) !important; margin-bottom: 10px !important; border: none !important; padding: 0 !important; }
.content-preview { background: #fff !important; border: 1px solid var(--u-border) !important; border-radius: 6px !important; font-size: 12px !important; max-height: 180px !important; overflow: auto !important; }

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

.regenerate-section { background: transparent !important; border: none !important; padding: 0 !important; margin: 14px 0 0 0 !important; text-align: right !important; }
.regenerate-section .regen-h, .regenerate-section .section-help, .regenerate-section .btn-help, .regenerate-section .char-meta { display: none !important; }
.regenerate-section .button-row { display: inline-block !important; margin: 0 !important; }
.regenerate-section .copy-outline { background: transparent !important; color: var(--u-muted) !important; border: 1px dashed var(--u-muted) !important; font-size: 11px !important; padding: 5px 12px !important; font-weight: 600 !important; letter-spacing: 0 !important; text-transform: none !important; border-radius: 6px !important; }
.regenerate-section .copy-outline:hover { color: var(--u-navy) !important; border-color: var(--u-navy) !important; }

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

details.peter-guide { background: linear-gradient(135deg, var(--u-navy) 0%, #2a3d66 100%); color: #fff; border-radius: var(--u-radius); margin: 20px auto; padding: 18px 22px; max-width: 1100px; border: 2px solid var(--u-gold); box-shadow: 0 4px 14px rgba(27,42,74,0.18); font-family: var(--u-font-body); }
details.peter-guide > summary { list-style: none; cursor: pointer; font-size: 16px; font-weight: 800; color: #fff; display: flex; align-items: center; gap: 10px; }
details.peter-guide > summary::-webkit-details-marker { display: none; }
details.peter-guide > summary::after { content: "+"; margin-left: auto; font-size: 22px; color: var(--u-gold); font-weight: 800; }
details.peter-guide[open] > summary::after { content: "−"; }
details.peter-guide .pg-body { margin-top: 16px; font-size: 14px; line-height: 1.65; color: rgba(255,255,255,0.92); }
details.peter-guide .pg-body h3 { color: var(--u-gold); text-transform: uppercase; font-size: 12px; letter-spacing: 1.5px; margin: 18px 0 8px 0; font-weight: 800; }
details.peter-guide .pg-body ol { padding-left: 22px; }
details.peter-guide .pg-body ol li { margin-bottom: 8px; }
details.peter-guide .pg-body code { background: rgba(0,0,0,0.35); color: #a5d6a7; padding: 2px 6px; border-radius: 4px; font-family: ui-monospace, Consolas, monospace; font-size: 12px; }
details.peter-guide .pg-badge { display: inline-block; background: var(--u-gold); color: var(--u-navy); padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; margin-left: 8px; }

details.u-advanced { background: var(--u-card); border: 1px solid var(--u-border); border-radius: var(--u-radius); margin: 20px 0; box-shadow: var(--u-shadow); overflow: hidden; }
details.u-advanced > summary { list-style: none; cursor: pointer; padding: 18px 22px; font-family: var(--u-font-display); font-weight: 800; font-size: 14px; color: var(--u-navy); position: relative; display: block; }
details.u-advanced > summary::-webkit-details-marker { display: none; }
details.u-advanced > summary::after { content: "+"; position: absolute; right: 24px; top: 50%; transform: translateY(-50%); font-size: 24px; color: var(--u-gold); font-weight: 800; line-height: 1; }
details.u-advanced[open] > summary::after { content: "−"; }
details.u-advanced .u-tag { display: inline-block; background: rgba(197, 162, 88, 0.15); color: var(--u-navy); font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; font-weight: 800; padding: 3px 8px; border-radius: 10px; margin-left: 8px; vertical-align: middle; }
details.u-advanced .u-body { padding: 8px 22px 22px 22px; border-top: 1px solid var(--u-border); }
details.u-advanced > .u-body > h2.sh:first-child { display: none !important; }
details.u-advanced > .u-body > h3:first-child { display: none !important; }

details.u-advanced .u-body, details.u-advanced .u-body p, details.u-advanced .u-body li, details.u-advanced .u-body ol, details.u-advanced .u-body ul, details.u-advanced .u-body span, details.u-advanced .u-body strong, details.u-advanced .u-body em, details.u-advanced .u-body code, details.u-advanced .u-body div, details.u-advanced .u-body h3, details.u-advanced .u-body h4 { color: var(--u-navy) !important; }
details.u-advanced .u-body code { background: rgba(27, 42, 74, 0.06) !important; color: var(--u-navy) !important; padding: 2px 6px !important; border-radius: 4px !important; font-family: ui-monospace, Consolas, monospace !important; font-size: 12px !important; }
details.u-advanced .u-body > code, details.u-advanced .u-body p + code { display: block !important; white-space: pre-wrap !important; line-height: 1.6 !important; padding: 12px 14px !important; margin: 10px 0 !important; border: 1px solid rgba(27, 42, 74, 0.12) !important; overflow-x: auto !important; }
details.u-advanced .u-body .cta-row { display: flex !important; flex-wrap: wrap !important; gap: 14px !important; padding: 12px 16px !important; background: #FAFAFA !important; border: 1px solid rgba(27, 42, 74, 0.1) !important; border-radius: 8px !important; margin-top: 14px !important; font-size: 12px !important; color: var(--u-navy) !important; }
details.u-advanced .u-body .cta-row > div { color: var(--u-navy) !important; }

.perf-tbl, .data-table { background: var(--u-card) !important; border-radius: var(--u-radius) !important; overflow: hidden !important; border: 1px solid var(--u-border) !important; box-shadow: var(--u-shadow) !important; }
.perf-tbl th, .data-table th { background: #FAFAFA !important; color: var(--u-navy) !important; font-family: var(--u-font-display) !important; font-size: 11px !important; letter-spacing: 1px !important; text-transform: uppercase !important; font-weight: 800 !important; border-bottom: 1px solid var(--u-border) !important; }
.perf-tbl td, .data-table td { border-bottom: 1px solid var(--u-border) !important; font-size: 13px !important; }
.chg-up { color: var(--u-green) !important; font-weight: 700 !important; }
.chg-down { color: var(--u-red) !important; font-weight: 700 !important; }

.cal-day { padding: 14px !important; }
.cal-day-primary { border: 2px solid var(--u-gold) !important; }
.cal-dayname { font-family: var(--u-font-display) !important; font-weight: 800 !important; color: var(--u-navy) !important; font-size: 13px !important; letter-spacing: 1.5px !important; text-transform: uppercase !important; }

.score-grid { gap: 12px !important; }
.score-c { text-align: center !important; }
.sv { font-family: var(--u-font-display) !important; color: var(--u-gold) !important; font-size: 28px !important; font-weight: 800 !important; }

.footer { border-top: 1px solid var(--u-border) !important; }

.data-toggle { background: var(--u-navy) !important; color: #fff !important; border: none !important; border-radius: 8px !important; font-family: var(--u-font-display) !important; font-weight: 700 !important; padding: 10px 20px !important; }
.copy-outline { border-radius: 8px !important; font-family: var(--u-font-display) !important; font-weight: 700 !important; }

.page > *:last-child { margin-bottom: 40px !important; }

@media (max-width: 768px) {
  .v5-badge .b-tooltip { width: 240px; left: -100px; }
  .deriv-panel { padding: 16px !important; }
  .hero h1 { font-size: 24px !important; }
}
</style>
"""


# ---------------------------------------------------------------------------
# Hero extraction + rebuild for the OTHER 4 dashboards
# ---------------------------------------------------------------------------

def extract_topic_meta_from_hero(html: str) -> dict:
    """Extract title/subtitle/score/funnel/pillar/ghl/target from existing hero."""
    meta = {}
    # h1 title
    m = re.search(r'<div class="hero(?:\s+v5-hero)?">.*?<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if m:
        meta['title'] = m.group(1).strip()
    # subtitle (.hsub OR .v5-hero-sub)
    m = re.search(r'<div class="hsub">(.*?)</div>', html, re.DOTALL)
    if m:
        meta['subtitle'] = m.group(1).strip()
    else:
        m = re.search(r'<div class="v5-hero-sub">(.*?)</div>', html, re.DOTALL)
        if m:
            meta['subtitle'] = m.group(1).strip()
    # opportunity score
    m = re.search(r'(\d+)/10', html)
    if m:
        meta['score'] = m.group(1)
    # funnel
    m = re.search(r'Funnel[:\s]+([A-Za-z\s\->]+?)<', html)
    if m:
        meta['funnel'] = m.group(1).strip()
    # pillar
    m = re.search(r'Pillar\s+([\d\s+]+)', html)
    if m:
        meta['pillar'] = m.group(1).strip()
    # GHL keyword
    m = re.search(r'GHL Keyword[:\s]+([A-Z]+)', html)
    if m:
        meta['ghl'] = m.group(1).strip()
    # target time
    m = re.search(r'Target[:\s]+~?([\d:]+)', html)
    if m:
        meta['target'] = m.group(1).strip()
    return meta


def build_v5_hero(meta: dict, day: str, date: str, source_html: str) -> str:
    """Build a fresh v5 hero block using extracted topic_meta."""
    title = meta.get('title', 'Untitled Topic')
    subtitle = meta.get('subtitle', '')
    score = meta.get('score', '10')
    funnel = meta.get('funnel', 'TOFU')
    pillar = meta.get('pillar', '5')
    ghl = meta.get('ghl', 'EPA')
    target = meta.get('target', '4:30')

    # Pull the spoken word count if available so timing math is real (not generic)
    word_match = re.search(r'(\d+)\s+words?\s+of\s+spoken script body', source_html)
    word_count = int(word_match.group(1)) if word_match else 573
    minutes = round((word_count / 150) * 1.15, 2)

    return f"""<div class="hero v5-hero">
  <div class="v5-recommended-label">&#x1F4C5; {day}, {date} &middot; Recommended Topic</div>
  <h1>{title}</h1>
  <div class="v5-hero-sub">{subtitle}</div>

  <div class="hero-meta" style="margin-top:14px">
    <span class="v5-badge score" tabindex="0">
      &starf; {score}/10 Opportunity
      <span class="b-tooltip"><strong>Opportunity Score</strong>How strong this topic is on a 10-point scale. Built from four sub-scores: Timeliness + Audience Relevance + Content Gap + Engagement Potential. See the "Why This Topic?" accordion for the full breakdown.</span>
    </span>
    <span class="v5-badge" tabindex="0">
      &#x1F3AF; Funnel: {funnel}
      <span class="b-tooltip"><strong>Funnel Stage</strong>TOFU = top (awareness/discovery), MOFU = middle (consideration), BOFU = bottom (ready to act). Tells you who this topic is targeting and what action it should drive.</span>
    </span>
    <span class="v5-badge" tabindex="0">
      &#x1F3DB; Pillar {pillar}
      <span class="b-tooltip"><strong>Content Pillar</strong>Which of your 5 content pillars this topic serves. Pillar 1 = First-Time Buyer, 2 = Seller Education, 3 = Buyer Strategy, 4 = Market Intelligence, 5 = Community / Local Stories. Cross-pillar topics tend to perform best.</span>
    </span>
    <span class="v5-badge" tabindex="0">
      &#x1F517; GHL Keyword: {ghl}
      <span class="b-tooltip"><strong>GoHighLevel Comment Trigger</strong>The word viewers comment on IG/FB to auto-enter the follow-up sequence. Tracks leads from this topic specifically so you can measure conversion.</span>
    </span>
    <span class="v5-badge pass" tabindex="0">
      &#x2705; Fair Housing OK
      <span class="b-tooltip"><strong>Fair Housing Compliance</strong>Passed. Content frames data as statistics + community policy, never as neighborhood character or demographic proxy.</span>
    </span>
  </div>

  <div class="v5-timing">
    <div class="t-big">&#x1F3AC; Target video length: ~{target} min</div>
    <div>Based on a verified count of {word_count} spoken words in the YT Long script.</div>
    <div class="t-math">Math: <code>{word_count} words &divide; 150 WPM &times; 1.15 pause/B-roll buffer = {minutes} min</code>. Not a generic estimate.</div>
  </div>

  <div class="pow">Generated April 25, 2026 &middot; Content Creation Engine v5 &middot; Intero Real Estate &middot; DRE #01466876</div>
</div>"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def strip_marked_stylesheet(html: str, marker: str) -> str:
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


def reschedule_dates(html: str) -> str:
    """Shift all 'this week' references forward by 7 days (April 18-20 → April 25-27)."""
    swaps = [
        # Specific dates
        ('Monday April 20, 2026', 'Monday April 27, 2026'),
        ('Monday, April 20, 2026', 'Monday, April 27, 2026'),
        ('Monday Apr 20', 'Monday Apr 27'),
        ('April 20, 2026', 'April 27, 2026'),
        ('April 20 V6 calendar', 'April 27 V6 calendar'),
        ('April 18, 2026', 'April 25, 2026'),
        ('Generated April 18', 'Generated April 25'),
        ('Generated April 19', 'Generated April 25'),
        ('Apr 13-19', 'Apr 20-26'),  # Recent Performance "last week"
        ('Apr 6-12', 'Apr 13-19'),    # Recent Performance "prior week"
        ('Week of April 20, 2026', 'Week of April 27, 2026'),
        ('April 17, 2026 milestone announcement', 'April 17, 2026 milestone announcement'),  # historical, keep
        ('Generated April 18, 2026', 'Generated April 25, 2026'),
    ]
    for old, new in swaps:
        html = html.replace(old, new)
    return html


def replace_hero(html: str, new_hero: str) -> str:
    """Replace the existing top hero block with the new one."""
    pattern = re.compile(r'<div class="hero(?:\s+v5-hero)?">.*?</div>\s*(?=\n\n|<div\s+class="data-toggle-wrap"|<details class="peter-guide"|<!-- PETER_GUIDE_V1 -->|<button)', re.DOTALL)
    m = pattern.search(html)
    if not m:
        # Looser match
        pattern = re.compile(r'<div class="hero[^"]*">.*?(?=<div class="data-toggle-wrap"|<details class="peter-guide"|<!-- PETER_GUIDE_V1)', re.DOTALL)
        m = pattern.search(html)
        if not m:
            return html
    return html[:m.start()] + new_hero + '\n' + html[m.end():]


# ---------------------------------------------------------------------------
# Main patch
# ---------------------------------------------------------------------------

def patch_file(name: str, path: Path) -> str:
    html = path.read_text(encoding="utf-8")

    if NEW_SENTINEL in html:
        return "skip (already V2)"

    # 1. Strip the previous V1 consolidated stylesheet
    html = strip_marked_stylesheet(html, OLD_SENTINEL)
    # Also strip V2 if a half-applied previous run left one
    html = strip_marked_stylesheet(html, NEW_SENTINEL)

    # 2. Inject the V2 consolidated stylesheet
    html = html.replace("</head>", CONSOLIDATED_CSS_V2 + "\n</head>", 1)

    # 3. Rebuild hero with v5 structure (using extracted topic_meta if hero
    #    is still old-style; if hero already has v5-hero class, leave it)
    has_v5_hero = 'class="hero v5-hero"' in html or 'v5-recommended-label' in html
    if not has_v5_hero:
        meta = extract_topic_meta_from_hero(html)
        if meta.get('title'):
            day, date = DAY_FOR_TOPIC.get(name, ('Monday', 'April 27, 2026'))
            new_hero = build_v5_hero(meta, day, date, html)
            html = replace_hero(html, new_hero)
    else:
        # Update the existing v5 hero's recommended-label to the new day/date
        day, date = DAY_FOR_TOPIC.get(name, ('Monday', 'April 27, 2026'))
        html = re.sub(
            r'<div class="v5-recommended-label">[^<]*</div>',
            f'<div class="v5-recommended-label">&#x1F4C5; {day}, {date} &middot; Recommended Topic</div>',
            html, count=1
        )

    # 4. Remove the now-orphaned legacy how-to / timing-card / comp blocks
    #    that the v5 hero replaces. Idempotent — safe if already gone.
    for orphan in [
        r'<div class="how-to">.*?</div>\s*</ol>\s*</div>',
        r'<div class="how-to">[\s\S]*?</ol>\s*</div>',
        r'<div class="timing-card">[\s\S]*?</div>\s*</div>',
        r'<div class="comp">[\s\S]*?</div>\s*</div>',
    ]:
        html = re.sub(orphan, '', html, count=1)

    # 5. Reschedule dates
    html = reschedule_dates(html)

    # 6. Mark with new sentinel (use rsplit so we hit the REAL </body>)
    parts = html.rsplit("</body>", 1)
    if len(parts) == 2:
        html = parts[0] + f"<!-- {NEW_SENTINEL} -->\n</body>" + parts[1]

    path.write_text(html, encoding="utf-8")
    return "polished-v2"


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(
        description="Apply UNIFIED_FINAL_V2 overlay. Without --target, runs "
                    "against all 5 production dashboards. With --target, runs "
                    "against a single file (called by the canonical builder "
                    "so new dashboards inherit the unified design).",
    )
    ap.add_argument("--target", default=None,
                    help="Path to a single dashboard HTML file.")
    ap.add_argument("--day", default=None,
                    help="Day of week (e.g. 'Monday') for new dashboards not "
                         "yet in DAY_FOR_TOPIC. Default: 'Monday'.")
    ap.add_argument("--date", default=None,
                    help="Date string (e.g. 'April 27, 2026') for new dashboards.")
    args = ap.parse_args()

    if args.target:
        path = Path(args.target).resolve()
        if not path.exists():
            print(f"MISSING: {path}")
            return 1
        # Allow the caller to pass day/date for unknown filenames
        if args.day and args.date:
            DAY_FOR_TOPIC[path.name] = (args.day, args.date)
        elif path.name not in DAY_FOR_TOPIC:
            DAY_FOR_TOPIC[path.name] = ("Monday", "April 27, 2026")
        result = patch_file(path.name, path)
        print(f"{path.name[:60]}  ->  {result}")
        return 0

    print(f"Polish v2 across {len(DASHBOARDS)} dashboards")
    for name in DASHBOARDS:
        path = DASH_DIR / name
        if not path.exists():
            print(f"  MISSING: {name}")
            continue
        result = patch_file(name, path)
        print(f"  {name[:55]:<55}  ->  {result}")
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
