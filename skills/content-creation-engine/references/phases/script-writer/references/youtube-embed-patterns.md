# YouTube Embed + Timestamp Link Patterns

> **Read by Phase 5 (script-writer) when generating blog post derivatives that include a YouTube source video.** Used in the YouTube-to-blog repurposing pipeline.

When Graeham repurposes a YouTube video into a blog post (own-channel content or competitor analysis with proper attribution), the blog should embed the source video and link to specific timestamps within the body. This:

1. Boosts watch time for the source video (own channel)
2. Lets readers verify claims in the blog by jumping to the moment in the video
3. Improves SEO (Google rewards blog posts that embed video content)
4. Pairs with the VideoObject schema for rich-result eligibility

---

## Standard Embed (Required for Every Video-Based Blog Post)

Place the embed near the top of the blog body, after the first 1-2 paragraphs of the introduction (after the AI summary block, before the first H2 section).

```html
<div class="video-embed" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%;">
  <iframe
    src="https://www.youtube.com/embed/[VIDEO_ID]?rel=0"
    title="[VIDEO_TITLE]"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    referrerpolicy="strict-origin-when-cross-origin"
    allowfullscreen
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
  </iframe>
</div>
```

**Notes:**
- `?rel=0` at the end of the embed URL prevents YouTube from showing OTHER channels' videos in the "related videos" overlay at the end. Keeps viewers on Graeham's content.
- The wrapping `<div>` with padding-bottom: 56.25% creates a 16:9 responsive container. Critical for mobile.
- `title="[VIDEO_TITLE]"` is required for accessibility.
- Replace `[VIDEO_ID]` with the actual YouTube video ID (the 11-char string after `v=` in the watch URL).

### Privacy-Enhanced Variant (Optional)

If Graeham wants to avoid YouTube setting cookies on his readers until they actually click play, use the privacy-enhanced domain:

```html
<iframe src="https://www.youtube-nocookie.com/embed/[VIDEO_ID]?rel=0" ...>
```

Same embed otherwise. Trade-off: slightly different analytics granularity for YouTube. For most use cases, standard `youtube.com/embed/` is fine.

---

## Timestamp Links (Inline in Body Text)

When the blog references a specific moment in the video — a quote, a stat, a key insight — link to that exact second so readers can jump there.

### Pattern

```html
<a href="https://www.youtube.com/watch?v=[VIDEO_ID]&t=[SECONDS]s">Watch Graeham break this down at [MM:SS]</a>
```

Or with the embed-friendly format:

```html
<a href="https://youtu.be/[VIDEO_ID]?t=[SECONDS]">Watch at [MM:SS]</a>
```

### Examples

> "I broke down the median price story for EPA in detail — [watch from 2:14 if you want the full data context](https://www.youtube.com/watch?v=abc123XYZ&t=134s)."

> "The sale-to-list ratio surprised me too — [Graeham reacts to the data at 5:42](https://youtu.be/abc123XYZ?t=342)."

### Anchor Text Guidance

- Reference the timestamp in the visible anchor text ("at 2:14")
- Make the surrounding sentence give the reader a reason to click ("the full data context," "Graeham reacts to the data," etc.)
- Don't use "click here" or "watch this"

### How to Get the Right Timestamp

If working from a transcript with timestamps (which `youtube_transcriber.py` produces):

1. Find the moment in the transcript where the relevant content starts
2. Convert the timestamp to seconds: `(minutes × 60) + seconds`
   - 0:30 → 30s
   - 2:14 → 134s
   - 12:05 → 725s
3. Insert into the URL as `&t=134s` or `?t=134`

For YouTube watch-page URLs, use `&t=134s`. For shortened `youtu.be/` URLs, use `?t=134` (no `s` suffix needed but accepted).

---

## How Many Timestamp Links Per Blog?

| Blog length | Timestamp links |
|---|---|
| Short (~600 words) | 1-2 |
| Medium (1,000-1,400 words) | 2-3 |
| Long (1,800+ words) | 3-5 |

Don't link every paragraph back to the video — readers tune out. Save timestamp links for genuinely high-value moments: surprising stats, direct quotes, the "aha" moment of the video, the CTA.

---

## When NOT To Embed

- **Source video is private / unlisted** — embed will show "Video unavailable." Skip.
- **Source video is age-restricted** — embed shows a sign-in wall. Skip.
- **Source video is from someone else's channel and Graeham hasn't gotten permission to embed for repurposed content** — fair use covers brief commentary, but full embeds of someone else's video as the centerpiece of Graeham's blog is gray-area. Default to: own-channel videos only for embeds. Competitor videos can be linked with attribution but not embedded.
- **Video has been deleted / channel removed** — confirm video is still live before publishing the blog.

---

## Pairing With VideoObject Schema

When this module fires, also fire `schema-markup-templates.md` to inject VideoObject schema. Both work together — embed for human readers, schema for AI search and Google rich results.

---

## Used By

- Phase 5 (script-writer) — when format = blog-post-draft AND source = YouTube video
- `content-creation-engine` channel-monitor flow — when the YouTube scraper feeds new own-channel videos into Phase 5 for blog repurposing
