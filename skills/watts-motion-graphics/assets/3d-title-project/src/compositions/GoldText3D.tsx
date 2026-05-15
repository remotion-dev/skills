import React, { useMemo } from "react";
import { staticFile } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import { Center, Text3D } from "@react-three/drei";
import { useThree } from "@react-three/fiber";
import * as THREE from "three";
import { RoomEnvironment } from "three/examples/jsm/environments/RoomEnvironment.js";
import {
  CAMERA_FOV,
  GOLD_FONT_SIZE,
  GOLD_FONTS,
  GoldFontKey,
  GOLD_VARIANTS,
  GoldVariantKey,
} from "../layout";

// Procedural studio environment so the metal has real reflections to catch.
const StudioEnvironment: React.FC<{ intensity: number }> = ({ intensity }) => {
  const { gl, scene } = useThree();
  useMemo(() => {
    const pmrem = new THREE.PMREMGenerator(gl);
    const env = pmrem.fromScene(new RoomEnvironment(), 0.02);
    scene.environment = env.texture;
    scene.environmentIntensity = intensity; // three r150+ : scales the IBL
    return env;
  }, [gl, scene, intensity]);
  return null;
};

type SceneProps = {
  text: string;
  fitScale: number;
  /** entrance scale 0..~1.1, driven by Title's pop-in spring (1 = settled) */
  entryScale: number;
  goldFontFile: string;
  variant: GoldVariantKey;
};

const Scene: React.FC<SceneProps> = ({
  text,
  fitScale,
  entryScale,
  goldFontFile,
  variant,
}) => {
  const v = GOLD_VARIANTS[variant];
  const groupScale = fitScale * entryScale;

  return (
    <>
      <StudioEnvironment intensity={v.envMapIntensity} />

      {/* High-contrast warm rig: a dominant top-front key gives the bright
          top faces, low fill lets the side faces fall into deep amber -
          that top-bright / side-dark split is what reads as rich gold. */}
      <directionalLight position={[4, 9, 6]} intensity={5.0} color={"#fff3d0"} />
      <directionalLight position={[-5, 4, -6]} intensity={2.0} color={"#ffd98a"} />
      <pointLight position={[0, 1, 8]} intensity={1.1} color={"#fff0cc"} />
      <ambientLight intensity={0.25} color={"#2a1d0a"} />

      <group scale={groupScale}>
        <Center>
          <Text3D
            font={staticFile(goldFontFile)}
            size={GOLD_FONT_SIZE}
            height={GOLD_FONT_SIZE * 0.4}
            bevelEnabled
            bevelThickness={GOLD_FONT_SIZE * 0.09}
            bevelSize={GOLD_FONT_SIZE * 0.04}
            bevelSegments={8}
            curveSegments={10}
          >
            {text}
            <meshStandardMaterial
              color={v.color}
              metalness={v.metalness}
              roughness={v.roughness}
              envMapIntensity={v.envMapIntensity}
              emissive={v.emissive}
              emissiveIntensity={v.emissiveIntensity}
            />
          </Text3D>
        </Center>
      </group>
    </>
  );
};

export type GoldText3DProps = {
  text: string;
  width: number;
  height: number;
  cameraZ: number;
  /** pre-computed in Title from the font metrics - fits text to frame width */
  fitScale: number;
  /** entrance scale from Title's pop-in spring; pass 1 for a static frame */
  entryScale: number;
  /** which 3D font to extrude */
  goldFont: GoldFontKey;
  /** which gold-chrome material preset */
  goldVariant: GoldVariantKey;
};

export const GoldText3D: React.FC<GoldText3DProps> = ({
  text,
  width,
  height,
  cameraZ,
  fitScale,
  entryScale,
  goldFont,
  goldVariant,
}) => {
  return (
    <ThreeCanvas
      width={width}
      height={height}
      camera={{ position: [0, 0, cameraZ], fov: CAMERA_FOV }}
      gl={{
        alpha: true,
        antialias: true,
        toneMapping: THREE.ACESFilmicToneMapping,
        toneMappingExposure: GOLD_VARIANTS[goldVariant].exposure,
      }}
    >
      <Scene
        text={text}
        fitScale={fitScale}
        entryScale={entryScale}
        goldFontFile={GOLD_FONTS[goldFont].file}
        variant={goldVariant}
      />
    </ThreeCanvas>
  );
};
