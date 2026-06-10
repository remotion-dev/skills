#!/usr/bin/env python3
"""
build_shot_plan.py — Turn a script + content_type into a Vaibhav-style shot plan.

Given a script, a content type, and a target runtime, produces:
  - Look recommendation with reasoning
  - Timed shot plan mapping each beat to a composition mode
  - Caption sheet for the editor
  - List of B-roll prompts needed from Higgsfield
  - Ready-to-run HeyGen CLI invocation

Usage:
    python3 build_shot_plan.py --script "Your script here" --content-type market_data --runtime 60
    python3 build_shot_plan.py --from-file script.txt --content-type hot_take --runtime 90

This is a SCAFFOLDING tool — it gives you the structure. Graeham (or Claude)
still needs to refine the actual caption text, exact cut timings, and B-roll
descriptions. Think of the output as a 70%-done shot plan that you polish.
"""
from __future__ import annotations

import argparse
import dataclasses
import math
import pathlib
import sys
import textwrap


# =========================================================================
# LOOK DECISION TREE
# =========================================================================

LOOK_BY_CONTENT_TYPE = {
    "market_data":     ("warm_desk_navy",  "Everyday default. Data-driven content doesn't need gravitas — warm desk navy is recognizable and versatile."),
    "everyday":        ("warm_desk_navy",  "Default look. Casual-professional tone fits most general content."),
    "hot_take":        ("podcast_studio",  "Moody podcast grade signals 'this is a bold opinion.' The darker environment earns the gravity of a strong take."),
    "opinion":         ("podcast_studio",  "Podcast grade communicates this is commentary, not neutral reporting."),
    "lifestyle":       ("loft_window",     "Dusk loft window cue reads as 'end of workday reflection' — fits lifestyle and neighborhood storytelling."),
    "neighborhood":    ("loft_window",     "The blurred city bokeh grounds the video in 'place' without naming it explicitly."),
    "seller_facing":   ("corporate_office","Suit + tie + executive office communicates 'I'm handling something important.' Earn this look — don't use it for casual content."),
    "listing_intro":   ("corporate_office","Listing introductions are high-stakes content that benefits from executive polish."),
    "educational":     ("modern_studio",   "Clean backdrop + glasses signal 'analyst mode / about to explain something.' The visual cue primes viewers to learn."),
    "contract_explain":("modern_studio",   "White oxford + glasses = 'contract walkthrough' visual cue. Viewers learn the signifier across videos."),
    "propos_product":  ("modern_studio",   "PropertyIQ educational content fits the analyst-mode visual signature."),
}


# =========================================================================
# CUT RHYTHM ARC (from reel analysis: 80s video, 52 total cuts)
# =========================================================================
#
# Section boundaries as fractions of runtime + cut share of total:
#   Hook:   first 12% of runtime, 40% of all cuts (~0.5s shots)
#   Setup:  12-38%,                15% of all cuts (~2.5s shots)
#   Body:   38-75%,                27% of all cuts (~2.0s shots)
#   Climax: 75-88%,                13% of all cuts (~1.4s shots)
#   CTA:    last 12%,              6% of all cuts  (~3.0s shots)

SECTIONS = [
    {"name": "Hook",    "runtime_start_pct": 0.00, "runtime_end_pct": 0.12, "cut_share_pct": 0.40, "shot_len_s": 0.5},
    {"name": "Setup",   "runtime_start_pct": 0.12, "runtime_end_pct": 0.38, "cut_share_pct": 0.15, "shot_len_s": 2.5},
    {"name": "Body",    "runtime_start_pct": 0.38, "runtime_end_pct": 0.75, "cut_share_pct": 0.27, "shot_len_s": 2.0},
    {"name": "Climax",  "runtime_start_pct": 0.75, "runtime_end_pct": 0.88, "cut_share_pct": 0.13, "shot_len_s": 1.4},
    {"name": "CTA",     "runtime_start_pct": 0.88, "runtime_end_pct": 1.00, "cut_share_pct": 0.06, "shot_len_s": 3.0},
]

# Typical mode distribution per section (composition modes from SKILL.md)
MODES_BY_SECTION = {
    "Hook":   ["Mode 1 (hook composite)", "Mode 1", "Mode 2 (talking head)", "Mode 1"],
    "Setup":  ["Mode 2", "Mode 3 (full-bleed B-roll)", "Mode 2"],
    "Body":   ["Mode 2", "Mode 4 (screenshot PiP)", "Mode 3", "Mode 2", "Mode 4"],
    "Climax": ["Mode 2", "Mode 3", "Mode 2"],
    "CTA":    ["Mode 2"],
}


# =========================================================================
# SHOT PLAN BUILDER
# =========================================================================

@dataclasses.dataclass
class Shot:
    index: int
    start_s: float
    end_s: float
    section: str
    mode: str
    needs_broll: bool

def build_shot_plan(runtime_s: int) -> list[Shot]:
    shots: list[Shot] = []
    index = 1
    total_target_cuts = max(6, round(runtime_s * 52 / 80))  # scale 52 cuts from 80s reference

    for section in SECTIONS:
        start_s = section["runtime_start_pct"] * runtime_s
        end_s = section["runtime_end_pct"] * runtime_s
        n_cuts_in_section = max(1, round(total_target_cuts * section["cut_share_pct"]))
        section_duration = end_s - start_s
        shot_len = section_duration / n_cuts_in_section

        modes_for_section = MODES_BY_SECTION[section["name"]]

        for i in range(n_cuts_in_section):
            shot_start = start_s + i * shot_len
            shot_end = shot_start + shot_len
            mode = modes_for_section[i % len(modes_for_section)]
            needs_broll = "Mode 1" in mode or "Mode 3" in mode or "Mode 4" in mode
            shots.append(Shot(
                index=index,
                start_s=round(shot_start, 2),
                end_s=round(shot_end, 2),
                section=section["name"],
                mode=mode,
                needs_broll=needs_broll,
            ))
            index += 1

    return shots


