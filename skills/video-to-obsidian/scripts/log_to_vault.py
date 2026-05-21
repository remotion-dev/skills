#!/usr/bin/env python3
"""
log_to_vault.py — Video URL -> Obsidian vault note for Graeham Watts.

Takes ANY video URL (Instagram, YouTube, Shorts, TikTok, etc.), transcribes it
via video-transcriber, auto-categorizes it, and writes a clean markdown note to
the Obsidian vault at Documents/Obsidian/Instagram Saves/.

The source URL is ALWAYS preserved in frontmatter. Non-negotiable.

Usage:
    python3 log_to_vault.py "https://www.instagram.com/reels/ABC/"
    python3 log_to_vault.py "URL" --folder "Hook Library" --my-use steal-hook
    python3 log_to_vault.py "URL" --metadata-json '{"engagement":{"views":12000}}'
    python3 log_to_vault.py "URL" --update      # update engagement stats only
    python3 log_to_vault.py "URL" --force       # overwrite even if exists
    python3 log_to_vault.py "URL" --dry-run     # show what would be written
    python3 log_to_vault.py "URL" --transcript-text "..."  # skip transcription
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def find_vault_root():
    candidates = [
        Path("/sessions/gifted-elegant-ritchie/mnt/Obsidian/Instagram Saves"),
        Path(r"C:\Users\Graeham Watts\Documents\Obsidian\Instagram Saves"),
        Path.home() / "Documents" / "Obsidian" / "Instagram Saves",
    ]
    for c in candidates:
        if c.exists():
            return c
    return candidates[0]


VAULT_ROOT = find_vault_root()
SKILLS_ROOT = Path(__file__).resolve().parents[3]
TRANSCRIBER_SCRIPT = SKILLS_ROOT / "skills" / "video-transcriber" / "scripts" / "transcribe.py"

FOLDERS = {
    "ai":     "AI & Tech Tutorials",
    "re":     "Real Estate Content",
    "howto":  "How-To Videos",
    "hook":   "Hook Library",
    "clone":  "Examples to Clone",
    "style":  "Style References",
    "inbox":  "_Inbox",
    "misc":   "Misc",
}


def detect_source(url):
    u = url.lower()
    if "instagram.com" in u: return "instagram"
    if "youtube.com" in u or "youtu.be" in u: return "youtube"
    if "tiktok.com" in u: return "tiktok"
    if "vimeo.com" in u: return "vimeo"
    if "twitter.com" in u or "x.com" in u: return "twitter"
    if "facebook.com" in u or "fb.watch" in u: return "facebook"
    if "linkedin.com" in u: return "linkedin"
    return "other"


def detect_post_type(url, source, duration_sec=0):
    u = url.lower()
    if source == "instagram":
        if "/reel" in u: return "reel"
        if "/p/" in u: return "carousel" if duration_sec == 0 else "reel"
        return "post"
    if source == "youtube":
        if "/shorts/" in u: return "short"
        return "video"
    return "video"


def transcribe_url(url):
    if not TRANSCRIBER_SCRIPT.exists():
        return {"error": f"video-transcriber not found at {TRANSCRIBER_SCRIPT}"}
    cmd = [sys.executable, str(TRANSCRIBER_SCRIPT), url, "--json"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if result.returncode != 0:
        return {"error": result.stderr[:500]}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": "Transcriber returned non-JSON output"}


AI_KEYWORDS = ["ai", "claude", "chatgpt", "gpt", "openai", "anthropic", "llm",
               "n8n", "mcp", "automation", "codex", "prompt", "agent",
               "machine learning", "neural"]
RE_KEYWORDS = ["real estate", "realtor", "listing", "mls", "home buying",
               "home buyer", "mortgage", "bay area", "peninsula", "east palo alto",
               "redwood city", "menlo park", "palo alto", "san mateo",
               "open house", "broker", "escrow"]


def folder_for(transcript_text, caption, source, explicit_folder, my_use):
    if explicit_folder: return explicit_folder
    if "hook-only" in my_use or "steal-hook" in my_use: return FOLDERS["hook"]
    if "full-clone" in my_use: return FOLDERS["clone"]
    if "style-ref" in my_use: return FOLDERS["style"]
    blob = (transcript_text + " " + caption).lower()
    if any(k in blob for k in AI_KEYWORDS): return FOLDERS["ai"]
    if any(k in blob for k in RE_KEYWORDS): return FOLDERS["re"]
    first_line = transcript_text.strip().split(".")[0].lower() if transcript_text else ""
    if any(s in first_line for s in ["how to", "here's how", "step 1", "tutorial", "the way to"]):
        return FOLDERS["howto"]
    return FOLDERS["inbox"]


def auto_content_types(transcript, caption, duration_sec):
    tags = []
    blob = (transcript + " " + caption).lower()
    first_line = transcript.strip().split(".")[0].lower() if transcript else ""
    if any(s in first_line for s in ["how to", "here's how", "step 1", "tutorial"]): tags.append("how-to")
    if any(k in blob for k in AI_KEYWORDS): tags.append("ai-workflow")
    if duration_sec and duration_sec < 90 and re.search(r"\b(i|my|let me|i'm|i'll)\b", first_line):
        tags.append("talking-head")
    if sum(blob.count(w) for w in ["first", "then", "next", "finally"]) >= 3: tags.append("walkthrough")
    if any(k in blob for k in [" vs ", " versus ", "compared to", "better than"]): tags.append("comparison")
    if re.search(r"\btop \d+\b|\b\d+ ways\b|\b\d+ tips\b|\bbest \d+\b", blob): tags.append("list")
    return sorted(set(tags))


def auto_hook_patterns(transcript):
    if not transcript: return []
    first = transcript.strip().split(".")[0].lower()
    tags = []
    if re.match(r"^(stop|don't|never|wrong|nobody|forget)\b", first): tags.append("pattern-interrupt")
    if any(p in first for p in ["most people think", "everyone says", "the truth is",
                                 "might be the most pointless", "this is wrong"]):
        tags.append("contrarian")
    if any(p in first for p in ["you won't believe", "the secret", "nobody talks about",
                                 "what they don't tell you", "the truth about"]):
        tags.append("curiosity-gap")
    if first.endswith("?"): tags.append("question-hook")
    if re.match(r"^here'?s how\b", first): tags.append("direct-promise")
    return sorted(set(tags))


def auto_topic_tags(caption, transcript):
    tags = set()
    for m in re.findall(r"#(\w+)", caption or ""): tags.add(m.lower())
    blob = (transcript or "").lower()
    keyword_map = {
        "ai": ["ai", "artificial intelligence"],
        "claude-code": ["claude code"],
        "real-estate": ["real estate", "realtor"],
        "bay-area": ["bay area", "peninsula"],
        "content": ["content", "post", "reel"],
        "automation": ["automation", "automate", "workflow"],
        "notion": ["notion"],
        "obsidian": ["obsidian"],
    }
    for tag, keywords in keyword_map.items():
        if any(k in blob for k in keywords): tags.add(tag)
    return sorted(tags)


def slugify(text, max_len=60):
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return s[:max_len] or "untitled"


def render_note(data):
    fm = {
        "url": data["url"], "source": data["source"],
        "creator": data.get("creator") or "@unknown",
        "creator_followers": data.get("creator_followers", 0),
        "post_type": data["post_type"], "post_date": data.get("post_date") or "",
        "saved_date": data["saved_date"], "duration_sec": data.get("duration_sec", 0),
        "content_type": data.get("content_type", []),
        "hook_pattern": data.get("hook_pattern", []),
        "topic_tags": data.get("topic_tags", []),
        "my_use": data.get("my_use", ["reference-only"]),
        "saved_for": data.get("saved_for", []),
        "engagement": data.get("engagement", {"views": 0, "likes": 0, "comments": 0, "saves": None, "engagement_rate": 0.0}),
        "status": data.get("status", "unprocessed"),
        "transcript_available": data.get("transcript_available", True),
        "discovered_via": data.get("discovered_via", "manual"),
    }

    def yaml_value(v):
        if isinstance(v, list):
            return "[" + ", ".join(yaml_value(x) for x in v) + "]"
        if isinstance(v, dict):
            return "\n  " + "\n  ".join(f"{k}: {yaml_value(val)}" for k, val in v.items())
        if isinstance(v, str):
            return f'"{v}"' if any(c in v for c in ": #@&*?|>%{}[],") else v
        if v is None: return "null"
        return str(v)

    fm_lines = ["---"]
    for k, v in fm.items():
        fm_lines.append(f"{k}: {yaml_value(v)}")
    fm_lines.append("---")
    fm_block = "\n".join(fm_lines)

    transcript = data.get("transcript", "")
    first_sentence = transcript.strip().split(".")[0].strip() + "." if transcript else ""
    title = data.get("title") or f"{fm['creator']} — {fm['post_date'] or 'undated'}"
    platform_name = data["source"].title()

    body = f"""

