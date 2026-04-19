#!/usr/bin/env python3
"""Dashboard v4: dual-button (Content + Prompt) + Full Research Data expandable panel.
Loads PROMPTS from v2 source and CONTENT from generated_content.py."""
import json, sys
from pathlib import Path

sys.path.insert(0, '/sessions/inspiring-gracious-volta/mnt/outputs')

# Load prompts via v2 script (run top part only — stop before panel building)
v2_src = open('/sessions/inspiring-gracious-volta/mnt/outputs/build_dashboard_v2.py').read()
v2_src_trimmed = v2_src.split("# Build panels")[0]
v2_ns = {}
exec(v2_src_trimmed, v2_ns)
PROMPTS = v2_ns['PROMPTS']
FORMAT_META = v2_ns['FORMAT_META']

# Load generated content
gc_src = open('/sessions/inspiring-gracious-volta/mnt/outputs/generated_content.py').read()
gc_ns = {}
exec(gc_src, gc_ns)
CONTENT = gc_ns['CONTENT']

print(f"Loaded {len(PROMPTS)} prompts, {len(CONTENT)} content pieces, {len(FORMAT_META)} metas")

# Pairing map: some formats have a "companion" format that's usually grabbed together
# Voice/text side paired with Production/editing side, etc.
PAIRINGS = {
    "yt-long-pt1": ("yt-long-pt2", "Copy Production Content", "B-roll prompts + Editing notes for Jason + AI video prompts (Seedance) + YouTube SEO + 3 alt hooks. Everything non-voice that the production team needs for this video."),
}

# Build panels
panels_html = []
for key, (label, meta, use_in) in FORMAT_META.items():
    is_active = " active" if key == "yt-long-pt1" else ""
    preview = CONTENT[key][:600].replace('<', '&lt;').replace('>', '&gt;')
    pchars = len(PROMPTS[key])
    cchars = len(CONTENT[key])

    # Optional paired button for voice + production pairing
    pair_block = ""
    if key in PAIRINGS:
        pair_key, pair_label, pair_desc = PAIRINGS[key]
        pair_content_chars = len(CONTENT[pair_key])
        pair_block = (
            '    <div class="pair-section">\n'
            '      <div class="cs-h" style="color:var(--purple)">Also Grab: Production Content (for Jason/production team)</div>\n'
            '      <div class="pair-desc">' + pair_desc + '</div>\n'
            '      <div class="button-row" style="margin-top:10px">\n'
            '        <button class="copy-big" style="background:var(--purple);color:#fff;box-shadow:0 2px 8px rgba(106,27,154,0.25)" onclick="copyContent(this,\'' + pair_key + '\')">' + pair_label + '</button>\n'
            '        <span class="char-meta">' + f"{pair_content_chars:,}" + ' chars</span>\n'
            '      </div>\n'
            '    </div>\n'
        )

    panel = (
        '<div class="deriv-panel' + is_active + '" id="panel-' + key + '">\n'
        '  <div class="prompt-card">\n'
        '    <div class="pc-h"><div class="pc-label">' + label + '</div><div class="pc-meta">' + meta + '</div></div>\n'
        '    <div class="content-section">\n'
        '      <div class="cs-h">Production Content (ready to post)</div>\n'
        '      <div class="content-preview">' + preview + '\n\n(Full content loaded - click Copy Content to grab the complete deliverable.)</div>\n'
        '      <div class="button-row">\n'
        '        <button class="copy-big" onclick="copyContent(this,\'' + key + '\')">Copy Content</button>\n'
        '        <span class="char-meta">Full content: ' + f"{cchars:,}" + ' chars</span>\n'
        '      </div>\n'
        '    </div>\n' +
        pair_block +
        '    <div class="regenerate-section">\n'
        '      <div class="regen-h">Need to regenerate? Copy the prompt to rerun through your AI:</div>\n'
        '      <div class="button-row">\n'
        '        <button class="copy-outline" onclick="copyPrompt(this,\'' + key + '\')">Copy Prompt</button>\n'
        '        <span class="char-meta">Prompt: ' + f"{pchars:,}" + ' chars</span>\n'
        '      </div>\n'
        '    </div>\n'
        '    <div class="use-in"><strong>How to use:</strong> ' + use_in + '</div>\n'
        '  </div>\n'
        '</div>'
    )
    panels_html.append(panel)

# Flow cards
flow_cards = []
for key, (label, meta, _) in FORMAT_META.items():
    active_cls = " core active" if key == "yt-long-pt1" else ""
    short_label = label.split(" - ")[0]
    short_title = label.split(" - ")[1] if " - " in label else meta.split(".")[0]
    if key == "production-brief":
        tag = '<div class="fc-tag" style="background:#f3e5f5;color:#6a1b9a">Crew+Edit</div>'
    elif key.startswith("yt-"):
        v = "~4:30" if key == "yt-long-pt1" else ("Edit+SEO" if key == "yt-long-pt2" else "~30s")
        tag = '<div class="fc-tag tag-yt">' + v + '</div>'
    elif key.startswith("ig-"):
        v = "~30s" if key == "ig-reel-1" else ("~20s" if key == "ig-reel-2" else "4:5")
        tag = '<div class="fc-tag tag-ig">' + v + '</div>'
    elif key == "tiktok":
        tag = '<div class="fc-tag tag-tk">~30s</div>'
    elif key == "blog":
        tag = '<div class="fc-tag tag-blog">AEO</div>'
    elif key == "gmb":
        tag = '<div class="fc-tag tag-gmb">250w</div>'
    elif key == "facebook":
        tag = '<div class="fc-tag tag-fb">200-400w</div>'
    elif key == "linkedin":
        tag = '<div class="fc-tag" style="background:#e3f2fd;color:#0077B5">300-500w</div>'
    elif key == "ad-copy":
        tag = '<div class="fc-tag" style="background:#fff3e0;color:#e65100">Paid</div>'
    elif key == "email":
        tag = '<div class="fc-tag tag-blog">Lead 400w</div>'
    elif key == "full-newsletter":
        tag = '<div class="fc-tag" style="background:#e0f2f1;color:#00695c">Full 7-sec</div>'
    else:
        tag = '<div class="fc-tag">Format</div>'
    card = (
        '<div class="flow-card' + active_cls + '" data-target="' + key + '">'
        '<div class="fc-type">' + short_label + '</div>'
        '<div class="fc-title">' + short_title + '</div>'
        + tag + '</div>'
    )
    flow_cards.append(card)

FLOW = "\n  ".join(flow_cards)
PANELS = "\n".join(panels_html)
PLIB = json.dumps(PROMPTS)
CLIB = json.dumps(CONTENT)

