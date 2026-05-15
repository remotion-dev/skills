import { Config } from "@remotion/cli/config";

// CRITICAL: PNG image format = the rendered frames carry an alpha channel.
// Without this line the background renders solid white. Do not remove it.
Config.setVideoImageFormat("png");

Config.setOverwriteOutput(true);
