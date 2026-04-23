#!/usr/bin/env python3
"""
weekly-calendar-builder.py -- Rule 14-compliant weekly calendar dashboard generator.

Takes a calendar JSON (per data-contracts.md schema 3) and emits the HTML
dashboard with all 7 required sections from Rule 14:
  1. Hero
  2. Top Recommendations (full per-criterion scoring visible)
  3. Goal Mix Check
  4. Cut Topics (collapsed, present)
  5. Cross-Topic Conflicts Panel (if any)
  6. Override Capture Panel
  7. Footer

Enforces Rule 14 in code so moving-ahead calendars can't silently drift back
to the pre-streamline format. If required fields are missing from the JSON,
the script raises rather than rendering a misleading dashboard.

Usage:
    python weekly-calendar-builder.py <input-json> <output-html>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_TOP_FIELDS = {"week_of", "generated_at", "goal", "funnel_mix", "topics"}
REQUIRED_TOPIC_FIELDS = {
    "slug", "title", "day", "scheduled_date", "primary_format",
    "funnel_tier", "ghl_keyword", "opportunity_score", "priority_axes",
    "time_decay_band", "justification_notes"
}
REQUIRED_OPP_SCORE_FIELDS = {
    "performance_signal", "search_demand", "audience_intent",
    "competitive_gap", "timeliness", "total", "threshold_status"
}
REQUIRED_PRIORITY_AXES = {"business_priority", "brand_priority", "engagement_priority"}

TIME_DECAY = {
    "breaking_48hr":  {"label": "BREAKING -- 48hr window", "color": "#c62828", "bg": "#FFF0F0"},
    "weekly_window":  {"label": "This week",               "color": "#e65100", "bg": "#FFF4E6"},
    "seasonal_4wk":   {"label": "Seasonal -- 4wk",          "color": "#1565C0", "bg": "#E8F1FB"},
    "evergreen":      {"label": "Evergreen",               "color": "#5a6478", "bg": "#F0F0F2"},
}
THRESHOLD = {
    "must_create": {"label": "must_create", "color": "#2e7d32"},
    "strong":      {"label": "strong",      "color": "#2e7d32"},
    "consider":    {"label": "consider",    "color": "#e65100"},
    "skip":        {"label": "skip",        "color": "#c62828"},
}


def validate(cal):
    missing = REQUIRED_TOP_FIELDS - set(cal.keys())
    if missing:
        raise ValueError("Calendar JSON missing top-level: " + str(missing))
    for i, t in enumerate(cal["topics"]):
        m = REQUIRED_TOPIC_FIELDS - set(t.keys())
        if m:
            raise ValueError("Topic " + str(i) + " (" + t.get("slug","?") + ") missing: " + str(m))
        o = REQUIRED_OPP_SCORE_FIELDS - set(t["opportunity_score"].keys())
        if o:
            raise ValueError("Topic " + str(i) + " opportunity_score missing: " + str(o))
        p = REQUIRED_PRIORITY_AXES - set(t["priority_axes"].keys())
        if p:
            raise ValueError("Topic " + str(i) + " priority_axes missing: " + str(p))
        if t["time_decay_band"] not in TIME_DECAY:
            raise ValueError("Topic " + str(i) + " invalid time_decay_band: " + t["time_decay_band"])


def priority_bar(label, value, color="#C5A258"):
    pct = (value / 5.0) * 100
    return (
        '<div class="pa-row">'
        '<div class="pa-label">' + label + '</div>'
        '<div class="pa-track"><div class="pa-fill" style="width:' + ("%.0f" % pct) + '%;background:' + color + '"></div></div>'
        '<div class="pa-val">' + ("%.1f" % value) + '/5</div>'
        '</div>'
    )


def render_topic_card(t, rank):
    s = t["opportunity_score"]
    pa = t["priority_axes"]
    td = TIME_DECAY[t["time_decay_band"]]
    th = THRESHOLD[s["threshold_status"]]
    weighted = s.get("weighted_total", s["total"])
    weight_note = ""
    if s.get("weighting_applied") and s["weighting_applied"] != "balanced":
        weight_note = ' <span class="tc-weight">(weighted x ' + s["weighting_applied"] + ')</span>'

    override_html = ""
    ov = t.get("user_override")
    if ov:
        override_html = (
            '<div class="tc-override">'
            '<strong>&#x1F4DD; Graeham overrode:</strong> moved from #' + str(ov["original_rank"]) +
            ' &rarr; #' + str(ov["final_rank"]) + '. <em>Reason:</em> ' + ov["reason"] +
            '</div>'
        )

    conflict_html = ""
    if t.get("topic_conflict"):
        cg = t.get("conflict_group", "?")
        conflict_html = (
            '<div class="tc-conflict">'
            '<strong>&#x26A0;&#xFE0F; Topic Conflict (group ' + str(cg) + '):</strong> '
            'Shares pillar+market+angle with another top pick. Pick one or split angles.'
            '</div>'
        )

    card_class = "tc breaking" if t["time_decay_band"] == "breaking_48hr" else "tc"

    crit_rows = ""
    for name, key in [
        ("Performance Signal", "performance_signal"),
        ("Search Demand", "search_demand"),
        ("Audience Intent", "audience_intent"),
        ("Competitive Gap", "competitive_gap"),
        ("Timeliness", "timeliness"),
    ]:
        crit_rows += '<tr><td>' + name + '</td><td class="sc-v">' + str(s[key]) + '/5</td></tr>'

    html = (
        '<div class="' + card_class + '">'
        '<div class="tc-head">'
        '<div class="tc-rank">#' + str(rank) + '</div>'
        '<div class="tc-td" style="background:' + td["bg"] + ';color:' + td["color"] + '">' + td["label"] + '</div>'
        '</div>'
        '<h3 class="tc-title">' + t["title"] + '</h3>'
        '<div class="tc-meta">'
        '<span>' + t["day"] + ' &middot; ' + t["scheduled_date"] + '</span>'
        '<span>' + t["funnel_tier"] + '</span>'
        '<span>' + t["primary_format"] + '</span>'
        '<span>GHL: <code>' + t["ghl_keyword"] + '</code></span>'
        '</div>'
        + override_html
        + conflict_html +
        '<div class="tc-grid">'
        '<div class="tc-score">'
        '<div class="tc-score-h">Opportunity Score</div>'
        '<table class="tc-tbl"><tbody>' + crit_rows + '</tbody>'
        '<tfoot>'
        '<tr class="tc-total"><td><strong>Base Total</strong></td><td class="sc-v"><strong>' + str(s["total"]) + '/25</strong></td></tr>'
        '<tr class="tc-total"><td><strong>Weighted Total</strong>' + weight_note + '</td><td class="sc-v"><strong>' + str(weighted) + '/25</strong></td></tr>'
        '<tr><td>Threshold</td><td class="sc-v" style="color:' + th["color"] + '"><strong>' + th["label"] + '</strong></td></tr>'
        '</tfoot></table></div>'
        '<div class="tc-priority">'
        '<div class="tc-score-h">Priority Axes (readout)</div>'
        + priority_bar("Business", pa["business_priority"], "#1B2A4A")
        + priority_bar("Brand", pa["brand_priority"], "#C5A258")
        + priority_bar("Engagement", pa["engagement_priority"], "#2e7d32")
        + '<div class="tc-td-note">' + t.get("time_decay_note", "") + '</div>'
        '</div></div>'
        '<div class="tc-just"><strong>Why this topic:</strong> ' + t["justification_notes"] + '</div>'
        '</div>'
    )
    return html


def render_goal_mix(cal):
    target = cal["funnel_mix"]
    topics = cal["topics"]
    if not topics:
        return ""
    tiers = [t["funnel_tier"].lower() for t in topics]
    actual = {
        "tofu": tiers.count("tofu") / len(tiers),
        "mofu": tiers.count("mofu") / len(tiers),
        "bofu": tiers.count("bofu") / len(tiers),
    }
    def row(tier):
        tg = target.get(tier, 0)
        ac = actual.get(tier, 0)
        drift = abs(tg - ac) > 0.1
        dn = ' <span style="color:#c62828">(drift &gt;10%)</span>' if drift else ""
        return '<tr><td>' + tier.upper() + '</td><td>' + ("%.0f" % (tg*100)) + '%</td><td>' + ("%.0f" % (ac*100)) + '%' + dn + '</td></tr>'
    return (
        '<h2 class="sh">Goal Mix Check</h2>'
        '<p class="sh-help">Did the selected topics match the Goal Clarifier\'s funnel-mix target?</p>'
        '<table class="mix-tbl">'
        '<thead><tr><th>Tier</th><th>Target</th><th>Actual</th></tr></thead>'
        '<tbody>' + row("tofu") + row("mofu") + row("bofu") + '</tbody>'
        '</table>'
    )


def render_cut_topics(cal):
    cuts = cal.get("cut_topics", [])
    if not cuts:
        return '<h2 class="sh">Cut Topics</h2><p class="sh-help">No topics cut this week.</p>'
    rows = ""
    for c in cuts:
        os = c["opportunity_score"]
        stat = os.get("threshold_status", "skip")
        rows += (
            '<tr>'
            '<td><code>' + c["slug"] + '</code></td>'
            '<td>' + c["title"] + '</td>'
            '<td class="sc-v">' + str(os.get("total","?")) + '/25</td>'
            '<td style="color:' + THRESHOLD.get(stat,{}).get("color","#c62828") + '">' + stat + '</td>'
            '<td>' + c.get("cut_reason","--") + '</td>'
            '</tr>'
        )
    return (
        '<h2 class="sh">Cut Topics (' + str(len(cuts)) + ')</h2>'
        '<p class="sh-help">Scored but didn\'t make top picks. Visible for audit -- nothing silently dropped.</p>'
        '<details class="cut-details" open>'
        '<summary>Expand / collapse cut topics list</summary>'
        '<table class="cut-tbl">'
        '<thead><tr><th>Slug</th><th>Title</th><th>Score</th><th>Status</th><th>Cut Reason</th></tr></thead>'
        '<tbody>' + rows + '</tbody>'
        '</table></details>'
    )


def render_conflicts(cal):
    conflicts = [t for t in cal["topics"] if t.get("topic_conflict")]
    if not conflicts:
        return ""
    groups = {}
    for t in conflicts:
        cg = t.get("conflict_group", 0)
        groups.setdefault(cg, []).append(t)
    rows = ""
    for cg, ts in groups.items():
        titles = "".join(['<li>' + t["title"] + '</li>' for t in ts])
        rows += (
            '<div class="cf-group">'
            '<div class="cf-head">Conflict Group ' + str(cg) + '</div>'
            '<ul>' + titles + '</ul>'
            '<div class="cf-resolve">Resolve by: (a) pick one, (b) split angles, (c) move one to next week</div>'
            '</div>'
        )
    return '<h2 class="sh">&#x26A0;&#xFE0F; Cross-Topic Conflicts</h2><p class="sh-help">Two or more top-pick topics share pillar + market + angle. Resolve before shipping.</p>' + rows


def render_overrides(cal):
    overrides = [(i+1, t) for i, t in enumerate(cal["topics"]) if t.get("user_override")]
    if not overrides:
        return '<h2 class="sh">Graeham\'s Edits</h2><p class="sh-help">No overrides yet -- tell Claude which topics to swap, drop, or add and they\'ll be captured here.</p>'
    rows = ""
    for rank, t in overrides:
        ov = t["user_override"]
        rows += (
            '<div class="ov-row">'
            '<strong>' + t["title"] + '</strong>'
            '<div class="ov-detail">Moved from #' + str(ov["original_rank"]) + ' &rarr; #' + str(ov["final_rank"]) + '. <em>Reason:</em> ' + ov["reason"] + '</div>'
            '</div>'
        )
    return '<h2 class="sh">Graeham\'s Edits (' + str(len(overrides)) + ')</h2><p class="sh-help">Captured overrides. Persist in JSON so next week\'s planner learns preferences.</p><div class="ov-list">' + rows + '</div>'


CSS = """
:root { --navy:#1B2A4A; --gold:#C5A258; --green:#2e7d32; --red:#c62828; --bg:#F7F5EF; --card:#FFFFFF; --border:rgba(27,42,74,0.10); --text:#1B2A4A; --muted:#5a6478; --radius:10px; --shadow:0 1px 3px rgba(27,42,74,0.06); }
*{box-sizing:border-box}
body{background:var(--bg);color:var(--text);font-family:'Plus Jakarta Sans',system-ui,sans-serif;margin:0;padding:32px 24px}
.wrap{max-width:1100px;margin:0 auto}
.hero{background:var(--navy);color:#fff;padding:32px;border-radius:var(--radius);margin-bottom:24px}
.hero h1{margin:0 0 8px;font-size:28px;font-weight:800}
.hero-ey{font-size:11px;text-transform:uppercase;letter-spacing:1.2px;opacity:0.75;margin-bottom:12px}
.hero-meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.hm-pill{background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.18);padding:6px 14px;border-radius:99px;font-size:11px;font-weight:600;color:#fff}
.hm-pill.hero-score{background:var(--gold);color:var(--navy);border-color:var(--gold)}
.sh{font-size:20px;font-weight:700;margin:40px 0 6px;color:var(--navy)}
.sh-help{font-size:13px;color:var(--muted);margin:0 0 16px;line-height:1.6}
.tc{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px;margin-bottom:16px;box-shadow:var(--shadow)}
.tc.breaking{border:2px solid var(--red)}
.tc-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.tc-rank{font-size:12px;font-weight:700;color:var(--muted);letter-spacing:1px}
.tc-td{display:inline-block;padding:4px 12px;border-radius:99px;font-size:10px;font-weight:700;letter-spacing:0.6px;text-transform:uppercase}
.tc-title{margin:8px 0 6px;font-size:18px;font-weight:700;line-height:1.3;color:var(--navy)}
.tc-meta{display:flex;flex-wrap:wrap;gap:10px;font-size:12px;color:var(--muted);margin-bottom:14px}
.tc-meta code{background:rgba(197,162,88,0.15);padding:1px 6px;border-radius:4px;color:var(--navy)}
.tc-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:16px 0}
@media(max-width:900px){.tc-grid{grid-template-columns:1fr}}
.tc-score-h{font-size:11px;font-weight:700;text-transform:uppercase;color:var(--muted);letter-spacing:0.8px;margin-bottom:8px}
.tc-tbl{width:100%;border-collapse:collapse;font-size:13px}
.tc-tbl td{padding:6px 4px;border-bottom:1px solid rgba(27,42,74,0.05)}
.tc-tbl td.sc-v{text-align:right;font-weight:700;color:var(--navy);white-space:nowrap}
.tc-tbl tr.tc-total td{background:rgba(197,162,88,0.06);border-top:2px solid var(--border)}
.tc-weight{font-size:10px;color:var(--gold);font-weight:600}
.tc-just{font-size:13px;color:var(--text);line-height:1.6;padding-top:14px;border-top:1px dashed var(--border);margin-top:4px}
.tc-override{background:rgba(197,162,88,0.12);border:1px solid var(--gold);padding:10px 14px;border-radius:6px;font-size:12px;margin:10px 0;color:var(--navy)}
.tc-conflict{background:rgba(198,40,40,0.08);border:1px solid var(--red);padding:10px 14px;border-radius:6px;font-size:12px;margin:10px 0;color:var(--red)}
.tc-td-note{font-size:11px;color:var(--muted);font-style:italic;margin-top:10px;padding-top:10px;border-top:1px dashed var(--border)}
.pa-row{display:grid;grid-template-columns:100px 1fr 50px;align-items:center;gap:10px;margin:8px 0;font-size:12px}
.pa-label{color:var(--muted);font-weight:600}
.pa-track{background:rgba(27,42,74,0.08);height:8px;border-radius:4px;overflow:hidden}
.pa-fill{height:100%;border-radius:4px;transition:width 0.3s}
.pa-val{text-align:right;font-weight:700;color:var(--navy)}
.mix-tbl,.cut-tbl{width:100%;border-collapse:collapse;font-size:13px;background:var(--card);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow);border:1px solid var(--border)}
.mix-tbl th,.cut-tbl th{background:rgba(27,42,74,0.04);text-align:left;padding:10px 14px;font-weight:700;color:var(--muted);text-transform:uppercase;font-size:11px;letter-spacing:0.6px;border-bottom:1px solid var(--border)}
.mix-tbl td,.cut-tbl td{padding:10px 14px;border-bottom:1px solid rgba(27,42,74,0.05)}
.mix-tbl td.sc-v,.cut-tbl td.sc-v{font-weight:700;color:var(--navy)}
.cut-details summary{cursor:pointer;font-weight:700;color:var(--navy);padding:8px 0}
.cf-group{background:rgba(198,40,40,0.06);border:1px solid var(--red);padding:14px 18px;border-radius:var(--radius);margin-bottom:12px}
.cf-head{font-weight:700;color:var(--red);margin-bottom:6px}
.cf-group ul{margin:6px 0;padding-left:22px;font-size:13px}
.cf-resolve{font-size:12px;color:var(--muted);margin-top:8px;font-style:italic}
.ov-list{display:flex;flex-direction:column;gap:10px}
.ov-row{background:rgba(197,162,88,0.08);border-left:3px solid var(--gold);padding:12px 16px;border-radius:4px;font-size:13px}
.ov-detail{font-size:12px;color:var(--muted);margin-top:4px}
.footer{margin-top:48px;padding:20px 0;border-top:1px solid var(--border);font-size:11px;color:var(--muted);text-align:center;line-height:1.8}
"""


def render_calendar(cal):
    validate(cal)
    n_topics = len(cal["topics"])
    n_cuts = len(cal.get("cut_topics", []))
    goal = cal["goal"]
    week_of = cal["week_of"]
    generated = cal["generated_at"]

    topic_cards = "".join(render_topic_card(t, i + 1) for i, t in enumerate(cal["topics"]))
    fm = cal["funnel_mix"]
    fm_display = str(int(fm["tofu"]*100)) + "/" + str(int(fm["mofu"]*100)) + "/" + str(int(fm["bofu"]*100))

    html = (
        '<!DOCTYPE html><html lang="en"><head>'
        '<meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        '<title>Weekly Content Calendar -- Week of ' + week_of + '</title>'
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap">'
        '<style>' + CSS + '</style></head><body><div class="wrap">'
        '<div class="hero">'
        '<div class="hero-ey">Content Creation Engine &middot; Weekly Calendar v7 &middot; Rule 14 Compliant</div>'
        '<h1>Content Calendar -- Week of ' + week_of + '</h1>'
        '<div class="hero-meta">'
        '<div class="hm-pill hero-score">Goal: ' + goal.replace("_", " ") + '</div>'
        '<div class="hm-pill">' + str(n_topics) + ' topics shipped</div>'
        '<div class="hm-pill">' + str(n_cuts) + ' topics cut</div>'
        '<div class="hm-pill">Funnel mix: ' + fm_display + ' T/M/B</div>'
        '</div></div>'
        '<h2 class="sh">Top Recommendations</h2>'
        '<p class="sh-help">Ranked by weighted Opportunity Score. Every per-criterion breakdown is visible -- no hidden scores per Rule 14. Breaking-news topics render with a red border and auto-pin to Monday/Tuesday regardless of total. Override annotations render with a gold banner; conflict flags with a red banner.</p>'
        + topic_cards
        + render_goal_mix(cal)
        + render_cut_topics(cal)
        + render_conflicts(cal)
        + render_overrides(cal)
        + '<div class="footer">Week of ' + week_of + ' &middot; Goal: ' + goal + ' &middot; Generated ' + generated + '<br>'
        + 'Content Creation Engine v2 (April 2026 streamline) &middot; Rule 14 compliant &middot; Intero Real Estate &middot; DRE #01466876<br>'
        + 'Data sources: Windsor MCP (IG/FB/YT perf, GSC), Apify Reddit (via content-ideation-engine), social-media-analyzer (competitors), web search (market context)'
        + '</div></div></body></html>'
    )
    return html


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    inp = Path(sys.argv[1])
    out = Path(sys.argv[2])
    cal = json.loads(inp.read_text())
    html = render_calendar(cal)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print("Wrote " + str(out) + " (" + str(len(html)) + " bytes, " + str(len(cal["topics"])) + " topics, " + str(len(cal.get("cut_topics",[]))) + " cuts)")


if __name__ == "__main__":
    main()
