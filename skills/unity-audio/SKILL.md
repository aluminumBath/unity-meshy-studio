---
name: unity-audio
description: Implement and polish Unity audio architecture, mixers, spatial sound, music transitions, ambience, pooling, ducking, and accessibility.
---
# Unity Audio

Use AudioMixer groups for meaningful categories and snapshots where appropriate.

Define:
- spatial versus non-spatial playback
- attenuation and doppler policy
- pooling and voice limits
- music transition rules
- pause behavior
- UI, dialogue, ambience, music, and effects routing
- ducking and priority
- subtitle/caption hooks
- user volume settings and persistence

Avoid spawning unbounded AudioSources or clipping through excessive gain.
