#!/usr/bin/env python3
"""
Video Creator Engine — Core rendering pipeline.
Uses Pillow for frame generation and ffmpeg for encoding.
Designed for real estate content: listing videos, social clips, market updates.
"""

import json
import math
import os
import subprocess
import tempfile
import textwrap
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

# ─── Constants ────────────────────────────────────────────────────────────────

FPS = 30
FONT_DIR = "/usr/share/fonts/opentype/urw-base35"

# Aspect ratios
LANDSCAPE = (1920, 1080)   # 16:9 YouTube / standard
PORTRAIT = (1080, 1920)    # 9:16 Reels / Shorts / TikTok
SQUARE = (1080, 1080)      # 1:1 Instagram feed

# Font paths (clean, professional sans-serif)
FONT_SANS = os.path.join(FONT_DIR, "NimbusSans-Regular.otf")
FONT_SANS_BOLD = os.path.join(FONT_DIR, "NimbusSans-Bold.otf")
FONT_SERIF = os.path.join(FONT_DIR, "NimbusRoman-Regular.otf")
FONT_SERIF_BOLD = os.path.join(FONT_DIR, "NimbusRoman-Bold.otf")

# Color palette — real estate professional
COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "dark_gray": (30, 30, 30),
    "charcoal": (45, 45, 45),
    "medium_gray": (120, 120, 120),
    "light_gray": (200, 200, 200),
    "off_white": (245, 245, 245),
    "gold": (198, 168, 124),
    "navy": (20, 40, 80),
    "deep_blue": (15, 25, 60),
    "teal": (0, 128, 128),
    "forest": (34, 85, 51),
    "warm_white": (255, 250, 240),
    "accent_blue": (60, 100, 170),
}


class Transition(Enum):
    CUT = "cut"
    FADE = "fade"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    DISSOLVE = "dissolve"
    WIPE_LEFT = "wipe_left"
    KENBURNS = "kenburns"


class TextAnimation(Enum):
    NONE = "none"
    FADE_IN = "fade_in"
    SLIDE_UP = "slide_up"
    TYPEWRITER = "typewriter"
    SCALE_IN = "scale_in"


@dataclass
class TextOverlay:
    """A text element to render on a frame."""
    text: str
    position: Tuple[int, int]  # (x, y) — top-left of text block
    font_path: str = FONT_SANS_BOLD
    font_size: int = 48
    color: Tuple[int, int, int] = (255, 255, 255)
    shadow: bool = True
    shadow_color: Tuple[int, int, int] = (0, 0, 0)
    shadow_offset: int = 3
    max_width: Optional[int] = None  # wrap text if set
    align: str = "left"  # left, center, right
    animation: TextAnimation = TextAnimation.FADE_IN
    bg_color: Optional[Tuple[int, int, int, int]] = None  # RGBA background pill
    bg_padding: int = 20
    line_spacing: int = 8


@dataclass
class LowerThird:
    """Professional lower-third bar with headline + subtitle."""
    headline: str
    subtitle: str = ""
    bar_color: Tuple[int, int, int] = (20, 40, 80)
    accent_color: Tuple[int, int, int] = (198, 168, 124)
    text_color: Tuple[int, int, int] = (255, 255, 255)
    position: str = "bottom"  # bottom or top
    width_pct: float = 0.65
    animation: TextAnimation = TextAnimation.SLIDE_UP


@dataclass
class Slide:
    """One segment of the video."""
    duration: float  # seconds
    background_color: Tuple[int, int, int] = (0, 0, 0)
    image_path: Optional[str] = None
    image_fit: str = "cover"  # cover, contain, fill
    texts: List[TextOverlay] = field(default_factory=list)
    lower_third: Optional[LowerThird] = None
    transition_in: Transition = Transition.FADE
    transition_duration: float = 0.5  # seconds for transition
    kenburns_direction: str = "zoom_in"  # zoom_in, zoom_out, pan_left, pan_right
    overlay_color: Optional[Tuple[int, int, int, int]] = None  # RGBA dark overlay
    blur_background: bool = False


@dataclass
class VideoProject:
    """Full video project definition."""
    slides: List[Slide]
    width: int = 1920
    height: int = 1080
    fps: int = 30
    output_path: str = "output.mp4"
    background_music: Optional[str] = None
    music_volume: float = 0.3


