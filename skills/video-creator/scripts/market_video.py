#!/usr/bin/env python3
"""
Market Update / Educational Video Template — Longer-form content for
market reports, educational explainers, and data-driven presentations.

Config shape:
{
    "type": "market_update" | "explainer",
    "title": "Silicon Valley Market Update",
    "subtitle": "March 2026",
    "sections": [
        {
            "headline": "Median Home Price",
            "content": "Prices rose 4.2% year-over-year to $1.85M",
            "stat_value": "$1.85M",
            "stat_label": "Median Price",
            "stat_change": "+4.2%",
            "image": "/path/to/chart.png"   # optional
        }
    ],
    "takeaways": ["Key point 1", "Key point 2"],
    "agent_name": "Graeham Watts",
    "agent_title": "REALTOR® | DRE# 02015066",
    "agent_contact": "graehamwatts@gmail.com",
    "theme": "luxury",
    "aspect_ratio": "landscape",
}
"""

import json
import os
import sys
from typing import Dict, List

sys.path.insert(0, os.path.dirname(__file__))
from video_engine import (
    COLORS, FONT_SANS, FONT_SANS_BOLD, FONT_SERIF,
    LowerThird, Slide, TextAnimation, TextOverlay, Transition,
    VideoProject, render_video,
)


THEMES = {
    "luxury": {
        "bg_dark": (15, 25, 50),
        "bg_light": (245, 240, 230),
        "accent": (198, 168, 124),
        "text_on_dark": (255, 255, 255),
        "text_on_light": (30, 30, 30),
        "stat_color": (198, 168, 124),
        "positive": (80, 200, 120),
        "negative": (255, 100, 100),
    },
    "modern": {
        "bg_dark": (20, 20, 25),
        "bg_light": (248, 248, 252),
        "accent": (60, 130, 220),
        "text_on_dark": (255, 255, 255),
        "text_on_light": (30, 30, 40),
        "stat_color": (60, 130, 220),
        "positive": (50, 205, 130),
        "negative": (255, 85, 85),
    },
}


