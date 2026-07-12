---
name: unity-performance
description: Diagnose and improve Unity CPU, GPU, memory, loading, rendering, physics, UI, and mobile performance without speculative optimization.
---
# Unity Performance

Measure before changing. Identify target device, frame budget, memory budget,
scene complexity, and reproduction path.

Inspect:
- Update/LateUpdate/FixedUpdate volume
- managed allocations and LINQ in hot paths
- repeated object searches and component lookups
- draw calls, batching, instancing, overdraw, and transparency
- texture dimensions, formats, mipmaps, and streaming
- mesh density, skinning, blend shapes, and LODs
- physics layers, collision matrix, and fixed timestep
- canvas rebuilds or UI Toolkit invalidation
- Addressables, scene loading, and asset lifetime
- shader variants and build size

Document measured evidence, change, expected effect, and regression risk.
