---
name: unity-architecture
description: Design or repair Unity project architecture, assembly definitions, namespaces, data boundaries, serialization, dependency flow, and maintainable folder structure.
---
# Unity Architecture

Inspect existing conventions before proposing changes. Preserve serialized field
names or use `FormerlySerializedAs` when migration is needed.

Prefer:
- cohesive feature folders over arbitrary type folders when established structure permits
- assembly definitions with intentional references
- ScriptableObjects for authored reusable data
- plain C# services for logic that does not require a Unity lifecycle
- explicit composition roots
- event ownership and reliable unsubscription
- interfaces only where they reduce coupling or enable tests

Avoid:
- global mutable state
- hidden scene searches
- service locator sprawl
- circular assembly references
- massive manager classes
- public fields used as an API
- domain logic embedded in UI callbacks

For a refactor, document old-to-new ownership, migration risks, prefab/scene
serialization impact, and rollback strategy.
