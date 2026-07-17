# Phase 9 — Delivery

Final phase. Takes the humanized content package from Phase 8 and splits it into separable artifact files plus a Property-OS-styled HTML preview. This is what Jason, Ellie, and Graeham actually consume.

## Why split files

A single monster markdown file works for archival but is terrible UX for editors. Jason wants to grab just the editing notes. Ellie wants just the captions. Graeham wants the HeyGen-ready script with no shot tags. Each artifact gets its own file so any team member can grab the one piece they need without scrolling through 200 lines of unrelated content.

## Output folder structure

For each repurpose job, the skill creates:

```
outputs/transcript-repurpose-{slug}-{YYYYMMDD-HHMM}/
├── index.html              ← Property-OS-styled preview, open in browser
├── transcript.txt          ← Raw source transcript
├── content-package.md      ← Canonical full markdown (everything)
├── hooks.md                ← 3 scored hook variants + recommendation
├── script-yt-long.md       ← Long-form YouTube script with shot tags
├── script-yt-short.md      ← YouTube Short script
├── script-ig-reel.md       ← Instagram Reel script
├── script-tiktok.md        ← TikTok script
├── script-blog.md          ← Blog version (SEO-tuned)
├── captions.md             ← All platform captions + hashtags
├── ssml.xml                ← ElevenLabs SSML voice markup
├── heygen-script.txt       ← HeyGen paste-ready (shot tags stripped)
├── broll-prompts.md        ← Higgsfield image + motion prompts
├── editing-notes.md        ← Jason's editor brief (shot list, timing, thumbnail)
└── manifest.json           ← Index of artifacts + metadata
```

Files only exist if their source section was produced. If the user only asked for a YouTube Short, the long-form and blog files are skipped.

## How to invoke

After Phase 8 (humanizer) produces the final content package markdown, run the delivery script:

```bash
python3 /sessions/*/mnt/Skills/skills/transcript-repurposer/scripts/deliver.py \
  --package /sessions/*/mnt/outputs/transcript-repurpose-{slug}-{ts}.md \
  --transcript /sessions/*/mnt/outputs/transcript-{slug}-{ts}.txt \
  --slug {slug} \
  --output-dir /sessions/*/mnt/Skills/online-content/repurpose/{slug}-{ts} \
  --source-url "{original_url}" \
  --platform "{platform}" \
  --title "{title}" \
  --duration-sec {duration} \
  --word-count {word_count} \
  --tier "{tier}"
```

The script returns a path to the folder. Hand the user a `computer://` link to `index.html` — opening it in a browser shows the Property-OS-styled preview with download buttons for each artifact.

## The HTML preview

The `index.html` is self-contained — no external dependencies, runs offline. Modern SaaS look (Vercel/Linear style):

- Header with title, source URL, platform badge, duration, word count, transcription tier, generated timestamp
- Files grid — every artifact rendered as a downloadable card with icon, name, description
- Hook variants preview block
- Full-package preview (scrollable, with a "copy full package" button)
- Footer

The HTML matches the visual language Property OS will eventually use, so editors get used to that look now. When Property OS launches with its real dashboard, the transition is muscle-memory.

## Save location

For Graeham personally, save into the regular outputs folder.

For published work that goes to the team, save into the `online-content` repo under `repurpose/` so it's persistently tracked and team members can find prior packages:

```
C:\Users\Graeham Watts\Documents\Skills LLMS\Claude\online-content\repurpose\{slug}-{YYYYMMDD-HHMM}\
```

This matches the pattern in `CLAUDE.md` — published content goes to the online-content repo, source code stays in the Skills repo.

## Edge cases

- **User only requested one derivative** (e.g., "just the IG Reel"): The skill still produces hooks + research, just skips the other platform scripts in Phase 6. Phase 9 only writes files for sections that exist.
- **Section parsing fails for a non-standard package**: The `deliver.py` script uses heading keyword matching, not strict regex. If a section is misnamed in the package markdown, it falls back to writing only the canonical `content-package.md` and the HTML preview without per-artifact files. Phase 8 should always produce the standard section headings.
- **Source transcript missing**: If Phase 0 fed Phase 1 directly without writing a transcript file, write the cleaned text from Phase 1's output as `transcript.txt` here so the artifact still exists.

## What gets stripped for the HeyGen-ready script

The HeyGen avatar reads the script word-for-word. Shot direction tags would get spoken aloud, which is catastrophic. The delivery script strips:

- Whole-line tags: `[TALKING HEAD]`, `[CUT]`, `[B-ROLL: <description>]`
- Inline tags: any `[ALL CAPS]` or `[ALL CAPS: text]` pattern embedded in dialogue lines

The result is paste-ready clean voice text. Graeham (or the editor) pastes this directly into HeyGen.

## Hand-off message to the user

After delivery, the skill returns this message to the user (with real values substituted):

```
Done. Repurposed package saved to:
{folder_path}

Open the preview: computer://{folder_path}/index.html

Files produced:
- transcript.txt — Raw transcript ({word_count} words)
- content-package.md — Full markdown (everything)
- hooks.md — 3 hook variants, top: "{recommended_hook}"
- script-yt-long.md, script-yt-short.md, script-ig-reel.md, script-tiktok.md
- captions.md — Per-platform captions
- ssml.xml — ElevenLabs paste-ready
- heygen-script.txt — HeyGen paste-ready (tags stripped)
- broll-prompts.md — {n} Higgsfield prompts
- editing-notes.md — For Jason

Next steps:
1. Open index.html to preview the package
2. Send heygen-script.txt + broll-prompts.md to Jason for the production
3. Use ssml.xml if generating voice in ElevenLabs first
```

This gives the user a one-glance summary of what was produced and where it lives.
