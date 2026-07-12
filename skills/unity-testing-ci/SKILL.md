---
name: unity-testing-ci
description: Add and repair Unity EditMode, PlayMode, integration, build, and CI tests with deterministic fixtures and actionable diagnostics.
---
# Unity Testing and CI

Select the smallest test layer that proves the behavior.

- EditMode for pure logic, import utilities, and editor tooling
- PlayMode for lifecycle, scene, physics, UI, animation, and integration behavior
- build smoke tests for player-specific compilation and startup
- batchmode-safe test setup
- deterministic clocks, seeds, and fixtures
- cleanup of created scenes, objects, assets, and static state

Do not make tests pass by weakening assertions or skipping genuine failures.
Report exact commands and test results.
