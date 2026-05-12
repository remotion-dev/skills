import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { BRAND } from "../lib/brand";

interface StatProps {
  eyebrow: string;
  value: string;
  /** True if this side is the "win" / emphasis side — renders value in gold */
  emphasize?: boolean;
}

interface Props {
  left: StatProps;
  right: StatProps;
}

const StatBox: React.FC<StatProps> = ({ eyebrow, value, emphasize }) => (
  <div
    style={{
      backgroundColor: BRAND.colors.panelFill,
      padding: `${BRAND.spacing.panelPaddingV}px ${BRAND.spacing.panelPaddingH}px`,
      minWidth: 320,
      textAlign: "center",
      position: "relative",
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
);

export const CompareCard: React.FC<Props> = ({ left, right }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, BRAND.animation.fadeIn], [0, 1], {
    extrapolateRight: "clamp",
  });
  const vsOpacity = interpolate(
    frame,
    [4, 4 + BRAND.animation.fadeIn],
    [0, 1],
    { extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{ justifyContent: "center", alignItems: "center", opacity }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: BRAND.spacing.pairGap,
        }}
      >
        <StatBox {...left} />
        <div
          style={{
            fontFamily: BRAND.fonts.body,
            fontSize: 36,
            fontWeight: 500,
            color: BRAND.colors.bodyText,
            opacity: vsOpacity,
          }}
        >
          vs
        </div>
        <StatBox {...right} />
      </div>
    </AbsoluteFill>
  );
};