# ─── Frame Rendering ─────────────────────────────────────────────────────────

def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    """Load a font, falling back to default if needed."""
    try:
        return ImageFont.truetype(path, size)
    except (IOError, OSError):
        try:
            return ImageFont.truetype(FONT_SANS, size)
        except:
            return ImageFont.load_default()


def fit_image(img: Image.Image, width: int, height: int, mode: str = "cover") -> Image.Image:
    """Resize and crop/pad image to fit target dimensions."""
    if mode == "cover":
        # Scale up to cover, then center-crop
        ratio_w = width / img.width
        ratio_h = height / img.height
        ratio = max(ratio_w, ratio_h)
        new_w = int(img.width * ratio)
        new_h = int(img.height * ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        left = (new_w - width) // 2
        top = (new_h - height) // 2
        img = img.crop((left, top, left + width, top + height))
    elif mode == "contain":
        img.thumbnail((width, height), Image.LANCZOS)
        bg = Image.new("RGB", (width, height), (0, 0, 0))
        offset_x = (width - img.width) // 2
        offset_y = (height - img.height) // 2
        bg.paste(img, (offset_x, offset_y))
        img = bg
    elif mode == "fill":
        img = img.resize((width, height), Image.LANCZOS)
    return img


def apply_kenburns(img: Image.Image, width: int, height: int,
                   progress: float, direction: str = "zoom_in") -> Image.Image:
    """Apply Ken Burns (slow zoom/pan) effect to an image."""
    # Start with image slightly larger than frame
    scale_start = 1.15
    scale_end = 1.0

    if direction == "zoom_in":
        scale_start, scale_end = 1.0, 1.15
    elif direction == "zoom_out":
        scale_start, scale_end = 1.15, 1.0
    elif direction == "pan_left":
        scale_start = scale_end = 1.15
    elif direction == "pan_right":
        scale_start = scale_end = 1.15

    # Smooth easing
    t = ease_in_out(progress)
    scale = scale_start + (scale_end - scale_start) * t

    scaled_w = int(width * scale)
    scaled_h = int(height * scale)
    img_scaled = img.resize((scaled_w, scaled_h), Image.LANCZOS)

    if direction == "pan_left":
        x_offset = int((scaled_w - width) * (1 - t))
        y_offset = (scaled_h - height) // 2
    elif direction == "pan_right":
        x_offset = int((scaled_w - width) * t)
        y_offset = (scaled_h - height) // 2
    else:
        x_offset = (scaled_w - width) // 2
        y_offset = (scaled_h - height) // 2

    return img_scaled.crop((x_offset, y_offset, x_offset + width, y_offset + height))


def ease_in_out(t: float) -> float:
    """Smooth easing function (cubic)."""
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - pow(-2 * t + 2, 3) / 2


def ease_out(t: float) -> float:
    """Ease-out (decelerate)."""
    return 1 - pow(1 - t, 3)


def render_text_on_frame(draw: ImageDraw.ImageDraw, frame: Image.Image,
                         text_overlay: TextOverlay, progress: float,
                         frame_width: int, frame_height: int):
    """Render a text overlay with optional animation."""
    font = load_font(text_overlay.font_path, text_overlay.font_size)

    # Word wrap if max_width is set
    if text_overlay.max_width:
        lines = wrap_text(text_overlay.text, font, text_overlay.max_width)
    else:
        lines = text_overlay.text.split('\n')

    # Calculate animation state
    anim_progress = min(1.0, progress * 3)  # animate over first ~0.33s equivalent
    alpha = 1.0
    y_offset = 0
    scale_factor = 1.0

    if text_overlay.animation == TextAnimation.FADE_IN:
        alpha = ease_out(anim_progress)
    elif text_overlay.animation == TextAnimation.SLIDE_UP:
        alpha = ease_out(anim_progress)
        y_offset = int(50 * (1 - ease_out(anim_progress)))
    elif text_overlay.animation == TextAnimation.SCALE_IN:
        scale_factor = 0.5 + 0.5 * ease_out(anim_progress)
        alpha = ease_out(anim_progress)
    elif text_overlay.animation == TextAnimation.TYPEWRITER:
        total_chars = sum(len(l) for l in lines)
        visible_chars = int(total_chars * min(1.0, progress * 2))
        lines = _typewriter_lines(lines, visible_chars)

    if alpha < 0.01:
        return

    # Calculate total text block size
    line_heights = []
    line_widths = []
    for line in lines:
        bbox = font.getbbox(line) if line else font.getbbox(" ")
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        line_widths.append(w)
        line_heights.append(h)

    total_height = sum(line_heights) + text_overlay.line_spacing * (len(lines) - 1)
    max_line_width = max(line_widths) if line_widths else 0

    x, y = text_overlay.position
    y += y_offset

    # Draw background pill if specified
    if text_overlay.bg_color and alpha > 0.5:
        pad = text_overlay.bg_padding
        pill_width = text_overlay.max_width if text_overlay.max_width else max_line_width
        bg_rect = [x - pad, y - pad,
                   x + pill_width + pad, y + total_height + pad]
        bg_overlay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        bg_draw = ImageDraw.Draw(bg_overlay)
        bg_color_with_alpha = (*text_overlay.bg_color[:3],
                               int(text_overlay.bg_color[3] * alpha))
        bg_draw.rounded_rectangle(bg_rect, radius=12, fill=bg_color_with_alpha)
        frame.paste(Image.alpha_composite(
            frame.convert("RGBA"), bg_overlay).convert("RGB"), (0, 0))
        # Need new draw object after paste
        draw = ImageDraw.Draw(frame)

    # Draw each line
    current_y = y
    for i, line in enumerate(lines):
        if not line.strip():
            current_y += line_heights[i] + text_overlay.line_spacing
            continue

        # Use max_width as the alignment container if set, otherwise use actual widest line
        align_width = text_overlay.max_width if text_overlay.max_width else max_line_width
        lx = x
        if text_overlay.align == "center":
            lx = x + (align_width - line_widths[i]) // 2
        elif text_overlay.align == "right":
            lx = x + (align_width - line_widths[i])

        # Shadow
        if text_overlay.shadow and alpha > 0.3:
            so = text_overlay.shadow_offset
            shadow_color = (*text_overlay.shadow_color, int(180 * alpha))
            # Use a temporary RGBA layer for shadow
            shadow_layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow_layer)
            shadow_draw.text((lx + so, current_y + so), line, font=font,
                           fill=shadow_color)
            frame.paste(Image.alpha_composite(
                frame.convert("RGBA"), shadow_layer).convert("RGB"), (0, 0))
            draw = ImageDraw.Draw(frame)

        # Main text
        if alpha >= 1.0:
            draw.text((lx, current_y), line, font=font, fill=text_overlay.color)
        else:
            txt_layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
            txt_draw = ImageDraw.Draw(txt_layer)
            color_with_alpha = (*text_overlay.color, int(255 * alpha))
            txt_draw.text((lx, current_y), line, font=font, fill=color_with_alpha)
            frame.paste(Image.alpha_composite(
                frame.convert("RGBA"), txt_layer).convert("RGB"), (0, 0))
            draw = ImageDraw.Draw(frame)

        current_y += line_heights[i] + text_overlay.line_spacing

    return draw


