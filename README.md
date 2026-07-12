# Unity Meshy Studio

An independent Claude skill for building polished Unity projects and
orchestrating Meshy generation, refinement, rigging, animation, download,
Unity import, prefab creation, and validation.

> Not affiliated with or endorsed by Unity Technologies, Anthropic, Claude,
> or Meshy.

## Distribution formats

This archive is the **Claude Code plugin** distribution.

Load it for a session with a recent Claude Code release:

```bash
claude --plugin-dir ./unity-meshy-studio-plugin
```

The skill is invoked as:

```text
/unity-meshy-studio:unity-meshy-studio
```

The plugin bundles Meshy's MCP server declaration. Export `MESHY_API_KEY`
before starting Claude Code.

## Meshy sign-in and API authentication

Meshy's public developer API uses API keys. This package does not request or
store a Meshy password.

The guided helper:

1. Opens Meshy in the browser for account sign-in.
2. Opens Meshy's API settings.
3. Prompts for an API key without echoing it.
4. Verifies the key against the balance endpoint.
5. Stores it through the operating-system credential store when available.

```bash
python -m venv .venv
python -m pip install -r tools/requirements.txt
python tools/meshy_auth.py login
```

The `MESHY_API_KEY` environment variable takes precedence over credential-store
values.

## Credit safety

Every REST operation that can consume credits requires:

```text
--confirm-spend
```

The tool also displays the operation and current balance before submission.
Claude must obtain the user's explicit approval before running refine, rig,
animation, remesh, retexture, image-to-3D, multi-image-to-3D, or any other
credit-consuming operation.

Preview generation also consumes credits and is gated.

## Examples

Check authentication:

```bash
python tools/meshy_auth.py status
python tools/meshy_client.py balance
```

Create a preview:

```bash
python tools/meshy_client.py text-to-3d-preview   --prompt "A single stylized stone golem, neutral pose, game-ready"   --confirm-spend
```

Refine a completed preview:

```bash
python tools/meshy_client.py text-to-3d-refine   --preview-task-id TASK_ID   --confirm-spend
```

Poll and download:

```bash
python tools/meshy_client.py wait --kind text-to-3d --id TASK_ID
python tools/meshy_client.py download   --kind text-to-3d   --id TASK_ID   --output Assets/Art/Generated/Meshy/StoneGolem
```

## Optional Meshy MCP server

Meshy's MCP package reads `MESHY_API_KEY` from the environment:

```bash
python tools/configure_claude_mcp.py
```

The configuration references the environment variable and does not embed the
secret.

## Unity installation

Copy `Assets`, `Docs`, and `tools` into the Unity project root. Generated
assets are organized beneath:

```text
Assets/Art/Generated/Meshy/<AssetName>/
```

Always review generated models, rig mappings, materials, scale, colliders,
LODs, animation loops, and performance in the target Unity version.

## License

MIT. See `LICENSE`, `NOTICE.md`, `SECURITY.md`, and `DEPENDENCIES.md`.


## Included specialist skills

Architecture, gameplay, UI polish, scenes and lighting, performance, animation,
shaders and materials, audio, testing and CI, release readiness, Meshy asset
direction, Meshy-to-Unity importing, and the main orchestrator.

## Validate before publishing

```bash
python tools/validate_release.py
```

See `PUBLISHING.md` and `CONTRIBUTING.md`.
