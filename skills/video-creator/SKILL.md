---
name: video-creator
description: "AI Video Creator — generates professional MP4 videos using Python + ffmpeg. Use this skill ANY time the user mentions: video, reel, short, TikTok, YouTube Short, Instagram Reel, listing video, property video, market update video, social media video, video content, create a video, make a video, video for social, animated video, slideshow video, video from photos, promo video, teaser video, explainer video, video presentation, or anything related to creating, rendering, or producing video content. Also trigger when the user wants to turn photos into a video, create motion graphics, make an animated market report, or produce any kind of video content from text or images. This skill renders finished MP4 files directly — no external tools or local setup needed."
---

# Video Creator Skill

Create professional MP4 videos entirely within the Cowork environment. This skill uses Python (Pillow + OpenCV) for frame generation and ffmpeg for encoding. No browser, no Chromium, no local setup — just describe what you want and get a finished video.

## Architecture

```
video-creator/
├── SKILL.md                    ← You are here
└── scripts/
    ├── video_engine.py         ← Core rendering engine (frames + ffmpeg)
    ├── listing_video.py        ← Real estate listing video template
    ├── social_video.py         ← Social media short-form template
    └── market_video.py         ← Market update / educational template
```

## How It Works

1. **Understand the request** — what kind of video, what content, what format
2. **Build a config dict** — structured data describing every slide
3. **Call the appropriate template** — or build custom slides using the engine
4. **Render** — Python generates frames, ffmpeg encodes to H.264 MP4
5. **Deliver** — save to outputs folder and provide download link

## Quick Start

Read the appropriate template script before generating video code. Each template accepts a JSON config and an output path.

```python
import sys
sys.path.insert(0, '<skill-path>/scripts')

# For listing videos:
from listing_video import create_listing_video
create_listing_video(config, '/sessions/.../mnt/outputs/my_video.mp4')

# For social media:
from social_video import create_social_video
create_social_video(config, '/sessions/.../mnt/outputs/my_reel.mp4')

# For market updates:
from market_video import create_market_video
create_market_video(config, '/sessions/.../mnt/outputs/market_update.mp4')

# For fully custom videos:
from video_engine import *
project = VideoProject(slides=[...], output_path='...')
render_video(project)
```

## Video Types & When to Use Each

### 1. Listing Video (`listing_video.py`)
Best for: Property showcases, open house promos, just-listed/just-sold announcements.

**Config reference:**
```json
{
    "address": "123 Main Street",
    "city_state_zip": "San Jose, CA 95125",
    "price": "$1,850,000",
    "beds": 4,
    "baths": 3,
    "sqft": "2,450",
    "lot_size": "6,200 sqft",
    "year_built": 1965,
    "description": "Stunning mid-century modern home...",
    "highlights": ["Renovated Kitchen", "Pool & Spa", "Top Schools"],
    "photos": ["/path/to/photo1.jpg", "/path/to/photo2.jpg"],
    "photo_captions": ["Living Room", "Kitchen"],
    "agent_name": "Graeham Watts",
    "agent_title": "REALTOR® | DRE# 02015066",
    "agent_contact": "graehamwatts@gmail.com",
    "agent_phone": "408-XXX-XXXX",
    "brokerage": "Compass",
    "theme": "luxury",
    "aspect_ratio": "landscape",
    "duration_per_photo": 4.0,
    "include_highlights": true,
    "cta_text": "Schedule Your Private Tour"
}
```

**Slide flow:** Title → Property Stats → Photo slides (with Ken Burns) → Highlights → Description → CTA

### 2. Social Media Video (`social_video.py`)
Best for: Instagram Reels, YouTube Shorts, TikTok, quick tips, market stats.

**Types available:**
- `"tips"` — Hook headline → numbered tip slides → CTA
- `"stats"` — Headline → stat cards with big numbers → CTA
- `"teaser"` — Quick photo montage with address overlay → CTA
- `"quote"` — Client testimonial or inspirational quote → CTA

**Config reference:**
```json
{
    "type": "tips",
    "headline": "3 Mistakes First-Time Buyers Make",
    "items": ["Not getting pre-approved first", "Skipping the inspection", "Waiving contingencies"],
    "background_image": "/path/to/bg.jpg",
    "agent_name": "Graeham Watts",
    "agent_handle": "@graehamwatts",
    "theme": "luxury",
    "aspect_ratio": "portrait"
}
```

For stats type:
```json
{
    "type": "stats",
    "headline": "Bay Area Market Update",
    "stats": [
        {"label": "Median Price", "value": "$1.85M", "change": "+4.2%"},
        {"label": "Days on Market", "value": "12", "change": "-3 days"},
        {"label": "Inventory", "value": "1.8 months", "change": "-15%"}
    ],
    "agent_name": "Graeham Watts",
    "agent_handle": "@graehamwatts",
    "theme": "luxury",
    "aspect_ratio": "portrait"
}
```

