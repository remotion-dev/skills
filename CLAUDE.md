# Remotion Skills - Claude Plugin

This is a knowledge base and skills documentation repository for **Remotion**, a framework for creating motion graphics and videos programmatically in React.

## Purpose

This plugin provides Claude with domain-specific knowledge about Remotion development. When helping users with Remotion code, Claude should reference the documentation in this repository to provide accurate, up-to-date guidance.

## Project Structure

```
skills/remotion/
├── SKILL.md              # Main skill definition and index
└── rules/                # Detailed documentation files
    ├── animations.md     # Core animation principles
    ├── compositions.md   # Defining compositions
    ├── assets.md         # Importing media assets
    └── ...               # 31 topic-specific guides
```

## How to Use This Knowledge Base

When working with Remotion code, read the relevant rule files from `skills/remotion/rules/` to get:

- **Best practices** for the specific feature being implemented
- **Code examples** demonstrating correct usage
- **API details** for Remotion components and hooks

### Key Rule Files by Topic

**Animation & Timing:**
- `animations.md` - useCurrentFrame(), interpolate(), animation basics
- `timing.md` - Easing functions, spring animations
- `transitions.md` - Scene transitions
- `sequencing.md` - Sequence component, timing patterns

**Media Assets:**
- `assets.md` - General asset importing
- `images.md` - Img component usage
- `videos.md` - Video embedding, trimming, looping
- `audio.md` - Audio playback, volume control
- `fonts.md` - Google Fonts and local fonts
- `gifs.md` - GIF synchronization

**Compositions:**
- `compositions.md` - Composition setup, stills, folders
- `calculate-metadata.md` - Dynamic duration and dimensions
- `parameters.md` - Parametrizable videos with Zod

**Advanced Features:**
- `3d.md` - Three.js integration
- `charts.md` - Data visualization
- `lottie.md` - Lottie animations
- `maps.md` - Mapbox integration
- `display-captions.md` - Caption display
- `tailwind.md` - TailwindCSS usage

## Development Commands

```bash
# Start Remotion Studio for development
npm run dev
```

## Important Conventions

1. **Always use Remotion hooks** - Use `useCurrentFrame()` and `useVideoConfig()` for animation timing
2. **Use interpolate() for animations** - Map frame numbers to animated values
3. **Static imports for assets** - Import assets at module level, not dynamically
4. **Compositions define videos** - Each video is a Composition with defined dimensions and duration

## Example Compositions

Working examples are available in:
- `skills/remotion/rules/assets/charts-bar-chart.tsx`
- `skills/remotion/rules/assets/text-animations-typewriter.tsx`
- `skills/remotion/rules/assets/text-animations-word-highlight.tsx`

These demonstrate real implementations of common patterns.
