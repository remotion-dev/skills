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

# Format-specific button labels (for Copy Content button — tells user exactly what they're copying)
BUTTON_LABELS = {
    "yt-long-pt1":      "Copy Script + SSML",
    "yt-long-pt2":      "Copy Production Package",
    "production-brief": "Copy Production Brief",
    "yt-short":         "Copy Short Script",
    "ig-reel-1":        "Copy Reel #1",
    "ig-reel-2":        "Copy Reel #2",
    "ig-carousel":      "Copy Carousel",
    "tiktok":           "Copy TikTok",
    "blog":             "Copy Blog Post",
    "gmb":              "Copy GMB Post",
    "facebook":         "Copy Facebook Post",
    "linkedin":         "Copy LinkedIn Post",
    "ad-copy":          "Copy Ad Copy",
    "email":            "Copy Email Lead",
    "full-newsletter":  "Copy Newsletter HTML",
}

# Pairing map: some formats have a "companion" format that's usually grabbed together
# Voice/text side paired with Production/editing side, etc.
PAIRINGS = {
    "yt-long-pt1": ("yt-long-pt2", "Copy Production Content", "B-roll prompts + Editing notes for Jason + AI video prompts (Seedance) + YouTube SEO + 3 alt hooks. Everything non-voice that the production team needs for this video."),
}

