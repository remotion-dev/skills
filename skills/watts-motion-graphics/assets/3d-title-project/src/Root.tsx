import React from "react";
import { Composition } from "remotion";
import { Title } from "./compositions/Title";
import { GOLD_VARIANTS, GoldVariantKey } from "./layout";

// ---- locked content + type system ----
const CURSIVE_LINE = "Bay Area Expert";
const GOLD_LINE = "GRAEHAM WATTS";
const THIRD_LINE = "650-308-4727";
// 8s: line entries at 0s / 2s / 4s, hold, then fade out over the last ~0.8s
const DURATION_FRAMES = 240;
const FPS = 30;

// shared defaults for the locked type system
const BASE = {
  cursiveLine: CURSIVE_LINE,
  goldLine: GOLD_LINE,
  thirdLine: THIRD_LINE,
  spacingMode: "balanced" as const,
  goldFont: "archivo-black" as const,
  cursiveFont: "sacramento" as const,
  bodyFont: "archivo" as const,
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* ---- main deliverables: 3-line title, locked fonts ---- */}
      <Composition
        id="TitleLandscape"
        component={Title}
        durationInFrames={DURATION_FRAMES}
        fps={FPS}
        width={1920}
        height={1080}
        defaultProps={{ ...BASE, goldVariant: "rich-gold" as const }}
      />
      <Composition
        id="TitlePortrait"
        component={Title}
        durationInFrames={DURATION_FRAMES}
        fps={FPS}
        width={1080}
        height={1920}
        defaultProps={{ ...BASE, goldVariant: "rich-gold" as const }}
      />

      {/* ---- gold-chrome material comparison (active decision) ---- */}
      {(Object.keys(GOLD_VARIANTS) as GoldVariantKey[]).map((key) => (
        <Composition
          key={`goldvar-${key}`}
          id={`GoldVariant-${key}`}
          component={Title}
          durationInFrames={1}
          fps={FPS}
          width={1920}
          height={1080}
          defaultProps={{ ...BASE, frozen: true, goldVariant: key }}
        />
      ))}
    </>
  );
};
