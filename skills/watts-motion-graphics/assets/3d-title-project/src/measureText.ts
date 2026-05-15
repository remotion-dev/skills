// Measures how wide a string will be when rendered by Three.js TextGeometry,
// by reading the typeface JSON's own glyph metrics. This is deterministic and
// runs in the normal DOM React tree - so it works with delayRender, unlike
// trying to measure geometry inside the R3F canvas (different reconciler,
// async font load, effects don't fire predictably).

type Glyph = { ha: number; x_min: number; x_max: number };
type TypefaceFont = {
  resolution: number;
  glyphs: Record<string, Glyph>;
};

const cache = new Map<string, TypefaceFont>();

export async function loadTypeface(url: string): Promise<TypefaceFont> {
  const cached = cache.get(url);
  if (cached) return cached;
  const res = await fetch(url);
  const font = (await res.json()) as TypefaceFont;
  cache.set(url, font);
  return font;
}

// width in world units for a given Text3D `size`. Sums glyph advances the
// same way TextGeometry lays out characters; trims the last glyph's trailing
// advance so the result matches the visible geometry width closely.
export function measureTextWidth(
  font: TypefaceFont,
  text: string,
  size: number
): number {
  if (text.length === 0) return 0;
  const scale = size / font.resolution;
  let advance = 0;
  for (const ch of text) {
    const glyph = font.glyphs[ch] ?? font.glyphs["?"];
    if (glyph) advance += glyph.ha;
  }
  // last visible glyph: its advance overshoots actual ink by (ha - x_max)
  const lastCh = text[text.length - 1];
  const lastGlyph = font.glyphs[lastCh] ?? font.glyphs["?"];
  if (lastGlyph) advance -= lastGlyph.ha - lastGlyph.x_max;
  return advance * scale;
}
