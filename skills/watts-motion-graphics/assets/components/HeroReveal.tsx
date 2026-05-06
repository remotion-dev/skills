import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { BRAND } from "../lib/brand";

interface Props {
  /** The HERO word or phrase (e.g., "TAX-FREE") */
  text: string;
  /** Position the text in the bottom-third or right-third (never centered) */
  anchor?: "bottom-right" | "bottom-left" | "right";
  /** Optional override for size — default 240px */
  size?: number;
  /** Total hold duration in frames — used to time the scale-out */
  holdFrames: number;
}

export const HeroReveal: React.FC<Props> = ({
  text,
  anchor = "bottom-right",
  size = BRAND.sizes.hero,
  holdFrames,
}) => {
  const frame = useCurrentFrame();

  // Scale in 95 → 100 over heroScaleIn frames
  const scaleIn = interpolate(
    frame,
    [0, BRAND.animation.heroScaleIn],
    [0.95, 1],
    { extrapolateRight: "clamp" }
  );

  // Opacity fade in
  const opacityIn = interpolate(
    frame,
    [0, BRAND.animation.heroScaleIn],
    [0, 1],
    { extrapolateRight: "clamp" }
  );

  // Scale out 100 → 105 in the last heroScaleOut frames
  const scaleOut = interpolate(
    frame,
    [holdFrames - BRAND.animation.heroScaleOut, holdFrames],
    [1, 1.05],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // Opacity fade out in last heroScaleOut frames
  const opacityOut = interpolate(
    frame,
    [holdFrames - BRAND.animation.heroScaleOut, holdFrames],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const finalScale = frame < BRAND.animation.heroScaleIn ? scaleIn : scaleOut;
  const finalOpacity =
    frame < BRAND.animation.heroScaleIn ? opacityIn : opacityOut;

  // Anchor positioning — never centered
  const justify =
    anchor === "bottom-left" ? "flex-start" : "flex-end";
  const align =
    anchor === "right" ? "center" : "flex-end";
  const padding =
    anchor === "bottom-right"
      ? "0 80px 80px 0"
      : anchor === "bottom-left"
      ? "0 0 80px 80px"
      : "0 80px 0 0";

  return (
    <AbsoluteFill
      style={{
        justifyContent: align,
        alignItems: justify,
        padding,
      }}
    >
      <div
        style={{
          fontFamily: BRAND.fonts.display,
          fontSize: size,
          fontWeight: 700,
          textTransform: "uppercase",
          color: BRAND.colors.wattsGold, // HERO ONLY
          letterSpacing: "-0.02em",
          lineHeight: 0.9,
          opacity: finalOpacity,
          transform: `scale(${finalScale})`,
          transformOrigin: anchor === "bottom-left" ? "left bottom" : "right bottom",
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};
