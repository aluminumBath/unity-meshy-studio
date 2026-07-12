# Changelog

## 1.2.0 — 2026-07-12

- The fallback REST client now covers the full Meshy pipeline: `image-to-3d`
  (single or multi-image via URL, data URI, or local file), `remesh`,
  `retexture`, `rig`, and `animate` (with optional FPS post-processing), all
  behind the same `--confirm-spend` gate and tested against the live API.
- Downloads handle nested rigging/animation result payloads and skip the
  empty URL strings Meshy returns for formats a task did not produce.
- API errors now include Meshy's response detail (for example rigging's
  "Pose estimation failed") instead of a bare HTTP status.

## 1.1.4 — 2026-07-12

- Rewrote the README around the marketplace install, with a real example run
  (credits, timing, output files), the stone golem preview image, and a
  troubleshooting section.
- Tightened the plugin and marketplace descriptions and CONTRIBUTING.

## 1.1.3 — 2026-07-12

- Downloads are now named after the output directory (for example
  `StoneGolem.glb`) instead of the format key (`glb.glb`).
- The task thumbnail is downloaded alongside the model files and skipped
  gracefully if unavailable.

## 1.1.2 — 2026-07-12

- Fixed editor-script compile errors on Unity 6: replaced the removed
  `ModelImporter.importMaterials` with `materialImportMode` and the deprecated
  `optimizeMeshPolygons`/`optimizeMeshVertices` with `meshOptimizationFlags`.
- Verified end-to-end in a clean Unity 6000.0.77f1 project: Meshy FBX import,
  material and missing-script checks, prefab creation, and health scan.

## 1.1.1 — 2026-07-12

- Added the `.claude-plugin/marketplace.json` manifest so the repository can
  be added directly as a Claude Code plugin marketplace.
- Removed a stray embedded `repo/` directory left over from the layout fix.

## 1.1.0 — 2026-07-12

- Split the plugin into 13 focused skills.
- Added four specialist review agents.
- Added non-mutating Unity edit reminders through a plugin hook.
- Added scene, texture, and generated-prefab health scanners.
- Added release validation, contribution guidance, and publishing checklist.
- Added marketplace packaging.
- Preserved explicit Meshy credit approval and credential safeguards.

## 1.0.0 — 2026-07-12

- Initial public standalone skill and Claude Code plugin release.
