#!/usr/bin/env python3
"""
Listing Video Template — Property showcase with photos, text overlays, transitions.
Designed for real estate agents to create professional listing videos.

Usage:
    python3 listing_video.py --config listing_config.json --output listing.mp4

Or import and use programmatically:
    from listing_video import create_listing_video
    create_listing_video(config, output_path)
"""

import argparse
import json
import os
import random
import sys
from typing import Dict, List, Optional

# Add parent dir to path
sys.path.insert(0, os.path.dirname(__file__))
from video_engine import (
    COLORS, FONT_SANS, FONT_SANS_BOLD, FONT_SERIF, FONT_SERIF_BOLD,
    LowerThird, Slide, TextAnimation, TextOverlay,
    Transition, VideoProject, create_cta_slide, create_photo_slide,
    create_text_slide, create_title_slide, render_video,
)


# ─── Color Themes ────────────────────────────────────────────────────────────

THEMES = {
    "luxury": {
        "bg_primary": (15, 25, 50),
        "bg_secondary": (245, 240, 230),
        "accent": (198, 168, 124),
        "text_light": (255, 255, 255),
        "text_dark": (30, 30, 30),
        "overlay": (0, 0, 0, 150),
    },
    "modern": {
        "bg_primary": (25, 25, 25),
        "bg_secondary": (250, 250, 250),
        "accent": (60, 140, 200),
        "text_light": (255, 255, 255),
        "text_dark": (30, 30, 30),
        "overlay": (0, 0, 0, 130),
    },
    "coastal": {
        "bg_primary": (20, 60, 90),
        "bg_secondary": (240, 248, 255),
        "accent": (100, 200, 200),
        "text_light": (255, 255, 255),
        "text_dark": (20, 40, 60),
        "overlay": (10, 30, 50, 140),
    },
    "warm": {
        "bg_primary": (60, 30, 20),
        "bg_secondary": (255, 250, 240),
        "accent": (210, 160, 90),
        "text_light": (255, 255, 255),
        "text_dark": (40, 30, 20),
        "overlay": (30, 15, 10, 140),
    },
    "minimal": {
        "bg_primary": (255, 255, 255),
        "bg_secondary": (245, 245, 245),
        "accent": (40, 40, 40),
        "text_light": (255, 255, 255),
        "text_dark": (30, 30, 30),
        "overlay": (0, 0, 0, 120),
    },
}


# ─── Listing Video Builder ───────────────────────────────────────────────────