def render_lower_third(frame: Image.Image, lt: LowerThird,
                       progress: float, width: int, height: int) -> Image.Image:
    """Render a professional lower-third bar."""
    anim_progress = ease_out(min(1.0, progress * 3))

    bar_width = int(width * lt.width_pct)
    bar_height = 90 if lt.subtitle else 60
    accent_height = 4

    # Slide in from left
    x_offset = int(bar_width * (1 - anim_progress)) * -1
    y_pos = height - bar_height - 80 if lt.position == "bottom" else 80

    overlay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    alpha = int(230 * anim_progress)

    # Main bar
    bar_color_alpha = (*lt.bar_color, alpha)
    draw.rectangle([x_offset, y_pos, x_offset + bar_width, y_pos + bar_height],
                   fill=bar_color_alpha)

    # Accent stripe on top
    accent_color_alpha = (*lt.accent_color, alpha)
    draw.rectangle([x_offset, y_pos, x_offset + bar_width, y_pos + accent_height],
                   fill=accent_color_alpha)

    # Headline
    headline_font = load_font(FONT_SANS_BOLD, 32)
    text_alpha = int(255 * anim_progress)
    draw.text((x_offset + 30, y_pos + accent_height + 8), lt.headline,
              font=headline_font, fill=(*lt.text_color, text_alpha))

    # Subtitle
    if lt.subtitle:
        sub_font = load_font(FONT_SANS, 22)
        draw.text((x_offset + 30, y_pos + accent_height + 46), lt.subtitle,
                  font=sub_font, fill=(*lt.accent_color, text_alpha))

    return Image.alpha_composite(frame.convert("RGBA"), overlay).convert("RGB")


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
    """Word-wrap text to fit within max_width pixels."""
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = font.getbbox(test_line)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]

    if current_line:
        lines.append(" ".join(current_line))

    return lines if lines else [text]


