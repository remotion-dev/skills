// Watts Motion Graphics — Timings Template
// Copy this file to src/lib/timings.ts in your project, then populate with real frame numbers
// after rendering audio in ElevenLabs and running Whisper transcription.
//
// Anchor rule: Each timing is associated with a SPOKEN PHRASE, not a wall-clock timestamp.
// Phrases are stable across re-renders; timestamps drift.
//
// Conversion: frame = Math.round(seconds_from_whisper * 30)

import { FPS } from "./brand";

/**
 * Each entry maps a graphic to:
 * - anchorPhrase: the spoken phrase the graphic should appear under
 * - startFrame: the frame at which it appears (placeholder, replace after Whisper)
 * - holdSeconds: how long it stays on screen
 */
export interface GraphicTiming {
  id: string;
  template: "stat" | "compare" | "framework" | "hero" | "endcard";
  anchorPhrase: string; // The phrase from the script the graphic anchors to
  startFrame: number;
  holdSeconds: number;
  note?: string;
}

// PLACEHOLDER TIMINGS — UPDATE AFTER AUDIO RENDERS
// Speech pace estimate: ~150 wpm = ~2.5 wps = ~75 frames/word at 30fps
export const TIMINGS: GraphicTiming[] = [
  // EXAMPLE — replace with real graphics for your video
  // {
  //   id: "MG-01",
  //   template: "stat",
  //   anchorPhrase: "Meta just announced eight thousand global layoffs",
  //   startFrame: 600, // PLACEHOLDER — find "eight thousand" in Whisper transcript
  //   holdSeconds: 4,
  //   note: "Top of Scene 1, hook reinforcement",
  // },
  // {
  //   id: "MG-14",
  //   template: "hero",
  //   anchorPhrase: "tax-free",
  //   startFrame: 7500, // PLACEHOLDER — find "tax-free" in Scene 5
  //   holdSeconds: 6,
  //   note: "HERO — music drops to silence at this trigger",
  // },
];

/** Total composition duration in frames — calculated from script length */
export const TOTAL_DURATION_FRAMES = 30 * FPS * 11; // 5:30 default — update for your video

/** Helper to convert seconds to frames at the project framerate */
export const sec = (seconds: number): number => Math.round(seconds * FPS);
