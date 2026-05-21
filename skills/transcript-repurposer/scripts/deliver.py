#!/usr/bin/env python3
"""
Phase 9 — Delivery: Split the content package into separable artifact files
plus render an index.html preview in the Property OS style.

Input: Final humanized content package markdown (from Phase 8)
Output: A folder containing:
  - index.html              ← Property-OS-styled preview, open in browser
  - transcript.txt          ← Raw source transcript
  - content-package.md      ← Everything in one markdown
  - hooks.md                ← 3 scored hook variants
  - script-yt-long.md       ← Long-form YouTube script
  - script-yt-short.md      ← YouTube Short
  - script-ig-reel.md       ← Instagram Reel
  - script-tiktok.md        ← TikTok
  - script-blog.md          ← Blog version
  - captions.md             ← All platform captions
  - ssml.xml                ← ElevenLabs SSML
  - heygen-script.txt       ← Paste-ready HeyGen script (shot tags stripped)
  - broll-prompts.md        ← Higgsfield image+motion prompts
  - editing-notes.md        ← For Jason the editor
  - manifest.json           ← Index of all artifacts + metadata

Usage:
    python3 deliver.py \
        --package /path/to/content-package.md \
        --transcript /path/to/source-transcript.txt \
        --slug bay-area-mortgage \
        --output-dir /path/to/output-folder
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


def split_sections(markdown: str) -> dict:
    """
    Parse the content package markdown and split into named sections.
    Section boundaries are h2 (##) headings ONLY — h3 (###) headings stay
    with their parent h2 section so we don't fragment things like
    "## Hook Variants" with three "### Hook Variant N" subsections.
    Returns a dict mapping section identifier → content.
    """
    sections = {}
    current_key = "preamble"
    current_lines = []

    for line in markdown.split("\n"):
        m2 = re.match(r"^##\s+(.+?)\s*$", line)
        if m2:
            if current_lines:
                sections[current_key] = "\n".join(current_lines).strip()
            current_key = slugify(m2.group(1).strip())
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections[current_key] = "\n".join(current_lines).strip()

    return sections


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def find_section(sections: dict, *keywords) -> str:
    """Find the first section whose key contains all keywords."""
    for key, content in sections.items():
        if all(kw in key for kw in keywords):
            return content
    return ""


def extract_ssml(text: str) -> str:
    """Pull the <speak>...</speak> block out of mixed markdown."""
    m = re.search(r"<speak>.*?</speak>", text, re.DOTALL)
    return m.group(0) if m else ""


def strip_shot_tags(script: str) -> str:
    """Remove [TALKING HEAD], [B-ROLL: ...], [TEXT OVERLAY: ...] tags
    so the result is paste-ready for HeyGen voice."""
    # Drop bracket-tagged lines entirely if the WHOLE line is a tag
    # Otherwise just strip the tag in place
    out_lines = []
    for line in script.split("\n"):
        stripped = line.strip()
        # Whole-line shot tags
        if re.match(r"^\[[^\]]+\]\s*$", stripped):
            continue
        # Inline shot tags — remove them but keep surrounding text
        cleaned = re.sub(r"\[[A-Z][A-Z\s]*(?::[^\]]+)?\]", "", line).strip()
        if cleaned:
            out_lines.append(cleaned)
    return "\n".join(out_lines)


def render_html(
    slug: str,
    package_md: str,
    transcript_text: str,
    sections: dict,
    artifacts: list,
    metadata: dict,
) -> str:
    """Render a Property-OS-styled HTML index page."""
    title = metadata.get("title", slug)
    source_url = metadata.get("source_url", "")
    platform = metadata.get("platform", "")
    duration = metadata.get("duration_sec", 0)
    word_count = metadata.get("word_count", 0)
    tier = metadata.get("tier", "")
    timestamp = metadata.get("created", datetime.now().strftime("%Y-%m-%d %H:%M"))

    # Build artifact cards
    artifact_cards = ""
    for art in artifacts:
        icon = art.get("icon", "📄")
        artifact_cards += f"""
        <a href="{art['filename']}" class="artifact-card" download>
          <div class="artifact-icon">{icon}</div>
          <div class="artifact-body">
            <div class="artifact-name">{art['name']}</div>
            <div class="artifact-desc">{art['description']}</div>
          </div>
          <div class="artifact-action">↓</div>
        </a>
        """

    # Hook section preview
    hooks_section = find_section(sections, "hook")
    hooks_preview = hooks_section[:600] + ("..." if len(hooks_section) > 600 else "")

    # Render
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Watts Content Pipeline</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif;
    background: #FAFAFA;
    color: #0A0A0A;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
  }}
  .wrap {{ max-width: 1100px; margin: 0 auto; padding: 32px 24px 80px; }}

  /* Header */
  header {{
    border-bottom: 1px solid #E5E5E5;
    padding-bottom: 24px;
    margin-bottom: 32px;
  }}
  .brand-line {{
    display: flex; align-items: center; gap: 10px;
    color: #525252; font-size: 13px; margin-bottom: 16px;
  }}
  .brand-dot {{ width: 6px; height: 6px; border-radius: 50%; background: #0A0A0A; }}
  h1 {{ font-size: 28px; font-weight: 600; letter-spacing: -0.02em; line-height: 1.2; }}
  .subtitle {{ color: #525252; font-size: 15px; margin-top: 8px; }}

  /* Meta strip */
  .meta {{
    display: flex; flex-wrap: wrap; gap: 24px;
    margin-top: 20px; padding: 16px 20px;
    background: white; border: 1px solid #E5E5E5; border-radius: 10px;
  }}
  .meta-item {{ display: flex; flex-direction: column; gap: 2px; }}
  .meta-label {{
    font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em;
    color: #737373; font-weight: 500;
  }}
  .meta-value {{ font-size: 14px; font-weight: 500; color: #0A0A0A; }}
  .meta-value.platform {{
    display: inline-block; padding: 2px 8px; background: #F5F5F5;
    border-radius: 4px; font-size: 12px;
  }}
  .meta-value a {{ color: #0A0A0A; text-decoration: none; border-bottom: 1px dashed #A3A3A3; }}
  .meta-value a:hover {{ border-bottom-style: solid; }}

  /* Section */
  section {{ margin-top: 40px; }}
  h2 {{
    font-size: 18px; font-weight: 600; letter-spacing: -0.01em;
    margin-bottom: 16px;
    display: flex; align-items: center; gap: 10px;
  }}
  h2::before {{
    content: ""; display: inline-block; width: 3px; height: 18px;
    background: #0A0A0A; border-radius: 2px;
  }}

  /* Artifact grid */
  .artifacts {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 12px; }}
  .artifact-card {{
    display: flex; align-items: center; gap: 14px;
    padding: 14px 16px; background: white;
    border: 1px solid #E5E5E5; border-radius: 10px;
    text-decoration: none; color: inherit;
    transition: all 0.15s ease;
  }}
  .artifact-card:hover {{ border-color: #0A0A0A; background: #FAFAFA; }}
  .artifact-icon {{
    width: 36px; height: 36px; flex: 0 0 36px;
    display: flex; align-items: center; justify-content: center;
    background: #F5F5F5; border-radius: 8px;
    font-size: 18px;
  }}
  .artifact-body {{ flex: 1; min-width: 0; }}
  .artifact-name {{ font-weight: 500; font-size: 14px; color: #0A0A0A; }}
  .artifact-desc {{ font-size: 12px; color: #737373; margin-top: 2px; }}
  .artifact-action {{ color: #A3A3A3; font-size: 18px; flex: 0 0 auto; }}
  .artifact-card:hover .artifact-action {{ color: #0A0A0A; }}

  /* Preview block */
  .preview {{
    background: white; border: 1px solid #E5E5E5; border-radius: 10px;
    padding: 24px; max-height: 480px; overflow-y: auto;
    font-size: 14px; line-height: 1.7;
  }}
  .preview pre {{
    white-space: pre-wrap; word-break: break-word;
    font-family: "SF Mono", Monaco, "Cascadia Code", monospace;
    font-size: 13px; color: #262626;
  }}

  /* Hooks block */
  .hooks {{
    background: white; border: 1px solid #E5E5E5; border-radius: 10px;
    padding: 24px;
  }}
  .hooks pre {{
    white-space: pre-wrap; word-break: break-word;
    font-family: "SF Mono", Monaco, monospace;
    font-size: 13px; color: #262626;
  }}

  /* Footer */
  footer {{
    margin-top: 64px; padding-top: 24px;
    border-top: 1px solid #E5E5E5;
    color: #737373; font-size: 13px;
    display: flex; justify-content: space-between; flex-wrap: wrap; gap: 12px;
  }}
  footer a {{ color: #0A0A0A; text-decoration: none; }}
  footer a:hover {{ text-decoration: underline; }}

  /* Copy button */
  .copy-btn {{
    background: white; border: 1px solid #E5E5E5; border-radius: 6px;
    padding: 6px 12px; font-size: 12px; cursor: pointer;
    color: #525252; transition: all 0.15s;
  }}
  .copy-btn:hover {{ border-color: #0A0A0A; color: #0A0A0A; }}
  .copy-btn.copied {{ background: #0A0A0A; color: white; border-color: #0A0A0A; }}
</style>
</head>
<body>
<div class="wrap">

  <header>
    <div class="brand-line">
      <div class="brand-dot"></div>
      <span>Watts Content Pipeline</span>
      <span style="color: #A3A3A3;">·</span>
      <span>Repurpose package</span>
    </div>
    <h1>{title}</h1>
    <p class="subtitle">Repurposed transcript ready for HeyGen, Higgsfield, and ElevenLabs handoff.</p>

    <div class="meta">
      <div class="meta-item">
        <div class="meta-label">Platform</div>
        <div class="meta-value"><span class="platform">{platform}</span></div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Source</div>
        <div class="meta-value">{('<a href="' + source_url + '" target="_blank">' + source_url[:48] + ('...' if len(source_url) > 48 else '') + '</a>') if source_url else '—'}</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Duration</div>
        <div class="meta-value">{duration}s</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Words</div>
        <div class="meta-value">{word_count}</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Transcription</div>
        <div class="meta-value">{tier}</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Generated</div>
        <div class="meta-value">{timestamp}</div>
      </div>
    </div>
  </header>

  <section>
    <h2>Files</h2>
    <div class="artifacts">
      {artifact_cards}
    </div>
  </section>

  <section>
    <h2>Hook variants</h2>
    <div class="hooks">
      <pre>{hooks_preview.replace('<', '&lt;').replace('>', '&gt;')}</pre>
    </div>
  </section>

  <section>
    <h2>Full package preview</h2>
    <div class="preview">
      <pre id="full-pkg">{package_md.replace('<', '&lt;').replace('>', '&gt;')}</pre>
    </div>
    <div style="margin-top: 12px; text-align: right;">
      <button class="copy-btn" onclick="copyPackage(this)">Copy full package</button>
    </div>
  </section>

  <footer>
    <div>Generated by transcript-repurposer · Property OS pipeline</div>
    <div>For Jason, Ellie, and Graeham · Watts content team</div>
  </footer>

</div>
<script>
function copyPackage(btn) {{
  const text = document.getElementById('full-pkg').innerText;
  navigator.clipboard.writeText(text).then(() => {{
    btn.classList.add('copied');
    btn.textContent = 'Copied';
    setTimeout(() => {{ btn.classList.remove('copied'); btn.textContent = 'Copy full package'; }}, 1500);
  }});
}}
</script>
</body>
</html>"""
    return html


def main():
    parser = argparse.ArgumentParser(description="Split content package into artifact files + render HTML index")
    parser.add_argument("--package", required=True, help="Path to the humanized content package markdown")
    parser.add_argument("--transcript", required=True, help="Path to the source transcript text")
    parser.add_argument("--slug", required=True, help="Short slug for the output folder")
    parser.add_argument("--output-dir", required=True, help="Where to write the artifact folder")
    parser.add_argument("--source-url", default="", help="Original video URL")
    parser.add_argument("--platform", default="", help="Source platform (youtube|instagram|tiktok|...)")
    parser.add_argument("--title", default="", help="Original video title")
    parser.add_argument("--duration-sec", type=int, default=0, help="Source video duration in seconds")
    parser.add_argument("--word-count", type=int, default=0, help="Transcript word count")
    parser.add_argument("--tier", default="whisper", help="Transcription tier used")
    args = parser.parse_args()

    pkg_path = Path(args.package)
    trans_path = Path(args.transcript)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    package_md = pkg_path.read_text(encoding="utf-8")
    transcript_text = trans_path.read_text(encoding="utf-8") if trans_path.exists() else ""

    sections = split_sections(package_md)

    # Write each artifact
    artifacts = []

    # Source transcript
    (out_dir / "transcript.txt").write_text(transcript_text, encoding="utf-8")
    artifacts.append({
        "filename": "transcript.txt", "name": "Source transcript", "icon": "📝",
        "description": "Raw transcribed text from the original video",
    })

    # Full content package (canonical)
    (out_dir / "content-package.md").write_text(package_md, encoding="utf-8")
    artifacts.append({
        "filename": "content-package.md", "name": "Full content package", "icon": "📦",
        "description": "Everything in one markdown — all derivatives + handoff blocks",
    })

    # Hooks (3 variants)
    hooks = find_section(sections, "hook")
    if hooks:
        (out_dir / "hooks.md").write_text(hooks, encoding="utf-8")
        artifacts.append({
            "filename": "hooks.md", "name": "Hook variants", "icon": "🎣",
            "description": "Three scored hook variants with the recommendation",
        })

    # YouTube Long
    yt_long = find_section(sections, "youtube", "long")
    if yt_long:
        (out_dir / "script-yt-long.md").write_text(yt_long, encoding="utf-8")
        artifacts.append({
            "filename": "script-yt-long.md", "name": "YouTube Long", "icon": "🎬",
            "description": "8-15 min long-form script with shot directions",
        })

    # YouTube Short
    yt_short = find_section(sections, "youtube", "short")
    if yt_short:
        (out_dir / "script-yt-short.md").write_text(yt_short, encoding="utf-8")
        artifacts.append({
            "filename": "script-yt-short.md", "name": "YouTube Short", "icon": "📱",
            "description": "30-59 sec vertical script for YT Shorts",
        })

    # IG Reel
    ig_reel = find_section(sections, "instagram", "reel") or find_section(sections, "reel")
    if ig_reel:
        (out_dir / "script-ig-reel.md").write_text(ig_reel, encoding="utf-8")
        artifacts.append({
            "filename": "script-ig-reel.md", "name": "Instagram Reel", "icon": "📸",
            "description": "30-60 sec Reel script with caption overlay tags",
        })

    # TikTok
    tiktok = find_section(sections, "tiktok")
    if tiktok:
        (out_dir / "script-tiktok.md").write_text(tiktok, encoding="utf-8")
        artifacts.append({
            "filename": "script-tiktok.md", "name": "TikTok", "icon": "🎵",
            "description": "30-60 sec TikTok script",
        })

    # Blog
    blog = find_section(sections, "blog")
    if blog:
        (out_dir / "script-blog.md").write_text(blog, encoding="utf-8")
        artifacts.append({
            "filename": "script-blog.md", "name": "Blog post", "icon": "📰",
            "description": "800-1200 word SEO-tuned blog version",
        })

    # ElevenLabs SSML (XML)
    ssml = extract_ssml(package_md)
    if ssml:
        (out_dir / "ssml.xml").write_text(ssml, encoding="utf-8")
        artifacts.append({
            "filename": "ssml.xml", "name": "ElevenLabs SSML", "icon": "🔊",
            "description": "XML voice markup — paste into ElevenLabs",
        })

    # HeyGen paste-ready script (script with shot tags stripped)
    if yt_long:
        heygen_clean = strip_shot_tags(yt_long)
        (out_dir / "heygen-script.txt").write_text(heygen_clean, encoding="utf-8")
        artifacts.append({
            "filename": "heygen-script.txt", "name": "HeyGen-ready script", "icon": "🎭",
            "description": "Shot tags stripped — paste into HeyGen avatar",
        })

    # Higgsfield B-roll prompts
    broll = find_section(sections, "higgsfield") or find_section(sections, "b-roll") or find_section(sections, "broll")
    if broll:
        (out_dir / "broll-prompts.md").write_text(broll, encoding="utf-8")
        artifacts.append({
            "filename": "broll-prompts.md", "name": "Higgsfield B-roll prompts", "icon": "🎥",
            "description": "Image + motion prompts for each B-roll shot",
        })

    # Editing notes (for Jason)
    edit_notes = find_section(sections, "editing", "notes") or find_section(sections, "jason")
    if edit_notes:
        (out_dir / "editing-notes.md").write_text(edit_notes, encoding="utf-8")
        artifacts.append({
            "filename": "editing-notes.md", "name": "Editing notes (Jason)", "icon": "✂️",
            "description": "Shot list, text overlay timing, pacing, thumbnail concept",
        })

    # Captions (all platforms)
    captions = find_section(sections, "caption")
    if captions:
        (out_dir / "captions.md").write_text(captions, encoding="utf-8")
        artifacts.append({
            "filename": "captions.md", "name": "Captions + hashtags", "icon": "💬",
            "description": "Per-platform captions and hashtags",
        })

    # Metadata
    metadata = {
        "title": args.title or args.slug.replace("-", " ").title(),
        "source_url": args.source_url,
        "platform": args.platform or "—",
        "duration_sec": args.duration_sec,
        "word_count": args.word_count,
        "tier": args.tier,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    # Render HTML index
    html = render_html(args.slug, package_md, transcript_text, sections, artifacts, metadata)
    (out_dir / "index.html").write_text(html, encoding="utf-8")

    # Manifest JSON
    manifest = {
        "slug": args.slug,
        "created": metadata["created"],
        "metadata": metadata,
        "artifacts": artifacts,
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"Delivered {len(artifacts)} artifacts to {out_dir}")
    print(f"Open in browser: {out_dir / 'index.html'}")



if __name__ == "__main__":
    main()
