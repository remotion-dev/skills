import React, { useState, useEffect } from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
  staticFile,
  delayRender,
  continueRender,
} from "remotion";
import { GoldText3D } from "./GoldText3D";
import { CURSIVE_FONTS, CursiveFontKey, BODY_FONTS, BodyFontKey } from "../fonts";
import { loadTypeface, measureTextWidth } from "../measureText";
import {
  visibleWorldWidth,
  GOLD_FONT_SIZE,
  GOLD_FONTS,
  GoldFontKey,
  GoldVariantKey,
} from "../layout";

export type SpacingMode = "balanced" | "snug" | "touching";

export type TitleProps = {
  cursiveLine: string;
  goldLine: string;
  /** optional flat bold line below the gold - e.g. a phone number */
  thirdLine?: string;
  /** when true: everything static - no entrance, no sway, no fade */
  frozen?: boolean;
  /** how close the cursive line sits to the gold text */
  spacingMode?: SpacingMode;
  /** which 3D font to extrude for the gold line */
  goldFont?: GoldFontKey;
  /** which gold-chrome material preset */
  goldVariant?: GoldVariantKey;
  /** which cursive font for the top line */
  cursiveFont?: CursiveFontKey;
  /** which flat sans family for the third line */
  bodyFont?: BodyFontKey;
};

// cursiveTop / thirdLineTop = vertical position as % of frame height.
// goldShiftY = how far the 3D canvas is nudged down (% of height).
const SPACING: Record<
  SpacingMode,
  {
    landscape: { cursiveTop: number; goldShiftY: number; thirdLineTop: number };
    portrait: { cursiveTop: number; goldShiftY: number; thirdLineTop: number };
  }
> = {
  balanced: {
    landscape: { cursiveTop: 30, goldShiftY: 2, thirdLineTop: 63 },
    portrait: { cursiveTop: 34, goldShiftY: 0, thirdLineTop: 56 },
  },
  snug: {
    landscape: { cursiveTop: 34, goldShiftY: 1, thirdLineTop: 62 },
    portrait: { cursiveTop: 37, goldShiftY: -1, thirdLineTop: 55 },
  },
  touching: {
    landscape: { cursiveTop: 39, goldShiftY: 3, thirdLineTop: 64 },
    portrait: { cursiveTop: 42, goldShiftY: 1, thirdLineTop: 57 },
  },
};

export const Title: React.FC<TitleProps> = ({
  cursiveLine,
  goldLine,
  thirdLine,
  frozen = false,
  spacingMode = "balanced",
  goldFont = "archivo-black",
  goldVariant = "bright-chrome",
  cursiveFont = "sacramento",
  bodyFont = "archivo",
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height, durationInFrames } = useVideoConfig();
  const isPortrait = height > width;

  // ----- layout / sizing per orientation -----
  // cursive + third line sized up so they hold their own next to the gold
  const cursiveFontPx = isPortrait ? 118 : 132;
  const thirdFontPx = isPortrait ? 90 : 108;
  const cameraZ = isPortrait ? 11 : 9;
  const fillFactor = isPortrait ? 0.86 : 0.84; // fraction of frame width text fills
  const maxScale = 2.4; // cap so a short word like "SOLD" doesn't get huge

  const spacing = SPACING[spacingMode][isPortrait ? "portrait" : "landscape"];
  const cursiveTop = `${spacing.cursiveTop}%`;
  const thirdLineTop = `${spacing.thirdLineTop}%`;
  const goldShiftY = `${spacing.goldShiftY}%`;

  const cursiveFamily = CURSIVE_FONTS[cursiveFont].family;
  const bodyFamily = BODY_FONTS[bodyFont].family;
  const goldFontFile = GOLD_FONTS[goldFont].file;

  // ----- measure the gold text + compute its fit scale (deterministic) -----
  const [fitScale, setFitScale] = useState<number | null>(null);
  const [measureHandle] = useState(() =>
    delayRender("Measuring gold text width")
  );

  useEffect(() => {
    let cancelled = false;
    loadTypeface(staticFile(goldFontFile))
      .then((font) => {
        if (cancelled) return;
        const naturalWidth = measureTextWidth(font, goldLine, GOLD_FONT_SIZE);
        const targetWidth =
          visibleWorldWidth(cameraZ, width, height) * fillFactor;
        let scale = naturalWidth > 0 ? targetWidth / naturalWidth : 1;
        if (scale > maxScale) scale = maxScale;
        setFitScale(scale);
        continueRender(measureHandle);
      })
      .catch(() => {
        if (cancelled) return;
        setFitScale(1);
        continueRender(measureHandle);
      });
    return () => {
      cancelled = true;
    };
  }, [
    goldLine,
    goldFontFile,
    cameraZ,
    width,
    height,
    fillFactor,
    maxScale,
    measureHandle,
  ]);

  // ----- entrance + exit animation -----
  // Pop-in: a scale spring with overshoot + a fast opacity ramp.
  // 2-second (60-frame) stagger between line 1, line 2, line 3.
  const popIn = (delayFrames: number) => {
    if (frozen) return { scale: 1, opacity: 1 };
    const scale = spring({
      frame: frame - delayFrames,
      fps,
      config: { damping: 11, mass: 0.6, stiffness: 130 },
      durationInFrames: 26,
    });
    const opacity = interpolate(frame - delayFrames, [0, 5], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    return { scale, opacity };
  };

  const cursivePop = popIn(0); // line 1 - 0s
  const goldPop = popIn(60); // line 2 - 2s
  const thirdPop = popIn(120); // line 3 - 4s

  // Fade-out: all three lines fade together over the last ~24 frames.
  const fadeOut = frozen
    ? 1
    : interpolate(frame, [durationInFrames - 24, durationInFrames], [1, 0], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });

  return (
    <AbsoluteFill>
      {/* ---- 3D gold layer (full-frame canvas, nudged down) ---- */}
      <AbsoluteFill
        style={{
          transform: `translateY(${goldShiftY})`,
          opacity: goldPop.opacity * fadeOut,
        }}
      >
        {fitScale !== null && (
          <GoldText3D
            text={goldLine}
            width={width}
            height={height}
            cameraZ={cameraZ}
            fitScale={fitScale}
            entryScale={goldPop.scale}
            goldFont={goldFont}
            goldVariant={goldVariant}
          />
        )}
      </AbsoluteFill>

      {/* ---- flat cursive layer, on top ---- */}
      <AbsoluteFill
        style={{ justifyContent: "flex-start", alignItems: "center" }}
      >
        <div
          style={{
            position: "absolute",
            top: cursiveTop,
            fontFamily: cursiveFamily,
            fontSize: cursiveFontPx,
            lineHeight: 1,
            color: "#ffffff",
            opacity: cursivePop.opacity * fadeOut,
            transform: `scale(${cursivePop.scale})`,
            textShadow: "0 4px 20px rgba(0,0,0,0.45)",
            whiteSpace: "nowrap",
            letterSpacing: "0.5px",
          }}
        >
          {cursiveLine}
        </div>

        {/* ---- flat bold third line, below the gold ---- */}
        {thirdLine && (
          <div
            style={{
              position: "absolute",
              top: thirdLineTop,
              fontFamily: bodyFamily,
              fontWeight: 800,
              fontSize: thirdFontPx,
              lineHeight: 1,
              color: "#ffffff",
              opacity: thirdPop.opacity * fadeOut,
              transform: `scale(${thirdPop.scale})`,
              textShadow: "0 4px 18px rgba(0,0,0,0.5)",
              whiteSpace: "nowrap",
              letterSpacing: "2px",
            }}
          >
            {thirdLine}
          </div>
        )}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