def _typewriter_lines(lines: List[str], visible_chars: int) -> List[str]:
    """Return lines with only the first N characters visible."""
    result = []
    remaining = visible_chars
    for line in lines:
        if remaining <= 0:
            break
        if remaining >= len(line):
            result.append(line)
            remaining -= len(line)
        else:
            result.append(line[:remaining])
            remaining = 0
    return result


# ─── Transition Rendering ────────────────────────────────────────────────────

def render_transition(frame_a: Image.Image, frame_b: Image.Image,
                      progress: float, transition: Transition) -> Image.Image:
    """Blend two frames according to the transition type."""
    t = ease_in_out(progress)
    w, h = frame_a.size

    if transition == Transition.CUT:
        return frame_b if progress > 0.5 else frame_a

    elif transition == Transition.FADE or transition == Transition.DISSOLVE:
        return Image.blend(frame_a, frame_b, t)

    elif transition == Transition.SLIDE_LEFT:
        offset = int(w * t)
        result = Image.new("RGB", (w, h))
        result.paste(frame_a, (-offset, 0))
        result.paste(frame_b, (w - offset, 0))
        return result

    elif transition == Transition.SLIDE_RIGHT:
        offset = int(w * t)
        result = Image.new("RGB", (w, h))
        result.paste(frame_a, (offset, 0))
        result.paste(frame_b, (-(w - offset), 0))
        return result

    elif transition == Transition.ZOOM_IN:
        scale = 1.0 + 0.3 * t
        scaled = frame_a.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        cx = (scaled.width - w) // 2
        cy = (scaled.height - h) // 2
        cropped = scaled.crop((cx, cy, cx + w, cy + h))
        return Image.blend(cropped, frame_b, t)

    elif transition == Transition.WIPE_LEFT:
        result = frame_a.copy()
        wipe_pos = int(w * t)
        result.paste(frame_b.crop((0, 0, wipe_pos, h)), (0, 0))
        return result

    else:
        return Image.blend(frame_a, frame_b, t)


# ─── Slide Frame Generation ──────────────────────────────────────────────────

def render_slide_frame(slide: Slide, frame_num: int, total_frames: int,
                       width: int, height: int) -> Image.Image:
    """Render a single frame of a slide (no transitions — just the slide content)."""
    progress = frame_num / max(total_frames - 1, 1)

    # Base frame
    frame = Image.new("RGB", (width, height), slide.background_color)

    # Background image
    if slide.image_path and os.path.exists(slide.image_path):
        try:
            img = Image.open(slide.image_path).convert("RGB")
            if slide.transition_in == Transition.KENBURNS:
                img = fit_image(img, int(width * 1.2), int(height * 1.2), "cover")
                frame = apply_kenburns(img, width, height, progress,
                                       slide.kenburns_direction)
            else:
                frame = fit_image(img, width, height, slide.image_fit)
        except Exception as e:
            print(f"Warning: Could not load image {slide.image_path}: {e}")

    # Blur background
    if slide.blur_background:
        frame = frame.filter(ImageFilter.GaussianBlur(radius=15))

    # Dark overlay
    if slide.overlay_color:
        overlay = Image.new("RGBA", (width, height), slide.overlay_color)
        frame = Image.alpha_composite(frame.convert("RGBA"), overlay).convert("RGB")

    # Text overlays
    draw = ImageDraw.Draw(frame)
    for text_overlay in slide.texts:
        draw = render_text_on_frame(draw, frame, text_overlay, progress, width, height)

    # Lower third
    if slide.lower_third:
        frame = render_lower_third(frame, slide.lower_third, progress, width, height)

    return frame


