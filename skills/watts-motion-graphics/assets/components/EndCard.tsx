import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { BRAND } from "../lib/brand";

interface Props {
  /** Person's name (e.g., "Graeham Watts") */
  name: string;
  /** Role/contact line (e.g., "Intero Real Estate · Peninsula") */
  role: string;
  /** Optional CTA text on the right side (e.g., "Comment OPTIONS below") */
  cta?: string;
  /** Width: "full" (entire width) or "twoThirds" (default — leaves negative space) */
  width?: "full" | "twoThirds";
}

export const EndCard: React.FC<Props> = ({
  name,
  role,
  cta,
  width = "twoThirds",
}) => {
  const frame = useCurrentFrame();

  // Slide up + opacity fade in
  const opacity = interpolate(
    frame,
    [0, BRAND.animation.largeFadeIn],
    [0, 1],
    { extrapolateRight: "clamp" }
  );
  const translateY = interpolate(
    frame,
    [0, BRAND.animation.largeFadeIn],
    [40, 0],
    { extrapolateRight: "clamp" }
  );

  const cardWidth = width === "full" ? "100%" : "66.67%";

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "flex-start",
        padding: "0 0 80px 80px",
      }}
    >
      <div
        style={{
          backgroundColor: BRAND.colors.panelFill,
          width: cardWidth,
          padding: "24px 48px",
          position: "relative",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 40,
          opacity,
          transform: `translateY(${translateY}px)`,
        }}
      >
        {/* Top accent stroke — full width */}
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            right: 0,
            height: BRAND.spacing.accentStroke,
            backgroundColor: BRAND.colors.generalAccent,
          }}
        />

        {/* Left: name + role */}
        <div>
          <div
            style={{
              fontFamily: BRAND.fonts.display,
              fontSize: BRAND.sizes.nameLabel,
              fontWeight: 700,
              color: BRAND.colors.white,
              lineHeight: 1.1,
            }}
          >
            {name}
          </div>
          <div
            style={{
              fontFamily: BRAND.fonts.body,
              fontSize: BRAND.sizes.roleLabel,
              fontWeight: 400,
              color: BRAND.colors.labelMuted,
              marginTop: 4,
            }}
          >
            {role}
          </div>
        </div>

        {/* Right: optional CTA */}
        {cta && (
          <div
            style={{
              fontFamily: BRAND.fonts.body,
              fontSize: 16,
              fontWeight: 600,
              letterSpacing: BRAND.tracking.eyebrow,
              textTransform: "uppercase",
              color: BRAND.colors.generalAccent,
              textAlign: "right",
            }}
          >
            {cta}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
