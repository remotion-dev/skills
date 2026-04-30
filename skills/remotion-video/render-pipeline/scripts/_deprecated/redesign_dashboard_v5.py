#!/usr/bin/env python3
"""
Dashboard redesign v5 — apply Graeham's feedback to the EPA Two Years prototype.

Changes (in priority order):
  1. Hero reframe — new eyebrow "Monday, April 20 · Recommended Topic",
     video title stays as the star, pills become CLICKABLE with inline
     explanations (Opportunity Score / Funnel / Pillar / GHL Keyword).
  2. Timing card rewritten in plain English.
  3. Fair Housing collapsed to a small pill inside the hero meta, not its
     own section.
  4. "Why This Topic? — The Research" — single collapsed accordion that
     contains Intelligence Stack + Recent Performance + Content Type
     Performance + GSC Top Demand + Opportunity Score Breakdown + Calendar
     Integration. All closed by default so Peter isn't overwhelmed.
  5. 7-Day Posting Calendar gets an explicit clarifier: "These are Peter's
     publish times. He pulls content from the Copy Bank below."
  6. Inline help blocks added to: Shot List (filming guide), Alternate
     Hooks (A/B swap-ins), Power User · Alternate ElevenLabs (voice quality
     upgrade path).

Idempotent via sentinel REDESIGN_V5.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path("/var/tmp/stage3/skills")
DASH_DIR = REPO / "content-calendars"

# Single-dashboard prototype first — we'll propagate after approval.
TARGET = "2026-04-18-epa-two-years-homicide-free-production.html"

SENTINEL = "REDESIGN_V5"

# ---------------------------------------------------------------------------
# CSS additions (appended inside <head> via sentinel check)
# ---------------------------------------------------------------------------

CSS_ADDITIONS = """
<style>
/* REDESIGN_V5_CSS */
.v5-hero { position: relative; padding-bottom: 6px; }
.v5-recommended-label {
  display: inline-block;
  background: #C5A258;
  color: #1B2A4A;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 2px;
  text-transform: uppercase;
  padding: 5px 12px;
  border-radius: 20px;
  margin-bottom: 12px;
}
.v5-hero-sub {
  font-size: 13px;
  color: rgba(255,255,255,0.72);
  margin-top: 6px;
  margin-bottom: 16px;
  line-height: 1.45;
}
.v5-badge {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255,255,255,0.08);
  color: #fff;
  padding: 7px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  margin: 4px 6px 4px 0;
  cursor: help;
  border: 1px solid rgba(255,255,255,0.15);
  transition: background 0.15s;
}
.v5-badge:hover { background: rgba(255,255,255,0.16); }
.v5-badge.score { background: #C5A258; color: #1B2A4A; border-color: #C5A258; }
.v5-badge.pass { background: rgba(46,125,50,0.2); border-color: rgba(46,125,50,0.6); color: #a5d6a7; }
.v5-badge .b-ico { font-size: 11px; opacity: 0.75; }
.v5-badge .b-tooltip {
  display: none;
  position: absolute;
  bottom: calc(100% + 8px);
  left: 0;
  z-index: 50;
  background: #fff;
  color: #1B2A4A;
  padding: 12px 14px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 400;
  line-height: 1.5;
  width: 280px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.25);
  border: 1px solid rgba(27,42,74,0.15);
  white-space: normal;
  text-align: left;
}
.v5-badge .b-tooltip strong { color: #C5A258; font-weight: 700; display: block; margin-bottom: 4px; font-size: 11px; letter-spacing: 1px; text-transform: uppercase; }
.v5-badge:hover .b-tooltip, .v5-badge:focus .b-tooltip { display: block; }
.v5-timing {
  background: #fff;
  border: 1px solid rgba(27,42,74,0.1);
  border-left: 4px solid #C5A258;
  padding: 16px 20px;
  border-radius: 0 10px 10px 0;
  margin: 22px 0 16px 0;
  font-size: 14px;
  line-height: 1.55;
  color: #2d3550;
}
.v5-timing .t-big {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 800;
  color: #1B2A4A;
  font-size: 20px;
  margin-bottom: 4px;
}
.v5-timing .t-math {
  font-size: 11px;
  color: #5a6478;
  margin-top: 6px;
}
.v5-timing code {
  background: rgba(27,42,74,0.06);
  padding: 1px 5px;
  border-radius: 3px;
  font-size: 11px;
}

/* "Why This Topic" accordion */
details.v5-research {
  background: linear-gradient(180deg, #F7F5EF 0%, #FEFCF6 100%);
  border-radius: 14px;
  margin: 24px 0;
  padding: 0;
  border: 1px solid rgba(197,162,88,0.35);
  overflow: hidden;
}
details.v5-research > summary {
  list-style: none;
  cursor: pointer;
  padding: 18px 24px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 800;
  font-size: 15px;
  color: #1B2A4A;
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
}
details.v5-research > summary::-webkit-details-marker { display: none; }
details.v5-research > summary::after {
  content: "+";
  position: absolute;
  right: 24px;
  font-size: 24px;
  color: #C5A258;
  font-weight: 800;
  line-height: 1;
}
details.v5-research[open] > summary::after { content: "−"; }
details.v5-research > summary .v5r-sub {
  font-family: 'DM Sans', sans-serif;
  font-weight: 500;
  font-size: 12px;
  color: #5a6478;
  margin-left: 4px;
}
details.v5-research .v5r-body {
  padding: 8px 24px 24px 24px;
  border-top: 1px solid rgba(197,162,88,0.25);
}

/* Posting calendar clarifier */
.v5-cal-clarifier {
  background: #EEF2FF;
  border-left: 4px solid #3b4f99;
  padding: 14px 18px;
  border-radius: 0 8px 8px 0;
  margin: 10px 0 18px 0;
  font-size: 13px;
  color: #1f2d5c;
  line-height: 1.55;
}
.v5-cal-clarifier strong { color: #1B2A4A; }

/* Format panel help blocks */
.v5-inline-help {
  background: #F7F5EF;
  border-left: 3px solid #C5A258;
  padding: 10px 14px;
  border-radius: 0 6px 6px 0;
  font-size: 12px;
  color: #3a4358;
  line-height: 1.5;
  margin: 10px 0;
}
.v5-inline-help strong { color: #1B2A4A; }
</style>
"""

# ---------------------------------------------------------------------------
# Replacement 1 — new hero block
# ---------------------------------------------------------------------------

NEW_HERO = """<div class="hero v5-hero">
  <div class="v5-recommended-label">&#x1F4C5; Monday, April 20, 2026 &middot; Recommended Topic</div>
  <h1>East Palo Alto Just Hit 2 Years Without a Homicide &mdash; And It's Changing Peninsula Home Prices</h1>
  <div class="v5-hero-sub">A counter-narrative content package built from the April 17, 2026 milestone announcement, cross-referenced against EPA MLS data (+1.7% YoY, DOM cut in half) and Peninsula-wide fragmentation (SMC &ndash;7.2% YoY).</div>

  <div class="hero-meta" style="margin-top:14px">
    <span class="v5-badge score" tabindex="0">
      &starf; 10/10 Opportunity
      <span class="b-tooltip"><strong>Opportunity Score</strong>How strong this topic is on a 10-point scale. Built from four sub-scores: Timeliness (3) + Audience Relevance (3) + Content Gap (2) + Engagement Potential (2) = 10. See the "Why This Topic?" accordion for the full breakdown.</span>
    </span>
    <span class="v5-badge" tabindex="0">
      &#x1F3AF; Funnel: MOFU &rarr; BOFU
      <span class="b-tooltip"><strong>Funnel Stage</strong>TOFU = top (awareness/discovery), MOFU = middle (consideration), BOFU = bottom (ready to act). This topic hooks MOFU buyers reassessing EPA, then drops a BOFU CMA CTA for sellers.</span>
    </span>
    <span class="v5-badge" tabindex="0">
      &#x1F3DB; Pillar 5 + 4
      <span class="b-tooltip"><strong>Content Pillar</strong>Which of your 5 content pillars this topic serves. Pillar 5 = Community / Local Stories. Pillar 4 = Market Intelligence. Cross-pillar topics (like this one) perform best because they reach both buyer and seller audiences.</span>
    </span>
    <span class="v5-badge" tabindex="0">
      &#x1F517; GHL Keyword: EPA
      <span class="b-tooltip"><strong>GoHighLevel Comment Trigger</strong>The word viewers comment on IG/FB to auto-enter the follow-up sequence. "EPA" = the campaign tag that tracks leads from this topic specifically, so you can measure which pieces are converting.</span>
    </span>
    <span class="v5-badge pass" tabindex="0">
      &#x2705; Fair Housing OK
      <span class="b-tooltip"><strong>Fair Housing Compliance</strong>Passed. Homicide data is framed as statistics plus community policy shift, not neighborhood character. No demographic references, no coded language, no school rankings.</span>
    </span>
  </div>

  <div class="v5-timing">
    <div class="t-big">&#x1F3AC; Target video length: ~4 minutes 30 seconds</div>
    <div>Based on a verified count of 573 spoken words in the YT Long script.</div>
    <div class="t-math">Math: <code>573 words &divide; 150 WPM &times; 1.15 pause/B-roll buffer = 4.39 min</code>. Not a generic estimate.</div>
  </div>

  <div class="pow">Generated April 18, 2026 &middot; Content Creation Engine v5 &middot; Intero Real Estate &middot; DRE #01466876</div>
</div>"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(msg: str) -> None:
    print(msg)


def wrap_research_accordion(html: str) -> str:
    """
    Wrap Intelligence Stack through Calendar Integration (or whatever is the
    last research block before the 7-Day Posting Calendar) inside a single
    collapsed accordion.
    """
    if "V5_RESEARCH_ACCORDION" in html:
        return html

    # Find the start — the Intelligence Stack h2
    start_m = re.search(r'<h2 class="sh">[^<]*Intelligence Stack', html)
    if not start_m:
        log("  [research] could not locate Intelligence Stack start — skipping")
        return html

    # Find the end — right before the 7-Day Posting Calendar h2
    end_m = re.search(r'<h2 class="sh">[^<]*7-Day Posting Calendar', html)
    if not end_m:
        log("  [research] could not locate 7-Day Posting Calendar — skipping")
        return html

    start = start_m.start()
    end = end_m.start()

    before = html[:start]
    section = html[start:end]
    after = html[end:]

    wrapped = (
        '<!-- V5_RESEARCH_ACCORDION -->\n'
        '<details class="v5-research">\n'
        '  <summary>&#x1F4CA; Why This Topic? &mdash; The Research <span class="v5r-sub">(click to expand &middot; 8 data sources + scoring + calendar context)</span></summary>\n'
        '  <div class="v5r-body">\n'
        + section
        + '\n  </div>\n'
        '</details>\n'
    )

    return before + wrapped + after


def add_calendar_clarifier(html: str) -> str:
    """Add Peter-facing clarifier above the 7-Day Posting Calendar grid."""
    if "V5_CAL_CLARIFIER" in html:
        return html

    clarifier = (
        '<!-- V5_CAL_CLARIFIER -->\n'
        '<div class="v5-cal-clarifier">\n'
        '  <strong>Who does what, when:</strong> These are the times <strong>Peter publishes</strong> each format to its platform. He pulls the finished content from the Copy Bank below or from each format panel. Times are based on your actual IG data (top posts land 6&ndash;9am and 5&ndash;8pm). Click any day card to jump to that format.\n'
        '</div>\n'
    )

    # Insert right after the section-help <p> that follows the 7-Day Posting Calendar h2
    pattern = re.compile(
        r'(<h2 class="sh">[^<]*7-Day Posting Calendar[^<]*</h2>\s*<p class="section-help">[^<]*(?:<[^<]+)*?</p>)',
        re.DOTALL,
    )
    m = pattern.search(html)
    if not m:
        log("  [cal-clarifier] could not locate 7-Day section intro — skipping")
        return html

    return html[:m.end()] + '\n' + clarifier + html[m.end():]


def add_inline_help(html: str) -> str:
    """Add inline help blocks to: Shot List, Alternate Hooks, Power User ElevenLabs."""
    changed = False

    # Shot List — actual heading is <h2 class="sh">Shot List &mdash; Hand to Peter and John</h2>
    if "V5_HELP_SHOTLIST" not in html:
        shotlist_help = (
            '<div class="v5-inline-help"><!-- V5_HELP_SHOTLIST --><strong>What a Shot List is:</strong> The filming guide for when you or a crew shoots b-roll or a live human-filmed version. It changes per format because IG Reels / TikTok need 9:16 vertical framing, YT Long needs 16:9 landscape, and YT Short needs 9:16 with tighter pacing. If you\'re rendering entirely via HeyGen avatar, you can ignore the shot list &mdash; it\'s for manual production only.</div>'
        )
        html = re.sub(
            r'(<h2[^>]*>\s*(?:&[#\w]+;\s*)?Shot List[^<]*</h2>)',
            r'\1\n' + shotlist_help,
            html,
            count=1,
            flags=re.IGNORECASE,
        )
        if "V5_HELP_SHOTLIST" in html:
            changed = True

    # Alternate Hooks
    if "V5_HELP_HOOKS" not in html:
        hooks_help = (
            '<div class="v5-inline-help"><!-- V5_HELP_HOOKS --><strong>What Alternate Hooks are:</strong> Three swap-in opening lines for A/B testing. If the primary hook underperforms 48 hours after posting (reach below your 2,125/wk IG average), re-upload with one of these swapped into the first 3 seconds. The hooks change per topic because they\'re written specifically to pair with the topic\'s emotional beat.</div>'
        )
        html = re.sub(
            r'(<h[23][^>]*>\s*(?:&[#\w]+;\s*)?\d*\s*Alternate Hooks[^<]*</h[23]>)',
            r'\1\n' + hooks_help,
            html,
            count=1,
            flags=re.IGNORECASE,
        )
        if "V5_HELP_HOOKS" in html:
            changed = True

    # Power-User Alternative: ElevenLabs + HeyGen Pipeline — actual heading
    # is <h3>&#x1F680; Power-User Alternative: ElevenLabs + HeyGen Pipeline (Optional)</h3>
    if "V5_HELP_ELEVEN" not in html:
        eleven_help = (
            '<div class="v5-inline-help"><!-- V5_HELP_ELEVEN --><strong>When to use this:</strong> HeyGen\'s built-in voice clone is great for 90% of your content, but for high-stakes videos (the YT Long, paid ads, sponsored content) you may want studio-grade voice. Use this path: (1) render the HeyGen avatar <em>without</em> audio, (2) generate the voiceover separately in ElevenLabs using your trained voice and this SSML script, (3) stitch audio + video in your editor. Trade-off: noticeably better voice quality for ~15 extra minutes of editing. Skip this for social-first content &mdash; HeyGen voice is fine there.</div>'
        )
        html = re.sub(
            r'(<h[23][^>]*>\s*(?:&[#\w]+;\s*)?Power-?User[^<]*ElevenLabs[^<]*</h[23]>)',
            r'\1\n' + eleven_help,
            html,
            count=1,
            flags=re.IGNORECASE,
        )
        if "V5_HELP_ELEVEN" in html:
            changed = True

    return html


# ---------------------------------------------------------------------------
# Main patch
# ---------------------------------------------------------------------------

def patch_file(path: Path) -> str:
    html = path.read_text(encoding="utf-8")

    if SENTINEL in html:
        return "skip (already v5)"

    # 1. Inject CSS additions (before </head>)
    if "REDESIGN_V5_CSS" not in html:
        html = html.replace("</head>", CSS_ADDITIONS + "\n</head>", 1)

    # 2. Replace the existing hero + its immediately-following how-to / timing /
    #    fair-housing blocks with the new hero. We locate the existing
    #    <div class="hero">...</div> and the two blocks after it.
    hero_pat = re.compile(
        r'<div class="hero">.*?</div>\s*</div>\s*<div class="data-toggle-wrap">',
        re.DOTALL,
    )
    # More forgiving: capture the hero div and its closing, up to the end of
    # the Fair Housing comp block.
    old_top = re.compile(
        r'<div class="hero">.*?(?=<div class="data-toggle-wrap">)',
        re.DOTALL,
    )
    # Simpler: just the hero div itself + how-to + timing + comp.
    top_block = re.compile(
        r'<div class="hero">.*?<div class="comp">.*?</div>\s*</div>',
        re.DOTALL,
    )
    m = top_block.search(html)
    if not m:
        # Fallback — replace just the hero
        hero_only = re.search(r'<div class="hero">.*?</div>\s*(?=\n|<div)', html, re.DOTALL)
        if hero_only:
            html = html[:hero_only.start()] + NEW_HERO + html[hero_only.end():]
        else:
            log("  [hero] could not locate hero block — skipping")
    else:
        html = html[:m.start()] + NEW_HERO + html[m.end():]

    # 3. Remove the now-orphaned how-to, timing-card, and comp blocks that
    #    may still be loose (if the top_block regex was partial). Our new
    #    hero already contains timing + fair-housing pill.
    for orphan_pat in [
        r'<div class="how-to">.*?</div>\s*</ol>\s*</div>',
        r'<div class="how-to">.*?</ol>\s*</div>',
        r'<div class="timing-card">.*?</div>\s*</div>',
        r'<div class="comp">.*?</div>\s*</div>',
    ]:
        html = re.sub(orphan_pat, '', html, count=1, flags=re.DOTALL)

    # 4. Wrap research sections in collapsed accordion
    html = wrap_research_accordion(html)

    # 5. Add 7-Day Calendar clarifier
    html = add_calendar_clarifier(html)

    # 6. Add inline help blocks
    html = add_inline_help(html)

    # 7. Sentinel — use rsplit so we insert before the REAL </body>, not the
    #    </body> that lives inside the CONTENT_LIBRARY JS string.
    parts = html.rsplit("</body>", 1)
    if len(parts) == 2:
        html = parts[0] + f"<!-- {SENTINEL} -->\n</body>" + parts[1]

    path.write_text(html, encoding="utf-8")
    return "redesigned"


def main() -> int:
    path = DASH_DIR / TARGET
    if not path.exists():
        log(f"MISSING: {path}")
        return 1
    result = patch_file(path)
    log(f"{TARGET} -> {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
