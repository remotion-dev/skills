import { continueRender, delayRender } from "remotion";

// ---- cursive accent fonts ----
import "@fontsource/great-vibes/latin-400.css";
import "@fontsource/allura/latin-400.css";
import "@fontsource/dancing-script/latin-400.css";
import "@fontsource/sacramento/latin-400.css";

// ---- Archivo: the whole flat-text system, one family ----
// Upright weights 400-900...
import "@fontsource/archivo/latin-400.css";
import "@fontsource/archivo/latin-500.css";
import "@fontsource/archivo/latin-600.css";
import "@fontsource/archivo/latin-700.css";
import "@fontsource/archivo/latin-800.css";
import "@fontsource/archivo/latin-900.css";
// ...and the matching italics.
import "@fontsource/archivo/latin-400-italic.css";
import "@fontsource/archivo/latin-500-italic.css";
import "@fontsource/archivo/latin-600-italic.css";
import "@fontsource/archivo/latin-700-italic.css";
import "@fontsource/archivo/latin-800-italic.css";
import "@fontsource/archivo/latin-900-italic.css";
//
// NOTE: Archivo's hairline weights (100/200/300) are deliberately NOT loaded.
// They're too thin to survive as burned-in text over b-roll - they vanish.
// If a future design genuinely needs them, add the import + a load() line
// below; nothing else has to change.

// cursive font catalog
export const CURSIVE_FONTS = {
  "great-vibes": { family: "'Great Vibes', cursive", label: "Great Vibes (elegant formal)" },
  allura: { family: "'Allura', cursive", label: "Allura (flowing, refined)" },
  "dancing-script": { family: "'Dancing Script', cursive", label: "Dancing Script (casual, friendly)" },
  sacramento: { family: "'Sacramento', cursive", label: "Sacramento (clean modern script)" },
} as const;

export type CursiveFontKey = keyof typeof CURSIVE_FONTS;

// The flat-text family. One entry on purpose - the whole system is Archivo.
// Weight + italic are chosen at the call site (see ARCHIVO_ROLES for the
// recommended mapping).
export const BODY_FONTS = {
  archivo: { family: "'Archivo', sans-serif", label: "Archivo (full weight + italic range)" },
} as const;

export type BodyFontKey = keyof typeof BODY_FONTS;

// Recommended weight/style for each flat-text role. The skill reads from
// this so every video uses the same tier mapping.
export const ARCHIVO_ROLES = {
  hero3D: { note: "uses Archivo Black (separate typeface file), not this family" },
  chunkyTitle: { weight: 800, italic: false },
  subHead: { weight: 600, italic: false },
  body: { weight: 400, italic: false },
  bodyMedium: { weight: 500, italic: false },
  emphasis: { weight: 600, italic: true },
} as const;

// Block the render until every font file has actually loaded, so no frame
// silently falls back to a default.
const handle = delayRender("Loading fonts");

if (typeof document !== "undefined") {
  const archivoWeights = [400, 500, 600, 700, 800, 900];
  const loads: Promise<unknown>[] = [
    document.fonts.load("400 120px 'Great Vibes'"),
    document.fonts.load("400 120px 'Allura'"),
    document.fonts.load("400 120px 'Dancing Script'"),
    document.fonts.load("400 120px 'Sacramento'"),
  ];
  for (const w of archivoWeights) {
    loads.push(document.fonts.load(`${w} 80px 'Archivo'`));
    loads.push(document.fonts.load(`italic ${w} 80px 'Archivo'`));
  }
  Promise.all(loads)
    .then(() => continueRender(handle))
    .catch(() => continueRender(handle));
} else {
  continueRender(handle);
}
