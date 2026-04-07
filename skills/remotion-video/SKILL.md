---
name: remotion-video
description: "Remotion Video Generator — creates professional React-based video projects using Remotion. Use this skill ANY time the user mentions: Remotion, React video, programmatic video, component-based video, animated video with React, Remotion composition, video template system, video from code, code-based video, or anything related to creating videos using React components and Remotion. Also trigger when the user wants reusable video components, animated compositions, property showcase videos, or asks to build a video template system. This skill generates complete Remotion projects with TypeScript, proper compositions, and render-ready output."
---

# Remotion Video Skill

Generate complete, production-ready Remotion video projects using React + TypeScript. This skill creates reusable component libraries, proper composition timelines, and fully typed video templates.

## What is Remotion?

Remotion is a framework for creating videos programmatically using React. Instead of a video editor, you write React components that render frame-by-frame. Remotion then uses a headless browser to capture each frame and ffmpeg to encode the final video.

## Environment Constraints

**Important**: Remotion rendering requires Chromium/Chrome to be installed. In the Cowork sandbox, Chrome cannot be installed. This means:

1. We **can** scaffold, write, and validate (typecheck) Remotion projects
2. We **cannot** render the final MP4 inside Cowork
3. The user renders locally with one command: `npm run render`

If the user needs a fully rendered MP4 without local setup, use the **video-creator** skill instead (Python + ffmpeg, renders in-sandbox).

## Project Structure

Always create this structure:

```
project-name/
├── package.json
├── tsconfig.json
├── remotion.config.ts
├── CLAUDE.md              ← Component API docs + render instructions
├── src/
│   ├── index.ts           ← registerRoot entry point
│   ├── Root.tsx            ← Composition registry
│   ├── lib/
│   │   ├── types.ts       ← All TypeScript interfaces
│   │   └── brand.ts       ← Brand system (colors, fonts, spacing)
│   ├── components/
│   │   └── *.tsx           ← Reusable video components
│   └── data/
│       └── sample.ts      ← Default data (easily swappable)
└── public/                ← Static assets (photos, logos, fonts)
```

## Step-by-Step Workflow

### 1. Scaffold the project

```bash
mkdir project-name && cd project-name
npm init -y
npm install remotion @remotion/cli @remotion/bundler react react-dom
npm install -D typescript @types/react @types/react-dom
```

### 2. Configure TypeScript

```json
{
  "compilerOptions": {
    "target": "ES2018",
    "module": "Node16",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "moduleResolution": "node16",
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"]
}
```

### 3. Create components

Each component should:
- Accept all visual data as props (no hardcoded content)
- Accept an optional `brand` prop for color/font overrides
- Accept an `animDelay` prop for staggered entrance animations
- Use Remotion's `useCurrentFrame()` + `interpolate()` for all animation
- Use `Easing` functions for professional motion (cubic, back, elastic)

### 4. Register compositions in Root.tsx

```tsx
import { Composition } from "remotion";

// Remotion requires Props extends Record<string, unknown>
// Use this helper for typed components:
const asComp = (c: any) => c;

<Composition
  id="MyVideo"
  component={asComp(MyComponent)}
  durationInFrames={90 * 30}
  fps={30}
  width={1080}
  height={1920}
  defaultProps={sampleData}
/>
```

### 5. Validate

```bash
npx tsc --noEmit  # Must pass with zero errors
```

### 6. Package for the user

- Create a tarball excluding node_modules: `tar -czf project.tar.gz --exclude=node_modules project/`
- Save to outputs folder
- Include clear render instructions

## Key Remotion APIs

### Animation
```tsx
import { useCurrentFrame, interpolate, Easing, spring } from "remotion";

const frame = useCurrentFrame();
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
  easing: Easing.out(Easing.cubic),
});
```

### Sequencing
```tsx
import { Sequence } from "remotion";

<Sequence from={90} durationInFrames={150} name="Section Name">
  <MyComponent />
</Sequence>
```

### Images
```tsx
import { Img, staticFile } from "remotion";

<Img src={staticFile("photo.jpg")} style={{ objectFit: "cover" }} />
// Or from props:
<Img src={photoUrl} />
```

### Frame Math
```tsx
const FPS = 30;
const sec = (s: number) => Math.round(s * FPS);
// sec(5) = 150 frames = 5 seconds
```

## Aspect Ratios

| Format | Width | Height | Use Case |
|--------|-------|--------|----------|
| Portrait (9:16) | 1080 | 1920 | Reels, Shorts, TikTok |
| Landscape (16:9) | 1920 | 1080 | YouTube, presentations |
| Square (1:1) | 1080 | 1080 | Instagram feed |

## Graeham Watts Brand Defaults

When building videos for Graeham (default user), use these brand values:
- Gold: #C4A265
- Black: #1C1C1C
- White: #FFFFFF
- Dark Navy: #1a2744
- Mid Blue: #2d4278
- Accent Green: #1a7a56
- Headline Font: Eagle CG Bold (fallback: Bebas Neue, Oswald)
- Body Font: SF Pro Display (fallback: Inter, system)
- Agent: Graeham Watts, REALTOR®, Intero (Berkshire Hathaway)
- DRE: 01466876
- Phone: 650-308-4727
- Email: graehamwatts@gmail.com

## Common Patterns

### Staggered entrance
```tsx
const items = ["A", "B", "C"];
{items.map((item, i) => (
  <AnimatedItem key={item} delay={baseDelay + i * 15} />
))}
```

### Ken Burns effect
```tsx
const scale = interpolate(frame, [0, totalFrames], [1, 1.12]);
<div style={{ transform: `scale(${scale})` }}>
  <Img src={photo} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
</div>
```

### Gold accent line animation
```tsx
const lineWidth = interpolate(frame, [delay, delay + 30], [0, 300], {
  easing: Easing.out(Easing.cubic),
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
<div style={{ width: lineWidth, height: 4, backgroundColor: brand.gold }} />
```

## Render Instructions (for the user)

Include these in every project's CLAUDE.md:

```
## How to Render

1. Make sure you have Node.js installed (v18+): https://nodejs.org
2. Open a terminal and navigate to the project folder
3. Install dependencies: npm install
4. Preview in browser: npm run studio
5. Render final video: npm run render
6. Your video will be at: out/showcase.mp4
```