# {title}

## Hook (first 3 seconds)

> {first_sentence}

## Why saved

{data.get('why_saved') or f"Logged via {fm['discovered_via']}"}

## Transcript

{transcript if transcript else '_(Transcription failed — see source URL.)_'}

## Visual notes

_(Add your notes about cuts, captions, on-screen text, style — transcripts don't capture this.)_

## Action

- [ ] Use this for: ____
- [ ] Pair with skill: ____
- [ ] Output target: ____

---

**Source:** [Watch on {platform_name}]({fm['url']})
"""
    return fm_block + body


def find_existing_note(vault_root, url):
    if not vault_root.exists(): return None
    for p in vault_root.rglob("*.md"):
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        m = re.search(r"^url:\s*(\S+)", content, re.MULTILINE)
        if m and m.group(1).strip().strip('"') == url:
            return p
    return None


def main():
    parser = argparse.ArgumentParser(description="Log a video URL to Obsidian vault")
    parser.add_argument("url")
    parser.add_argument("--folder", default=None)
    parser.add_argument("--my-use", default="reference-only")
    parser.add_argument("--saved-for", default="")
    parser.add_argument("--why", default="")
    parser.add_argument("--metadata-json", default="")
    parser.add_argument("--update", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--vault-root", default=str(VAULT_ROOT))
    parser.add_argument("--transcript-text", default=None)
    args = parser.parse_args()

    if not args.url:
        print("ERROR: URL is required", file=sys.stderr); sys.exit(1)

    vault_root = Path(args.vault_root)
    existing = find_existing_note(vault_root, args.url)
    if existing and not (args.update or args.force or args.dry_run):
        print(f"[skip] URL already in vault: {existing}", file=sys.stderr)
        print(str(existing)); return

    extra = {}
    if args.metadata_json:
        try: extra = json.loads(args.metadata_json)
        except json.JSONDecodeError as e:
            print(f"ERROR: --metadata-json is not valid JSON: {e}", file=sys.stderr); sys.exit(1)

    if args.transcript_text:
        print(f"[transcribe] using pre-supplied transcript ({len(args.transcript_text)} chars)", file=sys.stderr)
        t = {"transcript_plain": args.transcript_text}
    else:
        print(f"[transcribe] {args.url}", file=sys.stderr)
        t = transcribe_url(args.url)

    transcript_text = t.get("transcript_plain", "") if "error" not in t else ""
    title = t.get("title") or extra.get("title")
    duration = t.get("duration_sec") or extra.get("duration_sec") or 0
    creator = extra.get("creator") or (t.get("uploader") and f"@{t['uploader']}") or "@unknown"
    post_date = extra.get("post_date") or (t.get("upload_date") and f"{t['upload_date'][:4]}-{t['upload_date'][4:6]}-{t['upload_date'][6:8]}")
    caption = extra.get("caption", "")

    source = detect_source(args.url)
    post_type = detect_post_type(args.url, source, duration)
    my_use = [s.strip() for s in args.my_use.split(",") if s.strip()]
    saved_for = [s.strip() for s in args.saved_for.split(",") if s.strip()]

    content_type = auto_content_types(transcript_text, caption, duration)
    hook_pattern = auto_hook_patterns(transcript_text)
    topic_tags = auto_topic_tags(caption, transcript_text)

    folder_name = folder_for(transcript_text, caption, source, args.folder, my_use)
    target_dir = vault_root / folder_name
    target_dir.mkdir(parents=True, exist_ok=True)

    data = {
        "url": args.url, "source": source, "creator": creator,
        "creator_followers": extra.get("creator_followers", 0),
        "post_type": post_type, "post_date": post_date,
        "saved_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "duration_sec": duration, "content_type": content_type,
        "hook_pattern": hook_pattern, "topic_tags": topic_tags,
        "my_use": my_use, "saved_for": saved_for,
        "engagement": extra.get("engagement", {"views": 0, "likes": 0, "comments": 0, "saves": None, "engagement_rate": 0.0}),
        "status": "unprocessed", "transcript_available": bool(transcript_text),
        "discovered_via": extra.get("discovered_via", "manual"),
        "transcript": transcript_text, "title": title, "why_saved": args.why,
    }

    date_part = data["saved_date"]
    slug_part = slugify(title or creator.lstrip("@") or "video")
    filename = f"{date_part}-{slug_part}.md"

    target_path = existing if (existing and args.update) else (target_dir / filename)
    note = render_note(data)

    if args.dry_run:
        print(f"[dry-run] Would write to: {target_path}")
        print(note); return

    target_path.write_text(note, encoding="utf-8")
    print(f"[written] {target_path}", file=sys.stderr)
    print(str(target_path))


if __name__ == "__main__":
    main()
