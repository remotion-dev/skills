import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { BRAND } from "../lib/brand";

interface Props {
  /** Tiny uppercase label above the big number (e.g., "GLOBAL LAYOFFS · META · APRIL 23") */
  eyebrow: string;
  /** The big number/value (e.g., "8,000", "$100K", "+19%") */
  value: string;
  /** Optional: render value in gold instead of white for emphasis */
  emphasize?: boolean;
  /** Optional: position on canvas. Defaults to centered. */
  position?: { x?: number; y?: number };
}

export const StatCallout: React.FC<Props> = ({
  eyebrow,
  value,
  emphasize = false,
  position,
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, BRAND.animation.fadeIn], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: position?.y ? "flex-start" : "center",
        alignItems: position?.x ? "flex-start" : "center",
        opacity,
      }}
    >
      <div
        style={{
          backgroundColor: BRAND.colors.panelFill,
          padding: `${BRAND.spacing.panelPaddingV}px ${BRAND.spacing.panelPaddingH}px`,
          minWidth: 440,
          textAlign: "center",
          position: "relative",
          marginLeft: position?.x ?? 0,
          marginTop: position?.y ?? 0,
        }}
      >
        {/* Top accent stroke */}
        <div
          style={{
            position: "absolute",
            top: 0,
            left: "10%",
            right: "10%",
            height: BRAND.spacing.accentStroke,
            backgroundColor: BRAND.colors.generalAccent,
          }}
        />

        {/* Eyebrow label */}
        <div
          style={{
            fontFamily: BRAND.fonts.body,
            fontSize: BRAND.sizes.eyebrowLabel,
            fontWeight: 700,
            letterSpacing: BRAND.tracking.eyebrow,
            textTransform: "uppercase",
            color: BRAND.colors.generalAccent,
            marginBottom: 14,
          }}
        >
          {eyebrow}
        </div>

        {/* Big number */}
        <div
          style={{
            fontFamily: BRAND.fonts.display,
            fontSize: BRAND.sizes.bigNumber,
            fontWeight: 800,
            color: emphasize ? BRAND.colors.generalAccent : BRAND.colors.white,
            lineHeight: 1,
          }}
        >
          {value}
        </div>
      </div>
    </AbsoluteFill>
  );
};
