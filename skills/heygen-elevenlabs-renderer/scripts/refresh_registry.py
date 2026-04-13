#\!/usr/bin/env python3
"""
Rebuild references/registry.json by pulling live avatar + voice lists from
HeyGen (v2) and ElevenLabs. Run this anytime a new avatar or voice is trained.
"""
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CRED_DIR = Path(os.environ.get(
    "CLAUDE_CREDENTIALS_DIR",
    "/sessions/jolly-adoring-albattani/mnt/outputs/.claude-credentials"
))
OUT = Path(__file__).parent.parent / "references" / "registry.json"

def get_json(url, headers):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

def main():
    hg = (CRED_DIR / "heygen-key.txt").read_text().strip()
    el = (CRED_DIR / "elevenlabs-key.txt").read_text().strip()

    hg_av = get_json("https://api.heygen.com/v2/avatars", {"X-Api-Key": hg})
    hg_vo = get_json("https://api.heygen.com/v2/voices", {"X-Api-Key": hg})
    el_vo = get_json("https://api.elevenlabs.io/v1/voices", {"xi-api-key": el})

    avatars = hg_av.get("data", {}).get("avatars", [])
    talking = hg_av.get("data", {}).get("talking_photos", [])
    personal = [a for a in avatars if "graeham" in (a.get("avatar_name") or "").lower()]

    clone = None
    for v in el_vo.get("voices", []):
        if "graeham" in (v.get("name") or "").lower():
            clone = {"voice_id": v["voice_id"], "name": v["name"],
                     "category": v.get("category"), "labels": v.get("labels", {})}
            break

    reg = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0",
        "defaults": {
            "heygen_avatar_id": personal[0]["avatar_id"] if personal else None,
            "heygen_avatar_name": personal[0]["avatar_name"] if personal else None,
            "elevenlabs_voice_id": clone["voice_id"] if clone else None,
            "elevenlabs_voice_name": clone["name"] if clone else None,
            "elevenlabs_model": "eleven_multilingual_v2",
            "video_resolution": {"width": 1080, "height": 1920},
            "video_aspect": "9:16",
        },
        "heygen": {
            "personal_avatars_count": len(personal),
            "personal_avatars_full": [
                {"id": a["avatar_id"], "name": a.get("avatar_name"),
                 "preview": a.get("preview_image_url"),
                 "premium": a.get("premium", False)} for a in personal
            ],
        },
        "elevenlabs": {
            "graeham_voice_clone": clone,
            "total_voices": len(el_vo.get("voices", [])),
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(reg, indent=2))
    print(f"Wrote {OUT}")
    print(f"  Graeham avatars: {len(personal)}")
    print(f"  Voice clone: {clone['name'] if clone else 'MISSING'}")

if __name__ == "__main__":
    main()
