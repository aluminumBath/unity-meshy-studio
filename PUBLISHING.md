# Publishing checklist

## GitHub release

- Run `python tools/validate_release.py`.
- Test local loading with `claude --plugin-dir <plugin-directory>`.
- Test Meshy authentication with a disposable or restricted API key.
- Test one approved preview task and immediately download its output.
- Import a sample asset into a clean Unity project.
- Confirm no missing scripts, materials, textures, or broken avatars.
- Tag `v1.1.0`.
- Attach the plugin ZIP and standalone skill ZIP to the release.
- Include the changelog and third-party notices.

## Marketplace

Publish the repository and update the marketplace entry source URL. Users can
add the marketplace and install the namespaced plugin through Claude Code's
plugin manager.

## Before every release

Review current Anthropic plugin schemas, Meshy API endpoints and pricing, and
the supported Unity versions. These external interfaces can change.
