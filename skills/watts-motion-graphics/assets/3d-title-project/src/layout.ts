// Shared layout constants + the math that converts camera distance into
// how wide the visible frame is in 3D world units. Kept in one place so the
// measuring code (Title) and the rendering code (GoldText3D) agree exactly.

export const CAMERA_FOV = 38;
export const GOLD_FONT_SIZE = 1.0;

// 3D font catalog - the typeface JSON filename (in public/) + a label.
// helvetiker ships with three.js; the rest were converted from webfonts.
export const GOLD_FONTS = {
  helvetiker: {
    file: "helvetiker_bold.typeface.json",
    label: "Helvetiker Bold (clean, neutral)",
  },
  "archivo-black": {
    file: "archivo-black.typeface.json",
    label: "Archivo Black (heavy, blocky)",
  },
  anton: {
    file: "anton.typeface.json",
    label: "Anton (tall, condensed, dramatic)",
  },
  poppins: {
    file: "poppins-bold.typeface.json",
    label: "Poppins Bold (rounded, geometric)",
  },
} as const;

export type GoldFontKey = keyof typeof GOLD_FONTS;

// Gold-chrome material presets. All base colors are anchored to / derived
// from the Watts brand gold; the look comes from material + lighting, not
// just the base color. emissive keeps shadowed faces warm instead of muddy.
export const GOLD_VARIANTS = {
  "rich-gold": {
    label: "Rich Saturated Gold (warm, high-contrast)",
    color: "#C69320",
    metalness: 1.0,
    roughness: 0.16,
    envMapIntensity: 1.55,
    exposure: 1.32,
    emissive: "#1f1304",
    emissiveIntensity: 0.32,
  },
  "polished-brand": {
    label: "Polished Brand Gold (#B8945A, satin-shiny)",
    color: "#B8945A",
    metalness: 1.0,
    roughness: 0.11,
    envMapIntensity: 2.1,
    exposure: 1.25,
    emissive: "#000000",
    emissiveIntensity: 0,
  },
  "bright-chrome": {
    label: "Bright Gold Chrome (#C4A265, mirror finish)",
    color: "#C4A265",
    metalness: 1.0,
    roughness: 0.05,
    envMapIntensity: 2.9,
    exposure: 1.4,
    emissive: "#000000",
    emissiveIntensity: 0,
  },
  "hot-gold": {
    label: "Hot Gold Chrome (brightest, most reflective)",
    color: "#D9B45C",
    metalness: 1.0,
    roughness: 0.06,
    envMapIntensity: 3.2,
    exposure: 1.5,
    emissive: "#000000",
    emissiveIntensity: 0,
  },
  "deep-luxe": {
    label: "Deep Luxe Gold (#B8945A, rich satin metal)",
    color: "#B8945A",
    metalness: 1.0,
    roughness: 0.17,
    envMapIntensity: 1.9,
    exposure: 1.3,
    emissive: "#000000",
    emissiveIntensity: 0,
  },
} as const;

export type GoldVariantKey = keyof typeof GOLD_VARIANTS;

// visible width in world units at z = 0, for a given camera distance + aspect
export function visibleWorldWidth(
  cameraZ: number,
  pixelWidth: number,
  pixelHeight: number
): number {
  const fovRad = (CAMERA_FOV * Math.PI) / 180;
  const visibleHeight = 2 * cameraZ * Math.tan(fovRad / 2);
  return visibleHeight * (pixelWidth / pixelHeight);
}
