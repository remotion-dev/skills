#!/usr/bin/env python3
"""
frames.py — Scene-aware frame extraction with FFmpeg.

Two-strategy sampling:
  1. Scene-change detection (gt(scene, threshold)) — captures cuts, slide changes, B-roll switches
  2. Coverage floor (1 frame per N seconds) — ensures static segments aren't missed

Caps total frames at max_frames (default 80). Saves JPGs to <out_dir>/frames/<MMSS>.jpg.

Usage:
    python frames.py video.mp4 --out-dir cache/<slug>/ --max-frames 80 --threshold 0.3 --max-gap 45

Returns a manifest JSON describing each kept frame with its timestamp.
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


# -------------------------------------------------------------------
# Dependency checks
# -------------------------------------------------------------------

def check_ffmpeg() -> bool:
    return shutil.which('ffmpeg') is not None and shutil.which('ffprobe') is not None


def video_duration(video_path: Path) -> float:
    """Get video duration in seconds via ffprobe."""
    cmd = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', str(video_path)
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


# -------------------------------------------------------------------
# Strategy 1: Scene-change detection
# -------------------------------------------------------------------

def extract_scene_change_frames(video_path: Path,
                                 out_dir: Path,
                                 threshold: float = 0.3,
                                 resolution: int = 1280) -> list[dict]:
    """
    Extract frames at scene changes using FFmpeg's `select` filter.

    Filter: select='gt(scene,<threshold>)' — keep frames where the scene-change
    score exceeds the threshold. The scene score is the absolute frame difference
    normalized to 0-1.

    Output naming: scene_<6digit-frame-counter>.jpg
    Returns: list of {'kind': 'scene', 'path': Path, 'frame_n': int}
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    pattern = str(out_dir / 'scene_%06d.jpg')

    # vf chain: 1) scene filter, 2) scale to target width, preserving aspect
    vf = (
        f"select='gt(scene,{threshold})',"
        f"scale={resolution}:-1:flags=lanczos"
    )

    cmd = [
        'ffmpeg', '-hide_banner', '-loglevel', 'warning',
        '-i', str(video_path),
        '-vf', vf,
        '-vsync', 'vfr',
        '-frame_pts', '1',
        '-q:v', '3',  # JPEG quality (2-31, lower is better; 3 = high quality)
        pattern,
    ]
    subprocess.run(cmd, check=True)

    # FFmpeg with -vsync vfr + -frame_pts 1 names files by their *frame number*,
    # not their PTS in seconds. We need a second pass to get the PTS for each
    # surviving frame. Easier approach: re-run with showinfo and parse stderr.
    info_cmd = [
        'ffmpeg', '-hide_banner', '-i', str(video_path),
        '-vf', f"select='gt(scene,{threshold})',showinfo",
        '-f', 'null', '-',
    ]
    info = subprocess.run(info_cmd, capture_output=True, text=True)
    # Parse showinfo lines: pts_time:<float>
    import re
    pts_times = [float(m) for m in re.findall(r'pts_time:(\d+\.?\d*)', info.stderr)]

    files = sorted(out_dir.glob('scene_*.jpg'))
    out = []
    for i, f in enumerate(files):
        t = pts_times[i] if i < len(pts_times) else 0.0
        # Rename to <MMSS>.jpg using the timestamp
        new_name = out_dir / f"{int(t*100):06d}.jpg"
        if new_name.exists():
            new_name.unlink()
        f.rename(new_name)
        out.append({'kind': 'scene', 'path': new_name, 't': t})
    return out


# -------------------------------------------------------------------
# Strategy 2: Coverage floor (1 frame per N seconds)
# -------------------------------------------------------------------