# =========================================================================
# OUTPUT FORMATTING
# =========================================================================

def render_shot_plan_table(shots: list[Shot]) -> str:
    lines = []
    lines.append(f"{'#':>3}  {'Time':<12}  {'Section':<8}  {'Mode':<30}  {'B-roll?':<8}")
    lines.append("-" * 75)
    for s in shots:
        time_range = f"{s.start_s:>5.1f}–{s.end_s:<5.1f}s"
        broll_mark = "YES" if s.needs_broll else "—"
        lines.append(f"{s.index:>3}  {time_range:<12}  {s.section:<8}  {s.mode:<30}  {broll_mark:<8}")
    return "\n".join(lines)


def render_broll_todo(shots: list[Shot]) -> str:
    broll_shots = [s for s in shots if s.needs_broll]
    if not broll_shots:
        return "No B-roll required — all shots are talking head (Mode 2).\n"
    lines = [f"You need {len(broll_shots)} B-roll clips generated via higgsfield-video skill:\n"]
    for s in broll_shots:
        lines.append(f"  [{s.start_s:>5.1f}s] {s.mode} — describe the visual content here, then run through higgsfield-video")
    lines.append("\nEvery prompt must include Peninsula-specific anchors per higgsfield-video skill rules:")
    lines.append("  - flat terrain (no hills)")
    lines.append("  - San Francisco Bay visible in background")
    lines.append("  - stucco ranch homes / Silicon Valley suburban character")
    lines.append("  - name the specific neighborhood (Newbridge/Kavanaugh, The Gardens, West Side of 101)")
    return "\n".join(lines)


def render_heygen_invocation(look: str, script: str, runtime_s: int) -> str:
    return textwrap.dedent(f"""\
        # Once the shot plan above is final and the look is confirmed, render the talking-head base via heygen-video:

        python3 /mnt/skills/user/heygen-video/scripts/create.py \\
          --script {script!r} \\
          --look {look} \\
          --aspect 16:9 \\
          --title "Vaibhav template - {look} - $(date +%Y-%m-%d)"

        # The output will be a 16:9 MP4 of Graeham speaking the script at the chosen look.
        # Estimated render time: 2-10 minutes for a ~{runtime_s}s script.
        # Graeham's editor then:
        #   1. Takes the HeyGen MP4 as the talking-head base layer
        #   2. Cuts to B-roll at the times marked above
        #   3. Burns captions per references/typography.md
        #   4. Exports at 9:16 portrait for IG/TikTok (or keeps 16:9 for YouTube)
        """).strip()


# =========================================================================
# MAIN
# =========================================================================

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    script_group = p.add_mutually_exclusive_group(required=True)
    script_group.add_argument("--script", help="Script text directly on the command line.")
    script_group.add_argument("--from-file", help="Path to a text file containing the script.")
    p.add_argument("--content-type", required=True, choices=list(LOOK_BY_CONTENT_TYPE.keys()),
                   help="Content intent — determines which of the 5 looks to use.")
    p.add_argument("--runtime", type=int, default=60,
                   help="Target runtime in seconds (default: 60).")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    if args.from_file:
        script = pathlib.Path(args.from_file).read_text().strip()
    else:
        script = args.script.strip()

    look, look_reason = LOOK_BY_CONTENT_TYPE[args.content_type]
    shots = build_shot_plan(args.runtime)

    print("=" * 75)
    print("VAIBHAV TEMPLATE — SHOT PLAN")
    print("=" * 75)
    print()
    print(f"Content type:  {args.content_type}")
    print(f"Target runtime: {args.runtime}s")
    print(f"Total shots:    {len(shots)}")
    print()

    print("-" * 75)
    print("LOOK RECOMMENDATION")
    print("-" * 75)
    print(f"Use: {look}")
    print(f"Why: {look_reason}")
    print()

    print("-" * 75)
    print("SCRIPT")
    print("-" * 75)
    wrapped = textwrap.fill(script, width=73, initial_indent="  ", subsequent_indent="  ")
    print(wrapped)
    print()

    print("-" * 75)
    print("SHOT PLAN (map each beat of the script to a shot slot)")
    print("-" * 75)
    print(render_shot_plan_table(shots))
    print()
    print("NOTE: the script has been broken into timed slots above, but you")
    print("still need to assign actual caption text and B-roll content to each.")
    print("This scaffold gives you the rhythm; Claude fills in the substance.")
    print()

    print("-" * 75)
    print("B-ROLL TODO LIST")
    print("-" * 75)
    print(render_broll_todo(shots))
    print()

    print("-" * 75)
    print("HEYGEN RENDER COMMAND")
    print("-" * 75)
    print(render_heygen_invocation(look, script, args.runtime))
    print()

    print("-" * 75)
    print("REMINDERS")
    print("-" * 75)
    print("  - Typography spec: references/typography.md")
    print("  - Anti-cleft prompt formula for new B-roll of Graeham: references/prompt_formula.md")
    print("  - Look details + HeyGen IDs: references/looks.md")
    print("  - 40% of cuts go in the first 10% of runtime — this is what makes it feel fast")
    print("  - Warm face / cool background — this is the single most important grade rule")
    print("  - One look per video — never mix mid-video")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
