import React from "react";
import { AbsoluteFill } from "remotion";
import { BODY_FONTS, BodyFontKey } from "../fonts";

// A flat (non-3D) sample card showing one sans family doing the two jobs
// it would do in real videos: chunky burned-in title text, and plain
// readable body text. Rendered on transparent bg like everything else.

export type FontSampleProps = {
  bodyFont: BodyFontKey;
};

export const FontSample: React.FC<FontSampleProps> = ({ bodyFont }) => {
  const family = BODY_FONTS[bodyFont].family;

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        fontFamily: family,
      }}
    >
      <div style={{ textAlign: "center", color: "#ffffff" }}>
        {/* chunky title weight */}
        <div
          style={{
            fontWeight: 800,
            fontSize: 150,
            letterSpacing: "1px",
            lineHeight: 1,
            textShadow: "0 6px 24px rgba(0,0,0,0.45)",
          }}
        >
          JUST LISTED
        </div>

        {/* medium sub-line */}
        <div
          style={{
            fontWeight: 500,
            fontSize: 58,
            marginTop: 36,
            textShadow: "0 4px 18px rgba(0,0,0,0.45)",
          }}
        >
          Open House — Saturday 1 to 4 PM
        </div>

        {/* regular body line */}
        <div
          style={{
            fontWeight: 400,
            fontSize: 44,
            marginTop: 24,
            opacity: 0.92,
            textShadow: "0 4px 16px rgba(0,0,0,0.45)",
          }}
        >
          1247 Pulgas Avenue, East Palo Alto — Offered at $1,295,000
        </div>
      </div>
    </AbsoluteFill>
  );
};