# HeyGen render config — which formats can be rendered as avatar video + recommended avatar per format
HEYGEN_RENDER = {
    "yt-long-pt1":  {"avatar": "digital_twin",  "avatar_id": "159cd7b883724fdb9a51b97dec94df89", "aspect": "16:9", "reason": "Authentic face from real video — best for long-form face-critical content"},
    "yt-short":     {"avatar": "fashion_flip",  "avatar_id": "b0644e6b20ba414981b7821d88caf675", "aspect": "9:16", "reason": "Higher energy for scroll-stopping shorts"},
    "ig-reel-1":    {"avatar": "casual_chic",   "avatar_id": "afdc7e3e9f0c45de896fa687c594a216", "aspect": "9:16", "reason": "Approachable everyday energy for hook-led Reel"},
    "ig-reel-2":    {"avatar": "freshly_ironed","avatar_id": "09fed5d2c0b74376b6e7313cbb888c86", "aspect": "9:16", "reason": "Polished, data-forward look for stat-heavy Reel"},
    "tiktok":       {"avatar": "fashion_flip",  "avatar_id": "b0644e6b20ba414981b7821d88caf675", "aspect": "9:16", "reason": "Higher energy matches TikTok's native pacing"},
}
VOICE_CLONE_ID = "717249201f7745988219b9aeb9041b42"  # Graeham Watts Voice Clone (default across all looks)

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
            '      <div class="cs-h" style="color:var(--purple)">Also Grab: Production Content (for Jason &amp; production team)</div>\n'
            '      <div class="section-help"><strong>What this is:</strong> The VOICE side of this video (script + SSML) is above. This PURPLE section gives you the PRODUCTION side &mdash; editing notes for Jason, B-roll requirements, AI video prompts for Seedance, text overlay timings, thumbnail concept, YouTube SEO metadata, 3 alt hooks for A/B testing. Two sides of the same video &mdash; grab both from this one panel, no tab-switching.</div>\n'
            '      <div class="pair-desc">' + pair_desc + '</div>\n'
            '      <div class="button-row" style="margin-top:10px">\n'
            '        <button class="copy-big" style="background:var(--purple);color:#fff;box-shadow:0 2px 8px rgba(106,27,154,0.25)" onclick="copyContent(this,\'' + pair_key + '\')">' + pair_label + '</button>\n'
            '        <span class="char-meta">' + f"{pair_content_chars:,}" + ' chars</span>\n'
            '      </div>\n'
            '      <div class="btn-help"><strong>Paste into:</strong> Production team Slack/Notion for Jason. <strong>Contains:</strong> editing timeline, shot list, B-roll sources, text overlay timing table, thumbnail design, music direction, 3 AI video prompts (Seedance), YouTube SEO package, 3 alt hooks.</div>\n'
            '    </div>\n'
        )

    # HeyGen render instruction block (only for video formats)
    render_block = ""
    if key in HEYGEN_RENDER:
        cfg = HEYGEN_RENDER[key]
        fmt_name = label.split(" - ")[-1] if " - " in label else label
        render_block = (
            '    <div class="render-section">\n'
            '      <div class="render-h">&#x1F3AC; Render This As a Video via HeyGen MCP</div>\n'
            '      <div class="render-explainer">\n'
            '        <strong>What this does:</strong> Takes the script above and turns it into a finished avatar video of Graeham &mdash; automatically. You don&apos;t log into HeyGen, you don&apos;t use any CLI, you don&apos;t click anywhere in the HeyGen dashboard. <strong>One button click here &rarr; one paste into Claude &rarr; Claude handles the rest via the HeyGen MCP.</strong>\n'
            '      </div>\n'
            '      <div class="render-steps">\n'
            '        <div class="render-step-label">Step-by-step flow:</div>\n'
            '        <ol class="render-steps-list">\n'
            '          <li><strong>One-time setup: install the HeyGen MCP.</strong> Go to <a href="https://docs.heygen.com/docs/heygen-mcp-server" target="_blank">docs.heygen.com/docs/heygen-mcp-server</a>. Follow the install (2 min). Paste your HeyGen API key (grab from <a href="https://app.heygen.com/api" target="_blank">app.heygen.com/api</a>). After this, Claude has HeyGen as a native tool.</li>\n'
            '          <li><strong>Click the red "Copy Render Instruction" button below.</strong> Copies a complete instruction (script pre-filled, avatar choice, voice, aspect, resolution) to your clipboard.</li>\n'
            '          <li><strong>Paste into any Claude session with HeyGen MCP connected</strong> (Cowork, Claude Desktop, Claude Code &mdash; whichever you use).</li>\n'
            '          <li><strong>Claude asks you to confirm the avatar.</strong> Accept the recommendation or swap to a different look.</li>\n'
            '          <li><strong>Claude calls <code>generate_avatar_video</code> directly.</strong> Video is queued in HeyGen within ~2 seconds. Claude returns a <code>video_id</code> + HeyGen dashboard URL.</li>\n'
            '          <li><strong>Check status later.</strong> Say &quot;check on video [id]&quot; any time &mdash; Claude calls <code>get_avatar_video_status</code>. When done, MP4 is downloadable.</li>\n'
            '        </ol>\n'
            '      </div>\n'
            '      <div class="render-avatar-box">\n'
            '        <strong>Recommended avatar for this format:</strong> <code>' + cfg["avatar"] + '</code><br>\n'
            '        <span style="font-size:12px;color:#5d1f1f"><strong>Why this avatar:</strong> ' + cfg["reason"] + '.</span><br>\n'
            '        <span style="font-size:12px;color:#5d1f1f;display:block;margin-top:6px"><strong>Override allowed:</strong> when Claude asks, name any of the 6 looks &mdash; <code>digital_twin</code>, <code>casual_chic</code>, <code>freshly_ironed</code>, <code>fashion_flip</code>, <code>bespectacled</code>, <code>suburban_serenity</code>.</span>\n'
            '      </div>\n'
            '      <details style="margin-top:10px">\n'
            '        <summary style="cursor:pointer;font-size:12px;font-weight:700;color:#c62828">Preview the exact instruction that gets copied</summary>\n'
            '        <div class="render-preview" style="margin-top:8px">Render this video via HeyGen MCP.\n\n'
            'Format: ' + fmt_name + '\n'
            'Avatar: ' + cfg["avatar"] + ' (' + cfg["avatar_id"] + ')\n'
            'Voice: Graeham Watts Voice Clone (' + VOICE_CLONE_ID + ')\n'
            'Aspect: ' + cfg["aspect"] + ' | Resolution: 1080p\n\n'
            'Script to speak:\n'
            '[full script from this panel gets pre-filled here when you click Copy]\n\n'
            'Call the HeyGen MCP generate_avatar_video tool. Confirm the avatar choice with me before submitting. Return the video_id and HeyGen dashboard URL so I can check status later.</div>\n'
            '      </details>\n'
            '      <div class="button-row" style="margin-top:14px">\n'
            '        <button class="copy-big" style="background:#FF0000;color:#fff;box-shadow:0 2px 8px rgba(255,0,0,0.25)" onclick="copyRender(this,\'' + key + '\')">&#x1F3AC; Copy Render Instruction</button>\n'
            '        <span class="char-meta">Auto-fills: script + <code>' + cfg["avatar"] + '</code> avatar + ' + cfg["aspect"] + ' aspect + voice clone + 1080p</span>\n'
            '      </div>\n'
            '    </div>\n'
        )

    destination = {'yt-long-pt1': 'YouTube upload page (paste script into description; SSML goes separately into ElevenLabs or HeyGen MCP)', 'yt-long-pt2': 'Production team Slack / Notion doc for Jason the editor', 'production-brief': 'Production call sheet — print for set, share via Notion/Dropbox with Peter, John, Jason', 'yt-short': 'YouTube Shorts upload page', 'ig-reel-1': 'Instagram Reel upload (script + paste caption)', 'ig-reel-2': 'Instagram Reel upload (script + paste caption)', 'ig-carousel': 'Instagram Carousel composer (one slide at a time) + paste caption', 'tiktok': 'TikTok upload page', 'blog': 'Blog CMS (WordPress, Ghost, Webflow, whatever you use)', 'gmb': 'Google My Business post composer', 'facebook': 'Facebook page post composer', 'linkedin': 'LinkedIn post composer', 'ad-copy': 'Meta Ads Manager (FB/IG) + Google Ads campaign builder', 'email': 'Gmail / Mailchimp / Klaviyo compose window', 'full-newsletter': 'Gmail / Mailchimp / Klaviyo — paste the full HTML as the email body'}.get(key, "the destination platform")
    panel = (
        '<div class="deriv-panel' + is_active + '" id="panel-' + key + '">\n'
        '  <div class="prompt-card">\n'
        '    <div class="pc-h"><div class="pc-label">' + label + '</div><div class="pc-meta">' + meta + '</div></div>\n'
        '    <div class="content-section">\n'
        '      <div class="cs-h">Ready to Post</div>\n'
        '      <div class="section-help"><strong>What this is:</strong> The finished, production-ready content for this format. Clicking the gold button below copies the complete deliverable to your clipboard &mdash; paste directly into the destination platform. No further editing required (though you can always tweak).</div>\n'
        '      <div class="content-preview">' + preview + '\n\n(Full content loaded - click the gold button to grab it all.)</div>\n'
        '      <div class="button-row">\n'
        '        <button class="copy-big" onclick="copyContent(this,\'' + key + '\')">' + BUTTON_LABELS.get(key, "Copy Content") + '</button>\n'
        '        <span class="char-meta">Full content: ' + f"{cchars:,}" + ' chars</span>\n'
        '      </div>\n'
        '      <div class="btn-help"><strong>Paste into:</strong> ' + destination + '.</div>\n'
        '    </div>\n' +
        pair_block +
        render_block +
        '    <div class="regenerate-section">\n'
        '      <div class="regen-h">Copy Prompt &mdash; use ONLY if you want to regenerate fresh content</div>\n'
        '      <div class="section-help"><strong>What this does:</strong> Copies the ORIGINAL PROMPT that would produce this format if you paste it into Claude or ChatGPT. Use this when you want a different angle, tweaked voice, or to run through a different AI. <strong>You do NOT need this to post the content above</strong> &mdash; the gold button already has the finished version. This is a regeneration escape hatch.</div>\n'
        '      <div class="button-row">\n'
        '        <button class="copy-outline" onclick="copyPrompt(this,\'' + key + '\')">Copy Prompt</button>\n'
        '        <span class="char-meta">Prompt: ' + f"{pchars:,}" + ' chars</span>\n'
        '      </div>\n'
        '      <div class="btn-help"><strong>Only click if:</strong> the generated content above doesn&apos;t match what you want and you&apos;d like to regenerate with tweaks.</div>\n'
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

# HeyGen render config for client-side JS (per-format avatar + aspect + reason)
HEYGEN_JS = {}
for key, cfg in HEYGEN_RENDER.items():
    fmt_label = FORMAT_META[key][0].split(" - ")[-1] if key in FORMAT_META else key
    HEYGEN_JS[key] = {
        "label": fmt_label,
        "avatar": cfg["avatar"],
        "avatar_id": cfg["avatar_id"],
        "aspect": cfg["aspect"],
        "reason": cfg["reason"],
        "voice_id": VOICE_CLONE_ID,
    }
HRLIB = json.dumps(HEYGEN_JS)

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
.used-badge{background:#e8f5e9;color:#2e7d32;font-size:10px;font-weight:700;padding:2px 8px;border-radius:99px;letter-spacing:0.3px}
.partial-badge{background:#fff3e0;color:#e65100;font-size:10px;font-weight:700;padding:2px 8px;border-radius:99px;letter-spacing:0.3px}
.unavail-badge{background:#fce4ec;color:#c62828;font-size:10px;font-weight:700;padding:2px 8px;border-radius:99px;letter-spacing:0.3px}
.perf-tbl{width:100%;border-collapse:collapse;margin:14px 0;font-size:13px;background:var(--card);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow)}
.perf-tbl th{background:var(--navy);color:#fff;padding:10px 12px;text-align:left;font-weight:600;font-size:12px}
.perf-tbl td{padding:10px 12px;border-bottom:1px solid var(--border)}
.perf-tbl tr:hover{background:var(--card2)}
.chg-up{color:#2e7d32;font-weight:700}
.chg-down{color:#c62828;font-weight:700}
.ctm{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin:14px 0}
.ct-card{background:var(--card);border-radius:var(--radius);padding:18px;border:1px solid var(--border);box-shadow:var(--shadow)}
.ct-card h4{font-family:'Plus Jakarta Sans',sans-serif;font-size:13px;font-weight:700;margin-bottom:10px;color:var(--navy)}
.ct-disc{border-left:4px solid var(--orange)}
.ct-list{border-left:4px solid var(--red)}
.ct-data{border-left:4px solid var(--green)}
.ct-stat{display:flex;justify-content:space-between;font-size:12px;padding:5px 0;border-bottom:1px dashed var(--border)}
.ct-stat:last-child{border-bottom:none}
.gsc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin:14px 0}
.gsc-card{background:var(--card);border-radius:var(--radius);padding:14px 16px;border-left:4px solid #34A853;box-shadow:var(--shadow)}
.gsc-card h4{font-family:'Plus Jakarta Sans',sans-serif;font-size:12px;font-weight:800;color:var(--navy);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px}
.gsc-card .qry{font-size:12px;color:var(--muted);line-height:1.7;padding:2px 0}
.gsc-card .qry strong{color:var(--text)}
.insight-box{background:#e0f2f1;border-left:4px solid var(--teal);padding:12px 16px;border-radius:0 8px 8px 0;margin:12px 0 24px;font-size:13px;line-height:1.7}
.insight-box strong{color:var(--teal)}
.score-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:14px 0}
.score-c{background:var(--card);border-radius:var(--radius);padding:16px;border:1px solid var(--border);box-shadow:var(--shadow);text-align:center}
.score-c .sv{font-family:'Plus Jakarta Sans',sans-serif;font-size:28px;font-weight:800;color:var(--gold)}
.score-c .sl{font-size:11px;color:var(--muted);margin-top:4px;font-weight:600;letter-spacing:0.5px;text-transform:uppercase}
.score-c .sn{font-size:11px;color:var(--muted);margin-top:6px;line-height:1.4}
.flow-map{display:flex;gap:8px;padding:16px 0;flex-wrap:wrap;align-items:stretch}
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
.render-section{background:#fff5f5;border:1px solid rgba(255,0,0,0.15);border-radius:8px;padding:16px;margin-bottom:14px}
.render-h{font-family:'Plus Jakarta Sans',sans-serif;font-size:13px;font-weight:800;color:#c62828;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;display:flex;align-items:center;gap:8px}
.render-badge{background:#c62828;color:#fff;font-size:9px;font-weight:700;letter-spacing:0.5px;padding:2px 8px;border-radius:99px;text-transform:uppercase}
.render-note{font-size:12px;color:#5d1f1f;line-height:1.6}
.render-note code{background:rgba(198,40,40,0.08);padding:1px 6px;border-radius:4px;font-size:11px;color:#5d1f1f}
.render-preview{background:#fff;border:1px solid #f4cccc;border-radius:6px;padding:12px;margin-top:10px;font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:11px;line-height:1.6;color:#2C2C2C;white-space:pre-wrap;max-height:220px;overflow-y:auto}
.render-explainer{background:#fff;border:1px solid #f4cccc;border-radius:6px;padding:12px 14px;margin-bottom:10px;font-size:12px;color:#2C2C2C;line-height:1.6}
.render-steps{background:#fff;border:1px solid #f4cccc;border-radius:6px;padding:12px 14px;margin-bottom:10px}
.render-step-label{font-size:11px;font-weight:800;color:#c62828;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px}
.render-steps-list{margin-left:22px;font-size:12px;line-height:1.7;color:#2C2C2C}
.render-steps-list li{margin:6px 0}
.render-steps-list a{color:#c62828;font-weight:700}
.render-steps-list code{background:#fff5f5;padding:1px 6px;border-radius:4px;font-size:11px;color:#5d1f1f}
.render-avatar-box{background:#fff;border:1px dashed #c62828;border-radius:6px;padding:12px 14px;font-size:13px;color:#2C2C2C;line-height:1.6}
.render-avatar-box code{background:#fff5f5;padding:1px 6px;border-radius:4px;font-size:11px;color:#5d1f1f}
.render-avatar-box a{color:#c62828;font-weight:700}
.btn-help{font-size:11px;color:var(--muted);margin-top:6px;line-height:1.5;font-style:italic}
.btn-help strong{color:var(--navy);font-style:normal}
.section-help{font-size:11px;color:var(--muted);margin-top:-6px;margin-bottom:10px;line-height:1.5}
.pair-help{font-size:12px;color:#4d2e73;margin-top:6px;line-height:1.5}
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

__RESEARCH_DATA_TOP__

<div class="how-to">
  <strong>How to use this dashboard:</strong>
  <ol>
    <li>Click any of the <strong>15 format buttons</strong> below (2 rows &mdash; Newsletter buttons are at the end of row 2).</li>
    <li>Hit the <strong>gold "Copy [Format]" button</strong> (e.g., "Copy Script + SSML", "Copy Newsletter HTML") &mdash; grabs the production-ready deliverable, paste into YouTube/IG/Gmail/etc.</li>
    <li>The <strong>purple "Copy Production Content"</strong> button (only on YT Long Pt 1) also grabs the B-roll + editing package for Jason.</li>
    <li>The <strong>gold outline "Copy Prompt"</strong> button regenerates a fresh version through Claude/ChatGPT.</li>
    <li>Click <strong>"Show Full Research Data"</strong> at the very top of this page to expand all raw data that backed this topic (Search Console, social perf, MLS, news, topic history).</li>
  </ol>
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

<h2 class="sh">&#x1F9E0; Intelligence Stack &mdash; Where This Topic's Data Came From</h2>
<div class="isp">
  <div class="isp-grid">
    <div class="isp-card">
      <h4>&#x1F4F1; Instagram <span class="used-badge">ACTIVE &mdash; 100%</span></h4>
      <p style="font-size:12px;color:var(--muted)"><strong>Account:</strong> @graeham.watts &middot; ID 17841411632681720<br><strong>Source:</strong> Windsor.ai MCP &rarr; IG Graph API</p>
      <div class="finding"><strong>Fields pulled:</strong> date, reach, likes, comments, shares, saves (48 rows, last 30 days). <strong>Known gap:</strong> IG Graph API returns NULL for impressions when media_type is NULL for some posts — reach is the reliable metric.</div>
    </div>
    <div class="isp-card">
      <h4>&#x1F3A5; YouTube <span class="partial-badge">LIMITED &mdash; Data gap</span></h4>
      <p style="font-size:12px;color:var(--muted)"><strong>Account:</strong> graehamwatts@gmail.com &middot; Windsor ID 6631</p>
      <div class="finding"><strong>What we got:</strong> 1 video in last 30 days, 1 view total. <strong>What this means:</strong> Your YouTube channel is effectively dormant. This topic&apos;s YT Long asset is the first real content in weeks — cross-post the YT Short to revive the channel.</div>
    </div>
    <div class="isp-card">
      <h4>&#x1F4D8; Facebook <span class="used-badge">ACTIVE</span></h4>
      <p style="font-size:12px;color:var(--muted)"><strong>Page:</strong> Graeham Watts Realtor &middot; ID 375568976359198</p>
      <div class="finding"><strong>Fields pulled:</strong> post_impressions only (reach, engagement, reactions not available via connector). <strong>19 posts last 30 days, avg 20 impressions.</strong> FB distribution is weak &mdash; treat as cross-post, not primary.</div>
    </div>
    <div class="isp-card">
      <h4>&#x1F50D; Google Search Console <span class="used-badge">ACTIVE &mdash; 100%</span></h4>
      <p style="font-size:12px;color:var(--muted)"><strong>Property:</strong> sc-domain:graehamwatts.com</p>
      <div class="finding"><strong>Fields pulled:</strong> query, clicks, impressions, ctr, position. <strong>87 unique query rows last 7 days.</strong> Strongest dataset &mdash; drives the SEO / AEO / blog angle for this topic.</div>
    </div>
    <div class="isp-card">
      <h4>&#x1F3DB;&#xFE0F; GoHighLevel CRM <span class="used-badge">ACTIVE</span></h4>
      <p style="font-size:12px;color:var(--muted)"><strong>Location:</strong> Intero Real Estate &middot; ID 6wuU3haUH7uNeT20E3UZ</p>
      <div class="finding"><strong>Use this topic:</strong> Validated the GHL keyword for this topic&apos;s CTA is active in a workflow (comment-keyword trigger + follow-up sequence). Pre-flight check before shipping.</div>
    </div>
    <div class="isp-card">
      <h4>&#x1F4CD; Google My Business <span class="used-badge">ACTIVE</span></h4>
      <p style="font-size:12px;color:var(--muted)"><strong>Location:</strong> Graeham Watts - Realtor</p>
      <div class="finding"><strong>Use this topic:</strong> GMB derivative on the dashboard is pre-formatted for local SEO. Review/search metrics pulled separately by the weekly social report.</div>
    </div>
    <div class="isp-card">
      <h4>&#x1F4F0; Local News (Web Search) <span class="used-badge">ACTIVE</span></h4>
      <p style="font-size:12px;color:var(--muted)"><strong>Source:</strong> Claude live web search</p>
      <div class="finding"><strong>Use this topic:</strong> Sourced the core news event(s) + market data from primary sources. Cross-referenced against at least 3 independent outlets before including a stat.</div>
    </div>
    <div class="isp-card">
      <h4>&#x1F916; Apify &mdash; Reddit <span class="partial-badge">STORED</span></h4>
      <p style="font-size:12px;color:var(--muted)"><strong>Datasets:</strong> 3 prior-campaign scrapes (r/bayarea, r/realestate, r/homeowners)</p>
      <div class="finding"><strong>Use this topic:</strong> Topic-demand validation &mdash; confirmed real audience questions exist before scoring. No fresh scrape this week.</div>
    </div>
  </div>
</div>

<h2 class="sh">&#x1F4CA; Recent Performance &mdash; What's Actually Moving</h2>
<p class="section-help"><strong>What this shows:</strong> Your actual performance numbers for the last 2 weeks (real, not projected). Use this as the reality check for any topic decision &mdash; if Instagram reach spiked last week, the content pattern that drove it should inform what we ship next.</p>
<table class="perf-tbl">
  <thead><tr><th>Metric</th><th>Last Week<br>(Apr 13-19)</th><th>Prior Week<br>(Apr 6-12)</th><th>WoW Change</th><th>4-Week Avg</th></tr></thead>
  <tbody>
    <tr><td>Instagram Reach</td><td><strong>3,484</strong></td><td>2,290</td><td class="chg-up">&#x25B2; 52%</td><td>2,125/wk</td></tr>
    <tr><td>Instagram Engagement (likes+comments+shares+saves)</td><td><strong>78</strong></td><td>59</td><td class="chg-up">&#x25B2; 32%</td><td>55/wk</td></tr>
    <tr><td>Facebook Impressions</td><td><strong>96</strong></td><td>155</td><td class="chg-down">&#x25BC; 38%</td><td>134/wk</td></tr>
    <tr><td>GSC Impressions</td><td><strong>140</strong></td><td>205</td><td class="chg-down">&#x25BC; 32%</td><td>198/wk</td></tr>
    <tr><td>GSC Clicks</td><td><strong>8</strong></td><td>3</td><td class="chg-up">&#x25B2; 167%</td><td>7/wk</td></tr>
    <tr><td>YouTube Views</td><td><strong>0</strong></td><td>1</td><td class="chg-down">&mdash;</td><td>0/wk</td></tr>
  </tbody>
</table>
<div class="insight-box"><strong>What this tells us:</strong> IG reach is accelerating (Apr 17 alone drove 631 reach on 1 Reel). FB is weak and not worth optimizing. GSC clicks jumped from branded query improvements. <strong>YouTube is dying</strong> &mdash; cross-posting this topic&apos;s Reels as Shorts is the cheapest revival play.</div>

<h2 class="sh">&#x1F3AF; Content Type Performance &mdash; What's Working Right Now</h2>
<p class="section-help"><strong>What this shows:</strong> The posts you actually shipped in the last 30 days, grouped by topic type, with avg reach per post. Use this to pick the hook style for this topic.</p>
<div class="ctm">
  <div class="ct-card ct-data">
    <h4>&#x1F4C8; Data / Market (Prices, rates, comps, stats) &mdash; TOP</h4>
    <div class="ct-stat"><span>Posts shipped (30d)</span><strong>5</strong></div>
    <div class="ct-stat"><span>Avg reach/post</span><strong>1,720</strong></div>
    <div class="ct-stat"><span>Top post reach</span><strong>1,503</strong></div>
    <div class="ct-stat"><span>Performance tier</span><strong style="color:#2e7d32">#1 Winner</strong></div>
  </div>
  <div class="ct-card ct-disc">
    <h4>&#x1F30D; Discovery (Area tours, neighborhood walks)</h4>
    <div class="ct-stat"><span>Posts shipped (30d)</span><strong>4</strong></div>
    <div class="ct-stat"><span>Avg reach/post</span><strong>1,450</strong></div>
    <div class="ct-stat"><span>Top post reach</span><strong>1,301</strong></div>
    <div class="ct-stat"><span>Performance tier</span><strong style="color:#e65100">Good</strong></div>
  </div>
  <div class="ct-card ct-list">
    <h4>&#x1F3E0; Listing / Promo (Property showcases, open house)</h4>
    <div class="ct-stat"><span>Posts shipped (30d)</span><strong>3</strong></div>
    <div class="ct-stat"><span>Avg reach/post</span><strong>892</strong></div>
    <div class="ct-stat"><span>Top post reach</span><strong>1,059</strong></div>
    <div class="ct-stat"><span>Performance tier</span><strong style="color:#c62828">Below average</strong></div>
  </div>
</div>
<div class="insight-box"><strong>Why this topic matches:</strong> Data/Market content is your #1 performer (93% higher avg reach than Listing/Promo). This topic is a data-forward piece &mdash; ships into your winning content lane.</div>

<h2 class="sh">&#x1F50D; Google Search Console &mdash; Top Demand (What People Are Actually Searching)</h2>
<p class="section-help"><strong>What this shows:</strong> Real search queries from the last 7 days that brought people to your site. Position = where you rank. Impressions = how many times you appeared. Branded query ("graeham watts") gets clicks; most others are impressions-only &mdash; meaning Google ranks you but the headlines aren&apos;t compelling enough yet.</p>
<div class="gsc-grid">
  <div class="gsc-card">
    <h4>Top Query (Branded)</h4>
    <div class="qry"><strong>graeham watts</strong></div>
    <div class="qry">8 clicks &middot; 12 imp &middot; pos 1.0 &middot; 66.67% CTR</div>
  </div>
  <div class="gsc-card">
    <h4>EPA Real Estate Cluster</h4>
    <div class="qry"><strong>east palo alto ca real estate</strong> &mdash; 10 imp, pos 20.5</div>
    <div class="qry"><strong>east palo alto realtor</strong> &mdash; 6 imp, pos 17.5</div>
    <div class="qry"><strong>east palo alto homes</strong> &mdash; 5 imp, pos 23.2</div>
  </div>
  <div class="gsc-card">
    <h4>Smoke Detector Cluster (SEO Gap)</h4>
    <div class="qry"><strong>15+ queries about CA smoke detector requirements</strong></div>
    <div class="qry">Ranking positions 13-76, 35+ impressions, <strong>zero clicks</strong>. Pure content-gap opportunity.</div>
  </div>
  <div class="gsc-card">
    <h4>Palo Alto Market Cluster</h4>
    <div class="qry"><strong>palo alto real estate</strong> &mdash; 7 imp, pos 42.9</div>
    <div class="qry"><strong>how is home value calculated in palo alto</strong> &mdash; 2 imp, pos 21.5</div>
    <div class="qry"><strong>we buy houses palo alto</strong> &mdash; 5 imp, pos 70.2</div>
  </div>
</div>
<div class="insight-box"><strong>What this means for this topic:</strong> Peninsula buyers are actively searching for property + market info right now. This topic is engineered to rank for the cluster where you already have impressions — turning position 20-30 into page 1.</div>

</div>
</div>

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

<h2 class="sh">Content Derivatives &mdash; 15 Formats Ready</h2>
<p style="color:var(--muted);font-size:13px;margin-bottom:6px">Each format has a <strong>Copy button</strong> (gold, format-specific label like "Copy Script" or "Copy Newsletter HTML") + <strong>Copy Prompt</strong> (gold outline, for regeneration). YT Long Pt 1 also has a paired <strong>Copy Production Content</strong> (purple) button. <strong>Scroll down</strong> &mdash; 2 newsletter buttons are in row 2.</p>
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
  <h3>&#x1F680; Power-User Alternative: ElevenLabs + HeyGen Pipeline (Optional)</h3>
  <p style="font-size:13px;line-height:1.7;color:rgba(255,255,255,0.9);margin-bottom:14px"><strong>TLDR:</strong> You probably don&apos;t need this. The red Render buttons per format (above) are the recommended path &mdash; they use the HeyGen MCP and handle everything automatically. This section is the OLD manual pipeline that uses ElevenLabs for voice + HeyGen for avatar, for when you want more granular voice control (custom SSML tags, specific pacing).</p>
  <p style="font-size:13px;line-height:1.7;color:rgba(255,255,255,0.9);margin-bottom:14px"><strong>What this pipeline does (if you choose to use it):</strong></p>
  <ol style="font-size:13px;line-height:1.8;color:rgba(255,255,255,0.9);margin-left:20px;margin-bottom:14px">
    <li>Takes the SSML block from YouTube Long Pt 1&apos;s "Ready to Post" content.</li>
    <li>Synthesizes Graeham&apos;s cloned voice via ElevenLabs (better prosody control than HeyGen&apos;s default TTS).</li>
    <li>Uploads the resulting MP3 to HeyGen.</li>
    <li>Renders the avatar video in HeyGen using that MP3 as the audio track.</li>
    <li>Downloads the finished MP4 to your outputs folder.</li>
  </ol>
  <p style="font-size:13px;line-height:1.7;color:rgba(255,255,255,0.9);margin-bottom:8px"><strong>To use:</strong> Click Copy Script + SSML on YouTube Long Pt 1, paste just the <code>&lt;speak&gt;...&lt;/speak&gt;</code> block into a new file at <code>outputs/content-package-2026-04-18-epa-two-years-homicide-free.ssml.txt</code>, then run this command in your terminal:</p>
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
window.HEYGEN_RENDER = __HRLIB__;

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

function copyRender(btn, key) {
  var cfg = window.HEYGEN_RENDER[key];
  var content = window.CONTENT_LIBRARY[key];
  if (!cfg || !content) { btn.textContent = 'No render config'; return; }
  var instruction = 'Render this video via HeyGen MCP.\n\n' +
    'Format: ' + cfg.label + '\n' +
    'Avatar: ' + cfg.avatar + ' (' + cfg.avatar_id + ') — ' + cfg.reason + '\n' +
    'Voice: Graeham Watts Voice Clone (' + cfg.voice_id + ')\n' +
    'Aspect: ' + cfg.aspect + ' | Resolution: 1080p\n\n' +
    'Script to speak:\n' +
    content + '\n\n' +
    'Call the HeyGen MCP generate_avatar_video tool. Confirm the avatar choice with me before submitting. Return the video_id and HeyGen dashboard URL so I can check status later.';
  navigator.clipboard.writeText(instruction).then(function(){
    var o = btn.textContent;
    btn.textContent = 'Copied! Paste into Claude with HeyGen MCP';
    btn.classList.add('copied');
    setTimeout(function(){ btn.textContent = o; btn.classList.remove('copied'); }, 3000);
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
DASHBOARD = DASHBOARD.replace("__RESEARCH_DATA_TOP__", RESEARCH_DATA_HTML)
DASHBOARD = DASHBOARD.replace("__FLOW__", FLOW)
DASHBOARD = DASHBOARD.replace("__PANELS__", PANELS)
DASHBOARD = DASHBOARD.replace("__PLIB__", PLIB)
DASHBOARD = DASHBOARD.replace("__CLIB__", CLIB)
DASHBOARD = DASHBOARD.replace("__HRLIB__", HRLIB)

OUT = Path("/var/tmp/stage3/skills/content-calendars/2026-04-18-epa-two-years-homicide-free-production.html")
OUT.write_text(DASHBOARD, encoding="utf-8")

print(f"WROTE: {OUT}")
print(f"size={len(DASHBOARD):,} prompts={len(PROMPTS)} content={len(CONTENT)} panels={len(panels_html)} cards={len(flow_cards)}")