# ============================================================
# RESEARCH DATA HTML (static, pre-populated with actual pulled data)
# ============================================================
RESEARCH_DATA_HTML = """
<div class="data-toggle-wrap">
  <button class="data-toggle" onclick="toggleResearchData()">Show Full Research Data</button>
</div>

<div class="research-data" id="research-data">
  <div class="data-section">
    <h3>&#x1F50D; Google Search Console &mdash; Top Queries (Last 7 Days)</h3>
    <div class="ds-note">Source: Windsor MCP / searchconsole / sc-domain:graehamwatts.com. 87 queries total; showing top 25 by impressions. Only "graeham watts" branded query produced clicks (8). The rest are impressions-only &mdash; significant traffic opportunity gap.</div>
    <table class="data-table">
      <thead><tr><th>Query</th><th class="num">Clicks</th><th class="num">Impr</th><th class="num">CTR</th><th class="num">Pos</th></tr></thead>
      <tbody>
        <tr class="highlight"><td>graeham watts</td><td class="num">8</td><td class="num">12</td><td class="num">66.67%</td><td class="num">1.0</td></tr>
        <tr><td>east palo alto ca real estate</td><td class="num">0</td><td class="num">10</td><td class="num">0%</td><td class="num">20.5</td></tr>
        <tr><td>are smoke detectors required when selling a house</td><td class="num">0</td><td class="num">7</td><td class="num">0%</td><td class="num">13.7</td></tr>
        <tr><td>east palo alto ca homes for sale</td><td class="num">0</td><td class="num">7</td><td class="num">0%</td><td class="num">24.1</td></tr>
        <tr><td>east palo alto real estate</td><td class="num">0</td><td class="num">7</td><td class="num">0%</td><td class="num">27.9</td></tr>
        <tr><td>palo alto ca houses for sale</td><td class="num">0</td><td class="num">7</td><td class="num">0%</td><td class="num">37.6</td></tr>
        <tr><td>palo alto ca real estate</td><td class="num">0</td><td class="num">7</td><td class="num">0%</td><td class="num">42.9</td></tr>
        <tr><td>east palo alto ca houses for sale</td><td class="num">0</td><td class="num">6</td><td class="num">0%</td><td class="num">17.2</td></tr>
        <tr><td>east palo alto ca new construction for sale</td><td class="num">0</td><td class="num">6</td><td class="num">0%</td><td class="num">29.5</td></tr>
        <tr><td>east palo alto ca new homes for sale</td><td class="num">0</td><td class="num">6</td><td class="num">0%</td><td class="num">24.8</td></tr>
        <tr><td>east palo alto realtor</td><td class="num">0</td><td class="num">6</td><td class="num">0%</td><td class="num">17.5</td></tr>
        <tr><td>find your dream home menlo park ca</td><td class="num">0</td><td class="num">6</td><td class="num">0%</td><td class="num">32.3</td></tr>
        <tr><td>palo alto ca homes for sale</td><td class="num">0</td><td class="num">6</td><td class="num">0%</td><td class="num">42.0</td></tr>
        <tr><td>redwood city ca real estate</td><td class="num">0</td><td class="num">6</td><td class="num">0%</td><td class="num">49.5</td></tr>
        <tr><td>east palo alto homes for sale</td><td class="num">0</td><td class="num">5</td><td class="num">0%</td><td class="num">23.2</td></tr>
        <tr><td>palo alto real estate agents</td><td class="num">0</td><td class="num">5</td><td class="num">0%</td><td class="num">26.4</td></tr>
        <tr><td>redwood city ca new homes for sale</td><td class="num">0</td><td class="num">5</td><td class="num">0%</td><td class="num">48.4</td></tr>
        <tr><td>redwood city homes for sale</td><td class="num">0</td><td class="num">5</td><td class="num">0%</td><td class="num">43.4</td></tr>
        <tr><td>we buy houses palo alto california</td><td class="num">0</td><td class="num">5</td><td class="num">0%</td><td class="num">70.2</td></tr>
        <tr><td>houses for sale in east palo alto</td><td class="num">0</td><td class="num">4</td><td class="num">0%</td><td class="num">17.8</td></tr>
        <tr><td>palo alto real estate agent</td><td class="num">0</td><td class="num">4</td><td class="num">0%</td><td class="num">22.5</td></tr>
        <tr><td>centennial neighborhood bay area</td><td class="num">0</td><td class="num">3</td><td class="num">0%</td><td class="num">1.0</td></tr>
        <tr><td>east palo alto ca open houses</td><td class="num">0</td><td class="num">3</td><td class="num">0%</td><td class="num">27.3</td></tr>
        <tr><td>smoke alarms in houses</td><td class="num">0</td><td class="num">3</td><td class="num">0%</td><td class="num">50.0</td></tr>
        <tr><td>...smoke detector cluster (15+ queries)</td><td class="num">0</td><td class="num">35+</td><td class="num">0%</td><td class="num">34-76</td></tr>
      </tbody>
    </table>
  </div>

  <div class="data-section">
    <h3>&#x1F4F1; Instagram Performance &mdash; Last 30 Days</h3>
    <div class="ds-note">Source: Windsor MCP / Instagram / graeham.watts. 48 rows; top 12 by reach shown. Pattern: Reels dominate, top posts drive 10-23 shares, saves max 4 &mdash; content isn't reference-worthy yet.</div>
    <table class="data-table">
      <thead><tr><th>Date</th><th>Type</th><th class="num">Reach</th><th class="num">Likes</th><th class="num">Comments</th><th class="num">Saves</th><th class="num">Shares</th></tr></thead>
      <tbody>
        <tr class="highlight"><td>2026-03-24</td><td>Post</td><td class="num">1,503</td><td class="num">15</td><td class="num">1</td><td class="num">4</td><td class="num">23</td></tr>
        <tr class="highlight"><td>2026-04-10</td><td>Post</td><td class="num">1,301</td><td class="num">21</td><td class="num">0</td><td class="num">3</td><td class="num">11</td></tr>
        <tr><td>2026-03-23</td><td>Post</td><td class="num">1,059</td><td class="num">12</td><td class="num">0</td><td class="num">2</td><td class="num">2</td></tr>
        <tr><td>2026-04-14</td><td>Post</td><td class="num">726</td><td class="num">46</td><td class="num">0</td><td class="num">0</td><td class="num">0</td></tr>
        <tr><td>2026-04-15</td><td>Post</td><td class="num">657</td><td class="num">6</td><td class="num">1</td><td class="num">1</td><td class="num">3</td></tr>
        <tr><td>2026-04-16</td><td>Post</td><td class="num">650</td><td class="num">5</td><td class="num">1</td><td class="num">1</td><td class="num">2</td></tr>
        <tr><td>2026-04-17</td><td>Post</td><td class="num">631</td><td class="num">6</td><td class="num">2</td><td class="num">0</td><td class="num">2</td></tr>
        <tr><td>2026-03-22</td><td>Post</td><td class="num">507</td><td class="num">10</td><td class="num">3</td><td class="num">0</td><td class="num">1</td></tr>
        <tr><td>2026-04-11</td><td>Post</td><td class="num">429</td><td class="num">2</td><td class="num">0</td><td class="num">0</td><td class="num">0</td></tr>
        <tr><td>2026-04-13</td><td>Post</td><td class="num">288</td><td class="num">8</td><td class="num">0</td><td class="num">0</td><td class="num">1</td></tr>
        <tr><td>2026-04-01</td><td>Post</td><td class="num">214</td><td class="num">5</td><td class="num">0</td><td class="num">1</td><td class="num">0</td></tr>
        <tr><td>2026-04-12</td><td>Post</td><td class="num">205</td><td class="num">2</td><td class="num">0</td><td class="num">0</td><td class="num">2</td></tr>
      </tbody>
    </table>
  </div>

  <div class="data-section">
    <h3>&#x1F4D8; Facebook Performance &mdash; Last 30 Days</h3>
    <div class="ds-note">Source: Windsor MCP / Facebook Organic / Graeham Watts Realtor. 19 posts. Impressions only (no reach/engagement data from connector). Average ~20 impressions/post &mdash; FB distribution is weak.</div>
    <div class="data-cards">
      <div class="data-card"><div class="dc-v">19</div><div class="dc-l">Posts (30d)</div><div class="dc-c">~1 post / 1.5 days</div></div>
      <div class="data-card"><div class="dc-v">368</div><div class="dc-l">Total Impressions</div><div class="dc-c">~20 avg/post</div></div>
      <div class="data-card"><div class="dc-v">55</div><div class="dc-l">Best Post (Mar 24)</div><div class="dc-c">Same day as top IG</div></div>
      <div class="data-card"><div class="dc-v down">4</div><div class="dc-l">Worst Post (Apr 15)</div><div class="dc-c">Algorithmic dip</div></div>
    </div>
  </div>

  <div class="data-section">
    <h3>&#x1F3A5; YouTube Performance &mdash; Last 30 Days</h3>
    <div class="ds-note">Source: Windsor MCP / YouTube connector. <strong>CRITICAL:</strong> channel is dying. Revival plan: cross-post Reels as Shorts + commit to 1 Long/week.</div>
    <table class="data-table">
      <thead><tr><th>Date</th><th>Title</th><th class="num">Views</th><th class="num">Likes</th><th class="num">Comments</th><th class="num">Subs</th></tr></thead>
      <tbody>
        <tr><td>2026-03-27</td><td>House Tour: 2833 Georgetown St, EPA</td><td class="num">1</td><td class="num">0</td><td class="num">0</td><td class="num">0</td></tr>
      </tbody>
    </table>
  </div>

  <div class="data-section">
    <h3>&#x1F4CA; MLS Market Data &mdash; April 2026</h3>
    <div class="ds-note">Source: Web-sourced via Redfin, Benson Group, Own Team, Palo Alto Online, C.A.R. April 2026 reports. MLS direct login not executed (needs session auth).</div>
    <div class="data-cards">
      <div class="data-card"><div class="dc-v up">+1.7%</div><div class="dc-l">EPA YoY</div><div class="dc-c">Median ~$1.1M</div></div>
      <div class="data-card"><div class="dc-v down">-7.2%</div><div class="dc-l">SMC YoY</div><div class="dc-c">Median $1.9M SFH</div></div>
      <div class="data-card"><div class="dc-v up">+7.7%</div><div class="dc-l">SF YoY</div><div class="dc-c">Median $1.5M</div></div>
      <div class="data-card"><div class="dc-v">32 days</div><div class="dc-l">EPA DOM</div><div class="dc-c">Was 66 a year ago</div></div>
      <div class="data-card"><div class="dc-v">106.9%</div><div class="dc-l">SMC Sale-to-List</div><div class="dc-c">Bidding wars back</div></div>
      <div class="data-card"><div class="dc-v">6.46%</div><div class="dc-l">30yr Mortgage</div><div class="dc-c">Freddie Mac weekly</div></div>
      <div class="data-card"><div class="dc-v">$3.5M</div><div class="dc-l">Palo Alto Median</div><div class="dc-c">Exclusive $5M+</div></div>
      <div class="data-card"><div class="dc-v up">+27%</div><div class="dc-l">Luxury Sales YoY</div><div class="dc-c">Peninsula-wide</div></div>
    </div>
  </div>

  <div class="data-section">
    <h3>&#x1F4F0; Local News &amp; Events (last 7 days)</h3>
    <div class="ds-note">Source: Claude web search &mdash; queries "East Palo Alto news April 2026", "EPA development", "SMC real estate news", "Bay Area housing market".</div>
    <ul class="news-list">
      <li><span class="n-date">APR 17</span><a href="https://localnewsmatters.org/2026/04/17/east-palo-alto-two-years-without-homicide/" target="_blank">EPA marks 2 years without homicide</a> &mdash; Local News Matters. <strong>Primary source for this content package.</strong></li>
      <li><span class="n-date">APR 17</span><a href="https://www.almanacnews.com/east-palo-alto/2026/04/17/east-palo-alto-marks-two-years-without-a-homicide/" target="_blank">EPA marks two years without a homicide</a> &mdash; The Almanac</li>
      <li><span class="n-date">APR 13</span><a href="https://www.paloaltoonline.com/peninsula/2026/04/13/a-tale-of-2-housing-markets-spring-reveals-split-in-peninsula-real-estate/" target="_blank">A tale of 2 housing markets: Spring reveals split in Peninsula real estate</a> &mdash; Palo Alto Online</li>
      <li><span class="n-date">APR 13</span>Woodland Park West Bayshore-Newell: 772 units pre-app study session at EPA City Hall</li>
      <li><span class="n-date">APR 9</span><a href="https://www.paloaltoonline.com/technology/2026/04/09/east-palo-alto-eyes-digital-overhaul-for-city-services/" target="_blank">EPA eyes digital overhaul for city services</a> &mdash; 5-year plan adopted, 311 system coming</li>
      <li><span class="n-date">APR 8</span><a href="https://localnewsmatters.org/2026/04/08/east-palo-alto-council-shelves-flock-camera-contract-discussion-sparking-criticism/" target="_blank">EPA council shelves Flock camera contract discussion</a> &mdash; April 21 meeting will revisit</li>
    </ul>
  </div>

  <div class="data-section">
    <h3>&#x26A1; Trigger Events &mdash; Bay Area Tech Layoffs (WARN filings)</h3>
    <div class="ds-note">Source: WARN Firehose, SF Bay Area Times, ABC7. Feeds into buyer/seller trigger-event content.</div>
    <ul class="news-list">
      <li><span class="n-date">APR 28</span><strong>Amazon: 769 Bay Area employees</strong> (WARN filed Feb 3, 2026) &mdash; effective date 10 days out</li>
      <li><span class="n-date">MAR 20</span>Meta Platforms: 50 jobs in Menlo Park + 52 in Sunnyvale &mdash; Reality Labs division</li>
      <li><span class="n-date">YTD</span>95,278 tech employees impacted YTD 2026 (882/day national pace)</li>
      <li><span class="n-date">HIST</span>Menlo Park 2009-2026: 142 WARN notices, 10,138 workers; Meta 30% of total</li>
    </ul>
  </div>

  <div class="data-section">
    <h3>&#x1F4C5; Topic History &mdash; Previously Covered / Planned</h3>
    <div class="ds-note">Source: references/topic-history.json. Rolling 4-week window. Used to filter for content-gap score + prevent duplication.</div>
    <table class="data-table">
      <thead><tr><th>Week Of</th><th>Title</th><th>Funnel</th><th>Pillar</th><th>Market</th><th>GHL</th></tr></thead>
      <tbody>
        <tr><td>Apr 14</td><td>3 Pricing Mistakes EPA Sellers Make in 2026</td><td>BOFU</td><td>Buyer/Seller Ed</td><td>EPA</td><td>SELL</td></tr>
        <tr class="highlight"><td>Apr 21 (planned)</td><td>A Tale of Two Markets: AI Boom vs Layoffs</td><td>MOFU</td><td>Market Data</td><td>Peninsula</td><td>MARKET</td></tr>
        <tr class="highlight"><td>Apr 21 (planned)</td><td>Amazon Just Laid You Off &mdash; Home Equity Moves</td><td>BOFU</td><td>Trigger Events</td><td>Bay Area</td><td>OPTIONS</td></tr>
        <tr class="highlight"><td>Apr 21 (planned)</td><td>The Insurance Crisis Nobody Warned Bay Area Buyers</td><td>BOFU</td><td>Buyer/Seller Ed</td><td>Bay Area</td><td>READY</td></tr>
        <tr class="highlight"><td>Apr 21 (planned)</td><td>EPA Affordable Housing Policy Shift</td><td>MOFU</td><td>Community</td><td>EPA</td><td>EPA</td></tr>
        <tr class="highlight"><td>Apr 21 (planned)</td><td>Best Tacos from EPA to Redwood City</td><td>TOFU</td><td>Lifestyle</td><td>EPA-RWC</td><td>&mdash;</td></tr>
      </tbody>
    </table>
  </div>

  <div class="data-section">
    <h3>&#x1F916; Data Pull Metadata</h3>
    <div class="ds-note">Transparency for future rerun / debugging.</div>
    <div class="data-cards">
      <div class="data-card"><div class="dc-v">Apr 18 2026</div><div class="dc-l">Pull Timestamp</div><div class="dc-c">Phase R research</div></div>
      <div class="data-card"><div class="dc-v">8/8</div><div class="dc-l">Sources Hit</div><div class="dc-c">All Phase R sources</div></div>
      <div class="data-card"><div class="dc-v">7 days</div><div class="dc-l">Search Console</div><div class="dc-c">Apr 11-17</div></div>
      <div class="data-card"><div class="dc-v">30 days</div><div class="dc-l">Social Perf</div><div class="dc-c">Mar 19-Apr 17</div></div>
      <div class="data-card"><div class="dc-v">Windsor MCP</div><div class="dc-l">Data Layer</div><div class="dc-c">7 connectors live</div></div>
      <div class="data-card"><div class="dc-v">MLS manual</div><div class="dc-l">Gap</div><div class="dc-c">Direct login not run</div></div>
    </div>
  </div>
</div>
"""

