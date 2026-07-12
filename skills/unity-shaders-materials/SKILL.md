---
name: unity-shaders-materials
description: Create and repair Unity materials, Shader Graphs, custom shaders, texture assignments, PBR channels, render queues, and pipeline migrations.
---
# Unity Shaders and Materials

Detect the render pipeline and target hardware.

Verify:
- base color color-space assumptions
- normal map import type
- metallic, roughness/smoothness, AO, emission, and mask packing
- transparency mode and render queue
- double-sided requirements
- GPU instancing compatibility
- shader variant growth
- mobile fallback and precision
- SRP Batcher compatibility when applicable
- missing or pink materials after pipeline conversion

Do not duplicate materials unnecessarily. Prefer explicit material ownership.