# ─── Video Assembly ──────────────────────────────────────────────────────────

def render_video(project: VideoProject, progress_callback=None) -> str:
    """
    Render a complete video project to MP4.
    Returns the output file path.
    """
    width, height, fps = project.width, project.height, project.fps

    with tempfile.TemporaryDirectory() as tmpdir:
        frame_dir = os.path.join(tmpdir, "frames")
        os.makedirs(frame_dir)

        global_frame = 0
        total_frames_est = sum(int(s.duration * fps) for s in project.slides)

        # Pre-render all slide frames
        slide_frames_cache = {}  # slide_index -> {frame_num: Image}

        for slide_idx, slide in enumerate(project.slides):
            slide_total_frames = int(slide.duration * fps)

            for f in range(slide_total_frames):
                frame = render_slide_frame(slide, f, slide_total_frames, width, height)

                # Handle transitions between slides
                if slide_idx > 0 and f < int(slide.transition_duration * fps):
                    prev_slide = project.slides[slide_idx - 1]
                    prev_total = int(prev_slide.duration * fps)
                    prev_frame = render_slide_frame(prev_slide, prev_total - 1,
                                                     prev_total, width, height)
                    t_progress = f / max(int(slide.transition_duration * fps) - 1, 1)
                    frame = render_transition(prev_frame, frame, t_progress,
                                            slide.transition_in)

                # Save frame
                frame_path = os.path.join(frame_dir, f"frame_{global_frame:06d}.png")
                frame.save(frame_path, "PNG")
                global_frame += 1

                if progress_callback and global_frame % 10 == 0:
                    progress_callback(global_frame, total_frames_est)

        print(f"Rendered {global_frame} frames. Encoding video...")

        # Encode with ffmpeg
        output_path = project.output_path
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-framerate", str(fps),
            "-i", os.path.join(frame_dir, "frame_%06d.png"),
        ]

        # Add background music if provided
        if project.background_music and os.path.exists(project.background_music):
            ffmpeg_cmd.extend([
                "-i", project.background_music,
                "-filter_complex",
                f"[1:a]volume={project.music_volume}[a]",
                "-map", "0:v", "-map", "[a]",
                "-shortest",
            ])

        ffmpeg_cmd.extend([
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "medium",
            "-crf", "23",
            "-movflags", "+faststart",
            output_path
        ])

        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"ffmpeg error: {result.stderr}")
            raise RuntimeError(f"ffmpeg encoding failed: {result.stderr[-500:]}")

        print(f"Video saved to {output_path}")
        return output_path


# ─── Convenience Builders ────────────────────────────────────────────────────

