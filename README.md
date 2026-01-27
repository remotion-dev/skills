# @remotion/skills

A Claude plugin providing domain-specific knowledge for [Remotion](https://remotion.dev) - the framework for creating motion graphics and videos programmatically in React.

## Overview

This repository contains comprehensive documentation and best practices for Remotion development. It serves as a knowledge base that Claude can reference when helping developers create video compositions.

## Usage

### As a Claude Plugin

This repository is designed to be used as a Claude plugin. When Claude Code is working in a project that uses Remotion, it can reference this knowledge base to provide accurate guidance.

### Development

```bash
# Install dependencies
npm install

# Start Remotion Studio
npm run dev
```

## Contents

- **CLAUDE.md** - Plugin configuration and usage instructions for Claude
- **skills/remotion/SKILL.md** - Main skill definition and index
- **skills/remotion/rules/** - 31 detailed documentation files covering:
  - Animations and timing
  - Media assets (images, videos, audio, fonts)
  - Compositions and configuration
  - Advanced features (3D, charts, captions, maps)

## Documentation Topics

| Category | Topics |
|----------|--------|
| Animation | animations, timing, transitions, sequencing, text-animations |
| Media | assets, images, videos, audio, fonts, gifs, lottie |
| Composition | compositions, calculate-metadata, parameters |
| Processing | get-video-duration, get-audio-duration, can-decode, extract-frames |
| Advanced | 3d, charts, maps, tailwind, display-captions |

## License

Part of the [Remotion](https://github.com/remotion-dev/remotion) project.
