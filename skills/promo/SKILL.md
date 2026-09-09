---
name: remotion:promo
description: Create product-level promotional videos and animations using vibe-motion (Remotion). Use when the user wants to build landing page media, mockups, or promotional videos that require 1:1 realistic UI recreation and smooth interactions.
metadata:
  tags: promo, promotional, landing-page, product-video, mockup, marketing
---

## When to use

Use this skill when the user wants to create promotional videos, landing page media, product mockups, or marketing animations that require realistic UI recreation and polished interactions.

For Remotion technical foundations (compositions, assets, sequencing, transitions, etc.), load the [remotion skill](../remotion/SKILL.md) alongside this one.

## Core Principles

1. **Product-Level Realism**: The goal is NOT to make "conceptual animations" or abstract floating cards. The UI must be a 1:1 pixel-perfect recreation of the real frontend application (SaaS-level quality).
2. **Hybrid Media Strategy**:
   - Primary focus: Real product UI layouts (borders, shadows, typography, colors).
   - Motion focus: Smooth state-driven transitions, real interaction simulations.
3. **One Core "Aha" Moment**: Each video scene should be short (6–8s) and focus on demonstrating exactly one core value proposition or workflow.

## Mandatory Workflow

**BEFORE writing any code for the UI, you MUST:**

1. **Locate Target UI**: Search the actual frontend repository for the components you are trying to simulate. Use `Glob` or `Grep` tools.
2. **Read Real Source Code**: Read the source code of those components to understand the exact DOM structure, nested layout wrappers, and Tailwind classes used in the real product.
3. **Analyze Element Hierarchy & Metrics**: Pay special attention to parent-child wrapper relationships (e.g., is the Right Panel a sibling to the Editor, or inside a specific main container?), and capture specific arbitrary Tailwind values (like `rounded-[32px]`, `shadow-[-20px_0_40px_...]`).
4. **NEVER Guess**: Do NOT guess or hallucinate the layout, colors, or structural hierarchy based on generic patterns. The UI must match the actual implementation exactly (e.g., using the precise `bg-stone-100` instead of a generic `bg-gray-50`, real icons, and exact border treatments).

## Implementation Methods

### 1. UI Recreation

- **DOM Structure**: Mimic the actual React component structure from the frontend codebase. Replicate the nesting.
- **Styling**: Use exact Tailwind utility classes or inline styles for colors (e.g., `bg-stone-50`, `border-stone-200`, `text-stone-900`), rounded corners (`rounded-xl`), and shadows (`shadow-sm`, `shadow-[...]`).
- **Layout**: Build the complete context. Don't just show an isolated component; show the sidebar, header, and workspace to provide a grounded, realistic environment.

### 2. Animation & Easing

All animations MUST be driven by `useCurrentFrame()` and use Remotion's `interpolate` + `Easing` API. See [timing rules](../remotion/rules/timing.md) for full details. CSS transitions or `requestAnimationFrame` are FORBIDDEN.

```tsx
import { useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

// Smooth ease-out for entrances
const opacity = interpolate(frame, [0, 0.5 * fps], [0, 1], {
  extrapolateRight: "clamp",
  easing: Easing.bezier(0.16, 1, 0.3, 1),
});

// Smooth ease-in-out for transitions
const slideX = interpolate(frame, [1 * fps, 2 * fps], [-100, 0], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
  easing: Easing.bezier(0.45, 0, 0.55, 1),
});
```

For staggered list/card animations, offset each item's input range:

```tsx
const staggerItem = (index: number, startSec: number, durationSec: number) =>
  interpolate(
    frame,
    [
      (startSec + index * 0.1) * fps,
      (startSec + index * 0.1 + durationSec) * fps,
    ],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp",
      easing: Easing.bezier(0.16, 1, 0.3, 1) },
  );
```

### 3. Interaction Simulation

To make the video feel like a real product recording:

- **Fake Cursors**: Add an SVG mouse cursor that moves (interpolate X and Y coordinates) and clicks (`scale(0.9)` on click frame). Pay extra attention to whether the click location is correct.
- **Typing Effects**: Simulate text input with a blinking cursor block, revealing characters one by one driven by `interpolate`.
- **Loading States**: Use skeleton screens (`animate-pulse`), spinners, and loading bars before revealing the final content.
- **Camera Work (Zoom/Pan)**: Use a wrapper div with `transform: scale(...) translate(...)` driven by `interpolate` to subtly zoom in on the action (e.g., zooming into a specific panel when an action is triggered).

### 4. Frame-Driven Timeline

Use `useCurrentFrame()` and time-in-seconds to define the sequence of events. Map each event to a frame range.

```tsx
const frame = useCurrentFrame();
const { fps } = useVideoConfig();
const sec = frame / fps;

// Timeline events
const isModalVisible = sec < 0.8;
const modalOpacity = interpolate(frame, [0, 0.3 * fps], [1, 0], {
  extrapolateRight: "clamp",
});

const showFirstMsg = sec > 1.5;
const firstMsgOpacity = interpolate(
  frame,
  [1.5 * fps, 2 * fps],
  [0, 1],
  { extrapolateLeft: "clamp", extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1) },
);

const cursorX = interpolate(
  frame,
  [3 * fps, 3.8 * fps],
  [200, 450],
  { extrapolateLeft: "clamp", extrapolateRight: "clamp",
    easing: Easing.bezier(0.45, 0, 0.55, 1) },
);
```

## Checklist for Scene Creation

- [ ] **MANDATORY**: Did you actively search and read the actual frontend codebase for the target components BEFORE writing the scene?
- [ ] Does the UI match the real frontend code 1:1 (color palette, DOM nesting, exact Tailwind classes)?
- [ ] Is the context complete? (e.g., Sidebar, Header, Main Content Area)
- [ ] Are animations using Remotion `interpolate` + `Easing.bezier` instead of CSS transitions or linear interpolation?
- [ ] Are there simulated micro-interactions? (Cursor movements, hover states, button clicks, typing)
- [ ] Does the sequence clearly tell a single, impactful story within the 6–8s duration?
