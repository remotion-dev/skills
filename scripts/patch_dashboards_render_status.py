#!/usr/bin/env python3
"""
Patch every single-topic dashboard to:
  1) Fetch render_status.json from GitHub Pages on page load
  2) Inject a completion card (embedded MP4 + download link) into each video
     format panel once the render is done.
  3) Add a "For Peter — How to Use This Dashboard" collapsible block right
     below the hero so Peter (Graeham's posting VA) has a single source of truth.

Idempotent — safe to re-run. Each injection is wrapped in a sentinel comment
that's checked before inserting.
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

RENDER_STATUS_URL = "https://graehamwatts.github.io/skills/render_status.json"

# Sentinels — we check for these before injecting, so the patch is idempotent.
SENTINEL_JS = "<!-- RENDER_STATUS_WATCHER_V1 -->"
SENTINEL_PETER = "<!-- PETER_GUIDE_V1 -->"
SENTINEL_CSS = "<!-- RENDER_STATUS_CSS_V1 -->"

# ---------------------------------------------------------------------------
# CSS for the status cards + Peter's block
# ---------------------------------------------------------------------------

CSS_BLOCK = f"""
<style>
{SENTINEL_CSS}
.rs-card {{
  margin: 12px 0 16px 0;
  padding: 14px 16px;
  border-radius: 10px;
  font-family: 'DM Sans', system-ui, sans-serif;
  font-size: 13px;
  line-height: 1.5;
  border: 1px solid transparent;
}}
.rs-card.done {{
  background: #E8F5E9;
  border-color: #2e7d32;
  color: #1b5e20;
}}
.rs-card.pending {{
  background: #FFF8E1;
  border-color: #c5a258;
  color: #6d4c00;
}}
.rs-card.failed {{
  background: #FFEBEE;
  border-color: #c62828;
  color: #8b0000;
}}
.rs-card .rs-h {{
  font-weight: 800;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 6px;
}}
.rs-card video {{
  width: 100%;
  max-width: 480px;
  border-radius: 8px;
  margin-top: 8px;
  display: block;
  background: #000;
}}
.rs-card a.rs-dl {{
  display: inline-block;
  background: #1B2A4A;
  color: #fff;
  padding: 8px 14px;
  border-radius: 6px;
  font-weight: 700;
  font-size: 12px;
  text-decoration: none;
  margin-top: 10px;
  margin-right: 8px;
}}
.rs-card a.rs-dl:hover {{ background: #0f1a30; }}
.rs-card a.rs-open {{
  color: #1B2A4A;
  font-weight: 700;
  text-decoration: underline;
  font-size: 12px;
}}
.rs-dot {{
  display: inline-block;
  width: 8px; height: 8px;
  border-radius: 50%;
  margin-right: 6px;
  vertical-align: middle;
}}
.rs-dot.done {{ background: #2e7d32; }}
.rs-dot.pending {{ background: #c5a258; animation: rsPulse 1.2s infinite ease-in-out; }}
.rs-dot.failed {{ background: #c62828; }}
@keyframes rsPulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}

/* Peter's guide */
details.peter-guide {{
  background: linear-gradient(135deg, #1B2A4A 0%, #2a3d66 100%);
  color: #fff;
  border-radius: 12px;
  margin: 20px auto;
  padding: 18px 22px;
  max-width: 1100px;
  border: 2px solid #C5A258;
  box-shadow: 0 4px 14px rgba(27,42,74,0.18);
  font-family: 'DM Sans', system-ui, sans-serif;
}}
details.peter-guide > summary {{
  list-style: none;
  cursor: pointer;
  font-size: 16px;
  font-weight: 800;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 10px;
}}
details.peter-guide > summary::-webkit-details-marker {{ display: none; }}
details.peter-guide > summary::after {{
  content: "+";
  margin-left: auto;
  font-size: 22px;
  color: #C5A258;
  font-weight: 800;
}}
details.peter-guide[open] > summary::after {{ content: "−"; }}
details.peter-guide .pg-body {{
  margin-top: 16px;
  font-size: 14px;
  line-height: 1.65;
  color: rgba(255,255,255,0.92);
}}
details.peter-guide .pg-body h3 {{
  color: #C5A258;
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 1.5px;
  margin: 18px 0 8px 0;
  font-weight: 800;
}}
details.peter-guide .pg-body ol {{
  padding-left: 22px;
}}
details.peter-guide .pg-body ol li {{
  margin-bottom: 8px;
}}
details.peter-guide .pg-body code {{
  background: rgba(0,0,0,0.35);
  color: #a5d6a7;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: ui-monospace, Consolas, monospace;
  font-size: 12px;
}}
details.peter-guide .pg-badge {{
  display: inline-block;
  background: #C5A258;
  color: #1B2A4A;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-left: 8px;
}}
</style>
"""

# ---------------------------------------------------------------------------
# Peter's instructions block — inserted right after the hero
# ---------------------------------------------------------------------------

PETER_BLOCK = f"""
{SENTINEL_PETER}
<details class="peter-guide">
  <summary>&#x1F4D8; For Peter &mdash; How to Use This Dashboard <span class="pg-badge">Read first</span></summary>
  <div class="pg-body">

    <p><strong>What this dashboard is:</strong> A single topic's complete content package. Every piece of content I want posted this week lives on this page &mdash; 15 formats across YouTube, Instagram, TikTok, Facebook, LinkedIn, the blog, GMB, and the newsletter. Your job is to copy each piece from here and post it to the right platform on the right day.</p>

    <h3>1. Posting Workflow (Daily)</h3>
    <ol>
      <li>Scroll to the <strong>7-Day Posting Calendar</strong> section &mdash; it tells you exactly what goes out today and at what time.</li>
      <li>Click the day you're working on. It jumps to that format's panel.</li>
      <li>In that panel, click the gold <strong>Copy Content</strong> (or Copy Caption / Copy Newsletter HTML / etc) button. The finished post is now on your clipboard.</li>
      <li>Open the destination platform (Instagram, YouTube, LinkedIn, etc). Paste. Attach the video or image if applicable. Publish.</li>
      <li>Mark that day's card &#x2713; done in our shared tracker.</li>
    </ol>

    <h3>2. Rendering the Videos (Graeham-Only Step)</h3>
    <p>The five video formats (YT Long Pt 1, YT Short, IG Reel 1, IG Reel 2, TikTok) are rendered by Graeham via HeyGen. You do <em>not</em> need to run PowerShell. Here's what you'll see on each video panel:</p>
    <ol>
      <li><strong>While it's rendering:</strong> a yellow &#x1F7E1; <code>Rendering...</code> card appears. Don't post this format yet &mdash; wait until it turns green.</li>
      <li><strong>Once complete:</strong> a green &#x2705; card appears with the video embedded + a <code>Download MP4</code> button + <code>Open in HeyGen</code> link. Click Download, save the file, then post to the platform listed on the panel.</li>
      <li><strong>If it failed:</strong> a red card appears with the error. Tell Graeham &mdash; don't try to re-render yourself.</li>
    </ol>
    <p><strong>Important:</strong> Status auto-updates when the page loads. If you're waiting on a render, just refresh the page every few minutes.</p>

    <h3>3. Copy Bank (Fast Lane)</h3>
    <p>If you just need the finished text for every format in one place, scroll to the <strong>Copy Bank</strong> section. Every format gets a single gold button there &mdash; one click = content on clipboard. Use this when you're batch-posting.</p>

    <h3>4. What To Never Do</h3>
    <ol>
      <li><strong>Never edit the script / SSML / caption.</strong> If you see a typo, Slack Graeham &mdash; don't fix it yourself (the version here is the source of truth, and fixing it only in the post means next week's reuse loses the fix).</li>
      <li><strong>Never use the "Copy Prompt" (outline) button.</strong> That's for regenerating with AI. You want the gold <em>Copy Content</em> button.</li>
      <li><strong>Never post before the scheduled time.</strong> The 7-Day Calendar times are based on actual IG analytics (peak windows: 6-9am, 5-8pm).</li>
      <li><strong>Never post a video that's still showing the yellow "Rendering" card.</strong> It's not ready.</li>
    </ol>

    <h3>5. Quick Reference: Format &rarr; Platform</h3>
    <ol>
      <li><strong>YT Long Pt 1 + Pt 2</strong> &rarr; YouTube (long-form, 16:9)</li>
      <li><strong>YT Short</strong> &rarr; YouTube Shorts (9:16)</li>
      <li><strong>IG Reel 1 + IG Reel 2</strong> &rarr; Instagram Reels (9:16, burn captions from panel)</li>
      <li><strong>IG Carousel</strong> &rarr; Instagram feed (10 slides, use the slide text from the panel with our Canva template)</li>
      <li><strong>TikTok</strong> &rarr; TikTok (9:16, use IG Reel 1 video)</li>
      <li><strong>Blog</strong> &rarr; Graeham's website (copy HTML/markdown)</li>
      <li><strong>GMB Post</strong> &rarr; Google Business Profile</li>
      <li><strong>Facebook</strong> &rarr; Graeham's FB page</li>
      <li><strong>LinkedIn</strong> &rarr; Graeham's LinkedIn</li>
      <li><strong>Newsletter / Full Newsletter</strong> &rarr; Mailchimp (paste HTML into Code view, NOT the visual editor)</li>
      <li><strong>Ad Copy</strong> &rarr; Meta Ads Manager (only if Graeham confirms we're boosting)</li>
      <li><strong>Production Brief</strong> &rarr; Internal reference only &mdash; do not post.</li>
    </ol>

    <h3>6. If Something Breaks</h3>
    <p>Slack Graeham with a screenshot. Don't try to fix HTML, edit scripts, or re-render videos &mdash; those all need to stay clean so next week's system works.</p>

  </div>
</details>
"""

# ---------------------------------------------------------------------------
# JavaScript render-status watcher — injected before </body>
# ---------------------------------------------------------------------------

JS_BLOCK = f"""
<script>
{SENTINEL_JS}
(function () {{
  if (!window.TOPIC_SLUG) return;
  var STATUS_URL = "{RENDER_STATUS_URL}";
  // Cache-bust with minute-precision so refreshes pick up latest status
  var bust = Math.floor(Date.now() / 60000);

  fetch(STATUS_URL + "?t=" + bust, {{ cache: "no-cache" }})
    .then(function (r) {{
      if (!r.ok) throw new Error("status fetch " + r.status);
      return r.json();
    }})
    .then(function (data) {{
      var videos = (data && data.videos) || {{}};
      // Group by format_key for current topic; keep the most recently checked one
      var byFormat = {{}};
      Object.keys(videos).forEach(function (vid) {{
        var v = videos[vid];
        if (!v || v.topic_slug !== window.TOPIC_SLUG) return;
        var fk = v.format_key;
        if (!fk) return;
        var prev = byFormat[fk];
        if (!prev || new Date(v.checked_at || 0) > new Date(prev.checked_at || 0)) {{
          byFormat[fk] = v;
        }}
      }});

      Object.keys(byFormat).forEach(function (fk) {{
        injectStatus(fk, byFormat[fk]);
      }});
    }})
    .catch(function (err) {{
      // Quietly no-op — dashboard still works without render status
      if (window.console && console.debug) console.debug("[render-status]", err.message);
    }});

  function injectStatus(formatKey, v) {{
    var panel = document.getElementById("panel-" + formatKey);
    if (!panel) return;
    // Remove any prior injection so re-fetches are idempotent
    var existing = panel.querySelector(".rs-card");
    if (existing) existing.parentNode.removeChild(existing);

    var card = document.createElement("div");
    card.className = "rs-card " + stateClass(v.status);
    card.innerHTML = buildCardHtml(v);

    // Insert at the very top of the panel (before any content)
    panel.insertBefore(card, panel.firstChild);
  }}

  function stateClass(status) {{
    if (status === "completed") return "done";
    if (status === "failed" || status === "error") return "failed";
    return "pending";
  }}

  function fmtDuration(s) {{
    if (s == null) return "";
    var sec = Math.round(Number(s));
    if (isNaN(sec)) return "";
    var m = Math.floor(sec / 60);
    var r = sec % 60;
    return m ? (m + "m " + r + "s") : (r + "s");
  }}

  function esc(s) {{
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }}

  function buildCardHtml(v) {{
    var checked = v.checked_at ? new Date(v.checked_at).toLocaleString() : "";
    if (v.status === "completed" && v.video_url) {{
      var duration = fmtDuration(v.duration);
      var dashboardUrl = "https://app.heygen.com/videos/" + encodeURIComponent(v.video_id);
      return (
        '<div class="rs-h"><span class="rs-dot done"></span>Video Ready'
          + (duration ? ' &middot; ' + esc(duration) : '')
          + '</div>'
        + '<video src="' + esc(v.video_url) + '" controls'
          + (v.thumbnail_url ? ' poster="' + esc(v.thumbnail_url) + '"' : '')
          + '></video>'
        + '<a class="rs-dl" href="' + esc(v.video_url) + '" download>&#x1F4E5; Download MP4</a>'
        + '<a class="rs-open" href="' + esc(dashboardUrl) + '" target="_blank" rel="noopener">Open in HeyGen &rarr;</a>'
        + '<div style="font-size:11px;margin-top:8px;opacity:0.7">Checked ' + esc(checked) + '</div>'
      );
    }}
    if (v.status === "failed" || v.status === "error") {{
      return (
        '<div class="rs-h"><span class="rs-dot failed"></span>Render Failed</div>'
        + '<div>' + esc(v.error || "Unknown error from HeyGen.") + '</div>'
        + '<div style="font-size:11px;margin-top:8px;opacity:0.75">video_id: <code>'
          + esc(v.video_id) + '</code> &middot; Tell Graeham to re-trigger.</div>'
      );
    }}
    // processing / pending / waiting
    var label = v.status ? String(v.status) : "queued";
    return (
      '<div class="rs-h"><span class="rs-dot pending"></span>Rendering &middot; ' + esc(label) + '</div>'
      + '<div>HeyGen is still working on this video. The page will show a playable preview once it\\'s done. Refresh in a minute or two.</div>'
      + '<div style="font-size:11px;margin-top:8px;opacity:0.75">video_id: <code>'
        + esc(v.video_id) + '</code> &middot; Last checked ' + esc(checked) + '</div>'
    );
  }}
}})();
</script>
"""

# ---------------------------------------------------------------------------
# Patch one file
# ---------------------------------------------------------------------------

def patch_file(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    original = html
    changed = []

    # 1. Inject CSS block (before </head>)
    if SENTINEL_CSS not in html:
        if "</head>" in html:
            html = html.replace("</head>", CSS_BLOCK + "\n</head>", 1)
            changed.append("css")

    # 2. Inject Peter's guide (right after the first hero section — we look for
    #    the closing of the first <div ... class="hero"> or fall back to after
    #    <body>).
    # NOTE: The first <body> occurrence is the real opening tag — that's fine.
    # But CONTENT_LIBRARY sometimes contains literal "<body>" strings in
    # embedded HTML templates, so we still anchor on the opening <body ...>
    # before anything else.
    if SENTINEL_PETER not in html:
        # Try to insert right after the hero block
        hero_close = re.search(r"(</header>|</div>\s*<!--\s*/hero\s*-->)", html)
        if hero_close:
            insert_at = hero_close.end()
            html = html[:insert_at] + "\n" + PETER_BLOCK + "\n" + html[insert_at:]
        else:
            # Fallback: insert right after the opening <body ...> tag. Use the
            # FIRST match because the document's real opening <body> always
            # comes before any CONTENT_LIBRARY-embedded HTML strings (which
            # appear deep inside the later <script> block).
            m = re.search(r"<body[^>]*>", html)
            if m:
                html = html[:m.end()] + "\n" + PETER_BLOCK + "\n" + html[m.end():]
            else:
                html = PETER_BLOCK + "\n" + html
        changed.append("peter")

    # 3. Inject render-status JS right before the LAST </body> (the document
    #    close). CONTENT_LIBRARY often contains literal "</body></html>"
    #    strings inside JS (newsletter HTML templates), so using a plain
    #    str.replace here would inject into the middle of a JS string and
    #    shatter the page. Use rsplit to target the final </body> only.
    if SENTINEL_JS not in html:
        parts = html.rsplit("</body>", 1)
        if len(parts) == 2:
            html = parts[0] + JS_BLOCK + "\n</body>" + parts[1]
            changed.append("js")

    if html != original:
        path.write_text(html, encoding="utf-8")
        return ",".join(changed) or "no-op"
    return "skip (already patched)"


def main() -> int:
    print(f"Patching {len(DASHBOARDS)} dashboards in {DASH_DIR}")
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
 