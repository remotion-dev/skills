#!/usr/bin/env python3
"""
Social Media Video Template — Short-form vertical videos for Reels/Shorts/TikTok.
Designed for real estate tips, market stats, quick property teasers.

Usage:
    python3 social_video.py --config social_config.json --output reel.mp4

Config shape:
{
    "type": "tips" | "stats" | "teaser" | "quote",
    "headline": "3 Things Buyers Miss",
    "items": ["Item 1", "Item 2", "Item 3"],
    "stats": [{"label": "Median Price", "value": "$1.2M", "change": "+5.2%"}],
    "background_image": "/path/to/image.jpg",  # optional
    "agent_name": "Graeham Watts",
    "agent_handle": "@graehamwatts",
    "theme": "luxury",
    "aspect_ratio": "portrait",  # portrait (default), landscape, square
}
"""

import json
import os
import sys
from typing import Dict, List

sys.path.insert(0, os.path.dirname(__file__))
from video_engine import (
    COLORS, FONT_SANS, FONT_SANS_BOLD, FONT_SERIF, FONT_SERIF_BOLD,
    LowerThird, Slide, TextAnimation, TextOverlay, Transition,
    VideoProject, render_video,
)


THEMES = {
    "luxury": {
        "bg": (15, 25, 50),
        "accent": (198, 168, 124),
        "text": (255, 255, 255),
        "highlight_bg": (198, 168, 124, 220),
        "card_bg": (25, 40, 70, 220),
    },
    "modern": {
        "bg": (20, 20, 20),
        "accent": (60, 180, 220),
        "text": (255, 255, 255),
        "highlight_bg": (60, 180, 220, 220),
        "card_bg": (35, 35, 35, 220),
    },
    "bold": {
        "bg": (0, 0, 0),
        "accent": (255, 80, 80),
        "text": (255, 255, 255),
        "highlight_bg": (255, 80, 80, 220),
        "card_bg": (20, 20, 20, 220),
    },
    "clean": {
        "bg": (250, 250, 250),
        "accent": (40, 40, 40),
        "text": (30, 30, 30),
        "highlight_bg": (40, 40, 40, 220),
        "card_bg": (255, 255, 255, 220),
    },
}


def create_social_video(config: Dict, output_path: str) -> str:
    """Create a social media video from config."""
    video_type = config.get("type", "tips")
    theme_name = config.get("theme", "luxury")
    theme = THEMES.get(theme_name, THEMES["luxury"])

    ar = config.get("aspect_ratio", "portrait")
    if ar == "portrait":
        width, height = 1080, 1920
    elif ar == "square":
        width, height = 1080, 1080
    else:
        width, height = 1920, 1080

    if video_type == "tips":
        slides = _build_tips_video(config, theme, width, height)
    elif video_type == "stats":
        slides = _build_stats_video(config, theme, width, height)
    elif video_type == "teaser":
        slides = _build_teaser_video(config, theme, width, height)
    elif video_type == "quote":
        slides = _build_quote_video(config, theme, width, height)
    else:
        slides = _build_tips_video(config, theme, width, height)

    project = VideoProject(
        slides=slides,
        width=width,
        height=height,
        fps=30,
        output_path=output_path,
        background_music=config.get("background_music"),
        music_volume=config.get("music_volume", 0.3),
    )

    def progress(current, total):
        pct = int(current / total * 100)
        if pct % 20 == 0:
            print(f"  Rendering: {pct}%", flush=True)

    return render_video(project, progress_callback=progress)