### 3. Market Update Video (`market_video.py`)
Best for: Monthly market reports, educational content, data presentations.

**Config reference:**
```json
{
    "title": "Silicon Valley Market Update",
    "subtitle": "March 2026",
    "sections": [
        {
            "headline": "Median Home Price",
            "stat_value": "$1.85M",
            "stat_label": "Median Price",
            "stat_change": "+4.2%",
            "content": "Prices continue to climb as inventory remains tight."
        },
        {
            "headline": "Market Velocity",
            "stat_value": "12 Days",
            "stat_label": "Average Days on Market",
            "stat_change": "-3 days",
            "content": "Homes are selling faster than last quarter."
        }
    ],
    "takeaways": [
        "Sellers still have strong leverage in most price ranges",
        "Well-priced homes are getting multiple offers within a week",
        "Interest rates are stabilizing, bringing more buyers back"
    ],
    "agent_name": "Graeham Watts",
    "agent_title": "REALTOR® | DRE# 02015066",
    "agent_contact": "graehamwatts@gmail.com",
    "theme": "luxury",
    "aspect_ratio": "landscape"
}
```

### 4. Custom Video (use `video_engine.py` directly)
For anything that doesn't fit the templates — fully custom slide sequences.

**Available components:**
- `Slide` — base slide with background color/image, overlays, text, transitions
- `TextOverlay` — text with font, size, color, animation, background pill, shadow
- `LowerThird` — professional bar with headline + subtitle
- `VideoProject` — container for slides + encoding settings

**Transitions:** `FADE`, `DISSOLVE`, `SLIDE_LEFT`, `SLIDE_RIGHT`, `ZOOM_IN`, `WIPE_LEFT`, `KENBURNS`, `CUT`

**Text Animations:** `FADE_IN`, `SLIDE_UP`, `TYPEWRITER`, `SCALE_IN`, `NONE`

**Ken Burns directions:** `zoom_in`, `zoom_out`, `pan_left`, `pan_right`

## Themes

All templates support these color themes:

| Theme | Best For | Primary Color |
|-------|----------|---------------|
| `luxury` | High-end listings, premium branding | Navy + Gold |
| `modern` | Clean contemporary look | Dark + Blue accent |
| `coastal` | Beach/waterfront properties | Ocean blue + Teal |
| `warm` | Cozy homes, family neighborhoods | Warm brown + Gold |
| `minimal` | Ultra-clean, minimal design | White + Black |
| `bold` | Attention-grabbing social content | Black + Red |
| `clean` | Light professional look | Light gray + Dark |

Note: Not all themes are available in all templates. `luxury` and `modern` are universally supported.

## Aspect Ratios

| Setting | Resolution | Use Case |
|---------|-----------|----------|
| `landscape` | 1920×1080 | YouTube, website, presentations |
| `portrait` | 1080×1920 | Instagram Reels, TikTok, YouTube Shorts |
| `square` | 1080×1080 | Instagram feed, Facebook |

## Working with Photos

When the user provides photos (uploaded or from a folder):
1. Photos are at paths under `/sessions/.../mnt/uploads/` or the user's selected folder
2. Pass absolute paths in the config's `photos` array
3. The engine handles resizing, cropping (cover fit), and Ken Burns effects automatically
4. Supported formats: JPG, PNG, WebP, TIFF

If no photos are provided, the skill creates text-only slides with colored backgrounds — still professional and useful.

## Performance Notes

- A 30-second video at 30fps = ~900 frames. Expect 2-4 minutes render time.
- For faster test renders, use `fps=24` or even `fps=15`.
- Shorter videos (10-15 seconds) render in under a minute.
- Social media portrait videos are smaller (1080px wide) and render faster.

## Agent Info Defaults

When the user doesn't specify agent info, use these defaults for Graeham:
- Name: Graeham Watts
- Title: REALTOR® | DRE# 02015066
- Email: graehamwatts@gmail.com
- Brokerage: Compass

## Step-by-Step Workflow

1. **Ask what kind of video** if not clear from the request
2. **Read the relevant template script** to understand the config shape
3. **Build the config** from the user's input (fill in defaults for missing fields)
4. **Write a Python script** that imports the template and calls it with the config
5. **Run the script** via Bash with a timeout of 300000ms (5 min)
6. **Save output** to `/sessions/.../mnt/outputs/` and provide a computer:// link
7. **If the user wants changes**, modify the config and re-render

Always tell the user roughly how long rendering will take based on duration and fps.
