# Phase 1 — Ingest the Transcript

The job of this phase is simple: normalize whatever messy thing the user hands over into a clean `source_text` string plus a small `source_metadata` block. Don't write or analyze yet — just normalize.

## Accepted Input Formats

### 1. Pasted text (most common with SurfFast)

User pastes the transcript directly in chat. Strip:
- Quote markers (`>`, `"`, `'`, smart-quote variants)
- Leading/trailing whitespace per line
- Speaker labels if any (`Speaker 1:`, `Host:`, `[NARRATOR]`)
- Timestamps embedded inline (`[0:42]`, `(1:15)`, `00:00:23,500`)
- Repeated filler that obviously came from auto-transcription glitches (consecutive duplicate words, `[Music]`, `[Applause]`, `[Laughter]`)

Preserve:
- Sentence punctuation
- Paragraph breaks (signal of natural pauses)
- Proper nouns capitalized (don't lower-case everything)

### 2. `.txt` file

Read with the Read tool. Treat content same as pasted text — run the same strip rules.

### 3. `.srt` subtitle file

Structure looks like:

```
1
00:00:00,000 --> 00:00:03,500
Welcome back to the channel.

2
00:00:03,500 --> 00:00:07,200
Today we're talking about mortgage rates.
```

Strip sequence numbers, timing cues, and re-flow into continuous prose. Preserve paragraph breaks where there's a >2 second gap (signal of section breaks).

### 4. `.vtt` subtitle file

Similar to SRT but with `WEBVTT` header and slightly different timing format (`00:00:00.000 --> 00:00:03.500`). Same stripping rules.

### 5. SurfFast JSON

If SurfFast exports JSON, look for a `text`, `transcript`, or `subtitles` field. Extract it. Pull source metadata from:
- `source_url` → tells you the platform (instagram.com → IG, youtube.com → YT, tiktok.com → TT)
- `title` or `description` → useful as a fallback topic clue
- `creator` or `channel` → note for context but don't include in Graeham's output
- `duration` → calculate spoken pace from word count

### 6. Audio file (`.mp3`, `.wav`, `.m4a`, `.mp4` with audio)

**Stop. We don't transcribe in this skill.** Tell the user one of:

> "I can rebuild this once we have the transcript. You have two options: (1) run the audio through SurfFast's own subtitle download, or (2) use the Content Engine's Whisper transcriber (`video-script-creation-engine/scripts/youtube_transcriber.py`) — it's free and local. Paste the transcript back here when ready."

This isn't dodging — transcription is a separate concern with its own tooling, and the Content Engine already has it solved.

## Output of Phase 1

Produce two artifacts and pass them to Phase 2:

### `source_text`

The clean continuous-prose version, no timing, no speaker labels, no transcription artifacts. This is the only thing Phase 2 will read for analysis.

### `source_metadata`

A single paragraph:

```
Source: <platform if known, else "unknown">
Approx length: <word count> words / ~<duration estimate> when spoken
Creator handle (for reference only, will not appear in Graeham's output): <handle if visible>
Anomalies flagged: <anything suspicious — auto-transcription errors, missing chunks, language switches, etc.>
```

The creator handle is captured ONLY so Phase 4 can verify any factual claims the creator made (e.g., if they say "I'm a CFP" we know to verify the data they cite). It will never appear in Graeham's repurposed output. We are not crediting or referencing the original creator — repurposing is rewriting in Graeham's voice with his own framing and evidence.

## Edge Cases

- **Transcript is in another language.** Ask the user if they want the rebuild in English or in the source language. Default to English unless told otherwise.
- **Transcript is very short (< 50 words).** Probably not enough source signal to repurpose. Tell the user — it's better to use the Content Engine to write from scratch than to stretch a thin transcript.
- **Transcript is very long (> 4000 words, i.e. long podcast).** Ask the user: do they want one long-form repurpose covering the full thing, or should we extract the 2-3 strongest segments and repurpose each separately? Recommend the latter for podcasts — it produces tighter content.
- **Transcript has obvious factual errors.** Flag them in the `source_metadata` so Phase 4 knows not to carry them forward.
- **Transcript contains demographic/Fair-Housing-violating language.** Flag those exact lines. Phase 6 will strip them with explanation.