def extract_coverage_floor_frames(video_path: Path,
                                   out_dir: Path,
                                   already_seen: list[float],
                                   max_gap: float = 45.0,
                                   resolution: int = 1280) -> list[dict]:
    """
    Walk the video by `max_gap` second steps. If a step lands in a region with
    no scene-change frame within `max_gap/2` seconds, grab a frame at that time.

    This ensures a video with one slide for 5 minutes gets ~7 frames (one every
    45s), not 1.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    duration = video_duration(video_path)

    # Build list of timestamps where we WANT coverage
    desired_timestamps = []
    t = max_gap / 2
    while t < duration:
        # Skip if there's already a scene frame within max_gap/2 of this point
        nearest_existing = min((abs(t - x) for x in already_seen), default=float('inf'))
        if nearest_existing > max_gap / 2:
            desired_timestamps.append(t)
        t += max_gap

    out = []
    for t in desired_timestamps:
        outfile = out_dir / f"floor_{int(t*100):06d}.jpg"
        cmd = [
            'ffmpeg', '-hide_banner', '-loglevel', 'error',
            '-ss', f'{t:.2f}', '-i', str(video_path),
            '-frames:v', '1',
            '-vf', f'scale={resolution}:-1:flags=lanczos',
            '-q:v', '3',
            '-y',
            str(outfile),
        ]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            continue
        # Rename to canonical timestamped name
        canonical = out_dir / f"{int(t*100):06d}.jpg"
        if canonical.exists():
            outfile.unlink()
            continue
        outfile.rename(canonical)
        out.append({'kind': 'floor', 'path': canonical, 't': t})
    return out


# -------------------------------------------------------------------
# Cap selection — keep best N frames
# -------------------------------------------------------------------

def cap_frames(frames: list[dict], max_frames: int) -> list[dict]:
    """
    If we exceeded max_frames, downsample by keeping the most temporally-spread set.
    Strategy: sort by timestamp, then evenly sample max_frames of them.
    """
    if len(frames) <= max_frames:
        return frames
    frames_sorted = sorted(frames, key=lambda x: x['t'])
    n = len(frames_sorted)
    step = n / max_frames
    keep_idxs = {int(i * step) for i in range(max_frames)}
    kept = [frames_sorted[i] for i in sorted(keep_idxs)][:max_frames]
    # Delete the dropped frames from disk
    keep_paths = {f['path'] for f in kept}
    for f in frames_sorted:
        if f['path'] not in keep_paths and f['path'].exists():
            f['path'].unlink()
    return kept


# -------------------------------------------------------------------
# Orchestrator
# -------------------------------------------------------------------

def extract_frames(video_path: Path,
                    out_dir: Path,
                    threshold: float = 0.3,
                    max_gap: float = 45.0,
                    max_frames: int = 80,
                    resolution: int = 1280) -> dict:
    """
    Run scene detection, then coverage floor, then cap.

    Returns:
        {
            'video_duration': float,
            'frame_count': int,
            'frames': [{'t': float, 'kind': 'scene'|'floor', 'path': str}, ...],
            'manifest_path': str,
        }
    """
    if not check_ffmpeg():
        raise RuntimeError("ffmpeg + ffprobe required. Install with `apt install ffmpeg` or `brew install ffmpeg`.")

    out_dir.mkdir(parents=True, exist_ok=True)
    duration = video_duration(video_path)

    # Strategy 1
    scene_frames = extract_scene_change_frames(video_path, out_dir, threshold=threshold, resolution=resolution)

    # Strategy 2
    seen_timestamps = [f['t'] for f in scene_frames]
    floor_frames = extract_coverage_floor_frames(
        video_path, out_dir,
        already_seen=seen_timestamps,
        max_gap=max_gap,
        resolution=resolution,
    )

    all_frames = scene_frames + floor_frames
    all_frames.sort(key=lambda x: x['t'])
    all_frames = cap_frames(all_frames, max_frames)

    # Write manifest
    manifest = {
        'video_path': str(video_path),
        'video_duration': duration,
        'extraction_params': {
            'scene_threshold': threshold,
            'max_gap_sec': max_gap,
            'max_frames': max_frames,
            'resolution': resolution,
        },
        'frame_count': len(all_frames),
        'frames': [
            {'t': f['t'], 'kind': f['kind'], 'path': str(f['path'].relative_to(out_dir))}
            for f in all_frames
        ],
    }
    manifest_path = out_dir / 'frames-manifest.json'
    manifest_path.write_text(json.dumps(manifest, indent=2))
    manifest['manifest_path'] = str(manifest_path)
    return manifest


# -------------------------------------------------------------------
# CLI entry
# -------------------------------------------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scene-aware frame extraction with FFmpeg')
    parser.add_argument('video_path', type=Path)
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--threshold', type=float, default=0.3, help='Scene-change threshold (0-1). Lower = more sensitive')
    parser.add_argument('--max-gap', type=float, default=45.0, help='Coverage-floor interval in seconds')
    parser.add_argument('--max-frames', type=int, default=80)
    parser.add_argument('--resolution', type=int, default=1280, help='Output frame width in px')
    args = parser.parse_args()

    if not args.video_path.exists():
        print(f"Video not found: {args.video_path}", file=sys.stderr)
        sys.exit(1)

    result = extract_frames(
        args.video_path,
        args.out_dir,
        threshold=args.threshold,
        max_gap=args.max_gap,
        max_frames=args.max_frames,
        resolution=args.resolution,
    )
    print(f"✓ Extracted {result['frame_count']} frames from {result['video_duration']:.1f}s video")
    print(f"  Manifest: {result['manifest_path']}")
