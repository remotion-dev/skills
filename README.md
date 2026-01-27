# @remotion/skills

A Claude Code plugin providing domain-specific knowledge for [Remotion](https://remotion.dev) - the framework for creating motion graphics and videos programmatically in React.

## Installation

Install this plugin from a Claude Code marketplace:

```bash
/plugin install remotion
```

Or test locally during development:

```bash
claude --plugin-dir ./remotion-dev-skills
```

## What's Included

This plugin provides Claude with a **remotion-best-practices** skill that automatically activates when working with Remotion code. It includes:

- 31 detailed rule files covering all major Remotion features
- Code examples demonstrating correct usage patterns
- Best practices for animations, compositions, and media handling

## Plugin Structure

```
.claude-plugin/
└── plugin.json           # Plugin manifest

skills/
└── remotion/
    ├── SKILL.md          # Main skill definition
    └── rules/            # 31 topic-specific guides
        ├── animations.md
        ├── compositions.md
        └── ...
```

## Documentation Topics

| Category | Topics |
|----------|--------|
| Animation | animations, timing, transitions, sequencing, text-animations, trimming |
| Media | assets, images, videos, audio, fonts, gifs, lottie |
| Composition | compositions, calculate-metadata, parameters |
| Processing | get-video-duration, get-audio-duration, get-video-dimensions, can-decode, extract-frames |
| Advanced | 3d, charts, maps, tailwind, display-captions, transcribe-captions, measuring-text |

## Development

```bash
# Start Remotion Studio to test example compositions
npm run dev
```

## License

Part of the [Remotion](https://github.com/remotion-dev/remotion) project.
