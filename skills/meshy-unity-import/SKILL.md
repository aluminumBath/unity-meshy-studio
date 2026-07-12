---
name: meshy-unity-import
description: Import Meshy models, textures, rigs, and animations into Unity; create wrapper prefabs, materials, colliders, LODs, Animator setup, and validation reports.
---
# Meshy Unity Import

Store source and authored outputs separately:

Assets/Art/Generated/Meshy/<AssetName>/
- Source
- Models
- Textures
- Materials
- Animations
- Prefabs
- Metadata

Validate:
- units, scale, pivot, forward/up axes
- normals, tangents, UVs, and PBR texture types
- material pipeline compatibility
- model compression and Read/Write
- Humanoid avatar or Generic root
- root motion and loop settings
- colliders, Rigidbody, navigation, and interaction points
- LODGroup and shadow settings
- missing dependencies and prefab references

Never attach gameplay code directly to the imported model asset. Create an
authored wrapper prefab.
