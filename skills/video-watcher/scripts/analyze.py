#!/usr/bin/env python3
"""
analyze.py — Orchestrates the visual analysis pass (Mode B).

This script does NOT call Claude itself — it prepares the input bundle that
the calling Claude reads. Claude is the multimodal model; this script just:

  1. Loads the frame manifest (from frames.py)
  2. For each frame, computes the surrounding ±15s transcript window
  3. Builds an "analysis bundle" — a structured JSON payload + frame paths

Claude (the calling skill) then iterates the bundle, reads each frame as
multimodal input alongside the surrounding transcript text, and writes
the structured per-scene notes section. Claude finally renders the full
notes-mode-b.md template with all sections filled.

Usage:
    python analyze.py --frames cache/<slug>/frames-manifest.json \
                      --transcript cache/<slug>/transcript.json \
                      --out cache/<slug>/analysis-bundle.json
"""

import argparse
import json
from pathlib import Path


def build_transcript_index(segments: list[dict]) -> list[dict]:
    """Sort segments by timestamp, return as a list (for binary-search-style window selection)."""
    return sorted(segments, key=lambda s: s['t'])


def transcript_window(transcript: list[dict], target_t: float, before: float = 15.0, after: float = 15.0) -> list[dict]:
    """Return all transcript segments within [target_t - before, target_t + after]."""
    lo = target_t - before
    hi = target_t + after
    return [s for s in transcript if lo <= s['t'] <= hi]


def fmt_ts(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    return f"{m}:{s:02d}"


def build_bundle(frames_manifest: dict, transcript: dict) -> dict:
    """
    Build the analysis bundle Claude will consume.

    Schema:
        {
            'video': {
                'duration': float,
                'transcript_method': str,
                'segment_count': int,
            },
            'frames': [
                {
                    'index': int,
                    'timestamp': float,
                    'timestamp_str': '0:23',
                    'kind': 'scene' | 'floor',
                    'frame_path': 'frames/000023.jpg',  # relative to bundle dir
                    'transcript_window': [
                        {'t': 18.5, 'text': '...'},
                        {'t': 22.3, 'text': '...'},
                        ...
                    ],
                    'window_text': 'concatenated text within the window',
                },
                ...
            ],
            'plain_transcript': str,  # full plain-text transcript for TLDR/key-concepts pass
            'instructions_for_claude': str,  # what Claude is supposed to write per frame
        }
    """
    indexed_transcript = build_transcript_index(transcript.get('segments', []))

    frames_out = []
    for i, f in enumerate(frames_manifest['frames']):
        t = f['t']
        window = transcript_window(indexed_transcript, t, before=15.0, after=15.0)
        window_text = ' '.join(s['text'] for s in window)

        frames_out.append({
            'index': i,
            'timestamp': t,
            'timestamp_str': fmt_ts(t),
            'kind': f.get('kind', 'scene'),
            'frame_path': f['path'],
            'transcript_window': window,
            'window_text': window_text,
        })

    plain = transcript.get('plain_text', ' '.join(s['text'] for s in indexed_transcript))

    instructions = """For EACH frame in the bundle, do the following:

1. READ the frame as a multimodal image input.
2. Examine: what's on screen, on-screen text, framing/composition, any people/objects/UI elements visible.
3. Cross-reference with the `window_text` (transcript ±15s around the frame's timestamp).
4. Write a brief Per-Scene Note in this format (markdown):

### Scene {index} — [{timestamp_str}]
![Frame at {timestamp_str}](frames/{filename})
**On-screen text:** {what text appears on the frame, exact transcription if any, "(none)" if blank}
**Visual:** {1-2 sentences describing what's on screen — composition, subject, style}
**Said:** {1-line quote or paraphrase of the spoken line at this moment}
**Synthesis:** {1-2 sentence interpretation of why this beat matters — what's it accomplishing?}

After all per-scene notes, write THESE summary sections by aggregating across all frames:

- **TLDR** (3-4 sentences synthesizing the whole video)
- **Hooks** section — the visual + audio + analysis of the first 0:00–0:10
- **Key Concepts** — bulleted, with timestamps
- **B-Roll Catalog** — table of shot types with timestamps and % of runtime
- **On-Screen Text Catalog** — table of every on-screen text with timestamp + style notes
- **Production Style Fingerprint** — color grade, typography, motion graphics, framing, brand signals
- **Code & Commands** — if any code/commands appear on screen, transcribe them as fenced blocks
- **Replicate-This Brief** — what would you tell HeyGen + Higgsfield to recreate this video's structure?
- **Open Questions** — anything visible that you couldn't fully interpret

Render the final markdown using the notes-mode-b.md template.
"""

    return {
        'video': {
            'duration': frames_manifest.get('video_duration'),
            'transcript_method': transcript.get('method'),
            'segment_count': transcript.get('segment_count'),
        },
        'frames': frames_out,
        'plain_transcript': plain,
        'frame_count': len(frames_out),
        'scene_change_count': sum(1 for f in frames_out if f['kind'] == 'scene'),
        'coverage_floor_count': sum(1 for f in frames_out if f['kind'] == 'floor'),
        'instructions_for_claude': instructions,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build analysis bundle for Claude vision pass')
    parser.add_argument('--frames', type=Path, required=True, help='Path to frames-manifest.json')
    parser.add_argument('--transcript', type=Path, required=True, help='Path to transcript.json')
    parser.add_argument('--out', type=Path, required=True, help='Output bundle JSON path')
    args = parser.parse_args()

    frames_manifest = json.loads(args.frames.read_text())
    transcript = json.loads(args.transcript.read_text())

    bundle = build_bundle(frames_manifest, transcript)
    args.out.write_text(json.dumps(bundle, indent=2))
    print(f"✓ Bundle written: {args.out}")
    print(f"  Frames: {bundle['frame_count']} ({bundle['scene_change_count']} scene + {bundle['coverage_floor_count']} floor)")
    print(f"  Transcript method: {bundle['video']['transcript_method']}")
