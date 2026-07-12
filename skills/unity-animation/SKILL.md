---
name: unity-animation
description: Build and validate Unity Animator, Animation Rigging, avatars, root motion, state machines, blend trees, transitions, IK, and imported clips.
---
# Unity Animation

Validate avatar mapping and source rig before building controllers.

Check:
- Humanoid versus Generic choice
- root node and root motion ownership
- clip ranges, loop pose, foot IK, and cycle offset
- transition interruption and exit-time behavior
- parameter naming and write ownership
- foot sliding, contact stability, clipping, and joint collapse
- Animator layer masks and additive assumptions
- animation events and duplicated callbacks
- network or save-state implications

Avoid controllers with uncontrolled Any State transitions and ambiguous
parameters written from many systems.
