#!/usr/bin/env python3
"""
switchy_dashboard.py  —  unified Switchy clicks dashboard
=========================================================
Pulls every link's click count from the Switchy GraphQL API, groups by the link's
Switchy FOLDER (= traffic source: postcards, GMB, YouTube, yard signs, ads, ...),
snapshots for week-over-week deltas, and renders ONE branded HTML dashboard for
all Switchy clicks.

WHY GROUP BY FOLDER: the Switchy API exposes only a running `clicks` total per link
(no referrer/geo/device/time-series). But the folder a link lives in already encodes
its source, so folder-level grouping answers "where are the clicks coming from?"
even for links that were never tagged. Tags refine this further when present.

WEEK-OVER-WEEK: the API has no history, so we snapshot all click counts to a dated
JSON each run and diff against the most recent prior snapshot. First run = baseline
(deltas show from run #2 onward).

USAGE
-----
  export SWITCHY_API_TOKEN=...      # or ~/.switchy/token
  python switchy_dashboard.py --outdir <dir> [--snapdir <dir>]

Writes: <outdir>/index.html  and  <snapdir>/switchy-snapshot-YYYY-MM-DD.json
"""
import os, sys, json, argparse, urllib.request, urllib.error, glob
from pathlib import Path
from datetime import datetime, date

GRAPHQL = "https://graphql.switchy.io/v1/graphql"
MODEL = {"pixel_match_rate": 0.55, "frequency": 10, "cpm": 22.0,
         "min_audience": 100, "efficient_audience": 1000, "window_days": 30}
GOLD, INK, CREAM = "#C2A14E", "#1A1D2E", "#FBF7EC"


def token():
    t = os.environ.get("SWITCHY_API_TOKEN")
    if t:
        return t.strip()
    for p in (Path.home()/".switchy"/"token", Path(".switchy_token")):
        if p.exists():
            return p.read_text().strip()
    sys.exit("No SWITCHY_API_TOKEN found (env or ~/.switchy/token).")


def gql(q, tok):
    req = urllib.request.Request(GRAPHQL, data=json.dumps({"query": q}).encode(),
                                 headers={"Content-Type": "application/json",
                                          "Api-Authorization": tok}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read().decode())
    if "errors" in d:
        sys.exit("GraphQL error: " + json.dumps(d["errors"])[:400])
    return d["data"]


def audience(clicks):
    return int(round(clicks * MODEL["pixel_match_rate"]))


def budget(aud):
    if aud < MODEL["min_audience"]:
        return 0.0
    return round(aud * MODEL["frequency"] / 1000.0 * MODEL["cpm"], 0)