def _build_tips_video(config, theme, w, h):
    """Build a tips-style video: hook → numbered items → CTA."""
    headline = config.get("headline", "Tips You Need to Know")
    items = config.get("items", ["Tip 1", "Tip 2", "Tip 3"])
    bg_image = config.get("background_image")

    slides = []

    # Hook slide
    slides.append(Slide(
        duration=3.0,
        background_color=theme["bg"],
        image_path=bg_image,
        overlay_color=(0, 0, 0, 170) if bg_image else None,
        transition_in=Transition.FADE,
        transition_duration=0.5,
        texts=[
            TextOverlay(
                text=headline.upper(),
                position=(_cx(w, w - 160), h // 2 - 80),
                font_path=FONT_SANS_BOLD,
                font_size=64 if len(headline) < 30 else 48,
                color=theme["text"],
                max_width=w - 160,
                align="center",
                animation=TextAnimation.SCALE_IN,
                shadow=True,
            ),
            # Accent underline via text
            TextOverlay(
                text="▬" * 8,
                position=(_cx(w, w - 160), h // 2 + 20),
                font_path=FONT_SANS_BOLD,
                font_size=24,
                color=theme["accent"],
                max_width=w - 160,
                align="center",
                animation=TextAnimation.FADE_IN,
            ),
        ],
    ))

    # Individual tip slides
    for i, item in enumerate(items):
        number_text = f"{i + 1:02d}"
        slides.append(Slide(
            duration=3.5,
            background_color=theme["bg"],
            image_path=bg_image,
            overlay_color=(0, 0, 0, 180) if bg_image else None,
            transition_in=Transition.SLIDE_LEFT,
            transition_duration=0.4,
            texts=[
                # Big number
                TextOverlay(
                    text=number_text,
                    position=(_cx(w, w - 160), h // 2 - 160),
                    font_path=FONT_SANS_BOLD,
                    font_size=120,
                    color=theme["accent"],
                    max_width=w - 160,
                    align="center",
                    animation=TextAnimation.SCALE_IN,
                    shadow=False,
                ),
                # Tip text
                TextOverlay(
                    text=item,
                    position=(_cx(w, w - 160), h // 2 + 0),
                    font_path=FONT_SANS_BOLD,
                    font_size=40,
                    color=theme["text"],
                    max_width=w - 160,
                    align="center",
                    animation=TextAnimation.SLIDE_UP,
                    shadow=True,
                    line_spacing=12,
                ),
            ],
        ))

    # CTA slide
    agent_name = config.get("agent_name", "")
    handle = config.get("agent_handle", "")
    slides.append(_make_cta_slide(agent_name, handle, theme, w, h))

    return slides


def _build_stats_video(config, theme, w, h):
    """Build a market stats video: headline → stat cards → CTA."""
    headline = config.get("headline", "Market Update")
    stats = config.get("stats", [])
    bg_image = config.get("background_image")

    slides = []

    # Headline
    slides.append(Slide(
        duration=2.5,
        background_color=theme["bg"],
        transition_in=Transition.FADE,
        transition_duration=0.5,
        texts=[
            TextOverlay(
                text=headline.upper(),
                position=(_cx(w, w - 160), h // 2 - 60),
                font_path=FONT_SANS_BOLD,
                font_size=56,
                color=theme["text"],
                max_width=w - 160,
                align="center",
                animation=TextAnimation.FADE_IN,
                shadow=True,
            ),
        ],
    ))

    # Each stat gets its own slide
    for stat in stats:
        label = stat.get("label", "")
        value = stat.get("value", "")
        change = stat.get("change", "")

        texts = [
            TextOverlay(
                text=label.upper(),
                position=(_cx(w, w - 160), h // 2 - 140),
                font_path=FONT_SANS,
                font_size=32,
                color=theme["accent"],
                max_width=w - 160,
                align="center",
                animation=TextAnimation.FADE_IN,
            ),
            TextOverlay(
                text=value,
                position=(_cx(w, w - 160), h // 2 - 80),
                font_path=FONT_SANS_BOLD,
                font_size=96,
                color=theme["text"],
                max_width=w - 160,
                align="center",
                animation=TextAnimation.SCALE_IN,
                shadow=True,
            ),
        ]
        if change:
            change_color = (80, 200, 120) if change.startswith("+") else (255, 100, 100)
            texts.append(TextOverlay(
                text=change,
                position=(_cx(w, w - 160), h // 2 + 40),
                font_path=FONT_SANS_BOLD,
                font_size=44,
                color=change_color,
                max_width=w - 160,
                align="center",
                animation=TextAnimation.SLIDE_UP,
            ))

        slides.append(Slide(
            duration=3.5,
            background_color=theme["bg"],
            transition_in=Transition.FADE,
            transition_duration=0.4,
            texts=texts,
        ))

    # CTA
    slides.append(_make_cta_slide(
        config.get("agent_name", ""),
        config.get("agent_handle", ""),
        theme, w, h,
    ))

    return slides


def _build_teaser_video(config, theme, w, h):
    """Build a property teaser — quick photos with stats overlay."""
    photos = config.get("photos", [])
    address = config.get("address", "")
    price = config.get("price", "")

    slides = []

    # Quick flash through photos
    for i, photo in enumerate(photos[:6]):
        slide = Slide(
            duration=2.0,
            image_path=photo,
            transition_in=Transition.KENBURNS if i % 2 == 0 else Transition.SLIDE_LEFT,
            transition_duration=0.3,
            kenburns_direction=["zoom_in", "pan_left", "zoom_out", "pan_right"][i % 4],
            overlay_color=(0, 0, 0, 60),
        )

        # Address + price on first slide
        if i == 0 and (address or price):
            slide.overlay_color = (0, 0, 0, 140)
            if address:
                slide.texts.append(TextOverlay(
                    text=address.upper(),
                    position=(_cx(w, w - 120), h // 2 - 50),
                    font_path=FONT_SANS_BOLD,
                    font_size=52,
                    color=theme["text"],
                    max_width=w - 120,
                    align="center",
                    animation=TextAnimation.SCALE_IN,
                    shadow=True,
                ))
            if price:
                slide.texts.append(TextOverlay(
                    text=price,
                    position=(_cx(w, w - 120), h // 2 + 30),
                    font_path=FONT_SANS_BOLD,
                    font_size=44,
                    color=theme["accent"],
                    max_width=w - 120,
                    align="center",
                    animation=TextAnimation.FADE_IN,
                    shadow=True,
                ))

        slides.append(slide)

    # CTA
    slides.append(_make_cta_slide(
        config.get("agent_name", ""),
        config.get("agent_handle", ""),
        theme, w, h,
    ))

    return slides


def _build_quote_video(config, theme, w, h):
    """Build a quote/testimonial video."""
    quote = config.get("quote", config.get("headline", ""))
    attribution = config.get("attribution", "")
    bg_image = config.get("background_image")

    slides = [
        Slide(
            duration=6.0,
            background_color=theme["bg"],
            image_path=bg_image,
            overlay_color=(0, 0, 0, 170) if bg_image else None,
            blur_background=True if bg_image else False,
            transition_in=Transition.FADE,
            transition_duration=0.8,
            texts=[
                TextOverlay(
                    text=f'"{quote}"',
                    position=(_cx(w, w - 200), h // 2 - 100),
                    font_path=FONT_SERIF,
                    font_size=38,
                    color=theme["text"],
                    max_width=w - 200,
                    align="center",
                    animation=TextAnimation.FADE_IN,
                    shadow=True,
                    line_spacing=16,
                ),
                TextOverlay(
                    text=f"— {attribution}" if attribution else "",
                    position=(_cx(w, w - 200), h // 2 + 60),
                    font_path=FONT_SANS,
                    font_size=28,
                    color=theme["accent"],
                    max_width=w - 200,
                    align="center",
                    animation=TextAnimation.SLIDE_UP,
                ),
            ],
        ),
        _make_cta_slide(
            config.get("agent_name", ""),
            config.get("agent_handle", ""),
            theme, w, h,
        ),
    ]

    return slides


def _make_cta_slide(agent_name, handle, theme, w, h):
    """Reusable CTA slide."""
    texts = []
    if agent_name:
        texts.append(TextOverlay(
            text=agent_name,
            position=(_cx(w, w - 160), h // 2 - 40),
            font_path=FONT_SANS_BOLD,
            font_size=44,
            color=theme["text"],
            max_width=w - 160,
            align="center",
            animation=TextAnimation.FADE_IN,
            shadow=True,
        ))
    if handle:
        texts.append(TextOverlay(
            text=handle,
            position=(_cx(w, w - 160), h // 2 + 30),
            font_path=FONT_SANS,
            font_size=30,
            color=theme["accent"],
            max_width=w - 160,
            align="center",
            animation=TextAnimation.SLIDE_UP,
        ))
    texts.append(TextOverlay(
        text="FOLLOW FOR MORE",
        position=(_cx(w, w - 160), h // 2 + 80),
        font_path=FONT_SANS_BOLD,
        font_size=24,
        color=(160, 160, 160),
        max_width=w - 160,
        align="center",
        animation=TextAnimation.FADE_IN,
    ))

    return Slide(
        duration=3.0,
        background_color=theme["bg"],
        transition_in=Transition.FADE,
        transition_duration=0.6,
        texts=texts,
    )


def _cx(width, content_width):
    return (width - content_width) // 2


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default="social_video.mp4")
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)
    create_social_video(config, args.output)
