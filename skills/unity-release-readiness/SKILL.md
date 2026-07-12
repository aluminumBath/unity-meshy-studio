---
name: unity-release-readiness
description: Audit a Unity project for release, licensing, secrets, settings, builds, crash risks, store requirements, documentation, and source-control cleanliness.
---
# Unity Release Readiness

Audit:
- supported Unity version and package lock
- target platform player settings
- scripting backend and architectures
- scenes in build
- development flags and debug symbols
- secrets and service credentials
- license compatibility of code and assets
- privacy, analytics, permissions, and network disclosures
- save migration and backward compatibility
- crash logging and safe failure behavior
- build reproducibility
- repository size and ignored generated folders
- user-facing credits and third-party notices

Produce blockers, high-risk issues, recommendations, and a go/no-go summary.