def create_listing_video(config: Dict, output_path: str,
                         width: int = 1920, height: int = 1080,
                         fps: int = 30) -> str:
    """
    Create a complete listing video from a config dict.

    Config shape:
    {
        "address": "123 Main Street",
        "city_state_zip": "San Jose, CA 95125",
        "price": "$1,850,000",
        "beds": 4,
        "baths": 3,
        "sqft": "2,450",
        "lot_size": "6,200 sqft",          # optional
        "year_built": 1965,                 # optional
        "description": "Stunning mid-century modern...",  # optional
        "highlights": ["Renovated Kitchen", "Pool & Spa", ...],
        "photos": ["/path/to/photo1.jpg", ...],
        "photo_captions": ["Living Room", "Kitchen", ...],  # optional
        "agent_name": "Graeham Watts",
        "agent_title": "REALTOR® | DRE# 01466876",
        "agent_contact": "graehamwatts@gmail.com",
        "agent_phone": "408-XXX-XXXX",     # optional
        "brokerage": "Compass",             # optional
        "theme": "luxury",                  # luxury, modern, coastal, warm, minimal
        "aspect_ratio": "landscape",        # landscape, portrait, square
        "duration_per_photo": 4.0,          # seconds per photo slide
        "include_highlights": true,
        "cta_text": "Schedule Your Private Tour",
    }
    """

    theme_name = config.get("theme", "luxury")
    theme = THEMES.get(theme_name, THEMES["luxury"])

    # Aspect ratio
    ar = config.get("aspect_ratio", "landscape")
    if ar == "portrait":
        width, height = 1080, 1920
    elif ar == "square":
        width, height = 1080, 1080

    photo_duration = config.get("duration_per_photo", 4.0)
    photos = config.get("photos", [])
    captions = config.get("photo_captions", [])
    highlights = config.get("highlights", [])

    slides = []

    # ── 1. Title Slide ────────────────────────────────────────────────────
    # Use first photo as background if available
    title_bg = photos[0] if photos else None
    price_line = config.get("price", "")
    address = config.get("address", "Beautiful Home")
    city = config.get("city_state_zip", "")

    subtitle_parts = []
    if price_line:
        subtitle_parts.append(price_line)
    if city:
        subtitle_parts.append(city)
    subtitle = " | ".join(subtitle_parts)

    title_slide = Slide(
        duration=4.5,
        background_color=theme["bg_primary"],
        image_path=title_bg,
        overlay_color=theme["overlay"],
        transition_in=Transition.FADE,
        transition_duration=1.0,
        texts=[
            TextOverlay(
                text=address.upper(),
                position=(_center_x(width, 700), height // 2 - 90),
                font_path=FONT_SANS_BOLD,
                font_size=68 if len(address) < 25 else 52,
                color=theme["text_light"],
                max_width=700 if ar == "landscape" else 500,
                align="center",
                animation=TextAnimation.FADE_IN,
                shadow=True,
            ),
            TextOverlay(
                text=subtitle,
                position=(_center_x(width, 700), height // 2 + 10),
                font_path=FONT_SANS,
                font_size=30,
                color=theme["accent"],
                max_width=700,
                align="center",
                animation=TextAnimation.SLIDE_UP,
                shadow=True,
            ),
        ],
    )

    # Add stats bar
    stats_parts = []
    if config.get("beds"):
        stats_parts.append(f"{config['beds']} Beds")
    if config.get("baths"):
        stats_parts.append(f"{config['baths']} Baths")
    if config.get("sqft"):
        stats_parts.append(f"{config['sqft']} Sqft")
    if stats_parts:
        title_slide.texts.append(TextOverlay(
            text="  •  ".join(stats_parts),
            position=(_center_x(width, 700), height // 2 + 60),
            font_path=FONT_SANS,
            font_size=28,
            color=theme["text_light"],
            max_width=700,
            align="center",
            animation=TextAnimation.SLIDE_UP,
            shadow=True,
        ))

    slides.append(title_slide)

    # ── 2. Property Stats Slide ──────────────────────────────────────────
    stat_items = []
    if config.get("beds"):
        stat_items.append(f"Bedrooms: {config['beds']}")
    if config.get("baths"):
        stat_items.append(f"Bathrooms: {config['baths']}")
    if config.get("sqft"):
        stat_items.append(f"Living Area: {config['sqft']} sqft")
    if config.get("lot_size"):
        stat_items.append(f"Lot Size: {config['lot_size']}")
    if config.get("year_built"):
        stat_items.append(f"Year Built: {config['year_built']}")

    if stat_items:
        # Use second photo as background if available
        stat_bg = photos[1] if len(photos) > 1 else None
        stat_slide = Slide(
            duration=4.0,
            background_color=theme["bg_primary"],
            image_path=stat_bg,
            overlay_color=(0, 0, 0, 180) if stat_bg else None,
            blur_background=True if stat_bg else False,
            transition_in=Transition.FADE,
            transition_duration=0.6,
            texts=[
                TextOverlay(
                    text="PROPERTY DETAILS",
                    position=(120, 100) if ar == "landscape" else (80, 200),
                    font_path=FONT_SANS_BOLD,
                    font_size=42,
                    color=theme["accent"],
                    animation=TextAnimation.FADE_IN,
                    shadow=True,
                ),
                TextOverlay(
                    text="\n".join(stat_items),
                    position=(120, 180) if ar == "landscape" else (80, 280),
                    font_path=FONT_SANS,
                    font_size=34,
                    color=theme["text_light"],
                    max_width=width - 240,
                    animation=TextAnimation.SLIDE_UP,
                    shadow=True,
                    line_spacing=18,
                ),
            ],
        )
        slides.append(stat_slide)

    # ── 3. Photo Slides ──────────────────────────────────────────────────
    # Alternate Ken Burns directions for visual interest
    kb_directions = ["zoom_in", "zoom_out", "pan_left", "pan_right"]
    transitions = [Transition.KENBURNS, Transition.FADE, Transition.DISSOLVE, Transition.SLIDE_LEFT]

    for i, photo in enumerate(photos):
        caption = captions[i] if i < len(captions) else ""
        kb_dir = kb_directions[i % len(kb_directions)]
        trans = transitions[i % len(transitions)]

        slide = Slide(
            duration=photo_duration,
            image_path=photo,
            transition_in=trans if trans != Transition.KENBURNS else Transition.KENBURNS,
            transition_duration=0.6,
            kenburns_direction=kb_dir,
        )

        # Add caption if provided
        if caption:
            slide.lower_third = LowerThird(
                headline=caption,
                bar_color=theme["bg_primary"],
                accent_color=theme["accent"],
                text_color=theme["text_light"],
            )

        slides.append(slide)

    # ── 4. Highlights Slide ──────────────────────────────────────────────
    if highlights and config.get("include_highlights", True):
        highlights_slide = Slide(
            duration=5.0,
            background_color=theme["bg_secondary"],
            transition_in=Transition.FADE,
            transition_duration=0.5,
            texts=[
                TextOverlay(
                    text="PROPERTY HIGHLIGHTS",
                    position=(120, 80) if ar == "landscape" else (80, 200),
                    font_path=FONT_SANS_BOLD,
                    font_size=44,
                    color=theme["text_dark"],
                    animation=TextAnimation.FADE_IN,
                    shadow=False,
                ),
                TextOverlay(
                    text="\n".join(f"✦  {h}" for h in highlights[:8]),
                    position=(140, 170) if ar == "landscape" else (80, 300),
                    font_path=FONT_SANS,
                    font_size=32,
                    color=theme["text_dark"],
                    max_width=width - 280,
                    animation=TextAnimation.SLIDE_UP,
                    shadow=False,
                    line_spacing=16,
                ),
            ],
        )
        slides.append(highlights_slide)

    # ── 5. Description Slide (optional) ──────────────────────────────────
    if config.get("description"):
        desc_bg = photos[-1] if photos else None
        desc_slide = Slide(
            duration=5.0,
            background_color=theme["bg_primary"],
            image_path=desc_bg,
            overlay_color=(0, 0, 0, 190) if desc_bg else None,
            blur_background=True,
            transition_in=Transition.FADE,
            transition_duration=0.6,
            texts=[
                TextOverlay(
                    text=config["description"][:300],
                    position=(120, height // 2 - 100) if ar == "landscape" else (80, height // 2 - 200),
                    font_path=FONT_SERIF,
                    font_size=30,
                    color=theme["text_light"],
                    max_width=width - 240,
                    align="center",
                    animation=TextAnimation.FADE_IN,
                    shadow=True,
                    line_spacing=14,
                ),
            ],
        )
        slides.append(desc_slide)

    # ── 6. CTA / Contact Slide ───────────────────────────────────────────
    cta_text = config.get("cta_text", "Schedule Your Private Tour")
    agent_name = config.get("agent_name", "")
    agent_title = config.get("agent_title", "")
    agent_contact = config.get("agent_contact", "")
    agent_phone = config.get("agent_phone", "")
    brokerage = config.get("brokerage", "")

    contact_parts = []
    if agent_phone:
        contact_parts.append(agent_phone)
    if agent_contact:
        contact_parts.append(agent_contact)
    contact_line = "  |  ".join(contact_parts)

    agent_line = agent_name
    if agent_title:
        agent_line += f"  •  {agent_title}"

    cta_slide = Slide(
        duration=5.0,
        background_color=theme["bg_primary"],
        transition_in=Transition.FADE,
        transition_duration=1.0,
        texts=[
            TextOverlay(
                text=cta_text,
                position=(_center_x(width, 800), height // 2 - 120),
                font_path=FONT_SANS_BOLD,
                font_size=56,
                color=theme["text_light"],
                max_width=800,
                align="center",
                animation=TextAnimation.SCALE_IN,
                shadow=True,
            ),
            TextOverlay(
                text=agent_line,
                position=(_center_x(width, 800), height // 2 + 0),
                font_path=FONT_SANS_BOLD,
                font_size=30,
                color=theme["accent"],
                max_width=800,
                align="center",
                animation=TextAnimation.FADE_IN,
                shadow=True,
            ),
            TextOverlay(
                text=contact_line,
                position=(_center_x(width, 800), height // 2 + 50),
                font_path=FONT_SANS,
                font_size=26,
                color=(200, 200, 200),
                max_width=800,
                align="center",
                animation=TextAnimation.FADE_IN,
            ),
        ],
    )

    if brokerage:
        cta_slide.texts.append(TextOverlay(
            text=brokerage,
            position=(_center_x(width, 800), height // 2 + 100),
            font_path=FONT_SANS,
            font_size=22,
            color=(160, 160, 160),
            max_width=800,
            align="center",
            animation=TextAnimation.FADE_IN,
        ))

    slides.append(cta_slide)

    # ── Build & Render ───────────────────────────────────────────────────
    project = VideoProject(
        slides=slides,
        width=width,
        height=height,
        fps=fps,
        output_path=output_path,
        background_music=config.get("background_music"),
        music_volume=config.get("music_volume", 0.3),
    )

    def progress(current, total):
        pct = int(current / total * 100)
        if pct % 10 == 0:
            print(f"  Rendering: {pct}%", flush=True)

    return render_video(project, progress_callback=progress)


def _center_x(width: int, content_width: int) -> int:
    """Calculate x position to center content."""
    return (width - content_width) // 2


# ─── CLI ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a listing video")
    parser.add_argument("--config", required=True, help="Path to JSON config file")
    parser.add_argument("--output", default="listing_video.mp4", help="Output path")
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--fps", type=int, default=30)
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

    create_listing_video(config, args.output, args.width, args.height, args.fps)
