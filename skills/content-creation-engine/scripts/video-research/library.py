#!/usr/bin/env python3
"""
library.py — Slug computation, cache management, and Obsidian vault save.

Each processed video gets a directory under the Obsidian vault:

    Research/Videos/<channel>/<slug>/
    ├── notes.md           # The structured notes file (Mode A or Mode B)
    ├── transcript.json    # Raw transcript data
    ├── transcript.txt     # Plain-text transcript backup
    ├── meta.json          # Source URL, focus range, mode, etc.
    └── frames/            # Mode B only — JPGs referenced in notes.md

Slug format: YYYY-MM-DD-<title-slug>-<short-hash>
where short-hash = sha1(source_url + focus_range)[:6]

Re-running same URL + same focus range → cache hit (read existing notes.md).
"""

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


# Default Obsidian vault path. Override with env var OBSIDIAN_VAULT.
DEFAULT_VAULT = Path(r"C:\Users\Graeham Watts\Documents\Obsidian\PropIQ")


# -------------------------------------------------------------------
# Slug computation
# -------------------------------------------------------------------

def slugify(title: str, max_len: int = 50) -> str:
    """Convert a title to a filesystem-safe slug."""
    if not title:
        title = "untitled"
    # Lowercase, replace non-alphanumeric with hyphens, collapse hyphens
    s = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    return s[:max_len].rstrip('-') or "untitled"


def compute_slug(title: str, source_url: str, focus_range: str = "", date: datetime | None = None) -> str:
    """
    Compute the cache slug for a video.

    Format: YYYY-MM-DD-<title-slug>-<short-hash>

    The short_hash is derived from source_url + focus_range so that:
    - Same URL + same range = same slug (cache hit)
    - Same URL + different range = different slug (separate notes)
    """
    if date is None:
        date = datetime.now(timezone.utc)
    date_str = date.strftime("%Y-%m-%d")
    title_slug = slugify(title)
    hash_input = f"{source_url}|{focus_range}".encode("utf-8")
    short_hash = hashlib.sha1(hash_input).hexdigest()[:6]
    return f"{date_str}-{title_slug}-{short_hash}"


# -------------------------------------------------------------------
# Vault path management
# -------------------------------------------------------------------

def get_vault_root(custom: str | None = None) -> Path:
    """Resolve the Obsidian vault root from arg or env."""
    import os
    if custom:
        return Path(custom)
    env = os.environ.get("OBSIDIAN_VAULT")
    if env:
        return Path(env)
    return DEFAULT_VAULT


def get_video_cache_dir(vault_root: Path, channel: str, slug: str) -> Path:
    """
    Return the per-video directory under the vault.
    Creates parents as needed (but doesn't create the dir itself yet).
    """
    channel_safe = slugify(channel) if channel else "_unknown-channel"
    return vault_root / "Research" / "Videos" / channel_safe / slug


# -------------------------------------------------------------------
# Cache check
# -------------------------------------------------------------------

def cache_hit(cache_dir: Path) -> bool:
    """Return True if a cached notes.md exists for this slug."""
    return (cache_dir / "notes.md").exists() and (cache_dir / "meta.json").exists()


def read_cached_notes(cache_dir: Path) -> dict:
    """Return cached notes content + metadata."""
    notes_md = (cache_dir / "notes.md").read_text(encoding="utf-8")
    meta = json.loads((cache_dir / "meta.json").read_text(encoding="utf-8"))
    return {"notes_md": notes_md, "meta": meta, "from_cache": True}


# -------------------------------------------------------------------
# Save to vault
# -------------------------------------------------------------------

