---
name: unity-gameplay-systems
description: Implement polished Unity gameplay systems such as interaction, inventory, quests, combat, AI, saves, spawning, cameras, vehicles, and input.
---
# Unity Gameplay Systems

Build a complete player-facing slice with configuration, runtime behavior,
feedback, persistence implications, tests, and debugging support.

Requirements:
- match the active Input System
- separate authored values from runtime state
- use deterministic state transitions where practical
- guard against duplicate subscriptions and repeated initialization
- define interruption, cancellation, death, reload, and scene-change behavior
- expose useful diagnostics without logging every frame
- include clear audiovisual feedback hooks
- test happy paths and important failure paths

For save data, version the schema and never serialize direct scene references.
For AI, define perception, decisions, movement, recovery, and stuck behavior.