def create_title_slide(headline: str, subtitle: str = "",
                       bg_color=(20, 40, 80), accent_color=(198, 168, 124),
                       duration: float = 4.0, width: int = 1920,
                       height: int = 1080, image_path: str = None) -> Slide:
    """Create a professional title slide."""
    texts = []

    # Headline — centered
    headline_font_size = 72 if len(headline) < 30 else 56
    headline_y = height // 2 - 80
    texts.append(TextOverlay(
        text=headline,
        position=(width // 2 - 400, headline_y),
        font_path=FONT_SANS_BOLD,
        font_size=headline_font_size,
        color=(255, 255, 255),
        max_width=800,
        align="center",
        animation=TextAnimation.FADE_IN,
        shadow=True,
    ))

    # Accent line
    if subtitle:
        texts.append(TextOverlay(
            text=subtitle,
            position=(width // 2 - 400, headline_y + 100),
            font_path=FONT_SANS,
            font_size=32,
            color=accent_color,
            max_width=800,
            align="center",
            animation=TextAnimation.SLIDE_UP,
            shadow=True,
        ))

    return Slide(
        duration=duration,
        background_color=bg_color,
        image_path=image_path,
        overlay_color=(0, 0, 0, 140) if image_path else None,
        texts=texts,
        transition_in=Transition.FADE,
        transition_duration=0.8,
    )


def create_photo_slide(image_path: str, caption: str = "",
                       duration: float = 4.0, width: int = 1920,
                       height: int = 1080,
                       kenburns: bool = True) -> Slide:
    """Create a photo slide with optional caption and Ken Burns effect."""
    texts = []
    if caption:
        texts.append(TextOverlay(
            text=caption,
            position=(60, height - 140),
            font_path=FONT_SANS_BOLD,
            font_size=36,
            color=(255, 255, 255),
            max_width=width - 120,
            animation=TextAnimation.SLIDE_UP,
            shadow=True,
            bg_color=(0, 0, 0, 160),
            bg_padding=16,
        ))

    return Slide(
        duration=duration,
        image_path=image_path,
        texts=texts,
        transition_in=Transition.KENBURNS if kenburns else Transition.FADE,
        transition_duration=0.6,
        kenburns_direction="zoom_in",
    )


def create_text_slide(headline: str, bullets: List[str] = None,
                      bg_color=(245, 245, 245), text_color=(30, 30, 30),
                      duration: float = 5.0, width: int = 1920,
                      height: int = 1080) -> Slide:
    """Create a text/content slide with headline and optional bullets."""
    texts = [
        TextOverlay(
            text=headline,
            position=(120, 120),
            font_path=FONT_SANS_BOLD,
            font_size=52,
            color=text_color,
            max_width=width - 240,
            animation=TextAnimation.FADE_IN,
            shadow=False,
        )
    ]

    if bullets:
        bullet_text = "\n".join(f"• {b}" for b in bullets)
        texts.append(TextOverlay(
            text=bullet_text,
            position=(140, 220),
            font_path=FONT_SANS,
            font_size=36,
            color=(80, 80, 80),
            max_width=width - 280,
            animation=TextAnimation.SLIDE_UP,
            shadow=False,
            line_spacing=20,
        ))

    return Slide(
        duration=duration,
        background_color=bg_color,
        texts=texts,
        transition_in=Transition.FADE,
        transition_duration=0.5,
    )


def create_cta_slide(headline: str, subtitle: str = "",
                     contact_info: str = "",
                     bg_color=(20, 40, 80),
                     accent_color=(198, 168, 124),
                     duration: float = 5.0, width: int = 1920,
                     height: int = 1080) -> Slide:
    """Create a call-to-action / closing slide."""
    texts = [
        TextOverlay(
            text=headline,
            position=(width // 2 - 400, height // 2 - 100),
            font_path=FONT_SANS_BOLD,
            font_size=64,
            color=(255, 255, 255),
            max_width=800,
            align="center",
            animation=TextAnimation.SCALE_IN,
            shadow=True,
        )
    ]

    if subtitle:
        texts.append(TextOverlay(
            text=subtitle,
            position=(width // 2 - 400, height // 2 + 20),
            font_path=FONT_SANS,
            font_size=32,
            color=accent_color,
            max_width=800,
            align="center",
            animation=TextAnimation.FADE_IN,
        ))

    if contact_info:
        texts.append(TextOverlay(
            text=contact_info,
            position=(width // 2 - 400, height // 2 + 80),
            font_path=FONT_SANS,
            font_size=28,
            color=(200, 200, 200),
            max_width=800,
            align="center",
            animation=TextAnimation.FADE_IN,
        ))

    return Slide(
        duration=duration,
        background_color=bg_color,
        texts=texts,
        transition_in=Transition.FADE,
        transition_duration=1.0,
    )


# ─── Entry Point for Testing ────────────────────────────────────────────────

if __name__ == "__main__":
    print("Video Creator Engine loaded successfully.")
    print(f"Available fonts: {FONT_SANS}, {FONT_SANS_BOLD}")
    print(f"Pillow version: {Image.__version__}")

    # Quick smoke test — render one frame
    test_slide = create_title_slide("Test Video", "Engine Check")
    frame = render_slide_frame(test_slide, 15, 30, 1920, 1080)
    test_path = "/tmp/video_engine_test.png"
    frame.save(test_path)
    print(f"Test frame saved to {test_path}")