def load_prior(snapdir):
    files = sorted(glob.glob(os.path.join(snapdir, "switchy-snapshot-*.json")))
    if not files:
        return None, None
    f = files[-1]
    try:
        return json.load(open(f)), os.path.basename(f)
    except Exception:
        return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--snapdir", default=None)
    a = ap.parse_args()
    outdir = a.outdir
    snapdir = a.snapdir or os.path.join(outdir, "snapshots")
    Path(outdir).mkdir(parents=True, exist_ok=True)
    Path(snapdir).mkdir(parents=True, exist_ok=True)

    tok = token()
    data = gql("{ links(order_by:{clicks:desc}){ id domain url title tags clicks folderId } "
               "folders { id name } }", tok)
    links = data["links"]
    fname = {f["id"]: f["name"].strip() for f in data["folders"]}

    # snapshot
    today = date.today().isoformat()
    snap = {"date": today, "clicks": {l["id"]: l["clicks"] for l in links}}
    prior, prior_name = load_prior(snapdir)
    json.dump(snap, open(os.path.join(snapdir, f"switchy-snapshot-{today}.json"), "w"))

    def delta(lid, cur):
        if not prior:
            return None
        return cur - prior["clicks"].get(lid, 0)

    # group by folder (= source)
    groups = {}
    tot_clicks = tot_aud = tot_bud = tot_delta = 0
    for l in links:
        src = fname.get(l["folderId"], "Unfiled / no source tag")
        g = groups.setdefault(src, {"clicks": 0, "links": 0, "delta": 0, "rows": []})
        g["clicks"] += l["clicks"]; g["links"] += 1
        d = delta(l["id"], l["clicks"])
        if d:
            g["delta"] += d; tot_delta += d
        g["rows"].append(l)
        tot_clicks += l["clicks"]
    for s, g in groups.items():
        g["aud"] = audience(g["clicks"]); g["bud"] = budget(g["aud"])
        tot_aud += g["aud"]
    tot_bud = budget(tot_aud)
    ranked = sorted(groups.items(), key=lambda kv: kv[1]["clicks"], reverse=True)

    # top links
    top = links[:15]

    # ---- render ----
    def fmt(n):
        return f"{n:,}"
    week_note = (f"vs. {prior['date']} ({prior_name})" if prior
                 else "baseline — week-over-week deltas begin next run")
    src_labels = json.dumps([s for s, _ in ranked])
    src_clicks = json.dumps([g["clicks"] for _, g in ranked])

    rows_src = "\n".join(
        f"<tr><td>{s}</td><td class=n>{fmt(g['links'])}</td><td class=n>{fmt(g['clicks'])}</td>"
        f"<td class=n>{('+' if g['delta']>0 else '')+fmt(g['delta']) if prior else '—'}</td>"
        f"<td class=n>{fmt(g['aud'])}</td><td class=n>${fmt(int(g['bud']))}</td></tr>"
        for s, g in ranked)

    rows_top = "\n".join(
        f"<tr><td>{(l['title'] or l['id'])[:46]}</td>"
        f"<td>{fname.get(l['folderId'],'—')}</td>"
        f"<td class=mono>{l['domain']}/{l['id']}</td>"
        f"<td class=n>{fmt(l['clicks'])}</td>"
        f"<td class=n>{('+' if (delta(l['id'],l['clicks']) or 0)>0 else '')+fmt(delta(l['id'],l['clicks'])) if prior else '—'}</td></tr>"
        for l in top)

    html = f"""<!DOCTYPE html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Switchy Clicks Dashboard — Graeham Watts</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
:root{{--gold:{GOLD};--ink:{INK};--cream:{CREAM}}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:#f4f5f7;color:var(--ink);padding:28px;max-width:1100px;margin:0 auto}}
h1{{font-size:26px;letter-spacing:-.01em}}
.sub{{color:#667;margin:4px 0 22px;font-size:14px}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:24px}}
.kpi{{background:#fff;border-radius:14px;padding:18px 20px;box-shadow:0 1px 3px rgba(0,0,0,.08);border-top:3px solid var(--gold)}}
.kpi .v{{font-size:30px;font-weight:800}}
.kpi .l{{font-size:12px;color:#778;text-transform:uppercase;letter-spacing:.05em;margin-top:2px}}
.card{{background:#fff;border-radius:14px;padding:20px 22px;box-shadow:0 1px 3px rgba(0,0,0,.08);margin-bottom:22px}}
.card h2{{font-size:16px;margin-bottom:14px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th,td{{text-align:left;padding:9px 10px;border-bottom:1px solid #eef0f3}}
th{{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:#889}}
td.n{{text-align:right;font-variant-numeric:tabular-nums}}
td.mono{{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:#557}}
tr:last-child td{{border-bottom:none}}
.foot{{color:#889;font-size:12px;margin-top:8px;line-height:1.5}}
.badge{{display:inline-block;background:var(--gold);color:#fff;font-size:11px;font-weight:700;padding:2px 9px;border-radius:99px}}
</style></head><body>
<h1>Switchy Clicks Dashboard <span class=badge>ALL SOURCES</span></h1>
<div class=sub>Generated {datetime.now():%Y-%m-%d %H:%M} · {week_note} · model: 55% match · {MODEL['frequency']}×/30d · ${int(MODEL['cpm'])} CPM</div>

<div class=kpis>
  <div class=kpi><div class=v>{fmt(tot_clicks)}</div><div class=l>Total clicks / scans</div></div>
  <div class=kpi><div class=v>{('+'+fmt(tot_delta)) if prior else '—'}</div><div class=l>New this week</div></div>
  <div class=kpi><div class=v>{fmt(tot_aud)}</div><div class=l>Targetable audience</div></div>
  <div class=kpi><div class=v>${fmt(int(tot_bud))}</div><div class=l>Justified ad budget / mo</div></div>
</div>

<div class=card>
  <h2>Where the clicks come from (by Switchy folder)</h2>
  <canvas id=srcChart height=110></canvas>
</div>

<div class=card>
  <h2>Sources breakdown</h2>
  <table>
    <tr><th>Source (folder)</th><th class=n>Links</th><th class=n>Clicks</th><th class=n>New/wk</th><th class=n>Audience</th><th class=n>Budget/mo</th></tr>
    {rows_src}
    <tr style="font-weight:800;border-top:2px solid var(--ink)"><td>TOTAL</td><td class=n>{fmt(len(links))}</td><td class=n>{fmt(tot_clicks)}</td><td class=n>{('+'+fmt(tot_delta)) if prior else '—'}</td><td class=n>{fmt(tot_aud)}</td><td class=n>${fmt(int(tot_bud))}</td></tr>
  </table>
</div>

<div class=card>
  <h2>Top 15 links</h2>
  <table>
    <tr><th>Link</th><th>Source</th><th>Short URL</th><th class=n>Clicks</th><th class=n>New/wk</th></tr>
    {rows_top}
  </table>
</div>

<div class=foot>
  <b>How to read this:</b> <i>Audience</i> = clicks that resolve to a targetable pixeled user (55%). <i>Budget/mo</i> = what that audience can absorb at {MODEL['frequency']}×/30d, ${int(MODEL['cpm'])} CPM — a ceiling, not a target. Sources are the Switchy folders each link lives in; "Unfiled" links need a folder/tag to be attributable. Switchy's API gives click totals only — geo/referrer/device live in GA4 (via UTM) and Meta (via pixel).
</div>

<script>
new Chart(document.getElementById('srcChart'),{{type:'bar',
 data:{{labels:{src_labels},datasets:[{{label:'Clicks',data:{src_clicks},backgroundColor:'{GOLD}'}}]}},
 options:{{plugins:{{legend:{{display:false}}}},scales:{{y:{{beginAtZero:true}}}}}}}});
</script>
</body></html>"""

    out = os.path.join(outdir, "index.html")
    Path(out).write_text(html, encoding="utf-8")
    print(f"[dashboard] {out}")
    print(f"[totals] clicks={tot_clicks} audience={tot_aud} budget=${int(tot_bud)} sources={len(groups)} links={len(links)}")
    print(f"[snapshot] {os.path.join(snapdir, f'switchy-snapshot-{today}.json')} (prior: {prior_name or 'none'})")


if __name__ == "__main__":
    main()