def save_to_vault(cache_dir: Path,
                   notes_md: str,
                   transcript: dict,
                   meta: dict,
                   frames_src_dir: Path | None = None) -> dict:
    """
    Persist all artifacts to the vault directory.

    - notes.md         (structured notes file)
    - transcript.json  (raw transcript data)
    - transcript.txt   (plain-text backup)
    - meta.json        (cache key, source URL, mode, etc.)
    - frames/          (Mode B only — copy from frames_src_dir)
    """
    cache_dir.mkdir(parents=True, exist_ok=True)

    (cache_dir / "notes.md").write_text(notes_md, encoding="utf-8")
    (cache_dir / "transcript.json").write_text(
        json.dumps(transcript, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (cache_dir / "transcript.txt").write_text(
        transcript.get("plain_text", ""), encoding="utf-8"
    )
    (cache_dir / "meta.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8"
    )

    # Copy frames if Mode B
    if frames_src_dir and frames_src_dir.exists():
        frames_dst = cache_dir / "frames"
        frames_dst.mkdir(exist_ok=True)
        for f in frames_src_dir.glob("*.jpg"):
            shutil.copy2(f, frames_dst / f.name)

    return {
        "vault_path": str(cache_dir),
        "notes_path": str(cache_dir / "notes.md"),
        "frames_count": len(list((cache_dir / "frames").glob("*.jpg"))) if (cache_dir / "frames").exists() else 0,
    }


# -------------------------------------------------------------------
# Update vault index
# -------------------------------------------------------------------

def check_obsidian_sync(vault_root: Path) -> dict:
    """
    Check whether Obsidian Sync is configured on this vault. Returns a dict
    describing the state — the caller can warn the user when Mode B runs and
    Sync isn't set up properly.

    Sync state is stored in <vault>/.obsidian/sync.json. If absent, Sync is
    not configured at all. If present, it contains the sync type toggles.
    """
    obs_dir = vault_root / ".obsidian"
    if not obs_dir.exists():
        # Try parent (sometimes the vault root is one level up)
        if (vault_root.parent / ".obsidian").exists():
            obs_dir = vault_root.parent / ".obsidian"

    sync_json = obs_dir / "sync.json"
    state = {
        "obsidian_dir_found": obs_dir.exists(),
        "sync_configured": False,
        "image_sync_enabled": None,  # unknown
        "warnings": [],
    }

    if not obs_dir.exists():
        state["warnings"].append(
            "No .obsidian config folder found near the vault. "
            "Is this actually an Obsidian vault?"
        )
        return state

    if not sync_json.exists():
        state["warnings"].append(
            "Obsidian Sync is NOT configured (no sync.json found). "
            "Notes will only exist on this machine. To enable cross-device sync: "
            "open Obsidian → Settings → Sync → Connect."
        )
        return state

    state["sync_configured"] = True
    try:
        import json as _json
        cfg = _json.loads(sync_json.read_text(encoding="utf-8"))
        # Image sync flag varies by Obsidian version. Try the common keys.
        img = cfg.get("syncImage", cfg.get("syncImages", cfg.get("image", None)))
        state["image_sync_enabled"] = img
        if img is False:
            state["warnings"].append(
                "Obsidian Sync 'Images' is OFF. Mode B frame screenshots "
                "won't sync to other devices. Enable: Settings → Sync → "
                "Sync types → Images."
            )
    except Exception as e:
        state["warnings"].append(f"Could not parse sync.json: {e}")

    return state


def update_vault_index(vault_root: Path, channel: str, slug: str, title: str,
                        mode: str, duration: str, captured: str) -> Path:
    """
    Append a line to Research/Videos/_index.md so all processed videos are
    discoverable from one place.
    """
    index_path = vault_root / "Research" / "Videos" / "_index.md"
    index_path.parent.mkdir(parents=True, exist_ok=True)

    if not index_path.exists():
        index_path.write_text(
            "# Video Research Index\n\n"
            "All videos processed by `video-research-engine`. "
            "Newest first.\n\n"
            "| Captured | Channel | Title | Mode | Length |\n"
            "|---|---|---|---|---|\n",
            encoding="utf-8",
        )

    channel_safe = slugify(channel) if channel else "_unknown-channel"
    rel_path = f"{channel_safe}/{slug}/notes.md"
    line = (
        f"| {captured[:10]} | {channel} | "
        f"[[{rel_path}|{title}]] | {mode} | {duration} |\n"
    )

    # Insert after the table header (line 5)
    content = index_path.read_text(encoding="utf-8")
    lines = content.splitlines(keepends=True)
    if len(lines) >= 5:
        lines.insert(5, line)
    else:
        lines.append(line)
    index_path.write_text("".join(lines), encoding="utf-8")
    return index_path


# -------------------------------------------------------------------
# Public entry
# -------------------------------------------------------------------

def store_video_notes(*,
                       title: str,
                       channel: str,
                       source_url: str,
                       focus_range: str,
                       mode: str,
                       duration: str,
                       notes_md: str,
                       transcript: dict,
                       frames_src_dir: Path | None = None,
                       vault_root: Path | None = None) -> dict:
    """
    Top-level: compute slug, write everything to the vault, update the index.
    Returns a summary dict the caller can show the user.
    """
    if vault_root is None:
        vault_root = get_vault_root()

    slug = compute_slug(title, source_url, focus_range)
    cache_dir = get_video_cache_dir(vault_root, channel, slug)

    captured = datetime.now(timezone.utc).isoformat()
    meta = {
        "slug": slug,
        "title": title,
        "channel": channel,
        "source_url": source_url,
        "focus_range": focus_range,
        "mode": mode,
        "duration": duration,
        "captured": captured,
        "transcript_method": transcript.get("method"),
    }

    save_result = save_to_vault(
        cache_dir=cache_dir,
        notes_md=notes_md,
        transcript=transcript,
        meta=meta,
        frames_src_dir=frames_src_dir,
    )
    update_vault_index(vault_root, channel, slug, title, mode, duration, captured)

    # Check Obsidian Sync state and surface warnings, especially for Mode B
    sync_state = check_obsidian_sync(vault_root)
    sync_warnings = sync_state.get("warnings", [])
    if mode == "frame-by-frame" and not sync_state.get("sync_configured"):
        sync_warnings.insert(0,
            "[Mode B] Frames will only exist on this machine until Sync is on.")

    return {
        "from_cache": False,
        "slug": slug,
        "vault_path": str(cache_dir),
        "notes_path": save_result["notes_path"],
        "frames_count": save_result["frames_count"],
        "sync_state": sync_state,
        "sync_warnings": sync_warnings,
    }


# -------------------------------------------------------------------
# CLI entry
# -------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vault save + cache check")
    parser.add_argument("--check-cache", action="store_true")
    parser.add_argument("--check-sync", action="store_true")
    parser.add_argument("--title", default="")
    parser.add_argument("--channel", default="")
    parser.add_argument("--url", default="")
    parser.add_argument("--focus-range", default="")
    parser.add_argument("--vault-root", default=None)
    args = parser.parse_args()

    vault = get_vault_root(args.vault_root)

    if args.check_sync:
        import json as _j
        print(_j.dumps(check_obsidian_sync(vault), indent=2))
    elif args.check_cache:
        slug = compute_slug(args.title, args.url, args.focus_range)
        cache_dir = get_video_cache_dir(vault, args.channel, slug)
        print(f"{'HIT' if cache_hit(cache_dir) else 'MISS'}  {cache_dir}")
    else:
        slug = compute_slug(args.title, args.url, args.focus_range)
        cache_dir = get_video_cache_dir(vault, args.channel, slug)
        print(f"SLUG {slug}")
        print(f"PATH {cache_dir}")
