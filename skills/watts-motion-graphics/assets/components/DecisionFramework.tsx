import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { BRAND } from "../lib/brand";

interface Row {
  /** Condition text in the left column (e.g., "6+ months runway · sub-4% rate") */
  condition: string;
  /** Option label in the right column (e.g., "HELOC") */
  option: string;
}

interface Props {
  rows: Row[]; // Typically 3 rows
}

export const DecisionFramework: React.FC<Props> = ({ rows }) => {
  const frame = useCurrentFrame();
  const cardOpacity = interpolate(
    frame,
    [0, BRAND.animation.largeFadeIn],
    [0, 1],
    { extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        opacity: cardOpacity,
      }}
    >
      <div
        style={{
          backgroundColor: BRAND.colors.panelFill,
          minWidth: 830,
          position: "relative",
          padding: `${BRAND.spacing.panelPaddingV}px ${BRAND.spacing.largePaddingH}px`,
        }}
      >
        {/* Left edge vertical stroke */}
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            bottom: 0,
            width: BRAND.spacing.leftEdgeStroke,
            backgroundColor: BRAND.colors.generalAccent,
          }}
        />

        {rows.map((row, i) => {
          const rowFrame = i * BRAND.animation.rowStagger;
          const rowOpacity = interpolate(
            frame,
            [
              rowFrame + BRAND.animation.largeFadeIn,
              rowFrame + BRAND.animation.largeFadeIn + BRAND.animation.fadeIn,
            ],
            [0, 1],
            { extrapolateRight: "clamp" }
          );

          return (
            <div
              key={i}
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 60px 1fr",
                alignItems: "center",
                paddingTop: i === 0 ? 0 : BRAND.spacing.rowGap,
                paddingBottom: i === rows.length - 1 ? 0 : BRAND.spacing.rowGap,
                borderBottom:
                  i === rows.length - 1
                    ? "none"
                    : `1px solid ${BRAND.colors.generalAccent}E6`,
                opacity: rowOpacity,
              }}
            >
              {/* Left — condition */}
              <div
                style={{
                  fontFamily: BRAND.fonts.body,
                  fontSize: BRAND.sizes.bodyText,
                  fontWeight: 400,
                  color: BRAND.colors.bodyText,
                  lineHeight: 1.3,
                }}
              >
                {row.condition}
              </div>

              {/* Center — arrow */}
              <div
                style={{
                  fontFamily: BRAND.fonts.body,
                  fontSize: 24,
                  color: BRAND.colors.generalAccent,
                  textAlign: "center",
                }}
              >
                →
              </div>

              {/* Right — option label */}
              <div
                style={{
                  fontFamily: BRAND.fonts.display,
                  fontSize: BRAND.sizes.optionLabel,
                  fontWeight: 700,
                  letterSpacing: BRAND.tracking.optionLabel,
                  textTransform: "uppercase",
                  color: BRAND.colors.generalAccent,
                  textAlign: "right",
                }}
              >
                {row.option}
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