def create_market_video(config: Dict, output_path: str) -> str:
    """Create a market update or educational video."""
    theme_name = config.get("theme", "luxury")
    theme = THEMES.get(theme_name, THEMES["luxury"])

    ar = config.get("aspect_ratio", "landscape")
    if ar == "portrait":
        w, h = 1080, 1920
    elif ar == "square":
        w, h = 1080, 1080
    else:
        w, h = 1920, 1080

    slides = []

    # ── Title Slide ──────────────────────────────────────────────────────
    title = config.get("title", "Market Update")
    subtitle = config.get("subtitle", "")

    slides.append(Slide(
        duration=4.0,
        background_color=theme["bg_dark"],
        transition_in=Transition.FADE,
        transition_duration=0.8,
        texts=[
            TextOverlay(
                text=title.upper(),
                position=(_cx(w, w - 200), h // 2 - 80),
                font_path=FONT_SANS_BOLD,
                font_size=60 if len(title) < 30 else 46,
                color=theme["text_on_dark"],
                max_width=w - 200,
                align="center",
                animation=TextAnimation.FADE_IN,
                shadow=True,
            ),
            TextOverlay(
                text=subtitle,
                position=(_cx(w, w - 200), h // 2 + 10),
                font_path=FONT_SANS,
                font_size=30,
                color=theme["accent"],
                max_width=w - 200,
                align="center",
                animation=TextAnimation.SLIDE_UP,
            ),
        ],
    ))

    # ── Section Slides ───────────────────────────────────────────────────
    sections = config.get("sections", [])
    for i, section in enumerate(sections):
        # Alternate between dark and light backgrounds
        is_dark = i % 2 == 0
        bg = theme["bg_dark"] if is_dark else theme["bg_light"]
        text_color = theme["text_on_dark"] if is_dark else theme["text_on_light"]

        texts = []

        # Section headline
        texts.append(TextOverlay(
            text=section.get("headline", "").upper(),
            position=(120, 80) if ar == "landscape" else (80, 200),
            font_path=FONT_SANS_BOLD,
            font_size=42,
            color=theme["accent"],
            max_width=w - 240,
            animation=TextAnimation.FADE_IN,
            shadow=is_dark,
        ))

        # If there's a big stat value, show it prominently
        if section.get("stat_value"):
            texts.append(TextOverlay(
                text=section["stat_value"],
                position=(_cx(w, w - 200), h // 2 - 60),
                font_path=FONT_SANS_BOLD,
                font_size=96,
                color=theme["stat_color"],
                max_width=w - 200,
                align="center",
                animation=TextAnimation.SCALE_IN,
                shadow=is_dark,
            ))

            if section.get("stat_label"):
                texts.append(TextOverlay(
                    text=section["stat_label"],
                    position=(_cx(w, w - 200), h // 2 - 110),
                    font_path=FONT_SANS,
                    font_size=26,
                    color=text_color,
                    max_width=w - 200,
                    align="center",
                    animation=TextAnimation.FADE_IN,
                    shadow=is_dark,
                ))

            if section.get("stat_change"):
                change = section["stat_change"]
                change_color = theme["positive"] if change.startswith("+") else theme["negative"]
                texts.append(TextOverlay(
                    text=change,
                    position=(_cx(w, w - 200), h // 2 + 50),
                    font_path=FONT_SANS_BOLD,
                    font_size=40,
                    color=change_color,
                    max_width=w - 200,
                    align="center",
                    animation=TextAnimation.SLIDE_UP,
                ))

        # Content text (if no stat, or as supporting text)
        if section.get("content"):
            content_y = h // 2 + 100 if section.get("stat_value") else h // 2 - 40
            texts.append(TextOverlay(
                text=section["content"],
                position=(120, content_y) if ar == "landscape" else (80, content_y),
                font_path=FONT_SANS,
                font_size=30,
                color=text_color,
                max_width=w - 240,
                animation=TextAnimation.SLIDE_UP,
                shadow=is_dark,
                line_spacing=12,
            ))

        slide = Slide(
            duration=5.0,
            background_color=bg,
            image_path=section.get("image"),
            overlay_color=(0, 0, 0, 170) if section.get("image") else None,
            transition_in=Transition.FADE,
            transition_duration=0.5,
            texts=texts,
        )
        slides.append(slide)

    # ── Key Takeaways ────────────────────────────────────────────────────
    takeaways = config.get("takeaways", [])
    if takeaways:
        slides.append(Slide(
            duration=6.0,
            background_color=theme["bg_light"],
            transition_in=Transition.FADE,
            transition_duration=0.5,
            texts=[
                TextOverlay(
                    text="KEY TAKEAWAYS",
                    position=(120, 80) if ar == "landscape" else (80, 200),
                    font_path=FONT_SANS_BOLD,
                    font_size=44,
                    color=theme["text_on_light"],
                    animation=TextAnimation.FADE_IN,
                    shadow=False,
                ),
                TextOverlay(
                    text="\n".join(f"→  {t}" for t in takeaways),
                    position=(140, 170) if ar == "landscape" else (80, 300),
                    font_path=FONT_SANS,
                    font_size=30,
                    color=theme["text_on_light"],
                    max_width=w - 280,
                    animation=TextAnimation.SLIDE_UP,
                    shadow=False,
                    line_spacing=20,
                ),
            ],
        ))

    # ── CTA / Agent Slide ────────────────────────────────────────────────
    agent_name = config.get("agent_name", "")
    agent_title = config.get("agent_title", "")
    agent_contact = config.get("agent_contact", "")

    cta_texts = []
    if agent_name:
        cta_texts.append(TextOverlay(
            text=agent_name,
            position=(_cx(w, w - 600), h // 2 - 60),
            font_path=FONT_SANS_BOLD,
            font_size=48,
            color=theme["text_on_dark"],
            max_width=600,
            align="center",
            animation=TextAnimation.FADE_IN,
            shadow=True,
        ))
    if agent_title:
        cta_texts.append(TextOverlay(
            text=agent_title,
            position=(_cx(w, w - 600), h // 2 + 10),
            font_path=FONT_SANS,
            font_size=26,
            color=theme["accent"],
            max_width=600,
            align="center",
            animation=TextAnimation.SLIDE_UP,
        ))
    if agent_contact:
        cta_texts.append(TextOverlay(
            text=agent_contact,
            position=(_cx(w, w - 600), h // 2 + 50),
            font_path=FONT_SANS,
            font_size=24,
            color=(180, 180, 180),
            max_width=600,
            align="center",
            animation=TextAnimation.FADE_IN,
        ))

    slides.append(Slide(
        duration=4.0,
        background_color=theme["bg_dark"],
        transition_in=Transition.FADE,
        transition_duration=0.8,
        texts=cta_texts,
    ))

    # ── Render ───────────────────────────────────────────────────────────
    project = VideoProject(
        slides=slides,
        width=w,
        height=h,
        fps=30,
        output_path=output_path,
        background_music=config.get("background_music"),
        music_volume=config.get("music_volume", 0.3),
    )

    def progress(current, total):
        pct = int(current / total * 100)
        if pct % 10 == 0:
            print(f"  Rendering: {pct}%", flush=True)

    return render_video(project, progress_callback=progress)


def _cx(w, content_w):
    return (w - content_w) // 2


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default="market_video.mp4")
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)
    create_market_video(config, args.output)