# ============================================================
# HEAD + MAIN BODY
# ============================================================
HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EPA Two Years Homicide-Free - Production Dashboard v4 | Graeham Watts</title>
<style>
:root{--navy:#1B2A4A;--gold:#C5A258;--gold-soft:rgba(197,162,88,0.12);--bg:#f4f5f7;--card:#ffffff;--card2:#f8f9fb;--border:#e2e5ea;--text:#2C2C2C;--muted:#666;--yt:#FF0000;--ig1:#E1306C;--fb:#1877F2;--tk:#010101;--gsc:#34A853;--gmb:#4285f4;--blog:#10b981;--teal:#00695c;--purple:#6a1b9a;--red:#c62828;--green:#2e7d32;--orange:#e65100;--radius:12px;--shadow:0 2px 8px rgba(0,0,0,0.04)}
*{margin:0;padding:0;box-sizing:border-box}
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
body{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--text);line-height:1.65;-webkit-font-smoothing:antialiased}
.page{max-width:1400px;margin:0 auto;padding:0 24px 40px}
.hero{background:linear-gradient(135deg,var(--navy) 0%,#2a3d6b 60%,#3a5090 100%);color:#fff;padding:40px 44px 32px;border-radius:0 0 var(--radius) var(--radius);text-align:center;position:relative;overflow:hidden}
.hero::after{content:'';position:absolute;top:-80px;right:-80px;width:320px;height:320px;border-radius:50%;background:rgba(197,162,88,0.06)}
.hero-ey{font-family:'Plus Jakarta Sans',sans-serif;font-size:10px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--gold);margin-bottom:8px}
.hero h1{font-family:'Plus Jakarta Sans',sans-serif;font-size:30px;font-weight:800;margin-bottom:10px;max-width:900px;margin-left:auto;margin-right:auto;line-height:1.25}
.hsub{font-size:14px;color:rgba(255,255,255,0.75);max-width:820px;margin:0 auto 16px;line-height:1.7}
.hero-meta{display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin-top:16px}
.hm-pill{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);padding:6px 16px;border-radius:99px;font-size:11px;color:#fff;font-weight:600}
.hm-pill.hero-score{background:var(--gold);color:var(--navy);border-color:var(--gold)}
.pow{font-size:10px;color:rgba(255,255,255,0.3);margin-top:16px}
.sh{font-family:'Plus Jakarta Sans',sans-serif;font-size:20px;font-weight:800;color:var(--navy);margin:30px 0 14px;padding-bottom:8px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px}
.sh2{font-family:'Plus Jakarta Sans',sans-serif;font-size:15px;font-weight:700;margin:16px 0 8px;color:var(--navy)}
.timing-card{background:linear-gradient(135deg,#fff,#f8f9fb);border-radius:var(--radius);padding:24px;margin:20px 0;border:2px solid var(--navy);box-shadow:var(--shadow);position:relative}
.tc-h{font-family:'Plus Jakarta Sans',sans-serif;font-size:13px;font-weight:800;color:var(--navy);margin-bottom:4px;text-transform:uppercase;letter-spacing:1px}
.tc-v{font-family:'Plus Jakarta Sans',sans-serif;font-size:44px;font-weight:800;color:var(--navy);line-height:1;margin:8px 0}
.tc-meta{font-size:12px;color:var(--muted);line-height:1.6}
.tc-meta code{background:var(--card2);padding:2px 6px;border-radius:4px;font-size:11px;color:var(--navy)}
.comp{background:#e8f5e9;border:1px solid #a5d6a7;border-radius:var(--radius);padding:14px 18px;margin:16px 0;font-size:12px;color:#1b5e20;display:flex;align-items:flex-start;gap:10px}
.comp-icon{font-size:18px}
.isp{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:22px;margin-bottom:20px;box-shadow:var(--shadow)}
.isp-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.isp-card{background:var(--card2);border-radius:10px;padding:14px;border-left:4px solid var(--navy)}
.isp-card h4{font-family:'Plus Jakarta Sans',sans-serif;font-size:13px;font-weight:700;margin-bottom:6px;display:flex;align-items:center;gap:6px}
.isp-card p{font-size:12px;color:var(--muted);line-height:1.5}
.isp-card .finding{font-size:11px;margin-top:8px;padding-top:8px;border-top:1px solid var(--border);color:var(--navy);font-weight:600}
.score-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:14px 0}
.score-c{background:var(--card);border-radius:var(--radius);padding:16px;border:1px solid var(--border);box-shadow:var(--shadow);text-align:center}
.score-c .sv{font-family:'Plus Jakarta Sans',sans-serif;font-size:28px;font-weight:800;color:var(--gold)}
.score-c .sl{font-size:11px;color:var(--muted);margin-top:4px;font-weight:600;letter-spacing:0.5px;text-transform:uppercase}
.score-c .sn{font-size:11px;color:var(--muted);margin-top:6px;line-height:1.4}
.flow-map{display:flex;gap:8px;padding:16px 0;overflow-x:auto;align-items:stretch}
.flow-card{min-width:140px;padding:12px 14px;border-radius:var(--radius);border:2px solid var(--border);cursor:pointer;text-align:center;transition:all .2s;flex-shrink:0;background:var(--card)}
.flow-card:hover{border-color:var(--navy);transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,0.08)}
.flow-card.active{border-color:var(--navy);background:rgba(27,42,74,.06)}
.flow-card.core{background:linear-gradient(135deg,rgba(27,42,74,.08),rgba(27,42,74,.02));border-color:var(--navy)}
.flow-card .fc-type{font-size:10px;text-transform:uppercase;letter-spacing:1px;font-weight:700;margin-bottom:4px;color:var(--navy)}
.flow-card .fc-title{font-size:12px;color:var(--muted);line-height:1.3}
.flow-card .fc-tag{display:inline-block;font-size:9px;padding:2px 6px;border-radius:99px;margin-top:6px;font-weight:600}
.tag-yt{background:#fce4ec;color:var(--yt)}.tag-ig{background:#fce4ec;color:var(--ig1)}
.tag-tk{background:#e0f7fa;color:#00838f}.tag-blog{background:#e8f5e9;color:#2e7d32}
.tag-gmb{background:#e3f2fd;color:var(--gmb)}.tag-fb{background:#e3f2fd;color:var(--fb)}
.deriv-panel{background:var(--card2);border-radius:var(--radius);padding:22px;margin-top:12px;border:1px solid var(--border);display:none;box-shadow:inset 0 1px 3px rgba(0,0,0,0.03)}
.deriv-panel.active{display:block}
.prompt-card{background:#fafbfc;border:1px solid var(--border);border-radius:var(--radius);padding:20px;margin:12px 0;position:relative}
.prompt-card .pc-h{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;flex-wrap:wrap;gap:8px;padding-bottom:12px;border-bottom:1px solid var(--border)}
.prompt-card .pc-label{font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;font-weight:800;color:var(--navy)}
.prompt-card .pc-meta{font-size:11px;color:var(--muted)}
.content-section{background:#fff;border:1px solid var(--border);border-radius:8px;padding:16px;margin-bottom:14px}
.content-section .cs-h{font-family:'Plus Jakarta Sans',sans-serif;font-size:11px;font-weight:800;color:var(--green);text-transform:uppercase;letter-spacing:1px;margin-bottom:10px}
.content-preview{background:var(--card2);border:1px solid var(--border);border-radius:6px;padding:12px;max-height:240px;overflow-y:auto;font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:11px;line-height:1.6;color:var(--text);white-space:pre-wrap;margin-bottom:10px}
.pair-section{background:#faf5ff;border:1px solid rgba(106,27,154,0.18);border-radius:8px;padding:16px;margin-bottom:14px}
.pair-desc{font-size:12px;color:var(--muted);line-height:1.5;margin-top:4px}
.regenerate-section{background:#f8f5ee;border:1px dashed rgba(197,162,88,0.35);border-radius:8px;padding:14px}
.regen-h{font-size:11px;color:var(--muted);margin-bottom:8px;font-style:italic}
.button-row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.char-meta{font-size:11px;color:var(--muted)}
.copy-big{background:var(--gold);color:var(--navy);border:none;padding:10px 22px;border-radius:8px;font-size:13px;font-weight:800;cursor:pointer;font-family:'Plus Jakarta Sans',sans-serif;letter-spacing:0.3px;display:inline-flex;align-items:center;gap:6px;transition:all .15s;box-shadow:0 2px 8px rgba(197,162,88,0.25)}
.copy-big:hover{background:#b89348;transform:translateY(-1px);box-shadow:0 4px 12px rgba(197,162,88,0.35)}
.copy-big.copied{background:var(--green);color:#fff;box-shadow:0 2px 8px rgba(46,125,50,0.25)}
.copy-outline{background:transparent;color:var(--navy);border:2px solid var(--gold);padding:8px 18px;border-radius:8px;font-size:12px;font-weight:700;cursor:pointer;font-family:'Plus Jakarta Sans',sans-serif;letter-spacing:0.3px;transition:all .15s}
.copy-outline:hover{background:var(--gold-soft);transform:translateY(-1px)}
.copy-outline.copied{background:var(--green);color:#fff;border-color:var(--green)}
.use-in{margin-top:14px;font-size:11px;color:var(--muted);padding:10px 14px;background:rgba(0,105,92,0.06);border-left:3px solid var(--teal);border-radius:0 6px 6px 0}
.use-in strong{color:var(--navy)}
.shots{width:100%;border-collapse:collapse;margin:14px 0;font-size:12px;background:var(--card);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow)}
.shots th{background:var(--navy);color:#fff;padding:10px 12px;text-align:left;font-weight:600}
.shots td{padding:10px 12px;border-bottom:1px solid var(--border);vertical-align:top}
.shots tr:hover{background:var(--card2)}
.shots .sn{background:var(--navy);color:#fff;width:28px;height:28px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-weight:700;font-size:12px}
.hook-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px;margin:14px 0}
.hook-card{background:var(--card);border-radius:var(--radius);padding:18px;border:2px solid var(--border);box-shadow:var(--shadow);position:relative}
.hook-card.picked{border-color:var(--navy);background:linear-gradient(135deg,rgba(27,42,74,.06),rgba(27,42,74,.02))}
.hook-card h4{font-family:'Plus Jakarta Sans',sans-serif;font-size:13px;font-weight:700;color:var(--navy);margin-bottom:8px}
.hook-card p{font-size:13px;color:var(--text);line-height:1.6;font-style:italic}
.hook-card .hook-tag{position:absolute;top:10px;right:12px;background:var(--gold);color:var(--navy);font-size:10px;padding:3px 10px;border-radius:99px;font-weight:700;letter-spacing:0.5px}
.cta-card{background:linear-gradient(135deg,var(--navy),#2a3d6b);color:#fff;border-radius:var(--radius);padding:24px;margin:20px 0;box-shadow:var(--shadow)}
.cta-card h3{font-family:'Plus Jakarta Sans',sans-serif;font-size:16px;font-weight:800;color:var(--gold);margin-bottom:10px;text-transform:uppercase;letter-spacing:1px}
.cta-card code{background:rgba(0,0,0,0.3);padding:10px 14px;border-radius:6px;display:block;font-family:monospace;font-size:12px;margin:10px 0;overflow-x:auto;color:#a5d6a7}
.cta-card .cta-row{display:flex;gap:12px;flex-wrap:wrap;margin-top:12px}
.cta-card .cta-row div{background:rgba(255,255,255,0.08);padding:8px 14px;border-radius:6px;font-size:12px;border:1px solid rgba(255,255,255,0.12)}
.insight{background:#e0f2f1;border-left:4px solid var(--teal);padding:14px 18px;border-radius:0 var(--radius) var(--radius) 0;margin:14px 0;font-size:13px;line-height:1.7}
.insight strong{color:var(--teal)}
.cal-integrate{background:#fff3e0;border:1px solid #ffe0b2;border-radius:var(--radius);padding:18px 22px;margin:18px 0;font-size:13px;color:#5d4037;line-height:1.7}
.cal-integrate strong{color:var(--orange)}
.cal-integrate a{color:var(--orange);font-weight:700}
.how-to{background:linear-gradient(135deg,#e3f2fd,#e8f5e9);border-left:4px solid var(--fb);padding:16px 20px;border-radius:0 var(--radius) var(--radius) 0;margin:16px 0;font-size:13px;line-height:1.7}
.how-to strong{color:var(--navy)}
.how-to ol{margin-left:18px;margin-top:6px}
.how-to li{margin:4px 0}
.data-toggle-wrap{display:flex;justify-content:center;margin:18px 0}
.data-toggle{background:var(--navy);color:#fff;border:none;padding:11px 26px;border-radius:8px;font-size:13px;font-weight:700;cursor:pointer;font-family:'Plus Jakarta Sans',sans-serif;letter-spacing:0.3px;display:inline-flex;align-items:center;gap:8px;transition:all .15s}
.data-toggle:hover{background:#2a3d6b;transform:translateY(-1px);box-shadow:0 4px 10px rgba(27,42,74,0.2)}
.research-data{display:none;background:var(--card);border-radius:var(--radius);border:1px solid var(--border);margin:16px 0;padding:24px;box-shadow:var(--shadow)}
.research-data.open{display:block}
.data-section{margin:18px 0;padding-bottom:16px;border-bottom:1px solid var(--border)}
.data-section:last-child{border-bottom:none}
.data-section h3{font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;font-weight:800;color:var(--navy);margin-bottom:8px;display:flex;align-items:center;gap:8px}
.data-section .ds-note{font-size:11px;color:var(--muted);margin-bottom:10px;font-style:italic}
.data-table{width:100%;border-collapse:collapse;font-size:11px;margin-top:6px}
.data-table th{background:var(--card2);color:var(--navy);padding:8px 10px;text-align:left;font-weight:700;border-bottom:2px solid var(--border);font-size:10px;text-transform:uppercase;letter-spacing:0.5px}
.data-table td{padding:6px 10px;border-bottom:1px solid var(--border)}
.data-table tr:hover{background:var(--card2)}
.data-table .num{font-family:ui-monospace,monospace;text-align:right}
.data-table .highlight{background:rgba(197,162,88,0.08);font-weight:700}
.data-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin:10px 0}
.data-card{background:var(--card2);padding:12px;border-radius:8px;border-left:3px solid var(--navy)}
.data-card .dc-v{font-family:'Plus Jakarta Sans',sans-serif;font-size:20px;font-weight:800;color:var(--navy)}
.data-card .dc-l{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:0.5px;margin-top:2px}
.data-card .dc-c{font-size:11px;color:var(--muted);margin-top:4px}
.data-card .up{color:var(--green)}.data-card .down{color:var(--red)}
.news-list{list-style:none;padding:0}
.news-list li{padding:8px 0;border-bottom:1px dashed var(--border);font-size:12px}
.news-list li:last-child{border-bottom:none}
.news-list .n-date{color:var(--muted);font-size:10px;font-weight:700;display:inline-block;margin-right:8px}
.news-list a{color:var(--fb);text-decoration:none}
.news-list a:hover{text-decoration:underline}
.footer{text-align:center;padding:30px 20px;color:var(--muted);font-size:12px;border-top:1px solid var(--border);margin-top:30px}
.footer .brand{color:var(--navy);font-weight:700;font-size:14px;font-family:'Plus Jakarta Sans',sans-serif}
@media print{body{background:#fff;color:#000}.page{max-width:100%}}
@media (max-width:768px){.hero h1{font-size:22px}.tc-v{font-size:36px}.sh{font-size:17px}}
</style>
</head>
<body>
<div class="page">

<div class="hero">
  <div class="hero-ey">Content Engine Stage 3 &middot; Research-First &middot; v4 Dual-Button + Full Data &middot; Week of April 20, 2026</div>
  <h1>East Palo Alto Just Hit 2 Years Without a Homicide &mdash; And It's Changing Peninsula Home Prices</h1>
  <div class="hsub">A counter-narrative content package built from the April 17, 2026 milestone announcement, cross-referenced against EPA MLS data (+1.7% YoY, DOM cut in half) and Peninsula-wide fragmentation (SMC -7.2% YoY).</div>
  <div class="hero-meta">
    <div class="hm-pill hero-score">Opportunity Score 10/10 &starf;</div>
    <div class="hm-pill">Funnel: MOFU &rarr; BOFU</div>
    <div class="hm-pill">Pillar 5 + 4</div>
    <div class="hm-pill">GHL Keyword: EPA</div>
    <div class="hm-pill">Target: ~4:30</div>
  </div>
  <div class="pow">Generated April 18, 2026 &middot; Content Creation Engine v4 &middot; Intero Real Estate &middot; DRE #01466876</div>
</div>

<div class="how-to">
  <strong>How to use this dashboard (dual-button pattern):</strong>
  <ol>
    <li><strong>Copy Content</strong> (gold button) &mdash; the production-ready deliverable, paste directly into YouTube/IG/Gmail/etc.</li>
    <li><strong>Copy Prompt</strong> (gold outline) &mdash; use when you want to regenerate a fresh version, tweak the angle, or run through a different AI.</li>
    <li><strong>Show Full Research Data</strong> button (below) &mdash; expandable panel with all raw data that backed the findings (Search Console, social, MLS, news, topic history).</li>
  </ol>
  Both prompt and content pre-loaded. Each prompt already includes Agent Identity + Fair Housing + Date/Year QC + Timing Self-Check + Voice + Topic + AEO + Key Facts + GHL CTA.
</div>

<div class="timing-card">
  <div class="tc-h">Verified Timing Calculation (no generic defaults)</div>
  <div class="tc-v">~4:30 min</div>
  <div class="tc-meta">
    <strong>573 words</strong> of spoken script body &times; 150 WPM &times; 1.15 pause/B-roll buffer = <code>4.39 minutes</code><br>
    Corrected per SKILL.md mandatory timing calculation rule.
  </div>
</div>

<div class="comp">
  <span class="comp-icon">&#x2705;</span>
  <div><strong>Fair Housing Compliance: Passed.</strong> Homicide data framed as statistics plus community policy shift, not neighborhood character. No demographic references, no coded language, no school rankings.</div>
</div>

<h2 class="sh">Intelligence Stack &mdash; What Backed This Topic</h2>
<div class="isp">
  <div class="isp-grid">
    <div class="isp-card"><h4>&#x1F4F0; Local News</h4><p>EPA officially marked 2 years without a homicide on April 17, 2026. Last: April 2024. 1992 baseline: 42 homicides in 24K population.</p><div class="finding">Source: Local News Matters, The Almanac &mdash; April 17, 2026</div></div>
    <div class="isp-card"><h4>&#x1F4CA; MLS Market Data</h4><p>EPA median +1.7% YoY; DOM 66 &rarr; 32 days; SMC -7.2% YoY.</p><div class="finding">Source: Redfin EPA, Benson Group, Own Team &mdash; April 2026</div></div>
    <div class="isp-card"><h4>&#x1F50D; Search Console</h4><p>"East palo alto real estate" pos 20.5 / 10 imp; "epa realtor" pos 17.5 / 6 imp.</p><div class="finding">Source: sc-domain:graehamwatts.com &mdash; last 7 days</div></div>
    <div class="isp-card"><h4>&#x1F4F1; Social Performance</h4><p>Top IG posts avg 10-23 shares. Counter-narrative + bold stat = share pattern match.</p><div class="finding">Source: Windsor Instagram &mdash; last 30 days</div></div>
    <div class="isp-card"><h4>&#x1F3DB;&#xFE0F; Local Government</h4><p>City of EPA confirmed milestone. Drivers: community partnerships, youth/workforce, modernized policing.</p><div class="finding">Source: City of East Palo Alto &mdash; April 17, 2026</div></div>
    <div class="isp-card"><h4>&#x1F3AF; BOFU Cross-Reference</h4><p>No overlap with weeks of April 14 or April 21 planned calendar.</p><div class="finding">Source: references/topic-history.json</div></div>
  </div>
</div>

__RESEARCH_DATA__

<h2 class="sh">Opportunity Score Breakdown (10/10)</h2>
<div class="score-grid">
  <div class="score-c"><div class="sv">3/3</div><div class="sl">Timeliness</div><div class="sn">Story broke April 17, 2026</div></div>
  <div class="score-c"><div class="sv">3/3</div><div class="sl">Audience Relevance</div><div class="sn">Direct property value impact</div></div>
  <div class="score-c"><div class="sv">2/2</div><div class="sl">Content Gap</div><div class="sn">No existing coverage</div></div>
  <div class="score-c"><div class="sv">2/2</div><div class="sl">Engagement Potential</div><div class="sn">Counter-narrative share pattern</div></div>
</div>

<div class="cal-integrate">
  <strong>&#x1F4C5; Calendar Integration:</strong> Your April 20 V6 calendar was built April 14, before this story broke. Three options: <strong>(A)</strong> Replace Mon Apr 20 "EPA Homes Under $1M" with this anchor. <strong>(B)</strong> Add as Sat/Sun breaking interrupt. <strong>(C)</strong> Hold for April 27. <a href="./2026-04-20-production-calendar-v6.html">&rarr; Existing April 20 calendar</a>
</div>

<h2 class="sh">Content Derivatives &mdash; 14 Formats Ready</h2>
<p style="color:var(--muted);font-size:13px;margin-bottom:6px">Each format has <strong>Copy Content</strong> (gold, production-ready) + <strong>Copy Prompt</strong> (gold outline, for regeneration).</p>
<div class="flow-map">
  __FLOW__
</div>

<div id="panel-container">
__PANELS__
</div>

<h2 class="sh">Shot List &mdash; Hand to Peter and John</h2>
<table class="shots">
  <thead><tr><th style="width:40px">#</th><th>Shot Description</th><th style="width:110px">Duration</th><th>Setup Notes</th></tr></thead>
  <tbody>
    <tr><td><span class="sn">1</span></td><td><strong>Open Talking Head</strong> &mdash; Graeham neutral expression (no smile on hook)</td><td>0:00-0:20</td><td>Eye-level, 50mm look, clean backdrop</td></tr>
    <tr><td><span class="sn">2</span></td><td>Archival 1990s news clips / chyrons</td><td>0:20-0:35</td><td>Stock archival OR AI-generate</td></tr>
    <tr><td><span class="sn">3</span></td><td>TH cutback &mdash; setup context</td><td>0:35-1:05</td><td>Same framing as Shot 1</td></tr>
    <tr><td><span class="sn">4</span></td><td>90s newspaper headlines / period EPA photos</td><td>1:05-1:15</td><td>SF Chronicle / Mercury News archive</td></tr>
    <tr><td><span class="sn">5</span></td><td>TH Act 2 &mdash; warmer tone</td><td>1:15-1:45</td><td>Small camera repositioning</td></tr>
    <tr><td><span class="sn">6</span></td><td>Community B-roll &mdash; Joel Davis Park, youth programs</td><td>1:45-2:05</td><td>Shoot locally OR request from City of EPA</td></tr>
    <tr><td><span class="sn">7</span></td><td>TH milestone reveal &mdash; slower pace</td><td>2:05-2:35</td><td>Direct-to-camera, closer framing</td></tr>
    <tr><td><span class="sn">8</span></td><td>EPA City Hall / current streets / events</td><td>2:35-2:55</td><td>Shoot locally</td></tr>
    <tr><td><span class="sn">9</span></td><td>TH market angle &mdash; business tone</td><td>2:55-3:45</td><td>TH, stat overlays in post</td></tr>
    <tr><td><span class="sn">10</span></td><td>Motion graphic stat cards &mdash; DOM and price data</td><td>3:45-4:00</td><td>Motion graphics (Jason)</td></tr>
    <tr><td><span class="sn">11</span></td><td>TH CTA &mdash; direct, confident</td><td>4:00-4:30</td><td>TH, close framing</td></tr>
    <tr><td><span class="sn">12</span></td><td>End card &mdash; Graeham branding</td><td>4:30</td><td>Static, 3-4 sec hold</td></tr>
  </tbody>
</table>

<h2 class="sh">3 Alternate Hooks (A/B Testing)</h2>
<div class="hook-grid">
  <div class="hook-card picked"><div class="hook-tag">PICKED</div><h4>Hook A &mdash; Story-led</h4><p>"East Palo Alto was called 'the murder capital of America.' That was 1992. Last week &mdash; 34 years later &mdash; the city quietly hit a milestone almost nobody outside of here is talking about."</p></div>
  <div class="hook-card"><h4>Hook B &mdash; Buyer-math-led</h4><p>"If you've been shopping the Peninsula and skipping East Palo Alto &mdash; you're paying Palo Alto prices for a problem that stopped existing in 2024. Let me show you the data."</p></div>
  <div class="hook-card"><h4>Hook C &mdash; Counter-narrative-led</h4><p>"What if I told you the 'murder capital of America' has gone two full years without a single homicide &mdash; and the rest of the Peninsula just lost 7% of its home value while East Palo Alto quietly went up?"</p></div>
</div>
<div class="insight"><strong>Recommendation:</strong> Hook A as primary. Shares trigger on curiosity + charged phrase + reveal pattern.</div>

<div class="cta-card">
  <h3>&#x1F680; Auto-Render Hand-off (HeyGen)</h3>
  <p>After Copy Content on YouTube Long Pt 1, save the SSML block to <code>outputs/content-package-2026-04-18-epa-two-years-homicide-free.ssml.txt</code> then run:</p>
  <code>python3 skills/heygen-elevenlabs-renderer/scripts/full_render.py \\\\<br>&nbsp;&nbsp;--script outputs/content-package-2026-04-18-epa-two-years-homicide-free.ssml.txt \\\\<br>&nbsp;&nbsp;--slug "epa-two-years-homicide-free" \\\\<br>&nbsp;&nbsp;--resolution 1080p \\\\<br>&nbsp;&nbsp;--aspect 16:9</code>
  <div class="cta-row">
    <div><strong>Voice:</strong> Graeham clone Pa3vOYQHHpLJn1Tf7hnP</div>
    <div><strong>Avatar:</strong> 9a3600b16f604059b6ab8b9a55e29ea9</div>
    <div><strong>GHL Keyword:</strong> EPA</div>
  </div>
</div>

<div class="footer">
  <div class="brand">Graeham Watts &mdash; Intero Real Estate &middot; DRE #01466876</div>
  <div style="margin-top:6px">Content Creation Engine &middot; Stage 3 Research-First &middot; v4 Dual-Button + Full Data &middot; Generated April 18, 2026</div>
  <div style="margin-top:6px">Sources: Local News Matters &middot; The Almanac &middot; Redfin &middot; Benson Group &middot; Own Team &middot; Palo Alto Online &middot; City of East Palo Alto</div>
</div>

</div>

<script>
window.PROMPT_LIBRARY = __PLIB__;
window.CONTENT_LIBRARY = __CLIB__;

function copyPrompt(btn, key) {
  var v = window.PROMPT_LIBRARY[key];
  if (!v) { btn.textContent = 'No prompt'; return; }
  navigator.clipboard.writeText(v).then(function(){
    var o = btn.textContent;
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(function(){ btn.textContent = o; btn.classList.remove('copied'); }, 2000);
  });
}

function copyContent(btn, key) {
  var v = window.CONTENT_LIBRARY[key];
  if (!v) { btn.textContent = 'No content'; return; }
  navigator.clipboard.writeText(v).then(function(){
    var o = btn.textContent;
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(function(){ btn.textContent = o; btn.classList.remove('copied'); }, 2000);
  });
}

function toggleResearchData() {
  var el = document.getElementById('research-data');
  var btn = document.querySelector('.data-toggle');
  el.classList.toggle('open');
  btn.textContent = el.classList.contains('open') ? 'Hide Full Research Data' : 'Show Full Research Data';
}

document.querySelectorAll('.flow-card').forEach(function(card){
  card.addEventListener('click', function(){
    var t = card.dataset.target;
    document.querySelectorAll('.flow-card').forEach(function(c){ c.classList.remove('active'); });
    document.querySelectorAll('.deriv-panel').forEach(function(p){ p.classList.remove('active'); });
    card.classList.add('active');
    var panel = document.getElementById('panel-' + t);
    if (panel) panel.classList.add('active');
  });
});
</script>
</body>
</html>
"""

# Substitute placeholders
DASHBOARD = HEAD
DASHBOARD = DASHBOARD.replace("__RESEARCH_DATA__", RESEARCH_DATA_HTML)
DASHBOARD = DASHBOARD.replace("__FLOW__", FLOW)
DASHBOARD = DASHBOARD.replace("__PANELS__", PANELS)
DASHBOARD = DASHBOARD.replace("__PLIB__", PLIB)
DASHBOARD = DASHBOARD.replace("__CLIB__", CLIB)

OUT = Path("/var/tmp/stage3/skills/content-calendars/2026-04-18-epa-two-years-homicide-free-production.html")
OUT.write_text(DASHBOARD, encoding="utf-8")

print(f"WROTE: {OUT}")
print(f"size={len(DASHBOARD):,} prompts={len(PROMPTS)} content={len(CONTENT)} panels={len(panels_html)} cards={len(flow_cards)}")
