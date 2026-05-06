// Watts Motion Graphics — Brand Tokens
// Copy this file to src/lib/brand.ts in any Remotion project using the Watts overlay system.
// DO NOT EDIT the values without explicit approval — they are the locked brand system.

export const BRAND = {
  // Colors
  colors: {
    /** Reserved — used elsewhere in brand system, not in overlays */
    wattsNavy: "#0A1F44",
    /** HERO BEAT ONLY — one use per video, the climax moment */
    wattsGold: "#B8945A",
    /** All other gold accents (top borders, arrows, separators, option labels) */
    generalAccent: "#C4A265",
    /** Primary numbers and main labels */
    white: "#FFFFFF",
    /** All graphic boxes — solid black */
    panelFill: "#000000",
    /** Body copy on black panels — soft white */
    bodyText: "rgba(255, 255, 255, 0.85)",
    /** Eyebrow labels in light variant */
    labelMuted: "rgba(255, 255, 255, 0.6)",
    /** Pure chroma green canvas — NEVER change this */
    chromaGreen: "#00FF00",
  },

  // Typography
  fonts: {
    /** Display font — HERO, scene titles, option labels. Bold weight. */
    display: "Syne, 'Space Grotesk', 'Inter', sans-serif",
    /** Body font — eyebrow labels, body copy. */
    body: "Inter, 'SF Pro Display', system-ui, sans-serif",
  },

  // Font sizes (in pixels at 1920×1080 — scale up for short-form)
  sizes: {
    hero: 240, // 220-280pt range, tweak per word length
    sceneTitle: 56,
    optionLabel: 40,
    bigNumber: 64,
    eyebrowLabel: 11,
    bodyText: 24,
    nameLabel: 36,
    roleLabel: 18,
  },

  // Letter spacing
  tracking: {
    eyebrow: "2px", // Tracked-out uppercase eyebrow labels
    optionLabel: "0.5px",
    bodyText: "normal",
  },

  // Spacing system
  spacing: {
    panelPaddingV: 28, // Top/bottom padding inside panels
    panelPaddingH: 36, // Left/right padding inside panels
    largePaddingH: 40, // Horizontal padding for large panels (decision framework)
    rowGap: 28, // Between rows in stacked cards
    pairGap: 36, // Between paired panels and `vs` token
    accentStroke: 2, // Border accent stroke width
    leftEdgeStroke: 3, // Vertical left edge stroke on decision framework
  },

  // Animation timings (in frames at 30fps)
  animation: {
    fadeIn: 8,
    fadeOut: 8,
    largeFadeIn: 12,
    heroScaleIn: 24, // 0.8s
    heroScaleOut: 12,
    rowStagger: 8, // Decision framework row stagger
  },

  // Hold durations (in seconds)
  holds: {
    statCallout: 4,
    compareCard: 5,
    decisionFramework: 6,
    hero: 6, // 5-7s range, never less than 5
    endCard: 5,
  },
} as const;

/** Canvas dimensions */
export const CANVAS = {
  longform: { width: 1920, height: 1080 },
  shortform: { width: 1080, height: 1920 },
} as const;

export const FPS = 30;
