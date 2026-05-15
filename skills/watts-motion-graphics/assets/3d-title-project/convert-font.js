// Converts a .woff / .ttf font into the typeface.json format that
// Three.js TextGeometry / drei <Text3D> requires.
//
// Logic mirrors facetype.js (the canonical converter): command order and
// the control-point-after-endpoint quirk are what Three.js's typeface
// parser expects. Get those wrong and glyphs render garbled.

const fs = require("fs");
const path = require("path");
const opentype = require("opentype.js");

// characters we actually need - uppercase, lowercase, digits, common punctuation
const CHARSET =
  "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,!?&'\"-:";

function convert(fontPath, outPath) {
  const font = opentype.loadSync(fontPath);
  const unitsPerEm = font.unitsPerEm || 1000;
  // facetype.js scale: normalises every font to a 1000-unit resolution
  const scale = (1000 * 100) / (unitsPerEm * 72);

  const result = {
    glyphs: {},
    familyName: (font.names.fontFamily && font.names.fontFamily.en) || "Font",
    ascender: Math.round(font.ascender * scale),
    descender: Math.round(font.descender * scale),
    underlinePosition: Math.round((font.tables.post.underlinePosition || 0) * scale),
    underlineThickness: Math.round((font.tables.post.underlineThickness || 0) * scale),
    boundingBox: {
      yMin: Math.round(font.tables.head.yMin * scale),
      xMin: Math.round(font.tables.head.xMin * scale),
      yMax: Math.round(font.tables.head.yMax * scale),
      xMax: Math.round(font.tables.head.xMax * scale),
    },
    resolution: 1000,
    original_font_information: font.tables.name,
  };

  for (const ch of CHARSET) {
    const glyph = font.charToGlyph(ch);
    if (!glyph) continue;
    const token = {
      ha: Math.round(glyph.advanceWidth * scale),
      x_min: 0,
      x_max: 0,
      o: "",
    };
    const bb = glyph.getBoundingBox();
    token.x_min = Math.round(bb.x1 * scale);
    token.x_max = Math.round(bb.x2 * scale);

    const cmds = glyph.path.commands;
    for (const command of cmds) {
      let type = command.type.toLowerCase();
      if (type === "c") type = "b"; // cubic bezier
      token.o += type + " ";
      // IMPORTANT: endpoint (x,y) is emitted BEFORE the control points,
      // which is the order Three.js's typeface parser reads.
      if (command.x !== undefined && command.y !== undefined) {
        token.o += Math.round(command.x * scale) + " " + Math.round(command.y * scale) + " ";
      }
      if (command.x1 !== undefined && command.y1 !== undefined) {
        token.o += Math.round(command.x1 * scale) + " " + Math.round(command.y1 * scale) + " ";
      }
      if (command.x2 !== undefined && command.y2 !== undefined) {
        token.o += Math.round(command.x2 * scale) + " " + Math.round(command.y2 * scale) + " ";
      }
    }
    result.glyphs[ch] = token;
  }

  fs.writeFileSync(outPath, JSON.stringify(result));
  const n = Object.keys(result.glyphs).length;
  console.log(`  ${path.basename(outPath)} - ${n} glyphs, unitsPerEm ${unitsPerEm}`);
}

// usage: node convert-font.js <input.woff> <output.typeface.json>
const [, , inPath, outPath] = process.argv;
if (!inPath || !outPath) {
  console.error("usage: node convert-font.js <input> <output>");
  process.exit(1);
}
convert(inPath, outPath);
